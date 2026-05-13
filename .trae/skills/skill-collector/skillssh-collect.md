# Skills.sh Collector

## 功能描述

从 skills.sh 收录技能信息，**不下载到本地**，仅收集元数据和 GitHub 链接，生成中英双语说明，更新到对应分类的 README。

> 下载操作已禁用，仅执行信息收录和文档更新。

## 触发条件

- URL 匹配：`https://skills.sh/{author}/{category}/{skill-name}`
- 用户提到"收录 skills.sh 的技能"

## 执行步骤

### 1. 解析 URL

从 skills.sh URL 提取结构信息：

```
https://skills.sh/{author}/{category}/{skill-name}
```

提取字段：`author`（作者）、`category`（分类）、`skill-name`（技能名）

### 2. 获取页面内容

使用 WebFetch 获取 skills.sh 页面内容，提取以下信息：

| 信息 | 说明 | 必需 |
|------|------|------|
| GitHub 仓库地址 | 页面中的 GitHub 链接 | 是 |
| 技能描述 | 页面中的功能描述 | 是 |
| 标签/关键词 | 技能标签 | 否 |

### 3. 补充 GitHub 元数据

如果提取到 GitHub 仓库地址，按 github-collect.md 的流程获取元数据（stars、language、license 等）。

### 4. 生成中英双语说明

将英文描述翻译为中文，补充适用场景。技术术语保留英文原文。

### 5. 确定收录位置

根据技能分类确定记录位置：
- 默认位置：`project/skills/{category}/`
- 如果用户指定了位置，使用用户指定的位置

### 6. 更新 README

在技能分类目录的 README.md 中添加条目。

## 条目格式

```markdown
### [技能名](Skills.sh URL)
- **收录时间**: YYYY-MM-DD
- **来源**: [Skills.sh](https://skills.sh/{author}/{category}/{skill-name})
- **GitHub**: [仓库地址](GitHub URL)
- **描述**: 中文描述（翻译 + 适用场景补充）
- **Description**: English original description
- **分类**: {category}
- **作者**: {author}
```

如果 README.md 已有同名条目，更新其信息而非重复添加。

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| URL 格式错误 | 提示正确格式示例 |
| 页面获取失败 | 提示检查网络，支持手动输入信息 |
| 无法提取 GitHub 地址 | 仅记录 skills.sh 信息，标注 GitHub 地址缺失 |
| 解析部分失败 | 记录已获取的信息，标注缺失字段 |

## 注意事项

1. **禁止下载**：任何情况下不下载技能内容到本地
2. **双语必填**：每个条目必须同时包含中文描述和英文原文
3. **格式统一**：与 github-collect.md 的条目格式保持一致
4. **幂等操作**：重复收录同一技能只更新不重复
