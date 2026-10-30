#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render.py — moteur de clip Lyrics v6.0 (WTBW Salut & Stickers Doux, sans code).

Lit verses_map.json (build_map.py) et produit un MP4 1080x1920@30, H.264 + AAC.
Toutes les animations sont calculées par frame, aucun resize par frame (§5.1).

  python3 render.py                       # clip complet
  python3 render.py --start 0 --dur 20    # extrait
  python3 render.py --frames-only         # rendu image par image (debug)

Repères : les zones de sécurité du prompt sont en 768x1376 natif ; ici tout est
en 1080x1920 (rendu), la source étant agrandie 1188x2128 (SC 1.10) une seule fois.
"""
import argparse, json, math, os, random, subprocess, sys, time
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
import lettering

HERE = os.path.dirname(os.path.abspath(__file__))
# ffmpeg : variable FF, sinon binaire imageio-ffmpeg (portable, même sous la console)
if not os.environ.get("FF"):
    try:
        import imageio_ffmpeg
        os.environ["FF"] = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:                                # noqa: BLE001
        os.environ["FF"] = "ffmpeg"
FONTS = os.path.join(HERE, "fonts")
W, H, FPS = 1080, 1920, 30
BW, BH = 1188, 2128           # source agrandie (SC 1.10) : marge 108 px en x, 208 px en y
SCX, SCY = BW - W, BH - H

# ------------------------------------------------------------------ palettes
CREAM = (244, 247, 252)
GOLD = (244, 197, 98)
GOLD_HOT = (255, 224, 122)
INK = (8, 12, 18)
BLUE = (175, 190, 210)
DARK = (4, 8, 12)

_fcache = {}
def font(name, size):
    k = (name, size)
    if k not in _fcache:
        _fcache[k] = ImageFont.truetype(os.path.join(FONTS, f"Montserrat-{name}.ttf"), size)
    return _fcache[k]

def tw(dr, txt, f, spacing=0):
    if not txt:
        return 0
    if spacing == 0:
        return dr.textlength(txt, font=f)
    return sum(dr.textlength(c, font=f) + spacing for c in txt) - spacing

def draw_spaced(dr, xy, txt, f, fill, spacing=0, anchor_center=False, stroke=0, stroke_fill=None):
    x, y = xy
    if anchor_center:
        x -= tw(dr, txt, f, spacing) / 2
    for c in txt:
        dr.text((x, y), c, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
        x += dr.textlength(c, font=f) + spacing
    return x

# ------------------------------------------------------------------ cache plans
class Plan:
    """une image de fond + ses caches net / éteint / échelle."""
    _c = {}
    def __init__(self, path, lignes=()):
        im = Image.open(path).convert("RGB")
        if im.size != (768, 1376):
            im = im.resize((768, 1376), Image.LANCZOS)
        if lignes and any(lignes):                        # v6.2 : typo peinte par le moteur
            im = lettering.draw_lettering(im, lignes[0], lignes[1] if len(lignes) > 1 else "",
                                          os.path.join(FONTS, "Montserrat-ExtraBold.ttf"),
                                          dy=lettering.dy_for(path))
        self.net = im.resize((BW, BH), Image.LANCZOS)
        self._off = None
        self.path = path

    MANQUANTS = []

    @classmethod
    def get(cls, path, lignes=()):
        """repli déclaré : un plan absent ne casse jamais le rendu (ancre)."""
        if not os.path.exists(path):
            if path not in cls.MANQUANTS:
                cls.MANQUANTS.append(path)
            path = os.path.join(HERE, "fonds", "scene-01-ancre.png")
        key = (path, tuple(lignes or ()))
        if key not in cls._c:
            cls._c[key] = cls(path, lignes or ())
        return cls._c[key]

    def window(self, x0, y0, w=W, h=H):
        return self.net.crop((int(x0), int(y0), int(x0) + w, int(y0) + h))

# ------------------------------------------------------------------ vignette / grain
def build_vignette():
    m = Image.new("L", (W, H), 0)
    px = m.load()
    cx, cy = W / 2, H * 0.46
    maxd = math.hypot(W / 2, H * 0.62)
    step = 4
    for y in range(0, H, step):
        for x in range(0, W, step):
            d = math.hypot((x - cx) * 0.86, (y - cy)) / maxd
            v = int(min(1.0, max(0.0, (d - 0.62) / 0.55)) * 86)
            for yy in range(y, min(y + step, H)):
                for xx in range(x, min(x + step, W)):
                    px[xx, yy] = v
    return m.filter(ImageFilter.GaussianBlur(34))

def build_grains(n=4, seed=1776):
    out = []
    rnd = random.Random(seed)
    for k in range(n):
        g = Image.effect_noise((W, H), 26 + k).convert("L")
        out.append(g)
    return out

VIGNETTE = None
GRAINS = None

def post(frame, k):
    """vignette masque L + grain 35 mm cyclé sur Brightness 1.09 (§5.5)."""
    global VIGNETTE, GRAINS
    if VIGNETTE is None:
        VIGNETTE = build_vignette()
        GRAINS = build_grains()
    black = Image.new("RGB", frame.size, DARK)
    f = Image.composite(black, frame, VIGNETTE)
    f = f.point(lambda v: min(255, int(v * 1.09)))
    g = GRAINS[(k // 2) % 4].convert("RGB")
    return Image.blend(f, g, 0.045)

# ------------------------------------------------------------------ vecteurs
def ss_draw(size, fn, ss=3):
    """dessine en supersampling x3 puis réduit (icônes nettes)."""
    big = Image.new("RGBA", (size * ss, size * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    fn(d, size * ss)
    return big.resize((size, size), Image.LANCZOS)

def heart_path(cx, cy, r):
    pts = []
    for i in range(0, 360, 3):
        t = math.radians(i)
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x * r / 17, cy - y * r / 17))
    return pts

def icon_heart(d, s, color=GOLD, glow=True):
    c = s / 2
    pts = heart_path(c, c * 0.96, s * 0.42)
    if glow:
        for w, a in ((10, 40), (6, 70)):
            d.polygon(pts, fill=color + (a,))
    d.polygon(pts, fill=color + (255,))
    d.polygon(heart_path(c, c * 0.96, s * 0.30), fill=(20, 14, 8, 60))

def icon_plus(d, s, color=GOLD):
    c = s / 2
    r = s * 0.40
    for w in (14, 8):
        d.ellipse([c - r - w, c - r - w, c + r + w, c + r + w], outline=color + (40,), width=w)
    d.ellipse([c - r, c - r, c + r, c + r], fill=color + (255,))
    d.ellipse([c - r * 0.78, c - r * 0.78, c + r * 0.78, c + r * 0.78], fill=(18, 14, 8, 255))
    b = r * 0.48
    for rect in ([c - b, c - b * 0.19, c + b, c + b * 0.19], [c - b * 0.19, c - b, c + b * 0.19, c + b]):
        d.rounded_rectangle(rect, radius=r * 0.12, fill=color + (255,))

def icon_comment(d, s, color=GOLD):
    c = s / 2
    w, h = s * 0.76, s * 0.56
    box = [c - w / 2, c - h / 2 - s * 0.04, c + w / 2, c + h / 2 - s * 0.04]
    for k in (10, 6):
        d.rounded_rectangle([box[0] - k, box[1] - k, box[2] + k, box[3] + k], radius=s * 0.18,
                            outline=color + (35,), width=k)
    d.rounded_rectangle(box, radius=s * 0.16, fill=color + (255,))
    d.polygon([(c - s * 0.16, box[3] - 2), (c + s * 0.06, box[3] - 2), (c - s * 0.16, box[3] + s * 0.16)],
              fill=color + (255,))
    for dx in (-0.20, 0.0, 0.20):
        rr = s * 0.055
        d.ellipse([c + dx * s - rr, c - s * 0.04 - rr, c + dx * s + rr, c - s * 0.04 + rr], fill=(18, 14, 8, 255))

def star_path(cx, cy, r1, r2=None, n=4):
    r2 = r2 or r1 * 0.28
    pts = []
    for i in range(n * 2):
        a = math.pi / n * i - math.pi / 2
        r = r1 if i % 2 == 0 else r2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

ICONS = {"heart": icon_heart, "plus": icon_plus, "comment": icon_comment}
_icache = {}
def icon_img(kind, size):
    key = (kind, size)
    if key not in _icache:
        _icache[key] = ss_draw(size, lambda d, s: ICONS[kind](d, s))
    return _icache[key]

# ------------------------------------------------------------------ stickers doux
STICKERS = [
    ("heart", "LIKE LA VIDÉO", "Laisse un cœur si tu valides"),
    ("plus", "CLIQUE SUR + POUR T'ABONNER", "Rejoins Wolof TechStein beat wê"),
    ("comment", "COMMENTE SI TU AIMES !", "Dis-nous ton vers préféré"),
]

def draw_sticker(base, idx, cx, cy, t, alpha=1.0):
    """pilule 700x152 + icône vectorielle qui respire + flottement sinusoïdal."""
    kind, main, sub = STICKERS[idx]
    ph = idx * 0.63
    dy = 12 * math.sin(2 * math.pi * (t / (1.8 + 0.15 * idx)) + ph)
    dx = 14 * math.sin(2 * math.pi * (t / (2.1 - 0.1 * idx)) + ph * 1.7)
    pulse = 1 + 0.05 * math.sin(2 * math.pi * t / 1.4 + ph)

    w, h = 700, 152
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([20, 20, 20 + w, 20 + h], radius=60, fill=(10, 14, 20, 208))
    d.rounded_rectangle([20, 20, 20 + w, 20 + h], radius=60, outline=(244, 197, 98, 165), width=3)
    d.rounded_rectangle([20, 20, 20 + w, 20 + 52], radius=60, fill=(255, 255, 255, 12))
    ic = icon_img(kind, int(96 * pulse))
    layer.alpha_composite(ic, (44 + (96 - ic.width) // 2, 20 + (h - ic.height) // 2))
    maxw = w - 168 - 26
    fs = 34 if len(main) <= 22 else 30
    f1 = font("ExtraBold", fs)
    while d.textlength(main, font=f1) > maxw and fs > 17:
        fs -= 1
        f1 = font("ExtraBold", fs)
    f2 = font("SemiBold", 20)
    while d.textlength(sub, font=f2) > maxw and f2.size > 13:
        f2 = font("SemiBold", f2.size - 1)
    ty = 20 + (h - (fs + 30)) // 2
    d.text((168, ty), main, font=f1, fill=CREAM + (255,))
    d.text((168, ty + fs + 12), sub, font=f2, fill=(205, 214, 228, 235))
    if alpha < 1:
        a = layer.split()[3].point(lambda v: int(v * alpha))
        layer.putalpha(a)
    base.alpha_composite(layer, (int(cx - w / 2 - 20 + dx), int(cy - h / 2 - 20 + dy)))

# ------------------------------------------------------------------ cartes
def card_bg(plan, t, blur=9, bright=0.72):
    u = (t * 0.04) % 1.0
    x0 = SCX * (0.15 + 0.7 * (0.5 - 0.5 * math.cos(2 * math.pi * u)))
    y0 = SCY * 0.5
    im = plan.window(x0, y0).filter(ImageFilter.GaussianBlur(blur))
    im = im.point(lambda v: int(v * bright))
    scrim = Image.new("RGB", (W, H), (6, 9, 14))
    return Image.blend(im, scrim, 0.55)

def rules(dr, a=170):
    for y in (310, 1470):
        dr.line([(170, y), (910, y)], fill=(244, 197, 98, a), width=3)
        dr.line([(170, y + 5), (910, y + 5)], fill=(244, 197, 98, 55), width=1)

def header(base, alpha=255):
    d = ImageDraw.Draw(base)
    f = font("ExtraBold", 30)
    draw_spaced(d, (W / 2, 236), "WTBW · WOLOF TECHSTEIN BEAT WÊ !", f,
                (244, 197, 98, alpha), spacing=3, anchor_center=True,
                stroke=2, stroke_fill=(6, 9, 14, int(alpha * 0.8)))

def draw_card_intro(t, t0, plan, titre, artiste):
    base = card_bg(plan, t).convert("RGBA")
    dr = ImageDraw.Draw(base)
    rules(dr)
    header(base)
    half = t0 / 2
    if t < half:                                     # temps 1
        u = t / half
        a = int(255 * min(1, t / 0.45) * (1 if t < half - 0.25 else max(0, (half - t) / 0.25)))
        fy = 10 * math.sin(2 * math.pi * t / 1.9)
        dr = ImageDraw.Draw(base)
        draw_spaced(dr, (W / 2, 470 + fy), "SALUT · WTBW", font("ExtraBold", 84),
                    (255, 255, 255, a), spacing=2, anchor_center=True, stroke=3, stroke_fill=(0, 0, 0, a))
        dr.text((W / 2, 596 + fy), "Wolof TechStein beat wê", font=font("SemiBold", 40),
                fill=(244, 197, 98, a), anchor="mm")
        plaque(base, f"{titre.upper()} — {artiste.upper()}", 700, alpha=a)
    else:                                            # temps 2
        u = (t - half) / half
        a = int(255 * min(1, (t - half) / 0.45))
        dr = ImageDraw.Draw(base)
        draw_spaced(dr, (W / 2, 486), "BIENVENUE SUR WTBW", font("ExtraBold", 62),
                    (255, 255, 255, a), spacing=1, anchor_center=True, stroke=3, stroke_fill=(0, 0, 0, a))
        dr.text((W / 2, 578), "Soutiens le son en douceur :", font=font("SemiBold", 34),
                fill=(226, 233, 244, a), anchor="mm")
        plaque(base, f"{titre.upper()} · {artiste.upper()}", 700, alpha=a)
    for k in range(3):
        draw_sticker(base, k, W / 2, 845 + 200 * k, t, alpha=min(1.0, t / 0.6))
    dr = ImageDraw.Draw(base)
    dr.text((W / 2, 1400), "Wolof TechStein beat wê (WTBW)", font=font("SemiBold", 26),
            fill=(255, 255, 255, 150), anchor="mm")
    return base.convert("RGB")

def plaque(base, txt, width=700, alpha=255):
    d = ImageDraw.Draw(base)
    f = font("ExtraBold", 34)
    while tw(d, txt, f) > width - 56 and f.size > 18:
        f = font("ExtraBold", f.size - 2)
    h = 92
    y = 686
    d.rounded_rectangle([(W - width) / 2, y, (W + width) / 2, y + h], radius=26,
                        fill=(12, 16, 24, int(200 * alpha / 255)),
                        outline=(244, 197, 98, int(190 * alpha / 255)), width=3)
    d.text((W / 2, y + h / 2 + 2), txt, font=f, fill=(255, 255, 255, alpha), anchor="mm")

def draw_card_end(t, plan, titre, artiste):
    base = card_bg(plan, t, blur=9, bright=0.78).convert("RGBA")
    dr = ImageDraw.Draw(base)
    rules(dr)
    header(base)
    a = int(255 * min(1, t / 0.5))
    dr = ImageDraw.Draw(base)
    draw_spaced(dr, (W / 2, 452), "MERCI D'AVOIR ÉCOUTÉ !", font("ExtraBold", 62),
                (255, 255, 255, a), spacing=1, anchor_center=True, stroke=3, stroke_fill=(0, 0, 0, a))
    dr.text((W / 2, 548), "Wolof TechStein beat wê (WTBW)", font=font("SemiBold", 34),
            fill=(244, 197, 98, a), anchor="mm")
    plaque(base, f"{titre.upper()} · {artiste.upper()}", 700, alpha=a)
    for k in range(3):
        draw_sticker(base, k, W / 2, 845 + 200 * k, t + 3, alpha=min(1.0, t / 0.6))
    return base.convert("RGB")

# ------------------------------------------------------------------ cloche CTA (§6)
def bell(size, ang, t):
    s = size
    def fn(d, S):
        cx, cy = S / 2, S / 2
        d.ellipse([cx - S * 0.30, cy - S * 0.34, cx + S * 0.30, cy + S * 0.26], fill=(244, 197, 98, 60))
        body, N = [], 80
        for i in range(N + 1):                       # flanc gauche : doucine puis jupe évasée
            u = i / N
            y = -0.30 * S + u * 0.52 * S
            if u < 0.30:
                x = 0.045 * S + 0.085 * S * (u / 0.30) ** 1.6
            elif u < 0.78:
                x = 0.130 * S - 0.010 * S * math.sin(math.pi * (u - 0.30) / 0.48)
            else:
                x = 0.120 * S + 0.190 * S * ((u - 0.78) / 0.22) ** 1.9
            body.append((-x, y))
        for i in range(N, -1, -1):                   # retour par la droite
            x, y = body[i]
            body.append((-x, y))
        pts = [(cx + x * math.cos(math.radians(ang)) - y * math.sin(math.radians(ang)),
                cy + x * math.sin(math.radians(ang)) + y * math.cos(math.radians(ang))) for x, y in body]
        d.ellipse([cx - 0.075 * S, cy - 0.44 * S, cx + 0.075 * S, cy - 0.26 * S],
                  outline=(255, 224, 122, 255), width=int(0.035 * S))
        d.polygon(pts, fill=(244, 197, 98, 255), outline=(80, 55, 12, 255))
        d.rounded_rectangle([cx - 0.315 * S, cy + 0.205 * S, cx + 0.315 * S, cy + 0.27 * S],
                            radius=0.045 * S, fill=(255, 224, 122, 255))
        d.ellipse([cx - 0.07 * S, cy + 0.275 * S, cx + 0.07 * S, cy + 0.395 * S], fill=(255, 224, 122, 255))
    return ss_draw(size, fn, ss=3)

_bell_cache = {}
def bell_img(size, ang, phase):
    key = (size, int(ang * 2) % 720)
    if key not in _bell_cache:
        _bell_cache[key] = bell(size, ang, phase)
    return _bell_cache[key]

def draw_cta(base, t, a, b):
    """tile 720x720 centré x=540, y 620->1340."""
    k = min(1.0, (t - a) / 0.35, (b - t) / 0.35)
    if k <= 0:
        return base
    tile = Image.new("RGBA", (720, 720), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    d.rounded_rectangle([34, 8, 686, 712], radius=54, fill=(6, 10, 16, int(244 * k)))
    d.rounded_rectangle([34, 8, 686, 712], radius=54, outline=(244, 197, 98, int(150 * k)), width=3)
    # cloche : 36 angles, pendule amorti, période 4,0 s
    tt = t - a
    ang = 12 * math.cos(2 * math.pi * tt / 4.0) * math.exp(-tt / 6.0)
    bimg = bell_img(250, ang, tt)
    # halo + ondes
    glow = Image.new("RGBA", (720, 720), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r, al in ((150, 26), (120, 40)):
        gd.ellipse([300 - r, 130 - r, 300 + r, 130 + r], fill=(255, 214, 120, al))
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    tile.alpha_composite(glow)
    for i, ph in enumerate((0.0, 0.5)):
        u = ((tt / 0.9) + ph) % 1.0
        r = 60 + 190 * u
        al = int(110 * (1 - u) * k)
        d.ellipse([300 - r, 130 - r, 300 + r, 130 + r], outline=(255, 224, 122, al), width=2)
    tile.alpha_composite(bimg, (300 - 125, 130 - 125))
    for (sx, sy, sr, ph) in ((430, 60, 16, 0.0), (170, 210, 11, 0.4), (450, 250, 13, 0.7)):
        u = 0.6 + 0.4 * math.sin(2 * math.pi * (tt / 1.3) + ph)
        pts = star_path(sx, sy, sr * u)
        d.polygon(pts, fill=(255, 240, 190, int(210 * k)))
    # flèche clignotante
    ba = (0.55 + 0.45 * math.sin(2 * math.pi * tt / 0.8))
    fy = 12 * math.sin(2 * math.pi * tt / 0.8)
    d.polygon([(540, 300 - fy), (518, 334 - fy), (562, 334 - fy)],
              fill=(255, 224, 122, int(230 * ba * k)))
    f1 = font("ExtraBold", 56)
    draw_spaced(d, (360, 420), "CLIQUE SUR +", f1, (255, 255, 255, int(255 * k)), spacing=5, anchor_center=True,
                stroke=3, stroke_fill=(0, 0, 0, int(255 * k)))
    # pilule LIKE & PARTAGE
    d.rounded_rectangle([150, 510, 570, 606], radius=48, fill=(244, 197, 98, int(230 * k)))
    d.text((360, 558), "LIKE & PARTAGE", font=font("ExtraBold", 34), fill=(12, 14, 20, int(255 * k)), anchor="mm")
    d.text((360, 648), "Commente si tu aimes · WTBW", font=font("SemiBold", 30),
           fill=(226, 233, 244, int(240 * k)), anchor="mm")
    if k < 1:
        al = tile.split()[3].point(lambda v: int(v * min(1.0, k * 1.0)))
        tile.putalpha(al)
    base.alpha_composite(tile, (W // 2 - 360, 620))
    return base

# ------------------------------------------------------------------ vers
# 4 trajectoires, exprimées en déplacement centré (fx / fy ∈ [-1, 1]) ; les
# amplitudes XR / YR sont bornées pour que la bande peinte reste dans 620→1340
# et le visage au-dessus de y 190 malgré les 110 % de marge (§5.2).
TRAJ = [(-1.0, 1.0, -1.0, 1.0), (1.0, -1.0, -1.0, 1.0),
        (-0.6, 0.6, 1.0, -1.0), (0.6, -0.6, -1.0, 1.0)]
XR, YR = 45.0, 40.0

def window_for(plan, si, u, dur):
    """u ∈ [0,1] ; cycle cosinus 2,2 s si dur > 3,5 s (§5.2/5.6)."""
    if dur > 3.5:
        u = 0.5 - 0.5 * math.cos(2 * math.pi * (u * dur / 2.2))
    fx0, fx1, fy0, fy1 = TRAJ[si % 4]
    x = SCX / 2 + XR * (fx0 + (fx1 - fx0) * u)
    y = SCY / 2 + YR * (fy0 + (fy1 - fy0) * u)
    return plan.window(x, y)

_BAND_MASK = None
def extinguish(frame, g):
    """bande 620->1340 : Brightness 0.38 + GaussianBlur 3, bords fondus (§5.4).
    Le fondu de bord est indispensable : un paste net dessinait une barre horizontale
    visible en travers du plan (constaté sur le rendu v6.2)."""
    global _BAND_MASK
    if _BAND_MASK is None:
        m = Image.new("L", (W, 720), 0)
        d = ImageDraw.Draw(m)
        d.rectangle([0, 40, W, 680], fill=255)
        _BAND_MASK = m.filter(ImageFilter.GaussianBlur(46))
    band = frame.crop((0, 620, W, 1340))
    band = band.point(lambda v: int(v * 0.22)).filter(ImageFilter.GaussianBlur(7))
    out = frame.copy()
    out.paste(band, (0, 620), _BAND_MASK.point(lambda v: int(v * g)))
    return out

def verse_frame(slot, t, k):
    dur = max(0.001, slot["fin"] - slot["t"])
    u = min(1.0, max(0.0, (t - slot["t"]) / dur))
    plan = Plan.get(os.path.join(HERE, slot["image"]), slot.get("lignes", ()))
    f = window_for(plan, slot["i"], u, dur).convert("RGB")
    if dur > 3.5:                                    # respiration lumineuse ±12 %
        br = 1 + 0.12 * math.sin(2 * math.pi * (t - slot["t"]) / 1.7)
        f = f.point(lambda v: max(0, min(255, int(v * br))))
    g = min(1.0, max(0.0, (t - (slot["t"] + slot["affichage_s"])) / 0.35))
    if g > 0:
        f = extinguish(f, g)
    return f

def overlay_verse(frame, slot, t, doc, prog):
    base = frame.convert("RGBA")
    # badge Dsky (§7.4)
    rel = t - slot["t"]
    a = min(1.0, rel / 0.4) * (1 - min(1.0, max(0.0, (t - slot["fin"]) / 0.2)))
    a = min(a, 0.72)
    if a > 0.01:
        d = ImageDraw.Draw(base)
        d.text((W / 2, 165), "Dsky", font=font("ExtraBold", 32), fill=(255, 255, 255, int(255 * a)),
               anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0, int(200 * a)))
        w = 62 * a
        d.line([(W / 2 - w, 189), (W / 2 + w, 189)], fill=(244, 197, 98, int(200 * a)), width=2)
    # filet de progression
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([170, 1556, 910, 1564], radius=4, fill=(255, 255, 255, 48))
    d.rounded_rectangle([170, 1556, 170 + int(740 * prog), 1564], radius=4, fill=(244, 197, 98, 210))
    return base

# ------------------------------------------------------------------ traduction FR (§5.7, dormante ici)
def render_fr_translation(base, words, u_word, alpha=255):
    if not words:
        return base
    d = ImageDraw.Draw(base)
    w, h = 708, 20 + 38
    x0, y0 = W / 2 - w / 2, 1452
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=24, fill=(8, 12, 18, 222),
                        outline=(244, 197, 98, 185), width=2)
    d.rounded_rectangle([x0, y0 + h - 3, x0 + int(w * u_word), y0 + h], radius=2, fill=(255, 222, 118, alpha))
    active = min(len(words) - 1, int(u_word * len(words)))
    dx = round((0.5 - u_word) * 18)
    f = font("ExtraBold", 29)
    total = sum(d.textlength(t, font=f) + 11 for t in words) - 11
    cx = W / 2 - total / 2 + dx
    for i, t_ in enumerate(words):
        col = GOLD_HOT if i == active else (CREAM if i < active else BLUE)
        d.text((cx, y0 + 11), t_, font=f, fill=col + (alpha,), stroke_width=3, stroke_fill=(0, 0, 0, alpha))
        cx += d.textlength(t_, font=f) + 11
    return base

# ------------------------------------------------------------------ boucle
def build_audio(master, out):
    ff = os.environ.get("FF", "ffmpeg")
    if os.path.exists(out):
        return out
    p1 = subprocess.run([ff, "-hide_banner", "-nostats", "-i", master, "-map", "0:a:0", "-vn",
                         "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                        capture_output=True, text=True)
    js = p1.stderr[p1.stderr.rindex("{"):]
    js = js[:js.index("}") + 1]
    m = json.loads(js)
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", master, "-map", "0:a:0", "-vn",
                    "-af", af, "-ar", "48000", "-ac", "2", "-c:a", "libmp3lame", "-b:a", "320k", out], check=True)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--dur", type=float, default=None)
    ap.add_argument("--out", default="livrables/clip-9x16.mp4")
    ap.add_argument("--master", default="audio/master-14LUFS.mp3")
    args = ap.parse_args()

    doc = json.load(open(os.path.join(HERE, "verses_map.json"), encoding="utf-8"))
    slots = doc["vers"]
    t0 = slots[0]["t"]
    total = doc["clip_duree_s"]
    start = args.start
    dur = args.dur if args.dur else total - start
    end = min(total, start + dur)

    master = os.path.join(HERE, args.master)
    if not os.path.exists(master):
        print("… normalisation audio (2 passes loudnorm)")
        build_audio(os.path.join(os.path.dirname(HERE), "..", "..", "..", "On a nous volé notre éducation.mp3"), master)

    out = os.path.join(HERE, args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    ff = os.environ.get("FF", "ffmpeg")
    n = int(round((end - start) * FPS))
    cmd = [ff, "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-ss", f"{start:.3f}", "-i", master,
           "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-pix_fmt", "yuv420p",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
           "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
           "-t", f"{(end - start):.3f}", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    plans = [s for s in slots]
    first_plan = Plan.get(os.path.join(HERE, slots[0]["image"]))          # carte : art nu
    last_plan = Plan.get(os.path.join(HERE, slots[-1]["image"]))
    cta = doc["cta"]
    ts = time.time()
    for k in range(n):
        t = start + k / FPS
        if t < t0:
            frame = post(draw_card_intro(t, t0, first_plan, doc["titre"], doc["artiste"]), k)
        elif t >= doc["audio_duree_s"]:
            frame = post(draw_card_end(t - doc["audio_duree_s"], last_plan, doc["titre"], doc["artiste"]), k)
        else:
            idx = 0
            for j, s in enumerate(plans):
                if s["t"] <= t:
                    idx = j
                else:
                    break
            slot = plans[idx]
            frame = verse_frame(slot, t, k)
            # fondu enchaîné 0,35 s entre segments (§5.3)
            if idx > 0 and t - slot["t"] < 0.35:
                prev = plans[idx - 1]
                fp = verse_frame(prev, min(t, prev["fin"] - 0.001), k)
                a = (t - slot["t"]) / 0.35
                frame = Image.blend(fp.convert("RGB"), frame.convert("RGB"), a)
            frame = post(frame, k)
            prog = (t - t0) / (doc["audio_duree_s"] - t0)
            rgba = overlay_verse(frame, slot, t, doc, prog)
            for c in cta:
                if c["debut"] <= t <= c["fin"]:
                    rgba = draw_cta(rgba, t, c["debut"], c["fin"])
                    break
            frame = rgba.convert("RGB")
        proc.stdin.write(frame.tobytes())
        if k % 150 == 0:
            el = time.time() - ts
            print(f"  {k}/{n} frames · {el:6.1f}s · {k/max(el,1e-6):.1f} fps", flush=True)
    proc.stdin.close()
    proc.wait()
    if Plan.MANQUANTS:
        print("⚠ plans absents (repli ancre) :", ", ".join(os.path.basename(x) for x in Plan.MANQUANTS))
    print("rendu :", out, f"{end-start:.2f}s")


if __name__ == "__main__":
    main()
