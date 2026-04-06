---
name: "claw-code"
version: "latest"
author: "ultraworkers"
date: 2026-04-06
tags: [claude-code, rust, cli, agent, harness, open-source]
description: "Public Rust implementation of the claw CLI agent harness - the fastest repo to surpass 100K stars"
source: "https://github.com/ultraworkers/claw-code"
---

# Claw Code

## 功能描述

Claw Code 是 claw CLI agent harness 的公开 Rust 实现。这是历史上最快突破 100K 星标的仓库。

## 重要声明

> **此仓库不声称拥有原始 Claude Code 源材料的所有权。**
> **此仓库不隶属于、不由 Anthropic 认可或维护。**

## 仓库结构

```
claw-code/
├── rust/              # 规范的 Rust 工作区和 claw CLI 二进制文件
├── USAGE.md           # 面向任务的使用指南
├── PARITY.md          # Rust 移植一致性状态和迁移说明
├── ROADMAP.md         # 活跃路线图和清理待办事项
├── PHILOSOPHY.md      # 项目意图和系统设计框架
├── src/ + tests/      # 配套 Python/参考工作区和审计助手
└── docs/              # 文档
```

## 快速开始

### 构建项目

```bash
cd rust
cargo build --workspace
./target/debug/claw --help
./target/debug/claw prompt "summarize this repository"
```

### 身份验证

使用 API 密钥或内置 OAuth 流程：

```bash
# 方法 1: API 密钥
export ANTHROPIC_API_KEY="sk-ant-..."

# 方法 2: OAuth 流程
cd rust
./target/debug/claw login
```

### 运行测试

```bash
cd rust
cargo test --workspace
```

## 文档地图

| 文档 | 描述 |
|------|------|
| USAGE.md | 快速命令、认证、会话、配置、一致性测试工具 |
| rust/README.md | crate 地图、CLI 接口、功能、工作区布局 |
| PARITY.md | Rust 移植的一致性状态 |
| rust/MOCK_PARITY_HARNESS.md | 确定性模拟服务测试工具详情 |
| ROADMAP.md | 活跃路线图和开放清理工作 |
| PHILOSOPHY.md | 项目存在原因和运营方式 |
| docs/container.md | 容器优先工作流 |

## 核心组件

### rust/ — 规范 Rust 工作区

- claw CLI 二进制文件
- 主要运行时表面

### src/ + tests/ — 配套工作区

- Python/参考工作区
- 审计助手
- 非主要运行时表面

## 生态系统

Claw Code 与更广泛的 UltraWorkers 工具链一起构建：

| 项目 | 链接 |
|------|------|
| clawhip | UltraWorkers 生态 |
| oh-my-openagent | UltraWorkers 生态 |
| oh-my-claudecode | UltraWorkers 生态 |
| oh-my-codex | UltraWorkers 生态 |
| Discord | https://discord.gg/5TUQKqFWd |

## 关键特性

1. **Rust 实现**：高性能、内存安全的 CLI agent harness
2. **OAuth 支持**：内置认证流程
3. **容器优先**：支持容器化工作流
4. **模拟测试工具**：确定性测试支持
5. **开放源代码**：完全公开的 Rust 实现

## 使用建议

1. 从 **USAGE.md** 开始了解构建、认证、CLI、会话和一致性测试工作流
2. 构建后首先运行 `claw doctor` 进行健康检查
3. 参考 **rust/README.md** 了解 crate 级别详情
4. 阅读 **PARITY.md** 了解当前 Rust 移植检查点
5. 查看 **docs/container.md** 了解容器优先工作流

## 系统要求

- Rust 工具链
- Cargo
- Anthropic API 密钥（用于完整功能）

## 安装

```bash
git clone https://github.com/ultraworkers/claw-code.git
cd claw-code/rust
cargo build --workspace
```

## 相关链接

- GitHub: https://github.com/ultraworkers/claw-code
- Discord: https://discord.gg/5TUQKqFWd
