# MinerU Parse Skill

> **一键将 PDF / DOCX / PPTX / XLSX / 图片解析为结构化 Markdown**
>
> 基于 [MinerU](https://github.com/opendatalab/MinerU)（OpenDataLab）的文档解析工具，
> 封装为可直接调用的 Python 脚本 + Reasonix Code 技能，告别手动处理文档的繁琐流程。

---

## 它能做什么

你有一篇论文 PDF / 合同 DOCX / 课件 PPTX，想把它变成结构化的 Markdown 或 JSON 文本，方便：
- 喂给大模型做 RAG 检索
- 在 Reasonix 里对话分析
- 提取表格、公式等结构化内容

这个项目就是做这件事的。**一行命令，自动完成解析并在同目录输出 `.md` 文件。**

---

## 功能特性

- **多格式支持** — PDF、DOCX、PPTX、XLSX、图片
- **结构化输出** — Markdown + JSON（表格 → HTML，公式 → LaTeX）
- **版面保持** — 按人类阅读顺序重组内容，自动去除页眉页脚
- **一键调用** — 命令行传文件路径即可
- **自动输出** — 解析结果自动保存到原文件同目录
- **Reasonix 技能集成** — 可注册为 `/skill`，对话中直接 `@文件路径` 调用
- **纯 CPU 可用** — 无需 GPU，pipeline 后端在普通电脑上也能跑

---

## 快速开始

### 1. 环境要求

- Python **3.10 ~ 3.13**（⚠️ 不要用 3.14，部分依赖还不支持）
- Windows / Linux / macOS

### 2. 安装 MinerU

```bash
pip install mineru
```

> Windows 用户如果遇到 `ModuleNotFoundError: torch`，装 CPU 版 PyTorch：
> ```bash
> pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
> ```

### 3. 安装常用依赖

如果运行时缺包，一次性装全：

```bash
pip install torch torchvision transformers shapely pyclipper six ftfy
```

### 4. 运行

```bash
python mineru_parse.py "你的文件路径.pdf"
```

**输出效果**：原文件同级目录会出现：
```
你的文件.pdf                              ← 原始文件
你的文件_解析结果.md                       ← ✨ 解析出的 Markdown
你的文件/auto/                             ← MinerU 完整输出（含 JSON）
```

---

## 在 Reasonix Code 中使用

将 `mineru-parse.md` 复制到你的项目 `.reasonix/skills/` 目录：

```
your-project/
└── .reasonix/
    └── skills/
        └── mineru-parse.md
```

然后在 Reasonix 中直接说：

> "解析这篇论文 @path/to/paper.pdf"

Reasonix 会自动调用 MinerU 完成解析并返回结果。

---

## 解析流程

```
用户提供文件路径
        │
        ▼
mineru_parse.py
  ├── 设置 HF_HUB_DISABLE_SYMLINKS=1  （修复 Windows 符号链接问题）
  ├── 调用: mineru -p <文件> -o <目录> -b pipeline
  │     ├── Layout Detect  版面检测    (20页约30秒)
  │     ├── MFR 公式识别    → LaTeX
  │     ├── Table OCR 表格识别 → HTML
  │     ├── Text OCR 文字识别
  │     └── 阅读顺序重组    → 最终 Markdown
  └── 复制输出 .md 到原文件同目录
```

### 各阶段说明

| 阶段 | 功能 | 输出 |
|------|------|------|
| 版面检测 | 识别页面结构（正文/表格/图片区域） | 布局框 |
| 公式识别 | 识别数学公式 | LaTeX 字符串 |
| 表格识别 | 提取表格并识别单元格内容 | HTML 表格 |
| OCR 检测+识别 | 检测并识别文字区域 | 文本内容 |
| 阅读顺序 | 按人类阅读顺序重组内容 | Markdown |

---

## 依赖清单

- [MinerU](https://github.com/opendatalab/MinerU) 3.1+
- PyTorch（CPU 版即可）
- torchvision
- transformers（4.x 版本，5.x 不兼容）
- shapely、pyclipper、six、ftfy

---

## 项目文件

```
mineru-parse-skill/
├── mineru_parse.py          # 核心脚本 — 传文件路径即解析
├── mineru-parse.md          # Reasonix Code 技能定义文件
├── requirements.txt         # Python 依赖
├── README.md                # 英文文档
├── README_CN.md             # 中文文档（本文件）
└── .gitignore
```

---

## 常见问题

| 问题 | 解决办法 |
|------|----------|
| `ModuleNotFoundError: torch` | `pip install torch --index-url https://download.pytorch.org/whl/cpu` |
| `No module named 'transformers'` | `pip install transformers` |
| `No module named 'shapely'` | `pip install shapely` |
| `OSError: [WinError 1314]` 符号链接权限不足 | 脚本已自动设 `HF_HUB_DISABLE_SYMLINKS=1` |
| `find_pruneable_heads_and_indices` 报错 | 降级 transformers：`pip install "transformers<5"` |
| 运行成功但没看到输出 | 检查 `{文件名}/auto/` 子目录，MinerU 原始输出在里面 |

---

## 开放许可

MIT License

---

## 致谢

- [MinerU](https://github.com/opendatalab/MinerU) — OpenDataLab 出品的开源文档解析引擎
- [Reasonix Code](https://reasonix.com) — AI 编程助手平台
