#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LOGO WTBW SEUL — marque propre, lisible à 250 × 250 (avatar TikTok / IG / WhatsApp).

Trois dessins, trois coloris, trois tailles + 4 stories prêtes à publier.
Rien d'autre que le sigle et les quatre lettres W T B W : aucun nom, aucune baseline longue.

Usage : python3 logo_wtbw.py
Sortie : livrables/brand/logo/  et  livrables/brand/story/
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, "/home/user/lyric/productions/imelda-13-novembre")
sys.path.insert(0, "/home/user/lyric/productions/pub-wtbw")
import engine as E  # noqa: E402

OUT = "/home/user/lyric/productions/pub-wtbw"
LIV = f"{OUT}/livrables/brand"
SS = 4  # supersampling

CHAR = np.array([0.043, 0.043, 0.047], dtype=np.float32)   # #0B0B0C
CREAM = np.array([0.949, 0.937, 0.914], dtype=np.float32)  # #F2EFE9
BRASS = np.array([0.784, 0.631, 0.420], dtype=np.float32)  # #C8A16B
WHITE = np.array([1.0, 1.0, 1.0], dtype=np.float32)
BLACK = np.array([0.02, 0.02, 0.022], dtype=np.float32)

COLORS = {"blanc-sur-charbon": (WHITE, CHAR),
          "laiton-sur-charbon": (BRASS, CHAR),
          "noir-sur-creme": (BLACK, CREAM)}


# ───────────────────────── primitives (dessinées en grand, réduites ensuite)
def sigil_mask(sz, ring=True, simple=False):
    """le W dans son double cercle ; simple=True -> juste le cercle + le W (avatar 250)."""
    S = sz * SS
    img = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(img)
    c = S / 2
    if ring:
        d.ellipse([c - S * .478, c - S * .478, c + S * .478, c + S * .478],
                  outline=255, width=max(2, int(S * .016)))
        d.ellipse([c - S * .436, c - S * .436, c + S * .436, c + S * .436],
                  outline=170, width=max(1, int(S * .006)))
    wdt = max(3, int(S * .060))
    p = [(-.235, -.140), (-.117, .140), (0, -.050), (.117, .140), (.235, -.140)]
    pts = [(c + x * S, c + y * S) for x, y in p]
    d.line(pts, fill=255, width=wdt, joint="curve")
    for q in (pts[0], pts[-1]):
        d.ellipse([q[0] - wdt / 2, q[1] - wdt / 2, q[0] + wdt / 2, q[1] + wdt / 2], fill=255)
    if not simple:
        d.line([(c - S * .150, c + S * .268), (c + S * .150, c + S * .268)],
               fill=225, width=max(1, int(S * .010)))
        cx, cy, r = c, c + S * .350, S * .046
        pts2 = []
        for k in range(10):
            a = -np.pi / 2 + k * np.pi / 5
            rr = r if k % 2 == 0 else r * .42
            pts2.append((cx + rr * np.cos(a), cy + rr * np.sin(a)))
        d.polygon(pts2, fill=255)
    return np.asarray(img.resize((sz, sz), Image.LANCZOS), dtype=np.float32) / 255.0


def word_mask(w, size, stroke=None, track=0.24):
    """W T B W en Montserrat, interlettré, ajusté à la largeur w."""
    S = 4
    fnt = E.font("m", size * S)
    st = int((stroke if stroke is not None else size * 0.055) * S)
    tr = size * track * S
    tw = E.tracked_width(fnt, "WTBW", tr) + st * 2
    img = Image.new("L", (int(tw) + 8, int(size * S * 1.6)), 0)
    d = ImageDraw.Draw(img)
    E.draw_tracked(d, (4 + st, size * S * 1.12), "WTBW", fnt, tr, fill=255, stroke=st)
    a = np.asarray(img.resize((max(1, img.width // S), max(1, img.height // S)), Image.LANCZOS),
                   dtype=np.float32) / 255.0
    sc = w / a.shape[1]
    return np.asarray(Image.fromarray((a * 255).astype(np.uint8)).resize(
        (w, max(1, int(a.shape[0] * sc))), Image.LANCZOS), dtype=np.float32) / 255.0


def crop(m, thr=0.03):
    """rogne le masque sur son encre réelle -> placement exact."""
    ys = np.where((m > thr).any(axis=1))[0]
    xs = np.where((m > thr).any(axis=0))[0]
    if not len(ys) or not len(xs):
        return m
    return m[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1]


def compose(mask, fg, bg, size, margin=0.0, shadow=False):
    f = np.ones((size, size, 3), dtype=np.float32) * np.array(bg, dtype=np.float32)
    h, w = mask.shape
    x = (size - w) // 2
    y = (size - h) // 2
    if shadow:
        pad = Image.new("L", (size, size), 0)
        pad.paste(Image.fromarray((mask * 255).astype(np.uint8)), (x + int(size * .012), y + int(size * .015)))
        blur = np.asarray(pad.filter(ImageFilter.GaussianBlur(size * .035)), dtype=np.float32) / 255.0
        f *= (1 - blur[..., None] * 0.55)
    a = mask[..., None]
    f[y:y + h, x:x + w] = f[y:y + h, x:x + w] * (1 - a) + np.array(fg, dtype=np.float32) * a
    return f


def save_rgb(f, path, q=95):
    Image.fromarray((np.clip(f, 0, 1) * 255 + .5).astype(np.uint8)).save(path, quality=q, subsampling=1)
    os.chmod(path, 0o644)
    return path


def save_alpha(mask, path, color=(1, 1, 1)):
    rgba = Image.new("RGBA", (mask.shape[1], mask.shape[0]), (int(color[0] * 255),) * 3 + (0,))
    rgba.putalpha(Image.fromarray((mask * 255).astype(np.uint8)))
    rgba.save(path)
    return path


# ───────────────────────── les 3 dessins
def design_sigil(size, colorway):
    fg, bg = COLORS[colorway]
    m = sigil_mask(int(size * (.66 if size <= 300 else .74)), simple=(size <= 300))
    return compose(m, fg, bg, size, shadow=(colorway.startswith("blanc") or colorway.startswith("laiton")))


def design_word(size, colorway):
    fg, bg = COLORS[colorway]
    f = np.ones((size, size, 3), dtype=np.float32) * np.array(bg, dtype=np.float32)
    w = crop(word_mask(int(size * (.74 if size <= 300 else .80)), int(size * .175 if size > 300 else size * .21)))
    h, wd = w.shape
    x, y = (size - wd) // 2, (size - h) // 2
    a = w[..., None]
    f[y:y + h, x:x + wd] = f[y:y + h, x:x + wd] * (1 - a) + np.array(fg, dtype=np.float32) * a
    # filets laiton au-dessus et en dessous, collés au mot
    return f


def design_both(size, colorway):
    fg, bg = COLORS[colorway]
    m = sigil_mask(int(size * (.40 if size <= 300 else .44)), simple=(size <= 300))
    f = np.ones((size, size, 3), dtype=np.float32) * np.array(bg, dtype=np.float32)
    hh, hw = m.shape
    my = int(size * (.075 if size <= 300 else .055))
    a0 = m[..., None]
    f[my:my + hh, (size - hw) // 2:(size - hw) // 2 + hw] = (
        f[my:my + hh, (size - hw) // 2:(size - hw) // 2 + hw] * (1 - a0)
        + np.array(fg, dtype=np.float32) * a0)
    w = crop(word_mask(int(size * (.50 if size <= 300 else .60)), int(size * .105 if size > 300 else size * .140)))
    h, wd = w.shape
    x, y = (size - wd) // 2, int(size * (.70 if size <= 300 else .72))
    a = w[..., None]
    f[y:y + h, x:x + wd] = f[y:y + h, x:x + wd] * (1 - a) + np.array(fg, dtype=np.float32) * a
    return f


DESIGNS = {"SIGLE": design_sigil, "LETTRAGE": design_word, "SIGLE-LETTRAGE": design_both}


# ───────────────────────── stories 1080×1920
def story(kind):
    W, H = 1080, 1920
    f = np.ones((H, W, 3), dtype=np.float32) * CHAR
    yy = np.linspace(-1, 1, H, dtype=np.float32)[:, None]
    xx = np.linspace(-1, 1, W, dtype=np.float32)[None, :]
    r = np.sqrt(xx ** 2 + (yy * 0.6) ** 2) / 1.3
    f *= (1.0 - 0.55 * r ** 1.7)[..., None]

    def put(m, fg, cx, cy):
        h, w = m.shape
        x, y = int(cx - w / 2), int(cy - h / 2)
        a = m[..., None]
        f[y:y + h, x:x + w] = f[y:y + h, x:x + w] * (1 - a) + np.array(fg, dtype=np.float32) * a

    if kind == 1:      # sigle + WTBW, annonce de marque
        put(sigil_mask(430, simple=True), WHITE, W / 2, H * 0.355)
        put(crop(word_mask(520, 118, track=0.30)), WHITE, W / 2, H * 0.545)
    elif kind == 2:    # lettrage géant, laiton
        put(crop(word_mask(780, 205, track=0.22)), BRASS, W / 2, H * 0.455)
        f[int(H * .525):int(H * .525) + 3, int(W * .34):int(W * .66)] = BRASS * .8
    elif kind == 3:    # nouveau son
        put(sigil_mask(240, simple=True), WHITE, W / 2, H * 0.265)
        put(crop(word_mask(620, 155, track=0.18)), BRASS, W / 2, H * 0.505)
    else:              # service sur mesure
        put(sigil_mask(300, simple=True), WHITE, W / 2, H * 0.285)
        put(crop(word_mask(520, 112, track=0.26)), WHITE, W / 2, H * 0.445)
    return f


def type_line(f, txt, kind, size, y, color, track_r, maxw=0.8, op=1.0):
    W = f.shape[1]
    s = size
    while s > 12:
        fnt = E.font(kind, s)
        if E.tracked_width(fnt, txt, s * track_r) <= W * maxw:
            break
        s = int(s * 0.95)
    fnt = E.font(kind, s)
    im = Image.new("L", (W, int(s * 1.7)), 0)
    d = ImageDraw.Draw(im)
    tw = E.tracked_width(fnt, txt, s * track_r)
    E.draw_tracked(d, ((W - tw) / 2, s * 0.95), txt, fnt, s * track_r, fill=255)
    a = np.asarray(im, dtype=np.float32) / 255.0 * op
    h = a.shape[0]
    y = int(y)
    sub = a[..., None]
    f[y:y + h] = f[y:y + h] * (1 - sub) + np.array(color, dtype=np.float32) * sub
    return f


def story_full(kind):
    """story terminée : visuel + une ligne de texte seulement."""
    f = story(kind)
    if kind == 3:
        type_line(f, "NOUVEAU SON", "m", 40, 1920 * 0.375, CREAM, 0.44, op=0.85)
        type_line(f, "DISPONIBLE PARTOUT", "m", 24, 1920 * 0.590, BRASS, 0.36, op=0.9)
    elif kind == 4:
        type_line(f, "DIS-MOI L'OCCASION", "pf", 64, 1920 * 0.560, CREAM, 0.10)
        type_line(f, "J'ÉCRIS LA CHANSON", "pfi", 64, 1920 * 0.606, CREAM, 0.10)
    # grain léger
    rng = np.random.default_rng(kind)
    f = np.clip(f + rng.normal(0, 0.004, f.shape[:2])[..., None], 0, 1)
    return f


def main():
    os.makedirs(f"{LIV}/logo", exist_ok=True)
    os.makedirs(f"{LIV}/story", exist_ok=True)
    n = 0
    for dname, fn in DESIGNS.items():
        for cname in COLORS:
            # avatar TikTok 250
            f = fn(250, cname)
            save_rgb(f, f"{LIV}/logo/WTBW-{dname}-{cname}-250.png"); n += 1
            # 1080 (feed, favicon hi-dpi, presse)
            f = fn(1080, cname)
            save_rgb(f, f"{LIV}/logo/WTBW-{dname}-{cname}-1080.png", q=96); n += 1
    # versions transparentes (incrustation)
    for dname, fn in DESIGNS.items():
        for sz in (1080, 2000):
            if dname == "SIGLE":
                m = sigil_mask(sz, simple=False)
            elif dname == "LETTRAGE":
                m = word_mask(int(sz * .8), int(sz * .175))
            else:
                base = sigil_mask(int(sz * .46))
                canvas = np.zeros((sz, sz), dtype=np.float32)
                h, w = base.shape
                canvas[int(sz * .10):int(sz * .10) + h, (sz - w) // 2:(sz - w) // 2 + w] = base
                wm = word_mask(int(sz * .62), int(sz * .105))
                h2, w2 = wm.shape
                canvas[int(sz * .735):int(sz * .735) + h2, (sz - w2) // 2:(sz - w2) // 2 + w2] = wm
                m = canvas
            save_alpha(m, f"{LIV}/logo/WTBW-{dname}-transparent-{sz}.png"); n += 1
    # stories
    for k in (1, 2, 3, 4):
        save_rgb(story_full(k), f"{LIV}/story/WTBW-STORY-0{k}.jpg", q=94); n += 1
    print("logo ok", n)


if __name__ == "__main__":
    main()
