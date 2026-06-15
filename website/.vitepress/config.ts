import { defineConfig } from 'vitepress'

// 部署到 GitHub Pages 项目站点时 base 为仓库名；接自定义域名时改回 '/'。
const base = process.env.DOCS_BASE ?? '/DeepLearning.AI-Courses-ClaudeCode/'

export default defineConfig({
  title: 'Claude Code 中文精讲',
  description: 'DeepLearning.AI × Anthropic《Claude Code: A Highly Agentic Coding Assistant》中文教程，文字 + 可交互代码动画',
  lang: 'zh-CN',
  base,
  cleanUrls: true,
  appearance: 'dark',
  lastUpdated: true,
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '开始学习', link: '/guide/01-introduction' },
      { text: '术语表', link: '/glossary' },
    ],
    sidebar: [
      {
        text: '课程目录',
        items: [
          { text: '01 · 课程介绍', link: '/guide/01-introduction' },
          { text: '02 · 什么是 Claude Code', link: '/guide/02-what-is-claude-code' },
          { text: '03 · 配置与读懂代码库', link: '/guide/03-setup-and-codebase-understanding' },
          { text: '04 · 添加功能（一）', link: '/guide/04-adding-features-1' },
          { text: '05 · 添加功能（二）', link: '/guide/05-adding-features-2' },
          { text: '06 · 测试 / 调试 / 重构', link: '/guide/06-testing-debugging-refactoring' },
          { text: '07 · 同时推进多个功能', link: '/guide/07-adding-multiple-features' },
          { text: '08 · GitHub 集成与 hooks', link: '/guide/08-github-integration-and-hooks' },
          { text: '09 · 重构 Jupyter Notebook', link: '/guide/09-refactoring-jupyter-notebook' },
          { text: '10 · 从 Figma 稿做 Web App', link: '/guide/10-creating-web-app-figma' },
          { text: '11 · 结束语', link: '/guide/11-conclusion' },
        ],
      },
      {
        text: '附录',
        items: [{ text: '术语表', link: '/glossary' }],
      },
    ],
    search: { provider: 'local' },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/hamberluo/DeepLearning.AI-Courses-ClaudeCode' },
    ],
    outline: { level: [2, 3], label: '本页目录' },
    docFooter: { prev: '上一节', next: '下一节' },
    lastUpdatedText: '最后更新',
    darkModeSwitchLabel: '主题',
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '目录',
  },
})
