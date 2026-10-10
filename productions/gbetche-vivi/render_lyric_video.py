#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Clip lyrics 9:16 — Gbètché vivi (Dsky). 1080x1920 / 30 fps / H.264 CRF 24 / bt709.

Timeline (aucun decalage des horodatages fournis par l'artiste, §6 v5.7) :
  0,000 -> 5,867   carte d'accueil LIBRE (aucune parole) + clochette et CTA des l'ouverture
                   (moteur render_intro_cta.py) ; l'audio de cette zone EST l'entree du morceau
  5,867 -> 194,83  chanson + paroles, badge, clochettes dans les fenetres sans texte >= 5 s
  194,83 -> 199,83 carte finale « Merci d'avoir regardé » + code 0314 (silence)

Exigence artiste du tour 6 : **les paroles ne doivent pas cacher le visage**.
Les tetes des 26 fonds tiennent toutes au-dessus de y = 1134 (58,9 % de la hauteur, mesure
du detecteur de peau, cou inclus). Le bloc de paroles est donc cale en y 1160 -> 1330.
Le rendu AUTO-VÉRIFIE : a chaque frame controlee, la zone du visage doit etre strictement
identique a l'image de fond (seule exception autorisee : le bandeau du badge, y 152 -> 204).
"""
import csv, glob, json, math, os, re, subprocess, sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
# v2 = texte grave DANS les images + autocollants/icnes dessines par le moteur.
# Le fond de l'intro est fige a l'import de render_intro_cta -> drapeau pose AVANT.
V2 = ("--v2" in sys.argv) or os.environ.get("V2") == "1"
if V2:
    os.environ["V2"] = "1"
else:
    os.environ.pop("V2", None)
import render_intro_cta as INTRO
from render_intro_cta import W, H, FPS, font, draw_spaced, text_w, grad_mask, fade
import stickers as ST

PERS = os.path.join(HERE, "personnages")
OUT = os.path.join(HERE, "livrables")
os.makedirs(OUT, exist_ok=True)

T_INTRO = 5.867
D_SONG = 194.83
T_SONG_END = D_SONG
T_TAIL = 5.0
T_TOTAL = T_SONG_END + T_TAIL
N_FRAMES = int(round(T_TOTAL * FPS))

FACE_LIMIT = 1134                 # bas de tete max mesure sur les 26 fonds
LY_TOP, LY_BOT = 1160, 1330       # bloc de paroles : sous le visage, au-dessus de y 1574
BADGE_BAND = (140, 216)           # seule retouche autorisee au-dessus de FACE_LIMIT
LY_SAFE_W = 740
GOLD, CREAM, DIM = (255, 211, 90), (255, 243, 214), (214, 202, 178)
WAVE_AMP, WAVE_HZ = 4.5, 0.9
BELL_WINDOWS = [(30.24, 41.60), (94.38, 106.57), (173.11, 181.17)]
BADGE_Y, BADGE_OP = 160, 0.75
FILL = {27: "anim-09", 28: "anim-13", 29: "anim-22", 30: "anim-26"}   # A27-A30 en attente
CODE = "0314"


V2BG = {1: "anim-v2-01", 3: "anim-v2-03", 5: "anim-v2-05",
        12: "anim-v2-12", 29: "anim-v2-29", 30: "anim-v2-30"}   # plans ou l'ecriture a du sens


def bg_for(n):
    if V2 and n in V2BG:
        q = os.path.join(PERS, V2BG[n] + ".png")
        if os.path.exists(q):
            return q
    p = os.path.join(PERS, f"anim-{n:02d}.png")
    if not os.path.exists(p):
        p = os.path.join(PERS, f"{FILL[n]}.png")
    return p


def shots():
    rows = list(csv.DictReader(open(os.path.join(HERE, "plan_fonds.tsv"), encoding="utf-8"), delimiter="\t"))
    out = []
    for r in rows:
        n = int(r["id"][1:])
        out.append((n, float(r["debut"]), float(r["fin"]), bg_for(n), n in FILL))
    return out


def verses():
    src = glob.glob(os.path.join(REPO, "Gb*tch* vivi - Bandit positif.txt"))[0]
    raw = []
    for ln in open(src, encoding="utf-8"):
        m = re.match(r"\[(\d\d):(\d\d\.\d+)\](.*)", ln.strip())
        if not m:
            continue
        t = int(m.group(1)) * 60 + float(m.group(2))
        txt = m.group(3).replace("\u200e", "").replace("\u200f", "").strip()
        if txt:
            raw.append((t, txt))
    v = []
    for i, (t, txt) in enumerate(raw):
        nxt = raw[i + 1][0] if i + 1 < len(raw) else D_SONG
        d = min(4.0, max(2.0, 0.07 * len(txt) + 1.2))
        d = min(d, max(1.0, nxt - t - 0.05))
        v.append((t, min(nxt - 0.02, t + d), txt))
    return v


SH, VS = shots(), verses()
from collections import Counter as _C


def _norm(x):
    return re.sub(r"[^a-z0-9 ]+", "", x.lower()).strip()


_REFC = _C(_norm(v[2]) for v in VS)
REFR = {_norm(v[2]) for v in VS if _REFC[_norm(v[2])] >= 3}   # refrains = lignes qui reviennent 3 fois et plus


def tag_for(txt):
    """etiquette de section, deduite des paroles de l'artiste (rien d'invente)."""
    k = _norm(txt)
    if "wolof techstein" in k:
        return "ADLIB"
    return f"REFRAIN x{_REFC[k]}" if k in REFR else None
SC = Image.new("RGB", (W, H), (4, 6, 10))
_cache = {}


def base_of(path):
    if path not in _cache:
        im = Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)
        g = np.asarray(im.convert("L")).astype(np.float32)
        dark = Image.fromarray(np.clip(g * (0.80 if V2 else 0.74), 0, 255).astype(np.uint8)).convert("RGB")
        out = Image.composite(dark, im, Image.new("L", (W, H), 150))
        band = Image.new("L", (W, H), 0)
        ImageDraw.Draw(band).rounded_rectangle((56, LY_TOP - 40, W - 56, LY_BOT + 30), radius=58, fill=200 if not V2 else 178)
        band = band.filter(ImageFilter.GaussianBlur(40))
        out = Image.composite(SC, out, band)
        _cache[path] = np.asarray(out, np.uint8)
    return _cache[path]


_PROBE = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def fit(text):
    for sz in (78, 70, 64, 58, 52, 46):
        f, sk = font(sz, 800)
        if text_w(_PROBE, text, f, spacing=1, stroke=sk) <= LY_SAFE_W:
            return [text], f, sk
    words = text.split()
    for sz in (72, 64, 58, 52, 46, 42):
        f, sk = font(sz, 800)
        best = None
        for k in range(1, len(words)):
            a, b = " ".join(words[:k]), " ".join(words[k:])
            wm = max(text_w(_PROBE, a, f, spacing=1, stroke=sk), text_w(_PROBE, b, f, spacing=1, stroke=sk))
            if best is None or wm < best[0]:
                best = (wm, [a, b])
        if best and best[0] <= LY_SAFE_W:
            return best[1], f, sk
    f, sk = font(40, 800)
    return [text], f, sk


def lyric_layer(t, t0, t1, lines, f, sk):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    prog = 0.0 if t1 <= t0 else min(1.0, max(0.0, (t - t0) / (t1 - t0)))
    flat = " ".join(lines).split()
    n = max(1, len(flat))
    act = min(n - 1, int(prog * n))
    lh = int(f.size * 1.20)
    yc = (LY_TOP + LY_BOT) / 2 - lh * (len(lines) - 1) / 2
    k, a = 0, fade(t, t0 - 0.35, t1 + 0.18, 0.35)
    geo = []
    for li, line in enumerate(lines):
        ws = line.split()
        widths = [text_w(d, w_, f, spacing=1, stroke=sk) for w_ in ws]
        gap = 15
        x = W / 2 - (sum(widths) + gap * (len(ws) - 1)) / 2
        for j2, w_ in enumerate(ws):
            k += 1
            yy = yc + li * lh + math.sin(2 * math.pi * (WAVE_HZ * t + k * 0.28)) * WAVE_AMP
            geo.append((x, yy, widths[j2], w_, k - 1, li))
            x += widths[j2] + gap
    if V2 and geo:
        # 1) coup de surligneur sous le mot en cours de chant
        g = next((g for g in geo if g[4] == act), geo[0])
        hh = f.size
        # le surligneur depasse sa boite (pad + biais) : on le borne a la limite visage + 12 px
        ytop = max(FACE_LIMIT + 12, g[1] - hh * 0.60)
        ST.highlight(d, (g[0] - g[2] / 2, ytop, g[0] + g[2] / 2, g[1] + hh * 0.26),
                     col=(255, 211, 90), pad=8, alpha=112, seed=int(t * 10) % 9973)
        # 2) ligne soulignee au feutre creme, legerement ondulee
        last = [g for g in geo if g[5] == geo[-1][5]]
        x0 = min(g[0] - g[2] / 2 for g in last)
        x1 = max(g[0] + g[2] / 2 for g in last)
        yu = max(g[1] for g in last) + f.size * 0.52
        ST.squiggle(d, x0, min(yu, LY_BOT - 6), x1, col=GOLD, width=6, wob=5.0,
                    seed=int(1000 * t0) % 9973)
    for x, yy, wd, w_, idx, li in geo:
        on, done = idx == act, idx < act
        col = GOLD if on else (DIM if done else CREAM)
        al = int((255 if on else (206 if done else 244)) * a)
        att = prog * n - idx
        sw = sk + (2 if (on and att < 0.45) else 0)
        if V2 and on:
            al = 255
        d.text((x, yy), w_, font=f, fill=col + (al,), anchor="lm", stroke_width=sw,
               stroke_fill=(0, 0, 0, int(205 * a)))
    aabb = lay.getbbox()
    return lay, aabb


DECO_TOP, DECO_BOT = 1140, 1574          # zone dessinee par le moteur : sous le visage, dans les clous v5.7


DECO_TOP, DECO_BOT = 1140, 1574          # zone dessinee par le moteur : sous le visage, dans les clous v5.7
_DECO = {}                               # les autocollants ne dependent pas de t -> caches par plan


def _deco_static(cur):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x0, x1 = W / 2 - LY_SAFE_W / 2 - 24, W / 2 + LY_SAFE_W / 2 + 24
    ST.tape(d, x0 + 26, LY_TOP + 10, 126, 28, ang=-9)      # scotch : sous la limite visage, jamais dessus
    ST.tape(d, x1 - 26, LY_TOP + 10, 126, 28, ang=7)
    ST.dashed(d, (x0 + 6, LY_TOP + 4, min(x1, 906), LY_BOT - 2), col=(243, 236, 217), width=3,
              dash=13, gap=10, rad=10, alpha=118)
    ST.star(d, x0 - 4, DECO_TOP + 74, 30, points=9, rot=14, alpha=225)
    if cur:
        lab = tag_for(cur[2])
        if lab:
            f_t, _ = font(31, 900)
            ST.tag(d, x0 + 110, 1382, lab, f_t, rot=-5, pad=(16, 8),
                   fg=((255, 243, 214, 255) if lab == "ADLIB" else GOLD))
    return lay


def deco_v2(t, cur):
    """scotch, cadre pointille, etoile, etiquette de section + etincelles.
    Tout en y 1140 -> 1574 et x <= 910 : le controle parois du visage garde toute sa valeur."""
    lay = _deco_static(cur).copy()
    zones = [(W / 2 - LY_SAFE_W / 2 - 24, 1352, min(W / 2 + LY_SAFE_W / 2 + 24, 900), 1520)]
    sp, off = ST.sparkles(None, t, zones, rng_seed=int(cur[0] * 7) if cur else 7, n=4)
    lay.alpha_composite(sp, dest=off)
    return lay


_INTRO_DECO = None


def _intro_static():
    global _INTRO_DECO
    if _INTRO_DECO is None:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        ST.dashed(d, (W / 2 - 360, 1030, W / 2 + 360, 1130), col=(255, 211, 90), width=4,
                  dash=15, gap=9, rad=12, alpha=150)
        ST.arrow(d, (198, 1432), (262, 1236), col=(255, 138, 66), width=8, curve=-46, head=24)
        ST.icon(d, 366, 1400, "play", s=26, col=(255, 211, 90), width=5, alpha=225)
        ST.star(d, 150, 1148, 38, points=9, rot=10, alpha=225)
        ST.star(d, 884, 1306, 26, points=8, rot=-14, alpha=205)
        _INTRO_DECO = lay
    return _INTRO_DECO


def intro_v2(t):
    """rend l'appel a l'action tactile : cadre sur les pilules, fleche vers la cloche, etoiles, etincelles."""
    lay = _intro_static().copy()
    sp, off = ST.sparkles(None, t, [(120, 1140, 900, 1420)], rng_seed=3, n=5)
    lay.alpha_composite(sp, dest=off)
    return lay


def bell_block(dt):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bell = INTRO.bell_layer(dt)
    bw, bh = bell.size
    lay.alpha_composite(bell, (int(W / 2 - bw / 2), 612))
    d = ImageDraw.Draw(lay)
    f_a, s_a = font(64, 900)
    m = grad_mask(d, (W, H), W / 2, 1002, "ABONNE-TOI", f_a, spacing=7, stroke=s_a)
    xs = np.linspace(0, 1, W, dtype=np.float32)[None, :, None]
    g1, g2 = np.array([255, 255, 255], np.float32), np.array([168, 226, 255], np.float32)
    gt = Image.fromarray(np.repeat((g1 + (g2 - g1) * xs).astype(np.uint8), H, axis=0), "RGB").convert("RGBA")
    gt.putalpha(m)
    glow = Image.new("RGBA", (W, H), (60, 200, 255, 0))
    glow.putalpha(m.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.5)))
    lay = Image.alpha_composite(Image.alpha_composite(lay, glow), gt)
    labels = ["PARTAGE", "COMMENTE", "ENREGISTRE"]
    PH, GAP, MAXW = 78, 18, 730
    fp, sk = font(38, 800)
    sp = int(PH * 0.10)
    dd = ImageDraw.Draw(lay)
    ws = []
    for fsize in (38, 34, 31, 28, 25):
        fp, sk = font(fsize, 800)
        ws = [int(text_w(dd, s, fp, spacing=sp, stroke=sk)) + 44 for s in labels]
        if sum(ws) + GAP * (len(ws) - 1) <= MAXW:
            break
    x = int(W / 2 - (sum(ws) + GAP * (len(ws) - 1)) / 2)
    for txt, wd in zip(labels, ws):
        lay.alpha_composite(INTRO.pill((wd, PH), txt, fp, dt, spacing=sp), (x, 1044))
        x += wd + GAP
    return lay


def badge_layer(alpha=1.0):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((W / 2 - 125, BADGE_Y - 8, W / 2 + 125, BADGE_Y + 44), radius=26,
                        fill=(8, 10, 14, 118))
    f_i, s_i = font(34, 800)
    draw_spaced(d, W / 2, BADGE_Y + 22, "Dsky", f_i, (255, 255, 255, int(255 * BADGE_OP * alpha)),
                spacing=2, stroke=s_i, stroke_fill=(0, 0, 0, 120))
    return lay


_END = None


def endcard(dt):
    global _END
    if _END is None:
        im = Image.open(bg_for(30)).convert("RGB").resize((W, H), Image.LANCZOS)
        g = np.asarray(im.convert("L")).astype(np.float32)
        _END = np.asarray(Image.composite(Image.fromarray(np.clip(g * 0.30, 0, 255).astype(np.uint8)), im,
                                          Image.new("L", (W, H), 255)), np.uint8)
    base = Image.fromarray(_END, "RGB").convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    y = 600
    for txt, sz, wt, col in (("Merci d'avoir regardé", 74, 900, (255, 255, 255)),
                             ("Tu veux un son ou des lyrics", 48, 700, CREAM),
                             ("à réaliser pour toi ?", 48, 700, CREAM)):
        f, sk = font(sz, wt)
        if text_w(d, txt, f, spacing=2, stroke=sk) > 960:
            f, sk = font(max(30, int(sz * 960 / text_w(d, txt, f, spacing=2, stroke=sk))), wt)
        draw_spaced(d, W / 2, y, txt, f, col + (255,), spacing=2, stroke=sk, stroke_fill=(0, 0, 0, 215))
        y += int(sz * 1.62)
    f, sk = font(44, 700)
    draw_spaced(d, W / 2, y + 34, "Commente le code", f, (206, 226, 244, 255), spacing=1, stroke=sk,
                stroke_fill=(0, 0, 0, 200))
    fc, sc = font(190, 900)
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).text((W / 2, y + 210), CODE, font=fc, fill=255, anchor="mm", stroke_width=sc + 2,
                           stroke_fill=255)
    xs = np.linspace(0, 1, W, dtype=np.float32)[None, :, None]
    g1, g2 = np.array(GOLD, np.float32), np.array([255, 255, 255], np.float32)
    gt = Image.fromarray(np.repeat((g1 + (g2 - g1) * xs).astype(np.uint8), H, axis=0), "RGB").convert("RGBA")
    gt.putalpha(m)
    glow = Image.new("RGBA", (W, H), (255, 200, 90, 0))
    glow.putalpha(m.filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v * 0.65)))
    lay = Image.alpha_composite(Image.alpha_composite(lay, glow), gt)
    if V2:
        cb = m.getbbox()
        if cb:
            ST.dashed(ImageDraw.Draw(lay), cb, col=(255, 243, 214), width=4, dash=15, gap=10,
                      rad=22, alpha=165)
            d3 = ImageDraw.Draw(lay)
            ST.tape(d3, cb[0] - 34, cb[1] - 16, 118, 30, ang=-14)
            ST.tape(d3, cb[2] + 32, cb[3] + 16, 118, 30, ang=10)
            ST.star(d3, cb[0] - 54, (cb[1] + cb[3]) / 2 + 96, 34, points=9, rot=12, alpha=230)
            ST.star(d3, cb[2] + 52, (cb[1] + cb[3]) / 2 - 92, 28, points=8, rot=-9, alpha=215)
            sp, off = ST.sparkles(None, 1.0 + dt, [(cb[0] - 128, cb[1] - 60, cb[0] - 40, cb[3] + 60),
                                                   (cb[2] + 40, cb[1] - 60, cb[2] + 128, cb[3] + 60)],
                                  rng_seed=11, n=4)
            lay.alpha_composite(sp, dest=off)
    f2, s2 = font(36, 600)
    d2 = ImageDraw.Draw(lay)
    draw_spaced(d2, W / 2, y + 350, "4 chiffres · Gbètché vivi · regarde jusqu'à la fin", f2,
                (236, 236, 236, 255), spacing=1, stroke=s2, stroke_fill=(0, 0, 0, 190))
    fin = Image.alpha_composite(base, lay).convert("RGB")
    f = min(1.0, dt / 0.5) * (1.0 if dt < T_TAIL - 0.6 else max(0.0, (T_TAIL - dt) / 0.6))
    if f < 1.0:
        fin = Image.composite(SC, fin, Image.new("L", (W, H), int(255 * (1 - f))))
    return fin


def frame(t, want_diag=False):
    if t < T_INTRO:
        img = INTRO.frame(t)
        if V2:
            lay = intro_v2(t)
            img = Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")
        return (img, None) if want_diag else img
    if t >= T_SONG_END:
        img = endcard(t - T_SONG_END)
        return (img, None) if want_diag else img
    sh = next((s for s in SH if s[1] <= t < s[2]), SH[-1])
    base = Image.fromarray(base_of(sh[3]), "RGB")
    inbell = next((bw for bw in BELL_WINDOWS if bw[0] <= t < bw[1]), None)
    cur = next((v for v in VS if v[0] <= t < v[1]), None)
    diag = None
    lay = badge_layer(1.0 if not cur else fade(t, cur[0] - 0.4, cur[1] + 0.25, 0.4))
    comp = Image.alpha_composite(base.convert("RGBA"), lay)
    if inbell:
        a0, b0 = inbell
        rep = (t - a0) % 4.0
        vis = fade(t, a0, b0, 0.35) * (1.0 if rep < 3.5 else max(0.0, (3.75 - rep) / 0.25))
        if vis > 0.02:
            blk = bell_block(t - a0)
            blk.putalpha(blk.getchannel("A").point(lambda v: int(v * vis)))
            comp = Image.alpha_composite(comp, blk)
    elif cur:
        t0, t1, txt = cur
        lines, f, sk = fit(txt)
        lyr, aabb = lyric_layer(t, t0, t1, lines, f, sk)
        comp = Image.alpha_composite(comp, lyr)
        if V2:
            comp = Image.alpha_composite(comp, deco_v2(t, cur))
        if want_diag and aabb:
            diag = aabb
    return (comp.convert("RGB"), diag) if want_diag else comp.convert("RGB")


def ffexe():
    return subprocess.run([sys.executable, "-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"],
                          capture_output=True, text=True).stdout.strip().splitlines()[-1]


def master():
    ff = ffexe()
    src = glob.glob(os.path.join(REPO, "Gb*tch* vivi.mp3"))[0]
    wav, mp3 = os.path.join(OUT, "master-48k.wav"), os.path.join(OUT, "Gbetché vivi - master.mp3")
    p1 = subprocess.run([ff, "-hide_banner", "-nostats", "-i", src, "-af",
                         "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                        capture_output=True, text=True)
    txt = (p1.stderr or "") + (p1.stdout or "")
    i, j = txt.rfind("{"), txt.rfind("}")
    meas1 = {}
    if i >= 0 and j > i:
        try:
            meas1 = json.loads(txt[i:j + 1])
        except Exception:
            meas1 = {}
    d = meas1
    af = "loudnorm=I=-14:TP=-1.5:LRA=11"
    if d:
        af += (":linear=true:measured_I=%(input_i)s:measured_TP=%(input_tp)s:measured_LRA=%(input_lra)s"
               ":measured_thresh=%(input_thresh)s:offset=%(target_offset)s" % d)
    print("  mesure passe 1:", {k: meas1.get(k) for k in ("input_i", "input_tp", "input_lra", "target_tp")} if meas1 else "JSON non trouvé -> mode dynamique")
    subprocess.run([ff, "-v", "error", "-y", "-i", src, "-af", af, "-ar", "48000", wav], check=True)
    # plafond a -2,05 dBFS avant transcodage: l'encodeur MP3/AAC depasse toujours d'environ 0,5 dB
    subprocess.run([ff, "-v", "error", "-y", "-i", wav,
                     "-af", "alimiter=limit=0.79:level=false:attack=5:release=90",
                     "-b:a", "320k", mp3], check=True)
    cov = os.path.join(HERE, "covers", "gbetché-vivi-1080.jpg")
    if os.path.exists(cov):
        try:
            import make_cover
            tmp = os.path.join(OUT, "_master_tagged.mp3")
            rc, err = make_cover.embed(cov, mp3, tmp)
            if rc == 0:
                os.replace(tmp, mp3)
                print("  pochette APIC integree au master")
            else:
                print("  APIC:", err.strip()[-160:])
        except Exception as e:
            print("  APIC:", e)
    return wav, mp3, d


def audit():
    """Controle : rien d'autre que le badge au-dessus de y = FACE_LIMIT sur les frames paroles."""
    viol, checked, mins = 0, 0, 10 ** 9
    for s in SH:
        t = s[1] + min(2.0, (s[2] - s[1]) / 2)
        if t >= T_SONG_END or any(b[0] <= t < b[1] for b in BELL_WINDOWS):
            continue
        cur = next((v for v in VS if v[0] <= t < v[1]), None)
        if not cur:
            continue
        base = np.asarray(Image.fromarray(base_of(s[3]), "RGB"), np.int16)
        fr, aabb = frame(t, want_diag=True)
        fin = np.asarray(fr, np.int16)
        d = np.abs(fin - base).max(axis=2)
        mask = np.ones((H, W), bool)
        mask[BADGE_BAND[0]:BADGE_BAND[1], :] = False
        mask[FACE_LIMIT:, :] = False
        over = int((d[mask] > 6).sum())
        viol += 1 if over else 0
        checked += 1
        if aabb:
            mins = min(mins, aabb[1])
        print(f"  {s[0]:>2} t={t:6.2f} encre>=y{aabb[1] if aabb else '-'}pixels hors bande badge={over}")
    print(f"AUDIT parois du visage : {checked} frames testees, {viol} avec encre au-dessus de y{FACE_LIMIT} "
          f"| plus haut encre de parole = y{mins if mins < 10**9 else '-'}")
    return viol, checked


def main():
    if "--v2" in sys.argv:
        print("MODE v2 : texte grave dans les images + autocollants/icones dessines")
    wav = os.path.join(OUT, "master-48k.wav")
    meas = {}
    if "--no-master" not in sys.argv and (not os.path.exists(wav) or "--master" in sys.argv):
        wav, mp3, meas = master()
        print("master:", mp3, "|", {k: v for k, v in meas.items() if k.startswith(("input_i", "input_tp", "target_i", "target_tp"))})
    if "--audit" in sys.argv:
        audit()
        return 0
    ff = ffexe()
    vid = os.path.join(OUT, "Gbetché vivi - 916 v2.mp4" if V2 else "Gbetché vivi - 916.mp4")
    cmd = [ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", wav, "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-af", f"alimiter=limit=0.79:level=false:attack=5:release=90,apad=whole_dur={T_TOTAL:.3f}", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
           "-ac", "2", "-t", f"{T_TOTAL:.3f}", "-movflags", "+faststart", vid]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for i in range(N_FRAMES):
            p.stdin.write(frame(i / FPS).tobytes())
            if i % 600 == 0:
                print(f"frame {i}/{N_FRAMES}", flush=True)
    except BrokenPipeError:
        pass
    p.stdin.close()
    err = p.stderr.read().decode(errors="ignore")
    rc = p.wait()
    print(f"frames={N_FRAMES} duree={N_FRAMES/FPS:.3f}s rc={rc}")
    if rc:
        print(err[-1500:])
        return 1
    print("ok ->", vid)
    return 0


if __name__ == "__main__":
    sys.exit(main())
