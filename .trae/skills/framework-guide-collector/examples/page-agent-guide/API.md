---
name: "Page-Agent API 参考"
parent: ./SKILL.md
version: "1.0.0"
---

# Page-Agent API 参考

本模块提供 Page-Agent 核心 API 和配置类型的详细参考。

## 1. PageAgent 类

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

## 2. 配置类型

### PageAgentConfig

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

### 生产环境鉴权

```typescript
const agent = new PageAgent({
    model: 'qwen3.5-plus',
    baseURL: '/api/llm-proxy',
    customFetch: async (url, options) => {
        const headers = {
            ...options?.headers,
            'Authorization': `Bearer ${getAuthToken()}`,
        }
        return fetch(url, { ...options, headers })
    },
})
```

## 3. 扩展 API

### PageAgentExtension

```typescript
interface PageAgentExtension {
    execute(task: string, config?: { token?: string }): Promise<void>
    stop(): void
}
```

## 4. 参考链接

- 模型配置: https://alibaba.github.io/page-agent/docs/features/models
- API 文档: https://page-agent.js.org/docs/intro
