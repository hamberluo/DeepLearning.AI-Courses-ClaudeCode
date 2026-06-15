# DeepLearning.AI《Claude Code》课程中文化项目 — 设计文档

- 日期：2026-06-15
- 状态：阶段① 设计已确认，待开工

## 0. 项目目标

把 DeepLearning.AI × Anthropic 的短课 **《Claude Code: A Highly Agentic Coding Assistant》**（讲师 Elie Schoppik，Andrew Ng 开场，共 11 个视频 / 约 1h43m）做成一个**中文学习产品**，最终形态包含：

1. 高质量中文教程文稿
2. 一个漂亮的 GitHub Pages 静态站（文字 + 代码动画）
3. manim 动画版教程（中文女声、1.5 倍速）

全程中文。

## 1. 最高指导原则：保留「连小孩都听得懂」的灵魂

吴恩达系列课程被公认「连小孩都听得懂」。本项目所有中文转译**必须保留这层平实、好懂、把复杂讲简单的风格**：

- 用大白话和生活化比喻，不用「翻译腔」。
- 宁可多一句解释，也不留下读者看不懂的术语黑话。
- 句子短、节奏顺，像讲师在面对面聊天，而不是念论文。

这是凌驾于一切格式规范之上的准则。

## 2. 推进方式：串行三阶段

```
阶段① 字幕抓取 + 中文整理翻译   ← 当前阶段
阶段② GitHub Pages 网站（文字 + 代码动画）
阶段③ manim 动画课（中文女声 1.5×）
```

每阶段端到端跑通、确认后再进入下一阶段。每个子项目各自走 spec → plan → 实现。

## 3. 素材源（已核实并落地）

- YouTube 播放列表：`PLM3BowDjMUhai9fgX3JK_ZiMt8BotHZaH`（搬运频道 **Ted Tyler**）。
- 视频带**人工英文字幕 `en-GB`**（非机器自动），质量高。
- 中文由我们自己整理 + 翻译，**不使用** YouTube 的机翻 zh-Hans。

### 3.1 源播放列表的两处缺陷（已查清并修复）

抓取后逐条核对内容发现：

- **缺陷 A**：播放列表第 9 个视频（`WKr4f7tfyPU`，标题写「Refactoring a Jupyter Notebook」）实际只有 **37 秒**，且内容是**全课结束语**，并非 Jupyter 正课。
- **缺陷 B**：第 11 个视频（`aqcrYciF04s`，标题「Conclusion」）的字幕与第 08 节「Github & Hooks」**逐字节相同**（错误重复），并非真正的结束语。

**修复方案：**
- 缺失的 **Jupyter 正课**：从 DeepLearning.AI 公开课程页（lesson `33kzr`）抓取完整英文文字稿，存为 `09-refactoring-jupyter-notebook.en.txt`（无时间戳，但产出本就是中文文章，不影响）。
- **结束语**：使用那段 37 秒片段的字幕（即原第 9 个视频内容），存为 `11-conclusion.en.srt`。
- 丢弃错误重复的第 11 个视频字幕。

### 3.2 最终素材清单（11 个文件 = 完整 10 节课 + 结束语）

| 文件 | 来源 | 内容 |
|---|---|---|
| 01-introduction.en.srt | YT `_tHVJuIbc-s` | Introduction |
| 02-what-is-claude-code.en.srt | YT `JjQBijjVnMo` | What is Claude Code? |
| 03-setup-and-codebase-understanding.en.srt | YT `GMcGddfI8ls` | Setup & Codebase Understanding |
| 04-adding-features-1.en.srt | YT `srUCKLoe20E` | Adding Features (1) |
| 05-adding-features-2.en.srt | YT `HbqK8aPdcB0` | Adding Features (2) |
| 06-testing-debugging-refactoring.en.srt | YT `Ifx7Lb1ehu8` | Testing, Error Debugging & Refactoring |
| 07-adding-multiple-features.en.srt | YT `tn9W_WT779g` | Adding Multiple Features Simultaneously |
| 08-github-integration-and-hooks.en.srt | YT `icM60GWLpME` | Github Integration & Hooks |
| 09-refactoring-jupyter-notebook.en.txt | DLAI 课程页 `33kzr` | Refactoring a Jupyter Notebook & Dashboard |
| 10-creating-web-app-figma.en.srt | YT `nn5T9457tLU` | Creating Web App from a Figma Mockup |
| 11-conclusion.en.srt | YT `WKr4f7tfyPU`(37s) | Conclusion |

### 3.3 官方配套代码仓库（阶段②关键素材）

GitHub `https-deeplearning-ai/sc-claude-code-files` 提供**每节课的 prompts / reading notes + 完整代码文件**（含 Jupyter notebook 原版与重构版、Python 模块、Streamlit dashboard、示例数据集）。
→ 这解决了「课程里现场敲的代码不在字幕里」的隐患，是阶段②「代码动画」的代码来源。

## 4. 阶段① 详细设计

### 4.1 目录结构

```
DeepLearning.AI-Courses-ClaudeCode/
├── README.md
├── scripts/
│   └── fetch_subs.sh        # yt-dlp 批量抓 en-GB 英文字幕
├── data/
│   ├── playlist.json        # 11 个视频清单：序号/videoId/标题/时长/链接
│   └── subtitles/
│       ├── 01-introduction.en.srt
│       └── ...
├── glossary.md              # 术语对照表
└── content/                 # 最终产出：中文文稿
    ├── 01-introduction.md
    └── ...
```

### 4.2 Pipeline

1. **抓取**：`scripts/fetch_subs.sh` 用 yt-dlp 对整个 playlist 下载 `en-GB` 人工字幕
   （`--write-subs --sub-langs en-GB --skip-download --convert-subs srt`），落地 `data/subtitles/`。
2. **清洗**：去时间戳、合并碎句、去口水词（um/you know/重复）→ 干净英文段落（中间产物）。
3. **精翻润色**：由 AI 逐节翻译 + 润色，遵循第 1 节灵魂准则，产出 `content/NN-title.md`。

### 4.3 中文文稿格式

每篇 `content/NN-title.md` 含：

- front matter（供阶段②网站消费）：

```yaml
---
order: 1
slug: introduction
title_en: Introduction
title_zh: 课程介绍
instructor: Elie Schoppik
youtube_id: _tHVJuIbc-s
youtube_url: https://www.youtube.com/watch?v=_tHVJuIbc-s
duration: "04:26"
---
```

- 正文：分段 + 小标题，流畅口语化中文。

### 4.4 术语处理规范

`glossary.md` 列出全部术语（中文译名 + 一句话解释）。正文分三类：

1. **专有名词/产品名/协议名 → 永远英文不翻**：`Claude Code`、`MCP`、`CLAUDE.md`、`Figma`、`RAG`、`Git`。
2. **有自然中译的功能词 → 首次「中文（English）」，之后取顺**：`钩子（hooks）`、`子代理（subagent）`、`斜杠命令（slash command）`、`工作树（worktree）`。
3. **已有通用中译的普通词 → 直接中文**：`上下文`(context)、`提示词`(prompt)、`仓库`(repository)、`提交`(commit)。

### 4.5 命名约定

文件名用课程原序号 + kebab-case，如 `03-setup-and-codebase-understanding.md`。

### 4.6 阶段① 产出

- 11 篇高质量中文教程文稿（`content/`）
- 干净的术语表（`glossary.md`）
- 可复用的抓取脚本（`scripts/fetch_subs.sh`）+ 视频清单（`data/playlist.json`）

→ 直接作为阶段②网站的内容源。

## 5. 后续阶段轮廓（细节待该阶段再定）

### 阶段② GitHub Pages 网站

- 静态站，展示「文字 + 代码动画」。
- 内容源 = 阶段① 的 `content/*.md` + front matter。
- 代码素材源 = 官方仓库 `https-deeplearning-ai/sc-claude-code-files`（见 §3.3）。
- 代码动画形态待定（打字机 / 滚动叙事 scrollytelling / diff 高亮）。
- 技术栈待定。

### 阶段③ manim 动画课

- manim 生成讲解动画 + 中文女声 TTS，1.5 倍速。
- TTS 引擎待定（say / Edge-TTS / Azure / 火山 / ElevenLabs）。
- 动画定位待定（重新创作的讲解动画 vs 复刻原视频）——直接决定工作量量级。
- manim 尚未安装。

## 6. 暂不做（YAGNI）

- 不做视频下载（只要字幕；正片在 YouTube 可看）。
- 不用 YouTube 机翻中文字幕。
- 阶段②③ 的技术细节本阶段不锁定。
