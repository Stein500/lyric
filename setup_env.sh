#!/usr/bin/env bash
# Reconstruction de l'environnement (règle §4 — work/ non versionné, régénérable)
set -e
cd "$(dirname "$0")"
mkdir -p work
python3 -m venv work/venv
work/venv/bin/pip install --quiet --upgrade pip
work/venv/bin/pip install --quiet imageio-ffmpeg mutagen numpy pillow matplotlib scipy
mkdir -p work/bin
FF=$(work/venv/bin/python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
ln -sf "$FF" work/bin/ffmpeg
echo "OK — $(work/bin/ffmpeg -version | head -1)"
