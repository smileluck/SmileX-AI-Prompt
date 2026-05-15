#!/usr/bin/env python3
"""
md2pdf - Markdown 转 PDF 工具 (pandoc + typst)

使用 pandoc + typst 引擎，原生支持中文排版。
递归处理 Markdown 文件中的 .md 引用，保持目录结构，
将链接更新为 .pdf 后输出。
"""

import argparse
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Optional, Set, Tuple

# Windows console encoding fix
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    # winget 安装的工具可能不在当前 PATH 中
    _winget_links = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Links"
    if _winget_links.exists() and str(_winget_links) not in os.environ.get("PATH", ""):
        os.environ["PATH"] = str(_winget_links) + os.pathsep + os.environ.get("PATH", "")


# ─── 工具检测 ───────────────────────────────────────────────

REQUIRED_TOOLS = ["pandoc", "typst"]


def _run_cmd(cmd: list, timeout: int = 10) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")


def _check_tool(name: str) -> bool:
    try:
        result = _run_cmd([name, "--version"])
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def ensure_tools() -> None:
    missing = [t for t in REQUIRED_TOOLS if not _check_tool(t)]
    if not missing:
        return
    tips = {
        "pandoc": "安装 pandoc: winget install --id JohnMacFarlane.Pandoc",
        "typst": "安装 typst: winget install --id Typst.Typst",
    }
    msg = "缺少必要工具:\n" + "\n".join(f"  - {t}: {tips.get(t, '请手动安装')}" for t in missing)
    raise EnvironmentError(msg)


# ─── Markdown 解析 ──────────────────────────────────────────

INLINE_MD_LINK = re.compile(r'\[([^\]]*)\]\(([^)]+\.md(?:#[^\)]*)?)\)')
REF_MD_LINK = re.compile(r'^\s*\[[^\]]*\]:\s*(.+\.md(?:\s.*)?)$', re.MULTILINE)
EXTERNAL_URL = re.compile(r'^https?://')


def resolve_md_path(source_dir: Path, link_path: str) -> Optional[Path]:
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
    try:
        content = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    refs = []
    for match in INLINE_MD_LINK.finditer(content):
        start = match.start()
        if start > 0 and content[start - 1] == "!":
            continue
        link = match.group(2)
        if not EXTERNAL_URL.match(link):
            refs.append(link)
    for match in REF_MD_LINK.finditer(content):
        link = match.group(1).strip().split()[0]
        if not EXTERNAL_URL.match(link):
            refs.append(link)
    return refs


def collect_md_files(entry: Path, visited: Optional[Set[Path]] = None) -> Set[Path]:
    if visited is None:
        visited = set()
    entry = entry.resolve()
    if entry in visited:
        return visited
    if not entry.exists() or entry.suffix != ".md":
        return visited
    visited.add(entry)
    for ref in find_md_references(entry):
        resolved = resolve_md_path(entry.parent, ref)
        if resolved and resolved not in visited:
            collect_md_files(resolved, visited)
    return visited


def collect_dir_md_files(directory: Path) -> Set[Path]:
    files = set()
    for root, _, filenames in os.walk(directory):
        for fname in filenames:
            if fname.endswith(".md"):
                files.add((Path(root) / fname).resolve())
    return files


def replace_md_links(content: str) -> str:
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


def _collect_with_missing(file_path: Path, visited: Set[Path]) -> List[Path]:
    missing = []
    file_path = file_path.resolve()
    if file_path in visited:
        return missing
    visited.add(file_path)
    if not file_path.exists():
        missing.append(file_path)
        return missing
    for ref in find_md_references(file_path):
        resolved = resolve_md_path(file_path.parent, ref)
        if resolved is None:
            continue
        if not resolved.exists():
            missing.append(resolved)
            continue
        missing.extend(_collect_with_missing(resolved, visited))
    return missing


# ─── PDF 转换 ──────────────────────────────────────────────

def convert_md_to_pdf(
    md_file: Path,
    output_pdf: Path,
    css: Optional[str] = None,
) -> bool:
    """使用 pandoc + typst 将 Markdown 转换为 PDF"""
    template = Path(__file__).parent / "template.typ"

    cmd = [
        "pandoc", str(md_file),
        "--pdf-engine=typst",
        "--from=markdown-citations",
    ]
    if template.exists():
        cmd.append(f"--template={template}")
    if css:
        cmd.extend(["--css", css])
    cmd.extend(["-o", str(output_pdf)])

    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        print(f"    pandoc 错误: {result.stderr[:300]}", file=sys.stderr)
    return result.returncode == 0


# ─── 文件处理 ──────────────────────────────────────────────

def process_files(
    entry: Path,
    output_dir: Path,
    css: Optional[str],
    recursive: bool,
) -> Tuple[List[str], List[str], List[str]]:
    if entry.is_dir():
        md_files = collect_dir_md_files(entry)
        base_dir = entry.resolve()
    elif recursive:
        md_files = collect_md_files(entry)
        # 计算所有文件的公共父目录
        parents = sorted(f.parent for f in md_files)
        base_dir = parents[0] if parents else entry.parent.resolve()
        for p in parents[1:]:
            while not p.is_relative_to(base_dir) and base_dir != base_dir.parent:
                base_dir = base_dir.parent
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
    if recursive and not entry.is_dir():
        visited = set()
        missing_refs = _collect_with_missing(entry.resolve(), visited)
        missing_refs = [f for f in missing_refs if f not in md_files]

    print(f"找到 {len(md_files)} 个 .md 文件待转换")

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

        with tempfile.TemporaryDirectory(prefix="md2pdf_") as tmpdir:
            tmp_path = Path(tmpdir)
            tmp_md = tmp_path / rel_path
            tmp_md.parent.mkdir(parents=True, exist_ok=True)
            tmp_md.write_text(new_content, encoding="utf-8")

            # 复制同目录资源文件
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

            if convert_md_to_pdf(tmp_md, output_pdf, css):
                success.append(str(pdf_rel))
                print(f"    + {pdf_rel}")
            else:
                failed.append(str(rel_path))
                print(f"    x {rel_path} 转换失败")

    return success, failed, [str(m) for m in missing_refs]


# ─── 报告 ──────────────────────────────────────────────────

def print_report(success: List[str], failed: List[str], skipped: List[str]):
    print()
    print("md2pdf 转换完成")
    print("-" * 40)
    print(f"  成功: {len(success)} 个")
    print(f"  失败: {len(failed)} 个")
    if skipped:
        print(f"  跳过: {len(skipped)} 个 (文件不存在)")
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
        description="md2pdf - Markdown 转 PDF (pandoc + typst)，递归处理引用，保持目录结构"
    )
    parser.add_argument("input", help="输入的 .md 文件或目录路径")
    parser.add_argument("-o", "--output", default="./output", help="输出目录 (默认: ./output)")
    parser.add_argument("--css", help="自定义 CSS 样式文件路径")
    parser.add_argument("--no-recursive", action="store_true", help="不递归处理引用的 .md 文件")

    args = parser.parse_args()

    entry = Path(args.input).resolve()
    output_dir = Path(args.output).resolve()

    if not entry.exists():
        print(f"错误: 输入路径不存在: {entry}", file=sys.stderr)
        sys.exit(1)

    try:
        ensure_tools()
    except EnvironmentError as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    success, failed, skipped = process_files(
        entry=entry,
        output_dir=output_dir,
        css=args.css,
        recursive=not args.no_recursive,
    )

    print_report(success, failed, skipped)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
