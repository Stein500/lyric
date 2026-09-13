#!/usr/bin/env bash
# Reconstruction environnement lyric (v4.9 §4) — venv + deps + ffmpeg symlink
set -e
cd "$(dirname "$0")/.."
python3 -m venv .venv
.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q imageio-ffmpeg mutagen numpy pillow matplotlib fonttools brotli
FF=$(.venv/bin/python -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())')
mkdir -p work
ln -sf "$FF" work/ffmpeg
echo "ENV OK: $FF"
