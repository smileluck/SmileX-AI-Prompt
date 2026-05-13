# Skills 收录

本目录用于存放从 skills.sh 和 GitHub 收录的技能模块。

## 目录结构

```
skills/
├── agents/              # Agent 类型技能
│   ├── fastapi-templates/
│   └── react-state-management/
├── tools/               # Tool 类型技能
│   └── python-mcp-server-generator/
├── full-stack-skills/   # 全栈技能
│   └── electron/
├── agent-toolkit/       # Agent 工具包
│   └── react-dev/
├── security/            # 安全相关技能
│   └── security-best-practices/
├── superpowers/         # Superpowers 系列技能
│   └── brainstorming/
├── frontend/            # 前端设计技能
│   └── frontend-design/
├── content-creation/    # 内容创作技能
│   └── narrator-ai-cli-skill/
├── marketing/           # 营销技能
└── prompts/             # Prompt 类型技能
```

## 收录技能

### Agents

| 技能名称 | 来源 | 收录时间 | 描述 |
|---------|------|---------|------|
| [fastapi-templates](./agents/fastapi-templates/) | skills.sh/wshobson/agents | 2026-04-04 | 生产级 FastAPI 项目模板，包含异步模式、依赖注入、中间件等最佳实践 |
| [react-state-management](./agents/react-state-management/) | skills.sh/wshobson/agents | 2026-04-04 | React 状态管理综合指南，涵盖 Redux Toolkit、Zustand、Jotai、React Query 等方案 |

### Tools

| 技能名称 | 来源 | 收录时间 | 描述 |
|---------|------|---------|------|
| [python-mcp-server-generator](./tools/python-mcp-server-generator/) | skills.sh/github/awesome-copilot | 2026-04-04 | 生成完整的 Python MCP 服务器，包含类型安全、错误处理和完整文档 |

### Full-Stack Skills

| 技能名称 | 来源 | 收录时间 | 描述 |
|---------|------|---------|------|
| [electron](./full-stack-skills/electron/) | skills.sh/teachingai/full-stack-skills | 2026-04-04 | Electron 跨平台桌面应用开发，包含主进程、渲染进程、IPC 通信、窗口管理等完整指南 |

### Agent Toolkit

| 技能名称 | 来源 | 收录时间 | 描述 |
|---------|------|---------|------|
| [agent-skills](./agent-toolkit/agent-skills/) | GitHub/adddyosmani | 2026-04-30 | AI 编程代理的生产级工程技能包，包含 20 个结构化技能，涵盖 Define-Plan-Build-Verify-Review-Ship 全流程。适用于 Claude Code、Cursor、Windsurf 等主流 AI 编程工具 |
| [react-dev](./agent-toolkit/react-dev/) | skills.sh/softaworks/agent-toolkit | 2026-04-04 | React TypeScript 开发技能，包含组件模式、事件处理、Hooks 类型、泛型组件、React 19 新特性 |

### Security

| 技能名称 | 来源 | 收录时间 | 描述 |
|---------|------|---------|------|
| [security-best-practices](./security/security-best-practices/) | skills.sh/openai/skills | 2026-04-15 | 安全最佳实践技能，提供语言/框架识别、安全代码编写指导、漏洞检测和安全报告生成 |

### Superpowers

| 技能名称 | 来源 | 收录时间 | 描述 |
|---------|------|---------|------|
| [brainstorming](./superpowers/brainstorming/) | skills.sh/obra/superpowers | 2026-04-15 | 通过自然协作对话将想法转化为完整设计和规格的头脑风暴技能 |

### Frontend

| 技能名称 | 来源 | 收录时间 | 描述 |
|---------|------|---------|------|
| [frontend-design](./frontend/frontend-design/) | skills.sh/anthropics/skills | 2026-04-15 | 指导创建独特、生产级前端界面的技能，避免通用 AI 风格，注重美学细节和创意实现 |

### Content Creation

| 技能名称 | 来源 | 收录时间 | 描述 |
|---------|------|---------|------|
| [narrator-ai-cli-skill](./content-creation/narrator-ai-cli-skill/) | GitHub/NarratorAI-Studio | 2026-04-30 | AI 电影/短剧解说视频自动生成 CLI Skill，内置电影素材库、BGM、多语种配音、解说模板，全流程自动化 |

### Marketing

| 技能名称 | 来源 | 收录时间 | 描述 |
|---------|------|---------|------|
| [marketingskills](https://github.com/coreyhaines31/marketingskills) | GitHub/coreyhaines31 | 2026-05-13 | 面向 Claude Code 和 AI Agent 的营销技能集合，涵盖 CRO（转化率优化）、文案撰写、SEO、数据分析和增长工程等 41 个专业营销技能模块。适用于技术营销人员和创业者，让 AI 编程助手协助完成转化优化、文案创作、SEO 审计、分析追踪和增长实验等营销任务。兼容 Claude Code、OpenAI Codex、Cursor、Windsurf 等主流 AI 编程工具 |

## 使用说明

每个技能目录下包含：
- `SKILL.md` - 技能完整内容
- `META.json` - 元数据信息

## 收录方式

使用 skill-router 技能自动收录：
```
收录 https://skills.sh/{author}/{category}/{skill-name}
收录 https://github.com/{owner}/{repo}
```
