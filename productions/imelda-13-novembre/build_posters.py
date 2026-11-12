#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""10 affiches 1080x1350 — décors générés par IA (aucun visage généré),
photos réelles de Imelda intactes, lettrage et ornements du moteur WTBW.
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

import engine as E

ROOT = E.ROOT
OUT = E.OUT
BG = "/home/user/lyric/productions/imelda-13-novembre/assets/decors"
P = "IMG-20261111-WA"
PW, PH = 1080, 1350

POSTERS = [
    dict(bg="bg-01.png", photo="0066", eyebrow="13 · 11 · 2026",
         line=("Joyeux anniversaire,", "Imelda.")),
    dict(bg="bg-02.png", photo="0031", eyebrow="NOUKIKO TCHÉ WÊ",
         line=("Ce sourire-là, personne", "ne te l'enlèvera.")),
    dict(bg="bg-03.png", photo="0036", eyebrow="AYON DÈKPÈ",
         line=("Tu ne marches pas :", "tu fais danser la lumière.")),
    dict(bg="bg-04.png", photo="0033", eyebrow="13 · 11", layout="plate",
         line=("Et moi, je reste", "à regarder.")),
    dict(bg="bg-05.png", photo="0041", eyebrow="TON SOURIRE",
         line=("Il y a des sourires", "qui réparent une journée.")),
    dict(bg="bg-06.png", photo="0039", eyebrow="13 · 11 · 2026",
         line=("Le tien répare", "des années.")),
    dict(bg="bg-07.png", photo="0043", eyebrow="AYON DÈKPÈ", layout="plate", ink="dark",
         line=("Tu es trop jolie.",)),
    dict(bg="bg-08.png", photo="0067", eyebrow="TU ES TROP BELLE",
         line=("J'ai la trouille,", "c'est fou.")),
    dict(bg="bg-09.png", photo="0048", eyebrow="13 · 11 · 2026", layout="plate",
         line=("Seulement de", "ton regard.")),
    dict(bg="bg-10.png", photo="0030", eyebrow="MERCI D'EXISTER",
         line=("Joyeux anniversaire,", "Imelda.")),
]


def dark_window(g):
    """plus grande zone sombre = fenêtre où poser la photo."""
    for th in (28, 40, 55):
        mask = g < th
        lab, n = ndimage.label(mask)
        if n == 0:
            continue
        sizes = ndimage.sum(mask, lab, range(1, n + 1))
        i = int(np.argmax(sizes))
        if sizes[i] < 0.12 * g.size:
            continue
        ys, xs = np.where(lab == i + 1)
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        w, h = x1 - x0, y1 - y0
        if w < 0.28 * g.shape[1] or h < 0.22 * g.shape[0]:
            continue
        return x0, y0, x1, y1
    return None


def fit_cover(a, w, h):
    ih, iw = a.shape
    s = max(w / iw, h / ih)
    im = Image.fromarray((a * 255).astype(np.uint8)).resize(
        (max(1, int(iw * s)), max(1, int(ih * s))), Image.LANCZOS)
    left, top = (im.width - w) // 2, (im.height - h) // 2
    return np.asarray(im.crop((left, top, left + w, top + h)), dtype=np.float32) / 255.0


def build(p, idx):
    bg = Image.open(f"{BG}/{p['bg']}").convert("L").resize((PW, PH), Image.LANCZOS)
    b = np.asarray(bg, dtype=np.float32) / 255.0
    layout = p.get("layout", "frame")
    ink_dark = p.get("ink") == "dark"

    if layout == "plate":
        x0, y0, x1, y1 = (int(PW * 0.085), int(PH * 0.055),
                          int(PW * 0.915), int(PH * 0.625))
        win = (x0, y0, x1, y1)
        text_area = "below"
    else:
        win = dark_window(np.asarray(bg))
        if win is None:
            win = (int(PW * 0.10), int(PH * 0.10), int(PW * 0.90), int(PH * 0.86))
        x0, y0, x1, y1 = win
        m = int(min(x1 - x0, y1 - y0) * 0.045)
        x0, y0, x1, y1 = x0 + m, y0 + m, x1 - m, y1 - m
        win = (x0, y0, x1, y1)
        text_area = "inside"

    w, h = x1 - x0, y1 - y0
    photo = E.load_photo(f"{ROOT}/{P}{p['photo']}.jpg")
    ph = fit_cover(photo, w, h)

    if text_area == "inside":
        yy = np.arange(h, dtype=np.float32)[:, None] / h
        gsc = np.clip((yy - 0.44) / 0.56, 0, 1) ** 1.25 * 0.88
        ph = ph * (1 - gsc)
    b[y0:y1, x0:x1] = ph

    # filet clair autour de la photo
    edge_v = 0.18 if ink_dark else 0.55
    b[y0, x0:x1] = np.maximum(b[y0, x0:x1], edge_v)
    b[y1 - 1, x0:x1] = np.maximum(b[y1 - 1, x0:x1], edge_v)
    b[y0:y1, x0] = np.maximum(b[y0:y1, x0], edge_v)
    b[y0:y1, x1 - 1] = np.maximum(b[y0:y1, x1 - 1], edge_v)

    canvas = Image.new("L", (PW, PH), 0)
    dr = ImageDraw.Draw(canvas)

    def put(text, fnt, track, baseline, alpha=255, cx=None, stroke=0.0):
        tw = E.tracked_width(fnt, text, track)
        cx = PW / 2 if cx is None else cx
        E.draw_tracked(dr, (cx - tw / 2, baseline), text, fnt, track, fill=alpha, stroke=stroke)

    lines = p["line"]
    if text_area == "inside":
        eb_base = y0 + int(h * 0.705)
        line_base = y0 + int(h * 0.83)
        maxw = w * 0.88
        width_ref = w
    else:
        eb_base = int(PH * 0.715)
        line_base = int(PH * 0.795)
        maxw = PW * 0.76
        width_ref = PW

    # sur-titre
    eb = p["eyebrow"]
    fnt = E.font("m", 26)
    tw = E.tracked_width(fnt, eb, 9)
    k = min(1.0, maxw / max(1, tw))
    if k < 0.98:
        fnt = E.font("m", max(16, int(26 * k)))
    put(eb, fnt, 9, eb_base, 255, stroke=0.5)

    # lignes principales
    size = 64 if len(lines) == 1 else 58
    fnt = E.font("pfi", size)
    tw = max(E.tracked_width(fnt, l, 0.3) for l in lines)
    k = min(1.0, maxw / max(1, tw))
    if k < 0.98:
        fnt = E.font("pfi", max(26, int(size * k)))
    lh = int(fnt.size * 1.26)
    for i, l in enumerate(lines):
        put(l, fnt, 0.3, line_base + i * lh, 255, stroke=0.35)

    # signature discrète, toujours dans la marge basse du poster
    sg = "13 · 11 · 2026     WTBW"
    fnt = E.font("m", 21)
    put(sg, fnt, 7.0, int(PH * (0.935 if text_area == "inside" else 0.945)),
        215 if not ink_dark else 60, stroke=0.4)

    mask = np.asarray(canvas, dtype=np.float32) / 255.0
    if ink_dark:
        # bande de papier clair derrière l'encre (lisibilité sur le sumi-e)
        yy2 = np.arange(PH, dtype=np.float32)[:, None] / PH
        band = np.clip((yy2 - 0.685) / 0.05, 0, 1)
        b = b * (1 - 0.93 * band) + 0.975 * 0.93 * band
        b = E.composite(b, mask, 0.04, 1.0)
    else:
        sh = E.gauss(mask, 12)
        b *= (1 - 0.62 * sh)
        b = E.composite(b, mask, 1.0, 1.0)

    # ornement discret dans la marge
    if not ink_dark:
        orn = E.ornament_heart(1.0, size=32, alpha=200)
        E.paste_ornament(b, orn, PW // 2 - 16, int(PH * 0.877), 0.62)
    else:
        orn = E.ornament_flower(1.0, size=40, alpha=210)
        E.paste_ornament(b, orn, PW // 2 - 20, int(PH * 0.877), 0.85)

    rng = np.random.default_rng(100 + idx)
    b = E.clamp01(b + rng.normal(0, 0.008, (PH, PW)).astype(np.float32))

    out = f"{OUT}/livrables/affiches/AFFICHE-{idx:02d}-IMELDA-WTBW.jpg"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    Image.fromarray((b * 255 + 0.5).astype(np.uint8)).save(out, quality=94, subsampling=1)
    return out


if __name__ == "__main__":
    os.makedirs(f"{BG}", exist_ok=True)
    for i, p in enumerate(POSTERS, 1):
        print(i, build(p, i))
