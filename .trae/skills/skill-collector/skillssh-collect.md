# Skills.sh Collector

## 功能描述

本技能用于从 skills.sh 网站收录技能信息，**不执行本地下载操作**。仅收集技能的网址和简介信息，记录到文档中。

## 重要声明

**下载功能已禁用** - 本技能仅进行信息收录，不会将技能内容下载到本地。

## 触发条件

当用户提供以下类型的输入时激活本技能：
- URL格式匹配：`https://skills.sh/{author}/{category}/{skill-name}`
- 例如：`https://skills.sh/wshobson/agents/fastapi-templates`
- 用户明确提到"收录 skills.sh 的技能"
- 用户提到"记录这个技能"

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
使用 WebFetch 工具获取 skills.sh 页面的完整内容。

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

#### 2.3 内容解析策略
```
function parseSkillsShPage(html_content):
    github_patterns = [
        r"https://github\.com/[\w-]+/[\w-]+",
        r"href=['\"](https://github\.com/[^'\"]+)['\"]"
    ]

    for pattern in github_patterns:
        matches = regex_find_all(pattern, html_content)
        if matches:
            github_url = clean_github_url(matches[0])
            break

    description = extract_description(html_content)

    return {
        "github_url": github_url,
        "description": description
    }
```

### 3. 信息记录

#### 3.1 确定记录位置
根据技能分类确定记录位置：
- 默认位置：`project/skills/{category}/README.md`
- 如果用户指定了位置，使用用户指定的位置
- 目录结构：
  ```
  project/skills/
  ├── agents/
  │   └── README.md
  ├── tools/
  │   └── README.md
  └── prompts/
      └── README.md
  ```

#### 3.2 更新 README.md
在技能分类目录下更新 README.md 文件：

```markdown
## 收录技能

### [{skill-name}]({skills_sh_url})
- **来源**: [skills.sh](https://skills.sh/{author}/{category}/{skill-name})
- **GitHub**: [仓库地址]({github_url})
- **收录时间**: YYYY-MM-DD
- **描述**: {技能描述}
- **分类**: {category}
- **作者**: {author}
```

如果 README.md 不存在，则创建新文件。

#### 3.3 记录配置选项
```json
{
  "record_mode": "metadata_only",
  "default_location": "project/skills/",
  "update_readme": true,
  "store_github_url": true,
  "store_description": true
}
```

### 4. 执行流程总结

```
1. 解析URL → 提取 author, category, skill_name
2. 获取网页内容 → WebFetch
3. 解析网页内容 → 提取 github_url, description
4. 确定记录位置 → project/skills/{category}/README.md
5. 更新文档 → 在 README.md 中添加技能信息
6. 返回成功信息
```

## 下载防护机制

### 配置标志
```json
{
  "download_enabled": false,
  "record_mode": "metadata_only",
  "allow_local_download": false
}
```

### 验证函数伪代码
```
function validateNoDownloadOperation():
    if download_enabled == true:
        log_error("下载操作被明确禁止")
        raise ValidationError("禁止下载操作")
    if operation_type contains "download" or "clone":
        log_error("检测到下载意图")
        raise ValidationError("下载操作已禁用")
    return true
```

### 防护日志
所有操作都会记录明确的日志信息：
- `[INFO] 信息收录模式已启用`
- `[INFO] 下载功能已禁用`
- `[INFO] 正在收集技能信息...`
- `[WARN] 下载操作已被防护机制拦截`

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
错误信息：无法从页面提取信息
处理方式：
- 尝试多种解析策略
- 如果自动解析失败，至少记录URL基本信息
- 记录解析失败的页面内容供调试
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
            return "页面解析失败，已记录基本信息"
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
[INFO] 确定记录位置: {target_path}
[INFO] 文档更新完成
[INFO] 技能收录成功: {skill_name}
[ERROR] 收录失败: {error_message}
```

## 配置选项

### 可配置项
```json
{
  "record_mode": "metadata_only",
  "default_location": "project/skills/",
  "update_readme": true,
  "store_github_url": true,
  "store_description": true,
  "timeout_seconds": 30,
  "retry_count": 3,
  "retry_delay_seconds": 5
}
```

### 配置说明
- `record_mode`: 记录模式，仅收录元数据
- `default_location`: 默认记录位置
- `update_readme`: 是否更新 README.md
- `store_github_url`: 是否保存 GitHub 地址
- `store_description`: 是否保存技能描述
- `timeout_seconds`: 操作超时时间
- `retry_count`: 失败重试次数
- `retry_delay_seconds`: 重试间隔

## 使用示例

### 示例1：基本收录
用户输入：`收录 https://skills.sh/wshobson/agents/fastapi-templates`

执行步骤：
1. 解析URL：author=wshobson, category=agents, skill_name=fastapi-templates
2. 获取网页内容
3. 提取GitHub仓库地址和描述
4. 更新 project/skills/agents/README.md
5. 返回成功信息

### 示例2：指定记录位置
用户输入：`将 https://skills.sh/wshobson/agents/fastapi-templates 收录到 project/opensource`

执行步骤：
1. 解析URL
2. 获取网页内容并提取信息
3. 更新 project/opensource/README.md
4. 返回成功信息

### 示例3：解析部分失败
用户输入：`收录 https://skills.sh/some/skill`

执行步骤：
1. 解析URL成功
2. 获取网页内容成功
3. 解析部分成功：记录URL和基本信息
4. 更新文档，包含已获取的信息
5. 返回成功信息，提示部分信息缺失

## 质量标准

1. **URL解析准确率**：100% 正确解析符合格式的URL
2. **信息提取成功率**：90% 以上成功提取关键信息
3. **文档更新成功率**：100% 成功更新 README.md
4. **下载防护保证**：100% 拦截任何下载尝试
5. **响应时间**：整体操作在30秒内完成

## 注意事项

1. **下载严格禁止**：任何情况下都不执行下载操作
2. **网络依赖**：本技能需要稳定的网络连接
3. **信息记录**：仅记录网址和简介，不存储技能内容
4. **更新机制**：如需更新信息，重新执行收录命令即可
5. **跨平台兼容**：处理Windows和Unix路径差异

## 常见问题

### Q: 为什么不下载技能内容？
A: 本技能设计为轻量级信息收录工具，仅收集技能元数据进行管理和索引，不占用本地存储空间。

### Q: 收录的信息会保存到哪里？
A: 收录信息保存在项目的 README.md 文件中，按照技能分类组织。

### Q: 如何停止收录一个技能？
A: 从 README.md 中删除对应条目即可。

### Q: 支持收录私有仓库吗？
A: 可以记录基本信息，但可能无法获取完整的描述信息。
