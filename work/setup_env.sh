#!/usr/bin/env bash
# Reconstruction de l'environnement de production (PROMPT_UNIVERSEL v4.8.2 §4)
set -e
cd "$(dirname "$0")/.."
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install imageio-ffmpeg mutagen numpy pillow matplotlib
echo "OK — ffmpeg: $(.venv/bin/python -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())')"
