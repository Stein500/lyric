#!/bin/bash
# Re-generate ALL platform variants from the master youtube_full_HD.mp4 (which has audio)

set -e
cd /home/user/lyric/production/video

FFMPEG=/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
SRC=youtube_full_HD.mp4

# 16:9 — same as master (just copies)
cp -f $SRC facebook_full.mp4
cp -f $SRC telegram_full.mp4
cp -f $SRC mboazick_full.mp4
echo "✅ 16:9 facebook/telegram/mboazick"

# 9:16 — crop center, with audio
gen_vertical() {
  local out=$1; local start=$2; local dur=$3
  $FFMPEG -y -ss $start -t $dur -i $SRC \
    -vf "crop=ih*9/16:ih,scale=1080:1920" \
    -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
    -c:a aac -b:a 128k \
    "vertical/$out" 2>/dev/null
  size=$(du -h "vertical/$out" | cut -f1)
  echo "  ✅ $out ($size)"
}

# Crops with audio included (re-run from master)
gen_vertical tiktok_short1_viral.mp4     0   50
gen_vertical tiktok_short2_refrain.mp4    94  31
gen_vertical tiktok_short3_finale.mp4     165  30
gen_vertical instagram_reel1_chains.mp4   24   31
gen_vertical instagram_reel2_emotion.mp4  76   35
gen_vertical instagram_reel3_bridge.mp4   144  50
gen_vertical snapchat_ultrashort.mp4      0    30
gen_vertical whatsapp_status.mp4          76.5 30
gen_vertical x_twitter_short.mp4          0    140

echo ""
echo "=== Total processing complete ==="
ls -la vertical/*.mp4 | head -15
ls -la facebook_full.mp4 telegram_full.mp4 mboazick_full.mp4 2>&1
