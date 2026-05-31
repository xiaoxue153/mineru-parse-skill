# MinerU Parse Skill

[**English**](README.md) | **中文简体**

> **一键解析 PDF / DOCX / PPTX / XLSX / 图片 → 结构化 Markdown**
>
> 基于 OpenDataLab 开源的 [MinerU](https://github.com/opendatalab/MinerU) 引擎封装而成。
> 给文件路径，拿 Markdown 结果。也可作为 [Reasonix Code](https://reasonix.com) 技能使用。

---

## 能干什么

你有一篇论文 PDF、一份合同 DOCX、一份课件 PPTX，想把里面的文字、表格、公式变成结构化的 Markdown，用来喂给大模型做 RAG，或者在 Reasonix 里对话分析。

这个项目就是干这个的。**一行命令，全自动完成。** 不需要 GPU，普通电脑就能跑。

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

`.pdf` 换成 `.docx`、`.pptx`、`.xlsx` 或图片格式都行。解析出来的 `.md` 文件会自动出现在原文件旁边。

---

## Reasonix Code 技能集成

把 `mineru-parse.md` 复制到你的项目 `.reasonix/skills/` 目录下：

```
your-project/
└── .reasonix/
    └── skills/
        └── mineru-parse.md
```

在 Reasonix 里直接说：`"解析这篇论文 @path/to/paper.pdf"` 或输入 `/skill mineru-parse`。

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
    │     ├── 版面检测         （识别正文、表格、图片区域）
    │     ├── 公式识别         （→ LaTeX）
    │     ├── 表格 OCR         （→ HTML）
    │     ├── 文字 OCR         （检测 + 识别）
    │     └── 阅读顺序重组     （拼出最终 Markdown）
    └── 把输出 .md 复制到原文件同目录
```

| 阶段 | 检测内容 | 输出 |
|------|----------|------|
| 版面检测 | 页面结构 — 文字、表格、图片 | 边界框 |
| 公式识别 | 数学公式 | LaTeX |
| 表格 OCR | 含内容的表格单元格 | HTML `<table>` |
| 文字 OCR | 文字区域检测并识别 | 纯文本 |
| 阅读顺序 | 按人类阅读顺序拼装 | 最终 Markdown |

---

## 文件说明

```
mineru-parse-skill/
├── mineru_parse.py      ← 核心脚本
├── mineru-parse.md      ← Reasonix 技能定义文件
├── requirements.txt
├── README.md            ← 英文文档
├── README_CN.md         ← 中文文档（本页）
└── .gitignore
```

---

## 常见问题

| 错误提示 | 解决办法 |
|----------|----------|
| `ModuleNotFoundError: torch` | `pip install torch --index-url https://download.pytorch.org/whl/cpu` |
| `No module named 'transformers'` | `pip install transformers` |
| `No module named 'shapely'` | `pip install shapely` |
| `OSError: [WinError 1314]` | 脚本已自动处理（设 `HF_HUB_DISABLE_SYMLINKS=1`） |
| `find_pruneable_heads_and_indices` 报错 | `pip install "transformers<5"` |

---

## 致谢

- [MinerU](https://github.com/opendatalab/MinerU) — OpenDataLab 的开源文档解析引擎
- [Reasonix Code](https://reasonix.com) — AI 编程助手

## 许可证

MIT
