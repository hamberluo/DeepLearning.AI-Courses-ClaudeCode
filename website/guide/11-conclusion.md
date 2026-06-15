---
title: 结语
---

# 结语

::: info 本节信息
讲师 Elie Schoppik（Anthropic）· 时长 00:37 · [▶ 原视频](https://www.youtube.com/watch?v=WKr4f7tfyPU)
:::

<AudioPlayer src="audio/11-conclusion.mp3" />

恭喜你走到这里！

你已经学会了怎么用 Claude Code 去**探索、测试、重构和调试**代码库。

## 用到极致，记住这几点

想把 Claude Code 用到极致，把下面这几条变成习惯：

- **给清晰的指令、讲清上下文**：别只说「重构一下」，把当前状态、期望状态、要求都说清楚。
- **指向相关文件**：用 `@` 把该改的文件直接喂给它，比让它自己满世界找高效得多。
- **先计划，后动手**：改动稍大就进计划模式（Shift+Tab×2），认可计划后再执行。
- **把规则写进 `CLAUDE.md`**：项目级（进 git、团队共享）、本地级（`CLAUDE.local.md`、不共享）、用户级（全局通用）——按影响范围选对层。
- **从测试入手**：先写测试再改代码，给「持续盖楼」打下稳固地基。
- **扩展它的能力**：把它连上 Playwright、Figma 这样的 MCP 服务器，让它能截图、读设计稿、自我验证。
- **并行干活**：用 Git worktree 同时跑多个 Claude，互不覆盖，最后让 Claude 帮你合并。

谢谢你一路同行，迫不及待想看看你会用 Claude Code 创造出什么。

::: tip 下一步
想动手实践，可以去官方配套仓库拿每节课的提示词与代码：[https-deeplearning-ai/sc-claude-code-files](https://github.com/https-deeplearning-ai/sc-claude-code-files)
:::
