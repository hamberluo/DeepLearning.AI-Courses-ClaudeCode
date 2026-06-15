import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import ClaudeReplay from '../../components/ClaudeReplay.vue'
import AgentLoopDemo from '../../components/AgentLoopDemo.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('ClaudeReplay', ClaudeReplay)
    app.component('AgentLoopDemo', AgentLoopDemo)
  },
} satisfies Theme
