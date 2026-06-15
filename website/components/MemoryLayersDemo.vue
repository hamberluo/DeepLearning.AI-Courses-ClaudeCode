<script setup>
import { ref } from 'vue'

const layers = [
  {
    id: 'project',
    name: '项目级记忆',
    file: 'CLAUDE.md',
    where: '放在项目里（可在子目录嵌套多个）',
    git: '提交进 git，全团队共享',
    gitOk: true,
    example: '本项目用 UV 管理依赖；测试用 pytest。',
    tip: '`/init` 生成的就是这种。适合放「所有协作者都该遵守」的规则。',
  },
  {
    id: 'local',
    name: '本地级记忆',
    file: 'CLAUDE.local.md',
    where: '放在项目里，但只属于你',
    git: '被 git 忽略，不与别人共享',
    gitOk: false,
    example: '不要用 ./run.sh 启动服务器，我自己手动跑。',
    tip: '适合放「只对你这台机器/你的习惯有用」的个人偏好。',
  },
  {
    id: 'user',
    name: '用户级记忆',
    file: '~/.claude/CLAUDE.md',
    where: '放在你主目录的 .claude 文件夹',
    git: '只在你本机，跨全部项目生效',
    gitOk: false,
    example: '回答尽量简洁；提交信息一律用英文。',
    tip: '适合放「你所有 Claude Code 项目都通用」的全局习惯。',
  },
]

const active = ref('project')
</script>

<template>
  <div class="mem">
    <p class="lead">同样是「记忆」，写进哪一层，决定了它<strong>影响谁</strong>、<strong>要不要进 git</strong>。点下面三张卡片看区别：</p>
    <div class="tabs">
      <button
        v-for="l in layers"
        :key="l.id"
        :class="{ on: active === l.id }"
        @click="active = l.id"
      >{{ l.name }}</button>
    </div>

    <div v-for="l in layers" :key="l.id" v-show="active === l.id" class="panel">
      <div class="head">
        <code class="file">{{ l.file }}</code>
        <span class="git" :class="{ ok: l.gitOk }">{{ l.gitOk ? '✓ 进 git · 团队共享' : '✗ 不进 git / 仅本机' }}</span>
      </div>
      <div class="rows">
        <div class="row"><span class="k">放在哪</span><span class="v">{{ l.where }}</span></div>
        <div class="row"><span class="k">作用范围</span><span class="v">{{ l.git }}</span></div>
        <div class="row"><span class="k">写法举例</span><span class="v ex">“{{ l.example }}”</span></div>
      </div>
      <p class="tip">💡 {{ l.tip }}</p>
    </div>
  </div>
</template>

<style scoped>
.mem { border: 1px solid var(--vp-c-divider); border-radius: 12px; padding: 1.2rem; margin: 1.5rem 0; background: var(--vp-c-bg-soft); }
.lead { margin: 0 0 0.9rem; font-size: 0.9rem; color: var(--vp-c-text-2); }
.tabs { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem; }
.tabs button {
  padding: 0.4rem 0.95rem; border-radius: 8px; cursor: pointer;
  border: 1px solid var(--vp-c-divider); background: var(--vp-c-bg);
  color: var(--vp-c-text-2); font-size: 0.85rem; transition: all 0.2s;
}
.tabs button.on { border-color: var(--vp-c-brand-1); background: var(--vp-c-brand-soft); color: var(--vp-c-brand-1); font-weight: 700; }
.panel { animation: fade 0.3s ease; }
@keyframes fade { from { opacity: 0; } to { opacity: 1; } }
.head { display: flex; align-items: center; gap: 0.8rem; flex-wrap: wrap; margin-bottom: 0.8rem; }
.file { font-size: 0.95rem; background: var(--vp-c-bg); padding: 0.25rem 0.6rem; border-radius: 6px; color: var(--vp-c-brand-1); font-weight: 700; }
.git { font-size: 0.78rem; color: #ef4444; }
.git.ok { color: #22c55e; }
.rows { display: flex; flex-direction: column; gap: 0.5rem; }
.row { display: flex; gap: 0.8rem; padding: 0.5rem 0.7rem; border: 1px solid var(--vp-c-divider); border-radius: 8px; background: var(--vp-c-bg); }
.row .k { flex-shrink: 0; width: 5em; color: var(--vp-c-text-3); font-size: 0.85rem; }
.row .v { color: var(--vp-c-text-1); font-size: 0.88rem; }
.row .v.ex { font-style: italic; color: var(--vp-c-text-2); }
.tip { margin: 0.9rem 0 0; font-size: 0.85rem; color: var(--vp-c-text-2); }
</style>
