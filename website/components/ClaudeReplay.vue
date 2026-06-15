<script setup>
import { ref, computed, onUnmounted } from 'vue'

const props = defineProps({
  scene: { type: String, default: '' },
  title: { type: String, default: 'claude code' },
})

// 各节课的会话脚本，集中在此维护。
// step.kind: user | thinking | todo | tool | result
const scenes = {
  // 02 节：一句话做个可视化
  visualization: [
    { kind: 'user', text: '给我做个炫酷的可视化' },
    {
      kind: 'thinking',
      text: '用户没指定技术栈。做一个浏览器里就能跑的粒子动画最直观，用纯 HTML + Canvas，无需依赖。',
    },
    {
      kind: 'todo',
      items: [
        '创建 index.html 画布页面',
        '写粒子动画逻辑',
        '加上开关动画 / 清空的交互按钮',
      ],
    },
    { kind: 'tool', tool: 'Write', arg: 'index.html', out: '已创建（含 <canvas> 与控制按钮）' },
    { kind: 'tool', tool: 'Write', arg: 'particles.js', out: '已创建（粒子生成 + 逐帧绘制）' },
    {
      kind: 'result',
      text: '做好了一个粒子动画可视化：上百个彩色粒子在画布上漂浮、连线。要我在浏览器里打开看看吗？',
    },
    { kind: 'tool', tool: 'Bash', arg: 'open index.html', confirm: true, out: '已在默认浏览器打开' },
    { kind: 'result', text: '可视化已经跑起来了 ✨ 你可以点按钮开关动画、加更多粒子，或者清空重来。' },
  ],
}

const steps = computed(() => scenes[props.scene] ?? [])
const shown = ref(0)
const timer = ref(null)

const done = computed(() => shown.value >= steps.value.length)

function next() {
  if (shown.value < steps.value.length) shown.value++
}
function reset() {
  stop()
  shown.value = 0
}
function stop() {
  if (timer.value) {
    clearInterval(timer.value)
    timer.value = null
  }
}
function toggleAuto() {
  if (timer.value) {
    stop()
    return
  }
  if (done.value) shown.value = 0
  timer.value = setInterval(() => {
    if (done.value) {
      stop()
      return
    }
    next()
  }, 1100)
}

onUnmounted(stop)

const toolColors = {
  Read: '#5eb0ef',
  Write: '#22c55e',
  Edit: '#eab308',
  Bash: '#a78bfa',
  Search: '#f472b6',
  Web: '#2dd4bf',
}
function toolColor(t) {
  return toolColors[t] ?? 'var(--vp-c-brand-1)'
}
</script>

<template>
  <div class="replay">
    <div class="bar">
      <span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
      <span class="ttl">{{ title }}</span>
      <span class="count">{{ shown }} / {{ steps.length }}</span>
    </div>

    <div class="body">
      <p v-if="shown === 0" class="placeholder">点「下一步」开始这段会话回放 ↓</p>

      <template v-for="(s, i) in steps" :key="i">
        <div v-if="i < shown" class="step" :class="s.kind">
          <!-- 用户输入 -->
          <div v-if="s.kind === 'user'" class="line user">
            <span class="prompt">&gt;</span><span class="txt">{{ s.text }}</span>
          </div>

          <!-- 思考 -->
          <div v-else-if="s.kind === 'thinking'" class="line thinking">
            <span class="tag">✶ 思考</span><span class="txt">{{ s.text }}</span>
          </div>

          <!-- 待办清单 -->
          <div v-else-if="s.kind === 'todo'" class="line todo">
            <div class="tag">⏺ 制定计划</div>
            <ul>
              <li v-for="(it, k) in s.items" :key="k">☐ {{ it }}</li>
            </ul>
          </div>

          <!-- 工具调用 -->
          <div v-else-if="s.kind === 'tool'" class="line tool">
            <div class="callrow">
              <span class="badge" :style="{ background: toolColor(s.tool) }">{{ s.tool }}</span>
              <code class="arg">{{ s.arg }}</code>
              <span v-if="s.confirm" class="confirm">需确认 ✓</span>
            </div>
            <div v-if="s.out" class="out">⎿ {{ s.out }}</div>
          </div>

          <!-- 回答 -->
          <div v-else-if="s.kind === 'result'" class="line result">
            <span class="tag">⏺ Claude</span><span class="txt">{{ s.text }}</span>
          </div>
        </div>
      </template>
    </div>

    <div class="controls">
      <button class="primary" :disabled="done" @click="next">下一步</button>
      <button @click="toggleAuto">{{ timer ? '暂停' : '自动播放' }}</button>
      <button @click="reset">重置</button>
    </div>
  </div>
</template>

<style scoped>
.replay {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  margin: 1.5rem 0;
  overflow: hidden;
  background: var(--vp-c-bg-soft);
  font-size: 0.86rem;
}
.bar {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.55rem 0.9rem;
  background: var(--vp-c-bg-alt);
  border-bottom: 1px solid var(--vp-c-divider);
}
.dot { width: 11px; height: 11px; border-radius: 50%; display: inline-block; }
.dot.r { background: #ff5f56; }
.dot.y { background: #ffbd2e; }
.dot.g { background: #27c93f; }
.ttl { margin-left: 0.5rem; color: var(--vp-c-text-2); font-family: var(--vp-font-family-mono); font-size: 0.8rem; }
.count { margin-left: auto; color: var(--vp-c-text-3); font-size: 0.75rem; font-family: var(--vp-font-family-mono); }

.body { padding: 1rem 1.1rem; min-height: 90px; }
.placeholder { color: var(--vp-c-text-3); margin: 0; font-size: 0.85rem; }

.step { animation: fade 0.35s ease; margin-bottom: 0.7rem; }
.step:last-child { margin-bottom: 0; }
@keyframes fade {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

.line { line-height: 1.7; }
.txt { white-space: pre-wrap; }

.user .prompt { color: var(--vp-c-brand-1); font-weight: 700; margin-right: 0.5rem; font-family: var(--vp-font-family-mono); }
.user .txt { color: var(--vp-c-text-1); font-weight: 600; }

.thinking { color: var(--vp-c-text-3); font-style: italic; }
.thinking .tag { margin-right: 0.5rem; font-style: normal; }

.todo .tag { color: var(--vp-c-text-2); font-weight: 600; margin-bottom: 0.2rem; }
.todo ul { margin: 0.2rem 0 0; padding-left: 1.3rem; }
.todo li { color: var(--vp-c-text-2); list-style: none; }

.tool .callrow { display: flex; align-items: center; gap: 0.55rem; flex-wrap: wrap; }
.badge {
  color: #0d1117; font-weight: 700; font-size: 0.72rem;
  padding: 0.1rem 0.5rem; border-radius: 6px; font-family: var(--vp-font-family-mono);
}
.arg { color: var(--vp-c-text-1); background: var(--vp-c-bg); padding: 0.1rem 0.45rem; border-radius: 5px; }
.confirm { color: #eab308; font-size: 0.75rem; }
.out { color: var(--vp-c-text-3); margin-top: 0.25rem; padding-left: 0.3rem; font-family: var(--vp-font-family-mono); font-size: 0.8rem; }

.result .tag { color: var(--vp-c-brand-1); font-weight: 700; margin-right: 0.5rem; }
.result .txt { color: var(--vp-c-text-1); }

.controls {
  display: flex; gap: 0.55rem; padding: 0.7rem 0.9rem;
  border-top: 1px solid var(--vp-c-divider); background: var(--vp-c-bg-alt);
}
.controls button {
  padding: 0.32rem 0.95rem; border-radius: 8px; cursor: pointer;
  border: 1px solid var(--vp-c-brand-1); background: transparent;
  color: var(--vp-c-brand-1); font-size: 0.82rem; transition: all 0.2s;
}
.controls button:hover:not(:disabled) { background: var(--vp-c-brand-soft); }
.controls button.primary { background: var(--vp-c-brand-1); color: #fff; }
.controls button.primary:hover:not(:disabled) { background: var(--vp-c-brand-2); }
.controls button:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
