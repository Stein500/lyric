#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Feuille de contact de la salve 01 (tuiles >= 480 px de large, §11)."""
import os, sys, glob, json
import outils  # amorce Pillow (hors Git, réinstallé si purgé)
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sorted(glob.glob(os.path.join(HERE, "assets", "plans", "*.jpg")))
OUT = os.path.join(HERE, "controles", "contact-plans-tous.jpg")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
CONTRACT = json.load(open(os.path.join(HERE, "verses_map.json"), encoding="utf-8"))
NON_CONFORMES = {"plan-%02d.jpg" % int(k) for k in CONTRACT["plans_non_conformes"]}
TW, LABEL, COLS = 480, 44, 5
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 19)
except Exception:
    font = ImageFont.load_default()
_w, _h = Image.open(SRC[0]).size
th = round(TW * _h / _w)  # ratio réel des plans natifs 768 x 1376
rows = (len(SRC) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * TW, rows * (th + LABEL)), (18, 18, 24))
d = ImageDraw.Draw(sheet)
for n, f in enumerate(SRC):
    im = Image.open(f).convert("RGB").resize((TW, th), Image.LANCZOS)
    x, y = (n % COLS) * TW, (n // COLS) * (th + LABEL)
    sheet.paste(im, (x, y + LABEL))
    name = os.path.basename(f)
    bad = name in NON_CONFORMES
    d.rectangle([x, y, x + TW, y + LABEL], fill=(120, 28, 38) if bad else (24, 24, 32))
    d.text((x + 10, y + 11), ("NON CONFORME · " if bad else "") + name,
           fill=(255, 228, 228) if bad else (245, 235, 210), font=font)
sheet.save(OUT, quality=92)
print("contact sheet:", OUT, sheet.size, "tuiles", TW, "x", th,
      "|", len(SRC), "plans |", len(NON_CONFORMES), "non conformes")
