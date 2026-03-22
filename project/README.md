---
name: 开源项目管理
version: 1.1.0
author: SmileX
date: 2026-03-10
tags: [opensource, submodule, git]
description: 管理开源项目的 Git Submodule 使用指南
model: 通用
---

# 开源项目管理

本目录用于通过 Git Submodule 管理相关的开源项目。

## 目录结构

```
project/
├── README.md              # 本说明文件
├── opensource/            # 开源项目目录
│   ├── system-prompts-and-models-of-ai-tools/  # AI 工具系统提示词和模型
│   └── [其他项目]/        # 其他开源项目目录（通过 Git Submodule 管理）
├── llm/                   # LLM 仓库追踪目录
│   ├── awesome-llm-apps/ # awesome-llm-apps 追踪信息
│   └── [其他项目]/        # 其他 LLM 相关仓库
├── web-clone/             # Web克隆项目目录
│   ├── luma-front/        # Luma Front 项目
│   └── [其他项目]/        # 其他Web克隆项目目录（通过 Git Submodule 管理）
└── .gitmodules           # Git Submodule 配置文件
```

## 已追踪的仓库

### LLM 相关

| 项目名称 | 目录路径 | 仓库地址 | 描述 |
|---------|---------|---------|------|
| awesome-llm-apps | project/llm/awesome-llm-apps | https://github.com/Shubhamsaboo/awesome-llm-apps | Collection of awesome LLM apps with AI Agents and RAG using OpenAI, Anthropic, Gemini and opensource models. ⭐ 103090 |

### 开源项目

| 项目名称 | 目录路径 | 仓库地址 | 描述 |
|---------|---------|---------|------|
| system-prompts-and-models-of-ai-tools | project/opensource/system-prompts-and-models-of-ai-tools | https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools | 收集了 30+ AI 工具的系统提示词、内部工具和 AI 模型，包括 Claude Code、Cursor、Devin AI、Replit、Trae、Windsurf 等 |
| luma-front | project/web-clone/luma-front | https://github.com/words-of-wisdom/luma-front | Web克隆项目 |

### Git Submodule

> 以下项目通过 Git Submodule 管理：

| 项目名称 | 目录路径 | 仓库地址 | 描述 |
|---------|---------|---------|------|

## 使用指南

### 1. 添加开源项目到本地

使用 Git Submodule 将开源项目添加到本地：

```bash
# 添加新的开源项目
git submodule add <仓库地址> project/opensource/<项目名称>

# 示例
git submodule add https://github.com/example/project.git project/opensource/example-project
```

**注意事项：**
- `<仓库地址>`：开源项目的 Git 仓库地址
- `<项目名称>`：在本地保存的目录名称
- 添加后会自动生成 `.gitmodules` 文件

### 2. 克隆包含 Submodule 的仓库

当克隆本仓库时，需要额外步骤来初始化和更新 Submodule：

```bash
# 克隆主仓库
git clone <主仓库地址>

# 进入项目目录
cd SmileX-AI-Prompt

# 初始化 Submodule
git submodule init

# 更新 Submodule（拉取子模块内容）
git submodule update

# 或者使用一条命令完成初始化和更新
git submodule update --init --recursive
```

### 3. 更新开源项目

定期更新 Submodule 以获取最新的开源项目代码：

```bash
# 更新所有 Submodule 到最新版本
git submodule update --remote

# 更新指定的 Submodule
git submodule update --remote project/opensource/<项目名称>

# 进入子模块目录手动更新
cd project/opensource/<项目名称>
git pull origin main
```

### 4. 查看子模块状态

```bash
# 查看所有子模块的状态
git submodule status

# 输出说明：
# - 开头为空：子模块与主仓库记录的版本一致
# - 开头为 +：子模块有新的提交
# - 开头为 -：子模块未初始化
```

### 5. 删除子模块

如果需要移除某个开源项目：

```bash
# 1. 删除子模块的配置
git submodule deinit project/opensource/<项目名称>

# 2. 删除 .git/modules 中的相关目录
git rm -f project/opensource/<项目名称>

# 3. 删除本地目录（如果还存在）
rm -rf .git/modules/project/opensource/<项目名称>

# 4. 提交更改
git commit -m "移除子模块：<项目名称>"
```

## 工作流程建议

### 日常使用

1. **首次设置**：克隆仓库后运行 `git submodule update --init --recursive`
2. **定期更新**：运行 `git submodule update --remote` 更新所有子模块
3. **提交更改**：如果修改了子模块版本，记得提交 `.gitmodules` 文件

### 版本锁定

默认情况下，Submodule 会锁定到特定的 commit，确保团队协作时使用相同的版本：

```bash
# 查看当前子模块的 commit 版本
cd project/opensource/<项目名称>
git log -1

# 如果需要切换到特定版本
git checkout <commit-hash>
cd ../..
git add project/opensource/<项目名称>
git commit -m "锁定子模块版本到 <commit-hash>"
```

## 常见问题

### Q: 为什么 Submodule 目录是空的？

**A:** 需要运行初始化命令：
```bash
git submodule update --init --recursive
```

### Q: 如何在 Submodule 中进行开发？

**A:** 有两种方式：

1. **直接修改**（不推荐）：在 Submodule 目录中修改并提交，但这会修改外部仓库
2. **Fork 后使用**（推荐）：Fork 原项目，修改自己的 Fork 版本，然后将 Submodule 指向你的 Fork

### Q: Submodule 更新后如何同步到团队？

**A:** 更新 Submodule 后，需要提交 `.gitmodules` 和子模块的引用：
```bash
git add project/opensource/<项目名称>
git commit -m "更新子模块：<项目名称>"
git push
```

## 更新日志

- 2026-03-10: v1.1.0 - 添加 luma-front 项目到 web-clone 目录
- 2026-03-10: v1.0.0 - 初始版本，创建 Submodule 管理指南
