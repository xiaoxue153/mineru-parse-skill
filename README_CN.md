# MinerU Parse Skill

[**English**](README_EN.md) | [**GitHub**](https://github.com/xiaoxue153/mineru-parse-skill)

> **一键解析 PDF / DOCX / PPTX / XLSX / 图片 → 结构化 Markdown**
>
> 基于 OpenDataLab 开源的 [MinerU](https://github.com/opendatalab/MinerU) 引擎，
> 封装为 Python 脚本 + Reasonix Code 技能。给文件路径，拿 Markdown 结果。

---

## 能干什么

你有一篇论文 PDF、一份合同 DOCX、一份课件 PPTX，想把里面的文字、表格、公式变成结构化的 Markdown——

- 喂给大模型做 RAG
- 在 Reasonix 里对话分析
- 提取表格、公式等结构化数据

这个项目就是干这个的。**一行命令，全自动完成。** 也用不了 GPU，普通电脑就能跑。

```
原始文件.pdf                          →  原始文件_解析结果.md    （Markdown 输出）
                                     →  原始文件/auto/          （MinerU 完整原始输出，含 JSON）
```

---

## 快速开始

### 1. 环境要求

- **Python 3.10 ~ 3.13**（⚠️ 不要用 3.14，部分依赖还不支持）
- Windows / Linux / macOS
- 不需要 GPU

### 2. 安装

```bash
pip install mineru torch torchvision transformers shapely pyclipper six ftfy
```

> Windows 纯 CPU 用户先装 PyTorch：`pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu`

### 3. 运行

```bash
python mineru_parse.py "你的文件路径.pdf"
```

`.pdf` 换成 `.docx`、`.pptx`、`.xlsx` 或图片格式都行。

解析出来的 `.md` 文件自动出现在原文件旁边。

---

## 在 Reasonix Code 中使用

把 `mineru-parse.md` 复制到你的项目 `.reasonix/skills/` 目录下：

```
your-project/
├── .reasonix/
│   └── skills/
│       └── mineru-parse.md
└── ...
```

在 Reasonix 里直接说：

> "解析这篇论文 @path/to/paper.pdf"

或输入 `/skill mineru-parse`。

---

## 解析流程

```
你的文件
    │
    ▼
mineru_parse.py
    │
    ├── 自动设置 HF_HUB_DISABLE_SYMLINKS=1（修复 Windows 符号链接问题）
    ├── 调用 mineru -p <文件> -o <目录> -b pipeline
    │     ├── 版面检测        （识别正文、表格、图片区域）
    │     ├── 公式识别        （MFR → LaTeX）
    │     ├── 表格 OCR        （单元格内容 → HTML 表格）
    │     ├── 文字 OCR        （检测 + 识别文字）
    │     └── 阅读顺序重组    （按人类阅读顺序拼出最终输出）
    └── 把输出 .md 复制到原文件同目录
```

| 阶段 | 检测内容 | 输出格式 |
|------|----------|----------|
| 版面检测 | 页面结构 — 文字块、表格、图片 | 边界框 |
| 公式识别 | 数学公式 | LaTeX |
| 表格 OCR | 含内容的表格单元格 | HTML `<table>` |
| 文字 OCR | 文字区域检测并识别 | 纯文本 |
| 阅读顺序 | 按人类阅读顺序拼装 | 最终 Markdown |

---

## 为什么用这个包装脚本

- **MinerU 原生输出** 藏在复杂的子文件夹（`输入文件名/auto/`）里，这个脚本自动把 `.md` 复制到原文件旁边。
- **不再需要记参数** — `-b pipeline`、符号链接修复全自动处理。
- **Reasonix 集成** — 技能文件让你在对话里 `@文件路径` 就能调用，不用手敲命令。

---

## 文件说明

```
mineru-parse-skill/
├── mineru_parse.py      ← 核心脚本 — 给文件路径，出 Markdown
├── mineru-parse.md      ← Reasonix Code 技能定义文件
├── requirements.txt     ← Python 依赖清单
├── README.md            ← 项目首页（中英双入口）
├── README_EN.md         ← 完整英文文档
├── README_CN.md         ← 完整中文文档（本文件）
└── .gitignore
```

---

## 常见问题

| 错误提示 | 解决办法 |
|----------|----------|
| `ModuleNotFoundError: torch` | `pip install torch --index-url https://download.pytorch.org/whl/cpu` |
| `No module named 'transformers'` | `pip install transformers` |
| `No module named 'shapely'` | `pip install shapely` |
| `OSError: [WinError 1314]` 符号链接 | 脚本已自动处理（设 `HF_HUB_DISABLE_SYMLINKS=1`） |
| `find_pruneable_heads_and_indices` 报错 | `pip install "transformers<5"` |
| 跑完但没看到输出 | 检查 `{文件名}/auto/` 子目录，MinerU 原始输出在里面 |

---

## 致谢

- [MinerU](https://github.com/opendatalab/MinerU) — OpenDataLab 的开源文档解析引擎
- [Reasonix Code](https://reasonix.com) — AI 编程助手

---

## 许可证

MIT
