---
name: narrator-ai-cli
version: "1.0.5"
license: MIT
description: >-
  AI 电影/短剧解说视频自动生成（AI 解说大师 CLI Skill）。当用户需要创建电影解说视频、短剧解说、影视二创、AI 配音旁白视频、film commentary、video narration、drama dubbing、movie narration 时触发。内置电影素材库、BGM、多语种配音、解说模板。通过 narrator-ai-cli 命令行实现：搜片→选模板→选 BGM→选配音→生成文案→合成视频的全流程自动化。CLI client for Narrator AI video narration API.
user-invocable: true
tags:
  - video-narration
  - film-commentary
  - ai-video
  - short-drama
  - content-creation
  - dubbing
  - tts
  - video-production
metadata:
  openclaw:
    emoji: "🎬"
    primaryEnv: NARRATOR_APP_KEY
    install:
      - name: narrator-ai-cli
        type: pip
        spec: "narrator-ai-cli @ https://github.com/NarratorAI-Studio/narrator-ai-cli/archive/refs/tags/v1.0.0.zip"
    requires:
      bins:
        - narrator-ai-cli
      env:
        - NARRATOR_APP_KEY
---
# narrator-ai-cli — AI Video Narration CLI Skill
CLI client for [Narrator AI](https://openapi.jieshuo.cn) video narration API. Designed for AI agents and developers.
- **CLI repo**: https://github.com/NarratorAI-Studio/narrator-ai-cli
- **Resources preview** (BGM / dubbing / templates): https://ceex7z9m67.feishu.cn/wiki/WLPnwBysairenFkZDbicZOfKnbc
## Reference Index
This file covers decision flow, the common workflow, and pointers. Detailed lookups live in `references/`:
| Topic | File |
|---|---|
| Resource selection (material / BGM / dubbing / templates) — list commands, response formats, field mapping | `references/resources.md` |
| Full workflow steps with parameter tables and JSON examples (Fast Path + Standard Path) | `references/workflows.md` |
| Magic Video — optional visual template step (catalog, params, language rules) | `references/magic-video.md` |
| Polling pattern, task types, file ops, user account, error codes | `references/operations.md` |
## Pipeline at a Glance
```
                    ┌─── Fast Path (原创文案, cheaper) ───┐
                    │   fast-writing → fast-clip-data     │
  Source material ──┤              ↓                      ├──→ video-composing ──→ (magic-video)
  (material list /  │   [video-composing keys off         │   final MP4 URL       optional visual
   search-movie /   │    fast-clip-data.task_order_num]   │                        template pass
   file upload)     └─────────────────────────────────────┘
                    ┌─── Standard Path (二创文案) ────────┐
                    │   popular-learning → generate-      │
                    │   writing → clip-data               │
                    │              ↓                      │
                    │   [video-composing keys off         │
                    │    generate-writing.task_order_num] │
                    └─────────────────────────────────────┘
```
## Agent Rules (mandatory — apply across all steps)
> **Always:**
> - **Confirm before acting.** Every resource (source, BGM, dubbing, template) and every `magic-video` submission requires explicit user approval. Never auto-select, never auto-submit.
> - **Source data, never invent.** Construct `confirmed_movie_json` from `material list` fields or `task search-movie` output. If neither yields it, ask the user — do not fabricate.
> - **Honor the language chain.** The dubbing voice's language defines the writing task `language` param AND every `magic-video` text param. All three must match. → `references/magic-video.md` § Language Awareness
> - **Paginate `material list` to exhaustion, search programmatically.** Fetch all pages until `total` is consumed, then `grep -i` or `python3 -c` on the JSON. Never trust truncated terminal display.
> - **Poll with the canonical `while` loop at 5-second intervals.** Never use a fixed-iteration `for` loop. → `references/operations.md` § Task Polling
>
> **Never:**
> - **Submit `magic-video` without showing the full request body** (templates + every `template_params` value) and getting user confirmation. The cost is 30 pts/minute and irreversible.
> - **Submit Chinese default values for `magic-video` text params when narration language is non-Chinese.** The defaults are hardcoded Chinese and will appear as Chinese text in a non-Chinese video.
> - **Submit `.task_id` (32-char hex) as `order_num`.** Downstream tasks want `.task_order_num` (the prefixed string like `generate_writing_xxxxx`), not `.task_id`. Submitting the hex returns `10001 任务关联记录数据异常`. The other look-alike — `.results.order_info.order_num` (`script_xxxxx`) — is also wrong; see `references/operations.md` § Task Query Response Shape.
> - **Auto-switch paths after a failure.** If a step fails, surface the error to the user and ask explicitly: retry the same path, switch to the other path, or abort. Never infer a path switch on the agent's own initiative.
## Prerequisites
This skill assumes the `narrator-ai-cli` binary is installed and configured with a valid `NARRATOR_APP_KEY`. See [README.md](README.md) for install / setup. Agents can verify with `narrator-ai-cli user balance`.
## Core Concepts
| Concept | Description |
|---|---|
| **file_id** | 32-char hex string for uploaded files. Via `file upload` or task results |
| **task_id** | 32-char hex string returned on task creation. Poll with `task query` |
| **task_order_num** | Assigned after task creation. Used as `order_num` for downstream tasks |
| **files[]** | Output files in the completed task response (flat, top-level array). Each entry has `file_id`, `file_path`, `suffix`. Read `.files[0].file_id` for the next step's input |
| **learning_model_id** | Narration style model — from a pre-built template (90+) or `popular-learning` result |
| **learning_srt** | Reference SRT file_id. **Mutually exclusive** with `learning_model_id` |
## Conversation Initiation
> ⚠️ **Agent behavior — first message of a session**: Before asking the user for a movie title or workflow path, **proactively orient them** about what the skill offers. Most users assume they need to upload their own video + SRT and don't realize a pre-built material library ships with the skill. Skipping this step often results in unnecessary uploads or aborted sessions.
**Required opening (adapt to the conversation language):**
1. **Lead with the pre-built material library.** Mention upfront that ~100 ready-to-use movies are available with video + SRT already loaded — no upload needed in most cases.
2. **Offer three concrete entry points** (let the user pick one):
   - "I have a specific movie in mind" → take the title, search materials first, fall back to `task search-movie` only if not found
   - "Show me what's available" → run `material list --json` and present 5–8 titles spanning varied genres; offer to filter by genre on request
   - "I'll upload my own video + SRT" → guide through `file upload`
3. **Defer the Fast vs Standard path question** until source material is confirmed. Asking both at once forces a decision the user has no context for yet.
4. **Optionally share the visual resources preview link** (BGM / dubbing / templates browsable visually): https://ceex7z9m67.feishu.cn/wiki/WLPnwBysairenFkZDbicZOfKnbc — but only if the user wants to browse, not as a wall of links upfront.
**Example opening (Chinese conversation):**
> 你好，欢迎使用 AI 解说大师。这个技能可以帮你生成电影/短剧解说视频。我这边内置了约 100 部电影素材（视频 + 字幕都是现成的），所以大多数情况你**不需要自己上传任何文件**。
>
> 你想怎么开始？
> 1. **直接告诉我片名** — 我先查内置素材库，没有再去外部搜
> 2. **让我列一些内置素材** — 你可以按类型挑（喜剧 / 动作 / 悬疑 / 科幻…）
> 3. **自己上传视频 + 字幕** — 我引导你完成上传流程
After source material is confirmed, walk the user through the **decision sequence below — one question per turn, in order**. Do NOT collapse multiple decisions into one message; users cannot reason about `target_mode` before they've picked a path.
**Decision sequence** (each step waits for explicit user confirmation):
1. **Source material** — covered above.
2. **Workflow path** — Fast (原创文案) or Standard (二创文案). See "Two Workflow Paths" below.
3. **`target_mode`** — *only ask if path = Fast*. Choose mode 1 / 2 / 3 (see "Fast Path internal: `target_mode`" below). If path = Standard, **skip this question entirely** — Standard Path has no `target_mode`.
4. **BGM** → **Dubbing voice** → **Narration template** — see "Resource Selection Protocol".
> ⚠️ **Anti-pattern (do NOT do this)**:
> Asking "① 解说模式 (纯解说/原声混剪) ② 制作路线 (快速/标准)" in the same message.
> `纯解说` and `原声混剪` are **Fast Path internal modes** (target_mode 1 vs 2). They do not exist in Standard Path. Asking them alongside the path choice forces the user to make decisions in the wrong order and conflates two layers of the decision tree.
## Two Workflow Paths
Two end-to-end paths produce a finished narrated video. Choose with the user before starting.
| | **Fast Path** (原创文案, recommended) | **Standard Path** (二创文案) |
|---|---|---|
| Pipeline | material → fast-writing → fast-clip-data → video-composing → magic-video* | material → popular-learning** → generate-writing → clip-data → video-composing → magic-video* |
| Cost / speed | Faster, cheaper | Higher quality narration |
| When to use | Default unless user wants adapted-style narration | When user wants narration learned from a reference style |
\* magic-video is optional; only on explicit user request.
\*\* popular-learning is skippable when using a pre-built template (recommended).
> ⚠️ **Path is a standalone decision** — ask the user "Fast or Standard?" by itself, in its own message. Do not auto-select. Do not bundle it with `target_mode` or any other follow-up question.
>
> ⚠️ **Path choice is per-movie, evaluated fresh each time.** If the user switched paths for a previous movie in the same session (e.g. from Fast to Standard due to a failure), that choice has no bearing on the current movie. Always ask the path question anew for each new movie — do not carry over or infer the prior session's path.
### Fast Path internal: `target_mode` (ask only after path=Fast is confirmed)
> Skip this section entirely if the user picked Standard Path — `target_mode` only exists inside fast-writing.
| Mode | Use when | Required input |
|---|---|---|
| `"1"` 热门影视 (纯解说) | Known movie, narration from plot only | `confirmed_movie_json`; **no `episodes_data`** |
| `"2"` 原声混剪 (Original Mix) | Known movie + you have its SRT | `confirmed_movie_json` + `episodes_data[{srt_oss_key, num}]` |
| `"3"` 冷门/新剧 (New Drama) | Obscure/new content | `episodes_data[{srt_oss_key, num}]`; `confirmed_movie_json` optional |
## Resource Selection Protocol
Before any task, gather these resources **in this order, with explicit user confirmation at each step**:
1. **Source files** (video + SRT) — from `material list` or via `file upload`
2. **BGM** — from `bgm list`
3. **Dubbing voice** — from `dubbing list`
4. **Narration style template** — from `task narration-styles`
Detailed list commands, response shapes, and field mappings live in `references/resources.md`.
> ⚠️ **Universal rules — apply at every resource step:**
> 1. **Pre-filter by context.** Use the per-resource filter flag where supported: `bgm list --search`, `dubbing list --lang`, `task narration-styles --genre`. **`material list` does NOT accept these flags** — paginate the JSON and search programmatically with `grep -i` / `python3 -c`.
> 2. **Default presentation: 5–8 options** with the resource ID and key descriptive fields.
> 3. **If the user has no preference**: present **3 recommendations** with a one-line reason for each. Still wait for confirmation.
> 4. **Confirm one resource at a time.** Do not advance until the current one is confirmed.
> ⚠️ **Dubbing → writing `language` mismatch check**: if the user pre-specified a `language` value that conflicts with the chosen voice, surface the mismatch and ask before proceeding. (The general language-chain rule lives in Agent Rules above.)
## Fast Path — High-Level Flow
> Detailed parameter tables, all `target_mode` cases, and full JSON examples live in `references/workflows.md`.
**Step 0 — Find source material & determine `target_mode`:**
1. List materials: `narrator-ai-cli material list --json --page 1 --size 100`. Search programmatically with `grep -i` or `python3 -c` on the JSON output — do **NOT** rely on the terminal display (may be truncated). Paginate (`--page 2`, etc.) until exhausted if `total > 100`.
2. **Found in materials** → ask user: pure narration (`target_mode=1`) or original mix (`target_mode=2`)? Construct `confirmed_movie_json` from material fields (mapping in `references/resources.md`).
3. **Not found, known title** → `task search-movie "<name>" --json` → `target_mode=1` (or `target_mode=2` if user uploads SRT). May take 60+ seconds (Gradio backend, results cached 24h).
4. **Obscure / new content** → `target_mode=3` with user's uploaded SRT. `confirmed_movie_json` optional.
**Step 1 — fast-writing**: pass `learning_model_id`, `target_mode`, `playlet_name`, `confirmed_movie_json` and/or `episodes_data`, `model` (pricing: 纯解说文案 `flash` 5pts/1k-chars or `pro` 15pts/1k-chars; 原片混剪解说文案 `flash` 12pts/1k-chars or `pro` 40pts/1k-chars). Save `task_id` from the **creation response**, then poll until top-level `.status=2` and save `.files[0].file_id` from the completed task.
**Step 2 — fast-clip-data**: pass `task_id` + `file_id` from Step 1, plus `bgm`, `dubbing`, `dubbing_type`, and `episodes_data` with `video_oss_key` / `srt_oss_key` / `negative_oss_key`. Poll until top-level `.status=2`; read top-level `.task_order_num` from the response.
**Step 3 — video-composing**: pass `order_num: <.task_order_num from Step 2>` only. Poll → `.results.tasks[0].video_url` is the finished MP4.
**Step 4 (optional) — magic-video**: only on explicit user request. See `references/magic-video.md`.
## Standard Path — High-Level Flow
> Detailed parameter tables and JSON examples live in `references/workflows.md`.
**Step 0 — Source material**: same material/upload flow as Fast Path. Use `video_file_id` as `video_oss_key` and `negative_oss_key`, and `srt_file_id` as `srt_oss_key` in `episodes_data`.
**Step 1 — popular-learning** (skip if using a pre-built template): pass `video_srt_path`, `narrator_type`, `model_version`. Poll until top-level `.status=2`, then parse `.results.tasks[0].task_result` JSON → `agent_unique_code` is the `learning_model_id`. Or use a pre-built template `id` from `task narration-styles --json` directly.
**Step 2 — generate-writing**: pass `learning_model_id`, `playlet_name`, `playlet_num`, `episodes_data`, plus three additional required fields — `target_platform` (e.g. `"douyin"`), `vendor_requirements` (`""` if none), and `target_character_name` (`""` if not applicable). Omitting any of these returns `10001 ... Field required`. Full param table in `references/workflows.md`. Save `task_id` from the creation response.
**Step 3 — clip-data**: pass `order_num` (= top-level `.task_order_num` from Step 2's polled task record, e.g. `generate_writing_xxxxx`), plus `bgm`, `dubbing`, `dubbing_type`. ⚠️ **Different from Fast Path's fast-clip-data**, which takes `task_id` — clip-data takes `order_num` instead. Poll until top-level `.status=2` (required prerequisite for Step 4) — but **do not** use clip-data's own `task_order_num` for video-composing; Step 4 keys off `generate-writing`'s instead.
**Step 4 — video-composing**: pass `order_num` + `bgm` + `dubbing` + `dubbing_type` (all four required — re-pass the BGM/voice values from Step 3; the API does not inherit them, and submitting only `order_num` returns `10001 查询解说工程任务结果失败`). ⚠️ **Standard Path keys off `generate-writing`'s `task_order_num`** (`generate_writing_xxxxx`), **NOT** clip-data's. clip-data must reach top-level `.status=2` first as a prerequisite,
