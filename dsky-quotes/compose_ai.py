#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DSKY QUOTES — pipeline 100% IA (salve test 381-390).

Toute l'œuvre (citation FR + ligne EN + signature DSKY WTBW) est générée
par l'IA DANS l'image. Ce script ne fait que recadrer en 1080x1920 —
aucun branding codé, aucun texte ajouté.
Sortie : saison-02/tiktok/quote-N-tiktok.jpg
"""
import os
import sys
from PIL import Image
from compose import ROOT

W, H = 1080, 1920


def convert(num):
    src = os.path.join(ROOT, f"assets/bases/base-{num}.jpg")
    base = Image.open(src).convert("RGB")
    if base.size != (W, H):
        r = max(W / base.width, H / base.height)
        base = base.resize((int(base.width * r) + 1, int(base.height * r) + 1), Image.LANCZOS)
        x0 = (base.width - W) // 2
        y0 = (base.height - H) // 2
        base = base.crop((x0, y0, x0 + W, y0 + H))
    out = os.path.join(ROOT, f"saison-02/tiktok/quote-{num}-tiktok.jpg")
    base.save(out, quality=92, subsampling=0, optimize=True)
    print("✔", f"quote-{num}-tiktok.jpg  [100% IA]")


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "saison-02/tiktok"), exist_ok=True)
    for n in [int(a) for a in sys.argv[1:]]:
        convert(n)
