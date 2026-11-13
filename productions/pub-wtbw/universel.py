#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Salve « universel » — 10 visuels 1080x1350.
Pas de visage imposé : mains, silhouettes, objets, citations. Tout le monde s'y projette.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, "/home/user/lyric/productions/imelda-13-novembre")
sys.path.insert(0, "/home/user/lyric/productions/pub-wtbw")
import engine as E
import logo as L

OUT = "/home/user/lyric/productions/pub-wtbw"
ASSETS = f"{OUT}/assets"
LIV = f"{OUT}/livrables/universel"
W, H = 1080, 1350


# ───────────────────────── fonds ─────────────────────────
def photo(name, dark=0.52, blur=0.0, zoom=1.0):
    im = Image.open(f"{ASSETS}/{name}").convert("L")
    s = max(W / im.width, H / im.height) * zoom
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x0 = (im.width - W) // 2
    y0 = (im.height - H) // 2
    im = im.crop((x0, y0, x0 + W, y0 + H))
    if blur:
        from PIL import ImageFilter
        im = im.filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(im, dtype=np.float32) / 255.0
    a = a * dark + 0.02
    # vignettage
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.75)) ** 2)
    a = a * (1 - 0.42 * np.clip(r - 0.35, 0, 1) ** 1.6)
    return a


def charcoal():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - H * 0.45) / (H * 0.8)) ** 2)
    return np.clip(0.028 + 0.075 * np.exp(-(r ** 2) * 1.8), 0, 1)


# ───────────────────────── encre ─────────────────────────
def put(f, a, x, y, ink=1.0, op=1.0):
    h, w = a.shape
    ya, yb = max(0, int(y)), min(H, int(y) + h)
    xa, xb = max(0, int(x)), min(W, int(x) + w)
    if ya >= yb or xa >= xb:
        return
    sub = a[ya - int(y):yb - int(y), xa - int(x):xb - int(x)] * op
    f[ya:yb, xa:xb] = f[ya:yb, xa:xb] * (1 - sub) + ink * sub


def line_alpha(txt, kind, size, track, stroke=0, w=W):
    im = Image.new("L", (w, int(size * 1.7)), 0)
    d = ImageDraw.Draw(im)
    fnt = E.font(kind, size)
    tw = E.tracked_width(fnt, txt, track)
    E.draw_tracked(d, ((w - tw) / 2, size * 1.16), txt, fnt, track, fill=255, stroke=stroke)
    return np.asarray(im, dtype=np.float32) / 255.0


def fit(txt, kind, max_size, track_ratio=0.10, maxw=0.80, stroke=0):
    size = max_size
    while size > 10:
        fnt = E.font(kind, size)
        if E.tracked_width(fnt, txt, size * track_ratio) <= W * maxw:
            break
        size = int(size * 0.96)
    return line_alpha(txt, kind, size, size * track_ratio, stroke=stroke), size


def rule(f, y, w=150, op=0.55):
    x0 = int((W - w) / 2)
    f[int(y):int(y) + 2, x0:x0 + w] = 1.0 - (1 - f[int(y):int(y) + 2, x0:x0 + w]) * (1 - op)


def chrome(f, kicker="CITATIONS", idx=None):
    a, _ = fit(kicker, "m", 19, 0.34, maxw=0.5)
    put(f, a[:, :], 60, 74, 1.0, 0.55) if False else None
    # kicker à gauche
    im = Image.new("L", (500, 40), 0)
    d = ImageDraw.Draw(im)
    fnt = E.font("m", 19)
    E.draw_tracked(d, (0, 28), kicker, fnt, 6.5, fill=255)
    ka = np.asarray(im, dtype=np.float32) / 255.0
    put(f, ka, 62, 74, 1.0, 0.6)
    if idx:
        im2 = Image.new("L", (200, 40), 0)
        d2 = ImageDraw.Draw(im2)
        E.draw_tracked(d2, (0, 28), idx, fnt, 6.5, fill=255)
        put(f, np.asarray(im2, np.float32) / 255.0, W - 152, 74, 1.0, 0.6)


def signature(f, y=None):
    sg = L.sigil(64)
    y = H - 150 if y is None else y
    put(f, sg, (W - 64) // 2, y, 1.0, 0.75)


def grain(f, seed=1):
    rng = np.random.default_rng(seed)
    return E.clamp01(f + rng.normal(0, 0.0075, f.shape).astype(np.float32))


def save(f, name):
    os.makedirs(LIV, exist_ok=True)
    p = f"{LIV}/{name}.jpg"
    Image.fromarray((np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)).save(p, quality=94, subsampling=1)
    return p


def quote_card(bg, lines, kicker, idx, sub=None, ink=1.0, y=0.60, sig=True):
    f = bg.copy()
    chrome(f, kicker, idx)
    sizes = []
    for ln, kind, maxs, tr in lines:
        a, s = fit(ln, kind, maxs, tr)
        sizes.append(s)
    base = max(sizes)
    lh = base * 1.22
    total = lh * len(lines)
    y0 = H * y - total / 2
    for i, ((ln, kind, _, tr), s) in enumerate(zip(lines, sizes)):
        a = line_alpha(ln, kind, s, s * tr)
        put(f, a, 0, y0 + i * lh - (s * 0.28), ink, 1.0)
    rule(f, y0 + total + base * 1.30, w=160)
    if sub:
        sa, _ = fit(sub, "m", 27, 0.24, maxw=0.72)
        put(f, sa, 0, y0 + total + base * 1.62, ink, 0.95)
    if sig:
        signature(f, H - (132 if H < 1500 else 420))
    return grain(f), f"{total:.0f}"


SHOTS = []


def build():
    out = []

    # 01 — citation sur mur
    f, _ = quote_card(photo("uni-wall.jpg", dark=0.30), [
        ("TOUT LE MONDE A UNE HISTOIRE.", "pf", 96, 0.02),
        ("PEU DE GENS ONT SON MORCEAU.", "pf", 96, 0.02),
    ], "CITATIONS", "01 / 10", sub="DSKY · WTBW")
    out.append(save(f, "UNI-01-CITATION-HISTOIRE"))

    # 02 — mémoire
    f, _ = quote_card(photo("uni-memoire.jpg", dark=0.46), [
        ("ON NE CHOISIT PAS SA MÉMOIRE.", "pf", 92, 0.02),
        ("ON CHOISIT SA CHANSON.", "pfi", 92, 0.02),
    ], "MÉMOIRE", "02 / 10", sub="POUR CEUX QUI RESTENT")
    out.append(save(f, "UNI-02-CITATION-MEMOIRE"))

    # 03 — mains
    f, _ = quote_card(photo("uni-hands.jpg", dark=0.55), [
        ("LA MUSIQUE NE DEMANDE PAS TON NOM.", "pf", 88, 0.02),
        ("ELLE DEMANDE TON CŒUR.", "pfi", 88, 0.02),
    ], "FÊTE", "03 / 10", sub="DSKY · WTBW")
    out.append(save(f, "UNI-03-CITATION-COEUR"))

    # 04 — universel, silhouette
    f, _ = quote_card(photo("uni-silhouette.jpg", dark=0.58), [
        ("HOMME. FEMME. ENFANT.", "pf", 100, 0.04),
        ("LA MÊME ÉMOTION.", "pfi", 100, 0.04),
    ], "UNIVERSEL", "04 / 10", sub="UNE CHANSON POUR CHACUN", y=0.31)
    out.append(save(f, "UNI-04-UNIVERSEL-EMOTION"))

    # 05 — âges
    f, _ = quote_card(photo("uni-hands.jpg", dark=0.48, zoom=1.25), [
        ("8 ANS OU 80 ANS.", "pf", 104, 0.03),
        ("LE MÊME FRISSON.", "pfi", 104, 0.03),
    ], "UNIVERSEL", "05 / 10", sub="DE LA PREMIÈRE FÊTE À LA DERNIÈRE")
    out.append(save(f, "UNI-05-UNIVERSEL-AGES"))

    # 06 — clip 9:16
    f, _ = quote_card(photo("uni-phone.jpg", dark=0.46), [
        ("TON MORCEAU", "pf", 116, 0.03),
        ("TON CLIP 9:16", "pfi", 116, 0.03),
    ], "SERVICES", "06 / 10", sub="ÉCRIT · COMPOSÉ · ENREGISTRÉ · FILMÉ", y=0.50)
    out.append(save(f, "UNI-06-SERVICE-CLIP"))

    # 07 — dans ta poche
    f, _ = quote_card(photo("uni-studio.jpg", dark=0.46), [
        ("TON HISTOIRE", "pf", 112, 0.03),
        ("DANS TA POCHE.", "pfi", 112, 0.03),
    ], "SUR MESURE", "07 / 10", sub="UN MORCEAU QUI T'APPARTIENT", y=0.50)
    out.append(save(f, "UNI-07-SERVICE-POCHE"))

    # 08 — les quatre piliers (typographique)
    f = charcoal()
    chrome(f, "LE MÉTIER", "08 / 10")
    a, _ = fit("ÉDUCATEUR · PAROLIER", "pf", 78, 0.04, maxw=0.86)
    put(f, a, 0, 330)
    a, _ = fit("COMPOSITEUR · PRODUCTEUR", "pf", 78, 0.04, maxw=0.86)
    put(f, a, 0, 470)
    rule(f, 640, 200)
    for i, (t, s) in enumerate([
        ("J'ÉCRIS À PARTIR DE CE QUE TU VIS.", "ÉCRITURE"),
        ("JE COMPOSE, J'ENREGISTRE, JE FILME.", "PRODUCTION"),
        ("J'EXPLIQUE, JE TRANSMETS.", "ÉDUCATION"),
    ]):
        a, _ = fit(t, "pfi", 40, 0.02, maxw=0.80)
        put(f, a, 0, 720 + i * 140, 1.0, 0.92)
    signature(f, H - 150)
    out.append(save(grain(f), "UNI-08-METIER"))

    # 09 — badge universel
    f = photo("uni-wall.jpg", dark=0.36, zoom=1.15)
    b = L.badge(560)
    put(f, b, (W - 560) // 2, 330, 1.0, 0.95)
    a, _ = fit("UNE SEULE PASTILLE.", "pf", 74, 0.05, maxw=0.9)
    put(f, a, 0, 980, 1.0, 1.0)
    a2, _ = fit("PARTOUT.", "pfi", 74, 0.05, maxw=0.9)
    put(f, a2, 0, 1060, 1.0, 1.0)
    out.append(save(grain(f), "UNI-09-BADGE"))

    # 10 — manifeste (lettrage)
    f = charcoal()
    chrome(f, "MANIFESTE", "10 / 10")
    blk = L.type_block(int(W * 0.70))
    put(f, blk, (W - blk.shape[1]) // 2, 215, 1.0, 1.0)
    rule(f, 985, 160)
    a, _ = fit("POUR TOUT LE MONDE.", "pfi", 54, 0.03, maxw=0.86)
    put(f, a, 0, 1010, 1.0, 0.95)
    a2, _ = fit("COMME UNE CHANSON.", "pfi", 54, 0.03, maxw=0.86)
    put(f, a2, 0, 1080, 1.0, 0.95)
    out.append(save(grain(f), "UNI-10-MANIFESTE"))
    return out


if __name__ == "__main__":
    for p in build():
        print(p)
