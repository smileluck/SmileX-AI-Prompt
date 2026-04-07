---
name: "Page-Agent 使用指南"
version: "1.0.0"
source: "https://github.com/alibaba/page-agent"
collected_date: "2024-01-01"
framework_version: "1.7.1"
modules: []
---

# Page-Agent 开发框架使用指南

## 1. 项目概述

Page-Agent 是一个驻留在网页中的 GUI Agent，允许通过自然语言控制 Web 界面。

### 核心特性

| 特性 | 描述 |
|------|------|
| 轻量集成 | 无需浏览器扩展/Python/无头浏览器，仅需页面内 JavaScript |
| 文本化 DOM 操作 | 无需截图，无需多模态 LLM 或特殊权限 |
| 自定义 LLM | 支持接入任意 LLM 服务 |
| 多页面支持 | 可选 Chrome 扩展支持跨标签页任务 |
| MCP Server | Beta 版本，支持外部控制 |

### 适用场景

- **SaaS AI Copilot**: 快速为产品集成 AI 助手
- **智能表单填充**: 将复杂工作流简化为一句话指令
- **无障碍访问**: 通过自然语言使 Web 应用无障碍化
- **多页面 Agent**: 扩展 Web Agent 跨浏览器标签的能力

## 2. 安装方法

### CDN 快速集成（演示用）

```html
<!-- 全球镜像 -->
<script src="https://cdn.jsdelivr.net/npm/page-agent@1.7.1/dist/iife/page-agent.demo.js" crossorigin="true"></script>

<!-- 中国镜像 -->
<script src="https://registry.npmmirror.com/page-agent/1.7.1/files/dist/iife/page-agent.demo.js" crossorigin="true"></script>
```

### NPM 安装

```bash
npm install page-agent
```

## 3. 快速开始

### 基础用法

```javascript
import { PageAgent } from 'page-agent'

const agent = new PageAgent({
    model: 'qwen3.5-plus',
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    apiKey: 'YOUR_API_KEY',
    language: 'en-US',
})

await agent.execute('Click the login button')
```

### 配置参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `model` | string | 是 | LLM 模型名称 |
| `baseURL` | string | 是 | API 基础地址 |
| `apiKey` | string | 是 | API 密钥 |
| `language` | string | 否 | 语言设置，默认 'en-US' |

## 4. API 参考

### PageAgent 类

```typescript
class PageAgent {
    constructor(config: PageAgentConfig)
    execute(command: string): Promise<ExecutionResult>
}
```

### execute() 方法

执行自然语言指令，操作页面 DOM。

```javascript
// 点击操作
await agent.execute('Click the submit button')

// 表单填充
await agent.execute('Fill the email field with test@example.com')

// 复杂操作
await agent.execute('Navigate to settings and enable dark mode')
```

## 5. 高级用法

### Chrome 扩展集成

Page-Agent 提供可选的 Chrome 扩展，支持：
- 跨标签页任务执行
- 持久化会话管理
- 增强的页面访问能力

### MCP Server 集成

Beta 版本的 MCP Server 允许外部 Agent 客户端控制浏览器。

## 6. 约束与限制

### 安全注意事项

1. **API 密钥保护**: 切勿在前端代码中硬编码 API 密钥
2. **演示 CDN 限制**: 演示 CDN 使用免费测试 API，仅用于技术评估
3. **CORS 限制**: 部分网站可能有跨域限制

### 性能考虑

1. **DOM 处理**: 大型复杂 DOM 可能影响响应速度
2. **LLM 延迟**: 响应时间取决于 LLM 服务性能
3. **并发限制**: 避免同时执行过多指令

### 已知限制

1. 不支持需要特殊权限的操作
2. 部分动态加载内容可能需要等待
3. 跨域 iframe 内容无法访问

## 7. 参考链接

- 官方文档: https://page-agent.js.org/docs/intro
- GitHub 仓库: https://github.com/alibaba/page-agent
- Demo 演示: https://page-agent.js.org/demo
- NPM 包: https://www.npmjs.com/package/page-agent

## 8. 许可证

MIT License
