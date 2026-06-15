import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import ClaudeReplay from '../../components/ClaudeReplay.vue'
import AgentLoopDemo from '../../components/AgentLoopDemo.vue'
import MemoryLayersDemo from '../../components/MemoryLayersDemo.vue'
import PlanModeDemo from '../../components/PlanModeDemo.vue'
import WorktreeDemo from '../../components/WorktreeDemo.vue'
import HooksTimelineDemo from '../../components/HooksTimelineDemo.vue'
import AudioPlayer from '../../components/AudioPlayer.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('ClaudeReplay', ClaudeReplay)
    app.component('AgentLoopDemo', AgentLoopDemo)
    app.component('MemoryLayersDemo', MemoryLayersDemo)
    app.component('PlanModeDemo', PlanModeDemo)
    app.component('WorktreeDemo', WorktreeDemo)
    app.component('HooksTimelineDemo', HooksTimelineDemo)
    app.component('AudioPlayer', AudioPlayer)
  },
} satisfies Theme
