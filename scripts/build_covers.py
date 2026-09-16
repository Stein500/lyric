#!/usr/bin/env python3
"""§D.9 covers: base IA (s01_refrain1) + titre intégré en post (orthographe garantie).
Sorties: cover_<titre>_9x16.jpg (1080x1920 q92) + cover_<titre>_1080x1080.jpg (APIC).
Usage: .venv/bin/python scripts/build_covers.py
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CURSIVE = os.path.join(ROOT, "assets", "fonts", "GreatVibes-Regular.ttf")
BOLD = os.path.join(ROOT, "assets", "fonts", "DejaVuSans-Bold.ttf")
BASE = os.path.join(ROOT, "assets", "raw", "cover_base.jpg")  # base IA dédiée (salve covers) — v2
os.makedirs(os.path.join(ROOT, "livrables"), exist_ok=True)

TITLE = "Ayon dèkpè"
ARTIST = "Daïsky"
GOLD = (255, 205, 84)
GOLD_L = (255, 224, 130)
CREAM = (255, 246, 226)
AMBER = (255, 172, 60)

def cover_resize(img, w, h):
    iw, ih = img.size
    s = max(w/iw, h/ih)
    img = img.resize((round(iw*s), round(ih*s)), Image.LANCZOS)
    l = (img.width-w)//2; t = (img.height-h)//2
    return img.crop((l, t, l+w, t+h))

def fit_font(path, text, maxw, start=300, floor=40):
    size = start
    while size > floor and ImageFont.truetype(path, size).getlength(text) > maxw:
        size -= 4
    return ImageFont.truetype(path, size), size

def make_cover(w, h, top_scrim=True):
    im = cover_resize(Image.open(BASE).convert("RGB"), w, h).convert("RGB")
    arr = np.asarray(im).astype(np.float32)
    # top dark scrim for title legibility
    if top_scrim:
        band = int(h*0.42)
        for y in range(band):
            k = 1 - y/band
            arr[y] = arr[y]*(0.35 + 0.65*k) + np.array([8,10,18], np.float32)*(1-k)*0.9
    im = Image.fromarray(arr.astype(np.uint8))
    d = ImageDraw.Draw(im)
    cx = w/2
    # title cursive gold
    f, sz = fit_font(CURSIVE, TITLE, w*0.9, start=round(w*0.30), floor=40)
    d.text((cx - f.getlength(TITLE)/2 + 4, h*0.10 + 4), TITLE, font=f, fill=(60,20,0,255))
    d.text((cx - f.getlength(TITLE)/2, h*0.10), TITLE, font=f, fill=GOLD)
    # artist
    fa, _ = fit_font(BOLD, ARTIST, w*0.7, start=round(w*0.10), floor=24)
    ty = h*0.10 + sz*1.05 + 10
    d.text((cx - fa.getlength(ARTIST)/2, ty), ARTIST, font=fa, fill=CREAM)
    # badge bottom-center
    fb = ImageFont.truetype(BOLD, round(w*0.055))
    badge = "DSKY✓"
    by = h - round(w*0.055)*2 - 20
    d.text((cx - fb.getlength(badge)/2, by), badge, font=fb, fill=AMBER)
    return im

c16 = make_cover(1080, 1920)
c16.save(os.path.join(ROOT, "livrables", "cover_Ayon dèkpè_9x16.jpg"), quality=92)
# square: center crop of the 9:16 (keeps title + dancer focus)
sq = make_cover(1080, 1080, top_scrim=True)
sq.save(os.path.join(ROOT, "livrables", "cover_Ayon dèkpè_1080x1080.jpg"), quality=92)
print("covers written")
