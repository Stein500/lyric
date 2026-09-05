#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COVERS v2 (règle artiste 2026-09-03) : base IA = collage multi-panneaux du clip,
puis TEXTE posé en PIL (jamais généré par l'IA) :
  - passage fort en Great Vibes ambre
  - « Daïsky Prod » en bas comme AUTEUR + @daiskypro + signature
  - badge statique haut-gauche
Sorties : livrables/cover_..._{carre,9x16,16x9}.jpg
"""
import math

from PIL import Image, ImageDraw, ImageFilter, ImageFont

DEJ = "/usr/share/fonts/truetype/dejavu/"
GREAT = "fonts/GreatVibes-Regular.ttf"
CYAN = (77, 210, 255)
AMBER = (232, 163, 61)
BLANC = (245, 249, 255)

PASSAGE = "Je suis pauvre mais je kiffe ma vie, c'est étrange"

OUT = {
    "carre": ("work/cover_base_carre.png", (1080, 1080), "livrables/cover_je_suis_pauvre_mais_je_kiffe_carre_1080.jpg"),
    "916": ("work/cover_base_916.png", (1080, 1920), "livrables/cover_je_suis_pauvre_mais_je_kiffe_9x16.jpg"),
    "169": ("work/cover_base_169.png", (1920, 1080), "livrables/cover_je_suis_pauvre_mais_je_kiffe_16x9.jpg"),
}


def fit(path, W, H):
    im = Image.open(path).convert("RGB")
    rw, rh = W / im.width, H / im.height
    r = max(rw, rh)
    im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def glow_text(d, xy, txt, font, fill, blur=8, alpha=255):
    sp = Image.new("RGBA", (int(d.textlength(txt, font=font)) + 4 * blur + 60, font.size + 4 * blur + 40), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sp)
    sd.text((2 * blur + 30, 2 * blur + 10), txt, font=font, fill=fill + (alpha,))
    g = sp.filter(ImageFilter.GaussianBlur(blur))
    sp = Image.alpha_composite(g, sp)
    d = None
    return sp


def badge(d, x=36, y=36, scale=1.0):
    f_lab = ImageFont.truetype(DEJ + "DejaVuSans-Bold.ttf", int(34 * scale))
    f_hdl = ImageFont.truetype(DEJ + "DejaVuSans.ttf", int(24 * scale))
    lab, hdl = "DAÏSKY PROD", "@daiskypro"
    pad_x, pad_y, gap = int(22 * scale), int(16 * scale), int(42 * scale)
    tw = max(f_lab.getlength(lab), f_hdl.getlength(hdl))
    bw, bh = int(tw + pad_x * 2 + gap), int(pad_y * 2 + 34 * scale + 24 * scale + 6 * scale)
    layer = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    dd = ImageDraw.Draw(layer)
    dd.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=bh // 2,
                         fill=(5, 6, 10, 165), outline=CYAN + (235,), width=3)
    s = int(52 * scale)
    cx, cy = pad_x + gap / 2, bh / 2
    dd.polygon([(cx + 0.10 * s, cy - 0.50 * s), (cx - 0.28 * s, cy + 0.06 * s),
                (cx - 0.02 * s, cy + 0.06 * s), (cx - 0.12 * s, cy + 0.50 * s),
                (cx + 0.30 * s, cy - 0.10 * s), (cx + 0.02 * s, cy - 0.10 * s)],
               fill=AMBER + (255,))
    tx = pad_x + gap
    dd.text((tx, pad_y - 2), lab, font=f_lab, fill=BLANC + (255,))
    dd.text((tx, pad_y + int(36 * scale)), hdl, font=f_hdl, fill=CYAN + (235,))
    return layer


def wrap2(d, txt, font, max_w):
    words = txt.split()
    best = None
    for i in range(1, len(words)):
        a = " ".join(words[:i])
        b = " ".join(words[i:])
        w = max(d.textlength(a, font=font), d.textlength(b, font=font))
        if best is None or w < best[0]:
            best = (w, a, b)
    return best[1], best[2]


def center_sp(frame, txt, font, fill, y, blur=10):
    d = ImageDraw.Draw(frame)
    sp = glow_text(d, None, txt, font, fill, blur)
    x = (frame.width - sp.width) // 2
    band = Image.new("RGBA", (frame.width, sp.height + 8), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    bd.rectangle([0, 0, frame.width - 1, band.height - 1], fill=(5, 6, 10, 175))
    frame.paste(band, (0, y - 4), band)
    frame.paste(sp, (x, y), sp)
    return sp.height


def make(kind):
    src, (W, H), out = OUT[kind]
    frame = fit(src, W, H).convert("RGBA")
    d = ImageDraw.Draw(frame)

    if kind == "916":
        f_pas = ImageFont.truetype(GREAT, 104)
        l1, l2 = wrap2(d, PASSAGE, f_pas, W - 120)
        y = 150
        h1 = center_sp(frame, l1, f_pas, AMBER, y)
        center_sp(frame, l2, f_pas, AMBER, y + h1 + 10)
        yb = H - 260
    elif kind == "carre":
        f_pas = ImageFont.truetype(GREAT, 88)
        l1, l2 = wrap2(d, PASSAGE, f_pas, W - 100)
        y = H // 2 - 130
        h1 = center_sp(frame, l1, f_pas, AMBER, y)
        center_sp(frame, l2, f_pas, AMBER, y + h1 + 6)
        yb = H - 210
    else:
        f_pas = ImageFont.truetype(GREAT, 92)
        l1, l2 = wrap2(d, PASSAGE, f_pas, W - 200)
        y = H // 2 - 120
        h1 = center_sp(frame, l1, f_pas, AMBER, y)
        center_sp(frame, l2, f_pas, AMBER, y + h1 + 8)
        yb = H - 190

    d = ImageDraw.Draw(frame)
    d.rectangle([0, yb - 20, W, H], fill=(5, 6, 10, 205))
    f_aut = ImageFont.truetype(DEJ + "DejaVuSans-Bold.ttf", 64 if kind != "169" else 58)
    aut = "Daïsky Prod"
    d.text(((W - d.textlength(aut, font=f_aut)) / 2, yb), aut, font=f_aut, fill=BLANC + (255,))
    f_sub = ImageFont.truetype(DEJ + "DejaVuSans.ttf", 30)
    sub = "@daiskypro · « Wolof TechStein beat wê ! »"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, yb + 78), sub, font=f_sub, fill=CYAN + (235,))

    frame.paste(badge(d, scale=1.0), (36, 36), badge(d, scale=1.0))
    frame.convert("RGB").save(out, quality=92)
    print("cover ->", out)


for k in OUT:
    make(k)
