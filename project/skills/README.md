# Skills 收录

本目录用于存放从 skills.sh 等平台收录的技能模块。

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
└── prompts/             # Prompt 类型技能
```

## 收录技能

### Agents

| 技能名称 | 来源 | 收录时间 | 描述 |
|---------|------|---------|------|
| [fastapi-templates](./agents/fastapi-templates/) | skills.sh/wshobson/agents | 2026-04-04 | Production-ready FastAPI 项目模板，包含异步模式、依赖注入、中间件等最佳实践 |

### Tools

| 技能名称 | 来源 | 收录时间 | 描述 |
|---------|------|---------|------|
| [python-mcp-server-generator](./tools/python-mcp-server-generator/) | skills.sh/github/awesome-copilot | 2026-04-04 | 生成完整的 Python MCP 服务器，包含类型安全、错误处理和完整文档 |

### Full-Stack Skills

| 技能名称 | 来源 | 收录时间 | 描述 |
|---------|------|---------|------|
| [electron](./full-stack-skills/electron/) | skills.sh/teachingai/full-stack-skills | 2026-04-04 | Electron 跨平台桌面应用开发，包含主进程、渲染进程、IPC通信、窗口管理等完整指南 |

### Agent Toolkit

| 技能名称 | 来源 | 收录时间 | 描述 |
|---------|------|---------|------|
| [react-dev](./agent-toolkit/react-dev/) | skills.sh/softaworks/agent-toolkit | 2026-04-04 | React TypeScript 开发技能，包含组件模式、事件处理、Hooks 类型、泛型组件、React 19 新特性 |

## 使用说明

每个技能目录下包含：
- `SKILL.md` - 技能完整内容
- `META.json` - 元数据信息

## 收录方式

使用 skill-router 技能自动收录：
```
收录 https://skills.sh/{author}/{category}/{skill-name}
```
