#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Constantes et utilitaires communs — prod lyrics v6.3 (1080x1920 / natif 768x1376)."""
import os, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(REPO, "fonts")
NATIVE = (768, 1376)          # sortie générateur
OUT = (1080, 1920)            # sortie TikTok
FPS = 30

# --- polices ---
def font(weight, size):
    return ImageFont.truetype(os.path.join(FONTS, f"Montserrat-{weight}.ttf"), size)

# --- couleurs ---
GOLD_A, GOLD_B = (255, 232, 168), (232, 168, 66)        # or ligne 1 / cover
CY_A, CY_B = (240, 252, 255), (150, 205, 224)           # argent-cyan ligne 2
INK = (10, 14, 20)                                       # contour / halo
GOLD_HOT = (255, 224, 122)                               # mot actif pilule
GOLD_LINE = (232, 168, 66)

# --- géométrie (natif 768x1376) ---
LETTER_BOX = (150, 470, 590, 750)   # x0,y0,x1,y1 boîte lettrage §3.2

def load_plan(path):
    """Charge un plan du générateur et le normalise en 768x1376 ancré en HAUT."""
    im = Image.open(path).convert("RGB")
    w, h = im.size
    tw, th = NATIVE
    scale = tw / w
    nh = round(h * scale)
    im = im.resize((tw, nh), Image.LANCZOS)
    if nh >= th:
        im = im.crop((0, 0, tw, th))
    else:
        canvas = Image.new("RGB", (tw, th), (0, 0, 0))
        canvas.paste(im, (0, 0))
        im = canvas
    return im

def vgrad(size, top, bottom):
    """Dégradé vertical RGBA opaque."""
    w, h = size
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    a = np.array(top, dtype=np.float32)[None, None, :]
    b = np.array(bottom, dtype=np.float32)[None, None, :]
    arr = (a * (1 - t) + b * t).astype(np.uint8)
    arr = np.broadcast_to(arr, (h, w, 3)).copy()
    return Image.fromarray(arr, "RGB")

def deterministic_seed(*parts):
    s = "|".join(str(p) for p in parts).encode("utf-8")
    import zlib
    return zlib.crc32(s) & 0xFFFFFFFF

def blur(im, r):
    return im.filter(ImageFilter.GaussianBlur(r))

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)
