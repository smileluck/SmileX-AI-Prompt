---
name: "md2pdf"
version: "3.0.0"
author: "SmileX Team"
date: "2026-05-14"
tags: [markdown, pdf, pandoc, typst, conversion, documentation]
description: "将 Markdown 文件转换为 PDF（pandoc + typst），原生中文支持，递归处理引用的 .md 文件，保持目录结构并更新链接指向 PDF。"
dependencies: ["pandoc", "typst"]
---

# Markdown 转 PDF (md2pdf)

将 Markdown 文件转换为 PDF（pandoc + typst），原生支持中文排版，递归处理其中引用的其他 `.md` 文件，保持相同的目录结构输出，并将链接更新为 `.pdf`。

## 触发条件

- "将 {file.md} 转换为 PDF"
- "md2pdf {file.md}"
- "转换 markdown 为 PDF"
- "把这个 md 文件转成 PDF"
- "批量转换 markdown 到 PDF"

## 参数

| 参数 | 必填 | 默认值 | 描述 |
|------|------|--------|------|
| input | 是 | - | 输入的 .md 文件或目录路径 |
| output | 否 | `./output` | 输出目录 |
| css | 否 | - | 自定义 CSS 样式文件路径 |
| recursive | 否 | `true` | 是否递归处理引用的 .md 文件 |

## 前置条件

### 依赖（需预装）

| 依赖 | 用途 | 安装方式 |
|------|------|---------|
| pandoc | Markdown 解析与转换 | `winget install --id JohnMacFarlane.Pandoc` |
| typst | PDF 排版引擎（原生 CJK） | `winget install --id Typst.Typst` |

无需安装 Python PDF 库（不再使用 fpdf2/markdown）。

## 工作流程

### Step 1: 工具验证

1. 检测 `pandoc` 和 `typst` 是否可用
2. 缺少任一工具则给出安装提示并终止

### Step 2: 输入解析

根据输入类型确定处理模式：

| 输入类型 | 处理方式 |
|----------|----------|
| 单个 .md 文件 | 递归解析引用，构建文件集合 |
| 目录 | 收集目录下所有 .md 文件，再解析引用 |

### Step 3: 递归发现引用

从入口文件开始，解析 Markdown 中的 `.md` 链接，递归发现所有被引用的文件：

```
main.md
  ├── api/endpoints.md
  │     └── auth.md
  └── guide.md
```

解析规则：
- 行内链接：`[text](./path/file.md)` → 提取 `./path/file.md`
- 引用式链接：`[text]: ./path/file.md` → 提取 `./path/file.md`
- 忽略图片链接 `![...](...)`
- 忽略外部 URL（http:// 或 https://）
- 循环引用检测：维护已访问集合，避免无限递归

### Step 4: 链接替换

将 `.md` 链接替换为 `.pdf` 链接：

```
[text](./path/file.md)       → [text](./path/file.pdf)
[text](../other.md#anchor)   → [text](../other.pdf#anchor)
```

### Step 5: PDF 转换

对每个 .md 文件，使用 `pandoc --pdf-engine=typst` 转换：

- 使用自定义 `template.typ` 模板（设置 A4 页面、微软雅黑中文字体、蓝色链接）
- typst 原生支持中文、表格、代码块、列表等排版
- 无需 emoji 替换 hack（typst 直接渲染 Unicode 字符）

默认配置：
- 中文字体：Microsoft YaHei（微软雅黑）
- A4 页面，2cm/2.5cm 边距
- 链接蓝色，正文两端对齐

### Step 6: 输出与报告

输出文件保持原始目录结构：

```
输入: docs/main.md, docs/api/endpoints.md, docs/guide.md
输出: output/main.pdf, output/api/endpoints.pdf, output/guide.pdf
```

## 直接调用

```bash
# 转换单个文件（递归处理引用）
python .agents/skills/md2pdf/md2pdf.py docs/main.md

# 指定输出目录
python .agents/skills/md2pdf/md2pdf.py docs/main.md -o ./pdf-output

# 转换整个目录
python .agents/skills/md2pdf/md2pdf.py docs/ -o ./pdf-output

# 使用自定义 CSS
python .agents/skills/md2pdf/md2pdf.py docs/main.md --css style.css

# 不递归处理引用
python .agents/skills/md2pdf/md2pdf.py docs/main.md --no-recursive
```

## 错误处理

| 错误场景 | 处理方式 |
|----------|----------|
| pandoc/typst 未安装 | 给出安装提示，终止运行 |
| 引用的 .md 文件不存在 | 警告并跳过，继续转换其他文件 |
| PDF 生成失败 | 记录 pandoc 错误信息，继续转换其他文件 |
| 循环引用 | 维护已访问集合，避免无限递归 |
| 文件编码问题 | 优先使用 UTF-8 读取 |
