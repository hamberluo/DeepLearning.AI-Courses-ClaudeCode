<script setup>
import { ref, computed } from 'vue'

// 两种模式对比：左=直接动手，右=先计划后执行
const stages = [
  { id: 'idle', label: '收到需求', sub: '「给来源加上可点击的引用链接」' },
  { id: 'plan', label: '① 计划模式', sub: '按两次 Shift+Tab 进入。Claude 读相关文件、列出改动计划，但一行代码都不写。' },
  { id: 'review', label: '② 你来把关', sub: '看计划：满意就认可；不满意按 Esc 给反馈、让它改。主动权在你。' },
  { id: 'accept', label: '③ 自动接受', sub: '认可后按一次 Shift+Tab 开启 auto-accept，Claude 连续改文件不再逐个问你。' },
  { id: 'done', label: '④ 改动完成', sub: '按计划改完，你在编辑器里看到 diff，再验收。' },
]

const cur = ref(0)
const done = computed(() => cur.value >= stages.length - 1)
function next() { if (!done.value) cur.value++ }
function reset() { cur.value = 0 }
</script>

<template>
  <div class="pm">
    <div class="track">
      <template v-for="(s, i) in stages" :key="s.id">
        <div class="node" :class="{ on: i === cur, past: i < cur }">
          <span class="lbl">{{ s.label }}</span>
        </div>
        <div v-if="i < stages.length - 1" class="seg" :class="{ past: i < cur }"></div>
      </template>
    </div>

    <div class="readout">
      <span class="rt">{{ stages[cur].sub }}</span>
    </div>

    <div class="controls">
      <button class="primary" :disabled="done" @click="next">下一步</button>
      <button @click="reset">重置</button>
    </div>
    <p class="hint">口诀：<strong>改动越大，越要先计划</strong>。Shift+Tab×2 进计划模式，Shift+Tab×1 开自动接受。</p>
  </div>
</template>

<style scoped>
.pm { border: 1px solid var(--vp-c-divider); border-radius: 12px; padding: 1.3rem; margin: 1.5rem 0; background: var(--vp-c-bg-soft); }
.track { display: flex; align-items: center; flex-wrap: wrap; gap: 0.3rem; }
.node {
  padding: 0.5rem 0.8rem; border-radius: 8px; border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg); color: var(--vp-c-text-3); font-size: 0.82rem; transition: all 0.3s;
}
.node.on { border-color: var(--vp-c-brand-1); background: var(--vp-c-brand-soft); color: var(--vp-c-brand-1); font-weight: 700; transform: scale(1.05); }
.node.past { border-color: #22c55e; color: #22c55e; }
.seg { flex: 1; min-width: 14px; height: 2px; background: var(--vp-c-divider); transition: background 0.3s; }
.seg.past { background: #22c55e; }
.readout {
  margin-top: 1rem; padding: 0.85rem 1rem; border-radius: 8px; min-height: 3.3em;
  background: var(--vp-c-bg); border: 1px solid var(--vp-c-divider);
}
.rt { color: var(--vp-c-text-1); line-height: 1.7; }
.controls { display: flex; gap: 0.55rem; margin-top: 1rem; }
.controls button {
  padding: 0.32rem 0.95rem; border-radius: 8px; cursor: pointer;
  border: 1px solid var(--vp-c-brand-1); background: transparent;
  color: var(--vp-c-brand-1); font-size: 0.82rem; transition: all 0.2s;
}
.controls button:hover:not(:disabled) { background: var(--vp-c-brand-soft); }
.controls button.primary { background: var(--vp-c-brand-1); color: #fff; }
.controls button:disabled { opacity: 0.4; cursor: not-allowed; }
.hint { margin: 0.8rem 0 0; font-size: 0.8rem; color: var(--vp-c-text-3); }
</style>
