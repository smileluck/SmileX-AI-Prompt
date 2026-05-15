#!/usr/bin/env python3
"""
md2pdf - Markdown 转 PDF 工具

递归处理 Markdown 文件中的 .md 引用，保持目录结构，
将链接更新为 .pdf 后输出。

环境管理器优先级: uv > conda > pip
Python 命令跟随对应环境管理器。
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Optional, Set, Tuple


# ─── 环境检测 ───────────────────────────────────────────────

class EnvironmentError(Exception):
    """环境依赖异常"""
    pass


def _run_cmd(cmd: list, timeout: int = 10) -> subprocess.CompletedProcess:
    """执行命令并返回结果"""
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def _cmd_exists(name: str) -> bool:
    """检查命令行工具是否在 PATH 中可用"""
    try:
        result = _run_cmd([name, "--version"])
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def detect_env_manager() -> Tuple[str, str]:
    """
    检测环境管理器，返回 (env_manager, python_cmd)
    优先级: uv > conda > pip
    未找到则抛出 EnvironmentError
    """
    # 1. uv
    if _cmd_exists("uv"):
        try:
            result = _run_cmd(["uv", "python", "find"])
            if result.returncode == 0 and result.stdout.strip():
                python_path = result.stdout.strip().splitlines()[0]
                return "uv", python_path
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        # uv 存在但没找到 python，用 uv run python
        return "uv", "uv run python"

    # 2. conda
    if _cmd_exists("conda"):
        try:
            result = _run_cmd(["conda", "run", "python", "--version"])
            if result.returncode == 0:
                return "conda", "conda run python"
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    # 3. pip (系统 Python)
    for cmd in [sys.executable, "python3", "python", "py -3"]:
        try:
            if cmd == sys.executable:
                return "pip", cmd
            result = _run_cmd(cmd.split() + ["--version"])
            if result.returncode == 0:
                return "pip", cmd
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    raise EnvironmentError(
        "未找到任何可用的 Python 环境 (uv / conda / pip)，请先安装其中之一"
    )


ENV_MANAGER, PYTHON_CMD = detect_env_manager()


def check_tool(name: str) -> bool:
    """检查命令行工具是否可用"""
    return _cmd_exists(name)


def install_pandoc() -> bool:
    """尝试通过环境管理器自动安装 pandoc"""
    print(f"  尝试通过 {ENV_MANAGER} 安装 pandoc...")

    try:
        if ENV_MANAGER == "conda":
            result = _run_cmd(
                ["conda", "install", "-y", "-c", "conda-forge", "pandoc"],
                timeout=300,
            )
            if result.returncode == 0:
                print("  ✓ pandoc 安装成功 (conda)")
                return True
            print(f"  ✗ conda 安装失败: {result.stderr[:200]}", file=sys.stderr)

        elif ENV_MANAGER == "uv":
            # uv 没有系统包管理，尝试 pip 方式安装 pypandoc（含 pandoc 二进制）
            result = _run_cmd(
                ["uv", "pip", "install", "pypandoc_binary"],
                timeout=120,
            )
            if result.returncode == 0:
                print("  ✓ pypandoc_binary 安装成功 (uv)，pandoc 将通过 pypandoc 调用")
                return True
            print(f"  ✗ uv 安装失败: {result.stderr[:200]}", file=sys.stderr)

        elif ENV_MANAGER == "pip":
            result = _run_cmd(
                PYTHON_CMD.split() + ["-m", "pip", "install", "pypandoc_binary"],
                timeout=120,
            )
            if result.returncode == 0:
                print("  ✓ pypandoc_binary 安装成功 (pip)，pandoc 将通过 pypandoc 调用")
                return True
            print(f"  ✗ pip 安装失败: {result.stderr[:200]}", file=sys.stderr)

    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"  ✗ 安装异常: {e}", file=sys.stderr)

    return False


def install_tex_engine(engine: str) -> bool:
    """尝试通过环境管理器自动安装 TeX 引擎"""
    print(f"  尝试通过 {ENV_MANAGER} 安装 {engine}...")

    try:
        if ENV_MANAGER == "conda":
            pkg = "texlive-core" if engine in ("xelatex", "lualatex") else "texlive"
            result = _run_cmd(
                ["conda", "install", "-y", "-c", "conda-forge", pkg],
                timeout=600,
            )
            if result.returncode == 0:
                print(f"  ✓ {engine} 安装成功 (conda)")
                return True
            print(f"  ✗ conda 安装失败: {result.stderr[:200]}", file=sys.stderr)

    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"  ✗ 安装异常: {e}", file=sys.stderr)

    # uv 和 pip 无法安装系统级 TeX 引擎
    if ENV_MANAGER in ("uv", "pip"):
        print(f"  ✗ {ENV_MANAGER} 无法安装 {engine}（TeX 引擎需要系统级安装）", file=sys.stderr)

    return False


def ensure_pandoc() -> None:
    """确保 pandoc 可用，不可用则尝试自动安装"""
    if check_tool("pandoc"):
        return
    if not install_pandoc():
        raise EnvironmentError(
            "pandoc 不可用且自动安装失败。\n"
            "请手动安装:\n"
            "  conda: conda install -c conda-forge pandoc\n"
            "  pip:   pip install pypandoc_binary\n"
            "  手动:   https://pandoc.org/installing.html"
        )


def ensure_pdf_engine(engine: str) -> str:
    """
    确保 PDF 引擎可用，不可用则尝试自动安装。
    返回实际可用的引擎名称（可能降级）。
    """
    if check_tool(engine):
        return engine

    if install_tex_engine(engine):
        return engine

    # xelatex/lualatex 不可用时尝试降级为 pdflatex
    if engine in ("xelatex", "lualatex"):
        print(f"  警告: {engine} 不可用，尝试降级为 pdflatex（中文可能无法正常渲染）", file=sys.stderr)
        if check_tool("pdflatex"):
            return "pdflatex"
        if install_tex_engine("pdflatex"):
            return "pdflatex"

    raise EnvironmentError(
        f"{engine} 不可用且自动安装失败。\n"
        "请手动安装 TeX 发行版:\n"
        "  conda:  conda install -c conda-forge texlive-core\n"
        "  MiKTeX: https://miktex.org/\n"
        "  TeX Live: https://tug.org/texlive/"
    )


# ─── Markdown 解析 ──────────────────────────────────────────

# 匹配行内链接中的 .md 路径: [text](path/file.md) 或 [text](path/file.md#anchor)
INLINE_MD_LINK = re.compile(r'\[([^\]]*)\]\(([^)]+\.md(?:#[^\)]*)?)\)')

# 匹配引用式链接中的 .md 路径: [text]: path/file.md
REF_MD_LINK = re.compile(r'^\s*\[[^\]]*\]:\s*(.+\.md(?:\s.*)?)$', re.MULTILINE)

# 匹配外部 URL
EXTERNAL_URL = re.compile(r'^https?://')


def resolve_md_path(source_dir: Path, link_path: str) -> Optional[Path]:
    """将 Markdown 中的链接路径解析为绝对路径"""
    if EXTERNAL_URL.match(link_path):
        return None

    path_part = link_path.split("#")[0]
    if not path_part:
        return None

    resolved = (source_dir / path_part).resolve()
    if resolved.exists() and resolved.suffix == ".md":
        return resolved
    return None


def find_md_references(file_path: Path) -> List[str]:
    """解析 Markdown 文件中引用的 .md 文件路径"""
    try:
        content = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []

    refs = []

    # 行内链接
    for match in INLINE_MD_LINK.finditer(content):
        start = match.start()
        if start > 0 and content[start - 1] == "!":
            continue
        link = match.group(2)
        if not EXTERNAL_URL.match(link):
            refs.append(link)

    # 引用式链接
    for match in REF_MD_LINK.finditer(content):
        link = match.group(1).strip().split()[0]
        if not EXTERNAL_URL.match(link):
            refs.append(link)

    return refs


def collect_md_files(entry: Path, visited: Optional[Set[Path]] = None) -> Set[Path]:
    """递归收集所有被引用的 .md 文件"""
    if visited is None:
        visited = set()

    entry = entry.resolve()
    if entry in visited:
        return visited

    if not entry.exists() or entry.suffix != ".md":
        return visited

    visited.add(entry)

    refs = find_md_references(entry)
    source_dir = entry.parent

    for ref in refs:
        resolved = resolve_md_path(source_dir, ref)
        if resolved and resolved not in visited:
            collect_md_files(resolved, visited)

    return visited


def collect_dir_md_files(directory: Path) -> Set[Path]:
    """收集目录下所有 .md 文件"""
    files = set()
    for root, _, filenames in os.walk(directory):
        for fname in filenames:
            if fname.endswith(".md"):
                files.add((Path(root) / fname).resolve())
    return files


def replace_md_links(content: str) -> str:
    """将 Markdown 内容中的 .md 链接替换为 .pdf 链接"""

    def replace_inline(match):
        text = match.group(1)
        link = match.group(2)
        if EXTERNAL_URL.match(link):
            return match.group(0)
        new_link = re.sub(r'\.md(#|$)', r'.pdf\1', link)
        return f"[{text}]({new_link})"

    def replace_ref(match):
        full = match.group(0)
        link_part = match.group(1).strip().split()[0]
        if EXTERNAL_URL.match(link_part):
            return full
        new_link = link_part.replace(".md", ".pdf")
        return full.replace(link_part, new_link)

    content = INLINE_MD_LINK.sub(replace_inline, content)
    content = REF_MD_LINK.sub(replace_ref, content)

    return content


# ─── PDF 转换 ──────────────────────────────────────────────

def convert_md_to_pdf(
    md_file: Path,
    output_pdf: Path,
    pdf_engine: str = "xelatex",
    template: Optional[str] = None,
    css: Optional[str] = None,
) -> bool:
    """使用 pandoc 将 Markdown 转换为 PDF"""
    cmd = [
        "pandoc",
        str(md_file),
        "-o",
        str(output_pdf),
        f"--pdf-engine={pdf_engine}",
        "-V",
        "geometry:margin=1in",
        "--highlight-style=tango",
        "-f",
        "markdown+yaml_metadata_block",
    ]

    if pdf_engine in ("xelatex", "lualatex"):
        cmd.extend([
            "-V", "mainfont=SimSun",
            "-V", "CJKmainfont=SimSun",
        ])

    if template:
        cmd.extend(["--template", template])

    if css:
        cmd.extend(["--css", css])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"  pandoc 错误: {result.stderr[:200]}", file=sys.stderr)
            return False
        return True
    except subprocess.TimeoutExpired:
        print("  pandoc 超时", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("  pandoc 未找到", file=sys.stderr)
        return False


def process_files(
    entry: Path,
    output_dir: Path,
    pdf_engine: str,
    template: Optional[str],
    css: Optional[str],
    recursive: bool,
) -> Tuple[List[str], List[str], List[str]]:
    """处理文件转换，返回 (成功列表, 失败列表, 跳过列表)"""
    if entry.is_dir():
        md_files = collect_dir_md_files(entry)
        base_dir = entry.resolve()
    elif recursive:
        md_files = collect_md_files(entry)
        parents = [f.parent for f in md_files]
        base_dir = min(parents) if parents else entry.parent
        for p in parents:
            if not p.is_relative_to(base_dir):
                base_dir = p
                for pp in parents:
                    try:
                        base_dir = pp if not base_dir.is_relative_to(pp) else base_dir
                    except (ValueError, TypeError):
                        pass
    else:
        md_files = {entry.resolve()}
        base_dir = entry.parent.resolve()

    if not md_files:
        print("未找到任何 .md 文件")
        return [], [], []

    if not entry.is_dir() and recursive:
        entry_resolved = entry.resolve()
        if entry_resolved not in md_files:
            md_files.add(entry_resolved)

    missing_refs = []
    all_md_files = md_files.copy()

    if recursive and not entry.is_dir():
        visited = set()
        missing_refs = _collect_with_missing(entry.resolve(), visited)
        missing_refs = [f for f in missing_refs if f not in all_md_files]

    print(f"找到 {len(md_files)} 个 .md 文件待转换")

    with tempfile.TemporaryDirectory(prefix="md2pdf_") as tmpdir:
        tmp_path = Path(tmpdir)
        success = []
        failed = []

        for md_file in sorted(md_files):
            rel_path = md_file.relative_to(base_dir)
            print(f"  处理: {rel_path}")

            try:
                content = md_file.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError) as e:
                print(f"    读取失败: {e}", file=sys.stderr)
                failed.append(str(rel_path))
                continue

            new_content = replace_md_links(content)

            tmp_md = tmp_path / rel_path
            tmp_md.parent.mkdir(parents=True, exist_ok=True)
            tmp_md.write_text(new_content, encoding="utf-8")

            src_dir = md_file.parent
            for item in src_dir.iterdir():
                if item.is_file() and item.suffix not in (".md",):
                    dst = tmp_path / rel_path.parent / item.name
                    if not dst.exists():
                        try:
                            shutil.copy2(item, dst)
                        except OSError:
                            pass

            pdf_rel = rel_path.with_suffix(".pdf")
            output_pdf = output_dir / pdf_rel
            output_pdf.parent.mkdir(parents=True, exist_ok=True)

            if convert_md_to_pdf(tmp_md, output_pdf, pdf_engine, template, css):
                success.append(str(pdf_rel))
                print(f"    ✓ {pdf_rel}")
            else:
                failed.append(str(rel_path))
                print(f"    ✗ {rel_path} 转换失败")

    return success, failed, [str(m) for m in missing_refs]


def _collect_with_missing(file_path: Path, visited: Set[Path]) -> List[Path]:
    """递归收集引用，返回缺失的文件列表"""
    missing = []
    file_path = file_path.resolve()

    if file_path in visited:
        return missing
    visited.add(file_path)

    if not file_path.exists():
        missing.append(file_path)
        return missing

    refs = find_md_references(file_path)
    source_dir = file_path.parent

    for ref in refs:
        resolved = resolve_md_path(source_dir, ref)
        if resolved is None:
            continue
        if not resolved.exists():
            missing.append(resolved)
            continue
        missing.extend(_collect_with_missing(resolved, visited))

    return missing


# ─── 报告 ──────────────────────────────────────────────────

def print_report(success: List[str], failed: List[str], skipped: List[str]):
    """打印转换报告"""
    print()
    print("md2pdf 转换完成")
    print("─" * 40)
    print(f"✓ 成功: {len(success)} 个")
    print(f"✗ 失败: {len(failed)} 个")
    if skipped:
        print(f"⚠ 跳过: {len(skipped)} 个 (文件不存在)")

    if success:
        print()
        print("已转换:")
        for f in success:
            print(f"  {f}")

    if failed:
        print()
        print("转换失败:")
        for f in failed:
            print(f"  {f}")

    if skipped:
        print()
        print("已跳过:")
        for f in skipped:
            print(f"  {f} (文件不存在)")


# ─── 入口 ──────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="md2pdf - Markdown 转 PDF，递归处理引用，保持目录结构"
    )
    parser.add_argument("input", help="输入的 .md 文件或目录路径")
    parser.add_argument("-o", "--output", default="./output", help="输出目录 (默认: ./output)")
    parser.add_argument("--pdf-engine", default="xelatex", choices=["xelatex", "pdflatex", "lualatex"], help="PDF 引擎 (默认: xelatex)")
    parser.add_argument("--template", help="自定义 pandoc LaTeX 模板路径")
    parser.add_argument("--css", help="自定义 CSS 样式文件路径")
    parser.add_argument("--no-recursive", action="store_true", help="不递归处理引用的 .md 文件")

    args = parser.parse_args()

    entry = Path(args.input).resolve()
    output_dir = Path(args.output).resolve()

    if not entry.exists():
        print(f"错误: 输入路径不存在: {entry}", file=sys.stderr)
        sys.exit(1)

    print(f"环境: {ENV_MANAGER} | Python: {PYTHON_CMD}")

    # 自动安装缺失依赖，不可恢复则抛异常
    try:
        ensure_pandoc()
        pdf_engine = ensure_pdf_engine(args.pdf_engine)
    except EnvironmentError as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    success, failed, skipped = process_files(
        entry=entry,
        output_dir=output_dir,
        pdf_engine=pdf_engine,
        template=args.template,
        css=args.css,
        recursive=not args.no_recursive,
    )

    print_report(success, failed, skipped)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
