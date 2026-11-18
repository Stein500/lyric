#!/usr/bin/env bash
# =============================================================================
#  pipeline.sh — de l'audio maître au clip livré, en une commande
#  Annexe exécutable du PROMPT UNIVERSEL GOSPEL v8.0
#
#  Usage :
#    ./scripts/pipeline.sh                    # tout, avec les valeurs par défaut
#    ./scripts/pipeline.sh --segments 40      # découpe en 40 segments
#    ./scripts/pipeline.sh --skip-leger       # ne pas faire la version < 95 Mo
#    ./scripts/pipeline.sh --only bases       # une seule étape
#    ./scripts/pipeline.sh --help
#
#  Étapes : deps · measure · normalize · bases · segments · assemble · check
#           leger · teaser · covers · hashes
# =============================================================================
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

# ---------------------------------------------------------------- paramètres
AUDIO_RAW="${AUDIO_RAW:-data/master_mesias_audio_only.mp3}"
AUDIO_NORM="${AUDIO_NORM:-livrables/Averly Morillo - MESIAS (master normalise -14LUFS).mp3}"
CLIP_MASTER="${CLIP_MASTER:-livrables/Averly Morillo - MESIAS (clip lyrics 1080x1920).mp4}"
CLIP_LEGER="${CLIP_LEGER:-livrables/MESIAS_clip_1080x1920_leger.mp4}"
TEASER_START="${TEASER_START:-464.13}"
SEGMENTS="${SEGMENTS:-40}"
CRF="${CRF:-21}"
TAIL="${TAIL:-5.00}"
DUR=""
SIL=""
ONLY=""
SKIP_LEGER=0
SKIP_TEASER=0

while [ $# -gt 0 ]; do
  case "$1" in
    --audio-raw)   AUDIO_RAW="$2"; shift 2 ;;
    --audio)       AUDIO_NORM="$2"; shift 2 ;;
    --dur)         DUR="$2"; shift 2 ;;
    --silence)     SIL="$2"; shift 2 ;;
    --tail)        TAIL="$2"; shift 2 ;;
    --segments)    SEGMENTS="$2"; shift 2 ;;
    --crf)         CRF="$2"; shift 2 ;;
    --teaser-start) TEASER_START="$2"; shift 2 ;;
    --only)        ONLY="$2"; shift 2 ;;
    --skip-leger)  SKIP_LEGER=1; shift ;;
    --skip-teaser) SKIP_TEASER=1; shift ;;
    -h|--help)     sed -n '3,16p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "option inconnue : $1"; exit 1 ;;
  esac
done

# ---------------------------------------------------------------- utilitaires
c_ok()   { printf '\033[32m✓\033[0m %s\n' "$*"; }
c_run()  { printf '\n\033[1m▶ %s\033[0m\n' "$*"; }
c_warn() { printf '\033[33m!\033[0m %s\n' "$*"; }
die()    { printf '\033[31m✗ %s\033[0m\n' "$*"; exit 1; }

step() { [ -z "$ONLY" ] || [ "$ONLY" = "$1" ]; }

FF=""
need_ff() {
  if [ -z "$FF" ]; then
    FF="$(python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())' 2>/dev/null)" \
      || die "imageio-ffmpeg absent : lance l'étape deps"
  fi
}

# =============================================================================
# 1. DÉPENDANCES
# =============================================================================
if step deps; then
  c_run "1/11  dépendances"
  python3 -m pip install --break-system-packages -q \
    pillow imageio-ffmpeg numpy mutagen 2>&1 | tail -2
  python3 -c "import PIL, imageio_ffmpeg, numpy, mutagen" \
    || die "installation incomplète"
  mkdir -p data assets/fonts scripts livrables work/base work/check
  need_ff
  c_ok "python + ffmpeg embarqué ($($FF -version 2>/dev/null | head -1 | cut -c1-30))"
fi

# =============================================================================
# 2. MESURES AUDIO  (la durée décodée, pas la durée annoncée)
# =============================================================================
if step measure; then
  c_run "2/11  mesures de l'audio"
  [ -f "$AUDIO_NORM" ] || die "audio normalisé introuvable : $AUDIO_NORM"
  need_ff

  if [ -z "$DUR" ]; then
    DUR=$($FF -hide_banner -nostats -i "$AUDIO_NORM" -f null - 2>&1 \
          | grep -oE 'time=[0-9:.]+' | tail -1 | cut -d= -f2 \
          | awk -F: '{printf "%.3f", $1*3600+$2*60+$3}')
    [ -n "$DUR" ] || die "durée illisible"
  fi

  if [ -z "$SIL" ]; then
    SIL=$($FF -hide_banner -nostats -i "$AUDIO_NORM" \
          -af "silencedetect=n=-40dB:d=1.5" -f null - 2>&1 \
          | grep -oE 'silence_start: [0-9.]+' | tail -1 | awk '{print $2}')
    if [ -z "$SIL" ]; then
      SIL=$(python3 -c "print(round(float('$DUR') - 5.356, 3))")
      c_warn "aucun silence franc détecté : silence final estimé à $SIL s"
    fi
  fi

  TOTAL=$(python3 -c "print(round(float('$DUR') + float('$TAIL'), 3))")
  FRAMES=$(python3 -c "print(round(float('$TOTAL') * 30))")
  c_ok "durée décodée  $DUR s"
  c_ok "silence final  $SIL s"
  SEGFR=$(python3 -c "print(round($TOTAL*30/$SEGMENTS))")
  c_ok "total clip     $TOTAL s ($FRAMES frames à 30 i/s)"
  c_ok "par segment    $SEGFR frames ($SEGMENTS segments)"

  $FF -hide_banner -nostats -i "$AUDIO_NORM" -filter_complex ebur128=peak=true \
    -f null - 2>&1 | tail -16 | grep -E "^ +(I|Peak|LRA):" | sed 's/^/    /'
fi

# =============================================================================
# 3. NORMALISATION  (2 passes) — seulement si le fichier normalisé n'existe pas
# =============================================================================
if step normalize; then
  c_run "3/11  normalisation"
  if [ -f "$AUDIO_NORM" ]; then
    c_ok "déjà présent : $AUDIO_NORM (on ne réencode pas)"
  else
    [ -f "$AUDIO_RAW" ] || die "audio brut introuvable : $AUDIO_RAW"
    need_ff
    c_warn "mesure de la 1re passe…"
    M=$($FF -hide_banner -nostats -i "$AUDIO_RAW" \
        -af "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json" -f null - 2>&1 \
        | sed -n '/^{/,/^}/p')
    I=$(echo "$M"  | grep input_i       | grep -oE '\-?[0-9.]+')
    TP=$(echo "$M" | grep input_tp      | grep -oE '\-?[0-9.]+')
    LR=$(echo "$M" | grep input_lra     | grep -oE '\-?[0-9.]+')
    TH=$(echo "$M" | grep input_thresh  | grep -oE '\-?[0-9.]+')
    OF=$(echo "$M" | grep target_offset | grep -oE '\-?[0-9.]+')
    c_ok "entrée : I=$I TP=$TP LRA=$LR"
    mkdir -p livrables
    $FF -y -hide_banner -loglevel error -i "$AUDIO_RAW" \
      -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$I:measured_TP=$TP:measured_LRA=$LR:measured_thresh=$TH:offset=$OF:linear=true:print_format=summary" \
      -ar 48000 -ac 2 -c:a libmp3lame -b:a 320k -map_metadata -1 "$AUDIO_NORM" \
      || die "normalisation échouée"
    c_ok "écrit : $AUDIO_NORM"
  fi
fi

# =============================================================================
# 4. BASES 1080x1920  (toujours en PNG)
# =============================================================================
if step bases; then
  c_run "4/11  bases 1080x1920"
  python3 - <<'EOF' || die "construction des bases échouée"
import sys, os, glob
sys.path.insert(0, "scripts")
import render as R
os.makedirs("work/base", exist_ok=True)
n = 0
for f in sorted(glob.glob("assets/*.png")):
    out = os.path.join("work/base", os.path.basename(f))
    if not os.path.exists(out):
        R.base_image(f).save(out)
        n += 1
print(f"  {n} base(s) créée(s) · total {len(os.listdir('work/base'))}")
EOF
  c_ok "work/base prêt"
fi

# =============================================================================
# 5. SEGMENTS  (le gros du temps : 30 à 45 s par segment)
# =============================================================================
if step segments; then
  c_run "5/11  rendu des $SEGMENTS segments"
  # la durée ne se DEVINE pas : elle se mesure. Sans elle, le nombre de frames est
  # faux (constaté : +25 frames par segment sur un test réel) et le clip est décalé.
  if [ -z "$DUR" ] || [ -z "$SIL" ]; then
    c_warn "durée manquante : mesure automatique avant de rendre"
    need_ff
    DUR=$($FF -hide_banner -nostats -i "$AUDIO_NORM" -f null - 2>&1 \
          | grep -oE 'time=[0-9:.]+' | tail -1 | cut -d= -f2 \
          | awk -F: '{printf "%.3f", $1*3600+$2*60+$3}')
    [ -n "$DUR" ] || die "impossible de mesurer $AUDIO_NORM"
    if [ -z "$SIL" ]; then
      SIL=$($FF -hide_banner -nostats -i "$AUDIO_NORM" \
            -af "silencedetect=n=-40dB:d=1.5" -f null - 2>&1 \
            | grep -oE 'silence_start: [0-9.]+' | tail -1 | awk '{print $2}')
      [ -n "$SIL" ] || SIL=$(python3 -c "print(round(float('$DUR')-5.356,3))")
    fi
    c_ok "mesuré : durée $DUR s · silence $SIL s"
  fi
  rm -f work/clip_seg*.mp4
  FAIL=0
  for i in $(seq 0 $((SEGMENTS - 1))); do
    printf '  segment %2d/%d … ' "$((i + 1))" "$SEGMENTS"
    if python3 scripts/render_clip.py --seg "$i" "$SEGMENTS" --crf "$CRF" \
        --dur-audio "$DUR" --silence "$SIL" --tail "$TAIL" \
        --audio "$AUDIO_NORM" --out "work/clip_seg$i.mp4" >/tmp/seg$i.log 2>&1; then
      grep -oE 'seg[0-9]+ [0-9]+ frames' /tmp/seg$i.log | tail -1 | sed 's/^/ /' || echo " ok"
    else
      echo "ÉCHEC (voir /tmp/seg$i.log)"; FAIL=$((FAIL + 1))
    fi
  done
  N=$(ls work/clip_seg*.mp4 2>/dev/null | wc -l)
  [ "$N" -eq "$SEGMENTS" ] && c_ok "$N segments rendus" || die "$N/$SEGMENTS segments seulement"
fi

# =============================================================================
# 6. ASSEMBLAGE  (+ audio, apad pour la carte finale)
# =============================================================================
if step assemble; then
  c_run "6/11  assemblage"
  if [ -z "$DUR" ]; then
    need_ff
    DUR=$($FF -hide_banner -nostats -i "$AUDIO_NORM" -f null - 2>&1 \
          | grep -oE 'time=[0-9:.]+' | tail -1 | cut -d= -f2 \
          | awk -F: '{printf "%.3f", $1*3600+$2*60+$3}')
    [ -n "$DUR" ] || die "durée inconnue : lance l'étape measure"
  fi
  [ -n "$SIL" ] || SIL=$(python3 -c "print(round(float('$DUR')-5.356,3))")
  python3 scripts/render_clip.py --assemble \
    --dur-audio "$DUR" --silence "$SIL" --tail "$TAIL" \
    --audio "$AUDIO_NORM" || die "assemblage échoué"
  c_ok "$CLIP_MASTER"
fi

# =============================================================================
# 7. CONTRÔLES CHIFFRÉS  (sur le fichier assemblé)
# =============================================================================
if step check; then
  c_run "7/11  contrôles chiffrés"
  TOTAL=$(python3 -c "print(round(float('${DUR:?}') + float('$TAIL'), 3))")
  python3 scripts/checks.py "$CLIP_MASTER" --expect "$TOTAL" \
    --json work/check/clip_checks.json | tail -18
fi

# =============================================================================
# 8. VERSION PUBLIABLE  (< 95 Mo, calibrée, pas devinée)
# =============================================================================
if step leger && [ "$SKIP_LEGER" -eq 0 ]; then
  c_run "8/11  version publiable"
  need_ff
  if [ -f "$CLIP_LEGER" ]; then
    SZ=$(stat -c%s "$CLIP_LEGER" 2>/dev/null || echo 0)
    c_ok "déjà présent : $CLIP_LEGER ($(python3 -c "print(round($SZ/1048576,1))") Mo)"
  else
    # calibration sur 120 s avant d'encoder 12 minutes
    $FF -y -hide_banner -loglevel error -ss 300 -t 120 -i "$CLIP_MASTER" \
      -c:v libx264 -preset slow -crf 31 -maxrate 1150k -bufsize 2300k \
      -pix_fmt yuv420p -an /tmp/calib.mp4
    python3 - <<EOF
import os
s = os.path.getsize("/tmp/calib.mp4")
print(f"  calibration : extrait 120 s = {s/1048576:.1f} Mo -> {s*float('$DUR')/120/1048576:.0f} Mo estimés")
EOF
    $FF -y -hide_banner -loglevel error -i "$CLIP_MASTER" \
      -c:v libx264 -preset slow -crf 31 -maxrate 1150k -bufsize 2300k \
      -pix_fmt yuv420p -x264-params keyint=60:min-keyint=30 \
      -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
      -c:a aac -b:a 128k -ar 48000 -movflags +faststart "$CLIP_LEGER" \
      || die "encodage allégé échoué"
    SZ=$(stat -c%s "$CLIP_LEGER")
    [ "$SZ" -lt 100000000 ] \
      && c_ok "$CLIP_LEGER ($(python3 -c "print(round($SZ/1048576,1))") Mo)" \
      || c_warn "encore trop lourd ($(python3 -c "print(round($SZ/1048576,1))") Mo) : baisser maxrate"
  fi
fi

# =============================================================================
# 9. TEASER 15 s
# =============================================================================
if step teaser && [ "$SKIP_TEASER" -eq 0 ]; then
  c_run "9/11  teaser 15 s"
  python3 scripts/render_clip.py --teaser --teaser-start "$TEASER_START" --crf "$CRF" \
    || die "teaser échoué"
  c_ok "teaser rendu (450 frames attendues)"
fi

# =============================================================================
# 10. COUVERTURES
# =============================================================================
if step covers; then
  c_run "10/11  couvertures"
  python3 scripts/make_cover.py || die "couvertures échouées"
  c_ok "3 couvertures 1080x1920"
fi

# =============================================================================
# 11. EMPREINTES
# =============================================================================
if step hashes; then
  c_run "11/11  empreintes"
  cd livrables || die "livrables/ absent"
  ls -1 | grep -v '^SHA256SUMS' | grep -v 'clip lyrics' > /tmp/hashlist.txt
  xargs -a /tmp/hashlist.txt -d '\n' sha256sum > SHA256SUMS.txt
  sha256sum -c SHA256SUMS.txt | sed 's/^/  /'
  cd "$ROOT"
  c_ok "SHA256SUMS.txt écrit et vérifié"
fi

printf '\n\033[1m TERMINÉ\033[0m — durées : audio %s s · clip %s s\n' "$DUR" \
  "$(python3 -c "print(round(float('${DUR:-0}') + float('$TAIL'), 3))" 2>/dev/null)"
