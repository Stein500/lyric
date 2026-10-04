#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble une planche contact (vignettes + noms) pour un lot de fonds.
Usage : planche.py "<glob>" out.jpg "Titre" ["sous-titre"] [hauteur_vignette] [colonnes]"""
import sys, glob, os
from PIL import Image, ImageDraw, ImageFont

B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f = lambda s: ImageFont.truetype(B, s)


def planche(pattern, sortie, titre, sous_titre="", th=560, cols=None):
    files = []
    for pat in pattern.split(","):
        files += glob.glob(pat.strip())
    files = sorted(set(files))
    if not files:
        raise SystemExit("aucun fichier : " + pattern)
    ims = [(os.path.basename(x).replace(".png", ""), Image.open(x).convert("RGB")) for x in files]
    if cols is None:
        cols = len(ims)
    rows = (len(ims) + cols - 1) // cols
    pad, gap, lab = 22, 14, 70
    cw = max(int(im.width * th / im.height) for _, im in ims)
    W = pad * 2 + cols * cw + gap * (cols - 1)
    H = 88 + rows * (th + lab) + pad
    c = Image.new("RGB", (W, H), (12, 12, 16))
    d = ImageDraw.Draw(c)
    d.text((pad, 16), titre, font=f(25), fill=(255, 196, 78))
    if sous_titre:
        d.text((pad, 48), sous_titre, font=f(17), fill=(180, 180, 190))
    for k, (n, im) in enumerate(ims):
        r, col = divmod(k, cols)
        w = int(im.width * th / im.height)
        x = pad + col * (cw + gap)
        y = 88 + r * (th + lab)
        c.paste(im.resize((w, th), Image.LANCZOS), (x, y))
        d.rectangle([x, y, x + w, y + th], outline=(80, 80, 90))
        d.text((x + w // 2, y + th + 14), n, font=f(16), fill=(235, 235, 235), anchor="ma")
        d.text((x + w // 2, y + th + 36), f"{im.width}x{im.height}", font=f(14), fill=(150, 150, 160), anchor="ma")
    c.save(sortie, quality=90)
    print(sortie, c.size, len(ims), "images")


if __name__ == "__main__":
    planche(sys.argv[1], sys.argv[2], sys.argv[3],
            sys.argv[4] if len(sys.argv) > 4 else "",
            int(sys.argv[5]) if len(sys.argv) > 5 else 560,
            int(sys.argv[6]) if len(sys.argv) > 6 else None)
