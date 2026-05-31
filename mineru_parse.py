#!/usr/bin/env python3
"""
MinerU Parse Script — PDF/DOCX/PPTX/XLSX → Markdown
================================================================
基于 MinerU (OpenDataLab) 的一键文档解析脚本。
传文件路径，解析后 Markdown 自动输出到同目录。

用法:
    python mineru_parse.py <file_path>

示例:
    python mineru_parse.py "D:\papers\my_paper.pdf"
    python mineru_parse.py "C:\docs\report.docx"

前置:
    pip install mineru torch torchvision transformers shapely pyclipper six ftfy
"""

import os
import shutil
import subprocess
import sys


# ── 配置 ──────────────────────────────────────────────────
# 如果 mineru 命令不在 PATH 中，可以在这里指定完整路径
# MINERU_CMD = "mineru"   # 默认使用 PATH 中的 mineru
MINERU_CMD = "mineru"
# 解析后端：pipeline（CPU/GPU通用）, vlm-engine（需GPU）, hybrid-engine（需GPU）
BACKEND = "pipeline"
# ──────────────────────────────────────────────────────────


def find_mineru():
    """查找 mineru 可执行文件"""
    # 优先使用环境变量
    if os.environ.get("MINERU_PATH"):
        return os.environ["MINERU_PATH"]

    # 尝试直接使用命令
    return MINERU_CMD


def main():
    if len(sys.argv) < 2:
        print("Usage: python mineru_parse.py <file_path>")
        print()
        print("Examples:")
        print('  python mineru_parse.py "D:\\papers\\my_paper.pdf"')
        print('  python mineru_parse.py "C:\\docs\\report.docx"')
        sys.exit(1)

    # Fix Windows symlink issue with HuggingFace cache
    os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

    file_path = os.path.abspath(sys.argv[1])

    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        sys.exit(1)

    # Determine output directory (same folder as input file)
    output_dir = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    ext = os.path.splitext(file_path)[1].lower()

    supported_exts = {".pdf", ".docx", ".pptx", ".xlsx",
                      ".png", ".jpg", ".jpeg", ".bmp", ".tiff"}
    if ext not in supported_exts:
        print(f"[WARN] Unsupported file type: {ext}")
        print(f"       Supported: {', '.join(sorted(supported_exts))}")

    print(f"[MinerU] 输入文件: {file_path}")
    print(f"[MinerU] 输出目录: {output_dir}")
    print(f"[MinerU] 解析后端: {BACKEND}")
    print()

    mineru_cmd = find_mineru()

    # Run MinerU
    try:
        result = subprocess.run(
            [mineru_cmd, "-p", file_path, "-o", output_dir, "-b", BACKEND],
            check=False
        )
    except FileNotFoundError:
        print(f"[ERROR] 找不到 mineru 命令。")
        print(f"        请先安装: pip install mineru")
        print(f"        或设置环境变量 MINERU_PATH 指向 mineru.exe 的完整路径")
        sys.exit(1)

    if result.returncode != 0:
        print(f"[MinerU] 解析失败（退出码: {result.returncode}）")
        print(f"        常见原因: 缺少依赖包。试运行:")
        print(f"        pip install torch torchvision transformers shapely pyclipper six ftfy")
        sys.exit(result.returncode)

    # Copy MD output to the same folder as input
    md_source = os.path.join(output_dir, base_name, "auto", f"{base_name}.md")
    md_dest = os.path.join(output_dir, f"{base_name}_解析结果.md")

    if os.path.exists(md_source):
        shutil.copy2(md_source, md_dest)
        size_kb = os.path.getsize(md_dest) / 1024
        print(f"\n[MinerU] ✅ 解析完成!")
        print(f"         Markdown: {md_dest}")
        print(f"         大小: {size_kb:.0f} KB")
    else:
        print(f"\n[MinerU] ⚠️  解析可能完成，但未找到预期输出: {md_source}")
        print(f"         请检查 MinerU 输出目录: {os.path.join(output_dir, base_name)}")


if __name__ == "__main__":
    main()
