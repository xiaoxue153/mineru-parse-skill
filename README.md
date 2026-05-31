# MinerU Parse Skill

> **一键将 PDF / DOCX / PPTX / XLSX / 图片解析为结构化 Markdown**
>
> 基于 [MinerU](https://github.com/opendatalab/MinerU) (OpenDataLab) 的文档解析工具，
> 封装为可直接调用的 Python 脚本 + Reasonix Code 技能。

---

## Features

- **多格式支持** — PDF, DOCX, PPTX, XLSX, Images
- **结构化输出** — Markdown + JSON（表格 → HTML，公式 → LaTeX）
- **一键调用** — 命令行传文件路径即可
- **自动输出** — 解析结果自动保存到原文件同目录
- **Reasonix 技能集成** — 可作为 `/skill` 直接调用
- **CPU 友好** — 无需 GPU，纯 pipeline 后端

---

## Quick Start

### 1. Prerequisites

- Python **3.10 ~ 3.13**（不要用 3.14+，部分依赖不支持）
- Windows / Linux / macOS

### 2. Install MinerU

```bash
pip install mineru
```

> **Note for Windows users**: If you get a `ModuleNotFoundError: torch`, install the CPU version:
> ```bash
> pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
> ```

### 3. Install Common Dependencies

If you encounter `ModuleNotFoundError` on first run, install all pipeline dependencies at once:

```bash
pip install torch torchvision transformers shapely pyclipper six ftfy
```

### 4. Run

```bash
python mineru_parse.py "C:\path\to\your\document.pdf"
```

**Output**: A `.md` file will appear next to the original document:
```
your/document.pdf                              ← original
your/document_解析结果.md                      ← ✨ parsed Markdown
your/document/auto/                            ← full MinerU output
```

---

## Usage in Reasonix Code

Copy `mineru-parse.md` to your project's `.reasonix/skills/` directory:

```
your-project/.reasonix/skills/mineru-parse.md
```

Then in Reasonix, simply type `/skill mineru-parse` or say:

> "Parse this PDF @path/to/file.pdf"

---

## How It Works

```
User provides file path
        │
        ▼
mineru_parse.py
  ├── Sets HF_HUB_DISABLE_SYMLINKS=1  (fix Windows symlink issue)
  ├── Runs: mineru -p <file> -o <dir> -b pipeline
  │     ├── Layout Detection    (20 pages ~30s)
  │     ├── MFR Formula Recognition
  │     ├── Table OCR
  │     ├── Text OCR
  │     └── Reading Order Assembly
  └── Copies output .md to same folder as input
```

### Pipeline Stages

| Stage | What it does | Output |
|-------|-------------|--------|
| Layout Predict | Detects page structure (text/table/image blocks) | Layout boxes |
| MFR Predict | Recognizes mathematical formulas | LaTeX strings |
| Table OCR | Extracts table cells | HTML tables |
| OCR (det + rec) | Detects and recognizes text | Text strings |
| Reading Order | Reassembles content in human reading order | Markdown |

---

## Dependencies

- [MinerU](https://github.com/opendatalab/MinerU) 3.1+
- PyTorch (CPU-only is fine)
- torchvision
- transformers
- shapely, pyclipper, six, ftfy

---

## Project Structure

```
mineru-parse-skill/
├── mineru_parse.py          # Main script — call with file path
├── mineru-parse.md          # Reasonix Code skill definition
├── requirements.txt         # Python dependencies
├── README.md                # English documentation (this file)
├── README_CN.md             # Chinese documentation
└── .gitignore
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: torch` | `pip install torch --index-url https://download.pytorch.org/whl/cpu` |
| `No module named 'transformers'` | `pip install transformers` |
| `No module named 'shapely'` | `pip install shapely` |
| `OSError: [WinError 1314]` | Set `HF_HUB_DISABLE_SYMLINKS=1` (script does this automatically) |
| `find_pruneable_heads_and_indices` error | Downgrade transformers: `pip install "transformers<5"` |
| Script runs but no output | Check `{filename}/auto/` subfolder for MinerU raw output |

---

## License

MIT

---

## Credits

- [MinerU](https://github.com/opendatalab/MinerU) by OpenDataLab — the underlying document parsing engine
- [Reasonix Code](https://reasonix.com) — AI coding assistant platform
