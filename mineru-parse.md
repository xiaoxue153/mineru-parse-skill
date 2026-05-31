# MinerU Parse Skill for Reasonix Code
#
# 将此文件放到 .reasonix/skills/ 目录下。
# 之后在 Reasonix 中对话即可调用：
#   "解析这篇论文 @path/to/paper.pdf"
#   "/skill mineru-parse"

# 前置条件
# - Python 3.10 ~ 3.13
# - pip install mineru torch torchvision transformers shapely pyclipper six ftfy

## 执行流程

1. 用 `get_file_info` 确认文件存在
2. 运行解析:
   ```
   python mineru_parse.py "<用户提供的文件路径>"
   ```
3. 验证 `{原文件名}_解析结果.md` 已生成
4. 报告文件大小和路径

## 输出
- Markdown 文件与原文件同级: `{原文件名}_解析结果.md`
- MinerU 完整原始输出: `{原文件名}/auto/` 目录

## 注意
- 首次运行需下载模型（~2GB），后续缓存复用
- Windows 用户如遇符号链接错误（WinError 1314），脚本已自动处理
