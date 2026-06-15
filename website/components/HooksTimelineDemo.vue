<script setup>
import { ref, computed } from 'vue'

// 一次「读取文件」请求在生命周期里经过的事件点；我们在 PostToolUse 挂了个钩子
const events = [
  { id: 'submit', name: 'UserPromptSubmit', desc: '你提交提示词：「读取 run.sh 的内容」', hook: false },
  { id: 'pre', name: 'PreToolUse', desc: '工具执行之前——这里甚至可以阻止某个工具被调用', hook: false },
  { id: 'tool', name: '执行 Read 工具', desc: 'Claude 读取 run.sh', hook: false, isTool: true },
  { id: 'post', name: 'PostToolUse', desc: '工具执行之后——我们挂的钩子在这里触发', hook: true },
  { id: 'notify', name: 'Notification', desc: '需要通知时', hook: false },
  { id: 'stop', name: 'Stop', desc: '本次动作结束时', hook: false },
]

const cur = ref(-1)
const fired = computed(() => cur.value >= 0 && events[cur.value].hook)
const done = computed(() => cur.value >= events.length - 1)
function next() { if (!done.value) cur.value++; else cur.value = -1 }
function reset() { cur.value = -1 }
</script>

<template>
  <div class="hk">
    <div class="config">
      <span class="tag">.claude/settings.local.json</span>
      <pre>{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Read|Grep",
      "command": "say 'All done!'"
    }]
  }
}</pre>
      <p class="cdesc">含义：每当用到 <code>Read</code> 或 <code>Grep</code> 工具<strong>之后</strong>，就执行 <code>say 'All done!'</code>（让电脑念出来）。</p>
    </div>

    <div class="timeline">
      <div v-for="(e, i) in events" :key="e.id" class="ev" :class="{ on: i === cur, hookpt: e.hook, tool: e.isTool }">
        <span class="dot"></span>
        <div class="meta">
          <span class="nm">{{ e.name }}<span v-if="e.hook" class="badge">⬅ 钩子触发</span></span>
          <span v-if="i <= cur" class="ds">{{ e.desc }}</span>
        </div>
      </div>
    </div>

    <div class="speak" :class="{ show: fired }">🔊 “All done!”</div>

    <div class="controls">
      <button class="primary" @click="next">{{ done ? '再放一遍' : '下一步' }}</button>
      <button @click="reset">重置</button>
    </div>
    <p class="hint">可挂钩子的事件不止这些（还有子代理响应前等）。常见用途：自动跑测试 / linter、阻止危险工具、让 Claude 自查。⚠️ 运行任意 shell 命令务必小心。</p>
  </div>
</template>

<style scoped>
.hk { border: 1px solid var(--vp-c-divider); border-radius: 12px; padding: 1.3rem; margin: 1.5rem 0; background: var(--vp-c-bg-soft); }
.config { margin-bottom: 1.1rem; }
.tag { font-size: 0.72rem; color: var(--vp-c-text-3); font-family: var(--vp-font-family-mono); }
.config pre { margin: 0.3rem 0 0.4rem; background: var(--vp-c-bg); border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 0.7rem 0.9rem; font-size: 0.76rem; overflow-x: auto; color: var(--vp-c-text-1); }
.cdesc { margin: 0; font-size: 0.82rem; color: var(--vp-c-text-2); }
.timeline { display: flex; flex-direction: column; gap: 0; position: relative; padding-left: 0.3rem; }
.ev { display: flex; gap: 0.7rem; padding: 0.45rem 0; align-items: flex-start; opacity: 0.45; transition: opacity 0.3s; }
.ev.on { opacity: 1; }
.ev .dot { width: 12px; height: 12px; border-radius: 50%; background: var(--vp-c-divider); margin-top: 0.25rem; flex-shrink: 0; transition: all 0.3s; }
.ev.on .dot { background: var(--vp-c-brand-1); box-shadow: 0 0 0 4px var(--vp-c-brand-soft); }
.ev.hookpt.on .dot { background: #22c55e; box-shadow: 0 0 0 4px rgba(34,197,94,0.22); }
.ev.tool.on .dot { background: #5eb0ef; }
.nm { font-weight: 600; color: var(--vp-c-text-1); font-family: var(--vp-font-family-mono); font-size: 0.84rem; }
.badge { margin-left: 0.5rem; font-family: inherit; font-size: 0.72rem; color: #22c55e; font-weight: 700; }
.ds { display: block; font-size: 0.8rem; color: var(--vp-c-text-2); margin-top: 0.15rem; }
.speak { text-align: center; margin-top: 0.9rem; font-size: 1.05rem; font-weight: 700; color: #22c55e; opacity: 0; transform: scale(0.8); transition: all 0.3s; }
.speak.show { opacity: 1; transform: scale(1); }
.controls { display: flex; gap: 0.55rem; margin-top: 1rem; }
.controls button { padding: 0.32rem 0.95rem; border-radius: 8px; cursor: pointer; border: 1px solid var(--vp-c-brand-1); background: transparent; color: var(--vp-c-brand-1); font-size: 0.82rem; transition: all 0.2s; }
.controls button:hover { background: var(--vp-c-brand-soft); }
.controls button.primary { background: var(--vp-c-brand-1); color: #fff; }
.hint { margin: 0.8rem 0 0; font-size: 0.8rem; color: var(--vp-c-text-3); }
</style>
