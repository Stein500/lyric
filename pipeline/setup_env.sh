#!/usr/bin/env bash
# Reconstruit le venv + dépendances Python + fontes DejaVu.
# Usage depuis la racine du repo :  bash pipeline/setup_env.sh
set -e
cd "$(dirname "$0")/.."

python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install mutagen pillow numpy imageio-ffmpeg matplotlib

# Copier les fontes DejaVu (embarquées dans matplotlib) vers assets/fonts si absentes
MPL_FONTS="$(python3 -c 'import matplotlib,os;print(os.path.join(os.path.dirname(matplotlib.__file__),"mpl-data","fonts","ttf"))')"
mkdir -p assets/fonts
for f in DejaVuSans-Bold.ttf DejaVuSans.ttf; do
  [ -f "assets/fonts/$f" ] || cp "$MPL_FONTS/$f" assets/fonts/ 2>/dev/null || true
done

echo "OK — venv prêt. ffmpeg :"
python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"
