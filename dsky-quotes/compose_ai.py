#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pipeline 100 % IA — v2 ZONE SÛRE TIKTOK.
Usage : python3 compose_ai.py <n> [<n> ...]
Ouvre assets/bases/base-N.jpg, met à l'échelle en 1080 de large (~1620 de haut),
colle en HAUT du canvas 1080x1920 et prolonge le bandeau sombre du bas
(couleur échantillonnée) jusqu'à 1920. Résultat : citation, CTA et signature
remontent au-dessus de la barre de description TikTok (~80 % de hauteur).
"""
import os, sys
from PIL import Image, ImageDraw, ImageFilter

os.chdir(os.path.dirname(os.path.abspath(__file__)))

W, H = 1080, 1920
for arg in sys.argv[1:]:
    n = int(arg)
    src = Image.open(f"assets/bases/base-{n}.jpg").convert("RGB")
    nh = round(src.height * W / src.width)
    im = src.resize((W, nh), Image.LANCZOS)
    if nh >= H:
        top = (nh - H) // 2
        im = im.crop((0, top, W, top + H))
        canvas = im
    else:
        canvas = Image.new("RGB", (W, H))
        canvas.paste(im, (0, 0))
        strip = im.crop((0, nh - 24, W, nh)).resize((1, 1), Image.LANCZOS)
        r, g, b = strip.getpixel((0, 0))
        d = ImageDraw.Draw(canvas)
        for y in range(nh, H):
            t = (y - nh) / (H - nh)
            k = 1 - 0.38 * t
            d.line([(0, y), (W, y)], fill=(max(0, int(r * 0.9 * k)),
                                           max(0, int(g * 0.9 * k)),
                                           max(0, int(b * 0.9 * k))))
        seam = canvas.crop((0, nh - 10, W, nh + 10)).filter(ImageFilter.GaussianBlur(3))
        canvas.paste(seam, (0, nh - 10))
    canvas.save(f"saison-02/tiktok/quote-{n}-tiktok.jpg",
                quality=92, subsampling=0, optimize=True)
    print(f"✔ quote-{n}-tiktok.jpg  [100% IA · zone sûre v2]")
