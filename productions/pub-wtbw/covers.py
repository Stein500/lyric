#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pochettes de morceaux DSKY · WTBW — 1080x1080.
Système unique : fond (photo N&B ou charbon), titre serif, accroche italique, pastille + baseline.
`python3 covers.py` produit les 10 pochettes vedettes ; `--all` les 34 du catalogue.
"""
import os
import sys
import unicodedata

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, "/home/user/lyric/productions/imelda-13-novembre")
sys.path.insert(0, "/home/user/lyric/productions/pub-wtbw")
import engine as E  # noqa: E402
import logo as L  # noqa: E402
import universel as U  # noqa: E402

OUT = "/home/user/lyric/productions/pub-wtbw"
LIV = f"{OUT}/livrables/pochettes"
S = 1080

# (titre, accroche, fond)
HERO = [
    ("NOUKIKO TCHÉ WÊ", "c'est mon sourire à moi", "cov-light"),
    ("MONSTER POSITIVE", "they called it a curse, I called it power", "cov-bokeh"),
    ("NAN YI A GA DJIN WÊ", "j'irai au sommet", "cov-road"),
    ("GBÈTCHÉ VIVI", "ma vie me plaît, je suis béni", "cov-silk"),
    ("MAHU TI TÈ GBÈ", "God is always there", "cov-water"),
    ("TU ES TROP BELLE", "j'ai la trouille, c'est fou", "cov-silk"),
    ("SANGUIN", "le sang dans les veines", "cov-bokeh"),
    ("ON NOUS A VOLÉ NOTRE ÉDUCATION", "on se relève", "cov-road"),
    ("CONCENTRÉ SUR LE CHEMIN", "je regarde plus en arrière", "cov-light"),
    ("LE SURVIVANT", "toujours debout", None),
]

ALL = [
    "NOUKIKO TCHÉ WÊ", "AYON DÈKPÈ", "TU ES TROP BELLE", "MONSTER POSITIVE",
    "JE ME RELÈVE TOUJOURS", "GBÈTCHÉ VIVI", "NAN YI A GA DJIN WÊ",
    "CONCENTRÉ SUR LE CHEMIN", "SANGUIN", "ON NOUS A VOLÉ NOTRE ÉDUCATION",
    "ÇA MONTE, ÇA DESCEND", "LE GOÛT BON DE LA VIE", "MAHU TI TÈ GBÈ", "VIVI O O R",
    "GLACE", "GOINFRES", "GRAND MARCHEUR", "MASQUE", "GHOST U SEE", "NONVI KONOU",
    "YAFOY", "LE SURVIVANT", "JE SUIS PAUVRE ET RICHE", "TESTOSTÉRONE",
    "JE CRACHE LES DÉMONS", "DÈS LE DÉBUT", "ENTRE TES MAINS", "CALM IN OFF DOWN",
    "DRAGUE MOI", "JE M'AIME TELLEMENT", "SEUL DANS MA TÊTE", "L'AMOUR EST LA RÉPONSE",
    "MOTIVÉ", "WOLOF TECHSTEIN — ESSAIE",
]


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = "".join(c if c.isalnum() else "-" for c in t.upper())
    while "--" in t:
        t = t.replace("--", "-")
    return t.strip("-")[:38]


def cover_bg(name=None, dark=0.44):
    """photo -> carré 1080 (ou charbon si pas de photo)."""
    old_h = U.H
    try:
        U.H = S
        f = U.photo(f"{name}.jpg", dark=dark) if name else U.charcoal()
    finally:
        U.H = old_h
    return f


def text_alpha_box(txt, kind, size, track, w=S):
    im = Image.new("L", (w, int(size * 1.7)), 0)
    d = ImageDraw.Draw(im)
    fnt = E.font(kind, size)
    tw = E.tracked_width(fnt, txt, track)
    E.draw_tracked(d, ((w - tw) / 2, size * 1.14), txt, fnt, track, fill=255)
    return np.asarray(im, dtype=np.float32) / 255.0


def fit(txt, kind, max_size, track_ratio=0.04, maxw=0.84):
    size = max_size
    while size > 12:
        fnt = E.font(kind, size)
        if E.tracked_width(fnt, txt, size * track_ratio) <= S * maxw:
            break
        size = int(size * 0.95)
    return text_alpha_box(txt, kind, size, size * track_ratio), size


def wrap_title(title, max_size=150, maxw=0.86):
    """coupe le titre en 1-3 lignes équilibrées."""
    words = title.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        a, s = fit(test, "pf", max_size, 0.03, maxw)
        if s >= max_size * 0.55 or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def make(title, hook, bgname, idx=0):
    f = cover_bg(bgname)
    # bande sombre derrière le texte pour garantir le contraste
    yy = np.arange(S, dtype=np.float32)[:, None]
    band = 0.55 + 0.45 * np.abs(yy - S * 0.52) / (S * 0.30)
    f = f * np.clip(band, 0.55, 1.0)
    if not bgname:
        f = f.copy()
    # cadre + mentions
    U.chrome(f, "DSKY · WTBW", None)

    lines = wrap_title(title)
    sizes = [fit(ln, "pf", 132, 0.03, 0.86)[1] for ln in lines]
    base = min(sizes)
    lh = base * 1.16
    total = lh * len(lines)
    y0 = S * 0.50 - total / 2
    for i, ln in enumerate(lines):
        a = text_alpha_box(ln, "pf", sizes[i], sizes[i] * 0.03)
        U.put(f, a, 0, y0 + i * lh - base * 0.30, 1.0, 1.0)
    yb = y0 + total + base * 0.72
    U.rule(f, yb, 150)

    if hook:
        ha, _ = fit(hook, "pfi", 40, 0.02, 0.78)
        U.put(f, ha, 0, yb + 44, 1.0, 0.95)

    # pastille + baseline en bas
    sg = L.sigil(84)
    U.put(f, sg, (S - 84) // 2, S - 200, 1.0, 0.88)
    bl, _ = fit("WOLOF TECHSTEIN BEAT WÊ", "m", 22, 0.28, 0.66)
    U.put(f, bl, 0, S - 98, 1.0, 0.8)

    f = E.clamp01(f + np.random.default_rng(11 + idx).normal(0, 0.006, f.shape))
    return f


def save(f, title, idx, sub=""):
    d = f"{LIV}/{sub}" if sub else LIV
    os.makedirs(d, exist_ok=True)
    name = f"POCHE-{idx:02d}-{slug(title)}-1080.jpg"
    p = f"{d}/{name}"
    Image.fromarray((np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)).save(p, quality=94, subsampling=1)
    return p


if __name__ == "__main__":
    if "--all" in sys.argv:
        bgs = [None, "cov-light", "cov-bokeh", "cov-road", "cov-silk", "cov-water"]
        for i, t in enumerate(ALL, 1):
            bg = bgs[i % len(bgs)]
            print(save(make(t, None, bg, i), t, i, sub="catalogue"))
    else:
        for i, (t, h, bg) in enumerate(HERO, 1):
            print(save(make(t, h, bg, i), t, i))
