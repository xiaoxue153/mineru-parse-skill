# MinerU Parse Skill

**English** | [**中文简体**](README_CN.md)

> **One-click PDF / DOCX / PPTX / XLSX / Image → Structured Markdown**
>
> A Python wrapper around [MinerU](https://github.com/opendatalab/MinerU) by OpenDataLab.
> Drop a file in — get a clean Markdown file out. Also works as a [Reasonix Code](https://reasonix.com) skill.

---

## What It Does

You have a PDF paper. Or a DOCX contract. Or a PPTX slide deck. You want structured text — Markdown with tables in HTML, formulas in LaTeX, and content in reading order.

This project does exactly that. **One command, no manual steps.**

```
original.pdf                          →  original_解析结果.md   (Markdown output)
                                     →  original/auto/          (full MinerU output with JSON)
```

---

## Quick Start

### 1. Requirements

- **Python 3.10 ~ 3.13** (not 3.14 — some deps don't support it yet)
- Windows / Linux / macOS
- No GPU needed

### 2. Install

```bash
pip install mineru torch torchvision transformers shapely pyclipper six ftfy
```

> On Windows CPU-only: `pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu`

### 3. Run

```bash
python mineru_parse.py "your/file/path.pdf"
```

Replace `.pdf` with `.docx`, `.pptx`, `.xlsx`, or any image format. The parsed `.md` file appears right next to your original file.

---

## Reasonix Code Skill

Copy `mineru-parse.md` into your project's `.reasonix/skills/` folder:

```
your-project/
└── .reasonix/
    └── skills/
        └── mineru-parse.md
```

Then in Reasonix: `"Parse this paper @path/to/paper.pdf"` or `/skill mineru-parse`.

---

## How It Works

```
Your file
    │
    ▼
mineru_parse.py
    │
    ├── Fixes HF_HUB_DISABLE_SYMLINKS=1 (Windows symlink workaround)
    ├── Calls: mineru -p <file> -o <dir> -b pipeline
    │     ├── Layout Detection
    │     ├── Formula Recognition (→ LaTeX)
    │     ├── Table OCR (→ HTML)
    │     ├── Text OCR
    │     └── Reading Order Assembly
    └── Copies output .md next to original file
```

| Stage | What It Detects | Output |
|-------|----------------|--------|
| Layout | Page structure — text, tables, figures | Bounding boxes |
| MFR | Mathematical formulas | LaTeX |
| Table OCR | Table cells with content | HTML `<table>` |
| Text OCR | Text regions + recognition | Plain text |
| Assembly | Human reading order | Final Markdown |

---

## Files

```
mineru-parse-skill/
├── mineru_parse.py      ← Core script
├── mineru-parse.md      ← Reasonix skill definition
├── requirements.txt
├── README.md            ← English docs (this page)
├── README_CN.md         ← Chinese docs
└── .gitignore
```

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: torch` | `pip install torch --index-url https://download.pytorch.org/whl/cpu` |
| `No module named 'transformers'` | `pip install transformers` |
| `No module named 'shapely'` | `pip install shapely` |
| `OSError: [WinError 1314]` | Already handled — script sets `HF_HUB_DISABLE_SYMLINKS=1` |
| `find_pruneable_heads_and_indices` | `pip install "transformers<5"` |

---

## Credits

- [MinerU](https://github.com/opendatalab/MinerU) by OpenDataLab
- [Reasonix Code](https://reasonix.com)

## License

MIT
