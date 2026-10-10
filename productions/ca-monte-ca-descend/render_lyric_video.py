#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""« Ça monte, ça descend » — clip lyrics 9:16 (1080×1920, 30 fps) — prompt v5.7.

Ce que fait le script (sans rien inventer de plus que ce qui est écrit ci-dessous) :
  · lit les horodatages des paroles (`Ça monte, Ça descend.txt`, 55 vers horodatés) ;
  · calcule la durée d'affichage de chaque vers et les fenêtres sans texte ≥ 5 s
    (→ clochettes CTA) ; écrit `timings_audited.json` ;
  · fonds IA sans texte ni visage (4 scènes, Ken Burns + fondu croisé) ;
  · carte d'accueil : « Regarde jusqu'à la fin… » (0 → 4,9 s) ;
  · paroles mode mixte centrées (mot actif or, mots passés crème, vague d'eau) ;
  · badge « Dsky » par vers (fondu 0,4 s, opacité ≤ 75 %), SANS drapeau ;
  · clochette vectorielle premium : balancement, pulsation, ondes, étincelles, ABONNE-TOI,
    PARTAGE en pastille, rappel « Clique sur la cloche, puis PARTAGE » ;
  · carte finale : « Merci d'avoir regardé » + code 1010 (aucun contact).

Usage :  python3 render_lyric_video.py            (rendu complet → livrables/)
         python3 render_lyric_video.py --preview  (quelques images de contrôle en /tmp)
"""
import os
import re
import sys
import json
import math
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

REPO = '/home/user/lyric'
ROOT = os.path.join(REPO, 'productions/ca-monte-ca-descend')
SRC = os.path.join(REPO, 'Ça monte_ ça descend.mp3')
LRC = os.path.join(ROOT, 'timings_source.lrc')   # horodatages fournis par l'artiste (2026-10-10)
FONT = os.path.join(REPO, 'dsky-quotes/assets/fonts/Montserrat.ttf')
FFMPEG = os.environ.get('FFMPEG', '/tmp/lyric-venv/bin/ffmpeg')
OUT = os.path.join(REPO, 'livrables/Ca_monte_ca_descend_9x16_v1.mp4')
PREVIEW_DIR = '/tmp/work/preview'

W, H, FPS = 1080, 1920, 30
AUDIO_DUR = 197.60           # durée décodée réelle (mesurée, ffmpeg -f null)
END_DUR = 5.0                # carte finale
TOTAL = AUDIO_DUR + END_DUR
CW, CH = 1188, 2112          # canevas Ken Burns (ratio 9:16)

GOLD = (255, 214, 110)
CREAM = (246, 236, 214)
CYAN = (92, 242, 255)
MAG = (255, 79, 216)
# Scènes avec le couple (personnages/), indexées par bg_for()
BG_FILES = [
    'personnages/scene-01-entree-club.jpg',      # 0 intro
    'personnages/scene-02-danse-couple.jpg',     # 1 couplet 1
    'personnages/scene-04-toast-pre-refrain.jpg',  # 2 pré-refrain
    'personnages/scene-05-drop-explosion.jpg',   # 3 drop
    'personnages/scene-06-rue-nuit.jpg',         # 4 couplet 2
    'personnages/scene-07-foule-refrain.jpg',    # 5 refrain répété
    'personnages/scene-08-pont-toit.jpg',        # 6 pont
    'personnages/scene-09-aube-fin.jpg',         # 7 outro + carte finale
    'personnages/scene-03-gros-plan-visage.jpg',  # 8 gros plan
]
OUTRO_BG = 7
CTA_LOOP = 4.0               # répétition de la séquence clochette (s)
CTA_MIN = 5.0                # seuil fenêtre sans parole (s)
CODE = '1010'
THANKS = "Merci d'avoir regardé"


# ---------------------------------------------------------------- temps & paroles
def load_lines():
    out = []
    for raw in open(LRC, encoding='utf-8'):
        s = raw.replace('\u200e', '').replace('\u200f', '').strip()
        m = re.match(r'\[(\d+):(\d+(?:\.\d+)?)\](.*)$', s)
        if m:
            t = int(m.group(1)) * 60 + float(m.group(2))
            out.append({'t0': round(t, 2), 'text': m.group(3).strip()})
    return out


def bg_for(text, t0):
    l = text.lower()
    if t0 >= 170:
        return OUTRO_BG                # outro
    if 'redescend' in l or 'remonter' in l:
        return 6                       # pont calme
    if t0 < 12 or l in ("yeah! let's go!", 'ça monte!', 'ça descend!'):
        return 0                       # intro club
    if 'regarde autour' in l:
        return 8                       # gros plan visage
    if 'ça monte, ça monte' in l:
        return 2                       # pré-refrain (build-up)
    if text.isupper() or 'ça monte, ça descend' in l:
        return 3 if t0 < 60 else 5     # drop 1 / refrain répété
    if 60 <= t0 < 120 and ('kissi' in l or "j'suis" in l or 'gbètché' in l or 'yiwan' in l
                           or 'nonvi' in l or 'dokpè' in l or 'avance' in l):
        return 4                       # couplet 2
    return 1                           # couplet 1


def build_timeline(lines):
    for i, L in enumerate(lines):
        nxt = lines[i + 1]['t0'] if i + 1 < len(lines) else AUDIO_DUR
        d = min(4.0, max(2.0, 0.07 * len(L['text']) + 1.2))   # hypothèse d'affichage (à valider à l'écoute)
        L['t1'] = round(min(L['t0'] + d, nxt), 2)
        L['bg'] = bg_for(L['text'], L['t0'])
        L['nxt'] = round(nxt, 2)


def bell_windows(lines):
    wins = []
    for L in lines:
        if L['nxt'] - L['t1'] >= CTA_MIN:
            wins.append((round(L['t1'], 2), round(L['nxt'], 2)))
    return wins


def cta_cycles(windows):
    cyc = []
    for a, b in windows:
        k = 0
        while a + CTA_LOOP * k < b - 1.0:
            cs = a + CTA_LOOP * k
            cyc.append((cs, min(CTA_LOOP, b - cs)))
            k += 1
    return cyc


def bg_segments(lines):
    segs = [(0.0, 0)]
    for L in lines:
        if L['bg'] != segs[-1][1]:
            segs.append((L['t0'], L['bg']))
    if segs[-1][1] != OUTRO_BG:
        segs.append((AUDIO_DUR, OUTRO_BG))
    return segs


# ---------------------------------------------------------------- typographie
_fonts = {}


def F(size, weight=800):
    k = (size, weight)
    if k not in _fonts:
        f = ImageFont.truetype(FONT, size)
        f.set_variation_by_axes([weight])
        _fonts[k] = f
    return _fonts[k]


def grad_img(w, h, c1, c2, horizontal=False):
    n = w if horizontal else h
    t = np.linspace(0, 1, n)
    c = np.array(c1, float)[None, :] * (1 - t[:, None]) + np.array(c2, float)[None, :] * t[:, None]
    if horizontal:
        arr = np.broadcast_to(c[None, :, :], (h, w, 3))
    else:
        arr = np.broadcast_to(c[:, None, :], (h, w, 3))
    out = np.dstack([arr, np.full((h, w), 255.0)]).astype(np.uint8)
    return Image.fromarray(out, 'RGBA')


def tsprite(text, size, weight=800, fill=CREAM, alpha=255, grad=None, track=0,
            glow=None, glow_r=12, glow_a=150, shadow=True):
    """Texte premium : ombre portée douce, halo optionnel, remplissage uni ou dégradé."""
    f = F(size, weight)
    ws = [f.getlength(c) for c in text]
    tw = sum(ws) + track * max(0, len(text) - 1)
    asc, desc = f.getmetrics()
    pad = int(size * 0.35) + (glow_r * 3 if glow else 0) + 10
    w, h = int(tw) + 2 * pad, int(asc + desc) + 2 * pad
    mask = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(mask)
    x, base = pad, pad + asc
    for c, wc in zip(text, ws):
        d.text((x, base), c, font=f, fill=255, anchor='ls')
        x += wc + track
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    if shadow:
        sh = Image.new('L', (w, h), 0)
        sh.paste(mask, (0, int(size * 0.06)))
        sh = sh.filter(ImageFilter.GaussianBlur(max(2, size * 0.07)))
        blk = Image.new('RGBA', (w, h), (0, 0, 0, 255))
        blk.putalpha(sh.point(lambda v: int(v * 0.55)))
        out.alpha_composite(blk)
    if glow:
        gl = mask.filter(ImageFilter.GaussianBlur(glow_r))
        gc = Image.new('RGBA', (w, h), tuple(glow) + (255,))
        gc.putalpha(gl.point(lambda v: min(255, int(v * glow_a / 255))))
        out.alpha_composite(gc)
    col = grad_img(w, h, grad[0], grad[1]) if grad else Image.new('RGBA', (w, h), tuple(fill) + (255,))
    col.putalpha(mask)
    out.alpha_composite(col)
    return scale_alpha(out, alpha / 255.0)


def scale_alpha(im, a):
    if a >= 0.999:
        return im
    im = im.copy()
    im.putalpha(im.getchannel('A').point(lambda v: int(v * a)))
    return im


def wrap(words, f, maxw):
    rows, cur = [], []
    for w in words:
        if cur and f.getlength(' '.join(cur + [w])) > maxw:
            rows.append(cur)
            cur = [w]
        else:
            cur.append(w)
    if cur:
        rows.append(cur)
    return rows


def fit(text, maxw, maxh, sizes, weight=800):
    words = text.split()
    for s in sizes:
        rows = wrap(words, F(s, weight), maxw)
        if len(rows) * s * 1.12 <= maxh:
            return s, rows
    s = sizes[-1]
    return s, wrap(words, F(s, weight), maxw)


def block(rows, size, weight=800, fill=CREAM, grad=None, alpha=255, glow=None, glow_a=150):
    sps = [tsprite(' '.join(r), size, weight, fill=fill, grad=grad, glow=glow, glow_a=glow_a, alpha=alpha)
           for r in rows]
    lh = size * 1.12
    w = max(s.width for s in sps)
    h = int(lh * len(sps) + size)
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for i, s in enumerate(sps):
        out.alpha_composite(s, ((w - s.width) // 2, int(i * lh + lh / 2 - s.height / 2 + size * 0.4)))
    return out


def center_paste(canvas, sp, cx, cy, dy=0):
    canvas.alpha_composite(sp, (int(round(cx - sp.width / 2)), int(round(cy - sp.height / 2 + dy))))


# ---------------------------------------------------------------- paroles (mode mixte)
def prep_line(L):
    size, rows = fit(L['text'], 740, 760, list(range(96, 47, -4)))
    f = F(size)
    lh = size * 1.12
    n = len(rows)
    y0 = 960 - (n - 1) * lh / 2
    sp = f.getlength(' ')
    words, gi = [], 0
    for r, row in enumerate(rows):
        wd = [f.getlength(w) for w in row]
        tot = sum(wd) + sp * (len(row) - 1)
        x = 540 - tot / 2
        cy = y0 + r * lh
        for w, wdi in zip(row, wd):
            words.append({'text': w, 'cx': x + wdi / 2, 'cy': cy, 'idx': gi, 'wt': len(w) + 1})
            x += wdi + sp
            gi += 1
    L['size'] = size
    L['words'] = words
    L['wt_total'] = sum(w['wt'] for w in words)


_wcache = {}


def word_sprite(li, wi, state, size, text):
    k = (li, wi, state, size)
    if k not in _wcache:
        if state == 'past':
            _wcache[k] = tsprite(text, size, 800, fill=CREAM, alpha=228)
        elif state == 'future':
            _wcache[k] = tsprite(text, size, 800, fill=(255, 255, 255), alpha=105)
        else:
            _wcache[k] = tsprite(text, size, 900, grad=((255, 242, 178), (255, 170, 50)),
                                 glow=(255, 190, 70), glow_r=10, glow_a=170)
    return _wcache[k]


def line_env(L, t):
    if t < L['t0']:
        return 0.0
    a = min(1.0, (t - L['t0']) / 0.12)
    if t > L['t1']:
        a *= max(0.0, 1 - (t - L['t1']) / 0.35)
    return a


def draw_lyrics(frame, t, lines):
    for li, L in enumerate(lines):
        if t < L['t0'] or t > L['t1'] + 0.35:
            continue
        env = line_env(L, t)
        if env <= 0:
            continue
        pos = (t - L['t0']) / max(0.01, L['t1'] - L['t0']) * L['wt_total']
        active = -1
        if t < L['t1']:
            acc = 0
            for w in L['words']:
                if pos < acc + w['wt']:
                    active = w['idx']
                    break
                acc += w['wt']
        for w in L['words']:
            if active == -1 or w['idx'] < active:
                st = 'past'
            elif w['idx'] == active:
                st = 'active'
            else:
                st = 'future'
            sp = scale_alpha(word_sprite(li, w['idx'], st, L['size'], w['text']), env)
            dy = 4.5 * math.sin(2 * math.pi * 0.9 * t + w['cx'] * 0.012)   # vague d'eau
            center_paste(frame, sp, w['cx'], w['cy'], dy)


# ---------------------------------------------------------------- fonds
def kb(img, t, k):
    """Ken Burns : zoom 1,02→1,08 (respiration), pan sinusoïdal."""
    z = 1.05 + 0.03 * math.sin(2 * math.pi * t / 9.0 + k)
    cw, ch = CW / z, CH / z
    ax = math.sin(2 * math.pi * t / 13.0 + 1.3 * k) * (CW - cw) / 2
    ay = math.cos(2 * math.pi * t / 17.0 + 0.7 * k) * (CH - ch) / 2
    x0 = (CW - cw) / 2 + ax
    y0 = (CH - ch) / 2 + ay
    return img.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))


def make_scrim():
    y = np.arange(H)[:, None].astype(float)
    a = 34 + 118 * np.exp(-((y - 960) / 430.0) ** 2)
    arr = np.zeros((H, W, 4), np.uint8)
    arr[:, :, 3] = np.clip(np.broadcast_to(a, (H, W)), 0, 255).astype(np.uint8)
    return Image.fromarray(arr, 'RGBA')


def bg_at(segs, t):
    i = 0
    for k, (ts, _) in enumerate(segs):
        if ts <= t:
            i = k
    cur = segs[i][1]
    prev = segs[i - 1][1] if i > 0 else cur
    mix = 1.0 if prev == cur else min(1.0, (t - segs[i][0]) / 0.8)
    return cur, prev, mix


# ---------------------------------------------------------------- clochette vectorielle
def make_bell():
    S = 3
    N = 560 * S
    c = 280 * S

    def P(x, y):
        return (c + x * S, c + y * S)

    def w_of(y):
        u = max(0.0, (y + 110) / 210.0)
        return 58 + 92 * u ** 1.5

    left = [(-w_of(y), y) for y in np.linspace(-110, 100, 90)]
    bottom = [(x, 100 + 12 * (1 - (x / 150.0) ** 2)) for x in np.linspace(-150, 150, 70)]
    right = [(w_of(y), y) for y in np.linspace(100, -110, 90)]
    pts = [P(x, y) for x, y in left + bottom + right]
    mask = Image.new('L', (N, N), 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)

    # dégradé métal : or clair → bronze
    sy = [-120, -40, 10, 60, 115]
    sc = np.array([(255, 246, 196), (246, 199, 90), (214, 140, 36), (176, 98, 20), (104, 58, 10)], float)
    yu = (np.arange(N) - c) / S
    col = np.stack([np.interp(yu, sy, sc[:, k]) for k in range(3)], axis=1)
    arr = np.zeros((N, N, 4), np.uint8)
    arr[:, :, :3] = col[:, None, :]
    arr[:, :, 3] = 255
    body = Image.fromarray(arr, 'RGBA')
    body.putalpha(mask)
    bell = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    bell.alpha_composite(body)

    def layer():
        return Image.new('RGBA', (N, N), (0, 0, 0, 0))

    hl = layer()
    ImageDraw.Draw(hl).ellipse([*P(-116, -72), *P(-64, 34)], fill=(255, 255, 255, 150))
    hl = hl.filter(ImageFilter.GaussianBlur(6 * S))
    hl.putalpha(ImageChops.multiply(hl.getchannel('A'), mask))
    bell.alpha_composite(hl)

    hr = layer()
    ImageDraw.Draw(hr).ellipse([*P(70, -70), *P(92, 10)], fill=(255, 250, 225, 110))
    hr = hr.filter(ImageFilter.GaussianBlur(3 * S))
    hr.putalpha(ImageChops.multiply(hr.getchannel('A'), mask))
    bell.alpha_composite(hr)

    d = ImageDraw.Draw(bell)
    d.arc([*P(-150, 76), *P(150, 124)], start=0, end=180, fill=(255, 236, 170, 235), width=5 * S)
    d.rounded_rectangle([*P(-14, -122), *P(14, -104)], radius=5 * S, fill=(222, 168, 70, 255))
    d.rounded_rectangle([*P(-64, -116), *P(64, -100)], radius=6 * S, fill=(248, 206, 110, 255))
    d.ellipse([*P(-20, -168), *P(20, -128)], outline=(236, 186, 90, 255), width=9 * S)
    d.ellipse([*P(-17, 104), *P(17, 138)], fill=(255, 222, 134, 255), outline=(120, 70, 16, 255), width=3 * S)

    yy, xx = np.mgrid[0:N, 0:N]
    r = np.hypot(xx - c, yy - c) / (232 * S)
    a = np.clip(1 - r, 0, 1) ** 1.7 * 175
    harr = np.zeros((N, N, 4), np.uint8)
    harr[:, :, 0], harr[:, :, 1], harr[:, :, 2] = 255, 196, 96
    harr[:, :, 3] = a.astype(np.uint8)
    halo = Image.fromarray(harr, 'RGBA')
    sh = layer()
    ImageDraw.Draw(sh).ellipse([*P(-118, 136), *P(118, 160)], fill=(0, 0, 0, 170))
    halo.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7 * S)))

    return (bell.resize((560, 560), Image.LANCZOS), halo.resize((560, 560), Image.LANCZOS))


def scaled(img, s):
    if abs(s - 1) < 1e-3:
        return img
    n = int(round(560 * s))
    im = img.resize((n, n), Image.BILINEAR)
    out = Image.new('RGBA', (560, 560), (0, 0, 0, 0))
    off = (560 - n) // 2
    out.paste(im, (off, off), im)
    return out


def pill_sprites(text, size):
    ts = tsprite(text, size, 900, grad=(CYAN, MAG), track=4, glow=CYAN, glow_r=8, glow_a=90)
    pw, ph = ts.width + 130, int(size * 2.0)
    pad = 40
    W2, H2 = pw + 2 * pad, ph + 2 * pad
    mask = Image.new('L', (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw - 1, ph - 1], radius=ph // 2, fill=255)
    inner = Image.new('L', (pw, ph), 0)
    ImageDraw.Draw(inner).rounded_rectangle([5, 5, pw - 6, ph - 6], radius=ph // 2 - 5, fill=255)
    ring = ImageChops.subtract(mask, inner)
    body = Image.new('RGBA', (W2, H2), (0, 0, 0, 0))
    fillc = Image.new('RGBA', (pw, ph), (12, 10, 30, 228))
    body.paste(fillc, (pad, pad), mask)
    body.paste(grad_img(pw, ph, CYAN, MAG, horizontal=True), (pad, pad), ring)
    body.alpha_composite(ts, (pad + (pw - ts.width) // 2, pad + (ph - ts.height) // 2))
    glow = Image.new('RGBA', (W2, H2), tuple(CYAN) + (255,))
    gm = Image.new('L', (W2, H2), 0)
    gm.paste(ring, (pad, pad))
    glow.putalpha(gm.filter(ImageFilter.GaussianBlur(14)).point(lambda v: min(255, int(v * 1.6))))
    return glow, body


def make_arrow():
    im = Image.new('RGBA', (80, 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(10, 6), (70, 6), (40, 50)], fill=GOLD + (255,))
    return im.filter(ImageFilter.GaussianBlur(0.6))


def star(size, alpha):
    im = Image.new('RGBA', (size * 2, size * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size
    pts = []
    for i in range(8):
        ang = math.pi / 4 * i
        rr = size if i % 2 == 0 else size * 0.22
        pts.append((c + rr * math.cos(ang), c + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 246, 214, alpha))
    return im.filter(ImageFilter.GaussianBlur(0.8))


# ---------------------------------------------------------------- état global & rendu
ST = {}


def setup(lines):
    ST['bgs'] = [Image.open(os.path.join(ROOT, f)).convert('RGB').resize((CW, CH), Image.LANCZOS)
                 for f in BG_FILES]
    ST['scrim'] = make_scrim()
    for L in lines:
        prep_line(L)
    ST['lines'] = lines
    ST['bell'], ST['halo'] = make_bell()
    ST['glowp'], ST['pill'] = pill_sprites('PARTAGE', 104)
    ST['abonne'] = tsprite('ABONNE-TOI', 66, 900, grad=((255, 255, 255), (206, 232, 255)), track=7,
                           glow=CYAN, glow_r=8, glow_a=110)
    ST['remind'] = tsprite('Clique sur la cloche, puis PARTAGE', 34, 600, fill=CREAM, alpha=236)
    ST['arrow'] = make_arrow()
    # badge « Dsky » (sans drapeau)
    bt = tsprite('DSKY', 40, 800, fill=(255, 255, 255), track=5)
    bw, bh = bt.width + 90, 92
    badge = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
    ImageDraw.Draw(badge).rounded_rectangle([0, 0, bw - 1, bh - 1], radius=46,
                                            fill=(8, 6, 18, 150), outline=(255, 255, 255, 70), width=2)
    badge.alpha_composite(bt, ((bw - bt.width) // 2, (bh - bt.height) // 2))
    ST['badge'] = badge
    # carte d'accueil (0 → 4,9 s)
    s1, r1 = fit("Regarde jusqu'à la fin", 860, 300, list(range(120, 56, -4)), 900)
    ST['intro_a'] = block(r1, s1, 900, grad=((255, 242, 178), (255, 170, 50)), glow=GOLD, glow_a=130)
    s2, r2 = fit("pour découvrir comment proposer un son ou des lyrics à réaliser pour toi !",
                 860, 460, list(range(84, 46, -4)), 800)
    ST['intro_b'] = block(r2, s2, 800, fill=CREAM)
    # carte finale (sans contacts)
    s3, r3 = fit(THANKS, 860, 300, list(range(150, 66, -6)), 900)
    ST['thanks'] = block(r3, s3, 900, grad=((255, 242, 178), (255, 170, 50)), glow=GOLD, glow_a=120)
    s4, r4 = fit("Tu veux un son ou des lyrics à réaliser pour toi ?", 820, 220, [54, 50, 46, 42, 38], 600)
    ST['endsub'] = block(r4, s4, 600, fill=CREAM)
    ST['endcmd'] = tsprite('Commente le code', 46, 700, fill=CREAM, alpha=236)
    code = tsprite(CODE, 220, 900, grad=((255, 242, 178), (255, 170, 50)), glow=GOLD, glow_r=14, glow_a=160)
    cw_, ch_ = code.width + 170, 300
    box = Image.new('RGBA', (cw_, ch_), (0, 0, 0, 0))
    ImageDraw.Draw(box).rounded_rectangle([0, 0, cw_ - 1, ch_ - 1], radius=40, fill=(8, 6, 20, 205),
                                          outline=CYAN + (235,), width=5)
    box.alpha_composite(code, ((cw_ - code.width) // 2, (ch_ - code.height) // 2))
    ST['codebox'] = box
    ST['endfoot'] = tsprite('1 = ça monte   ·   0 = ça descend', 36, 600, fill=CREAM, alpha=222)
    ST['ringbuf'] = None


def render(t, segs, windows_cyc):
    cur, prev, mix = bg_at(segs, t)
    img = kb(ST['bgs'][cur], t, cur)
    if mix < 1.0:
        img = Image.blend(kb(ST['bgs'][prev], t, prev), img, mix)
    frame = img.convert('RGBA')
    frame.alpha_composite(ST['scrim'])

    lines = ST['lines']
    # badge « Dsky » : un fondu par vers, opacité max 75 %
    be = 0.0
    for L in lines:
        if L['t0'] <= t <= L['t1']:
            be = max(be, min(1.0, (t - L['t0']) / 0.4, (L['t1'] - t) / 0.4))
    if be > 0 and t < AUDIO_DUR:
        bd = ST['badge']
        frame.alpha_composite(scale_alpha(bd, 0.75 * be), ((W - bd.width) // 2, 160))

    # carte d'accueil
    if t < 2.25:
        a = min(1.0, t / 0.2) * min(1.0, (2.25 - t) / 0.25)
        if a > 0:
            center_paste(frame, scale_alpha(ST['intro_a'], a), 540, 800)
    elif t < 4.92:
        a = min(1.0, (t - 2.25) / 0.2) * min(1.0, (4.92 - t) / 0.25)
        if a > 0:
            center_paste(frame, scale_alpha(ST['intro_b'], a), 540, 800)

    # paroles
    if t < AUDIO_DUR:
        draw_lyrics(frame, t, lines)

    # clochettes CTA (fenêtres sans parole ≥ 5 s)
    for cs, cl in windows_cyc:
        if not (cs <= t < cs + cl):
            continue
        lt = t - cs
        env = min(1.0, lt / 0.35) * min(1.0, max(0.0, (cl - lt)) / 0.35)
        if env <= 0:
            continue
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * lt / 0.8)
        cx, cy = 540, 790
        # halo
        frame.alpha_composite(scale_alpha(ST['halo'], env * (0.55 + 0.45 * pulse)), (cx - 280, cy - 280))
        # cloche : balancement ±12° amorti (période 1,2 s) + pulsation 0,8 s
        ang = 12 * math.exp(-0.9 * lt) * math.cos(2 * math.pi * lt / 1.2)
        s = 1 + 0.035 * max(0.0, math.sin(2 * math.pi * lt / 0.8))
        bell = scaled(ST['bell'].rotate(ang, resample=Image.BICUBIC, center=(280, 150)), s)
        frame.alpha_composite(scale_alpha(bell, env), (cx - 280, cy - 280))
        # ondes + étincelles
        ring = Image.new('RGBA', (800, 800), (0, 0, 0, 0))
        rd = ImageDraw.Draw(ring)
        for k in (0, 1):
            p = ((lt - 0.45 * k) % 0.9) / 0.9
            rr = 150 + 170 * p
            col = CYAN if k == 0 else GOLD
            rd.ellipse([400 - rr, 400 - 20 - rr, 400 + rr, 400 - 20 + rr], outline=col + (int(200 * (1 - p)),), width=6)
        for k in range(3):
            th = 0.8 + 2.1 * k + lt * 0.5
            tw_ = max(0.0, math.sin(2 * math.pi * lt * 1.5 + 2 * k)) ** 2
            if tw_ > 0.02:
                st = star(int(10 + 8 * tw_), int(255 * tw_))
                rx, ry = 400 + 205 * math.cos(th), 380 + 205 * math.sin(th)
                ring.alpha_composite(st, (int(rx - st.width / 2), int(ry - st.height / 2)))
        frame.alpha_composite(scale_alpha(ring, env), (cx - 400, cy - 400))
        # flèche clignotante vers la cloche
        blink = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(2 * math.pi * lt * 2.5))
        frame.alpha_composite(scale_alpha(ST['arrow'], env * blink), (cx - 40, 556))
        # textes
        center_paste(frame, scale_alpha(ST['abonne'], env), cx, 1000)
        center_paste(frame, scale_alpha(ST['glowp'], env * (0.55 + 0.45 * pulse)), cx, 1180)
        center_paste(frame, scale_alpha(ST['pill'], env), cx, 1180)
        center_paste(frame, scale_alpha(ST['remind'], env), cx, 1322)

    # carte finale
    if t >= AUDIO_DUR:
        e = min(1.0, (t - AUDIO_DUR) / 0.5)
        center_paste(frame, scale_alpha(ST['thanks'], e), 540, 640)
        center_paste(frame, scale_alpha(ST['endsub'], e), 540, 880)
        center_paste(frame, scale_alpha(ST['endcmd'], e), 540, 1000)
        center_paste(frame, scale_alpha(ST['codebox'], e), 540, 1215)
        center_paste(frame, scale_alpha(ST['endfoot'], e), 540, 1462)

    # fondu final uniquement
    if t > TOTAL - 0.8:
        k = max(0.0, (TOTAL - t) / 0.8)
        black = Image.new('RGBA', (W, H), (0, 0, 0, 255))
        frame = Image.blend(black, frame, k)
    return frame


def main():
    preview = '--preview' in sys.argv
    lines = load_lines()
    build_timeline(lines)
    windows = bell_windows(lines)
    cyc = cta_cycles(windows)
    segs = bg_segments(lines)
    setup(lines)

    meta = {
        'source_audio': os.path.basename(SRC),
        'duree_audio_s': AUDIO_DUR,
        'duree_carte_finale_s': END_DUR,
        'duree_totale_s': TOTAL,
        'fps': FPS,
        'hypothese_affichage': 'min(4 s, max(2 s, 0,07 s × nb_caracteres + 1,2 s)), borné par le vers suivant',
        'fenetres_cta_5s': [{'debut': a, 'fin': b, 'duree': round(b - a, 2)} for a, b in windows],
        'cycles_cta': [{'debut': round(a, 2), 'duree': round(b, 2)} for a, b in cyc],
        'carte_accueil_s': [0.0, 4.92],
        'vers': [{'t0': L['t0'], 't1': L['t1'], 'fond': L['bg'], 'texte': L['text']} for L in lines],
    }
    if '--timings' in sys.argv or not preview:
        os.makedirs(os.path.join(ROOT), exist_ok=True)
        with open(os.path.join(ROOT, 'timings_audited.json'), 'w', encoding='utf-8') as fh:
            json.dump(meta, fh, ensure_ascii=False, indent=1)

    if '--timings' in sys.argv:
        print('timings_audited.json écrit', flush=True)
        return
    if preview:
        os.makedirs(PREVIEW_DIR, exist_ok=True)
        for t in [3.5, 30.0, 61.0, 118.0, 140.0, 148.0, 180.0, 199.0]:
            render(t, segs, cyc).convert('RGB').save(os.path.join(PREVIEW_DIR, f'p_{t:06.2f}.png'))
            print('ok', t, flush=True)
        print('fenetres', windows, flush=True)
        return

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cmd = [FFMPEG, '-y', '-loglevel', 'error',
           '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-i', SRC,
           '-map', '0:v', '-map', '1:a', '-af', f'apad=whole_dur={TOTAL:.3f}',
           '-t', f'{TOTAL:.3f}',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
           '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
           '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-ac', '2',
           '-movflags', '+faststart',
           '-metadata', 'title=Ça monte, ça descend', '-metadata', 'artist=Dsky',
           OUT]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(round(TOTAL * FPS))
    for f in range(n):
        frame = render(f / FPS, segs, cyc)
        proc.stdin.write(frame.convert('RGB').tobytes())
        if f % 900 == 0:
            print(f'frame {f}/{n}', flush=True)
    proc.stdin.close()
    rc = proc.wait()
    print('ffmpeg rc', rc, flush=True)
    print('sortie', OUT, flush=True)


if __name__ == '__main__':
    main()
