---
name: "page-agent-guide"
description: "Page-Agent GUI automation framework guide. Invoke when user needs browser automation with natural language, multi-page tasks, or MCP server integration."
---

# Page-Agent 开发框架使用指南

Page-Agent 是一个驻留在网页中的 GUI Agent，允许通过自然语言控制 Web 界面。

## When to Invoke

- 用户需要通过自然语言控制 Web 界面
- 用户需要实现智能表单填充或自动化操作
- 用户需要多页面任务或跨标签页自动化
- 用户需要 MCP Server 集成或 Chrome 扩展功能
- 用户询问 Page-Agent 的使用方法或模型配置

## 1. 项目概述

### 核心特性

| 特性 | 描述 |
|------|------|
| 🎯 轻量集成 | 无需浏览器扩展/Python/无头浏览器，仅需页面内 JavaScript |
| 📖 文本化 DOM 操作 | 无需截图，无需多模态 LLM 或特殊权限 |
| 🧠 自定义 LLM | 支持接入任意符合 OpenAI 接口规范的 LLM 服务 |
| 🐙 多页面支持 | 可选 Chrome 扩展支持跨标签页任务 |
| 🔌 MCP Server | Beta 版本，支持外部 Agent 客户端控制浏览器 |

### 适用场景

| 场景 | 描述 |
|------|------|
| SaaS AI Copilot | 快速为产品集成 AI 助手，无需后端重构 |
| 智能表单填充 | 将复杂工作流简化为一句话指令，适用于 ERP、CRM、管理系统 |
| 无障碍访问 | 通过自然语言使 Web 应用无障碍化，支持语音命令 |
| 多页面 Agent | 扩展 Web Agent 跨浏览器标签的能力 |
| MCP 集成 | 允许 Agent 客户端控制浏览器 |

## 2. 安装方法

### CDN 快速集成（演示用）

```html
<!-- 全球镜像 -->
<script src="https://cdn.jsdelivr.net/npm/page-agent@1.7.1/dist/iife/page-agent.demo.js" crossorigin="true"></script>

<!-- 中国镜像 -->
<script src="https://registry.npmmirror.com/page-agent/1.7.1/files/dist/iife/page-agent.demo.js" crossorigin="true"></script>
```

> ⚠️ **注意**: 演示 CDN 使用免费测试 API，仅用于技术评估，禁止用于生产环境。

### NPM 安装

```bash
npm install page-agent
```

## 3. 快速开始

### 基础用法

```typescript
import { PageAgent } from 'page-agent'

/**
 * 创建 PageAgent 实例
 * @param config 配置对象
 */
const agent = new PageAgent({
    model: 'qwen3.5-plus',
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    apiKey: 'YOUR_API_KEY',
    language: 'en-US',
})

// 执行自然语言指令
await agent.execute('Click the login button')
```

### 配置参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `model` | string | 是 | LLM 模型名称 |
| `baseURL` | string | 是 | API 基础地址 |
| `apiKey` | string | 是 | API 密钥 |
| `language` | string | 否 | 语言设置，默认 'en-US' |

### 常用操作示例

```typescript
// 点击操作
await agent.execute('Click the submit button')

// 表单填充
await agent.execute('Fill the email field with test@example.com')

// 复杂操作
await agent.execute('Navigate to settings and enable dark mode')

// 多步骤操作
await agent.execute('Login with username admin and password 123456, then go to dashboard')
```

## 4. 模型配置

### 已测试模型

| 提供商 | 推荐模型 | 备注 |
|--------|----------|------|
| Qwen | qwen3.5-plus ⭐, qwen3.5-flash ⭐ | 推荐 |
| OpenAI | gpt-5.1 ⭐, gpt-5, gpt-4.1 | |
| DeepSeek | deepseek-3.2 ⭐ | |
| Google | gemini-3-flash ⭐, gemini-3-pro | |
| Anthropic | claude-haiku-4.5 ⭐, claude-sonnet-4.5 | |
| xAI | grok-4, grok-4.1-fast | |
| MiniMax | MiniMax-M2.7, MiniMax-M2.5 | |

> ⭐ 推荐使用 ToolCall 能力强的轻量级模型

### 生产环境鉴权

```typescript
/**
 * 生产环境配置示例
 * 建议通过后端代理转发 LLM 请求
 */
const agent = new PageAgent({
    model: 'qwen3.5-plus',
    baseURL: '/api/llm-proxy',  // 后端代理地址
    customFetch: async (url, options) => {
        // 携带 Cookie 或其他鉴权信息
        const headers = {
            ...options?.headers,
            'Authorization': `Bearer ${getAuthToken()}`,
        }
        return fetch(url, { ...options, headers })
    },
})
```

> ⚠️ **安全警告**: 永远不要把真实的 LLM API Key 提交到前端代码中

### 本地运行时配置

#### Ollama

```typescript
/**
 * Ollama 本地模型配置
 * 需要开启 CORS 并设置足够的上下文长度
 */
const agent = new PageAgent({
    model: 'qwen3:14b',
    baseURL: 'http://localhost:11434/v1',
    apiKey: 'ollama',  // Ollama 不需要真实 key
})
```

**Ollama 启动参数**:

```bash
# macOS / Linux
OLLAMA_ORIGINS="*" OLLAMA_NUM_PARALLEL=4 ollama serve

# Windows (PowerShell)
$env:OLLAMA_ORIGINS="*"; $env:OLLAMA_NUM_PARALLEL=4; ollama serve
```

#### LM Studio

```typescript
/**
 * LM Studio 配置
 * 需要启用 disableNamedToolChoice
 */
const agent = new PageAgent({
    model: 'local-model',
    baseURL: 'http://localhost:1234/v1',
    apiKey: 'lm-studio',
})
```

## 5. Chrome 扩展集成

### 核心能力

| 能力 | 描述 |
|------|------|
| 🔓 多页任务 | 跨多个页面和标签页连续执行任务 |
| 🧭 浏览器级控制 | 支持跨标签导航、页面切换 |
| 🔌 开放集成接口 | 页面 JS、本地 Agent 或云端 Agent 可发起任务 |

### 安装扩展

1. **Chrome 应用商店**: 搜索 "Page Agent Extension"
2. **GitHub Releases**: 下载最新版本

### 第三方接入

通过页面 JavaScript 调用 `window.PAGE_AGENT_EXT`:

```typescript
/**
 * 执行多页面任务
 * @param task 自然语言任务描述
 * @param config 配置选项
 */
const result = await window.PAGE_AGENT_EXT.execute(
    'Search for TypeScript tutorials and open the first three results',
    {
        token: 'USER_PROVIDED_TOKEN',  // 用户授权的 Token
    }
)

/**
 * 停止当前任务
 */
window.PAGE_AGENT_EXT.stop()
```

### 授权与安全

- 扩展权限范围较广（页面访问、导航、多标签控制）
- 调用能力由 Token 保护
- 用户必须主动将 Token 提供给信任的应用

## 6. MCP Server 集成

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

Hub 是 Page Agent Extension 与外部调用者之间的通信控制中心。

> 🚧 **Beta 阶段**: 当前功能未完成，接口可能随时变更，请勿用于生产环境。

## 7. API 参考

### PageAgent 类

```typescript
class PageAgent {
    /**
     * 创建 PageAgent 实例
     * @param config 配置对象
     */
    constructor(config: PageAgentConfig)

    /**
     * 执行自然语言指令
     * @param command 自然语言指令
     * @returns 执行结果
     */
    execute(command: string): Promise<ExecutionResult>
}
```

### 配置类型

```typescript
interface PageAgentConfig {
    /** LLM 模型名称 */
    model: string
    /** API 基础地址 */
    baseURL: string
    /** API 密钥 */
    apiKey: string
    /** 语言设置 */
    language?: 'en-US' | 'zh-CN'
    /** 自定义 fetch 函数 */
    customFetch?: (url: string, options?: RequestInit) => Promise<Response>
}
```

### 扩展 API

```typescript
interface PageAgentExtension {
    /**
     * 执行多页面任务
     * @param task 任务描述
     * @param config 配置
     */
    execute(task: string, config?: { token?: string }): Promise<void>

    /** 停止当前任务 */
    stop(): void
}
```

## 8. 约束与限制

### 安全注意事项

| 注意事项 | 描述 |
|----------|------|
| API 密钥保护 | 切勿在前端代码中硬编码 API 密钥 |
| 演示 CDN 限制 | 仅用于技术评估，禁止用于生产环境 |
| CORS 限制 | 部分网站可能有跨域限制 |
| 数据安全 | 免费测试接口数据通过中国大陆服务器处理 |

### 性能考虑

| 考虑因素 | 建议 |
|----------|------|
| DOM 处理 | 大型复杂 DOM 可能影响响应速度 |
| LLM 延迟 | 响应时间取决于 LLM 服务性能 |
| 并发限制 | 避免同时执行过多指令 |
| 上下文长度 | 本地模型建议设置至少 8000 tokens |

### 已知限制

1. 不支持需要特殊权限的操作
2. 部分动态加载内容可能需要等待
3. 跨域 iframe 内容无法访问
4. 小于 10B 参数的模型通常效果不佳

## 9. 最佳实践

### 错误处理

```typescript
/**
 * 带错误处理的执行示例
 */
async function executeWithErrorHandling(command: string): Promise<void> {
    try {
        const result = await agent.execute(command)
        console.log('执行成功:', result)
    } catch (error) {
        if (error instanceof Error) {
            console.error('执行失败:', error.message)
            
            // 根据错误类型处理
            if (error.message.includes('timeout')) {
                console.log('请求超时，正在重试...')
                await executeWithErrorHandling(command)
            }
        }
    }
}
```

### 生产环境部署

```typescript
/**
 * 生产环境配置示例
 */
const productionAgent = new PageAgent({
    model: 'qwen3.5-plus',
    baseURL: '/api/llm-proxy',
    customFetch: async (url, options) => {
        const response = await fetch(url, {
            ...options,
            headers: {
                ...options?.headers,
                'X-Session-Id': getSessionId(),
            },
        })
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`)
        }
        
        return response
    },
})
```

## 10. 参考链接

| 资源 | 链接 |
|------|------|
| 官方文档 | https://alibaba.github.io/page-agent/docs/introduction/overview |
| GitHub 仓库 | https://github.com/alibaba/page-agent |
| Demo 演示 | https://alibaba.github.io/page-agent/ |
| NPM 包 | https://www.npmjs.com/package/page-agent |
| Chrome 扩展文档 | https://alibaba.github.io/page-agent/docs/features/chrome-extension |
| MCP Server 文档 | https://alibaba.github.io/page-agent/docs/features/mcp-server |
| 模型配置 | https://alibaba.github.io/page-agent/docs/features/models |

## 11. 许可证

MIT License

---

## 致谢

本项目基于 [browser-use](https://github.com/browser-use/browser-use) 的优秀工作构建。

DOM 处理组件和提示词源自 browser-use:
- Copyright (c) 2024 Gregor Zunic
- Licensed under the MIT License
