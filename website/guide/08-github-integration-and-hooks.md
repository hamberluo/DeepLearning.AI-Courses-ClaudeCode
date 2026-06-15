---
title: 探索 GitHub 集成与 hooks
---

# 探索 GitHub 集成与 hooks

::: info 本节信息
讲师 Elie Schoppik（Anthropic）· 时长 12:46 · [▶ 原视频](https://www.youtube.com/watch?v=icM60GWLpME)
:::

<AudioPlayer src="audio/08-github-integration-and-hooks.mp3" />

这一节，你会学到怎么在**终端之外**、通过 **GitHub 集成**来用 Claude Code：怎么配置它来**评审拉取请求（pull request）、修复 issue**。然后你会学到怎么用 **Claude Code 的钩子（hooks）**，在使用工具的前后执行代码。

## 收尾：删掉工作树并推到 GitHub

上一节我们合并了工作树，但忘了让 Claude 把工作树删掉。那就回 Claude——我用 **`--resume`** 参数回到之前那段关于工作树的对话，接着进度把工作树清理干净：「删掉 `.trees` 文件夹和底层的工作树，完成后把代码推到 GitHub。」我们给它权限去查看底层工作树，这样不仅删掉工作树，**对应的分支也一并删掉**，再 `git push origin main`。

## 安装 GitHub 集成

我用 `/install-github-app` 命令安装 Claude Code 自带的 **GitHub 集成**。这里可能需要在命令行里做额外的身份认证——照着设置步骤做就行。

这个集成能让我们在**拉取请求和 issue** 里用 Claude Code：回应反馈、修复错误、改代码等等。这套功能的底层，是 Claude Code 自带的 **SDK（软件开发工具包）**——正是这个 SDK 让你能在终端界面之外使用 Claude Code。

接着指定要安装的**工作流（workflow）**：在 issue 里 **@ 提及 Claude**，以及让 Claude **自动评审**拉取请求里的代码。两个都装。

装好后它会把我送回 GitHub 去**开一个包含这些改动的 PR**。这个 PR 自动让 **GitHub Actions** 启用了修 bug、写测试和代码评审的能力。开箱即用就有一套挺合理的默认值：能按作者过滤、能指定运行条件；想改代码评审里的提示词，在这儿改即可。

我把它**合并**进去，就能开始在 GitHub 里用 Claude Code 了。今后的 PR 里，Claude 都会帮我们读取并分析文件、检查代码质量、识别安全方面的考量——开箱即用，我们就多了一位新队友。这在「人可能漏掉某些东西、需要多一道检查」时非常有用。

## 让 Claude 在 GitHub 里修一个 issue

假设来了个 issue：随着我们不断加功能，出现了一个**新的页头**，但也许我们想**退回**到之前的样子。那就建一条 issue，具体说明：去掉「Course Materials Assistant」这个页头、去掉副标题、再去掉副标题下面那条**横线**，但**保留主题切换**。

建好后，我们**@ 提及 Claude**：「Claude，能帮我修一下吗？」给它点时间处理。你看到的过程会和命令行里**非常眼熟**：分析结构、移除页头、测试改动、提交、推送。

最后 Claude 还会花点时间**评审它自己写的代码**——这其实挺有用：再信任 Claude，也不妨让**另一个 Claude 复查它的工作**。合并它，回 VS Code `pull` 下改动——成了，页头和横线都去掉了。**不只在终端里，在 GitHub 里也能**用 Claude Code。

## hooks：在生命周期的关键节点注入代码

再展示一个最近发布的功能——给 Claude Code 加 **钩子（hooks）**。思路是：在 Claude Code 的不同操作节点上（比如执行某个工具、或某个工具执行之后），我们可以**注入特定代码**，在运行生命周期的任意时刻运行。

回到 VS Code、再进 Claude，输入 `/hooks` 就能管理这些配置。

> ⚠️ 我们有义务提醒你：**如果你要运行任意 shell 命令，务必非常小心你在做什么。**

下面这个示意，演示了一个 **PostToolUse**（工具使用后）钩子是怎么在生命周期里被触发的——我加了个 matcher（匹配器），指定每当用到 **Read** 或 **Grep** 工具时，就跑一条 `say 'All done!'` 让电脑念出来。点「下一步」看它在哪一步触发：

<HooksTimelineDemo />

钩子和权限一样，都存在 `.claude/settings.local.json` 里。试试看：退出再打开 Claude，让它「读取 `run.sh` 的内容」——一用到 read 工具，机器就用语音通知我们「All done」。

这虽然是个好玩的小例子，但你可以想象用它来：**跑测试、跑代码检查器（linter）**；或者在不希望某工具被用时**阻止它**；甚至在特定情况下**让 Claude 评审它自己**。你也随时可以让 Claude Code **帮你写 hooks**。

下一节，我们会探索怎么用 Claude Code 配合 **Jupyter notebook**：做可视化、重构代码。
