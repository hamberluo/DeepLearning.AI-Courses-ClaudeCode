#!/usr/bin/env python3
"""读 website/guide/*.md，清洗成朗读文本，用 edge-tts 生成 mp3 到 website/public/audio/。

用法：
  python3 tools/build-listen-audio.py                       # 生成全部
  python3 tools/build-listen-audio.py 02-what-is-claude-code # 只生成指定篇

依赖：edge-tts（见 tools/requirements.txt）。
声线：zh-CN-XiaoxiaoNeural，语速 +50%（≈1.5 倍速）。
"""
import asyncio
import re
import sys
from pathlib import Path

import edge_tts

WEB = Path(__file__).resolve().parent.parent
GUIDE = WEB / "guide"
OUT = WEB / "public" / "audio"
OUT.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "+50%"

SLUGS = [
    "01-introduction",
    "02-what-is-claude-code",
    "03-setup-and-codebase-understanding",
    "04-adding-features-1",
    "05-adding-features-2",
    "06-testing-debugging-refactoring",
    "07-adding-multiple-features",
    "08-github-integration-and-hooks",
    "09-refactoring-jupyter-notebook",
    "10-creating-web-app-figma",
    "11-conclusion",
]

# 朗读读法修正（只影响语音，不改正文）。长词在前，避免子串误伤。
TERM_READ = [
    # 多音字：「行」指「一行/换行」时应读 háng（银行的行），用同音字「航」纠正。
    # 仅纠正“行=行列”的词，运行/执行/进行/行业等 xíng 读法不受影响。
    ("命令行", "命令航"),
    ("换行", "换航"),
    ("一行", "一航"),
    ("每行", "每航"),
    ("逐行", "逐航"),
    ("多行", "多航"),
    ("单行", "单航"),
    ("整行", "整航"),
    ("几行", "几航"),
    ("行号", "航号"),
    ("行数", "航数"),
    # 年份逐位读（2023→二零二三），避免被读成「两千零二十三」。端口号等不在此列。
    ("2020", "二零二零"),
    ("2021", "二零二一"),
    ("2022", "二零二二"),
    ("2023", "二零二三"),
    ("2024", "二零二四"),
    ("2025", "二零二五"),
    ("2026", "二零二六"),
    ("v2.0.70", "2.0.70 版本"),
    ("CLAUDE.local.md", "Claude 本地配置文件"),
    ("CLAUDE.md", "Claude 配置文件"),
    ("settings.local.json", "本地设置文件"),
    ("MAX_RESULTS", "MAX RESULTS"),
    ("$ARGUMENTS", "ARGUMENTS 变量"),
    ("ai_generator.py", "AI generator 文件"),
    ("rag_system.py", "RAG system 文件"),
    ("search_tools.py", "search tools 文件"),
    ("search_tools", "search tools"),
    ("pyproject.toml", "pyproject 配置文件"),
    ("data_loader.py", "data loader 文件"),
    ("metrics.py", "metrics 文件"),
    ("dashboard.py", "dashboard 文件"),
    ("convert-to-dashboard.md", "convert to dashboard 文件"),
    ("backend-tool-refactor.md", "后端重构说明文件"),
    ("frontend-changes.md", "frontend changes 文件"),
    ("implement-feature.md", "implement feature 文件"),
    ("requirements.txt", "requirements 文件"),
    ("run.sh", "run 脚本"),
    ("localhost:3000", "本地 3000 端口"),
    ("localhost:8000", "本地 8000 端口"),
    ("Next.js", "Next JS"),
    ("D3.js", "D3 JS"),
]


def clean(md):
    # 去掉 front matter
    md = re.sub(r"^---\n.*?\n---\n", "", md, count=1, flags=re.DOTALL)
    # 代码块整体换成提示语
    md = re.sub(r"```.*?```", "\n（这里有一段代码，详见网页。）\n", md, flags=re.DOTALL)

    out = []
    skip_block = False  # 处在 ::: info 块里
    for line in md.splitlines():
        s = line.rstrip()

        # 容器块：info 块整段跳过（只是元信息），其它容器仅去掉标记行
        m = re.match(r"^\s*:::\s*(\w+)?", s)
        if m:
            kind = (m.group(1) or "").lower()
            if kind == "info":
                skip_block = True
            elif kind == "":  # 容器结束 :::
                skip_block = False
            # tip / warning 等：丢标记行、保留内容
            continue
        if skip_block:
            continue

        if not s.strip():
            out.append("")
            continue

        # AudioPlayer 控件整行删除（别念出文件名）
        if re.match(r"^\s*<AudioPlayer\b", s):
            continue
        # 其它交互演示组件 → 转成提示语
        if re.match(r"^\s*<[A-Z][A-Za-z]+\b[^>]*/?>", s):
            out.append("这里有一个交互演示，可以在网页上动手试试。")
            continue
        # markdown 表格行跳过
        if re.match(r"^\s*\|.*\|\s*$", s):
            continue

        s = re.sub(r"^#{1,6}\s*", "", s)          # 标题井号
        s = re.sub(r"^\s*[-*]\s+", "", s)          # 列表符
        s = re.sub(r"^\s*>\s?", "", s)             # 引用符
        s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)   # 加粗
        s = re.sub(r"`([^`]+)`", r"\1", s)         # 行内代码
        s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)  # 链接
        out.append(s)

    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    for en, zh in TERM_READ:
        text = text.replace(en, zh)
    text = normalize_symbols(text)
    return text.strip()


def normalize_symbols(text):
    """把朗读会读错的符号换成自然停顿或读法。斜杠命令（/init 等）保留不动。"""
    text = re.sub(r"—+", "，", text)                    # 破折号 → 停顿（别读成「破折号」）
    text = re.sub(r"\s*→\s*", "，", text)               # 流程箭头 → 停顿
    text = re.sub(r"\s+/\s+", "、", text)               # 带空格的斜杠分隔（项目级 / 本地级）
    text = re.sub(r"(?<=[\u4e00-\u9fa5])/(?=[\u4e00-\u9fa5])", "、", text)  # 中文间斜杠（深色/浅色）
    text = re.sub(r"@(?![A-Za-z])", " at 符号 ", text)   # @ 引用（命令里的 @latest 等保留）
    text = re.sub(r"\s#\s", " 井号 ", text)              # 独立的 #（# 内容）
    text = text.replace("×2", " 两次").replace("×", " 乘 ")
    text = text.replace("+", " 加 ")                    # Shift+Tab、A + B
    text = text.replace("\\", "")                       # 残留反斜杠（后文已有「反斜杠」说明）
    text = text.replace("_", " ")                       # 下划线读成空格（ui_feature 等）
    text = re.sub(r"，{2,}", "，", text)                 # 合并重复停顿
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text


async def synth(slug):
    src = GUIDE / f"{slug}.md"
    if not src.exists():
        print(f"[{slug}] 找不到 {src}，跳过")
        return
    text = clean(src.read_text(encoding="utf-8"))
    if not text:
        print(f"[{slug}] 清洗后为空，跳过")
        return
    comm = edge_tts.Communicate(text, VOICE, rate=RATE)
    await comm.save(str(OUT / f"{slug}.mp3"))
    kb = (OUT / f"{slug}.mp3").stat().st_size // 1024
    print(f"[{slug}] 生成 {kb} KB")


async def main(slugs):
    for slug in slugs:
        await synth(slug)


if __name__ == "__main__":
    targets = sys.argv[1:] or SLUGS
    asyncio.run(main(targets))
