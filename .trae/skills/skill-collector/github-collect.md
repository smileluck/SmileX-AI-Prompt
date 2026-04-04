# GitHub Repository Collector

## 功能描述

本技能用于追踪GitHub仓库信息，**不执行本地克隆操作**。仅收集和跟踪仓库的元数据、状态和变更信息。

## 重要声明

**克隆功能已禁用** - 本技能仅进行仓库追踪和元数据收集，不会将仓库内容下载到本地。

## 触发条件

当用户说出以下指令时激活本技能：
- "将某个github的地址收录"
- "收录这个github仓库"
- "添加这个仓库到项目"
- "追踪这个仓库"
- "添加git submodule"
- 其他类似的收录仓库请求

其中"某个github的地址"为用户提供的具体GitHub仓库URL。

## 执行步骤

### 1. 位置选择
- 根据用户描述提供的分类信息（如"opensource"），确定仓库的追踪位置
- 默认位置为：`project/opensource/`
- 支持多种追踪位置的选择，至少包括opensource分类
- 如果用户未指定位置，使用默认位置

### 2. 仓库信息提取
- 解析用户提供的GitHub仓库URL
- 提取项目名称：
  - 从URL中提取最后一个路径段
  - 移除.git后缀（如果存在）
  - 示例：`https://github.com/user/project-name.git` → `project-name`
- 提取所有者信息
- 识别仓库可见性（公开/私有）

### 3. 元数据收集
- 收集以下仓库信息：
  - 仓库名称
  - 仓库URL
  - 仓库所有者
  - 仓库描述（通过API获取）
  - 主要编程语言
  - 星标数量
  - Fork数量
  - 仓库大小（如果可用）
  - 创建时间
  - 最后更新时间
  - 仓库URL（原始URL和标准化URL）
  - 默认分支名称
- 记录追踪时间（格式：YYYY-MM-DD HH:mm:ss）

### 4. 状态监控配置
- 为追踪的仓库建立监控条目
- 记录以下监控信息：
  - 追踪状态（active/paused）
  - 最后检查时间
  - 变更检测开关
  - 通知偏好设置

### 5. 变更检测
- 配置变更检测参数：
  - 检测频率设置
  - 变更类型过滤（stars、forks、issues、releases等）
  - 变更阈值设置
- 记录变更历史

### 6. 文档更新功能
- 自动修改分类目录下的 readme.md 文件（如 `project/llm/README.md`）
- **不需要在仓库文件夹下创建额外的 README.md**
- 添加新追踪仓库的相关信息，包括：
  - 仓库名称
  - URL
  - 追踪时间
  - 简要描述（如果可用）
- 按照预设格式更新readme.md文件，保持文档结构清晰
- 如果readme.md不存在，创建新文件

### 7. 克隆验证检查
- **严格禁止任何克隆操作**
- 执行前验证：
  - 确认操作模式为"追踪模式"
  - 验证不存在任何克隆意图
  - 检查配置标志位 `CLONE_ENABLED = false`
- 如果检测到任何克隆尝试：
  - 立即终止操作
  - 记录警告日志
  - 返回错误信息："克隆操作已禁用，仅支持仓库追踪"

## 克隆防护机制

### 配置标志
```json
{
  "clone_enabled": false,
  "tracking_mode": "metadata_only",
  "allow_local_clone": false
}
```

### 验证函数伪代码
```
function validateNoCloneOperation():
    if clone_enabled == true:
        log_error("克隆操作被明确禁止")
        raise ValidationError("禁止克隆操作")
    if operation_type contains "clone":
        log_error("检测到克隆意图")
        raise ValidationError("克隆操作已禁用")
    return true
```

### 防护日志
所有操作都会记录明确的日志信息：
- `[INFO] 仓库追踪模式已启用`
- `[INFO] 克隆功能已禁用`
- `[INFO] 正在收集仓库元数据...`
- `[WARN] 克隆操作已被防护机制拦截`

## 错误处理

### 错误场景

1. **URL无效**：
   - 提示URL格式错误，请用户提供正确的GitHub仓库URL
   - 支持的格式：
     - `https://github.com/user/repo.git`
     - `https://github.com/user/repo`
     - `git@github.com:user/repo.git`

2. **网络问题**：
   - 提示网络连接问题
   - 建议检查网络后重试
   - 提供缓存数据的回退选项（如果之前有追踪过）

3. **API限制**：
   - GitHub API速率限制
   - 提供重试时间和缓解建议

4. **仓库不存在**：
   - 提示仓库可能已被删除或名称更改
   - 建议用户确认URL正确性

5. **权限问题**：
   - 私有仓库可能无法获取完整信息
   - 提示只能获取有限的公共元数据

### 反馈机制
操作完成后提供明确的成功/失败反馈：
- **成功**：显示"仓库追踪成功！"，并列出追踪的仓库信息
- **失败**：显示具体的错误信息和解决建议

## 技术要求

### 1. URL解析
- 支持多种GitHub URL格式：
  - `https://github.com/user/repo.git`
  - `https://github.com/user/repo`
  - `git@github.com:user/repo.git`
- 正确提取项目名称和所有者信息

### 2. 元数据收集
- 使用GitHub API获取仓库信息（无需认证的公开端点）
- 处理API响应和错误
- 缓存元数据以减少API调用
- 优雅处理API限制情况

### 3. 追踪管理
- 维护追踪列表（JSON或Markdown格式）
- 支持追踪多个仓库
- 提供状态更新机制

### 4. 文档更新
- 读取现有的readme.md文件
- 按照统一格式添加新追踪仓库信息
- 保持文档结构清晰
- 更新后保存文件

## README更新格式

在分类目录的 readme.md（如 `project/llm/README.md`）中添加以下格式的内容，**不需要在仓库文件夹下创建额外的 README.md**：

```markdown
## 追踪仓库

### [项目名称](仓库URL)
- **追踪时间**: YYYY-MM-DD
- **星标**: ⭐数量
- **语言**: 主要编程语言
- **描述**: [仓库描述]
```

如果readme.md中已有"追踪仓库"章节，则在该章节下添加新仓库信息。

## 追踪配置选项

### 可配置项
```json
{
  "clone_enabled": false,
  "tracking_mode": "metadata_only",
  "default_location": "project/opensource/",
  "update_readme": true,
  "cache_metadata": true,
  "change_detection": {
    "enabled": true,
    "frequency": "daily",
    "types": ["stars", "forks", "releases"]
  }
}
```

### 配置说明
- `clone_enabled`: **强制为false**，克隆功能始终禁用
- `tracking_mode`: 追踪模式，仅收集元数据
- `default_location`: 默认追踪位置
- `update_readme`: 是否自动更新README
- `cache_metadata`: 是否缓存元数据
- `change_detection`: 变更检测配置

## 日志记录规范

### 日志格式
```
[TIMESTAMP] [LEVEL] [MODULE] message
```

### 日志级别
- `[INFO]`: 正常追踪操作
- `[WARN]`: 警告信息（如API限制）
- `[ERROR]`: 错误信息
- `[SECURITY]`: 安全相关（如检测到克隆尝试）

### 关键日志信息
- 技能启动：`[INFO] 仓库追踪技能已启动`
- 克隆防护：`[SECURITY] 克隆操作已被禁止`
- URL解析：`[INFO] 解析仓库URL: {url}`
- 元数据收集：`[INFO] 正在收集元数据...`
- 追踪成功：`[INFO] 仓库追踪成功: {repo_name}`
- 文档更新：`[INFO] README已更新`

## 质量标准

1. **响应时间**：技能响应时间不超过3秒
2. **追踪成功率**：仓库追踪成功率达到99%以上
3. **文档格式**：readme.md文件更新格式统一、信息准确
4. **错误提示**：提供友好的错误提示和解决建议
5. **克隆防护**：100%拦截任何克隆尝试

## 使用示例

### 示例1：基本追踪
用户输入："将 https://github.com/user/project 收录到 opensource"

执行步骤：
1. 确认追踪位置：project/opensource/
2. 提取项目名称：project
3. 验证克隆防护：通过检查
4. 收集仓库元数据（通过GitHub API）
5. 更新 project/opensource/README.md，添加追踪信息
6. 返回成功信息（明确说明未执行克隆）

### 示例2：带描述的追踪
用户输入："将 https://github.com/user/awesome-lib 收录到 llm，这是一个很棒的库"

执行步骤：
1. 确认追踪位置：project/llm/
2. 提取项目名称：awesome-lib
3. 验证克隆防护：通过检查
4. 收集仓库元数据（包含用户描述）
5. 更新 project/llm/README.md，添加追踪信息和描述
6. 返回成功信息

### 示例3：指定位置
用户输入："将 https://github.com/user/tool 收录到 project/tools"

执行步骤：
1. 确认追踪位置：project/tools/
2. 提取项目名称：tool
3. 验证克隆防护：通过检查
4. 收集仓库元数据
5. 更新readme.md，添加追踪信息
6. 返回成功信息

### 示例4：私有仓库追踪
用户输入："将 https://github.com/user/private-repo 收录"

执行步骤：
1. 确认追踪位置：project/opensource/
2. 提取项目名称：private-repo
3. 验证克隆防护：通过检查
4. 尝试收集元数据（可能只能获取有限信息）
5. 记录追踪信息（标注为私有仓库）
6. 更新readme.md，添加追踪信息（包含限制说明）
7. 返回成功信息，提示只能追踪公开信息

### 示例5：检测到克隆尝试（防护测试）
用户输入或配置错误导致克隆请求

执行步骤：
1. 检测到克隆操作意图
2. 记录安全日志：`[SECURITY] 检测到克隆尝试`
3. 终止操作
4. 返回错误：`克隆操作已禁用，仅支持仓库追踪`

## 注意事项

1. **克隆严格禁止**：任何情况下都不执行克隆操作
2. **元数据获取**：使用GitHub公开API获取信息，无需认证（受速率限制）
3. **缓存策略**：建议缓存元数据以减少API调用
4. **处理API限制**：GitHub API有速率限制，实现退避策略
5. **隐私考虑**：不存储敏感的仓库内容，仅存储元数据
6. **跨平台兼容**：处理Windows和Unix路径差异
7. **配置管理**：追踪配置集中管理，便于修改

## 常见问题

### Q: 为什么不克隆仓库？
A: 本技能设计为轻量级追踪工具，仅收集仓库元数据进行管理和监控，不占用本地存储空间。

### Q: 如何获取仓库的完整内容？
A: 如需获取仓库内容，请使用标准的git clone命令手动克隆。本技能不提供此功能。

### Q: 追踪的信息会保存到哪里？
A: 追踪信息保存在项目的readme.md文件中，同时可以在配置中指定本地缓存文件。

### Q: 如何停止追踪一个仓库？
A: 从readme.md中删除对应条目即可停止追踪。

### Q: 支持追踪私有仓库吗？
A: 可以添加追踪记录，但只能获取有限的公开元数据，无法访问私有仓库的内部信息。
