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
import json, math, os, random, zlib
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
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


def line_layer(text, path, maxw, maxh, top, bot, seed, jitter=1.0):
    """une ligne : glyphes à jitter, contour d'encre, dégradé.
    Le contour est une DILATATION du masque placée DERRIÈRE les lettres : jamais de
    contre-forme bouchée (le A reste un A), anticrénelage conservé."""
    rnd = random.Random(seed)
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    f, _ = _fit(probe, text, path, maxw - 40, maxh - 26, 92)
    ow = max(3, f.size // 10)                       # épaisseur du contour
    boxes = [probe.textbbox((0, 0), c, font=f) for c in text]
    iw = [b[2] - b[0] for b in boxes]
    atop = min(b[1] for b in boxes)
    abot = max(b[3] for b in boxes)
    ih = abot - atop
    track = max(2.0, f.size * 0.055)
    total = sum(iw) + track * (len(text) - 1)
    PAD = 70
    canvas = Image.new("RGBA", (int(total) + 2 * PAD, int(ih) + 2 * PAD), (0, 0, 0, 0))
    x = PAD
    for i, c in enumerate(text):
        w = max(2, iw[i])
        tile = Image.new("RGBA", (w + 2 * PAD, ih + 2 * PAD), (0, 0, 0, 0))
        ImageDraw.Draw(tile).text((PAD - boxes[i][0], PAD - atop), c, font=f,
                                 fill=(255, 255, 255, 255))
        ang = 0.0 if c == " " else rnd.uniform(-jitter, jitter)
        rot = tile.rotate(ang, resample=Image.BICUBIC, expand=True)
        canvas.alpha_composite(rot, (int(x + w / 2 - rot.width / 2),
                                     int(PAD + ih / 2 - rot.height / 2)))
        x += iw[i] + track
    alpha = canvas.split()[3]                        # anticrénelé, jamais binarisé
    grad = _grad(canvas.size, top, bot).convert("RGBA")
    grad.putalpha(alpha)
    drop = alpha.filter(ImageFilter.MaxFilter(2 * (ow // 2) + 1))
    drop = ImageChops.offset(drop, 3, 4).filter(ImageFilter.GaussianBlur(1.6))
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 255))
    sh.putalpha(drop.point(lambda v: int(v * 0.45)))
    ol = alpha.filter(ImageFilter.MaxFilter(2 * ow + 1)).filter(ImageFilter.GaussianBlur(0.6))
    ink = Image.new("RGBA", canvas.size, (5, 7, 10, 255))
    ink.putalpha(ol.point(lambda v: int(v * 0.97)))
    res = Image.alpha_composite(Image.alpha_composite(sh, ink), grad)
    hi = ImageChops.subtract(alpha, ImageChops.offset(alpha, 0, 3)).filter(ImageFilter.GaussianBlur(0.6))
    lum = Image.new("RGBA", canvas.size, (255, 255, 255, 0))
    lum.putalpha(hi.point(lambda v: int(v * 0.55)))
    res = Image.alpha_composite(res, lum)
    return res.crop(res.split()[3].getbbox()), f


def dy_for(name):
    """décalage vertical du bloc, par plan (fichier typo_offsets.json)."""
    try:
        d = json.load(open(os.path.join(HERE, "typo_offsets.json"), encoding="utf-8"))
        return int(d.get(os.path.basename(name), 0))
    except Exception:
        return 0


def draw_lettering(base, l1, l2, font_path, bucket="nuit", neutralise=False, dy=0):
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
    return _paint(base, l1, l2, font_path, bucket, dy)


def _paint(base, l1, l2, font_path, bucket, dy=0):
    """halo = ombre portée qui épouse les lettres (jamais de flaque opaque)."""
    W, H = base.size
    x0, y0, x1, y1 = BOX
    y0, y1 = y0 + dy, y1 + dy
    bw, bh = x1 - x0, y1 - y0
    seed = zlib.crc32(("%s|%s" % (l1, l2)).encode("utf-8"))
    rnd = random.Random(seed)

    # ---------- 1. les deux lignes, calculées AVANT l'encre
    if l2:
        lay1, f1 = line_layer(l1, font_path, bw, int(bh * 0.44), GOLD_TOP, GOLD_BOT, seed + 1)
        lay2, f2 = line_layer(l2, font_path, bw, int(bh * 0.30), CYAN_TOP, CYAN_BOT, seed + 2)
        gap = 26
        th = lay1.height + gap + lay2.height
        top = y0 + (bh - th) / 2
        p1 = (int(x0 + (bw - lay1.width) / 2), int(top))
        p2 = (int(x0 + (bw - lay2.width) / 2), int(top + lay1.height + gap))
        yb = top + th
        poses = [(lay1, p1), (lay2, p2)]
    else:
        gold = bucket != "aube-b"
        lay1, f1 = line_layer(l1, font_path, bw, int(bh * 0.52),
                              GOLD_TOP if gold else CREAM_TOP, GOLD_BOT if gold else CREAM_BOT, seed + 1)
        p1 = (int(x0 + (bw - lay1.width) / 2), int(y0 + (bh - lay1.height) / 2))
        yb = p1[1] + lay1.height
        poses = [(lay1, p1)]

    glyph = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for lay, p in poses:
        glyph.alpha_composite(lay, p)
    ga = glyph.split()[3]

    # ---------- 2. ombre serrée : dilatation 5 px + deux flous, opacité bornée
    tight = ga.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(7))
    wide = ga.filter(ImageFilter.GaussianBlur(17))
    sh = ImageChops.lighter(tight.point(lambda v: int(v * 0.68)),
                            wide.point(lambda v: int(v * 0.40)))

    # ---------- 3. pulvérisation : mouchetures UNIQUEMENT autour des glyphes
    zone = ga.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(5)).point(lambda v: 255 if v > 40 else 0)
    sp = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(sp)
    for i in range(150):
        cx = rnd.uniform(x0 - 24, x1 + 24)
        cy = rnd.uniform(y0 - 20, y1 + 20)
        r = rnd.uniform(0.5, 2.1)
        sd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rnd.randint(45, 110))
    sp = sp.filter(ImageFilter.GaussianBlur(0.7))
    sp = Image.composite(sp, Image.new("L", (W, H), 0), zone)

    ink = Image.new("RGBA", (W, H), (4, 7, 11, 0))
    ink.putalpha(ImageChops.lighter(sh, sp))
    base = Image.alpha_composite(base.convert("RGBA"), ink)

    # ---------- 4. les lettres par-dessus
    for lay, p in poses:
        base.alpha_composite(lay, p)

    # ---------- 5. coulures d'encre sous le bloc
    dr = ImageDraw.Draw(base)
    for i in range(rnd.randint(3, 6)):
        dx = x0 + rnd.uniform(0.12, 0.88) * bw
        ln = rnd.uniform(14, 46)
        w = rnd.uniform(1.4, 3.0)
        dr.line([(dx, yb + 3), (dx, yb + 3 + ln)], fill=(4, 6, 9, 190), width=int(w))
        dr.ellipse([dx - w, yb + ln, dx + w, yb + ln + w * 2.2], fill=(4, 6, 9, 190))
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
