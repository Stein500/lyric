#!/system/bin/sh
# §D.11 — reconstruction environnement (sandbox reset / Termux)
cd "$(dirname "$0")/.." || exit 1
python3 -m venv .venv
.venv/bin/pip install --quiet numpy scipy pillow mutagen imageio-ffmpeg brotli fonttools
.venv/bin/python - <<'EOF'
import imageio_ffmpeg, os
os.makedirs("work", exist_ok=True)
os.symlink(imageio_ffmpeg.get_ffmpeg_exe(), "work/ffmpeg") if not os.path.exists("work/ffmpeg") else None
print("ENV READY")
EOF
