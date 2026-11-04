#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cover.py — couverture TikTok dédiée (§7.5 v6.3). Une image, pas une frame du clip.
Usage : python3 cover.py prods/TU-ES-TROP-BELLE [--art art/cover-tiktok.png]
Sortie : <prod>/out/COVER-tiktok-1080x1920.jpg (JPEG q95, 4:4:4)
"""
import argparse, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from common import font, GOLD_A, GOLD_B, INK, NATIVE, OUT, vgrad

TITLE1, SIZE1 = "TU ES TROP", 128
TITLE2, SIZE2 = "BELLE", 112
XMIN, XMAX = 90, 990          # largeur utile ≤ 900 px


def clean_text(text, fnt, size, tracking):
    """Masques (encre, contour) sans rotation — lettrage cover. Contour par dilatation."""
    ow = max(3, size // 12)
    widths = []
    for ch in text:
        bb = fnt.getbbox(ch)
        widths.append(bb[2] - bb[0])
    total = int(sum(widths) + tracking * max(0, len(text) - 1) + 2 * (ow + 8))
    bb0 = fnt.getbbox(text)
    hgt = int(bb0[3] - bb0[1] + 2 * (ow + 8))
    ink = Image.new("L", (total, hgt), 0)
    x = ow + 8
    for ch, wd in zip(text, widths):
        if ch != " ":
            g = Image.new("L", (wd + 2 * ow + 6, hgt), 0)
            ImageDraw.Draw(g).text((ow + 3 - fnt.getbbox(ch)[0], ow + 8 - bb0[1]), ch, font=fnt, fill=255)
            ink.paste(g, (x - ow - 3, 0), g)
        x += wd + tracking
    cont = ink.filter(ImageFilter.MaxFilter(2 * ow + 1))
    return ink, cont


def paint_line(text, size, tracking, top, canvas):
    fnt = font("ExtraBold", size)
    ink, cont = clean_text(text, fnt, size, tracking)
    # auto-réduction par pas de 2 px (§7.5)
    while ink.width > (XMAX - XMIN) and size > 40:
        size -= 2
        fnt = font("ExtraBold", size)
        ink, cont = clean_text(text, fnt, size, tracking)
    x = (OUT[0] - ink.width) // 2
    lay = Image.new("RGBA", OUT, (0, 0, 0, 0))
    lay.paste(Image.new("RGBA", ink.size, INK + (255,)), (x, top), cont)
    grad = vgrad(ink.size, GOLD_A, GOLD_B).convert("RGBA")
    grad.putalpha(ink)
    lay.alpha_composite(grad, (x, top))
    canvas.alpha_composite(lay)
    return top + ink.height


def main(prod, art_rel):
    art_path = os.path.join(prod, art_rel)
    art = Image.open(art_path).convert("RGB")
    w, h = art.size
    scale = OUT[0] / w
    nh = round(h * scale)
    art = art.resize((OUT[0], nh), Image.LANCZOS)
    if nh > OUT[1]:
        art = art.crop((0, 0, OUT[0], OUT[1]))     # ancré en HAUT, rognage du bas
    else:
        c = Image.new("RGB", OUT, (0, 0, 0)); c.paste(art, (0, 0)); art = c

    canvas = art.convert("RGBA")
    # voile d'encre dégradé sur les 300 px du bas (α max 0,72)
    veil = Image.new("RGBA", (OUT[0], 300), (0, 0, 0, 0))
    a = np.linspace(0, 0.72, 300, dtype=np.float32)
    arr = np.zeros((300, OUT[0], 4), dtype=np.uint8)
    arr[:, :, 3] = (a[:, None] * 255).astype(np.uint8)
    arr[:, :, :3] = np.array([6, 9, 14], dtype=np.uint8)[None, None, :]
    canvas.alpha_composite(Image.fromarray(arr, "RGBA"), (0, 1620))

    # titre 2 lignes (or dégradé + contour dilaté), zone calme y 1069→1687
    y = 1150
    y = paint_line(TITLE1, SIZE1, 4, y, canvas) + 18
    y = paint_line(TITLE2, SIZE2, 4, y, canvas)

    # DSKY (Bold 60, interlettrage 16) entre deux filets or, y 1495
    fnt = font("Bold", 60)
    tr = 16
    widths = [fnt.getbbox(ch)[2] - fnt.getbbox(ch)[0] for ch in "DSKY"]
    tw = int(sum(widths) + tr * 3)
    dsky = Image.new("RGBA", (tw + 8, 80), (0, 0, 0, 0))
    x = 4
    for ch, wd in zip("DSKY", widths):
        bb = fnt.getbbox(ch)
        g = Image.new("L", (wd + 8, 80), 0)
        ImageDraw.Draw(g).text((4 - bb[0], 6), ch, font=fnt, fill=255)
        dsky.paste(Image.new("RGBA", g.size, GOLD_A + (255,)), (x - 4, 0), g)
        x += wd + tr
    dx = (OUT[0] - dsky.width) // 2
    canvas.alpha_composite(dsky, (dx, 1462))
    d = ImageDraw.Draw(canvas)
    d.rectangle([XMIN, 1493, dx - 24, 1497], fill=GOLD_A + (255,))
    d.rectangle([dx + dsky.width + 24, 1493, XMAX, 1497], fill=GOLD_A + (255,))

    # série « Wolof TechStein beat wê » y 1560
    f2 = font("SemiBold", 32)
    s = "Wolof TechStein beat wê"
    bb = f2.getbbox(s)
    simg = Image.new("RGBA", (bb[2] - bb[0] + 4, bb[3] - bb[1] + 4), (0, 0, 0, 0))
    ImageDraw.Draw(simg).text((2 - bb[0], 2 - bb[1]), s, font=f2, fill=GOLD_A + (255,))
    canvas.alpha_composite(simg, ((OUT[0] - simg.width) // 2, 1560))

    out = canvas.convert("RGB")
    os.makedirs(os.path.join(prod, "out"), exist_ok=True)
    dst = os.path.join(prod, "out", "COVER-tiktok-1080x1920.jpg")
    out.save(dst, quality=95, subsampling=0)     # 4:4:4
    print(f"cover -> {dst} {out.size}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prod")
    ap.add_argument("--art", default="art/cover-tiktok.png")
    args = ap.parse_args()
    main(args.prod, args.art)
