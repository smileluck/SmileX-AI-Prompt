---
name: "framework-guide-collector"
description: "Collects and organizes development framework documentation from URLs. Invoke when user wants to create usage guides from web documentation or needs framework integration help."
---

# Framework Guide Collector

This skill helps collect, parse, and organize development framework documentation from specified URLs, generating comprehensive Markdown guides for development work.

## When to Invoke

- User wants to create a usage guide from a web documentation URL
- User needs to integrate a new framework and wants organized documentation
- User asks to "collect framework docs" or "organize framework guide"
- User provides a GitHub repository URL and wants a structured guide

## Workflow

### Step 1: Fetch Website Content

Use available web tools to fetch the target URL content:

```
Tools available:
- WebFetch: Fetch and convert HTML to markdown
- mcp_web_research_visit_page: Visit and extract page content
- mcp_duckduckgo_fetch_content: Fetch clean text from webpage
```

### Step 2: Parse and Structure Content

Extract the following information from the fetched content:

1. **Project Overview**
   - Project name and description
   - Key features and capabilities
   - Target use cases

2. **Installation Methods**
   - NPM/Yarn installation commands
   - CDN links (global and regional mirrors)
   - Browser compatibility

3. **Quick Start Guide**
   - Basic usage examples
   - Configuration options
   - Required dependencies

4. **API Reference**
   - Core classes and methods
   - Configuration parameters
   - Return types and examples

5. **Plugin System** (if applicable)
   - Plugin architecture and extension points
   - Available official plugins
   - Community plugin ecosystem
   - Plugin development guide

6. **Advanced Usage**
   - Extension options
   - Integration patterns
   - Best practices

7. **Constraints and Limitations**
   - Security considerations
   - Performance notes
   - Known issues

### Step 3: Identify Plugin System

Before generating documentation, identify if the framework has a plugin system:

#### Plugin System Indicators

| Indicator | Description |
|-----------|-------------|
| `plugin` keyword | Documentation mentions "plugin", "extension", "addon", "module" |
| `.use()` pattern | Framework uses `.use()` method to add functionality |
| Plugin packages | NPM packages with framework name prefix (e.g., `@milkdown/kit/plugin/*`) |
| Plugin directory | GitHub repo has `/plugins` or `/extensions` directory |
| Configuration hooks | API exposes hooks/events for extending functionality |

#### Plugin Detection Commands

```bash
# Search for plugin-related packages on NPM
npm search <framework-name>-plugin
npm search @<framework-scope>/plugin

# Check GitHub for plugin directory
# Look for: /plugins, /extensions, /packages/plugin-*
```

#### Plugin Information to Collect

1. **Official Plugins**
   - Plugin name and package
   - Installation command
   - Basic usage example
   - Configuration options

2. **Plugin Architecture**
   - How plugins are registered
   - Plugin lifecycle hooks
   - Plugin API/interfaces

3. **Community Plugins**
   - Popular third-party plugins
   - Installation sources
   - Compatibility notes

### Step 4: Generate Markdown Document

Create a structured Markdown document following this template:

```markdown
# {Framework Name} 使用指南

## 1. 项目概述
{Description and features}

## 2. 安装方法
{Installation commands and options}

## 3. 快速开始
{Basic usage examples}

## 4. API 参考
{Detailed API documentation}

## 5. 插件系统
{Plugin architecture and available plugins}

## 6. 高级用法
{Advanced patterns and extensions}

## 7. 约束与限制
{Security, performance, and limitations}

## 8. 参考链接
{Official documentation and resources}
```

## Example Usage

### Page-Agent Framework Guide

Based on the collected documentation from `https://github.com/alibaba/page-agent`:

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

---

## Output Requirements

When using this skill, always:

1. Provide complete, runnable code examples
2. Include both Chinese and English documentation when appropriate
3. Add proper error handling in code samples
4. Reference official documentation links
5. Note any version-specific information

## Error Handling

If URL fetch fails:
1. Try alternative fetch methods (WebFetch, mcp_web_research_visit_page, mcp_duckduckgo_fetch_content)
2. Use web search to find alternative documentation sources
3. Report the issue and suggest manual documentation input

## Plugin Documentation Template

When documenting plugins, use this structure:

```markdown
## 插件系统

### 插件架构

{Framework} 采用插件驱动架构，所有功能都通过插件扩展。

#### 插件注册方式

```typescript
// 方式一：链式调用
Editor.make()
    .use(pluginA)
    .use(pluginB)

// 方式二：数组批量注册
Editor.make()
    .use([pluginA, pluginB])
```

### 官方插件列表

| 插件名 | 包名 | 功能描述 |
|--------|------|----------|
| {Plugin Name} | `{package-name}` | {Description} |

### 插件使用示例

#### {Plugin Name}

```bash
npm install {package-name}
```

```typescript
import { pluginName } from '{package-name}'

// 基础用法
Editor.make()
    .use(pluginName)

// 带配置
Editor.make()
    .use(pluginName.configure({
        option1: 'value1'
    }))
```

#### 配置选项

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `option1` | string | - | 配置说明 |

### 社区插件

| 插件名 | 来源 | 功能描述 |
|--------|------|----------|
| {Plugin} | [GitHub](url) | {Description} |

### 开发自定义插件

```typescript
import { Plugin, pluginKey } from '{framework}'

/**
 * 自定义插件示例
 */
const myPlugin = Plugin.create({
    name: 'myPlugin',
    // 插件配置
    setup(ctx) {
        // 插件初始化逻辑
    }
})
```
```

## Plugin Collection Best Practices

### 1. Plugin Discovery

When collecting plugin information:

1. **Check Official Documentation First**
   - Look for "Plugins" or "Extensions" section
   - Check sidebar navigation for plugin listings

2. **Search NPM Registry**
   ```
   npm search @framework-scope/plugin
   npm search framework-plugin
   ```

3. **Explore GitHub Repository**
   - Check `/packages` directory for monorepo structure
   - Look for `/plugins` or `/extensions` folders
   - Review README for plugin mentions

4. **Community Resources**
   - Awesome lists on GitHub
   - Community forums/Discord
   - Stack Overflow tags

### 2. Plugin Documentation Checklist

- [ ] Plugin name and package identifier
- [ ] Installation command
- [ ] Basic usage example
- [ ] Configuration options with types
- [ ] Dependencies and peer dependencies
- [ ] Compatibility information (version requirements)
- [ ] Known issues or limitations
- [ ] Links to source/documentation

### 3. Plugin Versioning Notes

Always note:
- Minimum framework version required
- Breaking changes between major versions
- Deprecated plugins and alternatives

## Plugin Collection Example: Milkdown

Here's an example of how to collect plugin information for a framework:

### Plugin System Detection

Milkdown indicators found:
- ✅ Documentation mentions "plugin-driven architecture"
- ✅ Uses `.use()` method for plugin registration
- ✅ NPM packages under `@milkdown/kit/plugin/*`
- ✅ GitHub has `/packages` directory with plugins

### Official Plugins Collected

| Plugin | Package | Description |
|--------|---------|-------------|
| Commonmark | `@milkdown/kit/preset/commonmark` | CommonMark syntax support |
| GFM | `@milkdown/kit/preset/gfm` | GitHub Flavored Markdown |
| Listener | `@milkdown/kit/plugin/listener` | Event listeners for editor changes |
| History | `@milkdown/kit/plugin/history` | Undo/redo support |
| Clipboard | `@milkdown/kit/plugin/clipboard` | Clipboard operations |

### Plugin Usage Example

```typescript
import { Editor, rootCtx } from '@milkdown/kit/core'
import { commonmark } from '@milkdown/kit/preset/commonmark'
import { listener, listenerCtx } from '@milkdown/kit/plugin/listener'
import { history } from '@milkdown/kit/plugin/history'

const editor = Editor.make()
    .config((ctx) => ctx.set(rootCtx, root))
    .use(commonmark)      // Add CommonMark support
    .use(history)         // Add undo/redo
    .use(listener)        // Add event listeners
```

### Plugin Configuration

```typescript
// Listener plugin with configuration
.use(listener)
.config((ctx) => {
    ctx.get(listenerCtx).markdownUpdated((ctx, markdown) => {
        console.log('Content changed:', markdown)
    })
})
```
