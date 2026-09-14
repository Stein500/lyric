#!/usr/bin/env bash
# setup_env.sh — (re)create the local toolchain for the lyric pipeline.
# Idempotent. Requires internet. Versioned (scripts/); bin/ & .venv/ are gitignored.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== 1/4 Python venv =="
if [ ! -d .venv ]; then python3 -m venv .venv; fi
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet numpy scipy pillow fonttools brotli mutagen imageio-ffmpeg

echo "== 2/4 ffmpeg/ffprobe (static) =="
mkdir -p bin
FF=$(.venv/bin/python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
ln -sf "$FF" bin/ffmpeg
ln -sf "$FF" bin/ffprobe   # imageio-ffmpeg ships ffmpeg only; alias for convenience
chmod +x bin/ffmpeg

echo "== 3/4 fonts =="
mkdir -p assets/fonts
# DejaVu Sans Bold is usually present; ensure it is copied if found
for f in /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf; do
  [ -f "$f" ] && cp -f "$f" assets/fonts/ 2>/dev/null || true
done

echo "== 4/4 dirs =="
mkdir -p work assets/raw/portrait assets/raw/landscape livrables

echo "DONE. ffmpeg: $(bin/ffmpeg -version 2>/dev/null | head -1)"
