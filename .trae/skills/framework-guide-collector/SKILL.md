---
name: "framework-guide-collector"
version: "2.0.0"
author: "SmileX Team"
date: "2026-05-12"
tags: [documentation, framework, web-scraping, guide-generation]
description: "从 URL 收集并整理开发框架文档，生成模块化的 Markdown 使用指南。当用户需要从网页文档创建使用指南或需要框架集成帮助时调用。"
min_trust_level: "normal"
dependencies: []
---

# Framework Guide Collector

从网页 URL 收集并整理开发框架文档，生成模块化的 Markdown 使用指南。详细介绍请参阅 [README.md](./README.md)。

## 触发条件

- 用户想从网页文档 URL 创建使用指南
- 用户需要集成新框架并希望整理文档
- 用户要求"整理框架文档"或"生成使用指南"
- 用户提供 GitHub 仓库 URL 并想要结构化指南
- 用户要求更新已有的框架指南

## 工作流程

### Step 1: 内容获取

#### 1.1 获取入口页面

使用工具获取用户提供的 URL 内容。

工具优先级：
1. **WebFetch**（内置，始终可用）
2. mcp_web_research_visit_page（如已配置）
3. mcp_duckduckgo_fetch_content（如已配置）
4. WebSearch 搜索文档片段（降级方案）

#### 1.2 发现文档站结构

分析入口页面，识别文档导航：

| 特征 | 识别方式 |
|------|----------|
| 侧边栏导航 | 提取 sidebar 中的链接列表 |
| 顶部导航栏 | 提取 nav 元素中的文档链接 |
| Next.js 文档 | 查找 /docs/ 路径模式 |
| Docusaurus 站点 | 识别 sidebar-tree 数据 |
| VitePress 站点 | 识别 VPContent 结构 |

#### 1.3 确定抓取范围

根据框架类型（Step 1.5 识别结果），优先抓取关键页面：

- **必须抓取**：Getting Started、Installation、Quick Start
- **按需抓取**：API Reference、Plugins、Configuration、Advanced
- **可选抓取**：Changelog、Migration Guide、Contributing

#### 1.4 处理 SPA 文档站

如果 WebFetch 返回空内容或加载提示：
1. 尝试 GitHub 仓库的 `/docs` 或 `/documentation` 目录
2. 尝试 `{url}/README.md`
3. 使用 WebSearch 搜索 `site:{domain} {framework} docs`
4. 报告获取受限，建议用户提供文档 URL 列表

### Step 1.5: 框架类型识别

根据项目特征判断框架类型：

| 类型 | 判断特征 | 示例 |
|------|----------|------|
| UI 组件库 | 有组件 Demo、props 文档、主题系统 | Ant Design、Radix UI |
| 编辑器/WYSIWYG | 有插件系统、内容操作 API、工具栏 | Milkdown、TinyMCE |
| 构建工具 | 有配置文件、插件钩子、构建流程 | Vite、Webpack |
| 后端框架 | 有路由、中间件、数据库集成 | FastAPI、Express |
| 测试框架 | 有匹配器、Mock、断言 | Vitest、Jest |
| Agent/自动化 | 有任务执行、工具调用、MCP | Page-Agent、LangChain |

### Step 2: 解析与结构化内容

根据框架类型选择对应的章节模板，从抓取的内容中提取信息：

#### UI 组件库模板
SKILL.md: 概述 → 安装 → 快速开始 → 核心组件 → 主题定制 → 无障碍 → 约束
PLUGIN.md: 如有主题插件或组件扩展包

#### 编辑器模板
SKILL.md: 概述 → 安装 → 快速开始 → 核心概念 → 常见问题
PLUGIN.md: 插件架构 → 官方插件列表 → 插件开发
API.md: 编辑器实例方法 → 配置接口 → 事件系统

#### 构建工具模板
SKILL.md: 概述 → 安装 → 配置基础 → 常用功能
PLUGIN.md: 插件系统 → 官方插件 → 开发自定义插件

#### 后端框架模板
SKILL.md: 概述 → 安装 → 快速开始 → 路由 → 请求处理
PLUGIN.md: 中间件系统 → 官方中间件
API.md: 核心 API → 配置参考

#### 测试框架模板
SKILL.md: 概述 → 安装 → 快速开始 → 匹配器 → Mock → 配置
API.md: API 参考 → 配置选项

#### Agent/自动化模板
SKILL.md: 概述 → 安装 → 快速开始 → 模型配置 → 约束
PLUGIN.md: 扩展集成（Chrome 扩展、MCP 等）
API.md: 核心 API → 配置类型

#### 通用提取要点

1. **项目概述**
   - 项目名称和描述
   - 核心特性和能力
   - 适用场景

2. **安装方法**
   - NPM/Yarn 安装命令
   - CDN 链接（全球和区域镜像）
   - 浏览器兼容性

3. **快速开始**
   - 基础用法示例
   - 配置选项
   - 必需依赖

4. **API 参考**
   - 核心类和方法
   - 配置参数
   - 返回类型和示例

5. **插件系统**（如适用）
   - 插件架构和扩展点
   - 可用的官方插件
   - 社区插件生态
   - 插件开发指南

6. **高级用法**
   - 扩展选项
   - 集成模式
   - 最佳实践

7. **约束与限制**
   - 安全注意事项
   - 性能说明
   - 已知问题

### Step 3: 识别插件系统

在生成文档前，识别框架是否有插件系统：

#### 插件系统指示器

| 指示器 | 描述 |
|--------|------|
| `plugin` 关键词 | 文档提到 "plugin"、"extension"、"addon"、"module" |
| `.use()` 模式 | 框架使用 `.use()` 方法添加功能 |
| 插件包 | NPM 包带有框架名前缀（如 `@milkdown/kit/plugin/*`） |
| 插件目录 | GitHub 仓库有 `/plugins` 或 `/extensions` 目录 |
| 配置钩子 | API 暴露用于扩展功能的钩子/事件 |

#### 插件检测命令

```bash
# 在 NPM 上搜索插件相关包
npm search <framework-name>-plugin
npm search @<framework-scope>/plugin

# 检查 GitHub 上的插件目录
# 查找：/plugins, /extensions, /packages/plugin-*
```

#### 需要收集的插件信息

1. **官方插件**
   - 插件名和包名
   - 安装命令
   - 基础用法示例
   - 配置选项

2. **插件架构**
   - 插件注册方式
   - 插件生命周期钩子
   - 插件 API/接口

3. **社区插件**
   - 热门第三方插件
   - 安装来源
   - 兼容性说明

### Step 4: 生成模块化文档

按照模块化拆分执行规则，生成结构化的文档文件。

## 输出规范

### 输出路径

生成的框架指南存放于：

```
project/skills/framework-guides/{framework-name}/
├── SKILL.md              # 主入口：框架核心使用指南
├── PLUGIN.md             # 插件系统：插件架构与使用说明
├── API.md                # API 参考：详细 API 文档
├── ADVANCED.md           # 高级用法：进阶场景与最佳实践
└── examples/             # 示例代码目录（可选）
    ├── basic-usage.md    # 基础用法示例
    └── advanced.md       # 高级用法示例
```

### 模块化拆分执行规则

#### 第一步：评估总内容量

估算生成文档的总行数（基于抓取到的内容量）：
- **< 300 行**：仅生成 SKILL.md（单文件，不拆分）
- **300-600 行**：生成 SKILL.md + 1 个子模块
- **> 600 行**：生成 SKILL.md + 多个子模块

#### 第二步：确定拆分模块

根据内容特征选择拆分点：

| 拆分模块 | 触发条件 | 从 SKILL.md 移出的章节 |
|----------|----------|----------------------|
| PLUGIN.md | 框架有 ≥3 个官方插件，或插件文档 > 80 行 | "插件系统"完整章节 |
| API.md | API 参考内容 > 100 行 | "API 参考"完整章节 |
| ADVANCED.md | 高级用法 > 80 行 | "高级用法"完整章节 |

#### 第三步：写入子模块导航

SKILL.md 中被移出的章节替换为导航块：

```markdown
## 5. 插件系统

> 详细内容请参阅 [插件系统](./PLUGIN.md)

Milkdown 采用插件驱动架构，所有功能都通过 `.use()` 方法添加插件。
```

SKILL.md 的"子模块导航"章节列出所有可用模块：

```markdown
## 相关模块

- [插件系统](./PLUGIN.md) - 插件架构与使用说明
- [API 参考](./API.md) - 详细 API 文档
- [高级用法](./ADVANCED.md) - 进阶场景与最佳实践
- [示例代码](./examples/) - 可运行的代码示例
```

#### 第四步：确保子模块可独立阅读

每个子模块必须包含：
- frontmatter（name、parent、version）
- 简短概述（2-3 句话介绍该模块内容）
- 完整内容（不依赖主文件即可理解）

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
```

### PLUGIN.md 子模块结构

```markdown
---
name: {Framework Name} 插件系统
parent: ./SKILL.md
version: 1.0.0
---

# {Framework Name} 插件系统

本模块介绍 {Framework Name} 的插件架构、官方插件列表及插件开发指南。

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

## 示例

> 完整模块化示例请参阅 [examples/page-agent-guide/](./examples/page-agent-guide/)

### 简化示例预览

生成的文档结构：
- SKILL.md：项目概述 + 安装 + 快速开始 + 子模块导航
- PLUGIN.md：Chrome 扩展集成 + MCP Server 集成
- API.md：PageAgent 类 + 配置类型 + 扩展 API

## 多语言支持

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

## 性能优化

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

## 技能协作

### 独立触发

本技能独立运行，不依赖其他技能路由。触发方式：
- 用户直接请求："帮我整理 XX 框架的文档"
- 用户提供 URL + "生成使用指南"

### 产出消费

生成的指南可被以下场景使用：
- 作为项目技能被 AI 读取和引用
- 作为新技能的基础材料
- 团队共享的框架参考文档

## 错误处理

### 错误分类与处理策略

| 错误类型 | 处理策略 |
|----------|----------|
| 网络超时 | 重试 3 次，指数退避 |
| URL 无效 | 提示用户检查 URL 格式 |
| 内容解析失败 | 尝试其他获取工具（按工具优先级切换） |
| 权限受限 | 提示需要登录或权限，建议提供文档 URL |
| 内容过大 | 建议指定章节范围或分页获取 |
| SPA 内容为空 | 按 Step 1.4 的降级流程处理 |

### 错误恢复流程

```
1. 记录错误详情
2. 按优先级尝试备选工具
3. 如全部失败，建议用户提供文档 URL 列表或手动输入
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

## 质量验证

### Step 5: 生成后质量检查

生成文档后，执行以下验证：

#### 完整性检查

- [ ] SKILL.md 包含项目概述和核心特性
- [ ] 安装方法覆盖项目的主要安装方式
- [ ] 快速开始有可运行的代码示例
- [ ] 每个子模块可独立阅读（不依赖主文件）
- [ ] 子模块导航链接正确
- [ ] 参考链接指向实际存在的资源

#### 代码示例验证

- [ ] 每个示例不超过 30 行
- [ ] import 语句使用正确的包名
- [ ] 配置参数与 API 文档一致
- [ ] 示例可独立运行（不依赖未定义的变量）

#### 版本信息验证

- [ ] frontmatter 中 framework_version 与最新版一致
- [ ] CDN 链接中的版本号正确
- [ ] 安装命令中的版本号正确

#### 质量评分

根据完成度打分：
- **A（优秀）**：所有检查项通过，代码示例丰富
- **B（良好）**：核心检查通过，部分示例可补充
- **C（基本）**：有核心内容但缺少示例或细节
- **D（不足）**：关键章节缺失，需要补充

如果评分低于 B，报告缺失项并建议补充。

## 更新模式

当用户要求更新已有框架指南时：

### Step U1: 识别变更

1. 读取现有指南的 frontmatter（version、framework_version、collected_date）
2. 检查框架最新版本（`npm view`、GitHub releases、官方文档）
3. 对比确定变更范围：
   - 版本号变化 → 检查 Changelog/Breaking Changes
   - 新增插件 → 仅更新 PLUGIN.md
   - API 变更 → 仅更新 API.md
   - 大版本升级 → 建议全量重新生成

### Step U2: 增量更新

- 仅修改变更的子模块文件
- 在 frontmatter 中更新 collected_date 和 framework_version
- 在 SKILL.md 末尾保留更新历史记录：

```markdown
## 更新记录

| 日期 | 版本 | 变更内容 |
|------|------|----------|
| 2026-05-12 | v2.0.0 | 新增 X 插件文档，API 变更同步 |
| 2026-01-15 | v1.0.0 | 初始版本 |
```

### Step U3: 验证一致性

- 检查子模块间的交叉引用是否仍然有效
- 确认代码示例与最新 API 一致

## 插件文档模板

当文档化插件时，使用以下结构：

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

### 开发自定义插件

```typescript
import { Plugin, pluginKey } from '{framework}'

const myPlugin = Plugin.create({
    name: 'myPlugin',
    setup(ctx) {
        // 插件初始化逻辑
    }
})
```
```

## 插件收集最佳实践

### 1. 插件发现

收集插件信息时：

1. **优先检查官方文档**
   - 查找 "Plugins" 或 "Extensions" 章节
   - 检查侧边栏导航中的插件列表

2. **搜索 NPM 注册表**
   ```
   npm search @framework-scope/plugin
   npm search framework-plugin
   ```

3. **探索 GitHub 仓库**
   - 检查 `/packages` 目录（monorepo 结构）
   - 查找 `/plugins` 或 `/extensions` 文件夹
   - 查阅 README 中的插件提及

4. **社区资源**
   - GitHub 上的 Awesome 列表
   - 社区论坛/Discord
   - Stack Overflow 标签

### 2. 插件文档检查清单

- [ ] 插件名和包标识
- [ ] 安装命令
- [ ] 基础用法示例
- [ ] 配置选项及类型
- [ ] 依赖和对等依赖
- [ ] 兼容性信息（版本要求）
- [ ] 已知问题或限制
- [ ] 源码/文档链接

### 3. 插件版本说明

始终记录：
- 所需的最低框架版本
- 主要版本间的破坏性变更
- 已废弃的插件及其替代品

## 输出要求

使用本技能时，始终：

1. 提供完整、可运行的代码示例
2. 适当情况下提供中英文文档
3. 在代码示例中添加适当的错误处理
4. 引用官方文档链接
5. 注明版本特定信息

## 更新日志

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| 2.0.0 | 2026-05-12 | 添加模块化拆分执行规则、多页文档站抓取策略、框架类型识别、质量验证、更新模式；修复协作关系和工具引用 |
| 1.1.0 | 2024-01-01 | 添加模块化输出结构、性能优化指导、技能协作说明、增强错误处理 |
| 1.0.0 | 2024-01-01 | 初始版本 |
