---
layout: home

hero:
  name: Claude Code 中文精讲
  text: 高度自主的编程助手
  tagline: DeepLearning.AI × Anthropic 短课的中文版 · 文字 + 可交互代码动画 · 连小孩都听得懂
  actions:
    - theme: brand
      text: 开始学习
      link: /guide/01-introduction
    - theme: alt
      text: 术语表
      link: /glossary
    - theme: alt
      text: GitHub
      link: https://github.com/hamberluo/DeepLearning.AI-Courses-ClaudeCode

features:
  - icon: 🧠
    title: 它不只是「写代码」
    details: 从发现、解释、设计讲起——先用 Claude Code 读懂一个大代码库，再动手改。
  - icon: 🛠️
    title: 看懂 agent 怎么干活
    details: 用可交互的会话回放，一步步看 Claude 思考、调用工具、改文件、出结果。
  - icon: 🌲
    title: 进阶玩法
    details: Git worktree 并行、MCP 扩展工具、hooks 注入、从 Figma 稿生成 Web App。
---

## 这门课讲什么

这是 DeepLearning.AI 与 Anthropic 联手打造的短课 **《Claude Code: A Highly Agentic Coding Assistant》** 的中文精讲版。讲师 Elie Schoppik（Anthropic），吴恩达开场。

我们没有照搬机翻字幕，而是把全部英文人工字幕重新整理、翻译、润色成**平实好懂的中文文章**，并为每节配上**可交互的代码动画**——让你不只是「读」，而是「看到」Claude Code 一步步把活干完。

## 课程地图

| # | 标题 | 你会学到 |
|---|---|---|
| [01](/guide/01-introduction) | 课程介绍 | AI 编程这几年的演进，以及「给清晰上下文」为何是关键 |
| [02](/guide/02-what-is-claude-code) | 什么是 Claude Code | agent = 模型 + 工具 + 环境 + 记忆；为什么不建索引 |
| [03](/guide/03-setup-and-codebase-understanding) | 配置与读懂代码库 | `/init`、`CLAUDE.md` 三层记忆、用它快速摸清大项目 |
| [04](/guide/04-adding-features-1) | 添加功能（一） | 计划模式、`@` 引用文件、让它边想边改 |
| [05](/guide/05-adding-features-2) | 添加功能（二） | 在真实代码库里持续迭代功能 |
| [06](/guide/06-testing-debugging-refactoring) | 测试 / 调试 / 重构 | 多轮工具调用，自动定位并修复报错 |
| [07](/guide/07-adding-multiple-features) | 同时推进多个功能 | 用 Git worktree 并行开好几个 Claude |
| [08](/guide/08-github-integration-and-hooks) | GitHub 集成与 hooks | 在 GitHub 上用它，并用 hooks 注入自定义行为 |
| [09](/guide/09-refactoring-jupyter-notebook) | 重构 Jupyter Notebook | 把杂乱 notebook 重构成模块，再做成仪表盘 |
| [10](/guide/10-creating-web-app-figma) | 从 Figma 稿做 Web App | 接 MCP，看着设计稿生成 Next.js 应用 |
| [11](/guide/11-conclusion) | 结束语 | 回顾全课，以及下一步往哪走 |

::: tip 学习建议
按顺序看。每节里遇到 <span style="color:var(--vp-c-brand-1)">可点击的演示</span>，一定亲手点几下「下一步」——动手看一遍，胜过读十遍。
:::
