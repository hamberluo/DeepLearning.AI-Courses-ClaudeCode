<script setup>
import { ref, computed } from 'vue'

const nodes = [
  { id: 'model', icon: '🧠', name: '模型', desc: '负责思考、决策' },
  { id: 'tools', icon: '🛠️', name: '工具', desc: '读写文件、跑命令…' },
  { id: 'env', icon: '💻', name: '环境', desc: '你的机器 / 代码库' },
  { id: 'memory', icon: '📝', name: '记忆', desc: 'CLAUDE.md / 上下文' },
]

const steps = [
  { active: 'model', text: '你问：「demo 文件夹里的代码是干嘛的？」模型先接到问题。' },
  { active: 'model', text: '模型发现：自己并不知道文件内容，得借助一个工具去读。' },
  { active: 'tools', text: '模型决定调用「读取文件」工具，并说明要读哪个文件。' },
  { active: 'env', text: '工具在你的真实环境里执行，把文件内容取出来。' },
  { active: 'model', text: '内容回到模型手里——它现在「看见」代码了。' },
  { active: 'memory', text: '这次交互被记进上下文，下次提问它还记得。' },
  { active: 'model', text: '模型综合信息，给出回答。一个「问题 → 工具 → 环境 → 结果」的循环就此闭合。' },
]

const cur = ref(-1)
const activeNode = computed(() => (cur.value >= 0 ? steps[cur.value].active : ''))
const curText = computed(() => (cur.value >= 0 ? steps[cur.value].text : '点「下一步」，跟着一个问题走完整个 agent 循环。'))
const done = computed(() => cur.value >= steps.length - 1)

function next() {
  if (!done.value) cur.value++
  else cur.value = 0
}
function reset() {
  cur.value = -1
}
</script>

<template>
  <div class="loop">
    <div class="nodes">
      <template v-for="(n, i) in nodes" :key="n.id">
        <div class="node" :class="{ on: activeNode === n.id }">
          <div class="ic">{{ n.icon }}</div>
          <div class="nm">{{ n.name }}</div>
          <div class="ds">{{ n.desc }}</div>
        </div>
        <div v-if="i < nodes.length - 1" class="arrow" :class="{ live: activeNode }">→</div>
      </template>
    </div>

    <div class="readout">
      <span class="idx" v-if="cur >= 0">{{ cur + 1 }}/{{ steps.length }}</span>
      <span class="rt">{{ curText }}</span>
    </div>

    <div class="controls">
      <button class="primary" @click="next">{{ done ? '再看一遍' : '下一步' }}</button>
      <button @click="reset">重置</button>
    </div>
    <p class="hint">教学示意：真实运行中，「模型 ↔ 工具 ↔ 环境」这个循环可能反复跑很多轮，直到任务完成。</p>
  </div>
</template>

<style scoped>
.loop {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 1.3rem;
  margin: 1.5rem 0;
  background: var(--vp-c-bg-soft);
}
.nodes { display: flex; align-items: stretch; gap: 0.4rem; flex-wrap: wrap; }
.node {
  flex: 1; min-width: 110px; text-align: center;
  border: 1px solid var(--vp-c-divider); border-radius: 10px;
  padding: 0.8rem 0.5rem; transition: all 0.3s ease; background: var(--vp-c-bg);
}
.node.on {
  border-color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
  box-shadow: 0 0 0 2px var(--vp-c-brand-soft);
  transform: translateY(-3px);
}
.ic { font-size: 1.6rem; }
.nm { font-weight: 700; margin-top: 0.25rem; color: var(--vp-c-text-1); }
.ds { font-size: 0.72rem; color: var(--vp-c-text-3); margin-top: 0.15rem; }
.arrow { align-self: center; color: var(--vp-c-text-3); font-size: 1.2rem; transition: color 0.3s; }
.arrow.live { color: var(--vp-c-brand-1); }

.readout {
  margin-top: 1rem; padding: 0.8rem 1rem; border-radius: 8px;
  background: var(--vp-c-bg); border: 1px solid var(--vp-c-divider);
  min-height: 3.2em; display: flex; gap: 0.6rem; align-items: baseline;
}
.idx { color: var(--vp-c-brand-1); font-weight: 700; font-family: var(--vp-font-family-mono); flex-shrink: 0; }
.rt { color: var(--vp-c-text-1); line-height: 1.7; }

.controls { display: flex; gap: 0.55rem; margin-top: 1rem; }
.controls button {
  padding: 0.32rem 0.95rem; border-radius: 8px; cursor: pointer;
  border: 1px solid var(--vp-c-brand-1); background: transparent;
  color: var(--vp-c-brand-1); font-size: 0.82rem; transition: all 0.2s;
}
.controls button:hover { background: var(--vp-c-brand-soft); }
.controls button.primary { background: var(--vp-c-brand-1); color: #fff; }
.controls button.primary:hover { background: var(--vp-c-brand-2); }
.hint { margin-top: 0.8rem; margin-bottom: 0; font-size: 0.8rem; color: var(--vp-c-text-3); }

@media (max-width: 640px) {
  .arrow { transform: rotate(90deg); width: 100%; }
  .node { min-width: 0; }
}
</style>
