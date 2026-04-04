---
name: "skill-router"
description: "Intelligent skill router that automatically detects skill source type and routes to appropriate collector. Invoke when user wants to collect a skill but the source type is unclear, or as the main entry point for skill collection."
---

# Skill Router

## 功能描述

本技能是技能收录的主入口路由模块，负责：
1. 接收用户输入的链接或技能标识
2. 通过链接特征或内容分析，准确判断技能来源类型
3. 自动调用对应的收录模块执行收录操作

## 触发条件

当用户发出以下类型的指令时激活本技能：
- "收录这个技能：{url}"
- "下载这个技能：{url}"
- "添加技能：{url}"
- "收录 {url}"
- 或任何包含URL的技能收录请求

## 路由规则

### 支持的技能来源类型

| 来源类型 | URL特征 | 路由目标 |
|---------|--------|---------|
| GitHub | `https://github.com/...` | github-collect.md |
| GitHub (SSH) | `git@github.com:...` | github-collect.md |
| Skills.sh | `https://skills.sh/...` | skillssh-collect.md |

### URL匹配规则

#### GitHub URL 模式
```
模式1: https://github.com/{owner}/{repo}
模式2: https://github.com/{owner}/{repo}.git
模式3: git@github.com:{owner}/{repo}.git
模式4: https://github.com/{owner}/{repo}/tree/{branch}
模式5: https://github.com/{owner}/{repo}/blob/{branch}/{file}
```

#### Skills.sh URL 模式
```
模式: https://skills.sh/{author}/{category}/{skill-name}
```

## 执行流程

### 步骤1：输入解析

#### 1.1 提取URL
从用户输入中提取URL：
```
function extractUrl(input):
    # URL正则匹配
    url_patterns = [
        r"https?://[^\s]+",
        r"git@[^\s]+"
    ]
    
    for pattern in url_patterns:
        match = regex_search(pattern, input)
        if match:
            return match.group(0)
    
    return None
```

#### 1.2 验证URL存在
如果未提取到URL：
- 提示用户提供有效的URL
- 列出支持的URL格式示例

### 步骤2：来源类型判断

#### 2.1 判断逻辑
```
function detectSourceType(url):
    url_lower = url.lower()
    
    # 判断是否为 skills.sh
    if "skills.sh" in url_lower:
        return "skillssh"
    
    # 判断是否为 GitHub
    github_indicators = [
        "github.com",
        "git@github.com"
    ]
    for indicator in github_indicators:
        if indicator in url_lower:
            return "github"
    
    # 无法识别
    return "unknown"
```

#### 2.2 判断流程图
```
输入URL
    │
    ▼
┌─────────────────┐
│ 包含 skills.sh? │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
   Yes       No
    │         │
    ▼         ▼
skillssh   ┌─────────────────┐
           │ 包含 github.com? │
           └────────┬────────┘
                    │
               ┌────┴────┐
               │         │
              Yes       No
               │         │
               ▼         ▼
           github    unknown
```

### 步骤3：路由分发

#### 3.1 路由到 GitHub 收录模块
当检测到 GitHub 来源时，读取并执行 `github-collect.md` 中的收录逻辑。

#### 3.2 路由到 Skills.sh 收录模块
当检测到 Skills.sh 来源时，读取并执行 `skillssh-collect.md` 中的收录逻辑。

#### 3.3 无法识别来源
当无法识别来源类型时：
- 显示错误信息
- 列出支持的来源类型
- 提供格式示例

### 步骤4：执行结果处理

#### 4.1 成功处理
当收录模块返回成功：
- 显示收录成功信息
- 展示收录的技能信息摘要

#### 4.2 失败处理
当收录模块返回失败：
- 显示具体错误信息
- 提供解决建议
- 记录错误日志

## 路由配置

### 配置项
```json
{
  "routing_rules": [
    {
      "source_type": "github",
      "url_patterns": [
        "github.com",
        "git@github.com"
      ],
      "target_file": "github-collect.md"
    },
    {
      "source_type": "skillssh",
      "url_patterns": [
        "skills.sh"
      ],
      "target_file": "skillssh-collect.md"
    }
  ],
  "default_behavior": "error",
  "error_message": "无法识别的技能来源，请检查URL格式"
}
```

### 扩展新来源
要添加新的技能来源支持：
1. 在 `routing_rules` 中添加新规则
2. 创建对应的收录逻辑文件
3. 更新文档说明

## 错误处理

### 错误场景

#### 1. 未提供URL
```
错误信息：未检测到有效的URL
处理方式：
- 提示用户提供URL
- 示例：收录 https://github.com/user/repo
```

#### 2. URL格式无效
```
错误信息：URL格式无效
处理方式：
- 检查URL是否完整
- 确保URL以 http:// 或 https:// 开头
```

#### 3. 无法识别的来源
```
错误信息：无法识别的技能来源
处理方式：
- 列出支持的来源类型
- 提供正确的URL格式示例
```

#### 4. 收录模块调用失败
```
错误信息：收录模块执行失败
处理方式：
- 显示具体错误原因
- 提供重试选项
- 记录详细日志
```

### 错误处理伪代码
```
function handleRouteError(error):
    log_error(error)
    
    switch error.type:
        case "NO_URL":
            return {
                "message": "请提供要收录的技能URL",
                "examples": [
                    "收录 https://github.com/user/repo",
                    "收录 https://skills.sh/author/category/skill"
                ]
            }
        case "INVALID_URL":
            return {
                "message": "URL格式无效，请检查URL是否正确",
                "hint": "URL应以 http:// 或 https:// 开头"
            }
        case "UNKNOWN_SOURCE":
            return {
                "message": "无法识别的技能来源",
                "supported_sources": ["GitHub", "Skills.sh"],
                "examples": [
                    "GitHub: https://github.com/user/repo",
                    "Skills.sh: https://skills.sh/author/category/skill"
                ]
            }
        case "MODULE_ERROR":
            return {
                "message": f"收录失败: {error.detail}",
                "suggestion": "请检查网络连接或稍后重试"
            }
```

## 日志记录

### 日志格式
```
[TIMESTAMP] [LEVEL] [skill-router] message
```

### 关键日志
```
[INFO] 收到收录请求: {user_input}
[INFO] 提取URL: {url}
[INFO] 检测到来源类型: {source_type}
[INFO] 路由到: {target_file}
[INFO] 收录成功: {skill_name}
[ERROR] 路由失败: {error_message}
[WARN] 无法识别的来源: {url}
```

## 使用示例

### 示例1：GitHub URL
用户输入：`收录 https://github.com/user/awesome-project`

执行流程：
1. 提取URL：`https://github.com/user/awesome-project`
2. 检测来源：包含 `github.com` → GitHub
3. 执行 `github-collect.md` 中的收录逻辑
4. 返回结果

### 示例2：Skills.sh URL
用户输入：`收录 https://skills.sh/wshobson/agents/fastapi-templates`

执行流程：
1. 提取URL：`https://skills.sh/wshobson/agents/fastapi-templates`
2. 检测来源：包含 `skills.sh` → Skills.sh
3. 执行 `skillssh-collect.md` 中的收录逻辑
4. 返回结果

### 示例3：Git SSH URL
用户输入：`收录 git@github.com:user/repo.git`

执行流程：
1. 提取URL：`git@github.com:user/repo.git`
2. 检测来源：包含 `git@github.com` → GitHub
3. 执行 `github-collect.md` 中的收录逻辑
4. 返回结果

### 示例4：无法识别的来源
用户输入：`收录 https://unknown-site.com/some-skill`

执行流程：
1. 提取URL：`https://unknown-site.com/some-skill`
2. 检测来源：不匹配任何已知模式 → Unknown
3. 返回错误：
   ```
   无法识别的技能来源
   
   支持的来源类型：
   - GitHub: https://github.com/user/repo
   - Skills.sh: https://skills.sh/author/category/skill
   
   请使用上述格式的URL。
   ```

### 示例5：未提供URL
用户输入：`收录一个技能`

执行流程：
1. 尝试提取URL：未找到
2. 返回提示：
   ```
   请提供要收录的技能URL
   
   示例：
   - 收录 https://github.com/user/repo
   - 收录 https://skills.sh/author/category/skill
   ```

## 质量标准

1. **URL提取准确率**：99% 以上正确提取URL
2. **来源判断准确率**：100% 正确判断已知来源类型
3. **路由成功率**：99% 以上成功路由到正确模块
4. **响应时间**：路由判断在100ms内完成

## 注意事项

1. **URL优先级**：Skills.sh 的判断优先于 GitHub（因为 Skills.sh 页面可能包含 GitHub 链接）
2. **大小写不敏感**：URL判断不区分大小写
3. **URL编码**：正确处理URL编码的字符
4. **空格处理**：自动去除URL前后的空格
5. **多URL处理**：如果输入包含多个URL，只处理第一个

## 模块文件结构

```
skill-collector/
├── SKILL.md              # 主入口（路由判断）
├── github-collect.md     # GitHub收录逻辑
└── skillssh-collect.md   # Skills.sh收录逻辑
```

## 常见问题

### Q: 为什么我的URL无法识别？
A: 请确保URL格式正确，目前支持 GitHub 和 Skills.sh 两种来源。

### Q: 可以同时收录多个技能吗？
A: 目前每次只能收录一个技能，如需收录多个，请分别执行收录命令。

### Q: 如何添加新的技能来源支持？
A: 创建新的收录逻辑文件，并在路由配置中添加相应的规则。

### Q: 收录失败怎么办？
A: 检查网络连接，确认URL正确且可访问，或查看错误日志获取详细信息。
