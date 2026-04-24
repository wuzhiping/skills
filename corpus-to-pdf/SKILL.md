---
name: corpus-to-pdf
description: The corpus is converted into Markdown according to its structure, and then `generate_pdf.py` converts the Markdown into a beautiful PDF.
---

# 任务执行流程

## 第一阶段：语料转换为markdown
1. 获取语料
接收用户提供的语料内容，支持格式：
- 纯文本、文章、作文、对话
- 多段长文本（需自动拆分）
- 含图片/链接的富文本

2. 分析结构并拆分
- 识别结构：提取主标题、子标题、段落、列表、引用、代码块、表格、图片、链接。
- 拆分策略：
  - 若语料内容较少或单一主题：生成单个 Markdown 文件。
  - 若语料内容较多或多主题：按主标题或逻辑章节拆分为多个 Markdown 文件。
- 命名规范：按顺序命名，统一使用小写+连字符格式：
```plain
01-introduction.md
02-vocabulary.md
03-dialogue.md
04-grammar.md
```
> 规则：{两位数字}-{kebab-case标题}.md，如 02corpus.md ❌ → 02-corpus.md ✅

3. 转换格式
| 原始元素 | Markdown 格式    | 示例                                                                     |
| ---- | -------------- | ---------------------------------------------------------------------- |
| 主标题  | `# `           | `# 第一章 基础词汇`                                                           |
| 子标题  | `## ` / `### ` | `## 1.1 单词表`                                                           |
| 无序列表 | `- `           | `- apple /ˈæpl/ n. 苹果`                                                 |
| 有序列表 | `1. `          | `1. 首先打开书本`                                                            |
| 重点词汇 | `**加粗**`       | `**apple** /ˈæpl/ n. 苹果`                                               |
| 引用内容 | `> `           | `> 语言是思维的边界`                                                           |
| 图片   | `![alt](path)` | `![示意图](images/chart.png)`                                             |
| 链接   | `[text](url)`  | `[参考链接](https://example.com)`                                          |
| 表格   | `\|` 分隔符       | `\| 单词 \| 音标 \| 释义 \|`                                                 |
| 代码块  | ` ```python `  | 带语言标识的三反引号                                                             |
| 分页符  | HTML 注释        | `<!-- pagebreak -->` 或 `<div style="page-break-after: always;"></div>` |
| 其他内容 | 保留原样           | 维持原始段落结构                                                               |

4. 保存文件
- 输出目录：corpus/
- 编码：UTF-8
- 文件清单：保存后向用户汇报生成的文件列表及数量。

## markdown转换为pdf
1. 执行转换
`generate_pdf.py` 使用 `__file__` 自动定位 Skill 根目录，**无需关心当前工作目录**。

### 基本用法（使用默认路径）
```bash
uv run <SKILL_ROOT>/scripts/generate_pdf.py -i ./corpus -o ./corpus.pdf
```

2. 日志与结果同步
- 实时输出：将 generate_pdf.py 的 stdout/stderr 实时同步给用户。
- 失败：捕获异常，分类提示：
  - ModuleNotFoundError → Python 依赖缺失，指引 uv add markdown weasyprint pymdown-extensions
  - FileNotFoundError → Markdown 文件路径错误，检查 corpus/ 目录
