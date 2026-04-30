---
name: agent-skills
description: Production-grade engineering skills for AI coding agents. 包含 20 个结构化技能，涵盖 Define、Plan、Build、Verify、Review、Ship 全流程。适用于 Claude Code、Cursor、Windsurf、Gemini CLI 等主流 AI 编程工具。
useWhen: 需要为 AI 编程代理提供结构化工程工作流程时使用，包括任务分解、代码开发、测试验证、代码审查和发布部署等场景。
---

# Agent Skills

Production-grade engineering skills for AI coding agents.

## 概述

Agent Skills 将高级工程师的工作流程、质量门禁和最佳实践编码为技能包，使 AI 代理在开发的每个阶段都能一致地遵循这些标准。

## 核心命令 (7 Slash Commands)

| 命令 | 功能 | 关键原则 |
|------|------|---------|
| `/spec` | 定义要构建的内容 | 先规格后代码 |
| `/plan` | 规划如何构建 | 小而原子的任务 |
| `/build` | 增量构建 | 一次一个切片 |
| `/test` | 证明它有效 | 测试即证明 |
| `/review` | 合并前审查 | 提升代码健康度 |
| `/code-simplify` | 简化代码 | 清晰优于聪明 |
| `/ship` | 交付生产 | 更快即更安全 |

## 技能分类 (20 Skills)

### Define - 明确要构建什么

| 技能 | 功能 | 使用场景 |
|------|------|---------|
| `idea-refine` | 结构化发散/收敛思维，将模糊想法转化为具体提案 | 有一个需要探索的粗略概念 |
| `spec-driven-development` | 编写涵盖目标、命令、结构、代码风格、测试和边界的 PRD | 启动新项目、功能或重大变更 |

### Plan - 分解任务

| 技能 | 功能 | 使用场景 |
|------|------|---------|
| `planning-and-task-breakdown` | 将规格分解为可验证的任务，包含验收标准和依赖排序 | 已有规格，需要可实现的单元 |

### Build - 编写代码

| 技能 | 功能 | 使用场景 |
|------|------|---------|
| `incremental-implementation` | 薄垂直切片 - 实现、测试、验证、提交。特性开关、安全默认值、回滚友好变更 | 任何涉及多个文件的变更 |
| `test-driven-development` | 红-绿-重构，测试金字塔 (80/15/5)，测试规模，DAMP 优于 DRY，Beyonce 规则，浏览器测试 | 实现逻辑、修复 bug 或改变行为 |
| `context-engineering` | 在正确时间为代理提供正确信息 - 规则文件、上下文打包、MCP 集成 | 启动会话、切换任务或输出质量下降 |
| `source-driven-development` | 将每个框架决策基于官方文档 - 验证、引用、标记未验证项 | 希望获得权威的、有据可查的代码 |
| `frontend-ui-engineering` | 组件架构、设计系统、状态管理、响应式设计、WCAG 2.1 AA 可访问性 | 构建或修改用户界面 |
| `api-and-interface-design` | 契约优先设计、Hyrum's Law、单版本规则、错误语义、边界验证 | 设计 API、模块边界或公共接口 |

### Verify - 证明它有效

| 技能 | 功能 | 使用场景 |
|------|------|---------|
| `browser-testing-with-devtools` | Chrome DevTools MCP 获取实时运行时数据 - DOM 检查、控制台日志、网络追踪、性能分析 | 构建或调试任何在浏览器中运行的内容 |
| `debugging-and-error-recovery` | 五步排查：复现、定位、减少、修复、防护。停止线规则、安全 fallback | 测试失败、构建中断或行为异常 |

### Review - 合并前的质量门禁

| 技能 | 功能 | 使用场景 |
|------|------|---------|
| `code-review-and-quality` | 五轴审查，变更规模 (~100 行)，严重性标签 (Nit/Optional/FYI)，审查速度规范，分割策略 | 任何合并前的变更 |
| `code-simplification` | Chesterton's Fence，500 规则，在保持精确行为的同时降低复杂度 | 代码可以工作但比应有的更难阅读或维护 |
| `security-and-hardening` | OWASP Top 10 预防、认证模式、密钥管理、依赖审计、三层边界系统 | 处理用户输入、认证、数据存储或外部集成 |
| `performance-optimization` | 测量优先方法 - Core Web Vitals 目标、性能分析工作流、bundle 分析、反模式检测 | 存在性能要求或怀疑存在性能回归 |

### Ship - 部署信心

| 技能 | 功能 | 使用场景 |
|------|------|---------|
| `git-workflow-and-versioning` | 基于主干的开发、原子提交、变更规模 (~100 行)、提交即保存点模式 | 任何代码变更（始终使用） |
| `ci-cd-and-automation` | 左移、更快即更安全、特性开关、质量门禁管道、失败反馈循环 | 设置或修改构建和部署管道 |
| `deprecation-and-migration` | 代码作为负债思维、强制性 vs 建议性弃用、迁移模式、僵尸代码移除 | 移除旧系统、迁移用户或淘汰功能 |
| `documentation-and-adrs` | 架构决策记录、API 文档、内联文档标准 - 记录原因 | 做出架构决策、更改 API 或发布功能 |
| `shipping-and-launch` | 发布前检查清单、特性开关生命周期、分阶段 rollout、回滚程序、监控设置 | 准备部署到生产环境 |

## 支持的工具

### Claude Code (推荐)

安装命令：
```bash
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

本地开发：
```bash
git clone https://github.com/addyosmani/agent-skills.git
claude --plugin-dir /path/to/agent-skills
```

### Cursor

将任何 `SKILL.md` 复制到 `.cursor/rules/`，或引用完整的 `skills/` 目录。

### Gemini CLI

```bash
gemini skills install https://github.com/addyosmani/agent-skills.git --path skills
```

### Windsurf

将技能内容添加到 Windsurf rules 配置。

### OpenCode

通过 `AGENTS.md` 和 skill tool 使用代理驱动的技能执行。

### GitHub Copilot

将 agents/ 中的代理定义用作 Copilot personas，将技能内容放在 `.github/copilot-instructions.md`。

### Kiro IDE & CLI

技能位于 `.kiro/skills/` 下，可存储在项目或全局级别。

## 技能结构

每个技能遵循一致的 anatomy：

```
SKILL.md
├── Frontmatter (name, description, useWhen)
├── Overview          → 这个技能做什么
├── When to Use      → 触发条件
├── Process          → 逐步工作流
├── Rationalizations  → 借口 + 反驳
├── Red Flags        → 出问题的迹象
└── Verification     → 证据要求
```

## 设计原则

1. **流程而非文章** - 技能是代理遵循的工作流，不是参考文档
2. **反理性化** - 每个技能包含常见借口的表格及反驳论证
3. **验证不可协商** - 每个技能以证据要求结束
4. **渐进式披露** - SKILL.md 是入口点，支持引用仅在需要时加载

## 项目结构

```
agent-skills/
├── skills/                    # 20 个核心技能
│   ├── idea-refine/           # Define
│   ├── spec-driven-development/
│   ├── planning-and-task-breakdown/
│   ├── incremental-implementation/
│   ├── context-engineering/
│   ├── source-driven-development/
│   ├── frontend-ui-engineering/
│   ├── test-driven-development/
│   ├── api-and-interface-design/
│   ├── browser-testing-with-devtools/
│   ├── debugging-and-error-recovery/
│   ├── code-review-and-quality/
│   ├── code-simplification/
│   ├── security-and-hardening/
│   ├── performance-optimization/
│   ├── git-workflow-and-versioning/
│   ├── ci-cd-and-automation/
│   ├── deprecation-and-migration/
│   ├── documentation-and-adrs/
│   ├── shipping-and-launch/
│   └── using-agent-skills/
├── agents/                    # 3 个专家角色
├── references/                # 4 个补充检查清单
├── hooks/                     # 会话生命周期钩子
├── .claude/commands/          # 7 个 slash 命令
└── docs/                      # 每个工具的设置指南
```

## 参考检查清单

| 参考 | 覆盖内容 |
|------|---------|
| `testing-patterns.md` | 测试结构、命名、mock、React/API/E2E 示例、反模式 |
| `security-checklist.md` | 提交前检查、认证、输入验证、Headers、CORS、OWASP Top 10 |
| `performance-checklist.md` | Core Web Vitals 目标、前端/后端检查清单、测量命令 |
| `accessibility-checklist.md` | 键盘导航、屏幕阅读器、视觉设计、ARIA、测试工具 |

## Agent Personas

| 角色 | 视角 |
|------|------|
| `code-reviewer` | 高级 Staff 工程师 - 五轴代码审查 |
| `test-engineer` | QA 专家 - 测试策略、覆盖率分析、Prove-It 模式 |
| `security-auditor` | 安全工程师 - 漏洞检测、威胁建模、OWASP 评估 |

## 来源

本技能包包含来自 Google 工程文化的最佳实践，包括：
- Software Engineering at Google 的概念
- Hyrum's Law (API 设计)
- Beyonce Rule 和测试金字塔 (测试)
- 变更规模和审查速度规范 (代码审查)
- Chesterton's Fence (简化)
- 基于主干的开发 (git 工作流)
- 左移和特性开关 (CI/CD)
- 代码作为负债的弃用技能

## 许可证

MIT - 可在项目、团队和工具中使用这些技能。

## 仓库信息

- **仓库**: addyosmani/agent-skills
- **星标**: 25,337
- **Fork**: 3,138
- **语言**: Shell
- **许可证**: MIT
- **最新版本**: 0.5.0
