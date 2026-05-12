---
name: "Page-Agent 使用指南"
version: "1.0.0"
source: "https://github.com/alibaba/page-agent"
collected_date: "2026-05-12"
framework_version: "1.7.1"
modules: [PLUGIN, API]
---

# Page-Agent 开发框架使用指南

Page-Agent 是一个驻留在网页中的 GUI Agent，允许通过自然语言控制 Web 界面。

## 1. 项目概述

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

## 2. 安装方法

### CDN 快速集成（演示用）

```html
<script src="https://cdn.jsdelivr.net/npm/page-agent@1.7.1/dist/iife/page-agent.demo.js" crossorigin="true"></script>
```

### NPM 安装

```bash
npm install page-agent
```

## 3. 快速开始

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

## 4. 已测试模型

| 提供商 | 推荐模型 | 备注 |
|--------|----------|------|
| Qwen | qwen3.5-plus | 推荐 |
| OpenAI | gpt-5.1 | |
| DeepSeek | deepseek-3.2 | |
| Google | gemini-3-flash | |
| Anthropic | claude-haiku-4.5 | |

## 5. 相关模块

- [插件系统](./PLUGIN.md) - Chrome 扩展集成、MCP Server 集成
- [API 参考](./API.md) - PageAgent 类、配置类型、扩展 API

## 6. 约束与限制

- API 密钥切勿在前端代码中硬编码
- 演示 CDN 仅用于技术评估，禁止用于生产环境
- 不支持需要特殊权限的操作
- 跨域 iframe 内容无法访问

## 7. 参考链接

- 官方文档: https://page-agent.js.org/docs/intro
- GitHub 仓库: https://github.com/alibaba/page-agent
- NPM 包: https://www.npmjs.com/package/page-agent

## 8. 许可证

MIT License
