# Skills.sh Collector

## 功能描述

本技能用于从 skills.sh 网站自动收录技能模块。实现全流程自动化处理，包括网页内容解析、Git仓库地址提取、本地下载等功能。

## 触发条件

当用户提供以下类型的输入时激活本技能：
- URL格式匹配：`https://skills.sh/{author}/{category}/{skill-name}`
- 例如：`https://skills.sh/wshobson/agents/fastapi-templates`
- 用户明确提到"收录 skills.sh 的技能"
- 用户提到"从 skills.sh 下载技能"

## 执行步骤

### 1. URL解析与验证

#### 1.1 URL格式验证
验证输入URL是否符合 skills.sh 的标准格式：
```
https://skills.sh/{author}/{category}/{skill-name}
```

#### 1.2 提取关键信息
从URL中提取：
- `author`: 技能作者/组织名称
- `category`: 技能分类（如 agents, tools, prompts 等）
- `skill-name`: 技能名称

#### 1.3 URL验证伪代码
```
function parseSkillsShUrl(url):
    pattern = r"https://skills\.sh/([^/]+)/([^/]+)/([^/]+)"
    match = regex_match(pattern, url)
    if not match:
        raise ValidationError("无效的 skills.sh URL 格式")
    return {
        "author": match.group(1),
        "category": match.group(2),
        "skill_name": match.group(3)
    }
```

### 2. 网页内容获取与解析

#### 2.1 获取网页内容
使用 WebFetch 或类似工具获取 skills.sh 页面的完整内容。

#### 2.2 提取关键信息
从网页内容中提取以下信息：

**必须提取的信息**：
- **Git仓库地址**：查找页面中的 GitHub 仓库链接
  - 常见位置：页面顶部、侧边栏、"Source" 或 "Repository" 链接
  - 格式匹配：`https://github.com/{owner}/{repo}`
- **技能描述**：提取技能的功能描述文本
  - 通常位于页面标题下方或 "Description" 区域
- **作者信息**：技能作者/维护者信息

**可选提取的信息**：
- 标签/关键词
- 版本信息
- 最后更新时间
- 使用说明

#### 2.3 内容解析策略
```
function parseSkillsShPage(html_content):
    # 提取GitHub仓库链接
    github_patterns = [
        r"https://github\.com/[\w-]+/[\w-]+",
        r"href=['\"](https://github\.com/[^'\"]+)['\"]"
    ]
    
    for pattern in github_patterns:
        matches = regex_find_all(pattern, html_content)
        if matches:
            github_url = clean_github_url(matches[0])
            break
    
    # 提取技能描述
    description = extract_description(html_content)
    
    return {
        "github_url": github_url,
        "description": description
    }
```

### 3. 本地下载配置

#### 3.1 下载位置确定
根据技能分类确定下载位置：
- 默认位置：`project/skills/{category}/`
- 如果用户指定了位置，使用用户指定的位置
- 目录结构：
  ```
  project/skills/
  ├── agents/
  │   └── {skill-name}/
  ├── tools/
  │   └── {skill-name}/
  └── prompts/
      └── {skill-name}/
  ```

#### 3.2 下载参数配置
**关键配置**：确保不建立 Git 版本追踪关系
```json
{
  "git_init": false,
  "git_remote": false,
  "download_mode": "archive",
  "strip_git_dir": true,
  "preserve_structure": true
}
```

#### 3.3 下载执行方式
使用以下方式之一进行下载：

**方式1：GitHub Archive 下载（推荐）**
```bash
# 下载仓库归档文件
curl -L "https://github.com/{owner}/{repo}/archive/refs/heads/main.zip" -o temp.zip

# 解压到目标目录
Expand-Archive -Path temp.zip -DestinationPath target_dir

# 删除 .git 目录（如果存在）
Remove-Item -Path "target_dir/.git" -Recurse -Force -ErrorAction SilentlyContinue

# 清理临时文件
Remove-Item -Path temp.zip
```

**方式2：Git Clone 后移除 .git（备选）**
```bash
# 克隆仓库
git clone --depth 1 https://github.com/{owner}/{repo}.git temp_dir

# 移除 .git 目录
Remove-Item -Path "temp_dir/.git" -Recurse -Force

# 移动到目标位置
Move-Item -Path "temp_dir/*" -Destination "target_dir"
```

### 4. 文档更新

#### 4.1 更新 README.md
在技能分类目录下更新或创建 README.md 文件：

```markdown
## 收录技能

### [{skill-name}]({github_url})
- **来源**: skills.sh/{author}/{category}/{skill-name}
- **收录时间**: YYYY-MM-DD
- **描述**: {技能描述}
- **分类**: {category}
```

#### 4.2 创建技能元数据文件
在下载的技能目录下创建 `META.json`：

```json
{
  "name": "{skill-name}",
  "source": "skills.sh",
  "source_url": "https://skills.sh/{author}/{category}/{skill-name}",
  "github_url": "{github_url}",
  "author": "{author}",
  "category": "{category}",
  "collected_at": "YYYY-MM-DD HH:mm:ss",
  "description": "{技能描述}"
}
```

### 5. 执行流程总结

```
1. 解析URL → 提取 author, category, skill_name
2. 获取网页内容 → WebFetch
3. 解析网页内容 → 提取 github_url, description
4. 确定下载位置 → project/skills/{category}/{skill_name}
5. 执行下载 → 使用 archive 方式，不建立 git 追踪
6. 清理 .git 目录 → 确保无版本追踪
7. 更新文档 → README.md 和 META.json
8. 返回成功信息
```

## 错误处理

### 错误场景及处理

#### 1. URL格式错误
```
错误信息：无效的 skills.sh URL 格式
处理方式：
- 提示用户正确的URL格式
- 示例：https://skills.sh/wshobson/agents/fastapi-templates
```

#### 2. 网络连接失败
```
错误信息：无法访问 skills.sh 网站
处理方式：
- 检查网络连接状态
- 提供重试选项
- 记录错误日志
```

#### 3. 页面解析失败
```
错误信息：无法从页面提取 GitHub 仓库地址
处理方式：
- 尝试多种解析策略
- 如果自动解析失败，请求用户手动提供 GitHub 地址
- 记录解析失败的页面内容供调试
```

#### 4. GitHub仓库访问失败
```
错误信息：无法访问或下载 GitHub 仓库
处理方式：
- 检查仓库是否存在
- 检查是否为私有仓库
- 提供手动下载指引
```

#### 5. 下载过程错误
```
错误信息：下载过程中断或失败
处理方式：
- 清理部分下载的文件
- 提供重试选项
- 记录详细错误信息
```

#### 6. 磁盘空间不足
```
错误信息：目标磁盘空间不足
处理方式：
- 检查磁盘空间
- 提示用户清理空间或更换下载位置
```

### 错误处理伪代码
```
function handleCollectionError(error):
    log_error(error)
    
    switch error.type:
        case "INVALID_URL":
            return "URL格式错误，请使用正确的 skills.sh URL 格式"
        case "NETWORK_ERROR":
            return "网络连接失败，请检查网络后重试"
        case "PARSE_ERROR":
            return "页面解析失败，请手动提供 GitHub 仓库地址"
        case "DOWNLOAD_ERROR":
            return "下载失败，请检查仓库是否存在"
        case "DISK_ERROR":
            return "磁盘空间不足，请清理空间后重试"
        default:
            return "未知错误，请查看日志获取详情"
```

## 日志记录规范

### 日志格式
```
[TIMESTAMP] [LEVEL] [skillssh-collect] message
```

### 日志级别
- `[INFO]`: 正常操作信息
- `[WARN]`: 警告信息
- `[ERROR]`: 错误信息
- `[DEBUG]`: 调试信息

### 关键日志信息
```
[INFO] 开始收录 skills.sh 技能: {url}
[INFO] URL解析成功: author={author}, category={category}, skill={skill_name}
[INFO] 正在获取网页内容...
[INFO] 网页内容获取成功
[INFO] 提取到 GitHub 仓库: {github_url}
[INFO] 技能描述: {description}
[INFO] 确定下载位置: {target_path}
[INFO] 开始下载技能文件...
[INFO] 下载完成，清理 .git 目录...
[INFO] 文档更新完成
[INFO] 技能收录成功: {skill_name}
[ERROR] 收录失败: {error_message}
```

## 配置选项

### 可配置项
```json
{
  "default_location": "project/skills/",
  "download_mode": "archive",
  "strip_git_dir": true,
  "create_meta_file": true,
  "update_readme": true,
  "timeout_seconds": 60,
  "retry_count": 3,
  "retry_delay_seconds": 5
}
```

### 配置说明
- `default_location`: 默认下载位置
- `download_mode`: 下载模式（archive 或 clone）
- `strip_git_dir`: 是否移除 .git 目录
- `create_meta_file`: 是否创建 META.json
- `update_readme`: 是否更新 README.md
- `timeout_seconds`: 操作超时时间
- `retry_count`: 失败重试次数
- `retry_delay_seconds`: 重试间隔

## 使用示例

### 示例1：基本收录
用户输入：`https://skills.sh/wshobson/agents/fastapi-templates`

执行步骤：
1. 解析URL：author=wshobson, category=agents, skill_name=fastapi-templates
2. 获取网页内容
3. 提取GitHub仓库地址和描述
4. 下载到 project/skills/agents/fastapi-templates/
5. 清理 .git 目录
6. 更新 README.md 和创建 META.json
7. 返回成功信息

### 示例2：指定下载位置
用户输入：`将 https://skills.sh/wshobson/agents/fastapi-templates 收录到 project/opensource`

执行步骤：
1. 解析URL
2. 获取网页内容并提取信息
3. 下载到 project/opensource/fastapi-templates/
4. 清理 .git 目录
5. 更新文档
6. 返回成功信息

### 示例3：解析失败处理
用户输入：`https://skills.sh/some/skill`

执行步骤：
1. 解析URL成功
2. 获取网页内容成功
3. 解析失败：未找到GitHub链接
4. 提示用户："无法自动提取GitHub仓库地址，请手动提供"
5. 用户提供GitHub地址后继续下载流程

## 质量标准

1. **URL解析准确率**：100% 正确解析符合格式的URL
2. **信息提取成功率**：95% 以上成功提取GitHub仓库地址
3. **下载成功率**：99% 以上成功下载技能文件
4. **无Git追踪保证**：100% 确保下载后无 .git 目录
5. **响应时间**：整体操作在60秒内完成（视网络状况）

## 注意事项

1. **网络依赖**：本技能需要稳定的网络连接
2. **GitHub访问**：确保能够访问GitHub仓库
3. **磁盘空间**：确保有足够的磁盘空间存储技能文件
4. **版本追踪**：下载后不会与原仓库建立任何Git追踪关系
5. **更新机制**：如需更新技能，需要重新下载
6. **私有仓库**：如果GitHub仓库为私有，可能无法下载

## 常见问题

### Q: 为什么下载后没有 .git 目录？
A: 本技能设计为独立收录工具，不与原仓库建立版本追踪关系，便于离线使用和管理。

### Q: 如何更新已收录的技能？
A: 重新执行收录命令即可覆盖更新，或手动从原仓库下载最新版本。

### Q: 支持私有仓库吗？
A: 如果 skills.sh 页面指向的GitHub仓库为私有，需要相应的访问权限才能下载。

### Q: 下载失败怎么办？
A: 检查网络连接，确认GitHub仓库存在且为公开仓库，或尝试手动下载后放置到指定目录。

### Q: 可以自定义下载位置吗？
A: 可以，在指令中指定下载位置即可，如"收录到 project/my-skills"。
