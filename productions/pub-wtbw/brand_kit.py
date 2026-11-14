#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kit de marque DSKY · WTBW — 10 visuels 1080x1350.
Décors/mockups générés par IA (vierges), sigle + lettrage posés par le moteur.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, "/home/user/lyric/productions/imelda-13-novembre")
import engine as E
import logo as L

OUT = "/home/user/lyric/productions/pub-wtbw"
ASSETS = f"{OUT}/assets"
LIV = f"{OUT}/livrables/brand"
W, H = 1080, 1350


def load(p):
    im = Image.open(p).convert("L")
    return np.asarray(im, dtype=np.float32) / 255.0


def to_1080x1350(a):
    im = Image.fromarray((a * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
    return np.asarray(im, dtype=np.float32) / 255.0


def star(d, cx, cy, r, fill=255):
    pts = []
    for k in range(10):
        ang = -np.pi / 2 + k * np.pi / 5
        rr = r if k % 2 == 0 else r * 0.42
        pts.append((cx + rr * np.cos(ang), cy + rr * np.sin(ang)))
    d.polygon(pts, fill=fill)


def sigil(size):
    """sigle DSKY·WTBW dessiné au trait : anneau + W + étoile. Reproductible, imprimable."""
    S = 2048
    img = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(img)
    c = S / 2
    # anneau double
    d.ellipse([c - S * 0.478, c - S * 0.478, c + S * 0.478, c + S * 0.478],
              outline=255, width=int(S * 0.014))
    d.ellipse([c - S * 0.436, c - S * 0.436, c + S * 0.436, c + S * 0.436],
              outline=150, width=int(S * 0.006))
    # W central
    wdt = int(S * 0.072)
    p = [(-0.245, -0.135), (-0.120, 0.150), (0.000, -0.055), (0.120, 0.150), (0.245, -0.135)]
    pts = [(c + x * S, c + y * S) for x, y in p]
    d.line(pts, fill=255, width=wdt, joint="curve")
    for q in pts[:1] + pts[-1:]:
        d.ellipse([q[0] - wdt / 2, q[1] - wdt / 2, q[0] + wdt / 2, q[1] + wdt / 2], fill=255)
    # barre de mesure + étoile
    d.line([(c - S * 0.150, c + S * 0.265), (c + S * 0.150, c + S * 0.265)],
           fill=210, width=int(S * 0.009))
    star(d, c, c + S * 0.345, S * 0.042)
    img = img.resize((size, size), Image.LANCZOS)
    return np.asarray(img, dtype=np.float32) / 255.0


def word_block_deprecated(width, dark=False, with_emblem=True, emblem_ratio=0.42):
    """bloc de marque : sigle + DSKY + WTBW + baseline. Renvoie (alpha, hauteur)."""
    Wb = width
    eh = int(Wb * emblem_ratio) if with_emblem else 0
    hh = int(Wb * 0.30)
    sh = int(Wb * 0.09)
    bh = int(Wb * 0.075)
    total = eh + int(Wb * 0.06) + hh + int(Wb * 0.02) + sh + int(Wb * 0.035) + int(Wb * 0.10)
    canvas = Image.new("L", (Wb, total), 0)
    d = ImageDraw.Draw(canvas)
    y = 0
    if with_emblem:
        em = sigil(eh)
        emi = Image.fromarray((em * 255).astype(np.uint8))
        canvas.paste(emi, ((Wb - eh) // 2, 0))
        y += eh + int(Wb * 0.06)

    # DSKY
    fnt = E.font("pf", hh)
    tr = hh * 0.16
    tw = E.tracked_width(fnt, "DSKY", tr)
    E.draw_tracked(d, (Wb / 2 - tw / 2, y + hh * 0.78), "DSKY", fnt, tr, fill=255)
    y += hh + int(Wb * 0.02)

    # WTBW
    fnt2 = E.font("m", sh)
    tw2 = E.tracked_width(fnt2, "WTBW", sh * 0.30)
    E.draw_tracked(d, (Wb / 2 - tw2 / 2, y + sh * 0.78), "WTBW", fnt2, sh * 0.30, fill=255, stroke=1)
    y += sh + int(Wb * 0.035)

    # baseline
    txt = "WOLOF TECHSTEIN BEAT WÊ · BÉNIN"
    bh = int(Wb * 0.075)
    while True:
        fnt3 = E.font("m", bh)
        tw3 = E.tracked_width(fnt3, txt, bh * 0.20)
        if tw3 <= Wb * 0.86 or bh < 9:
            break
        bh = int(bh * 0.94)
    E.draw_tracked(d, (Wb / 2 - tw3 / 2, y + bh * 0.8), txt, fnt3, bh * 0.20, fill=255)
    return np.asarray(canvas, dtype=np.float32) / 255.0


def word_block(width, dark=False, with_emblem=True, emblem_ratio=0.42):
    return L.stack(width) if with_emblem else L.type_block(width)


def paste(frame, alpha_img, x, y, ink=1.0, strength=1.0, shade=True):
    """pose une encre : ink=1 (blanc) ou 0 (noir)."""
    h, w = alpha_img.shape
    ya, yb = max(0, y), min(H, y + h)
    xa, xb = max(0, x), min(W, x + w)
    if ya >= yb or xa >= xb:
        return
    a = alpha_img[ya - y:yb - y, xa - x:xb - x] * strength
    if shade:
        # l'encre suit légèrement l'ombre du support (rendu sérigraphie)
        local = frame[ya:yb, xa:xb]
        tint = ink * (0.78 + 0.22 * local)
        frame[ya:yb, xa:xb] = local * (1 - a) + tint * a
    else:
        frame[ya:yb, xa:xb] = frame[ya:yb, xa:xb] * (1 - a) + ink * a


def grain(f, seed):
    rng = np.random.default_rng(seed)
    return E.clamp01(f + rng.normal(0, 0.008, f.shape))


def make_logo_sheet():
    """planche identité — seul visuel avec l'accent Bénin en couleur."""
    f = np.full((H, W), 0.035, dtype=np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt((xx - W / 2) ** 2 + (yy - H * 0.42) ** 2) / (W * 0.85)
    f += 0.10 * np.exp(-(r ** 2) * 2.0)

    blk = word_block(int(W * 0.56), with_emblem=True)
    paste(f, blk, int((W - blk.shape[1]) / 2), int(H * 0.075), ink=1.0, strength=1.0, shade=False)

    # filet + drapeau du Bénin (accent unique)
    f[int(H * 0.835), 140:W - 140] = 0.35
    rgb = np.stack([f] * 3, axis=-1)
    fx, fy, fw, fh = 460, 1060, 160, 100
    rgb[fy:fy + fh, fx:fx + fw // 3] = np.array([0.0, 0.53, 0.27])       # vert
    rgb[fy:fy + fh // 2, fx + fw // 3:fx + fw] = np.array([0.99, 0.82, 0.09])  # jaune
    rgb[fy + fh // 2:fy + fh, fx + fw // 3:fx + fw] = np.array([0.91, 0.16, 0.16])  # rouge
    rgb = E.clamp01(rgb + np.random.default_rng(3).normal(0, 0.006, rgb.shape).astype(np.float32))

    out = f"{LIV}/BRAND-01-LOGO-1080x1350.jpg"
    Image.fromarray((rgb * 255 + 0.5).astype(np.uint8)).save(out, quality=95, subsampling=1)
    return out


ITEMS = [
    dict(src="merch-02-tshirt.jpg", out="BRAND-02-TSHIRT", x=0.50, y=0.415, w=0.255, ink=1.0),
    dict(src="merch-03-hoodie.jpg", out="BRAND-03-HOODIE", x=0.487, y=0.455, w=0.215, ink=1.0),
    dict(src="merch-04-tote.jpg", out="BRAND-04-TOTE", x=0.50, y=0.50, w=0.26, ink=0.06),
    dict(src="merch-05-cap.jpg", out="BRAND-05-CAP", x=0.44, y=0.455, w=0.115, ink=1.0),
    dict(src="merch-06-sneakers.jpg", out="BRAND-06-SNEAKERS", x=0.330, y=0.578, w=0.105, ink=0.12),
    dict(src="merch-07-bag.jpg", out="BRAND-07-BAG", x=0.600, y=0.520, w=0.115, ink=0.92, emblem=False),
    dict(src="merch-08-stickers.jpg", out="BRAND-08-STICKERS", x=0.155, y=0.245, w=0.085, ink=0.08, emblem=True, only=True),
    dict(src="merch-09-cards.jpg", out="BRAND-09-CARDS", x=0.478, y=0.632, w=0.128, ink=0.95, emblem=False),
    dict(src="merch-10-vinyl.jpg", out="BRAND-10-VINYL", x=0.22, y=0.44, w=0.22, ink=1.0),
]


def make_item(it, idx):
    f = to_1080x1350(load(f"{ASSETS}/{it['src']}"))
    bw = int(W * it["w"])
    if it.get("only"):
        blk = sigil(bw)
    else:
        blk = word_block(bw, with_emblem=it.get("emblem", True))
    x = int(W * it["x"] - bw / 2)
    y = int(H * it["y"] - blk.shape[0] / 2)
    paste(f, blk, x, y, ink=it["ink"], strength=0.92, shade=it["ink"] > 0.5)
    # marque discrète en pied d'image
    tag = np.zeros((H, W), dtype=np.float32)
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    fnt = E.font("m", 22)
    txt = "DSKY · WTBW"
    tw = E.tracked_width(fnt, txt, 9)
    E.draw_tracked(d, (W / 2 - tw / 2, H - 60), txt, fnt, 9, fill=255)
    tag = np.asarray(im, dtype=np.float32) / 255.0
    f = E.composite(f, tag, 0.92, 0.45)
    f = grain(f, 60 + idx)
    out = f"{LIV}/{it['out']}-1080x1350.jpg"
    Image.fromarray((f * 255 + 0.5).astype(np.uint8)).save(out, quality=94, subsampling=1)
    return out


def print_files_stein():
    """variante « état civil » : DSKY WTBW + C. JÉSUTONDJI SAMUEL STEIN."""
    os.makedirs(f"{LIV}/print", exist_ok=True)
    blk = L.stack_stein(2400)
    a = Image.fromarray((blk * 255).astype(np.uint8))
    rgba = Image.new("RGBA", a.size, (255, 255, 255, 0))
    rgba.putalpha(a)
    rgba.save(f"{LIV}/print/DSKY-WTBW-lockup-STEIN-blanc-2400px.png")
    rgba2 = Image.new("RGBA", a.size, (0, 0, 0, 0))
    rgba2.putalpha(Image.fromarray(((1 - blk) * 255).astype(np.uint8)))
    rgba2.save(f"{LIV}/print/DSKY-WTBW-lockup-STEIN-noir-2400px.png")
    return "stein ok " + str(a.size)


def print_files():
    """fichiers prêts à imprimer : PNG transparents haute résolution + SVG."""
    os.makedirs(f"{LIV}/print", exist_ok=True)
    # 1. lockup vertical (sigle + DSKY + WTBW + baseline) 3000 px
    blk = word_block(2400, with_emblem=True)
    a = Image.fromarray((blk * 255).astype(np.uint8))
    rgba = Image.new("RGBA", a.size, (255, 255, 255, 0))
    rgba.putalpha(a)
    rgba.save(f"{LIV}/print/DSKY-WTBW-lockup-blanc-2400px.png")
    blk2 = np.asarray(Image.fromarray(((1 - blk) * 255).astype(np.uint8)))
    rgba2 = Image.new("RGBA", (blk2.shape[1], blk2.shape[0]), (0, 0, 0, 0))
    rgba2.putalpha(Image.fromarray(blk2))
    rgba2.save(f"{LIV}/print/DSKY-WTBW-lockup-noir-2400px.png")
    # 2. sigle seul 2000 px
    sg = sigil(2000)
    r = Image.new("RGBA", (2000, 2000), (255, 255, 255, 0))
    r.putalpha(Image.fromarray((sg * 255).astype(np.uint8)))
    r.save(f"{LIV}/print/DSKY-WTBW-sigle-blanc-2000px.png")
    # 3. SVG vectoriel du sigle (imprimeur / broderie)
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-500 -500 1000 1000" width="1000" height="1000">
  <g fill="none" stroke="#000" stroke-width="14">
    <circle r="478"/><circle r="436" stroke-width="6" stroke-opacity=".6"/>
  </g>
  <polyline points="-245,-135 -120,150 0,-55 120,150 245,-135" fill="none" stroke="#000"
            stroke-width="72" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="-150" y1="265" x2="150" y2="265" stroke="#000" stroke-width="9" stroke-opacity=".85"/>
  <polygon points="0,303 8,323 30,325 13,339 18,361 0,349 -18,361 -13,339 -30,325 -8,323" fill="#000"/>
</svg>
"""
    open(f"{LIV}/print/DSKY-WTBW-sigle.svg", "w").write(svg)
    return "print ok"


if __name__ == "__main__":
    os.makedirs(LIV, exist_ok=True)
    print(make_logo_sheet())
    for i, it in enumerate(ITEMS, 2):
        print(make_item(it, i))
    print(print_files())
