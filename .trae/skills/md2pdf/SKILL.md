---
name: "md2pdf"
version: "1.0.0"
author: "SmileX Team"
date: "2026-05-13"
tags: [markdown, pdf, pandoc, conversion, documentation]
description: "将 Markdown 文件转换为 PDF，递归处理引用的 .md 文件，保持目录结构并更新链接指向 PDF。"
dependencies: ["pandoc", "xelatex"]
---

# Markdown 转 PDF (md2pdf)

将 Markdown 文件转换为 PDF，递归处理其中引用的其他 `.md` 文件，保持相同的目录结构输出，并将链接更新为指向 `.pdf`。

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
| template | 否 | - | 自定义 pandoc LaTeX 模板路径 |
| css | 否 | - | 自定义 CSS 样式文件路径 |
| recursive | 否 | `true` | 是否递归处理引用的 .md 文件 |
| pdf-engine | 否 | `xelatex` | PDF 引擎（xelatex / pdflatex / lualatex） |

## 前置条件

### 环境管理器（自动检测，优先级: uv > conda > pip）

脚本启动时自动检测环境管理器，按优先级选择：

| 优先级 | 管理器 | Python 命令 | pandoc 安装方式 | TeX 引擎安装 |
|--------|--------|------------|----------------|-------------|
| 1 | uv | `uv python find` / `uv run python` | `uv pip install pypandoc_binary` | ❌ 需手动安装 |
| 2 | conda | `conda run python` | `conda install -c conda-forge pandoc` | `conda install -c conda-forge texlive-core` |
| 3 | pip | `sys.executable` / `python3` / `python` | `pip install pypandoc_binary` | ❌ 需手动安装 |

如果找不到任何环境管理器，直接抛出异常终止，不会自动创建环境。

### 依赖自动安装

| 依赖 | 自动安装行为 |
|------|-------------|
| pandoc | 不可用时自动通过当前环境管理器安装（conda / uv pip / pip） |
| xelatex | 不可用时：conda 尝试自动安装 texlive-core；uv/pip 无法安装需手动处理 |
| pdflatex | xelatex 不可用时的降级方案，安装逻辑同上 |

### 手动安装（自动安装失败时）

```bash
# pandoc
conda install -c conda-forge pandoc    # conda
pip install pypandoc_binary             # pip/uv
# 或手动: https://pandoc.org/installing.html

# xelatex (TeX 引擎)
conda install -c conda-forge texlive-core  # 仅 conda
# 或手动安装 MiKTeX (https://miktex.org/) / TeX Live
```

## 工作流程

### Step 1: 环境验证与自动安装

1. 检测环境管理器（uv > conda > pip），未找到则抛出异常终止
2. 检查 pandoc 是否可用，不可用则通过当前环境管理器自动安装
3. 检查 xelatex 是否可用，不可用则尝试自动安装（仅 conda 支持），失败则降级为 pdflatex
4. 如果所有安装尝试均失败，抛出异常终止

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

在临时副本中将 `.md` 链接替换为 `.pdf` 链接：

```
[text](./path/file.md)       → [text](./path/file.pdf)
[text](../other.md#anchor)   → [text](../other.pdf#anchor)
```

仅替换以 `.md` 或 `.md#` 结尾的本地链接，不影响：
- 图片链接 `![...](...)`
- 外部 URL
- 非 .md 后缀的链接

### Step 5: Pandoc 转换

对每个 .md 文件调用 pandoc 转换为 PDF：

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="SimSun" \
  -V CJKmainfont="SimSun" \
  -V geometry:margin=1in \
  --highlight-style=tango \
  -f markdown+yaml_metadata_block
```

如用户指定了自定义模板或 CSS，追加相应参数。

### Step 6: 输出与报告

输出文件保持原始目录结构：

```
输入: docs/main.md, docs/api/endpoints.md, docs/guide.md
输出: output/main.pdf, output/api/endpoints.pdf, output/guide.pdf
```

转换完成后报告：
- 成功转换的文件列表
- 失败的文件及错误原因
- 被跳过的引用（文件不存在）

## 直接调用

脚本自动检测环境管理器（uv > conda > pip），并使用对应的 Python 执行。缺失的依赖会自动安装，无法安装则抛出异常。

```bash
# 转换单个文件（递归处理引用）
python .trae/skills/md2pdf/md2pdf.py docs/main.md

# 指定输出目录
python .trae/skills/md2pdf/md2pdf.py docs/main.md -o ./pdf-output

# 转换整个目录
python .trae/skills/md2pdf/md2pdf.py docs/ -o ./pdf-output

# 使用自定义模板
python .trae/skills/md2pdf/md2pdf.py docs/main.md --template my-template.tex

# 使用 pdflatex 引擎
python .trae/skills/md2pdf/md2pdf.py docs/main.md --pdf-engine pdflatex
```

启动时会输出检测到的环境信息，例如：`环境: pip | Python: D:\software\python312\python.exe`

## 错误处理

| 错误场景 | 处理方式 |
|----------|----------|
| 无环境管理器 | 抛出异常终止，不自动创建环境 |
| pandoc 未安装 | 自动安装（conda / uv pip / pip），失败则抛出异常 |
| xelatex 未安装 | conda 自动安装 texlive-core；uv/pip 无法安装则降级为 pdflatex |
| 所有 PDF 引擎不可用 | 抛出异常终止，提示手动安装 |
| 引用的 .md 文件不存在 | 警告并跳过，继续转换其他文件 |
| pandoc 转换失败 | 记录失败文件，继续转换其他文件 |
| 循环引用 | 维护已访问集合，避免无限递归 |
| 文件编码问题 | 优先使用 UTF-8 读取 |

## 输出格式

### 成功报告示例

```
md2pdf 转换完成
─────────────────────────────
✓ 成功: 3 个
✗ 失败: 0 个
⚠ 跳过: 1 个 (文件不存在)

已转换:
  docs/main.pdf
  docs/api/endpoints.pdf
  docs/guide.pdf

已跳过:
  docs/missing.md (文件不存在)
```

## 注意事项

1. 首次使用 xelatex 可能需要下载字体包，耗时较长
2. 复杂的 LaTeX 公式可能需要额外的宏包
3. 图片引用需要使用相对路径，确保图片文件在转换时可访问
4. 大文件转换可能需要较多内存
