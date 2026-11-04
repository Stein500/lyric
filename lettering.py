#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lettering.py — lettrage peint (graffiti) §4 v6.3 :
1. contour par dilatation (jamais stroke_width) ;
2. une tuile par glyphe à la taille de son encre, rotation ±1.0°, interlettrage 0,055·taille ;
3. halo = ombre serrée (MaxFilter(9)+flou 7 @60 %, flou 17 @34 %, 150 mouchetures) ;
4. décalage vertical par plan (typo_offsets.json).
Rendu : or #FFE8A8→#E8A83E (ligne 1), argent-cyan #F0FCFF→#96CDE0 (ligne 2).
Graine déterministe zlib.crc32(l1|l2). Coulures sous le bloc, jamais sur les lettres.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from common import font, GOLD_A, GOLD_B, CY_A, CY_B, INK, LETTER_BOX, NATIVE, vgrad, deterministic_seed

TRACK = 0.055   # interlettrage = 0,055 · taille


def _glyph_masks(ch, fnt, size, rng):
    """(masque_encre, masque_contour) d'un glyphe, tuile à sa taille d'encre, rotation ±1.0°."""
    ow = max(2, int(round(size / 10)))          # demi-largeur de contour
    pad = ow + 4
    big = Image.new("L", (size * 3, size * 3), 0)
    ImageDraw.Draw(big).text((size, size), ch, font=fnt, fill=255)
    bb = big.getbbox()
    if bb is None:
        return None, None
    glyph = big.crop(bb)                        # encre à sa taille exacte
    gw, gh = glyph.size
    cont = glyph.filter(ImageFilter.MaxFilter(2 * ow + 1))
    ink_t = Image.new("L", (gw + 2 * pad, gh + 2 * pad), 0)
    ink_t.paste(glyph, (pad, pad))
    cont_t = Image.new("L", (gw + 2 * pad, gh + 2 * pad), 0)
    cont_t.paste(cont, (pad - ow + pad - pad, pad - ow)) if False else cont_t.paste(cont, (pad - 0, pad - 0))
    # le contour dilaté déborde de ow : on le re-pose calé sur l'encre
    cont_t = Image.new("L", (gw + 2 * ow + 2 * pad, gh + 2 * ow + 2 * pad), 0)
    cont_t.paste(cont, (pad, pad))
    ink_t2 = Image.new("L", cont_t.size, 0)
    ink_t2.paste(glyph, (pad + ow, pad + ow))
    ang = (rng.random() * 2 - 1) * 1.0           # ±1.0°
    ink_r = ink_t2.rotate(ang, resample=Image.BICUBIC, expand=True)
    cont_r = cont_t.rotate(ang, resample=Image.BICUBIC, expand=True)
    return ink_r, cont_r


def _advance(ch, fnt, size):
    bb = fnt.getbbox(ch)
    return (bb[2] - bb[0]) + TRACK * size


def _line_width(text, fnt, size):
    w = 0.0
    for ch in text:
        bb = fnt.getbbox(ch)
        w += (bb[2] - bb[0]) + TRACK * size
    return w - TRACK * size


def _halo(ink_full, rng):
    """Halo = ombre serrée, jamais une flaque (§4.3)."""
    halo = ink_full.filter(ImageFilter.MaxFilter(9))
    h1 = np.asarray(halo.filter(ImageFilter.GaussianBlur(7))).astype(np.float32) * 0.60
    h2 = np.asarray(halo.filter(ImageFilter.GaussianBlur(17))).astype(np.float32) * 0.34
    h = h1 + h2
    ys, xs = np.nonzero(np.asarray(halo) > 30)
    if len(ys):
        idx = rng.integers(0, len(ys), 150)
        dys = rng.normal(0, 10, 150).astype(int)
        dxs = rng.normal(0, 12, 150).astype(int)
        for i, dy, dx in zip(idx, dys, dxs):
            y, x = int(ys[i]) + dy, int(xs[i]) + dx
            if 0 <= y < h.shape[0] - 1 and 0 <= x < h.shape[1] - 1:
                h[y:y + 2, x:x + 2] += 70
    return np.clip(h, 0, 255)


def _wrap(text, n):
    ws = text.split()
    per = -(-len(ws) // n)
    out, cur = [], []
    for w in ws:
        cur.append(w)
        if len(cur) >= per and len(out) < n - 1:
            out.append(" ".join(cur)); cur = []
    if cur:
        out.append(" ".join(cur))
    # ponctuation isolée rattachée à la ligne précédente
    merged = []
    for ln in out:
        if merged and all(not c.isalnum() for c in ln.replace(" ", "")):
            merged[-1] += " " + ln
        else:
            merged.append(ln)
    return merged


def paint(lines, seed_key, box=LETTER_BOX, dy=0):
    """
    Peint les paroles dans la boîte (natif 768x1376).
    lines : chaînes à afficher (déjà découpées) ; dy : décalage vertical §4.4.
    Renvoie (letters RGBA, meta).
    """
    text = " ".join(lines)
    x0, y0, x1, y1 = box
    y0 += dy; y1 += dy
    max_w, max_h = x1 - x0, y1 - y0
    rng = np.random.default_rng(deterministic_seed(text, seed_key))

    best = None
    for nlines in (2, 3, 4, 1):
        cand = _wrap(text, nlines)
        if len(cand) != nlines:
            continue
        lo, hi, fit = 16, 56, None
        while lo <= hi:
            mid = (lo + hi) // 2
            fnt = font("ExtraBold", mid)
            ok = all(_line_width(ln, fnt, mid) <= max_w for ln in cand)
            if ok and nlines * 1.22 * mid <= max_h:
                fit = mid; lo = mid + 1
            else:
                hi = mid - 1
        if fit:
            # pénalité : ligne = mot seul court (esthétique « mots empilés »)
            pen = sum(8 for ln in cand if len(ln.split()) == 1 and len(ln) < 6)
            if best is None or (fit - pen) > (best[0] - best[2]):
                best = (fit, cand, pen)
    if best is None:
        best = (16, [text], 0)
    size, display = best[0], best[1]
    fnt = font("ExtraBold", size)

    line_h = 1.22 * size
    block_h = len(display) * line_h
    y_top = y0 + (max_h - block_h) / 2

    # passe 1 : composer encre + contour par ligne
    ink_full = Image.new("L", NATIVE, 0)
    ink_parts, cont_parts = [], []
    x_cursor_info = []
    for li, ln in enumerate(display):
        lw = _line_width(ln, fnt, size)
        px = x0 + (max_w - lw) / 2
        py = y_top + li * line_h
        ink_l = Image.new("L", NATIVE, 0)
        cont_l = Image.new("L", NATIVE, 0)
        x = px
        for ch in ln:
            if ch == " ":
                bb = fnt.getbbox(" ")
                x += (bb[2] - bb[0]) + TRACK * size
                continue
            im_i, im_c = _glyph_masks(ch, fnt, size, rng)
            if im_i is not None:
                iw, ih = im_i.size
                pos = (int(x - 6), int(py + size * 0.12 - ih / 2))
                ink_l.paste(im_i, pos, im_i)
                cont_l.paste(im_c, pos, im_c)
            x += _advance(ch, fnt, size)
        ink_parts.append((ink_l, li))
        cont_parts.append(cont_l)
        ink_full = Image.fromarray(np.maximum(np.asarray(ink_full), np.asarray(ink_l)))

    canvas = Image.new("RGBA", NATIVE, (0, 0, 0, 0))
    # halo d'abord (ombre derrière)
    halo_rgba = Image.new("RGBA", NATIVE, INK + (0,))
    halo_rgba.putalpha(Image.fromarray(_halo(ink_full, rng).astype(np.uint8), "L").point(lambda v: int(v * 0.85)))
    canvas = Image.alpha_composite(canvas, halo_rgba)
    # contours (dilatés) derrière les lettres
    for cont_l in cont_parts:
        lay = Image.new("RGBA", NATIVE, INK + (0,))
        lay.putalpha(cont_l)
        canvas = Image.alpha_composite(canvas, lay)
    # lettres : dégradé or (ligne 1) / argent-cyan (ligne 2), alterné
    for ink_l, li in ink_parts:
        top, bot = (GOLD_A, GOLD_B) if li % 2 == 0 else (CY_A, CY_B)
        grad = vgrad(NATIVE, top, bot).convert("RGBA")
        grad.putalpha(ink_l)
        canvas = Image.alpha_composite(canvas, grad)

    # coulures d'encre sous le bloc, jamais sur les lettres
    d = ImageDraw.Draw(canvas)
    bot_y = int(y_top + block_h + 3)
    for k in range(4):
        dx = int(x0 + max_w * (0.18 + 0.21 * k) + rng.integers(-8, 8))
        ln_d = int(rng.integers(18, 55))
        col = GOLD_A if k % 2 == 0 else CY_A
        for s in range(ln_d):
            a = int(110 * (1 - s / ln_d))
            d.line([(dx, bot_y + s), (dx, bot_y + s)], fill=col + (a,))
    return canvas, {"size": size, "lines": display}
