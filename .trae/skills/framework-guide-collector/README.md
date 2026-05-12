# Framework Guide Collector

从网页 URL 收集并整理开发框架文档，自动生成模块化的 Markdown 使用指南。

## 解决什么问题

开发者在使用新框架时，往往需要反复查阅散落在多页文档站中的信息——安装方式在一个页面，API 参考在另一个页面，插件系统又是独立章节。本技能将这些分散的文档集中抓取、提取关键信息、按统一结构重新组织，生成一份可以直接被 AI 读取和引用的使用指南。

## 核心能力

| 能力 | 说明 |
|------|------|
| 多页文档站抓取 | 自动识别文档站导航结构（VitePress/Docusaurus/Next.js 等），遍历关键页面 |
| 框架类型适配 | 根据框架类型（UI 组件库/编辑器/构建工具/后端框架/测试框架/Agent）选择对应的章节模板 |
| 模块化输出 | 按内容量自动拆分为 SKILL.md + PLUGIN.md + API.md + ADVANCED.md，主入口精简、子模块完整 |
| 插件系统识别 | 自动检测框架的插件架构，收集官方和社区插件信息 |
| 增量更新 | 框架版本升级时，仅更新变化的子模块，避免全量重新生成 |
| 质量验证 | 生成后自动检查章节完整性、代码示例正确性、版本信息一致性 |

## 输入与产出

- **输入**：一个框架的文档 URL（官网、GitHub 仓库、文档站均可）
- **产出**：`project/skills/framework-guides/{framework-name}/` 下的模块化指南文件，可直接作为项目技能使用

## 适用场景示例

| 场景 | 输入 | 产出 |
|------|------|------|
| 集成新 UI 库 | Radix UI 文档站 URL | SKILL.md + API.md |
| 使用富文本编辑器 | Milkdown GitHub 仓库 | SKILL.md + PLUGIN.md + API.md |
| 搭建后端服务 | FastAPI 官方文档 | SKILL.md + API.md + ADVANCED.md |
| 更新已有指南 | "更新 page-agent 指南" | 仅更新变更的子模块 |

## 与 skill-collector 的区别

| | skill-collector | framework-guide-collector |
|---|---|---|
| 目的 | 收录现成的技能文件 | 从文档生成新的使用指南 |
| 输入 | GitHub 仓库或 Skills.sh 链接 | 任意框架文档 URL |
| 产出 | 原样保存技能文件 | 结构化的模块化指南 |
| 适用 | 已有 SKILL.md 的项目 | 需要自己整理文档的框架 |

## 目录结构

```
framework-guide-collector/
├── README.md                    # 本文件：技能介绍
├── SKILL.md                     # 技能定义：工作流程、输出规范、模板
└── examples/
    └── page-agent-guide/        # 完整模块化示例
        ├── SKILL.md             # 主入口
        ├── PLUGIN.md            # 插件系统
        └── API.md               # API 参考
```
