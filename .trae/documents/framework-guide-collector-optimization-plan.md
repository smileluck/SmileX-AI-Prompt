# Framework-Guide-Collector 技能优化计划

## 一、当前技能分析

### 1.1 现有结构

```
framework-guide-collector/
└── SKILL.md  (约 490 行)
```

### 1.2 优点

- ✅ 工作流程清晰，分为 4 个主要步骤
- ✅ 提供了详细的插件系统检测指南
- ✅ 包含完整的文档模板
- ✅ 有实际的示例（Page-Agent）
- ✅ 错误处理有基本覆盖

### 1.3 待优化问题

| 问题 | 严重程度 | 描述 |
|------|----------|------|
| 元信息不完整 | 中 | 缺少 version、author、date、tags |
| 示例过于冗长 | 高 | Page-Agent 示例占据约 130 行，影响可读性 |
| 缺少版本管理 | 中 | 没有更新日志机制 |
| 输出路径不明确 | 中 | 生成的文档应存储位置未定义 |
| 多语言策略模糊 | 低 | 提到中英文但无明确策略 |
| 性能指导缺失 | 中 | 大型文档处理无优化建议 |
| 技能协作未说明 | 低 | 与其他技能的协作关系未定义 |
| 错误处理不够细致 | 中 | 缺少错误分类和恢复策略 |

---

## 二、优化建议

### 2.1 元信息增强

**当前：**
```markdown
---
name: "framework-guide-collector"
description: "..."
---
```

**优化后：**
```markdown
---
name: "framework-guide-collector"
version: "1.1.0"
author: "SmileX Team"
date: "2024-01-01"
tags: [documentation, framework, web-scraping, guide-generation]
description: "Collects and organizes development framework documentation from URLs..."
min_trust_level: "normal"
dependencies: []
---
```

### 2.2 示例分离优化

**问题：** Page-Agent 示例过长（约 130 行），影响技能文件可读性

**方案：** 将示例分离到独立文件

```
framework-guide-collector/
├── SKILL.md              # 主技能文件（精简版）
└── examples/
    └── page-agent-guide.md  # 完整示例
```

**SKILL.md 中保留精简引用：**
```markdown
## Example Usage

> 完整示例请参阅 [examples/page-agent-guide.md](./examples/page-agent-guide.md)

### 简化示例预览

生成的文档结构：
- 项目概述
- 安装方法
- 快速开始
- API 参考
- 插件系统（如适用）
- 高级用法
- 约束与限制
```

### 2.3 添加版本管理机制

在技能文件末尾添加：

```markdown
## 更新日志

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| 1.1.0 | 2024-XX-XX | 添加插件系统检测流程，优化文档模板 |
| 1.0.0 | 2024-XX-XX | 初始版本 |
```

### 2.4 明确输出路径规范（模块化结构）⭐ 重点优化

添加输出规范章节：

```markdown
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
```

### 2.5 多语言支持策略

```markdown
## Multi-language Support

### 语言选择规则

1. **默认语言**：根据用户输入语言决定
2. **框架文档语言**：优先使用官方文档的原始语言
3. **双语支持**：对于国际化框架，提供中英双语版本

### 双语文档结构

```
framework-guides/
├── react-guide.md        # 中文版
└── react-guide.en.md     # 英文版
```
```

### 2.6 性能优化指导

```markdown
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
```

### 2.7 技能协作说明

```markdown
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
```

### 2.8 错误处理增强

```markdown
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
```

---

## 三、优化实施步骤

### 步骤 1：重构目录结构
- 创建 `examples/` 目录
- 将 Page-Agent 示例分离到独立文件

### 步骤 2：更新 SKILL.md
- 增强元信息
- 精简示例部分
- 添加输出规范章节
- 添加性能优化章节
- 添加技能协作说明
- 增强错误处理章节
- 添加版本管理

### 步骤 3：验证与测试
- 检查技能文件格式
- 验证链接有效性
- 确保与现有工作流兼容

---

## 四、优化后的目录结构

### 技能自身结构

```
framework-guide-collector/
├── SKILL.md                      # 主技能文件（约 300 行，精简后）
└── examples/
    └── page-agent-guide/         # 完整示例（模块化）
        ├── SKILL.md              # Page-Agent 主指南
        └── PLUGIN.md             # Page-Agent 插件说明（如有）
```

### 生成的框架指南结构（模块化）

```
project/skills/framework-guides/
├── react/
│   ├── SKILL.md                  # React 核心使用指南
│   ├── PLUGIN.md                 # React 插件/生态
│   ├── API.md                    # React API 参考
│   └── examples/
│       └── hooks-usage.md        # Hooks 示例
├── vue/
│   ├── SKILL.md                  # Vue 核心使用指南
│   └── PLUGIN.md                 # Vue 插件生态
└── milkdown/
    ├── SKILL.md                  # Milkdown 核心指南
    ├── PLUGIN.md                 # Milkdown 插件系统
    └── examples/
        └── basic-editor.md       # 基础编辑器示例
```

---

## 五、预期效果

### 技能文件优化效果

| 指标 | 优化前 | 优化后 |
|------|--------|--------|
| SKILL.md 行数 | ~490 行 | ~300 行 |
| 可读性 | 中等 | 高 |
| 可维护性 | 中等 | 高 |
| 错误处理覆盖 | 基础 | 完善 |
| 文档规范性 | 模糊 | 明确 |

### 模块化结构优势

| 优势 | 说明 |
|------|------|
| 主入口清晰 | SKILL.md 作为主入口，不会被大量内容淹没 |
| 按需查阅 | 用户可根据需要查阅 PLUGIN.md、API.md 等子模块 |
| 易于维护 | 各模块职责单一，更新时只需修改对应模块 |
| 便于扩展 | 可根据框架特点灵活添加新的子模块 |
| 复用性强 | 子模块可被其他技能或文档引用 |

### 模块化生成策略

```markdown
## 生成策略

### 必须生成
- SKILL.md（主入口）

### 条件生成
- PLUGIN.md：当检测到框架有插件系统时生成
- API.md：当框架 API 较复杂时生成
- ADVANCED.md：当有高级用法内容时生成

### 可选生成
- examples/：根据用户需求生成示例代码
```
