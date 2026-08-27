# -*- coding: utf-8 -*-
"""Vérification frame-by-frame de la fin vidéo + sections clés (règle v4.2)."""
import os, sys, subprocess, re
import importlib.util
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = os.path.join(os.environ.get('VENV', '/tmp/vidvenv'),
                  'lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2')
VIDEO = os.path.join(ROOT, 'livrables', 'Motivé_TikTokReels_9x16_v1.mp4')
OUTDIR = os.path.join(ROOT, 'work', 'frames')
os.makedirs(OUTDIR, exist_ok=True)


def grab(seconds, out):
    cmd = [FF, '-y', '-ss', '%.3f' % seconds, '-i', VIDEO, '-frames:v', '1', '-q:v', '2', out]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out


# Sections clés + trame de la fin (de DURATION-30 à la fin, toutes ~2.5s)
DURATION = 158.88
key = [1.0, 15.5, 22.0, 40.0, 55.0, 66.0, 83.0, 90.0, 105.0, 118.0, 126.0, 133.0, 136.0, 145.0, 150.5, 155.0, 158.5]
tail = [t for t in [x * 2.5 for x in range(int((DURATION - 30) / 2.5), int(DURATION / 2.5) + 1)] if 0 <= t <= DURATION]
times = sorted(set(key + tail))

imgs = []
for t in times:
    p = os.path.join(OUTDIR, 'f_%07.2f.png' % t)
    grab(t, p)
    imgs.append((t, p))

# contact sheet
thumb_w, thumb_h = 200, 356
cols = 4
cell_h = thumb_h + 26
cell_w = thumb_w + 16
rows = (len(imgs) + cols - 1) // cols
sheet = Image.new('RGB', (cols * cell_w + 20, rows * cell_h + 20), (5, 6, 10))
d = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
except Exception:
    font = ImageFont.load_default()
for i, (t, p) in enumerate(imgs):
    im = Image.open(p).resize((thumb_w, thumb_h))
    x = 10 + (i % cols) * cell_w
    y = 10 + (i // cols) * cell_h
    sheet.paste(im, (x, y))
    d.text((x, y + thumb_h + 5), '%.1fs' % t, fill=(232, 163, 61), font=font)
out = os.path.join(ROOT, 'work', 'contact_verify.png')
sheet.save(out)
print('frames:', len(imgs))
print('contact->', out, sheet.size)
