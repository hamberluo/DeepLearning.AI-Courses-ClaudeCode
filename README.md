# Claude Code 中文精讲

把 DeepLearning.AI × Anthropic 的短课 **《Claude Code: A Highly Agentic Coding Assistant》**（讲师 Elie Schoppik，吴恩达开场，共 11 节）做成一个**中文学习产品**：平实好懂的中文文稿 + 可交互代码动画 + 中文女声朗读。

🔗 **在线阅读**：<https://hamberluo.github.io/DeepLearning.AI-Courses-ClaudeCode/>

> 最高准则：保留吴恩达系列「连小孩都听得懂」的灵魂——大白话、生活化比喻、不留术语黑话。

## 这个项目做了什么

| 阶段 | 产物 |
|---|---|
| ① 字幕 → 中文文稿 | 下载英文人工字幕，重新整理、翻译、润色成 11 篇中文文章（`content/`）+ 术语表（`glossary.md`） |
| ② 网站 | VitePress 站点，每节配一个「招牌交互动画」，GitHub Pages 自动部署（`website/`） |
| ③ 语音 | 用 edge-tts 给每节生成中文女声（Xiaoxiao，1.5×）朗读 MP3，页面可「边读边听」 |

每节的招牌交互动画：会话回放（仿真终端逐步播放 Claude 干活）、agent 循环、计划模式、三层 `CLAUDE.md` 记忆、Git worktree 并行、hooks 生命周期等。

## 目录结构

```
.
├── content/                 # 阶段① 中文文稿（干净存档，也是语音稿来源）
├── glossary.md              # 术语对照表
├── data/
│   ├── playlist.json        # 11 节课清单（videoId / 标题 / 时长 / 来源）
│   └── subtitles/           # 英文字幕原文（.srt / .txt）
├── scripts/
│   └── fetch_subs.sh        # yt-dlp 批量抓 en-GB 英文字幕
├── website/                 # 阶段② VitePress 站点
│   ├── guide/               # 11 篇正文（内嵌交互组件 + 朗读播放器）
│   ├── components/          # Vue 交互组件 + AudioPlayer
│   ├── tools/               # build-listen-audio.py（阶段③ TTS 生成脚本）
│   └── .vitepress/          # 站点配置与主题
├── docs/                    # 设计文档
└── .github/workflows/       # GitHub Pages 自动部署
```

## 本地开发

### 网站（VitePress）

```bash
cd website
npm install
npm run docs:dev      # 本地预览 http://localhost:5173/DeepLearning.AI-Courses-ClaudeCode/
npm run docs:build    # 构建到 .vitepress/dist
```

### 生成朗读音频（edge-tts）

MP3 不进 git（生成的二进制），本地预览或部署时按需生成：

```bash
cd website
pip install -r tools/requirements.txt
python tools/build-listen-audio.py                       # 生成全部 11 节
python tools/build-listen-audio.py 02-what-is-claude-code  # 只生成指定节
```

声线 `zh-CN-XiaoxiaoNeural`，语速 `+50%`（≈1.5 倍速）。

### 重新抓取英文字幕（可选）

```bash
bash scripts/fetch_subs.sh   # 依赖 yt-dlp
```

## 部署

push 到 `main` 且改动 `website/**` 时，GitHub Actions 会自动：用 edge-tts 生成音频 → 构建 VitePress → 发布到 GitHub Pages。

## 素材来源

- 课程：[DeepLearning.AI《Claude Code: A Highly Agentic Coding Assistant》](https://learn.deeplearning.ai/courses/claude-code-a-highly-agentic-coding-assistant)
- 官方配套代码：[https-deeplearning-ai/sc-claude-code-files](https://github.com/https-deeplearning-ai/sc-claude-code-files)

## 声明

本项目是上述课程的**非官方中文学习整理**，仅供学习交流。课程版权归 DeepLearning.AI 与 Anthropic 所有；如有侵权请联系删除。
