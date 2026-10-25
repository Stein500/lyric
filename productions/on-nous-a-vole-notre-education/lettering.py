#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lettering.py — lettrage graffiti PEINT PAR LE MOTEUR (v6.2).

Le générateur d'images ne tient ni la taille, ni la position, ni l'orthographe du
texte peint : mesuré sur 18 plans, 0/18 dans la boîte, capitales 110 px pour 34
demandées. On garde donc du modèle **l'art** (personnage, décor, stickers) et on
peint les paroles ici, à la main, exactement dans la boîte :

    natif 768x1376 :  x 150 → 590 (440 px)   y 470 → 750 (280 px)

Rendu : halo d'encre pulvérisé + capitales Montserrat ExtraBold à jitter, contour
d'encre, dégradé or/crème (ligne 1) et argent-cyan (ligne 2), coulures, taches.
Le lettrage est CUIT dans le PNG : aucun calque mobile, aucun ghosting.
"""
import math, random
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

BOX = (150, 470, 590, 750)          # natif
GOLD_TOP, GOLD_BOT = (255, 232, 168), (232, 168, 62)
CYAN_TOP, CYAN_BOT = (240, 252, 255), (150, 205, 224)
CREAM_TOP, CREAM_BOT = (255, 255, 255), (214, 226, 240)


def _font(size, path):
    return ImageFont.truetype(path, size)


def _grad(size, top, bot):
    g = Image.new("RGB", size, top)
    d = ImageDraw.Draw(g)
    h = size[1]
    for y in range(h):
        u = y / max(1, h - 1)
        c = tuple(int(top[i] + (bot[i] - top[i]) * u) for i in range(3))
        d.line([(0, y), (size[0], y)], fill=c)
    return g


def _fit(draw, text, path, maxw, maxh, start):
    """taille de police : la ligne tient dans maxw x maxh."""
    s = start
    while s > 12:
        f = _font(s, path)
        b = draw.textbbox((0, 0), text, font=f, stroke_width=0)
        if b[2] - b[0] <= maxw and b[3] - b[1] <= maxh:
            return f, b
        s -= 1
    return _font(12, path), draw.textbbox((0, 0), text, font=_font(12, path))


def line_layer(text, path, maxw, maxh, top, bot, seed, jitter=1.1):
    """une ligne : lettres à jitter, contour d'encre, dégradé, léger arc.
    Chaque glyphe est tourné avec expand=True puis recentré : aucun accent coupé."""
    rnd = random.Random(seed)
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    f, bb = _fit(probe, text, path, maxw - 30, maxh - 24, 96)
    asc, desc = f.getmetrics()
    widths = [probe.textlength(c, font=f) for c in text]
    track = max(1.2, f.size * 0.045)
    total = sum(widths) + track * (len(text) - 1)
    PAD = 90
    canvas = Image.new("RGBA", (int(total) + 2 * PAD, asc + desc + 2 * PAD), (0, 0, 0, 0))
    x = PAD
    for i, c in enumerate(text):
        if c == " ":
            x += widths[i] + track
            continue
        w = int(widths[i]) + 8
        tile = Image.new("RGBA", (w + 2 * PAD, asc + desc + 2 * PAD), (0, 0, 0, 0))
        td = ImageDraw.Draw(tile)
        td.text((PAD, PAD), c, font=f, fill=(255, 255, 255, 255),
                stroke_width=max(3, f.size // 13), stroke_fill=(6, 8, 12, 255))
        ang = rnd.uniform(-jitter, jitter)
        rot = tile.rotate(ang, resample=Image.BICUBIC, expand=True)
        cx = x + w / 2
        cy = PAD + (asc + desc) / 2
        canvas.alpha_composite(rot, (int(cx - rot.width / 2), int(cy - rot.height / 2)))
        x += widths[i] + track
    # arc léger : les bords remontent de 4 px
    alpha = canvas.split()[3].point(lambda v: 255 if v > 20 else 0)
    grad = _grad(canvas.size, top, bot).convert("RGBA")
    grad.putalpha(alpha)
    ink = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ink.paste((5, 7, 10, 255), mask=canvas.split()[3].point(lambda v: 255 if v > 30 else 0))
    res = Image.alpha_composite(ink, grad)
    hi = ImageChops.subtract(alpha, ImageChops.offset(alpha, 0, 3)).filter(ImageFilter.GaussianBlur(0.5))
    lum = Image.new("RGBA", canvas.size, (255, 255, 255, 0))
    lum.putalpha(hi.point(lambda v: int(v * 0.65)))
    res = Image.alpha_composite(res, lum)
    return res.crop(res.split()[3].getbbox()), f


def draw_lettering(base, l1, l2, font_path, bucket="nuit", neutralise=False):
    """peint le bloc dans `base` (768x1376). neutralise=True si l'art contient déjà du texte."""
    W, H = base.size
    x0, y0, x1, y1 = BOX
    bw, bh = x1 - x0, y1 - y0

    if neutralise:
        F = 60
        bx0, by0, bx1, by1 = x0 - 46, y0 - 46, x1 + 46, y1 + 46
        box_w, box_h = bx1 - bx0, by1 - by0
        mask = Image.new("L", (box_w, box_h), 0)
        md = ImageDraw.Draw(mask)
        md.rounded_rectangle([F, F, box_w - F, box_h - F], radius=30, fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(F * 0.55))
        reg = base.crop((bx0, by0, bx1, by1)).filter(ImageFilter.GaussianBlur(9))
        reg = Image.blend(reg, Image.new("RGB", reg.size, (10, 20, 26)), 0.72)
        base.paste(reg, (bx0, by0), mask)
    return _paint(base, l1, l2, font_path, bucket)


def _paint(base, l1, l2, font_path, bucket):
    W, H = base.size
    x0, y0, x1, y1 = BOX
    bw, bh = x1 - x0, y1 - y0
    seed = abs(hash((l1, l2))) % 10 ** 6
    rnd = random.Random(seed)

    # ---------- halo d'encre pulvérisé (organique, aucune ligne droite)
    halo = Image.new("L", (W, H), 0)
    hd = ImageDraw.Draw(halo)
    for i in range(26):
        cx = x0 + rnd.uniform(0.05, 0.95) * bw
        cy = y0 + rnd.uniform(0.12, 0.92) * bh
        rx = rnd.uniform(0.20, 0.42) * bw
        ry = rnd.uniform(0.16, 0.34) * bh
        hd.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
    hd.rectangle([x0 - 26, y0 - 26, x1 + 26, y1 + 26], fill=255)
    halo = halo.filter(ImageFilter.GaussianBlur(30)).point(lambda v: int(min(255, v * 1.35)))
    sp = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(sp)
    for i in range(240):
        cx = x0 + rnd.uniform(-30, bw + 30)
        cy = y0 + rnd.uniform(-24, bh + 24)
        r = rnd.uniform(0.6, 2.6)
        sd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rnd.randint(60, 150))
    sp = sp.filter(ImageFilter.GaussianBlur(0.8))
    ink = Image.new("RGBA", (W, H), (3, 5, 8, 0))
    ink.putalpha(ImageChops.lighter(halo, sp).point(lambda v: int(v * 0.985)))
    base = Image.alpha_composite(base.convert("RGBA"), ink)

    # ---------- les deux lignes
    if l2:
        lay1, f1 = line_layer(l1, font_path, bw, int(bh * 0.44), GOLD_TOP, GOLD_BOT, seed + 1)
        lay2, f2 = line_layer(l2, font_path, bw, int(bh * 0.30), CYAN_TOP, CYAN_BOT, seed + 2)
        gap = 26
        total_h = lay1.height + gap + lay2.height
        top = y0 + (bh - total_h) / 2
        base.alpha_composite(lay1, (int(x0 + (bw - lay1.width) / 2), int(top)))
        base.alpha_composite(lay2, (int(x0 + (bw - lay2.width) / 2), int(top + lay1.height + gap)))
        yb = top + total_h
    else:
        gold = bucket != "aube-b"
        lay1, f1 = line_layer(l1, font_path, bw, int(bh * 0.52),
                              GOLD_TOP if gold else CREAM_TOP, GOLD_BOT if gold else CREAM_BOT, seed + 1)
        base.alpha_composite(lay1, (int(x0 + (bw - lay1.width) / 2), int(y0 + (bh - lay1.height) / 2)))
        yb = y0 + bh * 0.7

    # ---------- coulures d'encre
    dr = ImageDraw.Draw(base)
    for i in range(rnd.randint(3, 6)):
        dx = x0 + rnd.uniform(0.12, 0.88) * bw
        ln = rnd.uniform(14, 46)
        w = rnd.uniform(1.4, 3.0)
        dr.line([(dx, yb - 22), (dx, yb - 22 + ln)], fill=(4, 6, 9, 210), width=int(w))
        dr.ellipse([dx - w, yb - 24 + ln, dx + w, yb - 20 + ln + w * 2], fill=(4, 6, 9, 210))
    return base.convert("RGB")


if __name__ == "__main__":
    import sys, os
    here = os.path.dirname(os.path.abspath(__file__))
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "fonds", "scene-01-ancre.png")
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/test-lettering.png"
    im = Image.open(src).convert("RGB")
    im = draw_lettering(im, "ON NOUS A VOLÉ", "NOTRE ÉDUCATION",
                        os.path.join(here, "fonts", "Montserrat-ExtraBold.ttf"))
    im.save(out)
    im.crop((0, 380, 768, 1000)).save(out.replace(".png", "-crop.png"))
    print("écrit", out)
