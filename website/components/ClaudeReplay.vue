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

  // 03 节：和代码库对话，追踪一次请求
  codebase: [
    { kind: 'user', text: '给我一个这个代码库的总览，再追踪一次用户查询从前端到后端的完整流程。' },
    { kind: 'thinking', text: '不逐个翻文件，用 agentic search 自主定位出最相关的几个文件。' },
    { kind: 'tool', tool: 'Search', arg: '入口文件 / API 端点 / RAG 相关', out: '命中 app.py、rag_system.py、search_tools.py …' },
    { kind: 'tool', tool: 'Read', arg: 'frontend/script.js', out: '前端用 fetch 调 /api/query' },
    { kind: 'tool', tool: 'Read', arg: 'rag_system.py', out: 'RAG：向量检索 → 拼上下文 → 调模型' },
    { kind: 'result', text: '流程是：前端发请求 → API 端点 → RAG 系统在 Chroma 向量库检索 → 带上下文调用大模型 → 把回答发回前端。要我画成图吗？' },
  ],

  // 05 节：用 Playwright 让 Claude 自己截图、自改、自验证
  playwright: [
    { kind: 'user', text: '让「新建对话」按钮和下面的链接一样：左对齐、去掉边框。' },
    { kind: 'tool', tool: 'Playwright', arg: '打开浏览器，导航到 localhost:8000', confirm: true, out: '新标签页已打开' },
    { kind: 'tool', tool: 'Playwright', arg: '对当前页面截图', out: '已拿到截图' },
    { kind: 'thinking', text: '看出问题了：按钮有边框和背景色，而且居中，没和下面的链接对齐。' },
    { kind: 'tool', tool: 'Edit', arg: 'frontend/style.css', out: '去掉 border/background，改成左对齐' },
    { kind: 'tool', tool: 'Playwright', arg: '再次截图验证', out: '已拿到截图' },
    { kind: 'result', text: '改完并自查通过：按钮现在左对齐、无边框，和其他链接风格一致。整个截图—分析—修改—再截图的循环，全程我自己跑完，不用你手动截图。' },
  ],

  // 06 节：先写测试，再调试，揪出 MAX_RESULTS=0
  debug: [
    { kind: 'user', text: '应用查询时报错了。先给 AIGenerator、rag_system、search_tools 写测试，跑测试定位问题——别急着猜。多想想。' },
    { kind: 'thinking', text: '像是配置问题，错误可能在某处被吞掉了。先用 pytest 搭测试，把 ChromaDB 打桩。' },
    { kind: 'todo', items: ['用 pytest 建测试目录', 'mock 掉 ChromaDB 依赖', '跑单元测试 + 集成测试'] },
    { kind: 'tool', tool: 'Write', arg: 'tests/test_search_tools.py', out: '含 fixture 与 mock' },
    { kind: 'tool', tool: 'Bash', arg: 'uv run pytest', confirm: true, out: '部分用例失败，指向向量搜索返回 0 条' },
    { kind: 'tool', tool: 'Read', arg: 'config.py', out: '发现 MAX_RESULTS = 0 ！' },
    { kind: 'tool', tool: 'Edit', arg: 'config.py', out: 'MAX_RESULTS = 0 → 5' },
    { kind: 'tool', tool: 'Bash', arg: 'uv run pytest', out: '全部通过 ✓' },
    { kind: 'result', text: '真凶是 MAX_RESULTS 被设成了 0，向量检索一条都不返回。已修复，并留下一套能持续跑的测试基础设施——以后再坏，立刻就知道为什么。' },
  ],

  // 09 节：重构 notebook，拆分关注点
  notebook: [
    { kind: 'user', text: '重构这个 notebook：拆出「加载数据」「计算指标」两个 Python 模块，改进可视化，并写个 README 说明怎么用。' },
    { kind: 'tool', tool: 'Notebook', arg: '读取 analysis.ipynb 的各单元格', out: '已分析结构与数据流' },
    { kind: 'tool', tool: 'Write', arg: 'data_loader.py', out: '负责读取与清洗 CSV' },
    { kind: 'tool', tool: 'Write', arg: 'metrics.py', out: '负责计算营收、平均订单价值等业务指标' },
    { kind: 'tool', tool: 'Notebook', arg: '重写 analysis.ipynb', out: '改用模块，业务逻辑与展示分离' },
    { kind: 'result', text: '重构完成：notebook 现在只管「展示」，脏活交给两个模块；可视化更清爽，还配了 README。下一步可以一键变成 Streamlit 仪表盘。' },
  ],

  // 10 节：Figma 稿 → Next.js 应用 → 接真实数据
  figma: [
    { kind: 'user', text: '用这张 Figma 设计稿构建 Next.js 仪表盘，图表用 recharts，再用 Playwright 看看效果。' },
    { kind: 'tool', tool: 'Figma', arg: 'Get Image · 取设计稿预览', confirm: true, out: '已拿到设计稿截图' },
    { kind: 'tool', tool: 'Figma', arg: 'Get Code · 取设计稿背后的代码', out: '已拿到布局与样式信息' },
    { kind: 'tool', tool: 'Bash', arg: 'npm install recharts', out: '依赖已安装' },
    { kind: 'tool', tool: 'Write', arg: 'app/dashboard/page.tsx', out: '按组件化结构搭出仪表盘' },
    { kind: 'tool', tool: 'Playwright', arg: '导航到 localhost:3000 并截图', out: '与设计稿高度吻合' },
    { kind: 'result', text: '设计稿已变成可运行的 Next.js 页面。' },
    { kind: 'user', text: '再用美联储经济数据（FRED）的真实数据填充这些图表。' },
    { kind: 'tool', tool: 'Web', arg: '搜索 FRED API 文档与用法', out: '了解如何取 CPI / 失业率 / 国债收益率' },
    { kind: 'result', text: '取真实数据需要一个 API key，请你去 FRED 账号申请一个填进来。' },
    { kind: 'tool', tool: 'Write', arg: 'lib/fred.ts', out: '取数服务 + 代理请求' },
    { kind: 'result', text: '搞定 ✨ 图表里现在是真实的失业率、十年期国债收益率等数据——从「带假数据的设计稿」到「接入真实数据源」，只用了几分钟。' },
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
  Playwright: '#2dd4bf',
  Figma: '#f472b6',
  Notebook: '#fb923c',
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
