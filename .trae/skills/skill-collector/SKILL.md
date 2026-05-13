---
name: "skill-router"
description: "技能收录路由，根据 URL 类型自动分发到对应的收录模块。"
---

# Skill Router

技能收录主入口，根据 URL 特征判断来源类型并分发到对应收录模块。

## 触发条件

- "收录这个技能：{url}"
- "添加技能：{url}"
- "收录 {url}"

## 路由规则

| 来源 | URL 特征 | 收录模块 |
|------|----------|----------|
| GitHub | `github.com` 或 `git@github.com` | [github-collect.md](./github-collect.md) |
| Skills.sh | `skills.sh` | [skillssh-collect.md](./skillssh-collect.md) |

## 执行步骤

1. **提取 URL**：从用户输入中匹配 URL（支持 HTTP/HTTPS 和 SSH 格式）
2. **判断来源**：URL 包含 `skills.sh` → Skills.sh 收录；包含 `github.com` 或 `git@github.com` → GitHub 收录
3. **分发执行**：读取对应收录模块文件并按其流程执行

## 不支持的来源

如果 URL 不匹配任何已知来源，提示用户支持的格式：
- GitHub: `https://github.com/{owner}/{repo}`
- Skills.sh: `https://skills.sh/{author}/{category}/{skill-name}`
