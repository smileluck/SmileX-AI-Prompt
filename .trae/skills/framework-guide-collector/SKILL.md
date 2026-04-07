---
name: "framework-guide-collector"
version: "1.1.0"
author: "SmileX Team"
date: "2024-01-01"
tags: [documentation, framework, web-scraping, guide-generation]
description: "Collects and organizes development framework documentation from URLs. Invoke when user wants to create usage guides from web documentation or needs framework integration help."
min_trust_level: "normal"
dependencies: []
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

## Output Specifications

### 输出路径（模块化结构）

生成的框架指南采用**模块化目录结构**，主入口为 `SKILL.md`，子模块按需引用：

```
project/skills/framework-guides/{framework-name}/
├── SKILL.md              # 主入口：框架核心使用指南
├── PLUGIN.md             # 插件系统：插件架构与使用说明
├── API.md                # API 参考：详细 API 文档（可选）
├── ADVANCED.md           # 高级用法：进阶场景与最佳实践（可选）
└── examples/             # 示例代码目录（可选）
    ├── basic-usage.md    # 基础用法示例
    └── advanced.md       # 高级用法示例
```

### 模块职责划分

| 模块 | 职责 | 必需 |
|------|------|------|
| SKILL.md | 主入口，包含项目概述、安装、快速开始、核心概念 | ✅ 必需 |
| PLUGIN.md | 插件系统架构、官方插件列表、插件开发指南 | 有插件时必需 |
| API.md | 详细 API 参考、类型定义、配置参数 | 框架较大时建议 |
| ADVANCED.md | 高级用法、性能优化、最佳实践 | 可选 |
| examples/ | 可运行的代码示例 | 可选 |

### SKILL.md 主入口结构

```markdown
---
name: {Framework Name} 使用指南
version: 1.0.0
source: {原始文档 URL}
collected_date: {收集日期}
framework_version: {框架版本}
modules: [PLUGIN, API, ADVANCED]  # 可用子模块列表
---

# {Framework Name} 使用指南

## 1. 项目概述
## 2. 安装方法
## 3. 快速开始
## 4. 核心概念
## 5. 子模块导航

### 相关模块

- [插件系统](./PLUGIN.md) - 插件架构与使用说明
- [API 参考](./API.md) - 详细 API 文档
- [高级用法](./ADVANCED.md) - 进阶场景与最佳实践
- [示例代码](./examples/) - 可运行的代码示例
```

### PLUGIN.md 子模块结构

```markdown
---
name: {Framework Name} 插件系统
parent: ./SKILL.md
---

# {Framework Name} 插件系统

## 1. 插件架构概述
## 2. 插件注册方式
## 3. 官方插件列表
## 4. 插件配置详解
## 5. 开发自定义插件
## 6. 社区插件推荐
```

### 文件命名规范

- 目录名：使用小写字母和连字符，如 `react-guide`、`vue-guide`
- 主入口：固定为 `SKILL.md`
- 子模块：使用大写命名，如 `PLUGIN.md`、`API.md`
- 示例文件：使用小写和连字符，如 `basic-usage.md`

### 生成策略

#### 必须生成
- SKILL.md（主入口）

#### 条件生成
- PLUGIN.md：当检测到框架有插件系统时生成
- API.md：当框架 API 较复杂时生成
- ADVANCED.md：当有高级用法内容时生成

#### 可选生成
- examples/：根据用户需求生成示例代码

## Example Usage

> 完整示例请参阅 [examples/page-agent-guide/SKILL.md](./examples/page-agent-guide/SKILL.md)

### 简化示例预览

生成的文档结构：
- 项目概述（核心特性、适用场景）
- 安装方法（CDN、NPM）
- 快速开始（基础用法、配置参数）
- API 参考（核心类、方法）
- 高级用法（扩展集成）
- 约束与限制（安全、性能、已知限制）
- 参考链接

## Multi-language Support

### 语言选择规则

1. **默认语言**：根据用户输入语言决定
2. **框架文档语言**：优先使用官方文档的原始语言
3. **双语支持**：对于国际化框架，提供中英双语版本

### 双语文档结构

```
framework-guides/
├── react/
│   ├── SKILL.md        # 中文版
│   └── SKILL.en.md     # 英文版
```

## Performance Optimization

### 大型文档处理策略

| 策略 | 描述 |
|------|------|
| 分页获取 | 对于超长页面，使用分页参数分批获取 |
| 并行获取 | 多个相关页面并行获取，减少总耗时 |
| 缓存机制 | 相同 URL 在短期内不重复获取 |
| 增量更新 | 只更新变更部分，避免全量重新生成 |

### 获取超时处理

```
默认超时：30 秒
重试次数：3 次
重试间隔：指数退避（1s, 2s, 4s）
```

### 资源限制

- 单次获取最大内容：100KB
- 并发获取上限：5 个
- 总获取时间上限：5 分钟

## Skill Collaboration

### 与其他技能的协作关系

| 技能 | 协作方式 |
|------|----------|
| skill-router | 作为框架文档收集的入口，被路由到此技能 |
| skill-creator | 收集的文档可作为新技能的基础材料 |
| submodule-updater | 当框架是 Git 子模块时，可联动更新 |

### 协作流程示例

```
用户请求 → skill-router → framework-guide-collector → 生成文档
                                    ↓
                            skill-creator（可选）
```

## Error Handling

### 错误分类

| 错误类型 | 错误码 | 处理策略 |
|----------|--------|----------|
| 网络超时 | E001 | 重试 3 次，指数退避 |
| URL 无效 | E002 | 提示用户检查 URL 格式 |
| 内容解析失败 | E003 | 尝试其他获取工具 |
| 权限受限 | E004 | 提示需要登录或权限 |
| 内容过大 | E005 | 建议分页或指定章节 |

### 错误恢复流程

```
1. 记录错误详情
2. 尝试备选方案
3. 如全部失败，提供手动输入选项
4. 生成错误报告供用户参考
```

### 错误报告模板

```markdown
## 文档收集失败报告

- **URL**: {原始 URL}
- **错误类型**: {错误类型}
- **错误详情**: {详细错误信息}
- **尝试过的方案**: {方案列表}
- **建议操作**: {用户可执行的操作}
```

### URL 获取失败处理

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

## Output Requirements

When using this skill, always:

1. Provide complete, runnable code examples
2. Include both Chinese and English documentation when appropriate
3. Add proper error handling in code samples
4. Reference official documentation links
5. Note any version-specific information

## 更新日志

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| 1.1.0 | 2024-01-01 | 添加模块化输出结构、性能优化指导、技能协作说明、增强错误处理 |
| 1.0.0 | 2024-01-01 | 初始版本 |
