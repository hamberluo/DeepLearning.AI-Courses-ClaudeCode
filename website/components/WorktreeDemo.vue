<script setup>
import { ref, computed } from 'vue'

const trees = [
  { id: 'ui', name: 'ui_feature', task: '深 / 浅色主题切换', files: ['style.css', 'app.js', 'pyproject.toml'] },
  { id: 'test', name: 'testing_feature', task: '补 FastAPI 端点测试', files: ['tests/test_api.py'] },
  { id: 'quality', name: 'quality_feature', task: '接入 black 等质量工具', files: ['pyproject.toml'] },
]

// 步骤驱动：建树 → 并行开工 → 各自提交 → 合并 → 冲突 → 解决
const steps = [
  { phase: 'create', text: 'git worktree add 在 .trees/ 下建三个隔离的工作目录，各自一个分支。' },
  { phase: 'work', text: '三个 Claude 并行开工，各做各的功能。即使改了同名文件也互不覆盖——因为它们在不同工作树里。' },
  { phase: 'commit', text: '每棵树各自 add + commit，配描述性提交信息，方便合并时一目了然。' },
  { phase: 'merge', text: '回到 main，让 Claude 用 git merge 逐个合并。testing、ui 顺利合入。' },
  { phase: 'conflict', text: '冲突！ui 和 quality 都改过 pyproject.toml。让 Claude 分析冲突、自动解决，再跑测试确认没坏。' },
  { phase: 'done', text: '三个功能全部合入 main，冲突已解决、测试通过。横跨整个技术栈的改动，全程没有覆盖、没有手忙脚乱。' },
]

const cur = ref(0)
const phase = computed(() => steps[cur.value].phase)
const done = computed(() => cur.value >= steps.length - 1)
function next() { if (!done.value) cur.value++ }
function reset() { cur.value = 0 }

function treeState(t) {
  const p = phase.value
  if (p === 'create') return 'idle'
  if (p === 'work') return 'work'
  if (p === 'commit') return 'commit'
  if (p === 'merge') return t.id === 'quality' ? 'work' : 'merged'
  if (p === 'conflict') return t.id === 'quality' ? 'conflict' : 'merged'
  return 'merged'
}
const stateText = { idle: '已创建', work: '开发中…', commit: '已提交', merged: '已合并 ✓', conflict: '冲突，解决中…' }
</script>

<template>
  <div class="wt">
    <div class="main">main 分支</div>
    <div class="trees">
      <div v-for="t in trees" :key="t.id" class="tree" :class="treeState(t)">
        <div class="tname">🌳 {{ t.name }}</div>
        <div class="ttask">{{ t.task }}</div>
        <div class="tfiles">
          <code
            v-for="f in t.files"
            :key="f"
            :class="{ clash: f === 'pyproject.toml' && (phase === 'conflict') }"
          >{{ f }}</code>
        </div>
        <div class="tstate">{{ stateText[treeState(t)] }}</div>
      </div>
    </div>

    <div class="readout"><span class="idx">{{ cur + 1 }}/{{ steps.length }}</span><span class="rt">{{ steps[cur].text }}</span></div>

    <div class="controls">
      <button class="primary" :disabled="done" @click="next">下一步</button>
      <button @click="reset">重置</button>
    </div>
    <p class="hint">教学示意：工作树 = 同一仓库的多份隔离副本，并行干活、最后合并。合并冲突也能交给 Claude 处理。</p>
  </div>
</template>

<style scoped>
.wt { border: 1px solid var(--vp-c-divider); border-radius: 12px; padding: 1.3rem; margin: 1.5rem 0; background: var(--vp-c-bg-soft); }
.main { text-align: center; font-weight: 700; color: var(--vp-c-brand-1); padding: 0.4rem; border: 1px dashed var(--vp-c-brand-1); border-radius: 8px; margin-bottom: 0.9rem; }
.trees { display: flex; gap: 0.7rem; flex-wrap: wrap; }
.tree {
  flex: 1; min-width: 150px; border: 1px solid var(--vp-c-divider); border-radius: 10px;
  padding: 0.8rem; background: var(--vp-c-bg); transition: all 0.35s ease;
}
.tree.work { border-color: var(--vp-c-brand-1); box-shadow: 0 0 0 2px var(--vp-c-brand-soft); }
.tree.commit { border-color: #a78bfa; }
.tree.merged { border-color: #22c55e; opacity: 0.85; }
.tree.conflict { border-color: #ef4444; box-shadow: 0 0 0 2px rgba(239,68,68,0.18); }
.tname { font-weight: 700; color: var(--vp-c-text-1); font-size: 0.9rem; }
.ttask { font-size: 0.78rem; color: var(--vp-c-text-3); margin: 0.25rem 0 0.5rem; }
.tfiles { display: flex; flex-wrap: wrap; gap: 0.3rem; }
.tfiles code { font-size: 0.72rem; background: var(--vp-c-bg-soft); padding: 0.1rem 0.4rem; border-radius: 5px; color: var(--vp-c-text-2); }
.tfiles code.clash { background: rgba(239,68,68,0.18); color: #ef4444; font-weight: 700; }
.tstate { margin-top: 0.6rem; font-size: 0.78rem; color: var(--vp-c-text-2); font-family: var(--vp-font-family-mono); }
.readout { margin-top: 1rem; padding: 0.85rem 1rem; border-radius: 8px; min-height: 3.3em; background: var(--vp-c-bg); border: 1px solid var(--vp-c-divider); display: flex; gap: 0.6rem; align-items: baseline; }
.idx { color: var(--vp-c-brand-1); font-weight: 700; font-family: var(--vp-font-family-mono); flex-shrink: 0; }
.rt { color: var(--vp-c-text-1); line-height: 1.7; }
.controls { display: flex; gap: 0.55rem; margin-top: 1rem; }
.controls button { padding: 0.32rem 0.95rem; border-radius: 8px; cursor: pointer; border: 1px solid var(--vp-c-brand-1); background: transparent; color: var(--vp-c-brand-1); font-size: 0.82rem; transition: all 0.2s; }
.controls button:hover:not(:disabled) { background: var(--vp-c-brand-soft); }
.controls button.primary { background: var(--vp-c-brand-1); color: #fff; }
.controls button:disabled { opacity: 0.4; cursor: not-allowed; }
.hint { margin: 0.8rem 0 0; font-size: 0.8rem; color: var(--vp-c-text-3); }
@media (max-width: 640px) { .tree { min-width: 0; } }
</style>
