#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Variations — 10 visuels 1080x1350 en duotone laiton (chaud), layouts différents.
Série « or » : photos chaudes, chiffres géants, citation à gauche, frise, annonce.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, "/home/user/lyric/productions/imelda-13-novembre")
sys.path.insert(0, "/home/user/lyric/productions/pub-wtbw")
import engine as E  # noqa: E402
import universel as U  # noqa: E402

OUT = "/home/user/lyric/productions/pub-wtbw"
LIV = f"{OUT}/livrables/variations"
W, H = 1080, 1350
SH = np.array([0.055, 0.043, 0.030], dtype=np.float32)
HI = np.array([0.955, 0.905, 0.800], dtype=np.float32)
ACC = np.array([0.784, 0.631, 0.420], dtype=np.float32)
INK = np.array([0.965, 0.940, 0.890], dtype=np.float32)


def duotone(g):
    g = np.clip(g, 0, 1)[..., None]
    g = g ** 1.06
    return SH + g * (HI - SH)


def photo(name, dark=0.46):
    old = U.H
    try:
        U.H = H
        g = U.photo(f"{name}.jpg", dark=dark)
    finally:
        U.H = old
    return duotone(g)


def charcoal():
    old = U.H
    try:
        U.H = H
        g = U.charcoal()
    finally:
        U.H = old
    return duotone(g)


def put(f, a, x, y, color=INK, op=1.0, shadow=0.0):
    h, w = a.shape
    ya, yb = max(0, int(y)), min(H, int(y) + h)
    xa, xb = max(0, int(x)), min(W, int(x) + w)
    if ya >= yb or xa >= xb:
        return
    sub = a[ya - int(y):yb - int(y), xa - int(x):xb - int(x)]
    if shadow > 0:
        from PIL import ImageFilter
        bl = Image.fromarray((sub * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9))
        sa = (np.asarray(bl, dtype=np.float32) / 255.0 * shadow)[..., None]
        f[ya:yb, xa:xb] = f[ya:yb, xa:xb] * (1 - np.clip(sa * 1.6, 0, 0.92))
    s = (sub * op)[..., None]
    f[ya:yb, xa:xb] = f[ya:yb, xa:xb] * (1 - s) + color * s


def text_a(txt, kind, size, track, align="center", x=0, maxw=W):
    im = Image.new("L", (maxw, int(size * 1.8)), 0)
    d = ImageDraw.Draw(im)
    fnt = E.font(kind, size)
    tw = E.tracked_width(fnt, txt, track)
    if align == "center":
        px = (maxw - tw) / 2
    elif align == "right":
        px = maxw - tw - x
    else:
        px = x
    E.draw_tracked(d, (px, size * 1.16), txt, fnt, track, fill=255)
    return np.asarray(im, dtype=np.float32) / 255.0


def fit(txt, kind, size, track_r, align="center", x=0, maxw=0.84, min_size=14):
    s = size
    while s > min_size:
        fnt = E.font(kind, s)
        if E.tracked_width(fnt, txt, s * track_r) <= W * maxw:
            break
        s = int(s * 0.95)
    if align == "center":
        return text_a(txt, kind, s, s * track_r, "center", 0, W), s
    return text_a(txt, kind, s, s * track_r, "left", x, W), s


def rule(f, y, w=150, op=0.6, x=None, color=ACC):
    x0 = int(x if x is not None else (W - w) / 2)
    f[int(y):int(y) + 2, x0:x0 + w] = f[int(y):int(y) + 2, x0:x0 + w] * (1 - op) + color * op


def kicker(f, txt, idx, color=INK, op=0.55):
    im = Image.new("L", (520, 44), 0)
    d = ImageDraw.Draw(im)
    fnt = E.font("m", 19)
    E.draw_tracked(d, (0, 30), txt, fnt, 6.5, fill=255)
    put(f, np.asarray(im, np.float32) / 255.0, 60, 74, color, op)
    if idx:
        im2 = Image.new("L", (240, 44), 0)
        d2 = ImageDraw.Draw(im2)
        E.draw_tracked(d2, (0, 30), idx, fnt, 6.5, fill=255)
        put(f, np.asarray(im2, np.float32) / 255.0, W - 200, 74, color, op)


def sig(f, y=None):
    from logo import sigil
    s = sigil(66)
    put(f, s, (W - 66) // 2, H - 170 if y is None else y, ACC, 0.9)


def save(f, name):
    os.makedirs(LIV, exist_ok=True)
    p = f"{LIV}/{name}.jpg"
    f = E.clamp01(f + np.random.default_rng(len(name)).normal(0, 0.006, f.shape).astype(np.float32))
    Image.fromarray((f * 255 + 0.5).astype(np.uint8)).save(p, quality=94, subsampling=1)
    return p


def band(f, yc, spread=0.16, depth=0.45):
    yy = np.arange(H, dtype=np.float32) / H
    k = 1 - depth * np.exp(-((yy - yc) ** 2) / (2 * spread ** 2))
    f *= k[:, None, None]
    return f


def center_card(bg, lines, kicker_txt, idx, sub=None, y=0.55, depth=0.62):
    f = band(bg.copy(), y, 0.19, depth)
    kicker(f, kicker_txt, idx)
    sizes = [fit(ln[0], ln[1], ln[2], 0.03)[1] for ln in lines]
    base = max(sizes)
    lh = base * 1.26
    total = lh * len(lines)
    y0 = H * y - total / 2
    for i, (ln, a) in enumerate(zip(lines, sizes)):
        t = text_a(ln[0], ln[1], sizes[i], sizes[i] * 0.03)
        put(f, t, 0, y0 + i * lh - base * 0.28, shadow=0.85)
    rule(f, y0 + total + base * 1.28)
    if sub:
        s, _ = fit(sub, "m", 26, 0.22, maxw=0.72)
        put(f, s, 0, y0 + total + base * 1.60, ACC, 0.95)
    sig(f)
    return f


def left_card(bg, lines, kicker_txt, idx, sub=None):
    f = band(bg.copy(), 0.50, 0.24, 0.55)
    kicker(f, kicker_txt, idx)
    # gros guillemet
    q = fit("“", "pf", 220, 0.0, "center", maxw=0.2)[0]
    put(f, q, -330, 210, ACC, 0.5)
    y = 560
    for ln, kind, size in lines:
        a, s = fit(ln, kind, size, 0.03, "left", 84, maxw=0.84)
        put(f, a, 84, y - 40, shadow=0.85)
        y += int(s * 1.32)
    rule(f, y + 20, 140, 0.7, x=84)
    if sub:
        s, _ = fit(sub, "m", 25, 0.22, "left", 84, maxw=0.7)
        put(f, s, 84, y + 56, ACC, 0.95)
    sig(f)
    return f


def numeral_card(n, label, sub, idx):
    f = charcoal()
    kicker(f, "LE CATALOGUE", idx)
    a, s = fit(n, "pf", 640, 0.0, "center", maxw=0.9)
    put(f, a, 0, 250, INK, 1.0, shadow=0.5)
    l, _ = fit(label, "m", 34, 0.26, maxw=0.8)
    put(f, l, 0, 250 + int(s * 1.34), INK, 0.85)
    rule(f, 250 + int(s * 1.34) + 90, 200)
    sb, _ = fit(sub, "pfi", 42, 0.02, maxw=0.78)
    put(f, sb, 0, 250 + int(s * 1.34) + 140, INK, 0.9)
    sig(f, H - 190)
    return f


def timeline_card(idx):
    f = charcoal()
    kicker(f, "COMMENT ÇA MARCHE", idx)
    t, _ = fit("DE TON IDÉE À TON MORCEAU", "pf", 84, 0.03, maxw=0.86)
    put(f, t, 0, 210, shadow=0.9)
    steps = [("01", "TU ME DIS L'OCCASION", "mariage, anniversaire, hommage, fête"),
             ("02", "J'ÉCRIS LE TEXTE", "tes prénoms, tes dates, ton histoire"),
             ("03", "JE COMPOSE ET J'ENREGISTRE", "voix, beat, mixage"),
             ("04", "TU REÇOIS TON MORCEAU", "fichier audio + clip 9:16")]
    y = 430
    for num, t1, t2 in steps:
        a, s = fit(num, "pf", 60, 0.0, "left", 84, maxw=0.2)
        put(f, a, 84, y - 20, ACC, 0.95)
        b, _ = fit(t1, "m", 27, 0.20, "left", 210, maxw=0.72)
        put(f, b, 210, y - 12, INK, 1.0)
        c, _ = fit(t2, "pfi", 26, 0.02, "left", 210, maxw=0.72)
        put(f, c, 210, y + 40, ACC, 0.85)
        rule(f, y + 96, 120, 0.35, x=210)
        y += 190
    sig(f, H - 160)
    return f


def main():
    out = []
    # 1 — album
    out.append(save(center_card(photo("var-album", 0.46), [
        ("CE QUE LES PHOTOS NE DISENT PAS,", "pf", 76),
        ("LA CHANSON LE CHANTE.", "pfi", 76),
    ], "MÉMOIRE", "01 / 10", sub="POUR CEUX QUI RESTENT", y=0.52, depth=0.68), "VAR-01-ALBUM"))
    # 2 — danse
    out.append(save(center_card(photo("var-danse", 0.52), [
        ("PREMIER REGARD.", "pf", 88),
        ("PREMIÈRE DANSE.", "pf", 88),
        ("PREMIÈRE CHANSON.", "pfi", 88),
    ], "MARIAGE", "02 / 10", sub="SUR MESURE", y=0.52), "VAR-02-DANSE"))
    # 3 — enfants
    out.append(save(center_card(photo("var-enfants", 0.50), [
        ("UN MORCEAU QU'ILS ÉCOUTERONT", "pf", 74),
        ("DANS VINGT ANS.", "pfi", 74),
    ], "ANNIVERSAIRE", "03 / 10", sub="POUR UN ENFANT, POUR TOUJOURS", y=0.55, depth=0.7), "VAR-03-ENFANTS"))
    # 4 — guitare
    out.append(save(center_card(photo("var-guitare", 0.44), [
        ("TON NOM", "pf", 96),
        ("DANS LE REFRAIN.", "pfi", 96),
    ], "SUR MESURE", "04 / 10", sub="LE PRÉNOM, LA DATE, L'HISTOIRE", y=0.50), "VAR-04-GUITARE"))
    # 5 — salle
    out.append(save(center_card(photo("var-salle", 0.52), [
        ("LE PUBLIC NE CONNAÎT PAS", "pf", 72),
        ("TON NOM. IL CONNAÎT TA CHANSON.", "pfi", 72),
    ], "SCÈNE", "05 / 10", sub="DSKY · WTBW", y=0.50, depth=0.72), "VAR-05-SALLE"))
    # 6 — chiffre
    out.append(save(numeral_card("34", "MORCEAUX ÉCRITS, COMPOSÉS, MIXÉS",
                                 "un seul homme, une seule signature", "06 / 10"), "VAR-06-34"))
    # 7 — citation à gauche
    out.append(save(left_card(photo("var-album", 0.34), [
        ("LA CHANSON N'EFFACE PAS", "pf", 70),
        ("LA DOULEUR.", "pfi", 70),
        ("ELLE LA PORTE AVEC TOI.", "pfi", 56),
    ], "MÉMOIRE", "07 / 10", sub="POUR CEUX QUI RESTENT"), "VAR-07-CITATION"))
    # 8 — frise
    out.append(save(timeline_card("08 / 10"), "VAR-08-FRISE"))
    # 9 — merci
    out.append(save(center_card(photo("var-guitare", 0.30), [
        ("MERCI À CEUX QUI ÉCOUTENT", "pf", 74),
        ("ENCORE EN BOUCLE.", "pfi", 74),
    ], "MERCI", "09 / 10", sub="34 MORCEAUX, ET CE N'EST QUE LE DÉBUT", y=0.52, depth=0.7), "VAR-09-MERCI"))
    # 10 — annonce (réutilisable)
    f = charcoal()
    kicker(f, "PROCHAIN MORCEAU", "10 / 10")
    a, _ = fit("LE PROCHAIN", "pf", 96, 0.04, maxw=0.86)
    put(f, a, 0, 380)
    b, _ = fit("S'APPELLE…", "pfi", 96, 0.04, maxw=0.86)
    put(f, b, 0, 500)
    for i, xx in enumerate(range(200, 880, 40)):
        f[700:702, xx:xx + 24] = f[700:702, xx:xx + 24] * 0.4 + ACC * 0.6
    c, _ = fit("DATE DE SORTIE", "m", 22, 0.28, maxw=0.6)
    put(f, c, 0, 726, INK, 0.45)
    d, _ = fit("TIKTOK & YOUTUBE — @DSKYWTBW", "m", 24, 0.24, maxw=0.78)
    put(f, d, 0, H - 260, ACC, 0.9)
    sig(f, H - 180)
    out.append(save(f, "VAR-10-ANNONCE"))
    return out


if __name__ == "__main__":
    for p in main():
        print(p)
