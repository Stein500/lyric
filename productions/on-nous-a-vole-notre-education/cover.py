#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cover.py — couverture TikTok 9:16 pour ON NOUS A VOLÉ NOTRE ÉDUCATION.

Le générateur ne peint aucun texte : il fournit l'art (fonds/cover-tiktok.png),
ce script pose la typo dans la zone sombre de la veste, sous le visage.

  python3 cover.py            # -> livrables/COVER-tiktok-1080x1920.jpg
"""
import os

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

import lettering

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "livrables", "COVER-tiktok-1080x1920.jpg")

GOLD_TOP, GOLD_BOT = (255, 233, 170), (226, 160, 54)
CREAM, GOLD_HOT = (255, 255, 255), (255, 224, 122)


def spaced(dr, xy, txt, f, fill, spacing=0, anchor=None, stroke=0, stroke_fill=None):
    """texte à interlettrage, centré sur xy."""
    widths = [dr.textlength(c, font=f) for c in txt]
    total = sum(widths) + spacing * (len(txt) - 1)
    x, y = xy
    if anchor == "mm":
        x -= total / 2
    for c, w in zip(txt, widths):
        dr.text((x, y), c, font=f, fill=fill, anchor="lm" if anchor == "mm" else "la",
                stroke_width=stroke, stroke_fill=stroke_fill)
        x += w + spacing
    return total


def grad_text(txt, f, top, bot, stroke=6):
    """capitales en dégradé vertical, contour d'encre par dilatation."""
    tmp = Image.new("RGBA", (10, 10))
    d0 = ImageDraw.Draw(tmp)
    b = d0.textbbox((0, 0), txt, font=f)
    pad = 40
    w, h = b[2] - b[0] + 2 * pad, b[3] - b[1] + 2 * pad
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).text((pad - b[0], pad - b[1]), txt, font=f, fill=255)
    grad = lettering._grad((w, h), top, bot).convert("RGBA")
    grad.putalpha(m)
    ol = m.filter(ImageFilter.MaxFilter(2 * stroke + 1)).filter(ImageFilter.GaussianBlur(0.8))
    ink = Image.new("RGBA", (w, h), (4, 6, 10, 255))
    ink.putalpha(ol.point(lambda v: int(v * 0.95)))
    drop = m.filter(ImageFilter.MaxFilter(2 * max(1, stroke // 2) + 1))
    drop = ImageChops.offset(drop, 6, 9).filter(ImageFilter.GaussianBlur(6))
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    sh.putalpha(drop.point(lambda v: int(v * 0.5)))
    res = Image.alpha_composite(Image.alpha_composite(sh, ink), grad)
    return res.crop(res.split()[3].getbbox())


def main():
    im = Image.open(os.path.join(HERE, "fonds", "cover-tiktok.png")).convert("RGB")
    im = im.resize((1080, 1920), Image.LANCZOS)
    W, H = im.size
    base = im.convert("RGBA")

    # voile d'encre doux dans le bas (lisibilité du titre), fondu sur 300 px
    veil = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(veil)
    for y in range(1180, H):
        vd.line([(0, y), (W, y)], fill=int(200 * min(1.0, (y - 1180) / 300)))
    veil = veil.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.72))
    base = Image.alpha_composite(base, Image.merge("RGBA", [
        Image.new("L", (W, H), 3), Image.new("L", (W, H), 5),
        Image.new("L", (W, H), 9), veil]))

    d = ImageDraw.Draw(base)
    f_big = ImageFont.truetype(os.path.join(FONTS, "Montserrat-ExtraBold.ttf"), 128)
    f_mid = ImageFont.truetype(os.path.join(FONTS, "Montserrat-ExtraBold.ttf"), 104)
    f_sm = ImageFont.truetype(os.path.join(FONTS, "Montserrat-SemiBold.ttf"), 40)

    # ligne 1 : ON NOUS A VOLÉ · ligne 2 : NOTRE ÉDUCATION
    MAXW = 900                       # marge de sécurité : rien hors de x 90 -> 990
    for txt, f0, y in (("ON NOUS A VOLÉ", f_big, 1288), ("NOTRE ÉDUCATION", f_mid, 1402)):
        f = f0
        lay = grad_text(txt, f, GOLD_TOP, GOLD_BOT, stroke=max(4, f.size // 14))
        while lay.width > MAXW and f.size > 40:
            f = ImageFont.truetype(f.path, f.size - 2)
            lay = grad_text(txt, f, GOLD_TOP, GOLD_BOT, stroke=max(4, f.size // 14))
        base.alpha_composite(lay, (int(W / 2 - lay.width / 2), int(y - lay.height / 2)))

    # artiste + série
    d = ImageDraw.Draw(base)
    spaced(d, (W / 2, 1495), "DSKY", ImageFont.truetype(os.path.join(FONTS, "Montserrat-Bold.ttf"), 60),
           CREAM + (255,), spacing=16, anchor="mm", stroke=4, stroke_fill=(6, 8, 12, 230))
    d.text((W / 2, 1560), "Wolof TechStein beat wê", font=f_sm, fill=GOLD_HOT + (240,), anchor="mm")
    d.line([(W / 2 - 250, 1521), (W / 2 - 150, 1521)], fill=GOLD_HOT + (220,), width=3)
    d.line([(W / 2 + 150, 1521), (W / 2 + 250, 1521)], fill=GOLD_HOT + (220,), width=3)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    base.convert("RGB").save(OUT, quality=95, subsampling=0)
    print("écrit", OUT, base.size)


if __name__ == "__main__":
    main()
