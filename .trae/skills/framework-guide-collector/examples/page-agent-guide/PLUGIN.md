---
name: "Page-Agent 插件系统"
parent: ./SKILL.md
version: "1.0.0"
---

# Page-Agent 插件系统

本模块介绍 Page-Agent 的扩展集成方式，包括 Chrome 扩展和 MCP Server。

## 1. Chrome 扩展集成

### 核心能力

| 能力 | 描述 |
|------|------|
| 多页任务 | 跨多个页面和标签页连续执行任务 |
| 浏览器级控制 | 支持跨标签导航、页面切换 |
| 开放集成接口 | 页面 JS、本地 Agent 或云端 Agent 可发起任务 |

### 第三方接入

通过页面 JavaScript 调用 `window.PAGE_AGENT_EXT`：

```typescript
const result = await window.PAGE_AGENT_EXT.execute(
    'Search for TypeScript tutorials and open the first three results',
    { token: 'USER_PROVIDED_TOKEN' }
)

window.PAGE_AGENT_EXT.stop()
```

### 授权与安全

- 扩展权限范围较广（页面访问、导航、多标签控制）
- 调用能力由 Token 保护
- 用户必须主动将 Token 提供给信任的应用

## 2. MCP Server 集成

### 概述

MCP Server 允许本地 Agent 发送自然语言浏览器任务给 Page Agent Extension。

### 使用步骤

1. 在 Chrome 中安装 Page Agent Extension
2. 将 MCP Server 添加到本地 Agent 客户端
3. 启动客户端，在浏览器中批准 Hub 连接
4. 让 Agent 在浏览器中执行任务

### Hub 架构

```
本地 Agent → MCP Server → Hub (浏览器标签) → Page Agent Extension → 页面操作
```

> **Beta 阶段**: 当前功能未完成，接口可能随时变更，请勿用于生产环境。

## 3. 参考链接

- Chrome 扩展文档: https://alibaba.github.io/page-agent/docs/features/chrome-extension
- MCP Server 文档: https://alibaba.github.io/page-agent/docs/features/mcp-server
