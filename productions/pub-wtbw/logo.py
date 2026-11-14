#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Marque DSKY · WTBW — sigle + lettrage + badge.
Trois déclinaisons : « stack » (affiche/tee), « type » (fashion, gros), « badge » (pastille ronde).
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, "/home/user/lyric/productions/imelda-13-novembre")
import engine as E

OUT = "/home/user/lyric/productions/pub-wtbw"
LIV = f"{OUT}/livrables/brand"


# ───────────────────────── sigle ─────────────────────────
def star(d, cx, cy, r, fill=255):
    pts = []
    for k in range(10):
        ang = -np.pi / 2 + k * np.pi / 5
        rr = r if k % 2 == 0 else r * 0.42
        pts.append((cx + rr * np.cos(ang), cy + rr * np.sin(ang)))
    d.polygon(pts, fill=fill)


def sigil(size, ring=True):
    S = 2048
    img = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(img)
    c = S / 2
    if ring:
        d.ellipse([c - S * 0.478, c - S * 0.478, c + S * 0.478, c + S * 0.478],
                  outline=255, width=int(S * 0.016))
        d.ellipse([c - S * 0.436, c - S * 0.436, c + S * 0.436, c + S * 0.436],
                  outline=170, width=int(S * 0.006))
    wdt = int(S * (0.060 if ring else 0.064))
    p = [(-0.235, -0.140), (-0.117, 0.140), (0.000, -0.050), (0.117, 0.140), (0.235, -0.140)]
    pts = [(c + x * S, c + y * S) for x, y in p]
    d.line(pts, fill=255, width=wdt, joint="curve")
    for q in pts[:1] + pts[-1:]:
        d.ellipse([q[0] - wdt / 2, q[1] - wdt / 2, q[0] + wdt / 2, q[1] + wdt / 2], fill=255)
    d.line([(c - S * 0.150, c + S * 0.268), (c + S * 0.150, c + S * 0.268)],
           fill=225, width=int(S * 0.010))
    star(d, c, c + S * 0.350, S * 0.046)
    return np.asarray(img.resize((size, size), Image.LANCZOS), dtype=np.float32) / 255.0


# ───────────────────────── texte ─────────────────────────
def text_alpha(w, h, fn):
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    fn(d, im)
    return np.asarray(im, dtype=np.float32) / 255.0


def tracked_line(w, txt, kind, size, track, stroke=0, h=None):
    """rend une ligne centrée, largeur = w."""
    fnt = E.font(kind, size)
    h = h or int(size * 1.6)
    a = text_alpha(w, h, lambda d, im: (
        E.draw_tracked(d, (w / 2 - E.tracked_width(fnt, txt, track) / 2, h * 0.78),
                       txt, fnt, track, fill=255, stroke=stroke)))
    return a


def fit_line(w, txt, kind, track_ratio, max_size, stroke=0, margin=0.94):
    s = max_size
    while s > 8:
        fnt = E.font(kind, s)
        if E.tracked_width(fnt, txt, s * track_ratio) <= w * margin:
            break
        s = int(s * 0.96)
    return tracked_line(w, txt, kind, s, s * track_ratio, stroke=stroke,
                        h=int(s * 1.55)), s


def center_in(a, w):
    out = np.zeros((a.shape[0], w), dtype=np.float32)
    x0 = (w - a.shape[1]) // 2
    out[:, x0:x0 + a.shape[1]] = a
    return out


def stack(w):
    """bloc vertical : sigle · DSKY · WTBW · filet · baseline."""
    gh = int(w * 0.60)
    parts = [center_in(sigil(gh), w)]
    gap = lambda r: np.zeros((int(w * r), w), dtype=np.float32)

    ds, _ = fit_line(w, "DSKY", "pf", 0.125, int(w * 0.27))
    wt, _ = fit_line(w, "WTBW", "m", 0.32, int(w * 0.145), stroke=max(2, int(w * 0.0045)))
    bl, _ = fit_line(w, "WOLOF TECHSTEIN BEAT WÊ · BÉNIN", "m", 0.19, int(w * 0.062))
    rule = np.zeros((max(2, int(w * 0.004)), w), dtype=np.float32)
    ri = Image.new("L", (w, rule.shape[0]), 0)
    ImageDraw.Draw(ri).rectangle([int(w * 0.34), 0, int(w * 0.66), rule.shape[0] - 1], fill=255)
    rule = np.asarray(ri, dtype=np.float32) / 255.0

    blocks = [parts[0], gap(0.05), ds, gap(0.012), wt, gap(0.035), rule, gap(0.03), bl]
    return np.vstack(blocks)


def stack_stein(w):
    """bloc vertical avec la ligne d'état civil : sigle · DSKY · WTBW · filet · NOM · métiers."""
    gh = int(w * 0.56)
    parts = [center_in(sigil(gh), w)]
    gap = lambda r: np.zeros((int(w * r), w), dtype=np.float32)

    ds, _ = fit_line(w, "DSKY", "pf", 0.125, int(w * 0.27))
    wt, _ = fit_line(w, "WTBW", "m", 0.32, int(w * 0.145), stroke=max(2, int(w * 0.0045)))
    nm, _ = fit_line(w, "C. JÉSUTONDJI SAMUEL STEIN", "m", 0.16, int(w * 0.058))
    mt, _ = fit_line(w, "LYRICISTE · ÉDUCATEUR · BÉNIN", "m", 0.20, int(w * 0.042))
    ri = Image.new("L", (w, max(2, int(w * 0.004))), 0)
    ImageDraw.Draw(ri).rectangle([int(w * 0.34), 0, int(w * 0.66), int(w * 0.004) - 1], fill=255)
    rule = np.asarray(ri, dtype=np.float32) / 255.0

    blocks = [parts[0], gap(0.045), ds, gap(0.010), wt, gap(0.032), rule,
              gap(0.026), nm, gap(0.012), mt]
    return np.vstack(blocks)


def type_block(w):
    """lettrage fashion : DSKY / WTBW énormes, sigle discret dessous."""
    ds, _ = fit_line(w, "DSKY", "pf", 0.10, int(w * 0.38))
    wt, _ = fit_line(w, "WTBW", "m", 0.26, int(w * 0.20), stroke=max(2, int(w * 0.005)))
    sg = center_in(sigil(int(w * 0.16)), w)
    pad = np.zeros((int(w * 0.02), w), dtype=np.float32)
    return np.vstack([ds, pad, wt, np.zeros((int(w * 0.06), w), np.float32), sg])


def polar_text(txt, size, radius, track, angle0=0.0, invert=False):
    """rend un texte courbé : renvoie (alpha, (cx, cy)) sur un carré de côté 2*(radius+size)."""
    fnt = E.font("m", size)
    tw = int(E.tracked_width(fnt, txt, track)) + 8
    strip = Image.new("L", (tw, int(size * 1.5)), 0)
    d = ImageDraw.Draw(strip)
    E.draw_tracked(d, (4, size * 1.12), txt, fnt, track, fill=255)
    src = np.asarray(strip, dtype=np.float32) / 255.0

    side = int(2 * (radius + size * 1.5))
    c = side / 2
    yy, xx = np.mgrid[0:side, 0:side].astype(np.float32)
    dx, dy = xx - c, yy - c
    r = np.hypot(dx, dy)
    th = np.arctan2(dy, dx)
    # angle 0 = haut
    ang = (th + np.pi / 2)
    arc = (ang - angle0) * radius
    xs = ((tw / 2 - arc) if invert else (arc + tw / 2)).astype(np.int32)
    ys = ((r - radius + size * 0.55) if invert else (radius + size * 1.15 - r)).astype(np.int32)
    inside = (xs >= 0) & (xs < tw) & (ys >= 0) & (ys < src.shape[0])
    out = np.zeros((side, side), dtype=np.float32)
    out[inside] = src[ys[inside], xs[inside]]
    return out, side


def badge(w):
    """pastille ronde : sigle + DSKY · WTBW courbé + baseline courbée."""
    side = w
    canvas = Image.new("L", (side, side), 0)
    d = ImageDraw.Draw(canvas)
    c = side / 2
    d.ellipse([c - side * 0.487, c - side * 0.487, c + side * 0.487, c + side * 0.487],
              outline=255, width=int(side * 0.009))
    d.ellipse([c - side * 0.30, c - side * 0.30, c + side * 0.30, c + side * 0.30],
              outline=255, width=int(side * 0.006))
    # sigle au centre
    sg = sigil(int(side * 0.42))
    canvas.paste(Image.fromarray((sg * 255).astype(np.uint8)),
                 (int(c - sg.shape[0] / 2), int(c - sg.shape[1] / 2)))
    base = np.asarray(canvas, dtype=np.float32) / 255.0

    top, s1 = polar_text("DSKY · WTBW", int(side * 0.075), side * 0.395, side * 0.028)
    bot, s2 = polar_text("WOLOF TECHSTEIN BEAT WÊ", int(side * 0.042), side * 0.400,
                         side * 0.019, angle0=np.pi, invert=True)
    for layer in (top, bot):
        L = layer.shape[0]
        o = int(c - L / 2)
        h, ww = L, L
        ya, yb = max(0, o), min(side, o + L)
        xa, xb = max(0, o), min(side, o + L)
        sub = layer[ya - o:yb - o, xa - o:xb - o]
        base[ya:yb, xa:xb] = np.maximum(base[ya:yb, xa:xb], sub)
    return base


VARIANTS = {"stack": stack, "type": type_block, "badge": badge}


def alpha_for(variant, width):
    a = VARIANTS[variant](width)
    if variant == "badge":
        a = np.clip(a, 0, 1)
    return a


if __name__ == "__main__":
    os.makedirs(f"{LIV}/print", exist_ok=True)
    # planche de contrôle
    tiles = []
    for v, wd in (("stack", 700), ("type", 700), ("badge", 700)):
        a = alpha_for(v, wd)
        im = Image.new("L", (800, 800), 8)
        ai = Image.fromarray((a * 255).astype(np.uint8))
        im.paste(ai, ((800 - ai.width) // 2, (800 - ai.height) // 2))
        tiles.append(im)
    sheet = Image.new("L", (800 * 3, 800), 8)
    for i, t in enumerate(tiles):
        sheet.paste(t, (800 * i, 0))
    sheet.save("/home/user/work/logo3.png")

    # fichiers d'impression
    pr = f"{LIV}/print"
    os.makedirs(pr, exist_ok=True)
    def png(a, path):
        im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
        rgba = Image.new("RGBA", im.size, (255, 255, 255, 0))
        rgba.putalpha(im)
        rgba.save(path)
    png(stack(2400), f"{pr}/DSKY-WTBW-lockup-blanc-2400px.png")
    png(type_block(2400), f"{pr}/DSKY-WTBW-lettrage-blanc-2400px.png")
    png(badge(2000), f"{pr}/DSKY-WTBW-badge-blanc-2000px.png")
    png(sigil(2000), f"{pr}/DSKY-WTBW-sigle-blanc-2000px.png")
    noir = 1 - np.clip(stack(2400), 0, 1)
    png(noir, f"{pr}/DSKY-WTBW-lockup-noir-2400px.png")
    print("print ok")
