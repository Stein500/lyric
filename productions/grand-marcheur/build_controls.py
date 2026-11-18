#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Feuilles de contact : plans bruts, plans cuits, crops 1:1 de la bande texte (§11)."""
import glob, json, os
import outils  # amorce Pillow (hors Git)
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "controles")
os.makedirs(OUT, exist_ok=True)
CONTRACT = json.load(open(os.path.join(HERE, "verses_map.json"), encoding="utf-8"))
RED = {int(k) for k in CONTRACT["plans_non_conformes"]}
try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 19)
except Exception:
    FONT = ImageFont.load_default()
LABEL, COLS = 44, 5


def sheet(paths, out, tile_w, red_numbers=(), crop=None):
    im0 = Image.open(paths[0])
    th = (round(tile_w * (crop[3] - crop[1]) / (crop[2] - crop[0]))
          if crop else round(tile_w * im0.height / im0.width))
    rows = (len(paths) + COLS - 1) // COLS
    sheet_im = Image.new("RGB", (COLS * tile_w, rows * (th + LABEL)), (18, 18, 24))
    d = ImageDraw.Draw(sheet_im)
    for n, p in enumerate(paths):
        im = Image.open(p).convert("RGB")
        if crop:
            im = im.crop(crop)                      # 1:1, aucun redimensionnement
        else:
            im = im.resize((tile_w, th), Image.LANCZOS)
        x, y = (n % COLS) * tile_w, (n // COLS) * (th + LABEL)
        sheet_im.paste(im, (x, y + LABEL))
        name = os.path.basename(p)
        num = int(name.split("-")[1].split(".")[0])
        bad = num in red_numbers
        d.rectangle([x, y, x + tile_w, y + LABEL], fill=(120, 28, 38) if bad else (24, 24, 32))
        d.text((x + 10, y + 11), ("NON CONFORME · " if bad else "") + name,
               fill=(255, 228, 228) if bad else (245, 235, 210), font=FONT)
    sheet_im.save(out, quality=92)
    print(out, sheet_im.size, "tuiles", tile_w, "x", th, "|", len(paths), "plans")


raw = sorted(glob.glob(os.path.join(HERE, "assets", "plans", "*.jpg")))
cuit = sorted(glob.glob(os.path.join(HERE, "assets", "cuits", "*.jpg")))
sheet(raw, os.path.join(OUT, "contact-plans.jpg"), 480, RED)
sheet(cuit, os.path.join(OUT, "contact-cuits.jpg"), 480, RED)
sheet(cuit, os.path.join(OUT, "crops-texte-1-1.jpg"), 526, (), crop=(121, 400, 647, 1000))
