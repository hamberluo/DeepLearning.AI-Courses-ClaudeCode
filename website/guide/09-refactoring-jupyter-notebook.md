---
title: 重构 Jupyter Notebook 并制作仪表盘
---

# 重构 Jupyter Notebook 并制作仪表盘

::: info 本节信息
讲师 Elie Schoppik（Anthropic）· 时长约 12:00 · [▶ DeepLearning.AI 课程页](https://learn.deeplearning.ai/courses/claude-code-a-highly-agentic-coding-assistant/lesson/33kzr/refactoring-a-jupyter-notebook-%26-creating-a-dashboard)
:::

::: tip 关于本节
本节在搬运的 YouTube 播放列表里缺失，文字稿取自 DeepLearning.AI 公开课程页。
:::

Claude Code 自带读取和编辑 Jupyter notebook 的工具。这一节，我们做第二个例子：用 Claude Code **重构一个 Jupyter notebook，并把它变成一个仪表盘**。

## 一个又乱又糙的 notebook

我这里有个 notebook，装着一些虚构的电商数据。它从 `ecommerce_data` 文件夹里的几个 CSV 读数据，用 pandas 读进来、显示出来。能拿到想要的答案，但**这些数据组织得并不好**：格式和展示都不太顺眼。

往下翻，我开始做更复杂的操作，比如挖出**逐年的营收**（2023 对 2022），中间还涉及两个 CSV 和数据框（DataFrame）的合并。我一步步逼近答案，但过程中冒出一些警告（warning），光是把结果在视觉上恰当呈现就得花不少时间——结果是拿到了，但**又啰嗦又乱**。

带着这个想法，我们来用 Claude Code 重构它，把**业务逻辑**和**展示**更好地分开。

## 写一份清楚的重构提示词

我打开 Claude，准备贴进一条事先写好的提示词，用 `@` 引用了这个 notebook 和其他文件。

> **如果你不确定该怎么提示、怎么向 Claude 提要求，随时可以问 Claude 本身。** 我常常直接问它：「我想做这件事，给我一条最好的提示词来完成它。」

提示词里有几块：对结构布局的**重构要求**、一些**代码质量改进**，以及对几个特定 Python 文件的要求。我们让 Claude：单独建一个 Python 文件负责**加载和处理数据**，再建一个负责**计算指标**。这种**关注点分离**，能让我们更好地测试、也更好地理解代码。我们还要求**改进可视化**，并对数据多一点**配置**能力。

> 总的来说，**让 Claude 知道你期待什么，是个好习惯**。别只说「重构一下」，而要说清楚你想要的底层资产、函数文档、业务指标计算方式、依赖文件，以及一个 README。

下面这段回放，还原了「读 notebook → 拆出模块 → 重写 notebook」的过程：

<ClaudeReplay scene="notebook" title="claude code · 重构 notebook" />

它用「读 notebook」的工具去探查单元格、分析结构，然后建出负责加载数据、处理数据、计算业务指标的几个文件。这种**面向对象**的写法，比把一切都塞进 notebook 里干净多了。

## 出了个 KeyError，让 Claude 修

我把所有单元格跑一遍，往下滚发现**这里报错了**，像是某种 **KeyError**。那我让 Claude 帮我修：我说「我跑某个单元格时遇到 KeyError」，并**直接把我用的代码也给它**，让它多点上下文。Claude 查出问题、替我改好。

改完再跑，报错没有了。再看返回的业务指标：摘要更漂亮、客户满意度更好读；营收分析数值更清晰；品类表现、按州的地理可视化（悬停还能看逐州信息）都如预期般不错。

## 从 notebook 到 Streamlit 仪表盘

接下来我想从 notebook 迈向一个**基于网页的界面**——一个用 **Streamlit** 驱动的漂亮仪表盘。Streamlit 是一个 Python 库，很适合做仪表盘，能非常顺滑地从 notebook 过渡过来。

我新建一个 markdown 文件 `convert-to-dashboard.md` 放提示词，让 Claude 把重构后的 notebook **按这个确切布局**转成专业的 Streamlit 仪表盘：

- 一个带**标题和筛选器**的页头；
- 一排 **KPI 卡片**：营收、增长、平均订单价值、订单总数；
- 一些**图表**：营收、品类、按州营收，以及一个满意度柱状图；
- 底部一行放**两张卡片**。

它创建仪表盘：导入 Streamlit、pandas、Plotly，写自定义 CSS 做样式、更新 `requirements.txt`。我开一个新终端，用 `streamlit run dashboard.py` 启动——发现没有 `streamlit` 命令，于是 `pip install` 装齐依赖再跑。

## 再迭代：默认年份与月份筛选

回浏览器看，这个仪表盘是个不错的起点，但缺了点东西：那些卡片是**空的**、而且多余；同时**从 2024 开始**有点别扭。所以让 Claude：把**默认年份设成 2023**、加上**按月份筛选**、**去掉每行那张空卡片**。

回浏览器看效果：2023 成了默认值，空卡片也没了。短短时间里，我们从一个又乱又难读的 notebook，迁移到了一个**能部署、能和团队共享、能快速迭代**的仪表盘。

下一节，我们会构建一个 **Next.js** 应用，并用 Claude Code 连接 **Figma 和 Playwright** 的 MCP 服务器——从一张设计稿出发，快速搭出一个强大的 Web 应用。
