# 开源项目追踪管理

本目录用于追踪和管理各类开源项目、AI 技能、开发工具和 LLM 相关资源。

## 管理理念

- **仅追踪，不克隆**：通过元数据追踪仓库信息，不占用本地存储空间
- **中英双语**：每个条目包含中文描述和英文原文
- **分类管理**：按项目类型归入对应目录

## 目录结构

```
project/
├── opensource/     # 通用开源项目
├── llm/            # LLM/AI 相关项目
├── skills/         # AI 技能和 Skill 项目
├── tools/          # 开发工具
└── web-clone/      # 网站克隆项目
```

## 收录方式

使用 skill-router 技能收录新项目：

```
收录 https://github.com/{owner}/{repo}
```

系统会自动：
1. 获取仓库元数据（stars、语言、许可证等）
2. 生成中英双语描述
3. 根据项目类型归入对应分类
4. 更新分类目录的 README.md

## 条目格式

```markdown
### [项目名](GitHub URL)
- **收录时间**: YYYY-MM-DD
- **星标**: ⭐ 数量
- **语言**: 主要编程语言
- **许可证**: 许可证类型
- **描述**: 中文描述（翻译 + 适用场景补充）
- **Description**: English original description
- **主题**: topic1, topic2
```

## 迁移记录

原有 Git Submodule 已迁移为追踪模式，不再克隆到本地：

| 项目 | 原路径 | 迁移时间 |
|------|--------|----------|
| system-prompts-and-models-of-ai-tools | project/opensource/ | 2026-05-13 |
| luma-front | project/web-clone/ | 2026-05-13 |
| cc-switch | project/tools/ | 2026-05-13 |
