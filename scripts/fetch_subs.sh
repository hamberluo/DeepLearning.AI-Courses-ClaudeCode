#!/usr/bin/env bash
#
# 抓取 DeepLearning.AI《Claude Code》课程的英文人工字幕（en-GB）。
#
# 依赖：yt-dlp
# 用法：bash scripts/fetch_subs.sh
#
# 说明：
#   - 只下字幕，不下视频（--skip-download）。
#   - 统一转成 .srt。
#   - 源 playlist（Ted Tyler 搬运）有两处缺陷，见 docs 设计文档 §3.1：
#       * 「Jupyter Notebook」正课在 YouTube 缺失 → 需从 DLAI 课程页另取（本脚本不覆盖）。
#       * 第 11 个「Conclusion」视频字幕错误重复 → 抓取后已手动清理。
#   - 因此本脚本抓取的是“原始”字幕，命名/清理另见 data/subtitles 现有成品。

set -euo pipefail

PLAYLIST="https://www.youtube.com/playlist?list=PLM3BowDjMUhai9fgX3JK_ZiMt8BotHZaH"
OUT_DIR="$(cd "$(dirname "$0")/.." && pwd)/data/subtitles/_raw"

mkdir -p "$OUT_DIR"

yt-dlp \
  --write-subs \
  --sub-langs en-GB \
  --skip-download \
  --convert-subs srt \
  -o "$OUT_DIR/%(playlist_index)02d-%(title)s.%(ext)s" \
  "$PLAYLIST"

echo "完成。原始字幕在：$OUT_DIR"
echo "注意：Jupyter 节需从 DeepLearning.AI 课程页(lesson 33kzr)单独抓取文字稿。"
