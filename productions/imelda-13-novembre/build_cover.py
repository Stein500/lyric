#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Couverture TikTok 1080x1920 — même langage graphique que le film."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import build_video as bv

W, H = bv.W, bv.H


def main():
    a = bv.load_photo("/home/user/lyric/IMG-20261111-WA0066.jpg")
    h, w = a.shape
    # cadrage : visage haut, buste large
    s = max(W / w, H / h) * 1.22
    im = Image.fromarray((a * 255).astype(np.uint8)).resize(
        (int(w * s), int(h * s)), Image.LANCZOS)
    iw, ih = im.size
    left = (iw - W) // 2
    top = int((ih - H) * 0.30)
    im = im.crop((left, top, left + W, top + H))
    f = np.asarray(im, dtype=np.float32) / 255.0

    # étalonnage local plus dense
    f = np.clip((f - 0.02) * 1.06, 0, 1)

    # dégradés de lisibilité (haut + bas)
    yy = np.arange(H, dtype=np.float32)[:, None] / H
    top_g = np.clip((0.30 - yy) / 0.30, 0, 1) ** 1.4 * 0.55
    bot_g = np.clip((yy - 0.52) / 0.48, 0, 1) ** 1.5 * 0.96
    f = f * (1 - top_g) * (1 - bot_g)

    dr_layer = Image.new("L", (W, H), 0)

    def tracked(text, fnt, tracking, y, alpha=255, stroke=0.0):
        im2 = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(im2)
        tw = bv.tracked_width(fnt, text, tracking)
        bv.draw_tracked(d, (W / 2 - tw / 2, y), text, fnt, tracking, fill=alpha, stroke=stroke)
        return bv.mask_to_float(im2)

    # en-tête éditorial
    m = tracked("13 · 11 · 2026", bv.font("m", 27), 7.4, 232, 255, 0.45)
    m2 = tracked("WTBW", bv.font("m", 27), 8.0, 232, 255, 0.45)
    # WTBW à droite : on redessine proprement
    imr = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(imr)
    fnt = bv.font("m", 27)
    tw = bv.tracked_width(fnt, "WTBW", 8.0)
    bv.draw_tracked(d, (W - 100 - tw, 232), "WTBW", fnt, 8.0, fill=255, stroke=0.45)
    m2 = bv.mask_to_float(imr)
    f = bv.composite(f, m, 1.0, 0.85)
    f = bv.composite(f, m2, 1.0, 0.85)
    f[260, 100:W - 100] = np.maximum(f[260, 100:W - 100], 0.35)

    # bloc titre
    m = tracked("JOYEUX ANNIVERSAIRE", bv.font("m", 31), 9.5, 1372, 255, 0.55)
    f = bv.composite(f, m, 1.0, 0.92)
    m = tracked("Imelda", bv.font("pfi", 196), 4, 1560, 255, 0.3)
    f = bv.composite(f, m, 1.0, 1.0)
    # filet + signature
    f[1610, W // 2 - 150:W // 2 + 150] = np.maximum(f[1610, W // 2 - 150:W // 2 + 150], 0.55)
    m = tracked("WTBW", bv.font("m", 28), 11.0, 1690, 255, 0.5)
    f = bv.composite(f, m, 1.0, 0.80)

    # ombre derrière le titre (lisibilité)
    mask_txt = bv.gauss(np.maximum(m, 0), 16)
    f *= (1 - 0.30 * mask_txt)

    # petit cœur
    heart = bv.ornament_heart(1.0, size=54, alpha=225)
    bv.paste_ornament(f, heart, W // 2 - 27, 1252, 0.9)

    # cadre extérieur fin
    f[74, 74:W - 74] = 0.22
    f[H - 75, 74:W - 74] = 0.22
    f[74:H - 74, 74] = 0.22
    f[74:H - 74, W - 75] = 0.22

    # grain
    rng = np.random.default_rng(3)
    f = bv.clamp01(f + rng.normal(0, 0.010, (H, W)).astype(np.float32))

    out = bv.OUT + "/livrables/COVER-IMELDA-13-NOVEMBRE-1080x1920.jpg"
    Image.fromarray((f * 255 + 0.5).astype(np.uint8)).convert("RGB").save(out, quality=94, subsampling=1)
    print("cover ->", out)


if __name__ == "__main__":
    main()
