#!/usr/bin/env python3
"""render.py — clip 9:16 1080x1920@30 (v6.4 §5-§7, §12).

Mouvement : fenêtre glissante sur source x1.10 (aucun resize par frame), 4 trajectoires,
xfade 0.35 s entre segments, extinction (Brightness 0.22 + blur 7) UNIQUEMENT quand la pilule
FR est active (MODE HYBRIDE), grain 8 motifs un par frame (0.045 ; 0.28 sur cartes), vignette
masque L #04080C, badge clignotant Daïsky<->WTBW (2.4 s/mot, fondu 0.4 s, alpha<=0.72),
filet y1560, pilule FR défilante y1452-1545, CTA clochettes dans les fenêtres instrumentales,
cartes SALUT·WTBW (2 temps) et MERCI·WTBW animées (zoom+ dérive, grain 0.28).
Pipe rawvideo rgb24 -> ffmpeg + audio_clip.m4a, puis passage faststart.
"""
import json, os, math, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
FFMPEG = "/usr/local/lib/python3.13/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v9.0.2"
W, H, FPS = 1080, 1920, 30
SC = 1.10
BW, BH = int(W * SC), int(H * SC)          # 1188 x 2112
MX, MY = BW - W, BH - H                    # 108 x 192
TITRE, ARTISTE = "MONSTER POSITIVE", "DSKY"
OR = (232, 168, 62)

mp = json.load(open(os.path.join(ROOT, "verses_map.json"), encoding="utf-8"))
VERSES = mp["verses"]; D = mp["duree_audio_s"]; CTA = mp["cta"]
T_END = mp["duree_clip_s"]; N = round(T_END * FPS)
T0 = VERSES[0]["t"]

MON = os.path.join(ROOT, "fonts", "Montserrat.ttf")
NOTO = os.path.join(ROOT, "fonts", "NotoSansKR.ttf")
_noto = {}
def noto(size):
    if size not in _noto:
        f = ImageFont.truetype(NOTO, size)
        try: f.set_variation_by_axes([700])
        except Exception: pass
        _noto[size] = f
    return _noto[size]
_fc = {}
def mont(size, wght=800):
    k = (size, wght)
    if k not in _fc:
        f = ImageFont.truetype(MON, size)
        try: f.set_variation_by_axes([wght])
        except Exception: pass
        _fc[k] = f
    return _fc[k]

def tracked(d, xy, text, f, fill, tr=0, anchor_center=False):
    """texte avec interlettrage tr px ; anchor_center=True centre sur xy[0]."""
    widths = [d.textlength(c, font=f) for c in text]
    total = sum(widths) + tr * max(0, len(text) - 1)
    x = xy[0] - total / 2 if anchor_center else xy[0]
    y = xy[1]
    for c, w in zip(text, widths):
        fc = noto(f.size) if ord(c) >= 0xAC00 else f
        d.text((x, y), c, font=fc, fill=fill)
        x += w + tr
    return total

def tracked_w(text, f, tr=0):
    d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    return sum(d.textlength(c, font=f) for c in text) + tr * max(0, len(text) - 1)

# ---------- grains (8 motifs, un par frame) ----------
rng = np.random.default_rng(42)
GRAINS = [rng.integers(-14, 15, size=(H, W), dtype=np.int16) for _ in range(8)]
# ---------- vignette masque L ----------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
cx, cy = W / 2, H / 2
r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / math.hypot(cx, cy)
VIG = np.clip((r * 1.35) ** 2 * 86 / 255.0, 0, 86 / 255.0).astype(np.float32)
VIG = np.array(Image.fromarray((VIG * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(34)), dtype=np.float32) / 255.0
VIGC = np.array([4, 8, 12], dtype=np.float32)

def apply_fx(arr, k, grain_w):
    g = GRAINS[k % 8]
    arr = arr.astype(np.int16) + (g * grain_w).astype(np.int16)[..., None]  # arr + g*blend (g=±14)
    arr = np.clip(arr, 0, 255)
    v = VIG[..., None]
    arr = arr * (1 - v) + VIGC * v
    return arr.astype(np.uint8)

# ---------- trajectoires (4) ----------
TRAJ = [(0.0, 0.02, 1.0, 0.98), (1.0, 0.02, 0.0, 0.98), (0.18, 0.98, 0.82, 0.02), (0.82, 0.02, 0.18, 0.98)]

# ---------- plans : chargement paresseux ----------
_cache = {}
def baked_name(img):
    return "baked-" + os.path.basename(img)

def get_plan(img):
    if img not in _cache:
        if len(_cache) > 2:
            _cache.clear()
        b = Image.open(os.path.join(ROOT, img)).convert("RGB")
        big = b.resize((BW, BH), Image.LANCZOS)
        et = big.filter(ImageFilter.GaussianBlur(0))  # placeholder
        from PIL import ImageEnhance
        et = ImageEnhance.Brightness(big).enhance(0.22).filter(ImageFilter.GaussianBlur(7))
        _cache[img] = (big, et)
    return _cache[img]

def window(big, i, u):
    ax0, ay0, ax1, ay1 = TRAJ[i % 4]
    x = int((ax0 + (ax1 - ax0) * u) * MX)
    y = int((ay0 + (ay1 - ay0) * u) * MY)
    return big.crop((x, y, x + W, y + H))

# ---------- icônes vectorielles ----------
def icon_heart(d, x, y, s, col, wd=6):
    r = s / 2
    d.arc([x, y, x + s, y + s], 180, 360, fill=col, width=wd)
    d.arc([x + s / 2, y, x + 3 * s / 2, y + s], 180, 360, fill=col, width=wd)
    d.line([x + wd / 2, y + s / 2, x + s / 2, y + s + s / 2], fill=col, width=wd)
    d.line([x + s + s / 2 - wd / 2, y + s / 2, x + s / 2, y + s + s / 2], fill=col, width=wd)

def icon_plus(d, x, y, s, col, wd=6):
    d.rounded_rectangle([x, y, x + s, y + s], radius=s * 0.28, outline=col, width=wd)
    m = s * 0.28
    d.line([x + s / 2, y + m, x + s / 2, y + s - m], fill=col, width=wd)
    d.line([x + m, y + s / 2, x + s - m, y + s / 2], fill=col, width=wd)

def icon_bubble(d, x, y, s, col, wd=6):
    d.rounded_rectangle([x, y, x + s, y + s * 0.72], radius=s * 0.25, outline=col, width=wd)
    d.polygon([(x + s * 0.2, y + s * 0.68), (x + s * 0.42, y + s * 0.68), (x + s * 0.2, y + s)], fill=col)

ICONS = [icon_heart, icon_plus, icon_bubble]
STICKERS = [("LIKE LA VIDÉO", "Laisse un cœur si tu valides"),
            ("CLIQUE SUR + POUR T'ABONNER", "Rejoins Wolof TechStein beat 웨"),
            ("COMMENTE SI TU AIMES !", "Dis-nous ton vers préféré")]

def draw_sticker(ov, cx, cy, i, t):
    T = 2.2 + 0.3 * i
    dy = 8 * math.sin(2 * math.pi * t / T + i * 1.7)
    dx = 5 * math.sin(2 * math.pi * t / (T * 0.8) + i)
    x, y = cx - 350 + dx, cy - 76 + dy
    d0 = ImageDraw.Draw(ov)
    d0.rounded_rectangle([x, y, x + 700, y + 152], radius=38, fill=(10, 14, 20, 225), outline=(255, 255, 255, 60), width=2)
    breathe = 1 + 0.045 * math.sin(2 * math.pi * t / 1.6 + i)
    s = 92 * breathe
    ix, iy = x + 44, y + (152 - s) / 2
    tmp = Image.new("RGBA", (int(s * 3), int(s * 3)), (0, 0, 0, 0))
    ICONS[i](ImageDraw.Draw(tmp), s, s, s * 2, (255, 255, 255, 255), wd=int(7 * breathe))
    tmp = tmp.resize((int(s * 3 * 0.9), int(s * 3 * 0.9)), Image.LANCZOS)  # ~90px
    ov.alpha_composite(tmp, (int(ix), int(iy)))
    d = ImageDraw.Draw(ov)
    f1, f2 = mont(30, 800), mont(20, 600)
    tracked(d, (x + 190, y + 34), STICKERS[i][0], f1, (255, 255, 255, 255), tr=4)
    tracked(d, (x + 190, y + 82), STICKERS[i][1], f2, (255, 255, 255, 175), tr=1)

def draw_bell(ov, t, w0):
    """cloche vectorielle pendule ±12°, halo, 2 ondes (0.9 s), 3 étincelles, flèche clignotante."""
    SS = 3
    tile = Image.new("RGBA", (720 * SS, 720 * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    px, py = 360 * SS, 120 * SS          # pivot
    ang = math.radians(12 * math.sin(2 * math.pi * (t - w0) / 4.0))
    L = 300 * SS
    ex = px + L * math.sin(ang); ey = py + L * math.cos(ang)
    d.line([px, py, ex, ey], fill=(255, 255, 255, 255), width=10 * SS)
    # cloche
    bw, bh = 150 * SS, 170 * SS
    d.arc([ex - bw / 2, ey - bh * 0.2, ex + bw / 2, ey + bh * 0.8], 180, 360, fill=(255, 255, 255, 255), width=10 * SS)
    d.line([ex - bw / 2, ey + bh * 0.3, ex + bw / 2, ey + bh * 0.3], fill=(255, 255, 255, 255), width=10 * SS)
    d.line([ex - bw / 2, ey + bh * 0.3, ex - bw / 2, ey + bh * 0.55], fill=(255, 255, 255, 255), width=10 * SS)
    d.line([ex + bw / 2, ey + bh * 0.3, ex + bw / 2, ey + bh * 0.55], fill=(255, 255, 255, 255), width=10 * SS)
    d.ellipse([ex - 16 * SS, ey + bh * 0.55, ex + 16 * SS, ey + bh * 0.55 + 32 * SS], fill=(255, 255, 255, 255))
    # ondes concentriques période 0.9 s
    ph = (t - w0) % 0.9 / 0.9
    for j in range(2):
        rr = (ph + j * 0.5) % 1.0
        a = int(160 * (1 - rr))
        d.ellipse([ex - 120 * SS * rr - 40 * SS, ey - 120 * SS * rr - 40 * SS,
                   ex + 120 * SS * rr + 40 * SS, ey + 120 * SS * rr + 40 * SS], outline=(255, 255, 255, a), width=5 * SS)
    # 3 étincelles
    for j, (sx, sy) in enumerate([(0.25, 0.3), (0.75, 0.25), (0.6, 0.7)]):
        sxp, syp = px + (sx - 0.5) * 500 * SS, py + sy * 400 * SS
        rr = 14 * SS * (0.7 + 0.3 * math.sin(t * 5 + j))
        d.line([sxp - rr, syp, sxp + rr, syp], fill=(255, 255, 255, 220), width=5 * SS)
        d.line([sxp, syp - rr, sxp, syp + rr], fill=(255, 255, 255, 220), width=5 * SS)
    # flèche clignotante vers la cloche
    if math.sin(t * 4) > 0:
        ax, ay = px, py - 70 * SS
        d.polygon([(ax, ay + 40 * SS), (ax - 24 * SS, ay), (ax + 24 * SS, ay)], fill=OR + (255,))
    tile = tile.filter(ImageFilter.GaussianBlur(0))  # net
    halo = tile.filter(ImageFilter.GaussianBlur(18 * SS)).point(lambda a: int(a * 0.5))
    out = Image.new("RGBA", tile.size, (0, 0, 0, 0))
    out.alpha_composite(halo); out.alpha_composite(tile)
    out = out.resize((720, 720), Image.LANCZOS)
    ov.alpha_composite(out, (180, 640))

def draw_cta(ov, t, w0, w1):
    a = min(1.0, (t - w0) / 0.35, (w1 - t) / 0.35)
    if a <= 0: return
    tile = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    d.rounded_rectangle([214, 648, 866, 1312], radius=54, fill=(6, 10, 16, int(235 * a)))
    tile = tile.filter(ImageFilter.GaussianBlur(5))
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base.alpha_composite(tile)
    draw_bell(base, t, w0)
    d = ImageDraw.Draw(base)
    f = mont(56, 800)
    tracked(d, (540, 1010), "CLIQUE SUR +", f, (255, 255, 255, int(255 * a)), tr=5, anchor_center=True)
    d.rounded_rectangle([330, 1100, 750, 1196], radius=48, fill=OR + (int(255 * a),), outline=(255, 255, 255, int(120 * a)), width=3)
    tracked(d, (540, 1122), "LIKE & PARTAGE", mont(34, 800), (10, 10, 14, int(255 * a)), tr=6, anchor_center=True)
    tracked(d, (540, 1240), "Commente si tu aimes · WTBW", mont(30, 600), (255, 255, 255, int(220 * a)), tr=2, anchor_center=True)
    ov.alpha_composite(base)

# ---------- pilule FR défilante ----------
def draw_pill(ov, v, t):
    tr = v["traduction"]
    if not tr: return
    u = min(1.0, max(0.0, (t - v["t"]) / v["affichage_s"]))
    a = min(1.0, (t - v["t"]) / 0.35, (v["t"] + v["affichage_s"] - t) / 0.35)
    if a <= 0: return
    dx = 9 * math.sin(2 * math.pi * (t - v["t"]) / max(0.5, v["affichage_s"]))
    pill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(pill)
    # pilule plus haute et plus lisible : y 1444 -> 1556
    d.rounded_rectangle([186, 1444, 894, 1556], radius=26, fill=(8, 12, 18, int(228 * a)), outline=OR + (int(200 * a),), width=3)
    words = tr.split()
    fsize, tr_px = 32, 6
    f = mont(fsize, 800)
    def total_w():
        return sum(tracked_w(w, f, tr_px) for w in words) + tr_px * (len(words) - 1)
    while total_w() > 690 and fsize > 22:
        fsize -= 2; f = mont(fsize, 800)
    x = 540 - total_w() / 2 + dx
    act = min(len(words) - 1, int(u * len(words)))
    for j, w in enumerate(words):
        col = (255, 224, 122, int(255 * a)) if j == act else (240, 244, 248, int(235 * a))
        if j == act:  # halo 3 px
            m = Image.new("L", (W, H), 0)
            ImageDraw.Draw(m).text((x, 1476), w, font=f, fill=255)
            m = m.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(3))
            halo = Image.new("RGBA", (W, H), (255, 200, 80, int(170 * a)))
            pill.paste(halo, (0, 0), m)
        d = ImageDraw.Draw(pill)
        tracked(d, (x, 1476), w, f, col, tr=tr_px)
        x += tracked_w(w, f, tr_px) + tr_px
    d = ImageDraw.Draw(pill)
    d.rectangle([186, 1548, 186 + int(708 * u), 1556], fill=OR + (int(255 * a),))
    ov.alpha_composite(pill)

# ---------- badge clignotant + filet ----------
def draw_badge(ov, t, v):
    rel = t % 4.8
    fade_in = min(1.0, (t - v["t"]) / 0.4)
    fade_out = min(1.0, (v["fin"] - t) / 0.2)
    ag = 0.72 * min(fade_in, fade_out)
    if ag <= 0: return
    d = ImageDraw.Draw(ov)
    f = mont(32, 800)
    words = [(ARTISTE, 62), ("WTBW", 72)]
    # fondu croisé 0.4 s autour des bascules (2.4 et 4.8)
    def alpha_of(idx):
        other = 1 - idx
        sw = rel if idx == 0 else (rel - 2.4 if rel >= 2.4 else rel + 2.4)
        return None
    a0 = 1.0 if rel < 2.4 else 0.0
    if 2.4 - 0.4 < rel < 2.4 + 0.4:
        a0 = 1 - (rel - (2.4 - 0.4)) / 0.8
    a0 = min(1.0, max(0.0, a0))
    for idx, (wtext, uw) in enumerate(words):
        a = (a0 if idx == 0 else 1 - a0) * ag
        if a <= 0.01: continue
        col = (255, 255, 255, int(255 * a))
        # liséré sombre (stroke 3)
        tw = tracked_w(wtext, f, 2)
        for ox, oy in [(-3, 0), (3, 0), (0, -3), (0, 3)]:
            tracked(d, (540 + ox, 165 + oy), wtext, f, (5, 6, 8, int(200 * a)), tr=2, anchor_center=True)
        tracked(d, (540, 165), wtext, f, col, tr=2, anchor_center=True)
        d.rectangle([540 - uw / 2, 189, 540 + uw / 2, 192], fill=(255, 255, 255, int(255 * a)))

def draw_filet(ov, t):
    fr = min(1.0, max(0.0, (t - T0) / (D - T0)))
    ov_l = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov_l)
    d.rectangle([170, 1558, 910, 1562], fill=(255, 255, 255, 48))
    d.rectangle([170, 1556, 170 + int(740 * fr), 1564], fill=OR + (210,))
    ov.alpha_composite(ov_l)

# ---------- cartes ----------
def card_bg(plan_img, t):
    b = Image.open(os.path.join(ROOT, plan_img)).convert("RGB")
    b = b.filter(ImageFilter.GaussianBlur(9))
    from PIL import ImageEnhance
    b = ImageEnhance.Brightness(b).enhance(0.62)
    z = 1.04 + 0.035 * math.sin(2 * math.pi * t / 7.7)
    dx = 6 * math.sin(2 * math.pi * t / 9.3)
    dy = 8 * math.sin(2 * math.pi * t / 7.7 + 1.0)
    bw, bh = int(W * z), int(H * z)
    b = b.resize((bw, bh), Image.LANCZOS)
    x = (bw - W) // 2 + int(dx); y = (bh - H) // 2 + int(dy)
    b = b.crop((max(0, x), max(0, y), max(0, x) + W, max(0, y) + H))
    ov = b.convert("RGBA")
    veil = Image.new("RGBA", (W, H), (6, 9, 14, 140))
    ov.alpha_composite(veil)
    return ov

def draw_card(ov, t, kind):
    d = ImageDraw.Draw(ov)
    # filets horizontaux
    d.line([170, 310, 910, 310], fill=(255, 255, 255, 90), width=2)
    d.line([170, 1470, 910, 1470], fill=(255, 255, 255, 90), width=2)
    tracked(d, (540, 340), "WTBW · WOLOF TECHSTEIN BEAT WÊ !", mont(30, 800), (255, 255, 255, 235), tr=2, anchor_center=True)
    if kind == "accueil":
        if t < T0 / 2:
            dy = 6 * math.sin(2 * math.pi * t / 2.2)
            tracked(d, (540, 520 + dy), "SALUT · WTBW", mont(76, 800), (255, 255, 255, 255), tr=3, anchor_center=True)
            tracked(d, (540, 630), "Wolof TechStein beat 웨", mont(34, 700), OR + (255,), tr=2, anchor_center=True)
            d.rounded_rectangle([290, 700, 790, 786], radius=18, outline=(255, 255, 255, 160), width=2, fill=(8, 10, 14, 200))
            tracked(d, (540, 722), f"{TITRE} — {ARTISTE}", mont(36, 800), (255, 255, 255, 255), tr=2, anchor_center=True)
        else:
            tracked(d, (540, 500), "BIENVENUE SUR WTBW", mont(64, 800), (255, 255, 255, 255), tr=3, anchor_center=True)
            tracked(d, (540, 610), "Soutiens le son en douceur :", mont(34, 600), (255, 255, 255, 230), tr=1, anchor_center=True)
            tracked(d, (540, 690), f"{TITRE} · {ARTISTE}", mont(36, 800), OR + (255,), tr=2, anchor_center=True)
    else:
        # MERCI · WTBW (baseline ~436)
        tw = tracked_w("MERCI · WTBW", mont(76, 800), 3)
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).text((540 - tw / 2, 400), "MERCI · WTBW", font=mont(76, 800), fill=255)
        cont = m.filter(ImageFilter.MaxFilter(9))
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        layer.paste(Image.new("RGBA", (W, H), (5, 6, 8, 255)), (0, 0), cont)
        ov.alpha_composite(layer)
        tracked(d, (540, 400), "MERCI · WTBW", mont(76, 800), (255, 255, 255, 255), tr=3, anchor_center=True)
        tracked(d, (540, 500), f"Merci d'avoir écouté · Wolof TechStein beat 웨 (WTBW)", mont(30, 600), (255, 255, 255, 230), tr=1, anchor_center=True)
        d.rounded_rectangle([300, 580, 780, 660], radius=18, outline=(255, 255, 255, 160), width=2, fill=(8, 10, 14, 200))
        tracked(d, (540, 600), f"{TITRE} · {ARTISTE}", mont(34, 800), (255, 255, 255, 255), tr=2, anchor_center=True)
    for i in range(3):
        draw_sticker(ov, 540, 921 + i * 200, i, t)   # centres y 921 / 1121 / 1321

# ---------- boucle principale ----------
def verse_at(t):
    for i, v in enumerate(VERSES):
        if v["t"] <= t < v["fin"]:
            return i, v
    return (len(VERSES) - 1, VERSES[-1]) if t >= VERSES[-1]["t"] else (0, VERSES[0])

def main():
    out_tmp = os.path.join(ROOT, "livrables", "clip_tmp.mp4")
    out_fin = os.path.join(ROOT, "livrables", f"{TITRE.replace(' ', '-')}-{ARTISTE}-9x16.mp4")
    cmd = [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", os.path.join(ROOT, "livrables", "audio_clip.m4a"), "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-c:a", "copy", "-shortest", out_tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    prev_arr = None; prev_seg = None
    for k in range(N):
        t = k / FPS
        if t < T0:
            ov = card_bg(os.path.join("fonds", baked_name(VERSES[0]["image"])), t)
            draw_card(ov, t, "accueil")
            arr = apply_fx(np.array(ov.convert("RGB")), k, 0.28)
        elif t >= D:
            last = baked_name(VERSES[-1]["image"])
            ov = card_bg(os.path.join("fonds", last), t - D)
            draw_card(ov, t - D, "finale")
            arr = apply_fx(np.array(ov.convert("RGB")), k, 0.28)
        else:
            i, v = verse_at(t)
            big, et = get_plan(os.path.join("fonds", baked_name(v["image"])))
            u = min(1.0, max(0.0, (t - v["t"]) / max(0.01, v["fin"] - v["t"])))
            frame_n = window(big, i, u)
            # EXTINCTION SUPPRIMÉE (demande artiste 2026-11-11) : les paroles peintes
            # restent toujours 100 % nettes ; la pilule FR défile en bas sans voiler.
            # respiration lumineuse ±12 % sur les vers > 3.5 s
            if (v["fin"] - v["t"]) > 3.5:
                b = 1 + 0.12 * math.sin(2 * math.pi * (t - v["t"]) / (v["fin"] - v["t"]))
                frame_n = frame_n.point(lambda px: min(255, int(px * b)))
            arr = apply_fx(np.array(frame_n), k, 0.045)
            # fondu enchaîné 0.35 s entre segments
            if prev_arr is not None and prev_seg is not None and t - v["t"] < 0.35 and prev_seg != i:
                a = (t - v["t"]) / 0.35
                arr = (prev_arr.astype(np.float32) * (1 - a) + arr.astype(np.float32) * a).astype(np.uint8)
            prev_arr = arr; prev_seg = i
            ov = Image.fromarray(arr, "RGB").convert("RGBA")
            draw_badge(ov, t, v)
            draw_filet(ov, t)
            draw_pill(ov, v, t)
            for w0, w1 in CTA:
                if w0 <= t <= w1:
                    draw_cta(ov, t, w0, w1)
            arr = np.array(ov.convert("RGB"))
        p.stdin.write(arr.tobytes())
        if k % 300 == 0:
            print(f"frame {k}/{N} t={t:.2f}s", flush=True)
    p.stdin.close(); p.wait()
    print("pass 1 ok ->", out_tmp)
    subprocess.run([FFMPEG, "-y", "-i", out_tmp, "-c", "copy", "-movflags", "+faststart", out_fin],
                   capture_output=True)
    print("faststart ok ->", out_fin)

if __name__ == "__main__":
    main()
