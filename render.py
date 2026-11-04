#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render.py — clip 1080x1920 @30fps (§5, §7 v6.3).
Usage : python3 render.py prods/TU-ES-TROP-BELLE [--start 0] [--end 210] [--out out/clip.mp4] [--silent]
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from common import (REPO, font, GOLD_A, GOLD_B, CY_A, CY_B, INK, GOLD_HOT, GOLD_LINE,
                    NATIVE, OUT, FPS, vgrad, blur, ensure_dir, deterministic_seed)

FF = os.path.expanduser("~/.local/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v9.0.2")
W, H = OUT

# ------------------------------------------------------------------ zoom / travelling
def scale_factor(z):
    return 1.5469 * z / 1.10        # §5.1 : SC 1,10 pour z = 1,10 → 1188x2128

class Scaled:
    """Mise à l'échelle unique par (frame, niveau de zoom) — aucun resize par frame."""
    def __init__(self, img):
        self.src = img
        self.cache = {}
    def get(self, z):
        key = round(z, 3)
        if key not in self.cache:
            if len(self.cache) > 6:
                self.cache.pop(next(iter(self.cache)))
            s = scale_factor(key)
            self.cache[key] = np.asarray(self.src.resize(
                (round(NATIVE[0] * s), round(NATIVE[1] * s)), Image.BILINEAR))
        return self.cache[key]

def window(arr, z, t, period=17.0, xr=45, yr=40, phase=0.0):
    h, w = arr.shape[:2]
    xm, ym = max(0, w - W), max(0, h - H)
    ax, ay = min(xr, xm / 2), min(yr, ym / 2)
    x = xm / 2 + ax * math.sin(2 * math.pi * t / period + phase)
    y = ym / 2 + ay * math.sin(2 * math.pi * t / period + 1.1 + phase)
    x = int(min(max(x, 0), xm)); y = int(min(max(y, 0), ym))
    return arr[y:y + H, x:x + W]

def zoom_travel(t):
    return 1.09 + 0.035 * math.sin(2 * math.pi * t / 17.0)   # §5.2

def zoom_card(t):
    return 1.04 + 0.035 * math.sin(2 * math.pi * t / 7.7)    # §5.5 cartes

# ------------------------------------------------------------------ grain / vignette
rng_g = np.random.default_rng(20261104)
def _grain_motif():
    small = rng_g.integers(0, 256, (H // 3 + 1, W // 3 + 1), dtype=np.uint8)
    im = Image.fromarray(small, "L").resize((W, H), Image.BICUBIC)
    return np.asarray(im)
GRAINS = [_grain_motif() for _ in range(8)]
_VIG = None
def vignette():
    global _VIG
    if _VIG is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        _VIG = np.clip(1.0 - 0.16 * np.clip(d - 0.55, 0, None) ** 1.5 * 3.2, 0.82, 1.0)[:, :, None]
    return _VIG

def apply_grain(frame, k, amount):
    """Grain 35 mm : 8 motifs, un par frame (k % 8), blend additif (amount x 128)."""
    g = (GRAINS[k % 8].astype(np.int16) - 128) * (amount * 128 / 128)
    amt = amount * (64 if amount > 0.1 else 128)
    out = frame.astype(np.int16) + (g[:, :, None] * (amt / 128)).astype(np.int16)
    return np.clip(out, 0, 255).astype(np.uint8)

# ------------------------------------------------------------------ éléments moteur
def text_img(text, fnt, fill, tracking=0, stroke=0, stroke_fill=INK):
    if tracking == 0 and stroke == 0:
        bb = fnt.getbbox(text)
        im = Image.new("RGBA", (bb[2] - bb[0] + 8, bb[3] - bb[1] + 8), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((4 - bb[0], 4 - bb[1]), text, font=fnt, fill=fill)
        return im
    # lettrage espacé + contour par dilatation
    ow = stroke
    widths = []
    for ch in text:
        bb = fnt.getbbox(ch)
        widths.append(bb[2] - bb[0])
    total = sum(widths) + tracking * max(0, len(text) - 1) + 2 * (ow + 10)
    bb0 = fnt.getbbox(text)
    hgt = bb0[3] - bb0[1] + 2 * (ow + 10)
    mask = Image.new("L", (total, hgt), 0)
    x = ow + 10
    for ch, wd in zip(text, widths):
        if ch != " ":
            g = Image.new("L", (wd + 2 * ow + 6, hgt), 0)
            ImageDraw.Draw(g).text((ow + 3 - fnt.getbbox(ch)[0], ow + 10 - bb0[1]), ch, font=fnt, fill=255)
            if ow > 0:
                cont = g.filter(ImageFilter.MaxFilter(2 * ow + 1))
            else:
                cont = None
            if cont is not None:
                pass
            mask.paste(g, (x - ow - 3, 0), g)
        x += wd + tracking
    if ow > 0:
        cont = mask.filter(ImageFilter.MaxFilter(2 * ow + 1))
    im = Image.new("RGBA", mask.size, (0, 0, 0, 0))
    if ow > 0:
        im.paste(Image.new("RGBA", mask.size, stroke_fill + (255,)), (0, 0), cont)
    im.paste(Image.new("RGBA", mask.size, fill + (255,)), (0, 0), mask)
    return im

def paste_center(base, img, cy, cx=None):
    x = (W - img.width) // 2 if cx is None else cx - img.width // 2
    base.alpha_composite(img, (x, int(cy - img.height // 2)))

def text_fit(text, weight, size, fill, max_w, **kw):
    """text_img auto-réduit par pas de 2 px pour tenir dans max_w (§7.5)."""
    s = size
    while s > 16:
        img = text_img(text, font(weight, s), fill, **kw)
        if img.width <= max_w:
            return img
        s -= 2
    return text_img(text, font(weight, 16), fill, **kw)

def rounded_panel(w, h, r, fill, rim=None, rim_w=2):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=fill,
                        outline=rim, width=rim_w if rim else 0)
    return im

# --- icônes vectorielles (supersampling x3) ---
def icon_bell(size=120, col=(255, 232, 168)):
    s = size * 3
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = s // 2
    d.rounded_rectangle([cx - int(s * 0.26), int(s * 0.30), cx + int(s * 0.26), int(s * 0.66)],
                        radius=int(s * 0.12), fill=col)
    d.pieslice([cx - int(s * 0.36), int(s * 0.16), cx + int(s * 0.36), int(s * 0.52)], 180, 360, fill=col)
    d.ellipse([cx - int(s * 0.07), int(s * 0.62), cx + int(s * 0.07), int(s * 0.76)], fill=col)
    d.ellipse([cx - int(s * 0.05), int(s * 0.10), cx + int(s * 0.05), int(s * 0.20)], fill=col)
    return im.resize((size, size), Image.LANCZOS)

def icon_heart(size=120, col=(255, 232, 168)):
    s = size * 3
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = int(s * 0.19)
    d.ellipse([s * 0.16, s * 0.20, s * 0.16 + 2 * r, s * 0.20 + 2 * r], fill=col)
    d.ellipse([s * 0.84 - 2 * r, s * 0.20, s * 0.84, s * 0.20 + 2 * r], fill=col)
    d.polygon([(s * 0.175, s * 0.44), (s * 0.825, s * 0.44), (s * 0.5, s * 0.86)], fill=col)
    return im.resize((size, size), Image.LANCZOS)

def icon_share(size=120, col=(255, 232, 168)):
    s = size * 3
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.line([(s * 0.22, s * 0.72), (s * 0.78, s * 0.24)], fill=col, width=int(s * 0.09))
    d.polygon([(s * 0.84, s * 0.14), (s * 0.84, s * 0.50), (s * 0.52, s * 0.22)], fill=col)
    return im.resize((size, size), Image.LANCZOS)

def icon_comment(size=120, col=(255, 232, 168)):
    s = size * 3
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([s * 0.12, s * 0.18, s * 0.88, s * 0.68], radius=int(s * 0.14), fill=col)
    d.polygon([(s * 0.30, s * 0.66), (s * 0.52, s * 0.66), (s * 0.32, s * 0.90)], fill=col)
    dark = (10, 14, 20)
    for i in range(3):
        d.ellipse([s * (0.26 + i * 0.16), s * 0.38, s * (0.32 + i * 0.16), s * 0.48], fill=dark)
    return im.resize((size, size), Image.LANCZOS)

def icon_plus(size=120, col=(255, 232, 168)):
    s = size * 3
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([s * 0.10, s * 0.10, s * 0.90, s * 0.90], radius=int(s * 0.22),
                        outline=col, width=int(s * 0.10))
    d.line([(s * 0.5, s * 0.28), (s * 0.5, s * 0.72)], fill=col, width=int(s * 0.10))
    d.line([(s * 0.28, s * 0.5), (s * 0.72, s * 0.5)], fill=col, width=int(s * 0.10))
    return im.resize((size, size), Image.LANCZOS)

# ------------------------------------------------------------------ état / timeline
class Timeline:
    def __init__(self, prod):
        self.prod = prod
        vm = json.load(open(os.path.join(prod, "verses_map.json"), encoding="utf-8"))
        self.vm = vm
        self.song_end = vm["song_end"]
        self.fin = vm["fin_video"]
        self.cta = vm["cta_windows"]
        self.accueil = vm["accueil"]
        # lettre d'infos par vers + bornes d'affichage
        nxt = [v["t0"] for v in vm["verses"][1:]] + [self.song_end]
        self.verses = []
        for i, v in enumerate(vm["verses"]):
            t0, t1 = v["t0"], min(nxt[i] - 0.10, v["fin"] + 0.50)
            for a, b in self.cta:                      # la carte ne couvre jamais une typo affichée
                if t1 > a and t0 < b:
                    t1 = min(t1, a - 0.15)
            self.verses.append({**v, "t0": t0, "t1": max(t0 + 0.8, t1)})
        self.first = self.verses[0]["t0"]
        self.last = self.verses[-1]["t1"]

    def verse_at(self, t):
        for v in self.verses:
            if v["t0"] - 0.001 <= t < v["t1"]:
                return v
        return None

    def in_cta(self, t):
        for a, b in self.cta:
            if a <= t < b:
                return (a, b)
        return None

    def in_accueil(self, t):
        for i, (a, b) in enumerate(self.accueil):
            if a <= t < b:
                return i
        return None

# ------------------------------------------------------------------ rendu d'une frame
class Renderer:
    def __init__(self, prod, tl):
        self.prod = prod
        self.tl = tl
        baked = os.path.join(prod, "baked")
        self.scaled = {}
        self.art_dim = {}
        # badge tiles : texte (haut y 165) + soulignement (y 189) — §7.4
        self.badge = {}
        for word, uw in (("DSKY", 62), ("WTBW", 72)):
            t = text_img(word, font("ExtraBold", 32), (255, 255, 255), stroke=3, stroke_fill=(8, 11, 16))
            t = t.crop(t.getbbox())            # recadré sur l'encre -> haut = 165
            lay = Image.new("RGBA", (max(t.width, uw) + 20, 40), (0, 0, 0, 0))
            lay.alpha_composite(t, ((lay.width - t.width) // 2, 0))
            d = ImageDraw.Draw(lay)
            x0 = (lay.width - uw) // 2
            d.rectangle([x0, 22, x0 + uw, 27], fill=(255, 232, 168, 255))   # 189 abs
            self.badge[word] = lay
        self.badge_baked = False

    def get_scaled(self, vid, img):
        if vid not in self.scaled:
            if len(self.scaled) > 3:
                self.scaled.pop(next(iter(self.scaled)))
            self.scaled[vid] = Scaled(img)
        return self.scaled[vid]

    def verse_frame(self, v, t):
        """Frame 1080x1920 numpy pour un vers (art + lettres cuites, extinction si pilule)."""
        if v["id"] not in self.art_dim:
            baked = Image.open(os.path.join(self.prod, "baked", f"{v['id']}.png")).convert("RGB")
            if v.get("extinguish"):
                art = baked.filter(ImageFilter.GaussianBlur(7))
                arr = (np.asarray(art).astype(np.float32) * 0.22).astype(np.uint8)
                letters = Image.open(os.path.join(self.prod, "baked", "letters", f"{v['id']}.png"))
                comp = Image.alpha_composite(Image.fromarray(arr, "RGB").convert("RGBA"), letters).convert("RGB")
                self.art_dim[v["id"]] = comp
            else:
                self.art_dim[v["id"]] = baked
        sc = self.get_scaled(v["id"], self.art_dim[v["id"]])
        z = zoom_travel(t)
        return window(sc.get(z), z, t)

    def gap_frame(self, vref, t):
        z = zoom_travel(t)
        sc = self.get_scaled(vref["id"], self.art_dim.get(vref["id"]) or self.verse_frame_cached(vref))
        return window(sc.get(z), z, t)

    def verse_frame_cached(self, v):
        self.verse_frame(v, 0.0)
        return self.art_dim[v["id"]]

    def card_bg(self, pid_img, t, key="card"):
        sc = self.get_scaled(key, pid_img)
        z = zoom_card(t)
        return window(sc.get(z), z, t, period=7.7, xr=30, yr=26, phase=0.7)

    def card_img(self, pid, blur9=True):
        """Fond de carte : art du plan, flou 9, brightness x 0,72 (§7.2) + redressement
        de lisibilité (l'art nuit du lot SEINEN est très sombre) — mis en cache."""
        key = f"cardimg-{pid}"
        if key not in self.art_dim:
            img = Image.open(os.path.join(self.prod, "baked", "plans", f"{pid}.png")).convert("RGB")
            if blur9:
                img = blur(img, 9).point(lambda px: int(px * 0.72))
            mean = np.asarray(img).mean()
            gain = min(2.2, 74.0 / max(mean, 1.0))
            if gain > 1.0:
                img = img.point(lambda px: min(255, int(px * gain)))
            self.art_dim[key] = img
        return self.art_dim[key]

    # ---- overlays ----
    def badge_layer(self, t, v):
        """Badge clignotant DSKY↔WTBW (§7.4) — jamais sur cartes/CTA."""
        rel = max(0.0, t - v["t0"])
        if t >= v["t1"]:
            return None
        env = min(1.0, rel / 0.4)
        rem = v["t1"] - t
        if rem < 0.2:
            env *= rem / 0.2
        phase = t % 4.8
        # fondu croisé 0,4 s à chaque bascule
        if phase < 2.2:
            w = 1.0
        elif phase < 2.6:
            w = 1.0 - (phase - 2.2) / 0.4
        elif phase < 4.6:
            w = 0.0
        else:
            w = (phase - 4.6) / 0.4
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for word, a in (("DSKY", w), ("WTBW", 1 - w)):
            if a <= 0.004:
                continue
            tile = self.badge[word].copy()
            al = tile.split()[3].point(lambda px: int(px * a * 0.72 * env))
            tile.putalpha(al)
            lay.alpha_composite(tile, ((W - tile.width) // 2, 165))
        return lay

    def filet_layer(self, t):
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        d.rectangle([170, 1560, 910, 1564], fill=(255, 255, 255, 48))
        fr = (t - self.tl.first) / (self.tl.song_end - self.tl.first)
        fr = min(max(fr, 0.0), 1.0)
        if fr > 0:
            d.rectangle([170, 1558, 170 + int(740 * fr), 1566], fill=GOLD_A + (210,))
        return lay

    def pill_layer(self, v, t):
        words = v.get("pill")
        if not words:
            return None
        t0, t1 = v["t0"], v["t1"]
        if not (t0 <= t < t1):
            return None
        prog = (t - t0) / max(0.001, t1 - t0)
        fsize, track = 29, 11
        gap = 16
        while True:
            fnt = font("ExtraBold", fsize)
            widths = []
            for w in words:
                bb = fnt.getbbox(w)
                widths.append(bb[2] - bb[0])
            total = sum(widths) + track * sum(len(w) for w in words) + gap * (len(words) - 1)
            if total <= 672 or (track <= 7 and fsize <= 22):
                break
            if track > 7:
                track -= 2
            else:
                fsize -= 2
        pill = rounded_panel(708, 93, 24, (8, 12, 18, 222), rim=(232, 168, 66, 185), rim_w=2)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        x = max(18.0, (708 - total) / 2)
        active = min(len(words) - 1, int(prog * len(words)))
        drift = 9 * math.sin(2 * math.pi * prog)
        for i, (w, wd) in enumerate(zip(words, widths)):
            col = GOLD_HOT if i == active else (222, 228, 236)
            tw = text_img(w, fnt, col, tracking=track,
                          stroke=3 if i == active else 0,
                          stroke_fill=(255, 224, 122) if i == active else INK)
            pill.alpha_composite(tw, (int(x + drift), int(46 - tw.height / 2)))
            x += wd + track * len(w) + gap
        # curseur karaoké en bas de pilule
        d = ImageDraw.Draw(pill)
        d.rounded_rectangle([24, 82, 24 + int(660 * prog), 86], radius=2, fill=GOLD_A + (215,))
        lay.alpha_composite(pill, (186, 1452))
        return lay

    # ---- cartes ----
    def accueil_layers(self, idx, t):
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        if idx == 0:
            t1 = text_img("SALUT · WTBW", font("ExtraBold", 76), (255, 255, 255), tracking=3,
                          stroke=4, stroke_fill=INK)
            paste_center(lay, t1, 880)
            t2 = text_img("Wolof TechStein beat wê", font("SemiBold", 40), GOLD_A)
            paste_center(lay, t2, 990)
        else:
            t1 = text_img("BIENVENUE SUR WTBW", font("ExtraBold", 64), (255, 255, 255), tracking=3,
                          stroke=4, stroke_fill=INK)
            paste_center(lay, t1, 700)
            t2 = text_img("Soutiens le son en douceur :", font("SemiBold", 34), GOLD_A)
            paste_center(lay, t2, 810)
            icons = [(icon_heart(64), "LIKE"), (icon_share(64), "PARTAGE"), (icon_comment(64), "COMMENTE")]
            x = W // 2 - 380
            for ic, lab in icons:
                pil = rounded_panel(244, 92, 24, (10, 16, 24, 235), rim=(232, 168, 66, 185))
                pil.alpha_composite(ic, (14, 14))
                lt = text_fit(lab, "Bold", 26, (240, 240, 240), 244 - 96 - 12)
                pil.alpha_composite(lt, (92, int(46 - lt.height / 2)))
                lay.alpha_composite(pil, (x, 920))
                x += 264
        return lay

    def cta_layer(self, prog):
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        panel = rounded_panel(800, 890, 28, (6, 10, 16, 235), rim=(232, 168, 66, 215), rim_w=3)
        bell = icon_bell(150)
        panel.alpha_composite(bell, ((800 - 150) // 2, 120))
        t1 = text_img("CLIQUE SUR +", font("ExtraBold", 56), (255, 255, 255), tracking=2, stroke=3)
        panel.alpha_composite(t1, ((800 - t1.width) // 2, 330))
        past = rounded_panel(520, 96, 48, (232, 168, 66, 255))
        pt = text_img("LIKE & PARTAGE", font("ExtraBold", 42), (10, 14, 20))
        past.alpha_composite(pt, ((520 - pt.width) // 2, int(48 - pt.height / 2)))
        panel.alpha_composite(past, ((800 - 520) // 2, 480))
        t3 = text_img("Commente si tu aimes · WTBW", font("SemiBold", 30), (222, 228, 236))
        panel.alpha_composite(t3, ((800 - t3.width) // 2, 660))
        lay.alpha_composite(panel, ((W - 800) // 2, 310))
        return lay

    def fin_layer(self, t):
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        t1 = text_img("MERCI · WTBW", font("ExtraBold", 76), (255, 255, 255), tracking=3,
                      stroke=4, stroke_fill=INK)
        paste_center(lay, t1, 436)
        t2 = text_img("Merci d'avoir écouté · Wolof TechStein beat wê", font("SemiBold", 30), GOLD_A)
        paste_center(lay, t2, 566)
        t3 = text_img("TU ES TROP BELLE · DSKY", font("Bold", 36), (240, 240, 240), tracking=2, stroke=2)
        paste_center(lay, t3, 700)
        icons = [(icon_heart(72), "LIKE"), (icon_share(72), "PARTAGE"), (icon_comment(72), "COMMENTE")]
        x = W // 2 - 375
        for ic, lab in icons:
            pil = rounded_panel(240, 130, 26, (8, 13, 20, 235), rim=(232, 168, 66, 185))
            pil.alpha_composite(ic, ((240 - 72) // 2, 12))
            lt = text_fit(lab, "Bold", 24, (240, 240, 240), 224)
            pil.alpha_composite(lt, ((240 - lt.width) // 2, 92))
            lay.alpha_composite(pil, (x, 860))
            x += 255
        return lay


def render(prod, start=0.0, end=None, out_path=None, silent=True):
    tl = Timeline(prod)
    end = tl.fin if end is None else min(end, tl.fin)
    R = Renderer(prod, tl)
    ensure_dir(os.path.dirname(out_path) or ".")
    n0, n1 = int(start * FPS), int(end * FPS)

    cmd = [FF, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
           "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
           "-color_trc", "bt709", out_path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    art_default = None
    try:
        for k in range(n0, n1):
            t = k / FPS
            in_acc = tl.in_accueil(t)
            cta = tl.in_cta(t)
            v = tl.verse_at(t)

            if in_acc is not None:
                pid = tl.verses[0]["plan"]
                frame = R.card_bg(R.card_img(pid), t, key="card-acc").astype(np.float32)
                frame = frame * 0.45 + np.array([6, 9, 14]) * 0.55   # voile #06090E 55%
                frame = frame.astype(np.uint8)
                base = Image.fromarray(frame, "RGB").convert("RGBA")
                base.alpha_composite(R.accueil_layers(in_acc, t))
                frame = np.asarray(base.convert("RGB"))
                frame = apply_grain(frame, k, 0.28)
            elif cta is not None:
                if v is None:
                    vref = None
                    for vv in tl.verses:
                        if vv["t1"] <= t:
                            vref = vv
                    if vref is None:
                        vref = tl.verses[0]
                    vimg = R.verse_frame_cached(vref)
                    sc = R.get_scaled(f"gap-{vref['id']}", vimg)
                    z = zoom_travel(t)
                    frame = window(sc.get(z), z, t)
                else:
                    frame = R.verse_frame(v, t)
                base = Image.fromarray(frame, "RGB").convert("RGBA")
                prog = (t - cta[0]) / max(0.001, cta[1] - cta[0])
                base.alpha_composite(R.cta_layer(prog))
                frame = np.asarray(base.convert("RGB"))
                frame = apply_grain(frame, k, 0.28)
            elif t >= tl.song_end:
                # carte finale MERCI · WTBW (fin_chanson → +5,00 s)
                pid = tl.verses[-1]["plan"]
                frame = R.card_bg(R.card_img(pid), t, key="card-fin").astype(np.float32)
                frame = frame * 0.45 + np.array([6, 9, 14]) * 0.55
                frame = frame.astype(np.uint8)
                base = Image.fromarray(frame, "RGB").convert("RGBA")
                base.alpha_composite(R.fin_layer(t))
                frame = np.asarray(base.convert("RGB"))
                frame = apply_grain(frame, k, 0.28)
            elif v is not None:
                frame = R.verse_frame(v, t)
                # respiration lumineuse ±12 % sur les vers > 3,5 s (§5.3)
                dur = v["t1"] - v["t0"]
                rel = t - v["t0"]
                if dur > 3.5 and rel < 0.35:
                    f = 1.0 - 0.12 * math.sin(math.pi * rel / 0.35)
                    frame = (frame.astype(np.float32) * f).astype(np.uint8)
                base = Image.fromarray(frame, "RGB").convert("RGBA")
                lay = R.badge_layer(t, v)
                if lay is not None:
                    base.alpha_composite(lay)
                pl = R.pill_layer(v, t)
                if pl is not None:
                    base.alpha_composite(pl)
                frame = np.asarray(base.convert("RGB"))
                frame = apply_grain(frame, k, 0.045)
            else:
                # respiration nue entre les vers : décor du vers le plus proche
                vref = None
                for vv in tl.verses:
                    if vv["t1"] <= t:
                        vref = vv
                nxt = None
                for vv in tl.verses:
                    if vv["t0"] > t:
                        nxt = vv
                        break
                vref = nxt or vref or tl.verses[0]
                frame = R.verse_frame(vref, t)
                frame = apply_grain(frame, k, 0.045)

            # filet de progression (hors cartes finales ; présent vers+gaps)
            if not (t >= tl.song_end):
                base = Image.fromarray(frame, "RGB").convert("RGBA")
                base.alpha_composite(R.filet_layer(t))
                frame = np.asarray(base.convert("RGB"))
            frame = (frame.astype(np.float32) * vignette()).astype(np.uint8)
            proc.stdin.write(frame.tobytes())
            if k % 300 == 0:
                print(f"  frame {k}/{n1} t={t:.1f}s", flush=True)
    finally:
        proc.stdin.close()
        proc.wait()
    print(f"render -> {out_path} ({(n1-n0)/FPS:.1f}s)")
    return out_path

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("prod")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out = args.out or os.path.join(args.prod, "out", "clip-silent.mp4")
    render(args.prod, args.start, args.end, out)
