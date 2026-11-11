#!/usr/bin/env python3
"""qc_sheet.py — planche contact (tuiles >= 480 px de large) + grille 16 px pour un groupe de plans."""
import sys, os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
files = sys.argv[1:-1]
out = sys.argv[-1]
TW = 500  # tile width >= 480
cols = 4
tiles = []
for f in files:
    im = Image.open(os.path.join(ROOT, f)).convert("RGB")
    r = TW / im.width
    im = im.resize((TW, int(im.height * r)), Image.LANCZOS)
    tiles.append((f, im))
rows = (len(tiles) + cols - 1) // cols
TH = max(t[1].height for t in tiles)
sheet = Image.new("RGB", (cols * (TW + 8) + 8, rows * (TH + 28) + 8), (24, 24, 28))
d = ImageDraw.Draw(sheet)
for idx, (name, im) in enumerate(tiles):
    x = 8 + (idx % cols) * (TW + 8)
    y = 8 + (idx // cols) * (TH + 28)
    sheet.paste(im, (x, y + 24))
    d.text((x + 4, y + 4), name, fill=(255, 232, 168))
    # grille 16 px sur la tuile
    gd = ImageDraw.Draw(sheet)
    for gx in range(x, x + TW, 16):
        gd.line([(gx, y + 24), (gx, y + 24 + im.height)], fill=(255, 255, 255, 40))
    for gy in range(y + 24, y + 24 + im.height, 16):
        gd.line([(x, gy), (x + TW, gy)], fill=(255, 255, 255, 40))
sheet.save(os.path.join(ROOT, out), quality=88)
print("écrit:", out, sheet.size, "|", len(files), "plans")
