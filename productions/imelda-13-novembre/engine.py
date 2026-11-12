#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IMELDA · 13 NOVEMBRE — un seul chef-d'œuvre.
Moteur de rendu 1080x1920 : photos réelles de Imelda, étalonnage N&B adaptatif,
lettrage moteur (Playfair / Montserrat), ornements vectoriels, vague douce,
grains par frame, fondus et respirations calés sur le medley des 3 refrains.
Aucune image IA, aucun son généré.
"""
import json
import math
import os
import subprocess
import sys

import numpy as np
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = "/home/user/lyric"
OUT = f"{ROOT}/productions/imelda-13-novembre"
CACHE = f"{OUT}/cache"
FF = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 1080, 1920
FPS = 30
FONT = {
    "pf": f"{OUT}/PlayfairDisplay.ttf",
    "pfi": f"{OUT}/PlayfairDisplay-Italic.ttf",
    "m": f"{OUT}/Montserrat.ttf",
    "mi": f"{OUT}/Montserrat-Italic.ttf",
}

# fenêtre photo : 940 x 1253 = 0.7502 (3:4)
WX0, WY0, WX1, WY1 = 70, 300, 1010, 1553
WW, WH = WX1 - WX0, WY1 - WY0

AUDIO = json.load(open(f"{CACHE}/audio_duration.json"))
DUR = float(AUDIO["duration"])
FRAMES = int(round(DUR * FPS))

XF = 0.55          # durée des fondus enchaênés visuels

rng = np.random.default_rng(7)
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
SWEEP_GRID = _xx + 0.62 * _yy


def sweep_on_mask(mask, t, start, dur=1.15, amp=0.55):
    p = (t - start) / dur
    if p <= 0 or p >= 1:
        return None
    pos = -500 + p * 2300
    band = np.exp(-((SWEEP_GRID - pos) / 130.0) ** 2) * amp
    return mask * band


# ----------------------------------------------------------------------------- utils
def font(kind, size):
    return ImageFont.truetype(FONT[kind], size)


def smoothstep(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


def clamp01(x):
    return np.clip(x, 0.0, 1.0)


def tracked_width(fnt, text, tracking):
    if not text:
        return 0
    return sum(fnt.getlength(c) for c in text) + tracking * (len(text) - 1)


def draw_tracked(dr, xy, text, fnt, tracking, fill=255, stroke=0.0):
    """dessine caractère par caractère avec interlettrage (x, y = baseline gauche)."""
    x, y = xy
    for i, ch in enumerate(text):
        dr.text((x, y), ch, font=fnt, fill=fill, anchor="ls",
                stroke_width=stroke, stroke_fill=fill)
        x += fnt.getlength(ch) + tracking


def mask_to_float(img):
    return np.asarray(img.convert("L"), dtype=np.float32) / 255.0


def composite(base, mask, color=1.0, alpha=1.0):
    a = mask * alpha
    return base * (1.0 - a) + color * a


def gauss(a, r):
    im = Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8))
    im = im.filter(ImageFilter.GaussianBlur(r))
    return np.asarray(im, dtype=np.float32) / 255.0


# ----------------------------------------------------------------------------- photo
def grade_photo(path):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    g = np.asarray(im.convert("L"), dtype=np.float32) / 255.0
    lo, hi = np.percentile(g, [0.6, 99.4])
    g = clamp01((g - lo) / max(1e-3, hi - lo))
    g = g ** 0.96
    g = 0.5 + (g - 0.5) * 1.24          # contraste franc mais sans écraser les visages
    g = clamp01(g * 1.03 - 0.015)       # noirs profonds
    img = Image.fromarray((g * 255).astype(np.uint8))
    img = img.filter(ImageFilter.UnsharpMask(radius=2.4, percent=82, threshold=2))
    a = np.asarray(img, dtype=np.float32) / 255.0
    bloom = np.asarray(img.filter(ImageFilter.GaussianBlur(16)), dtype=np.float32) / 255.0
    a = 1 - (1 - a) * (1 - 0.13 * bloom)   # halo argentique
    # vignettage
    h, w = a.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) / 1.414
    a *= (1 - 0.28 * r ** 2.0)
    a = clamp01(a)
    # taille de travail : hauteur max 1600
    scale = min(1.0, 1600 / max(a.shape))
    if scale < 1.0:
        im2 = Image.fromarray((a * 255).astype(np.uint8)).resize(
            (int(w * scale), int(h * scale)), Image.LANCZOS)
        a = np.asarray(im2, dtype=np.float32) / 255.0
    return a


def load_photo(path):
    key = os.path.basename(path).replace(".jpg", "")
    f = f"{CACHE}/grade-{key}.png"
    if os.path.exists(f):
        return np.asarray(Image.open(f), dtype=np.float32) / 255.0
    a = grade_photo(path)
    Image.fromarray((a * 255).astype(np.uint8)).save(f)
    return a


def make_background(a):
    """fond 1080x1920 : même photo, flou profond, très sombre."""
    h, w = a.shape
    s = max(W / w, H / h) * 1.08
    im = Image.fromarray((a * 255).astype(np.uint8)).resize(
        (int(w * s) + 1, int(h * s) + 1), Image.LANCZOS)
    iw, ih = im.size
    left = (iw - W) // 2
    top = (ih - H) // 2
    im = im.crop((left, top, left + W, top + H)).filter(ImageFilter.GaussianBlur(34))
    b = np.asarray(im, dtype=np.float32) / 255.0
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 1.414
    b *= (0.55 - 0.40 * r ** 1.5)
    # halo de scène derrière la fenêtre
    halo = np.exp(-(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - (WY0 + WH * 0.45)) / (H * 0.34)) ** 2)) * 0.10
    return b + halo


def make_window_fill(a):
    """fond flou (format fenêtre) pour les photos plus étroites que 3:4."""
    h, w = a.shape
    s = max(WW / w, WH / h)
    im = Image.fromarray((a * 255).astype(np.uint8)).resize(
        (int(w * s) + 1, int(h * s) + 1), Image.LANCZOS)
    iw, ih = im.size
    left, top = (iw - WW) // 2, (ih - WH) // 2
    im = im.crop((left, top, left + WW, top + WH)).filter(ImageFilter.GaussianBlur(26))
    f = np.asarray(im, dtype=np.float32) / 255.0
    return f * 0.42


# ----------------------------------------------------------------------------- typo
def build_text(items, block_bottom=None, block_center=None, maxw=760, center_x=W // 2):
    """items = [{'kind':'eyebrow'|'display'|'line', 'text':..., 'size':..., 'tracking':...}]
    Renvoie (mask, shadow_mask, bbox)."""
    pad = 40
    canvas = Image.new("L", (W, H), 0)
    dr = ImageDraw.Draw(canvas)
    # mesures
    rows = []
    total = 0
    for it in items:
        kind = it.get("kind", "line")
        size = it["size"]
        fnt = font(it.get("font", "pfi" if kind != "eyebrow" else "m"), size)
        tracking = it.get("tracking", 0)
        text = it["text"]
        lines = it.get("lines") or [text]
        lh = it.get("lh", int(size * (1.34 if kind != "eyebrow" else 1.5)))
        gap_before = it.get("gap_before", 0)
        widths = [tracked_width(fnt, l, tracking) for l in lines]
        wmax = max(widths) if widths else 0
        if wmax > maxw:                      # auto-ajustement à la largeur utile
            k = maxw / wmax
            size = max(30, int(size * k))
            fnt = font(it.get("font", "pfi" if kind != "eyebrow" else "m"), size)
            lh = it.get("lh", int(size * (1.34 if kind != "eyebrow" else 1.5)))
            lh = int(lh * k)
            widths = [tracked_width(fnt, l, tracking) for l in lines]
            wmax = max(widths) if widths else 0
        rows.append(dict(fnt=fnt, tracking=tracking, lines=lines, lh=lh,
                         w=wmax, gap=gap_before,
                         alpha=it.get("alpha", 255), size=size, stroke=it.get("stroke", 0.0)))
        total += gap_before + lh * len(lines)

    if block_center is not None:
        y = block_center - total / 2
    else:
        y = block_bottom - total
    y0 = y
    for r in rows:
        y += r["gap"]
        for ln in r["lines"]:
            tw = tracked_width(r["fnt"], ln, r["tracking"])
            x = center_x - tw / 2
            draw_tracked(dr, (x, y + r["lh"] * 0.78), ln, r["fnt"], r["tracking"],
                         fill=int(r["alpha"]), stroke=r["stroke"])
            y += r["lh"]
    mask = np.asarray(canvas, dtype=np.float32) / 255.0
    shadow = gauss(mask, 13) * 1.0
    return mask, shadow, (y0, y)


HEADER_ITEMS = None


def build_header():
    canvas = Image.new("L", (W, H), 0)
    dr = ImageDraw.Draw(canvas)
    fnt = font("m", 26)
    draw_tracked(dr, (100, 228), "13 · 11 · 2026", fnt, 7.4, fill=255, stroke=0.45)
    tw = tracked_width(fnt, "WTBW", 8.0)
    draw_tracked(dr, (W - 100 - tw, 228), "WTBW", fnt, 8.0, fill=255, stroke=0.45)
    dr.line([(100, 256), (W - 100, 256)], fill=120, width=1)
    return np.asarray(canvas, dtype=np.float32) / 255.0


# ----------------------------------------------------------------------------- ornements
_ORN_CACHE = {}


def _supersampled(size, fn, ss=3):
    s = ss
    im = Image.new("L", (size[0] * s, size[1] * s), 0)
    dr = ImageDraw.Draw(im)
    fn(dr, s)
    return im.resize(size, Image.LANCZOS)


def ornament_flourish(p, width=210, color_alpha=1.0):
    """petit filet courbe symétrique avec losange central."""
    key = ("fl", round(p, 2), width)
    if key in _ORN_CACHE:
        return _ORN_CACHE[key]
    w, h = width, 34
    def draw(dr, s):
        c = w / 2 * s
        yy = h / 2 * s
        L = (w / 2 - 6) * s * ease_out(p)
        steps = 60
        for i in range(steps):
            q = i / (steps - 1)
            x = c - L * q
            y = yy + math.sin(q * math.pi * 1.0) * 3.0 * s * (1 - q * 0.35)
            dr.ellipse([x - 0.9 * s, y - 0.9 * s, x + 0.9 * s, y + 0.9 * s], fill=int(205 * color_alpha))
            dr.ellipse([2 * c - x - 0.9 * s, y - 0.9 * s, 2 * c - x + 0.9 * s, y + 0.9 * s], fill=int(205 * color_alpha))
        if p > 0.75:
            q = smoothstep((p - 0.75) / 0.25)
            d = 5.0 * s * q
            dr.polygon([(c, yy - d), (c + d, yy), (c, yy + d), (c - d, yy)], fill=int(235 * color_alpha))
    im = _supersampled((w, h), draw)
    _ORN_CACHE[key] = im
    return im


def ornament_heart(p, size=64, alpha=235):
    key = ("ht", round(p, 2), size)
    if key in _ORN_CACHE:
        return _ORN_CACHE[key]
    def draw(dr, s):
        pts = []
        n = 180
        m = max(2, int(n * ease_out(p)))
        for i in range(m):
            t = 2 * math.pi * i / (n - 1)
            x = 16 * math.sin(t) ** 3
            y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
            pts.append((size / 2 * s + x * s * size / 44, size / 2 * s + y * s * size / 44))
        if len(pts) > 1:
            dr.line(pts, fill=int(alpha), width=int(2.1 * s), joint="curve")
    im = _supersampled((size, size), draw)
    _ORN_CACHE[key] = im
    return im


def ornament_flower(p, size=54, alpha=210, petals=5, rot=0.0):
    key = ("flw", round(p, 2), size, petals, round(rot, 2))
    if key in _ORN_CACHE:
        return _ORN_CACHE[key]
    def draw(dr, s):
        c = size / 2 * s
        r = size * 0.30 * s * ease_out(p)
        for k in range(petals):
            a = rot + 2 * math.pi * k / petals - math.pi / 2
            dr.ellipse([c + math.cos(a) * r - r * 0.42, c + math.sin(a) * r - r * 0.42,
                        c + math.cos(a) * r + r * 0.42, c + math.sin(a) * r + r * 0.42],
                       outline=int(alpha), width=max(1, int(1.5 * s)))
        if p > 0.6:
            q = smoothstep((p - 0.6) / 0.4)
            dr.ellipse([c - 1.6 * s * q, c - 1.6 * s * q, c + 1.6 * s * q, c + 1.6 * s * q], fill=int(alpha))
    im = _supersampled((size, size), draw)
    _ORN_CACHE[key] = im
    return im


def ornament_arrow(p, w=340, h=250, alpha=215, flip=False):
    """flèche courbe dessinée à la main, pointe en cœur discret."""
    key = ("ar", round(p, 2), w, h, flip)
    if key in _ORN_CACHE:
        return _ORN_CACHE[key]
    def draw(dr, s):
        # bézier de (w*0.95, h*0.90) vers (w*0.18, h*0.22)
        pts = []
        p0 = (w * 0.93, h * 0.92); p1 = (w * 0.55, h * 1.02); p2 = (w * 0.20, h * 0.55); p3 = (w * 0.24, h * 0.20)
        n = 120
        m = max(2, int(n * ease_out(p)))
        for i in range(m):
            t = i / (n - 1)
            x = ((1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0])
            y = ((1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1])
            pts.append((x * s, y * s))
        if len(pts) > 1:
            dr.line(pts, fill=int(alpha), width=int(2.0 * s), joint="curve")
        if p > 0.82:
            q = smoothstep((p - 0.82) / 0.18)
            ex, ey = pts[-1]
            a = math.radians(-108)
            l = 26 * s * q
            for da in (0.42, -0.42):
                dr.line([(ex, ey), (ex + math.cos(a + da) * l, ey + math.sin(a + da) * l)],
                        fill=int(alpha), width=int(2.0 * s))
    im = _supersampled((w, h), draw)
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    _ORN_CACHE[key] = im
    return im


def ornament_sparkle(p, size=40, alpha=190):
    key = ("sp", round(p, 2), size)
    if key in _ORN_CACHE:
        return _ORN_CACHE[key]
    def draw(dr, s):
        c = size / 2 * s
        r = size * 0.42 * s * ease_out(p)
        for k in range(4):
            a = math.pi / 2 * k
            dr.line([(c - math.cos(a) * r, c - math.sin(a) * r),
                     (c + math.cos(a) * r, c + math.sin(a) * r)], fill=int(alpha), width=max(1, int(1.4 * s)))
        d = r * 0.22
        dr.ellipse([c - d, c - d, c + d, c + d], fill=int(alpha))
    im = _supersampled((size, size), draw)
    _ORN_CACHE[key] = im
    return im


# ----------------------------------------------------------------------------- particules
def make_particle_sprites():
    sprites = []
    for r in (2, 3, 5):
        im = Image.new("L", (r * 8, r * 8), 0)
        dr = ImageDraw.Draw(im)
        dr.ellipse([r * 8 / 2 - r, r * 8 / 2 - r, r * 8 / 2 + r, r * 8 / 2 + r], fill=255)
        sprites.append(im.filter(ImageFilter.GaussianBlur(0.6)))
    return sprites


PARTICLES = make_particle_sprites()
PARTICLE_SEEDS = [
    (0.08, 0.15, 0.035, 1), (0.22, 0.62, 0.028, 0), (0.41, 0.31, 0.041, 0), (0.63, 0.78, 0.026, 1),
    (0.79, 0.22, 0.047, 0), (0.91, 0.55, 0.031, 0), (0.34, 0.86, 0.022, 1), (0.55, 0.09, 0.038, 0),
    (0.72, 0.44, 0.025, 0), (0.15, 0.94, 0.033, 1), (0.86, 0.81, 0.021, 0), (0.48, 0.52, 0.018, 0),
]


def draw_particles(frame, t, intensity=1.0):
    for i, (x0, y0, sp, sz) in enumerate(PARTICLE_SEEDS):
        phase = (t * sp + i * 0.137) % 1.0
        y = H * (y0 - phase * 0.55 - 0.1)
        x = W * x0 + 26 * math.sin(2 * math.pi * (phase * 1.3 + i))
        if y < -40 or y > H + 40:
            continue
        a = 0.05 + 0.10 * math.sin(math.pi * phase) * intensity
        a *= 0.55 + 0.45 * math.sin(t * 0.7 + i)
        if a <= 0.004:
            continue
        spr = PARTICLES[sz]
        m = mask_to_float(spr)
        y0i, x0i = int(y - spr.height / 2), int(x - spr.width / 2)
        # clipping
        ya, yb = max(0, y0i), min(H, y0i + spr.height)
        xa, xb = max(0, x0i), min(W, x0i + spr.width)
        if ya >= yb or xa >= xb:
            continue
        sub = m[ya - y0i:yb - y0i, xa - x0i:xb - x0i]
        frame[ya:yb, xa:xb] = composite(frame[ya:yb, xa:xb], sub, 1.0, max(0.0, a))


# ----------------------------------------------------------------------------- scene
class Shot:
    def __init__(self, photo, t0, t1, items=None, zoom=(1.03, 1.10), pan=(0.0, 0.0),
                 text_center=None, ornaments=None, bg_boost=1.0, fit="cover"):
        self.fit = fit
        self.photo_path = f"{ROOT}/{photo}"
        self.img = load_photo(self.photo_path)
        self.fill = None
        self.bg = make_background(self.img)
        self.t0, self.t1 = t0, t1
        self.items = items or []
        self.zoom = zoom
        self.pan = pan
        self.text_center = text_center
        self.ornaments = ornaments or []
        self.mask, self.shadow, self.bbox = build_text(items, block_center=text_center) if items else (None, None, None)
        self.bg_boost = bg_boost
        if fit == "contain":
            self.fill = make_window_fill(self.img)

    # --- contenu de la fenêtre
    def window(self, t):
        local = (t - self.t0) / max(1e-6, (self.t1 - self.t0))
        z = self.zoom[0] + (self.zoom[1] - self.zoom[0]) * smoothstep(local)
        a = self.img
        h, w = a.shape
        if self.fit == "contain":
            return self.window_contain(t, local, z)
        # cadrage contenant (0.75) puis zoom
        s = max(WW / w, WH / h) * z
        cw, ch = WW / s, WH / s
        cx = w / 2 + self.pan[0] * w * (local - 0.5)
        cy = h / 2 + self.pan[1] * h * (local - 0.5)
        cx = min(max(cx, cw / 2), w - cw / 2)
        cy = min(max(cy, ch / 2), h - ch / 2)
        box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
        im = Image.fromarray((a * 255).astype(np.uint8)).crop(box).resize((WW, WH), Image.BICUBIC)
        win = np.asarray(im, dtype=np.float32) / 255.0

        # effet vague (déplacement horizontal sinusoïdal lent)
        ys = np.arange(WH, dtype=np.float32)[:, None]
        off = 1.9 * np.sin(2 * np.pi * (ys / 210.0 - t * 0.16))
        xs = np.arange(WW, dtype=np.float32)[None, :] + off
        x0 = np.floor(xs).astype(np.int32)
        fx = xs - x0
        x0 = np.clip(x0, 0, WW - 1)
        x1 = np.clip(x0 + 1, 0, WW - 1)
        win = (np.take_along_axis(win, x0, axis=1) * (1 - fx)
               + np.take_along_axis(win, x1, axis=1) * fx)

        # balayage de lumière doux
        sweep_pos = -0.35 + 1.7 * local
        xx = np.arange(WW, dtype=np.float32)[None, :] / WW
        yy = np.arange(WH, dtype=np.float32)[:, None] / WH
        d = np.abs(xx * 0.75 + yy * 0.55 - (sweep_pos * 0.9 + yy * 0.15))
        band = np.exp(-(d ** 2) / (2 * 0.05 ** 2)) * 0.075
        win = 1 - (1 - win) * (1 - band)
        return clamp01(win)

    def window_contain(self, t, local, z):
        a = self.img
        h, w = a.shape
        s = min(WW / w, WH / h) * z
        cw, ch = w * s, h * s
        cx = WW / 2 + self.pan[0] * WW * (local - 0.5)
        cy = WH / 2 + self.pan[1] * WH * (local - 0.5)
        cx = min(max(cx, cw / 2), WW - cw / 2)
        cy = min(max(cy, ch / 2), WH - ch / 2)
        iw2, ih2 = max(1, int(round(cw))), max(1, int(round(ch)))
        im = Image.fromarray((a * 255).astype(np.uint8)).resize((iw2, ih2), Image.BICUBIC)
        if im.width > WW or im.height > WH:      # zoom : on rogne au centre
            l = max(0, (im.width - WW) // 2)
            t = max(0, (im.height - WH) // 2)
            im = im.crop((l, t, l + min(WW, im.width), t + min(WH, im.height)))
        win = self.fill.copy()
        x0, y0 = int(round(cx - cw / 2)), int(round(cy - ch / 2))
        x0 = min(max(0, x0), WW - im.width)
        y0 = min(max(0, y0), WH - im.height)
        win[y0:y0 + im.height, x0:x0 + im.width] = np.asarray(im, dtype=np.float32) / 255.0
        # ourlet lumineux du bord de la photo (effet tirage posé)
        win[y0, x0:x0 + im.width] = np.maximum(win[y0, x0:x0 + im.width], 0.55)
        win[y0 + im.height - 1, x0:x0 + im.width] = np.maximum(
            win[y0 + im.height - 1, x0:x0 + im.width], 0.55)
        ys = np.arange(WH, dtype=np.float32)[:, None]
        off = 1.9 * np.sin(2 * np.pi * (ys / 210.0 - t * 0.16))
        xs = np.arange(WW, dtype=np.float32)[None, :] + off
        xi0 = np.floor(xs).astype(np.int32)
        fx = xs - xi0
        xi0 = np.clip(xi0, 0, WW - 1)
        xi1 = np.clip(xi0 + 1, 0, WW - 1)
        win = (np.take_along_axis(win, xi0, axis=1) * (1 - fx)
               + np.take_along_axis(win, xi1, axis=1) * fx)
        return clamp01(win)

    def background(self, t):
        local = (t - self.t0) / max(1e-6, (self.t1 - self.t0))
        z = 1.02 + 0.10 * smoothstep(local)
        b = self.bg
        # dérive lente : simple translation sous-échantillonnée
        dx = int(round(14 * (local - 0.5)))
        dy = int(round(10 * math.sin(local * math.pi)))
        b2 = np.roll(np.roll(b, dy, axis=0), dx, axis=1) * self.bg_boost
        return clamp01(b2 * z * 0.98)


# ----------------------------------------------------------------------------- cartes
class Card:
    def __init__(self, t0, t1, render):
        self.t0, self.t1 = t0, t1
        self.render = render


# ----------------------------------------------------------------------------- rendu
HEADER = build_header()


def scrim(win, where="bottom", strength=0.80):
    """assombrit le bas (ou le haut) de la fenêtre pour la lisibilité."""
    h, w = win.shape
    yy = np.arange(h, dtype=np.float32)[:, None] / h
    if where == "bottom":
        g = np.clip((yy - 0.48) / 0.52, 0, 1) ** 1.35
    else:
        g = np.clip((0.45 - yy) / 0.45, 0, 1) ** 1.5
    return win * (1 - strength * g)


def render_frame(t):
    frame = np.zeros((H, W), dtype=np.float32)
    shot_a = shot_b = None
    shot = None
    for s in SCENES:
        if s.t0 - XF / 2 <= t < s.t1 + XF / 2:
            if t < s.t0 + XF / 2:
                prev = [p for p in SCENES if p.t1 <= s.t0 + 1e-6]
                if prev:
                    shot_a, shot_b = prev[-1], s
            else:
                shot_b = s
            shot = s
            break

    if shot_a is not None and shot_b is not None:
        p = smoothstep((t - (shot_b.t0 - XF / 2)) / XF)
        fa = render_scene(shot_a, t)
        fb = render_scene(shot_b, t)
        frame = fa * (1 - p) + fb * p
        # micro flash argentique sur les coupes de refrain
        for cue in CUTS:
            d = abs(t - cue)
            if d < 0.10:
                frame = 1 - (1 - frame) * (1 - 0.35 * (1 - d / 0.10))
    else:
        frame = render_scene(shot_b if shot_b else SCENES[0], t)

    # en-tête (sauf carte titre)
    if t >= 5.35:
        ha = smoothstep((t - 5.35) / 0.8)
        frame = composite(frame, HEADER, 1.0, 0.86 * ha * (1 - smoothstep((t - 57.3) / 0.35) * 0.0))

    # poussières + grain
    draw_particles(frame, t, 1.9 if t > FINALE_T0 else 1.0)
    noise = rng.normal(0, 0.0085, (H, W)).astype(np.float32)
    frame = clamp01(frame + noise)

    # fondu d'ouverture / fermeture
    if t < 0.45:
        frame *= 0.55 + 0.45 * smoothstep(t / 0.45)
    end = DUR - 0.85
    if t > end:
        frame *= 1 - 0.62 * smoothstep((t - end) / 0.85)
    return frame


def paste_ornament(frame, im, x, y, alpha=1.0):
    m = mask_to_float(im)
    h, w = m.shape
    ya, yb = max(0, y), min(H, y + h)
    xa, xb = max(0, x), min(W, x + w)
    if ya >= yb or xa >= xb:
        return
    sub = m[ya - y:yb - y, xa - x:xb - x]
    frame[ya:yb, xa:xb] = composite(frame[ya:yb, xa:xb], sub, 1.0, alpha)


def render_scene(scene, t):
    return scene.render(t)


def scene_shot(shot):
    def r(t):
        frame = shot.background(t).copy()
        win = shot.window(t)
        local = (t - shot.t0) / max(1e-6, (shot.t1 - shot.t0))
        # scrim derrière le texte
        if shot.items:
            win = scrim(win, "bottom", 0.88)
        frame[WY0:WY1, WX0:WX1] = win

        # cadre fin + coins
        frame[WY0, WX0:WX1] = np.maximum(frame[WY0, WX0:WX1], 0.70)
        frame[WY1 - 1, WX0:WX1] = np.maximum(frame[WY1 - 1, WX0:WX1], 0.70)
        frame[WY0:WY1, WX0] = np.maximum(frame[WY0:WY1, WX0], 0.70)
        frame[WY0:WY1, WX1 - 1] = np.maximum(frame[WY0:WY1, WX1 - 1], 0.70)
        # filet extérieur décalé (mat de tirage)
        off = 9
        frame[WY0 - off, WX0 - off:WX1 + off] = np.maximum(frame[WY0 - off, WX0 - off:WX1 + off], 0.22)
        frame[WY1 - 1 + off, WX0 - off:WX1 + off] = np.maximum(frame[WY1 - 1 + off, WX0 - off:WX1 + off], 0.22)
        frame[WY0 - off:WY1 + off, WX0 - off] = np.maximum(frame[WY0 - off:WY1 + off, WX0 - off], 0.22)
        frame[WY0 - off:WY1 + off, WX1 - 1 + off] = np.maximum(frame[WY0 - off:WY1 + off, WX1 - 1 + off], 0.22)
        for (cx, cy, sx, sy) in ((WX0, WY0, 1, 1), (WX1 - 1, WY0, -1, 1),
                                 (WX0, WY1 - 1, 1, -1), (WX1 - 1, WY1 - 1, -1, -1)):
            for i in range(30):
                x, y = cx + sx * i, cy
                if 0 <= x < W:
                    frame[y, x] = max(frame[y, x], 0.92)
                x, y = cx, cy + sy * i
                if 0 <= y < H:
                    frame[y, x] = max(frame[y, x], 0.92)

        # ombre intérieure douce du cadre
        inner = 46
        for i in range(inner):
            a = (1 - i / inner) ** 2 * 0.30
            frame[WY0 + i, WX0:WX1] *= (1 - a)
            frame[WY1 - 1 - i, WX0:WX1] *= (1 - a * 0.8)

        # ornements
        for kind, params in shot.ornaments:
            pr = ease_out(min(1.0, max(0.0, (local - params.get("delay", 0.25)) / params.get("dur", 1.1))))
            if pr <= 0.01:
                continue
            if kind == "flower":
                im = ornament_flower(pr, size=params.get("size", 54), alpha=params.get("alpha", 200),
                                     petals=params.get("petals", 5), rot=params.get("rot", 0.0))
            elif kind == "heart":
                im = ornament_heart(pr, size=params.get("size", 56), alpha=params.get("alpha", 220))
            elif kind == "sparkle":
                im = ornament_sparkle(pr, size=params.get("size", 40), alpha=params.get("alpha", 180))
            elif kind == "arrow":
                im = ornament_arrow(pr, w=params.get("w", 340), h=params.get("h", 250),
                                    alpha=params.get("alpha", 200), flip=params.get("flip", False))
            else:
                continue
            paste_ornament(frame, im, int(params["x"]), int(params["y"]), params.get("a", 1.0))

        # texte
        if shot.items:
            ta = smoothstep((t - shot.t0 - 0.30) / 0.65) * (1 - smoothstep((t - shot.t1 + 0.30) / 0.30))
            rise = (1 - smoothstep((t - shot.t0 - 0.30) / 0.8)) * 16
            if ta > 0.004:
                # filet sous le texte
                fl = ornament_flourish(min(1.0, max(0.0, (t - shot.t0 - 0.45) / 0.9)), width=190)
                fx = W // 2 - fl.width // 2
                fy = int(shot.bbox[1] + 26 + rise)
                paste_ornament(frame, fl, fx, fy, 0.75 * ta)
                sh = shot.shadow
                frame *= (1 - 0.78 * sh * ta)
                # décalage vertical : on glisse le masque
                dy = int(round(rise))
                if dy:
                    m = np.zeros_like(shot.mask)
                    if dy < H:
                        m[dy:] = shot.mask[:H - dy]
                else:
                    m = shot.mask
                frame = composite(frame, m, 1.0, ta)
        return frame
    return r


# ----------------------------------------------------------------------------- cartes : titre / finale
def title_card(t):
    frame = np.zeros((H, W), dtype=np.float32)
    # souffle lumineux très lent
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W * 0.5, H * 0.46
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / (W * 1.1)
    glow = np.exp(-(r ** 2) * 2.6) * 0.10 * (0.7 + 0.3 * math.sin(t * 0.9))
    frame += glow
    # filet horizontal qui se dessine
    p = ease_out(min(1.0, max(0.0, (t - 0.10) / 0.85)))
    if p > 0.01:
        half = 265 * p
        x0, x1 = int(W / 2 - half), int(W / 2 + half)
        frame[796, x0:x1] = np.maximum(frame[796, x0:x1], 0.60)
        frame[797, x0:x1] = np.maximum(frame[797, x0:x1], 0.28)
    # sur-titre
    a1 = smoothstep((t - 0.75) / 0.7)
    if a1 > 0.01:
        im = Image.new("L", (W, H), 0)
        dr = ImageDraw.Draw(im)
        fnt = font("m", 30)
        txt = "13 · 11 · 2026"
        tw = tracked_width(fnt, txt, 8.6)
        draw_tracked(dr, (W / 2 - tw / 2, 866), txt, fnt, 8.6, fill=255, stroke=0.6)
        m = mask_to_float(im)
        frame = composite(frame, m, 1.0, 0.92 * a1)
    # IMELDA lettre par lettre
    word = "IMELDA"
    fnt = font("pf", 170)
    tracking = 30
    total = tracked_width(fnt, word, tracking)
    x = W / 2 - total / 2
    im = Image.new("L", (W, H), 0)
    dr = ImageDraw.Draw(im)
    for i, ch in enumerate(word):
        ai = smoothstep((t - 1.05 - i * 0.075) / 0.55)
        if ai <= 0.01:
            x += fnt.getlength(ch) + tracking
            continue
        dy = (1 - ai) * 22
        dr.text((x, 1035 + dy), ch, font=fnt, fill=int(255 * ai), anchor="ls")
        x += fnt.getlength(ch) + tracking
    m = mask_to_float(im)
    frame = composite(frame, m, 1.0, 1.0)
    sw = sweep_on_mask(m, t, 2.10, 1.5, 0.55)
    if sw is not None:
        frame = np.clip(frame + sw, 0, 1)
    # sous-titre
    a3 = smoothstep((t - 2.05) / 0.7)
    if a3 > 0.01:
        im = Image.new("L", (W, H), 0)
        dr = ImageDraw.Draw(im)
        fnt2 = font("m", 31)
        txt = "JOYEUX ANNIVERSAIRE"
        tw = tracked_width(fnt2, txt, 9.5)
        draw_tracked(dr, (W / 2 - tw / 2, 1128), txt, fnt2, 9.5, fill=255, stroke=0.55)
        frame = composite(frame, mask_to_float(im), 1.0, 0.92 * a3)
    # trois losanges
    a4 = smoothstep((t - 2.75) / 0.8)
    if a4 > 0.01:
        for k, dx in enumerate((-30, 0, 30)):
            cx2 = W / 2 + dx
            d = 5.0 * a4
            frame[int(1180 - d):int(1180 + d) + 1, int(cx2 - d):int(cx2 + d) + 1] = np.maximum(
                frame[int(1180 - d):int(1180 + d) + 1, int(cx2 - d):int(cx2 + d) + 1], 0.80 * a4)
    return frame


def finale_card(t):
    frame = np.zeros((H, W), dtype=np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx = W * 0.5 + 40 * math.sin(0.21 * t)
    cy = H * 0.52 + 26 * math.cos(0.17 * t)
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / (W * 1.15)
    frame += np.exp(-(r ** 2) * 2.2) * 0.085 * (0.70 + 0.30 * math.sin(t * 0.8))
    base = t - FINALE_T0

    def fade(start, dur=0.7):
        return smoothstep((base - start) / dur)

    groups = []

    # sur-titre
    im = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(im)
    fnt = font("m", 31); txt = "JOYEUX ANNIVERSAIRE"
    tw = tracked_width(fnt, txt, 9.5)
    draw_tracked(dr, (W / 2 - tw / 2, 742), txt, fnt, 9.5, fill=255, stroke=0.55)
    groups.append((mask_to_float(im), 0.92, fade(0.28)))

    # Imelda
    im = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(im)
    fnt = font("pfi", 178); txt = "Imelda"
    tw = tracked_width(fnt, txt, 4)
    draw_tracked(dr, (W / 2 - tw / 2, 930), txt, fnt, 4, fill=255)
    groups.append((mask_to_float(im), 1.0, fade(0.55)))

    sw = sweep_on_mask(groups[1][0], t, FINALE_T0 + 1.0, 1.6, 0.5)
    if sw is not None:
        frame = np.clip(frame + sw, 0, 1)
    # filet
    p = ease_out(min(1, max(0, (base - 1.15) / 0.9)))
    if p > 0.01:
        half = 165 * p
        frame[1000, int(W / 2 - half):int(W / 2 + half)] = 0.62

    # vœux (2 lignes)
    im = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(im)
    fnt = font("pfi", 54)
    for i, ln in enumerate(("Que cette année te rende", "tout ce que ton sourire donne.")):
        tw = tracked_width(fnt, ln, 0.5)
        draw_tracked(dr, (W / 2 - tw / 2, 1096 + i * 70), ln, fnt, 0.5, fill=255)
    groups.append((mask_to_float(im), 1.0, fade(1.35)))

    # merci
    im = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(im)
    fnt = font("m", 27); txt = "MERCI D'EXISTER"
    tw = tracked_width(fnt, txt, 9.5)
    draw_tracked(dr, (W / 2 - tw / 2, 1275), txt, fnt, 9.5, fill=255, stroke=0.5)
    groups.append((mask_to_float(im), 0.88, fade(2.05)))

    for m, al, a in groups:
        if a > 0.004:
            frame = composite(frame, m, 1.0, al * a)

    # cœur dessiné
    hp = ease_out(min(1, max(0, (base - 2.35) / 1.1)))
    if hp > 0.01:
        h = ornament_heart(hp, size=58, alpha=230)
        paste_ornament(frame, h, W // 2 - 29, 1330, 0.95)
    # petite signature en bas
    a = fade(2.6, 0.9)
    if a > 0.01:
        im = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(im)
        fnt = font("m", 30); txt = "WTBW"
        tw = tracked_width(fnt, txt, 11.0)
        draw_tracked(dr, (W / 2 - tw / 2, 1520), txt, fnt, 11.0, fill=255, stroke=0.5)
        dr.line([(W / 2 - 215, 1552), (W / 2 - 45, 1552)], fill=130, width=1)
        dr.line([(W / 2 + 45, 1552), (W / 2 + 215, 1552)], fill=130, width=1)
        frame = composite(frame, mask_to_float(im), 1.0, 0.80 * a)

    # dérive infime : la carte respire (anti-gel)
    dx = int(round(2.2 * math.cos(0.31 * t)))
    dy = int(round(2.6 * math.sin(0.43 * t)))
    if dx or dy:
        out = np.zeros_like(frame)
        ys0, ys1 = max(0, dy), H + min(0, dy)
        xs0, xs1 = max(0, dx), W + min(0, dx)
        out[ys0:ys1, xs0:xs1] = frame[ys0 - dy:ys1 - dy, xs0 - dx:xs1 - dx]
        frame = out
    return frame




# =============================================================================
# PROJETS (un film = un refrain)
# =============================================================================
class Project:
    def __init__(self, cfg):
        self.cfg = cfg
        self.slug = cfg["slug"]
        self.duration = float(cfg["duration"])
        self.frames = int(round(self.duration * FPS))
        self.audio = cfg["audio"]
        self.title = cfg["title"]
        self.fin = cfg["finale"]
        self.shots = cfg["shots"]
        self.scenes = []
        self.finale_t0 = cfg["finale_t0"]
        self.cuts = cfg.get("cuts", [])
        self.build()

    def build(self):
        self.scenes.append(Card(0.0, self.title["t1"], lambda t: title_card_cfg(t, self.title)))
        for sh in self.shots:
            s = Shot(sh["photo"], sh["t0"], sh["t1"], items=sh["items"],
                     zoom=sh.get("zoom", (1.03, 1.11)), pan=sh.get("pan", (0, 0)),
                     text_center=sh.get("text_center", 1360), ornaments=sh.get("ornaments", []),
                     fit=sh.get("fit", "cover"))
            s.render = scene_shot(s)
            self.scenes.append(s)
        self.scenes.append(Card(self.finale_t0, self.duration, lambda t: finale_card_cfg(t, self.fin, self.finale_t0)))


def title_card_cfg(t, cfg):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W * 0.5, H * 0.46
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / (W * 1.1)
    frame = 0.055 + 0.075 * np.exp(-(r ** 2) * 1.4) * (1.0 + 0.10 * math.sin(t * 0.9))
    p = ease_out(min(1.0, max(0.0, (t - 0.10) / 0.85)))
    if p > 0.01:
        half = 265 * p
        frame[796, int(W / 2 - half):int(W / 2 + half)] = np.maximum(
            frame[796, int(W / 2 - half):int(W / 2 + half)], 0.60)
        frame[797, int(W / 2 - half):int(W / 2 + half)] = np.maximum(
            frame[797, int(W / 2 - half):int(W / 2 + half)], 0.28)

    a1 = smoothstep((t - 0.75) / 0.7)
    if a1 > 0.01:
        im = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(im)
        fnt = font("m", 30)
        tw = tracked_width(fnt, cfg["eyebrow"], 8.6)
        draw_tracked(dr, (W / 2 - tw / 2, 866), cfg["eyebrow"], fnt, 8.6, fill=255, stroke=0.6)
        frame = composite(frame, mask_to_float(im), 1.0, 0.92 * a1)

    word = cfg["word"]
    fnt = font("pf", 170)
    tracking = 30
    total = tracked_width(fnt, word, tracking)
    x = W / 2 - total / 2
    im = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(im)
    for i, ch in enumerate(word):
        ai = smoothstep((t - 1.05 - i * 0.075) / 0.55)
        if ai <= 0.01:
            x += fnt.getlength(ch) + tracking
            continue
        dy = (1 - ai) * 22
        dr.text((x, 1035 + dy), ch, font=fnt, fill=int(255 * ai), anchor="ls")
        x += fnt.getlength(ch) + tracking
    m = mask_to_float(im)
    frame = composite(frame, m, 1.0, 1.0)
    sw = sweep_on_mask(m, t, 2.05, 1.4, 0.55)
    if sw is not None:
        frame = np.clip(frame + sw, 0, 1)

    a3 = smoothstep((t - 2.05) / 0.7)
    if a3 > 0.01:
        im = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(im)
        fnt2 = font("m", 31)
        tw = tracked_width(fnt2, cfg["sub"], 9.5)
        draw_tracked(dr, (W / 2 - tw / 2, 1128), cfg["sub"], fnt2, 9.5, fill=255, stroke=0.55)
        frame = composite(frame, mask_to_float(im), 1.0, 0.92 * a3)

    a4 = smoothstep((t - 2.75) / 0.8)
    if a4 > 0.01:
        for dx in (-30, 0, 30):
            cx2 = W / 2 + dx
            d = 5.0 * a4
            frame[int(1180 - d):int(1180 + d) + 1, int(cx2 - d):int(cx2 + d) + 1] = np.maximum(
                frame[int(1180 - d):int(1180 + d) + 1, int(cx2 - d):int(cx2 + d) + 1], 0.80 * a4)
    return frame


def finale_card_cfg(t, cfg, t0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx = W * 0.5 + 40 * math.sin(0.21 * t)
    cy = H * 0.52 + 26 * math.cos(0.17 * t)
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / (W * 1.15)
    frame = 0.050 + 0.090 * np.exp(-(r ** 2) * 1.3) * (1.0 + 0.12 * math.sin(t * 0.8))
    base = t - t0

    def fade(start, dur=0.7):
        return smoothstep((base - start) / dur)

    groups = []
    im = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(im)
    fnt = font("m", 31)
    tw = tracked_width(fnt, cfg["eyebrow"], 9.5)
    draw_tracked(dr, (W / 2 - tw / 2, 742), cfg["eyebrow"], fnt, 9.5, fill=255, stroke=0.55)
    groups.append((mask_to_float(im), 0.92, fade(0.28)))

    im = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(im)
    fnt = font("pfi", 178)
    tw = tracked_width(fnt, cfg["word"], 4)
    draw_tracked(dr, (W / 2 - tw / 2, 930), cfg["word"], fnt, 4, fill=255)
    groups.append((mask_to_float(im), 1.0, fade(0.55)))

    sw = sweep_on_mask(groups[1][0], t, t0 + 1.0, 1.6, 0.5)
    if sw is not None:
        frame = np.clip(frame + sw, 0, 1)

    p = ease_out(min(1, max(0, (base - 1.15) / 0.9)))
    if p > 0.01:
        half = 165 * p
        frame[1000, int(W / 2 - half):int(W / 2 + half)] = 0.62

    im = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(im)
    fnt = font("pfi", 54)
    for i, ln in enumerate(cfg["wish"]):
        tw = tracked_width(fnt, ln, 0.5)
        draw_tracked(dr, (W / 2 - tw / 2, 1096 + i * 70), ln, fnt, 0.5, fill=255)
    groups.append((mask_to_float(im), 1.0, fade(1.35)))

    im = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(im)
    fnt = font("m", 27)
    tw = tracked_width(fnt, cfg["thanks"], 9.5)
    draw_tracked(dr, (W / 2 - tw / 2, 1275), cfg["thanks"], fnt, 9.5, fill=255, stroke=0.5)
    groups.append((mask_to_float(im), 0.88, fade(2.05)))

    for m, al, a in groups:
        if a > 0.004:
            frame = composite(frame, m, 1.0, al * a)

    hp = ease_out(min(1, max(0, (base - 2.35) / 1.1)))
    if hp > 0.01:
        h = ornament_heart(hp, size=58, alpha=230)
        paste_ornament(frame, h, W // 2 - 29, 1330, 0.95)

    a = fade(2.6, 0.9)
    if a > 0.01:
        im = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(im)
        fnt = font("m", 30)
        tw = tracked_width(fnt, cfg["brand"], 11.0)
        draw_tracked(dr, (W / 2 - tw / 2, 1520), cfg["brand"], fnt, 11.0, fill=255, stroke=0.5)
        dr.line([(W / 2 - 215, 1552), (W / 2 - 45, 1552)], fill=130, width=1)
        dr.line([(W / 2 + 45, 1552), (W / 2 + 215, 1552)], fill=130, width=1)
        frame = composite(frame, mask_to_float(im), 1.0, 0.80 * a)

    dx = int(round(2.2 * math.cos(0.31 * t)))
    dy = int(round(2.6 * math.sin(0.43 * t)))
    if dx or dy:
        out = np.zeros_like(frame)
        ys0, ys1 = max(0, dy), H + min(0, dy)
        xs0, xs1 = max(0, dx), W + min(0, dx)
        out[ys0:ys1, xs0:xs1] = frame[ys0 - dy:ys1 - dy, xs0 - dx:xs1 - dx]
        frame = out
    return frame


def render_frame_p(project, t):
    scenes = project.scenes
    shot_a = shot_b = None
    cur = None
    for s in scenes:
        if s.t0 - XF / 2 <= t < s.t1 + XF / 2:
            if t < s.t0 + XF / 2:
                prev = [p for p in scenes if p.t1 <= s.t0 + 1e-6]
                if prev:
                    shot_a, shot_b = prev[-1], s
            else:
                shot_b = s
            cur = s
            break

    if shot_a is not None and shot_b is not None:
        p = smoothstep((t - (shot_b.t0 - XF / 2)) / XF)
        fa = shot_a.render(t)
        fb = shot_b.render(t)
        frame = fa * (1 - p) + fb * p
        for cue in project.cuts:
            d = abs(t - cue)
            if d < 0.10:
                frame = 1 - (1 - frame) * (1 - 0.35 * (1 - d / 0.10))
    else:
        frame = (shot_b if shot_b else scenes[0]).render(t)

    if t >= 3.55:
        ha = smoothstep((t - 3.55) / 0.8)
        frame = composite(frame, HEADER, 1.0, 0.86 * ha)

    draw_particles(frame, t, 1.9 if t > project.finale_t0 else 1.0)
    noise = rng.normal(0, 0.0118, (H, W)).astype(np.float32)
    flicker = 1.0 + 0.016 * math.sin(t * 43.0) + 0.010 * math.sin(t * 17.7 + 1.1)
    frame = clamp01(frame * flicker + noise)

    if t < 0.45:
        frame *= 0.55 + 0.45 * smoothstep(t / 0.45)
    end = project.duration - 0.85
    if t > end:
        frame *= 1 - 0.62 * smoothstep((t - end) / 0.85)
    return frame


def encode(project):
    out = f"{OUT}/livrables/{project.cfg['file']}"
    cmd = [FF, "-y", "-hide_banner", "-loglevel", "warning",
           "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0",
           "-i", project.audio,
           "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-pix_fmt", "yuv420p",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
           "-c:a", "copy", "-shortest", "-movflags", "+faststart", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(project.frames):
        t = i / FPS
        f = clamp01(render_frame_p(project, t))
        proc.stdin.write((f * 255 + 0.5).astype(np.uint8).tobytes())
        if i % 150 == 0:
            print(f"[{project.slug}] frame {i}/{project.frames} t={t:.2f}", flush=True)
    proc.stdin.close()
    code = proc.wait()
    print(f"[{project.slug}] encode exit {code} -> {out}")
    return code
