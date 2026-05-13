# GitHub Repository Collector

## 功能描述

从 GitHub 仓库收录项目信息，**不克隆到本地**，仅收集元数据并生成中英双语说明，更新到对应分类的 README。

> 克隆操作已禁用，仅执行元数据追踪和文档更新。

## 触发条件

- "收录这个 github 仓库：{url}"
- "添加 {url} 到项目"
- "追踪这个仓库"
- 其他包含 GitHub URL 的收录请求

## 执行步骤

### 1. 解析 URL

从 GitHub URL 中提取信息：

| URL 格式 | 提取规则 |
|----------|----------|
| `https://github.com/{owner}/{repo}` | 直接提取 owner/repo |
| `https://github.com/{owner}/{repo}.git` | 去掉 .git 后缀 |
| `git@github.com:{owner}/{repo}.git` | 提取 owner/repo |
| `https://github.com/{owner}/{repo}/tree/{branch}` | 提取 owner/repo，忽略 branch |
| `https://github.com/{owner}/{repo}/blob/{branch}/{file}` | 提取 owner/repo，忽略分支和文件 |

### 2. 获取仓库元数据

使用 GitHub API（`https://api.github.com/repos/{owner}/{repo}`）获取：

| 字段 | API 字段 | 说明 |
|------|----------|------|
| 项目名 | `name` | 仓库名称 |
| 描述 | `description` | 英文原描述 |
| 星标 | `stargazers_count` | Star 数 |
| Fork | `forks_count` | Fork 数 |
| 语言 | `language` | 主要编程语言 |
| 许可证 | `license.spdx_id` | 开源许可证 |
| 主题 | `topics` | 仓库标签 |
| 最后更新 | `updated_at` | 最近更新时间 |

### 3. 生成中英双语说明

将英文描述翻译为中文，补充适用场景。技术术语保留英文原文。

**翻译规范：**
- 准确传达项目核心功能
- 补充项目的适用场景和典型用例
- 技术术语保持英文（如 React、FastAPI、MCP 等）
- 中文描述应比原文更易理解，而非逐字翻译

### 4. 确定收录分类

根据项目类型选择分类目录：

| 分类 | 目录 | 适用项目 |
|------|------|----------|
| opensource | `project/opensource/` | 通用开源项目 |
| llm | `project/llm/` | LLM/AI 相关项目 |
| tools | `project/tools/` | 开发工具类项目 |
| skills | `project/skills/` | AI 技能/Skill 项目 |
| web-clone | `project/web-clone/` | 网站克隆项目 |

如果用户指定了分类，使用用户指定的分类。否则根据项目内容和 topics 自动判断。

### 5. 更新 README

在对应分类目录的 README.md 中添加条目。

## 条目格式

```markdown
### [项目名](GitHub URL)
- **收录时间**: YYYY-MM-DD
- **星标**: ⭐ 数量
- **语言**: 主要编程语言
- **许可证**: 许可证类型
- **描述**: 中文描述（翻译 + 适用场景补充）
- **Description**: English original description
- **主题**: topic1, topic2, topic3
```

如果 README.md 已有同名条目，更新其信息而非重复添加。

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| URL 格式无效 | 提示正确格式并给出示例 |
| 仓库不存在 | 提示仓库可能已删除或更名 |
| API 速率限制 | 提示稍后重试，或由用户提供描述信息 |
| 网络连接失败 | 提示检查网络，支持用户手动输入描述 |
| 私有仓库 | 尝试获取公开信息，标注为私有仓库 |
| 分类目录不存在 | 提示可用分类列表，默认使用 opensource |

## 注意事项

1. **禁止克隆**：任何情况下不执行 git clone 或 git submodule add
2. **双语必填**：每个条目必须同时包含中文描述和英文原文
3. **格式统一**：所有分类目录使用相同的条目格式
4. **幂等操作**：重复收录同一仓库只更新不重复
