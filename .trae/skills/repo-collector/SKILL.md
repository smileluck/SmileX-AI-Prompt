---
name: "repo-collector"
description: "Automatically adds GitHub repositories as submodules and updates README. Invoke when user says '将某个github的地址收录' or requests to add/include a GitHub repository."
---

# Repository Collector

## 功能描述

本技能用于自动化收录GitHub仓库到项目中，包括添加git子模块和更新README文档。

## 触发条件

当用户说出以下指令时激活本技能：
- "将某个github的地址收录"
- "收录这个github仓库"
- "添加这个仓库到项目"
- "添加git submodule"
- 其他类似的收录仓库请求

其中"某个github的地址"为用户提供的具体GitHub仓库URL。

## 执行步骤

### 1. 位置选择
- 根据用户描述提供的分类信息（如"opensource"），确定仓库的收录位置
- 默认位置为：`project/opensource/`
- 支持多种收录位置的选择，至少包括opensource分类
- 如果用户未指定位置，使用默认位置

### 2. 仓库添加操作
- 优先使用 HTTPS 协议执行 git submodule add 命令
- 命令格式：`git submodule add <用户提供的GitHub仓库地址> project/opensource/<从仓库URL提取的项目名称>`
- 正确解析用户提供的GitHub仓库URL，提取项目名称
- 项目名称提取规则：
  - 从URL中提取最后一个路径段
  - 移除.git后缀（如果存在）
  - 示例：`https://github.com/user/project-name.git` → `project-name`
- **HTTPS 失败自动重试机制**：
  - 当 HTTPS 协议下载失败时，自动将 URL 转换为 SSH 格式并重试
  - HTTPS 到 SSH 转换规则：
    - `https://github.com/user/repo.git` → `git@github.com:user/repo.git`
    - `https://github.com/user/repo` → `git@github.com:user/repo.git`
  - 重试前记录失败原因，重试成功后记录使用的协议
  - 最多重试一次（HTTPS → SSH）

### 3. 文档更新功能
- 自动修改project目录下的readme.md文件
- 添加新收录仓库的相关信息，包括：
  - 仓库名称
  - URL
  - 收录时间（格式：YYYY-MM-DD）
  - 简要描述（如果用户提供）
- 按照预设格式更新readme.md文件，保持文档结构清晰
- 如果readme.md不存在，创建新文件

### 4. 错误处理
确保git submodule命令执行成功，并处理可能的错误情况：
- **仓库已存在**：提示用户该仓库已被收录，询问是否需要更新
- **HTTPS 下载失败**：
  - 自动将 URL 转换为 SSH 格式并重试
  - 如果 SSH 也失败，提示用户检查网络连接或 SSH 密钥配置
  - 记录失败原因和重试过程
- **网络问题**：提示网络连接问题，建议检查网络后重试
- **权限问题**：
  - HTTPS 权限问题：自动尝试 SSH，如仍失败则提示配置 SSH 密钥
  - SSH 权限问题：提示检查 SSH 密钥是否已添加到 GitHub 账户
- **URL无效**：提示URL格式错误，请用户提供正确的GitHub仓库URL
- **目录已存在**：提示目标目录已存在，询问是否覆盖
- **SSH 密钥未配置**：提供 SSH 密钥配置指引

### 5. 反馈机制
操作完成后提供明确的成功/失败反馈：
- **成功**：显示"仓库收录成功！"，并列出收录的仓库信息
- **失败**：显示具体的错误信息和解决建议

## 技术要求

1. **URL解析**：
   - 支持多种GitHub URL格式：
     - `https://github.com/user/repo.git`
     - `https://github.com/user/repo`
     - `git@github.com:user/repo.git`
   - 正确提取项目名称

2. **URL 转换**：
   - 实现 HTTPS 到 SSH 的自动转换功能
   - 转换算法：
     - 解析 HTTPS URL 提取用户名和仓库名
     - 重组为 SSH 格式：`git@github.com:<user>/<repo>.git`
   - 处理带 .git 和不带 .git 后缀的 URL
   - 验证转换后的 URL 格式正确性

3. **Git操作**：
   - 优先使用 HTTPS 协议执行 git submodule add 命令
   - 检测 HTTPS 失败的错误类型（网络错误、权限错误等）
   - 失败时自动转换为 SSH 并重试
   - 验证命令执行结果
   - 处理git命令的输出和错误
   - 记录使用的协议（HTTPS 或 SSH）

4. **文档更新**：
   - 读取现有的readme.md文件
   - 按照统一格式添加新仓库信息
   - 保持文档结构清晰
   - 更新后保存文件

## README更新格式

在readme.md中添加以下格式的内容：

```markdown
## 收录仓库

### [项目名称](仓库URL)
- **收录时间**: YYYY-MM-DD
- **描述**: [简要描述，如果用户提供]
```

如果readme.md中已有"收录仓库"章节，则在该章节下添加新仓库信息。

## 质量标准

1. **响应时间**：技能响应时间不超过5秒
2. **成功率**：仓库添加成功率达到95%以上
3. **文档格式**：readme.md文件更新格式统一、信息准确
4. **错误提示**：提供友好的错误提示和解决建议

## 使用示例

### 示例1：基本收录
用户输入："将 https://github.com/user/project 收录到 opensource"

执行步骤：
1. 确认收录位置：project/opensource/
2. 提取项目名称：project
3. 执行命令：`git submodule add https://github.com/user/project project/opensource/project`
4. 更新readme.md，添加项目信息
5. 返回成功信息

### 示例2：带描述的收录
用户输入："将 https://github.com/user/awesome-lib 收录，这是一个很棒的库"

执行步骤：
1. 确认收录位置：project/opensource/
2. 提取项目名称：awesome-lib
3. 执行命令：`git submodule add https://github.com/user/awesome-lib project/opensource/awesome-lib`
4. 更新readme.md，添加项目信息和描述
5. 返回成功信息

### 示例3：指定位置
用户输入："将 https://github.com/user/tool 收录到 project/tools"

执行步骤：
1. 确认收录位置：project/tools/
2. 提取项目名称：tool
3. 执行命令：`git submodule add https://github.com/user/tool project/tools/tool`
4. 更新readme.md，添加项目信息
5. 返回成功信息

### 示例4：HTTPS 失败自动重试
用户输入："将 https://github.com/user/private-repo 收录"

执行步骤：
1. 确认收录位置：project/opensource/
2. 提取项目名称：private-repo
3. 执行命令：`git submodule add https://github.com/user/private-repo project/opensource/private-repo`
4. 检测到 HTTPS 失败（可能是私有仓库或网络问题）
5. 自动转换为 SSH 格式：`git@github.com:user/private-repo.git`
6. 执行命令：`git submodule add git@github.com:user/private-repo.git project/opensource/private-repo`
7. 更新readme.md，添加项目信息
8. 返回成功信息，并提示"已使用 SSH 协议成功收录仓库"

## 注意事项

1. 在执行git命令前，确保当前工作目录正确
2. 检查git是否已初始化（.git目录是否存在）
3. 处理Windows和Linux路径差异
4. 考虑网络超时问题，设置合理的超时时间
5. 在更新readme.md前，备份原文件（可选）
6. **SSH 密钥配置**：
   - 当 HTTPS 失败且自动重试 SSH 也失败时，提示用户配置 SSH 密钥
   - 配置步骤：
     1. 生成 SSH 密钥：`ssh-keygen -t ed25519 -C "your_email@example.com"`
     2. 启动 SSH 代理：`eval "$(ssh-agent -s)"` (Linux/Mac) 或 `ssh-agent` (Windows)
     3. 添加密钥到代理：`ssh-add ~/.ssh/id_ed25519`
     4. 复制公钥内容：`cat ~/.ssh/id_ed25519.pub`
     5. 在 GitHub 设置中添加 SSH 密钥：Settings → SSH and GPG keys → New SSH key
     6. 测试连接：`ssh -T git@github.com`
   - Windows 用户可能需要使用 Git Bash 或 PowerShell 配置 SSH
