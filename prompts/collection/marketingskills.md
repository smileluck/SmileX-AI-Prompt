---
name: marketingskills
version: 1.10.0
author: Corey Haines
date: 2026-05-13
tags: [营销, CRO, 文案, SEO, 数据分析, 增长工程, AI Agent, Claude Code, 技能]
description: 面向 AI Agent 的 41 个专业营销技能模块，涵盖转化优化、文案撰写、SEO、数据分析和增长工程
model: Claude Code / OpenAI Codex / Cursor / Windsurf
---

# marketingskills 收录

## 仓库基本信息

| 属性 | 值 |
|------|-----|
| **仓库名称** | marketingskills |
| **原作者** | Corey Haines |
| **GitHub** | https://github.com/coreyhaines31/marketingskills |
| **官网** | https://marketing-skills.com |
| **星标** | ⭐ 28,210 |
| **Fork** | 4,549 |
| **许可证** | MIT |
| **技能总数** | 41 个 |
| **技能版本** | v1.10.0 |
| **主要语言** | JavaScript |
| **主题** | claude, codex, marketing |

## 项目简介

Marketing skills for Claude Code and AI agents. CRO, copywriting, SEO, analytics, and growth engineering.

**面向技术营销人员和创业者的 AI Agent 营销技能集合** —— 41 个专业营销技能模块，每个都包含专门的知识框架和工作流程，让 AI 编程助手协助完成转化优化、文案创作、SEO 审计、分析追踪和增长实验等营销任务。

### 技能协作机制

所有技能以 `product-marketing-context` 为基础，其他技能在执行前会先读取产品营销上下文，理解产品、受众和定位后再开展工作。技能之间可交叉引用，形成完整的营销工作流。

```
 ┌──────────────────────────────────────┐
 │ product-marketing-context            │
 │ (所有技能首先读取此基础)              │
 └──────────────────┬───────────────────┘
                    │
    ┌──────────────┼─────────────┬─────────────┬──────────────┬──────────────┐
    ▼              ▼             ▼             ▼              ▼              ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐ ┌──────────┐ ┌───────────┐
│SEO &内容 │ │CRO转化   │ │内容&文案 │ │付费&度量   │ │增长&留存 │ │策略&销售  │
├──────────┤ ├──────────┤ ├──────────┤ ├────────────┤ ├──────────┤ ├───────────┤
│seo-audit │ │page-cro  │ │copywriting│ │paid-ads   │ │referral  │ │revops     │
│ai-seo    │ │signup-cro│ │copy-edit │ │ad-creative│ │free-tool │ │sales-enable│
│site-arch │ │onboarding│ │cold-email│ │ab-test    │ │churn-    │ │launch     │
│programm  │ │form-cro  │ │email-seq │ │analytics  │ │ prevent  │ │pricing    │
│-seo      │ │popup-cro │ │social    │ │           │ │community │ │comp-alts  │
│schema    │ │paywall   │ │video     │ │           │ │lead-magnt│ │comp-profile│
│aso-audit │ │          │ │image     │ │           │ │co-mktg   │ │mktg-ideas │
│content   │ │          │ │          │ │           │ │directory │ │mktg-psych │
│-strategy │ │          │ │          │ │           │ │          │ │customer   │
│          │ │          │ │          │ │           │ │          │ │-research  │
└──────────┘ └──────────┘ └──────────┘ └────────────┘ └──────────┘ └───────────┘
```

## 快速开始

```bash
# CLI 安装（推荐）
npx skills add coreyhaines31/marketingskills

# 安装指定技能
npx skills add coreyhaines31/marketingskills --skill page-cro copywriting

# Claude Code 插件安装
/plugin marketplace add coreyhaines31/marketingskills
/plugin install marketing-skills

# Git Submodule 方式
git submodule add https://github.com/coreyhaines31/marketingskills.git .agents/marketingskills
```

## 技能分类目录

### 🔄 转化率优化 (CRO)

| 技能 | 说明 |
|------|------|
| page-cro | 营销页面转化优化（首页、落地页等） |
| signup-flow-cro | 注册/试用激活流程优化 |
| onboarding-cro | 注册后引导和激活优化 |
| form-cro | 非注册类表单转化优化（线索收集、联系表单等） |
| popup-cro | 弹窗/模态框/覆盖层转化优化 |
| paywall-upgrade-cro | 应用内付费墙和升级转化优化 |

### ✍️ 内容与文案 (Content & Copy)

| 技能 | 说明 |
|------|------|
| copywriting | 营销页面文案撰写和优化 |
| copy-editing | 现有营销文案编辑和润色 |
| cold-email | B2B 冷邮件和跟进序列 |
| email-sequence | 自动化邮件流和生命周期邮件 |
| social-content | 社交媒体内容创建和排期 |
| image | AI 图像生成、设计工具和优化 |
| video | AI 视频内容创作和制作 |

### 🔍 SEO 与发现 (SEO & Discovery)

| 技能 | 说明 |
|------|------|
| seo-audit | 技术和页面 SEO 审计 |
| ai-seo | AI 搜索优化（AEO、GEO、LLMO） |
| programmatic-seo | 规模化 SEO 页面生成 |
| site-architecture | 网站层级、导航、URL 结构规划 |
| competitor-alternatives | 竞品对比和替代页面创建 |
| schema-markup | 结构化数据标记 |
| content-strategy | 内容策略规划 |
| aso-audit | App Store / Google Play 列表优化 |
| directory-submissions | 产品提交到各类目录 |

### 💰 付费与分发 (Paid & Distribution)

| 技能 | 说明 |
|------|------|
| paid-ads | Google / Meta / LinkedIn 广告投放 |
| ad-creative | 批量广告素材生成和迭代 |

### 📊 度量与测试 (Measurement & Testing)

| 技能 | 说明 |
|------|------|
| analytics-tracking | 事件追踪和分析设置 |
| ab-test-setup | 实验设计和 A/B 测试 |

### 🔁 留存 (Retention)

| 技能 | 说明 |
|------|------|
| churn-prevention | 取消流程、挽留优惠、支付恢复 |

### 🚀 增长工程 (Growth Engineering)

| 技能 | 说明 |
|------|------|
| co-marketing | 联合营销伙伴识别和协作活动 |
| free-tool-strategy | 营销工具和计算器策略 |
| referral-program | 推荐和联盟计划 |
| community-marketing | 社区建设和运营 |
| lead-magnets | 铅磁铁/引流内容创建 |

### 🧠 策略与变现 (Strategy & Monetization)

| 技能 | 说明 |
|------|------|
| marketing-ideas | 140+ SaaS 营销创意 |
| marketing-psychology | 心理模型和行为科学在营销中的应用 |
| launch-strategy | 产品发布和公告策略 |
| pricing-strategy | 定价、包装和变现策略 |
| customer-research | 客户调研和洞察分析 |
| competitor-profiling | 竞品研究和分析 |

### 💼 销售与营收运营 (Sales & RevOps)

| 技能 | 说明 |
|------|------|
| revops | 营收运营、线索生命周期、管线管理 |
| sales-enablement | 销售资料、演示脚本、异议处理 |

### 📋 基础 (Foundation)

| 技能 | 说明 |
|------|------|
| product-marketing-context | 产品营销上下文（所有技能的基础依赖） |

## 使用方式

### 方式一：CLI 安装（推荐）

```bash
npx skills add coreyhaines31/marketingskills
```

### 方式二：Claude Code 插件

```
/plugin marketplace add coreyhaines31/marketingskills
/plugin install marketing-skills
```

### 方式三：自然语言调用

```
"帮我优化这个落地页的转化率"     → 使用 page-cro 技能
"为我的 SaaS 写首页文案"         → 使用 copywriting 技能
"设置 GA4 注册追踪"             → 使用 analytics-tracking 技能
"创建 5 封欢迎邮件序列"          → 使用 email-sequence 技能
```

### 方式四：直接调用

```
/page-cro
/email-sequence
/seo-audit
```

## 相关资源

- [Marketing Skills 官网](https://marketing-skills.com) - 技能详情和文档
- [Conversion Factory](https://conversionfactory.co) - Corey Haines 的转化优化机构
- [Swipe Files](https://swipefiles.com) - 营销知识和策略订阅
- [Magister](https://magistermarketing.com) - 使用这些技能的自主 AI CMO
- [Coding for Marketers](https://codingformarketers.com) - 营销人员编程指南

## 更新日志

- 2026-05-13: v1.0.0 - 收录 marketingskills 仓库（v1.10.0，41 个技能模块）
