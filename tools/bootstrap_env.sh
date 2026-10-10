#!/usr/bin/env bash
# Recree l'environnement de rendu hors depot (le sandbox ne persiste pas /home/user/venv
# d'un tour a l'autre). Idempotent, ~10 s.
set -e
VENV=/home/user/venv
if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV"
fi
"$VENV/bin/pip" install --quiet --disable-pip-version-check pillow numpy imageio-ffmpeg
"$VENV/bin/python" - <<'EOF'
import numpy, PIL, imageio_ffmpeg
print("env OK | pillow", PIL.__version__, "| numpy", numpy.__version__)
print("ffmpeg |", imageio_ffmpeg.get_ffmpeg_exe())
EOF
