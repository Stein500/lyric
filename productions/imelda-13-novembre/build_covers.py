#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Couvertures TikTok 1080x1920 (une par film) — même langage que les films."""
import os

import numpy as np
from PIL import Image, ImageDraw

import engine as E

P = "IMG-20261111-WA"
COVERS = [
    dict(photo="0031", out="COVER-01-NOUKIKO-1080x1920.jpg", sub="NOUKIKO TCHÉ WÊ", cy=0.30),
    dict(photo="0043", out="COVER-02-AYON-DEKPE-1080x1920.jpg", sub="AYON DÈKPÈ", cy=0.18),
    dict(photo="0066", out="COVER-03-TROP-BELLE-1080x1920.jpg", sub="TU ES TROP BELLE", cy=0.34),
]


def build(c, idx):
    a = E.load_photo(f"{E.ROOT}/{P}{c['photo']}.jpg")
    h, w = a.shape
    s = max(E.W / w, E.H / h) * 1.06
    im = Image.fromarray((a * 255).astype(np.uint8)).resize(
        (int(w * s), int(h * s)), Image.LANCZOS)
    left = (im.width - E.W) // 2
    top = int((im.height - E.H) * c["cy"])
    top = min(max(0, top), im.height - E.H)
    f = np.asarray(im.crop((left, top, left + E.W, top + E.H)), dtype=np.float32) / 255.0

    yy = np.arange(E.H, dtype=np.float32)[:, None] / E.H
    top_g = np.clip((0.32 - yy) / 0.32, 0, 1) ** 1.4 * 0.55
    bot_g = np.clip((yy - 0.48) / 0.52, 0, 1) ** 1.45 * 0.95
    f = f * (1 - top_g) * (1 - bot_g)

    def tracked(text, fnt, tr, y, alpha=255, stroke=0.0, cx=E.W / 2):
        im2 = Image.new("L", (E.W, E.H), 0)
        d = ImageDraw.Draw(im2)
        tw = E.tracked_width(fnt, text, tr)
        E.draw_tracked(d, (cx - tw / 2, y), text, fnt, tr, fill=alpha, stroke=stroke)
        return E.mask_to_float(im2)

    # en-tête
    f = E.composite(f, tracked("13 · 11 · 2026", E.font("m", 27), 7.4, 236, 255, 0.45), 1.0, 0.85)
    imr = Image.new("L", (E.W, E.H), 0)
    d = ImageDraw.Draw(imr)
    fnt = E.font("m", 27)
    tw = E.tracked_width(fnt, "WTBW", 8.0)
    E.draw_tracked(d, (E.W - 100 - tw, 236), "WTBW", fnt, 8.0, fill=255, stroke=0.45)
    f = E.composite(f, E.mask_to_float(imr), 1.0, 0.85)
    f[264, 100:E.W - 100] = np.maximum(f[264, 100:E.W - 100], 0.35)

    # titre
    f = E.composite(f, tracked(c["sub"], E.font("m", 31), 9.5, 1330, 255, 0.55), 1.0, 0.94)
    f = E.composite(f, tracked("IMELDA", E.font("pf", 150), 26, 1520, 255, 0.0), 1.0, 1.0)
    f[1580, E.W // 2 - 130:E.W // 2 + 130] = np.maximum(f[1580, E.W // 2 - 130:E.W // 2 + 130], 0.55)

    # signature
    f = E.composite(f, tracked("WTBW", E.font("m", 27), 11.0, 1692, 255, 0.5), 1.0, 0.72)

    # cadre fin
    f[74, 74:E.W - 74] = 0.20
    f[E.H - 75, 74:E.W - 74] = 0.20
    f[74:E.H - 74, 74] = 0.20
    f[74:E.H - 74, E.W - 75] = 0.20

    rng = np.random.default_rng(200 + idx)
    f = E.clamp01(f + rng.normal(0, 0.010, (E.H, E.W)).astype(np.float32))
    out = f"{E.OUT}/livrables/{c['out']}"
    Image.fromarray((f * 255 + 0.5).astype(np.uint8)).convert("RGB").save(
        out, quality=94, subsampling=1)
    print(out)


if __name__ == "__main__":
    os.makedirs(f"{E.OUT}/livrables", exist_ok=True)
    for i, c in enumerate(COVERS, 1):
        build(c, i)
