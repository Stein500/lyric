#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOTEUR DE RENDU LYRICS — « Dès le début » (Daïsky)
Produit la maquette de validation (défaut : 14,5 s) :
  · texte mot à mot hybride (mot actif or/crème, mots passés atténués, vague d'eau)
  · badge Dsky + drapeau Bénin en fondu 0,4 s à chaque vers, opacité ≤ 75 %
  · CLOCHETTES CTA (s'abonner + surtout PARTAGER) dans les fenêtres sans parole > 5 s
  · bandeau Bénin 54 px en pied de cadre
  · Ken Burns 1,02→1,08 + pan sinusoïdal + « respiration » (vague d'eau) sur les fonds
Sortie : apercu/MAQUETTE_Des_le_debut.mp4 (+ planche de contrôle)

Usage :
  python moteur_maquette.py                 # maquette 14,5 s par défaut
  python moteur_maquette.py --debut 106 --duree 14.5 --sortie apercu/x.mp4
"""
import argparse, io, math, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------ chemins
HERE = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(PROD, "..", ".."))
FONDS = os.path.join(PROD, "fonds")
FONT_LYR = os.path.join(ROOT, "assets", "fonts", "BarlowCondensed-Bold.ttf")
FONT_UI = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
AUDIO = os.path.join(ROOT, "Dès le début.mp3")
PAROLES = os.path.join(ROOT, "Dès le début- Jésus-Christ sauveur.txt")
FFMPEG = os.environ.get("FFMPEG", "/tmp/lyric-venv/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2")

# ------------------------------------------------------------------ constantes visuelles
W, H = 1080, 1920
FPS = 30
CANVAS = 1.10                      # marge de recadrage Ken Burns
MAXW = 720                         # largeur sûre des paroles (x 180 → 900)
CENTRE_Y = H // 2                  # 960
GOLD = (255, 196, 78)
CREAM = (248, 243, 231)
BENIN = ((0, 135, 81), (252, 209, 22), (232, 17, 45))

# scènes : (slot, début_song_s, fin_song_s) — cf. PLAN_20_SCENES.md
SCENES = [("s10", 103.65, 116.00), ("s11", 116.00, 126.61)]
# fenêtres CTA (début, fin) en temps chanson — extraites de l'analyse (>5 s sans parole)
CTA_WINDOWS = [(106.90, 116.24)]

ap = argparse.ArgumentParser()
ap.add_argument("--debut", type=float, default=106.0, help="début dans la chanson (s)")
ap.add_argument("--duree", type=float, default=14.5)
ap.add_argument("--sortie", default=os.path.join(PROD, "apercu", "MAQUETTE_Des_le_debut.mp4"))
args = ap.parse_args()
T0, DUR = args.debut, args.duree
N = int(round(DUR * FPS))

# ------------------------------------------------------------------ outils
def font(size, ui=False):
    return ImageFont.truetype(FONT_UI if ui else FONT_LYR, size)

def sprite(text, f, fill, stroke=(0, 0, 0, 190), stroke_w=4):
    """Rend un mot en sprite RGBA numpy (rgb float + alpha float)."""
    box = f.getbbox(text, stroke_width=stroke_w)
    w, h = box[2] - box[0], box[3] - box[1]
    im = Image.new("RGBA", (w + 4, h + 4), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((2 - box[0], 2 - box[1]), text, font=f, fill=fill + (255,),
                            stroke_width=stroke_w, stroke_fill=stroke)
    a = np.asarray(im, dtype=np.float32)
    return a[:, :, :3], a[:, :, 3] / 255.0

def read_verses():
    out = []
    for line in open(PAROLES, encoding="utf-8").read().splitlines():
        m = re.match(r"\[(\d+):(\d+\.\d+)\]\u200e?(.*)", line)
        if m:
            t = int(m.group(1)) * 60 + float(m.group(2))
            txt = m.group(3).replace("\u200e", "").strip()
            if txt:
                out.append((t, txt))
    return out

VERSES = read_verses()
DUREE_CHANSON = 199.99

def display_duration(words):
    return min(4.5, max(2.2, 1.15 + 0.33 * words))

def verse_window(idx):
    """Fenêtre réelle d'un vers : durée bornée par le départ du vers suivant (jamais de chevauchement)."""
    t, txt = VERSES[idx]
    nxt = VERSES[idx + 1][0] if idx + 1 < len(VERSES) else DUREE_CHANSON
    dur = display_duration(len(txt.split()))
    dur = max(1.2, min(dur, nxt - t - 0.12))
    return t, dur

# ------------------------------------------------------------------ mise en page des paroles
def layout(txt):
    """Choisit taille + retour à la ligne (≤ MAXW) et renvoie les lignes."""
    words = txt.split()
    n = len(words)
    for size in range(78, 45, -2):
        f = font(size)
        # découpe équilibrée en 1 → 3 lignes
        best = None
        for nlines in (1, 2, 3):
            if n < nlines:
                continue
            target = len(txt) / nlines
            lines, cur, acc = [], [], 0
            for wd in words:
                add = len(wd) + (1 if cur else 0)
                if cur and acc + add > target * 1.15 and len(lines) < nlines - 1:
                    lines.append(" ".join(cur)); cur, acc = [wd], len(wd)
                else:
                    cur.append(wd); acc += add
            if cur:
                lines.append(" ".join(cur))
            widest = max(f.getbbox(l, stroke_width=4)[2] - f.getbbox(l, stroke_width=4)[0] for l in lines)
            lh = int(size * 1.12)
            if widest <= MAXW and len(lines) <= 3:
                cand = (size, lines, widest, lh)
                if best is None or len(lines) < len(best[1]):
                    best = cand
        if best:
            return best
    return (46, [" ".join(words)], MAXW, 52)

def verse_sprites():
    """Prépare pour chaque vers : lignes, sprites (actif/passé) et positions."""
    prep = []
    for idx, (t, txt) in enumerate(VERSES):
        size, lines, widest, lh = layout(txt)
        f = font(size)
        total_h = lh * len(lines)
        y0 = CENTRE_Y - total_h // 2
        items = []       # (sprite_actif, sprite_passe, x, y, appear_s, index)
        for li, line in enumerate(lines):
            words = line.split()
            widths = [f.getbbox(wd, stroke_width=4)[2] - f.getbbox(wd, stroke_width=4)[0] for wd in words]
            space = f.getbbox(" ")[2] - f.getbbox(" ")[0]
            line_w = sum(widths) + space * (len(words) - 1)
            x = (W - line_w) // 2
            for wi, wd in enumerate(words):
                act = sprite(wd, f, GOLD, stroke=(0, 0, 0, 215), stroke_w=6)
                past = sprite(wd, f, CREAM, stroke=(0, 0, 0, 205), stroke_w=6)
                items.append([act, past, x, y0 + li * lh, None, wi, len(words)])
                x += widths[wi] + space
        t0, dur = verse_window(idx)
        prep.append(dict(t=t0, src_t=t, txt=txt, dur=dur, size=size, lines=lines, items=items,
                         height=total_h, top=y0, bottom=y0 + total_h, widest=widest))
    return prep

VERSES_PREP = verse_sprites()

# ------------------------------------------------------------------ décor : drapeau, badge, cloche
def benin_band(h=54):
    """Bandeau Bénin pleine largeur : vert tiers gauche, jaune en haut à droite, rouge en bas."""
    band = np.zeros((h, W, 3), dtype=np.float32)
    third = W // 3
    band[:, :third] = BENIN[0]
    band[: h // 2, third:] = BENIN[1]
    band[h // 2:, third:] = BENIN[2]
    return band

BAND = benin_band()

def make_scrim():
    from PIL import ImageFilter
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([60, CENTRE_Y - 300, W - 60, CENTRE_Y + 300], radius=120, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(70))
    a = np.asarray(m, dtype=np.float32) / 255.0 * 0.68
    return a

SCRIM = make_scrim()

def flag_picto(h=34):
    """Drapeau béninois vectoriel compact (pour le badge)."""
    w = int(h * 1.5)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    third = w // 3
    d.rectangle([0, 0, third, h], fill=BENIN[0] + (255,))
    d.rectangle([third, 0, w, h // 2], fill=BENIN[1] + (255,))
    d.rectangle([third, h // 2, w, h], fill=BENIN[2] + (255,))
    d.rectangle([0, 0, w - 1, h - 1], outline=(10, 10, 10, 160), width=2)
    a = np.asarray(im, dtype=np.float32)
    return a[:, :, :3], a[:, :, 3] / 255.0

def badge_sprite():
    """Badge « Dsky » + drapeau béninois, police UI nette."""
    f = font(40, ui=True)
    txt = "Dsky"
    box = f.getbbox(txt)
    fw, fh = flag_picto(34)[0].shape[1], 34
    pad = 16
    w = (box[2] - box[0]) + 22 + fw + pad * 2
    h = 72
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=34, fill=(8, 12, 22, 205),
                        outline=(255, 196, 78, 210), width=2)
    d.text((pad - box[0], (h - (box[3] - box[1])) // 2 - box[1]), txt, font=f, fill=(255, 240, 205, 255))
    frgb, fa = flag_picto(34)
    x0 = pad - box[0] + (box[2] - box[0]) + 22
    y0 = (h - 34) // 2
    reg = im.crop((x0, y0, x0 + frgb.shape[1], y0 + 34))
    comp = np.asarray(reg, dtype=np.float32)
    a3 = fa[:, :, None]
    comp = comp[:, :, :3] * (1 - a3) + frgb * a3
    im.paste(Image.fromarray(comp.astype(np.uint8)), (x0, y0))
    a = np.asarray(im, dtype=np.float32)
    return a[:, :, :3], a[:, :, 3] / 255.0

BADGE = badge_sprite()

def bell_sprite(size=340):
    S = size * 3
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = S / 2
    y_top, y_lip = S * 0.20, S * 0.76
    half = S * 0.33
    prof = []
    NN = 80
    for k in range(NN + 1):
        s = k / NN
        w = half * (1 - s ** 3.0) ** 0.5 * (1 + 0.10 * (1 - s) ** 2)
        prof.append((cx - w, y_lip - s * (y_lip - y_top)))
    for k in range(NN + 1):
        s = 1 - k / NN
        w = half * (1 - s ** 3.0) ** 0.5 * (1 + 0.10 * (1 - s) ** 2)
        prof.append((cx + w, y_lip - s * (y_lip - y_top)))
    d.polygon(prof, fill=GOLD + (255,))
    d.line(prof + [prof[0]], fill=(255, 236, 168, 255), width=int(S * 0.012), joint="curve")
    d.rounded_rectangle([cx - half * 1.16, y_lip - S * 0.045, cx + half * 1.16, y_lip + S * 0.035],
                        radius=S * 0.028, fill=GOLD + (255,), outline=(255, 236, 168, 255), width=int(S * 0.01))
    d.arc([cx - S * 0.085, y_top - S * 0.10, cx + S * 0.085, y_top + S * 0.055],
          start=180, end=360, fill=(255, 236, 168, 255), width=int(S * 0.032))
    d.ellipse([cx - S * 0.070, y_lip + S * 0.020, cx + S * 0.070, y_lip + S * 0.150],
              fill=(255, 236, 168, 255), outline=(158, 104, 18, 255), width=int(S * 0.008))
    d.ellipse([cx - half * 0.72, y_top + S * 0.05, cx - half * 0.40, y_top + S * 0.22],
              fill=(255, 255, 255, 95))
    from PIL import ImageFilter
    halo = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    g = im.filter(ImageFilter.GaussianBlur(S * 0.045))
    halo.paste(g, (0, 0), g)
    im = Image.alpha_composite(halo, im)
    a = np.asarray(im.resize((size, size), Image.LANCZOS), dtype=np.float32)
    return a[:, :, :3], a[:, :, 3] / 255.0

BELL = bell_sprite(340)
SHARE_FONT = font(42, ui=True)

def star(d, cx, cy, r, col):
    d.polygon([(cx, cy - r), (cx + r * .28, cy - r * .28), (cx + r, cy), (cx + r * .28, cy + r * .28),
               (cx, cy + r), (cx - r * .28, cy + r * .28), (cx - r, cy), (cx - r * .28, cy - r * .28)], fill=col)

def make_cta_layer(t, elapsed):
    """Calque CTA clochettes (entrée 0,35 s / sortie 0,35 s)."""
    IN = 0.35
    seq = 3.0
    fade = min(1.0, elapsed / IN)
    if fade <= 0:
        return None
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    cx = W // 2
    # ondes de sonnerie
    for k in range(2):
        u = ((t / 0.9) + k * 0.5) % 1.0
        rr = 150 + 250 * u
        d.ellipse([cx - rr, 840 - rr, cx + rr, 840 + rr],
                  outline=(255, 196, 78, int(150 * (1 - u) ** 1.6 * fade)), width=5)
    # cloche animée
    swing = 13 * math.sin(2 * math.pi * t / 1.2) * math.exp(-0.22 * ((t % 1.2) / 1.2))
    pulse = 1.0 + 0.05 * math.sin(2 * math.pi * t / 0.8)
    sz = int(340 * pulse)
    b = Image.fromarray(BELL[0].astype(np.uint8)).convert("RGBA")
    b.putalpha(Image.fromarray((np.clip(BELL[1] * fade, 0, 1) * 255).astype(np.uint8)))
    b = b.resize((sz, sz), Image.LANCZOS).rotate(swing, resample=Image.BICUBIC, center=(sz / 2, sz * 0.10))
    lay.alpha_composite(b, (cx - sz // 2, 670))
    # étincelles
    for sx, sy, off in [(cx - 190, 740, 0.0), (cx + 180, 770, 0.35), (cx + 105, 690, 0.7)]:
        u = ((t / 0.7) + off) % 1.0
        al = int(235 * (1 - abs(0.5 - u) * 2) ** 0.8 * fade)
        if al > 0:
            star(d, sx, sy, 8 + 7 * math.sin(math.pi * u), (255, 240, 190, al))
    # flèche clignotante
    u = (t / 1.0) % 1.0
    if u < 0.72:
        al = int(255 * (1 - u / 0.72) * fade)
        yy = 630 + u * 26
        d.polygon([(cx, yy + 30), (cx - 22, yy), (cx + 22, yy)], fill=(255, 255, 255, al))
    # textes
    d.rounded_rectangle([cx - 235, 1052, cx + 235, 1120], radius=26,
                        fill=(8, 12, 24, int(130 * fade)))
    d.text((cx, 1090), "ABONNE-TOI", font=font(52, ui=True), fill=(255, 255, 255, int(255 * fade)),
           anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0, int(190 * fade)))
    box = [cx - 300, 1140, cx + 300, 1210]
    d.rounded_rectangle(box, radius=35, fill=(10, 20, 34, int(200 * fade)),
                        outline=(86, 226, 255, int((110 + 90 * math.sin(2 * math.pi * t / 0.9)) * fade)), width=4)
    # icône partage
    r = 15
    p = [(cx - 190, 1175), (cx - 105, 1152), (cx - 105, 1198)]
    for a_, b_ in [(p[0], p[1]), (p[0], p[2])]:
        d.line([a_, b_], fill=(255, 255, 255, int(255 * fade)), width=8)
    for x, y in p:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, int(255 * fade)))
    d.polygon([(cx - 105, 1136), (cx - 63, 1152), (cx - 105, 1168)], fill=(255, 255, 255, int(255 * fade)))
    d.text((cx + 60, 1175), "PARTAGE", font=SHARE_FONT, fill=(255, 255, 255, int(255 * fade)),
           anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0, int(190 * fade)))
    d.rounded_rectangle([cx - 300, 1240, cx + 300, 1292], radius=22,
                        fill=(8, 12, 24, int(120 * fade)))
    d.text((cx, 1265), "Clique sur la cloche — puis PARTAGE", font=font(30, ui=True),
           fill=(255, 232, 160, int(240 * fade)), anchor="mm", stroke_width=4,
           stroke_fill=(0, 0, 0, int(170 * fade)))
    a = np.asarray(lay, dtype=np.float32)
    return a[:, :, :3], a[:, :, 3] / 255.0

# ------------------------------------------------------------------ fonds
def load_canvas(slot):
    p = os.path.join(FONDS, "portrait", slot + ".jpg")
    if not os.path.exists(p):
        cand = [x for x in os.listdir(os.path.join(FONDS, "portrait")) if x.startswith(slot)]
        p = os.path.join(FONDS, "portrait", cand[0])
    im = Image.open(p).convert("RGB")
    cw, ch = int(W * CANVAS), int(H * CANVAS)
    return im.resize((cw, ch), Image.LANCZOS)

CANVAS_IMG = {slot: load_canvas(slot) for slot, _, _ in SCENES}
CANVAS_ARR = {k: np.asarray(v, dtype=np.uint8) for k, v in CANVAS_IMG.items()}

def scene_for(song_t):
    for k, (slot, a, b) in enumerate(SCENES):
        if a <= song_t < b:
            return k, slot, (song_t - a) / max(1e-6, (b - a)), (b - a)
    k = len(SCENES) - 1
    return k, SCENES[-1][0], 1.0, 1.0

def render_bg(song_t, t):
    """Ken Burns + pan + respiration (vague d'eau) sur le fond."""
    k, slot, u, sdur = scene_for(song_t)
    arr = CANVAS_ARR[slot]
    ch, cw = arr.shape[:2]
    zoom = 1.02 + 0.06 * (u if k % 2 == 0 else (1 - u))
    cwid = int(W * CANVAS / zoom)
    chei = int(H * CANVAS / zoom)
    amp_x = (cw - cwid) / 2 * 0.65
    amp_y = (ch - chei) / 2 * 0.65
    cx = cw / 2 + amp_x * math.sin(2 * math.pi * t / 11.0 + k * 0.9)
    cy = ch / 2 + amp_y * math.sin(2 * math.pi * t / 13.0 + k * 0.6)
    x0 = int(max(0, min(cw - cwid, cx - cwid / 2)))
    y0 = int(max(0, min(ch - chei, cy - chei / 2)))
    crop = arr[y0:y0 + chei, x0:x0 + cwid]
    img = Image.fromarray(crop).resize((W, H), Image.LANCZOS)
    fr = np.asarray(img, dtype=np.float32)
    # respiration : déplacement vertical sinusoïdal par colonne
    xs = np.arange(W, dtype=np.float32)
    dy = 3.0 * np.sin(2 * math.pi * xs / 210.0 + 2 * math.pi * 0.9 * t)
    rows = np.arange(H, dtype=np.float32)[:, None]
    idx = np.clip((rows + dy[None, :]).round().astype(np.int32), 0, H - 1)
    fr = np.take_along_axis(fr, idx[:, :, None], axis=0)
    return fr

# ------------------------------------------------------------------ texte
def compose_verse(fr, vp, song_t):
    """Texte du vers : apparition mot à mot, mot actif or, passé crème, vague d'eau."""
    t = song_t
    start = vp["t"]
    dur = vp["dur"]
    if not (start - 0.15 <= t <= start + dur + 0.45):
        return fr
    # fenêtre d'apparition
    nw = len(vp["items"])
    appear_span = 0.55 * dur
    band_h = vp["bottom"] - vp["top"] + 40
    ytop = vp["top"] - 20
    band = np.zeros((band_h, W, 3), dtype=np.float32)
    alpha = np.zeros((band_h, W), dtype=np.float32)
    fade_out = 1.0
    if t > start + dur:
        fade_out = max(0.0, 1.0 - (t - (start + dur)) / 0.45)
    for i, item in enumerate(vp["items"]):
        act, past, x, y, _, wi, _ = item
        t_app = start + 0.10 + (i / max(1, nw)) * appear_span
        if t < t_app:
            continue
        t_next = start + 0.10 + ((i + 1) / max(1, nw)) * appear_span
        is_active = t < t_next + 0.18
        spr, cov = act if is_active else past
        a_word = min(1.0, (t - t_app) / 0.22) * fade_out
        if a_word <= 0:
            continue
        h, w = cov.shape
        yy = y - 20 - vp["top"] + 20 + (ytop - ytop)   # position relative à la bande
        yy = y - ytop
        if yy < 0 or yy + h > band_h or x < 0 or x + w > W:
            continue
        a3 = (cov * a_word)[:, :, None]
        reg = band[yy:yy + h, x:x + w]
        band[yy:yy + h, x:x + w] = reg * (1 - a3) + spr * a3
        aa = alpha[yy:yy + h, x:x + w]
        alpha[yy:yy + h, x:x + w] = aa * (1 - a3[:, :, 0]) + a3[:, :, 0]
    if alpha.max() <= 0:
        return fr
    # scrim central doux derrière le texte (jamais sur le visage : bande du milieu)
    vis = float(np.clip(alpha.mean() * 26.0, 0.0, 1.0)) * 0.85
    sc = (SCRIM * vis)[:, :, None]
    fr = fr * (1 - sc) + (fr * 0.42 + 10.0) * sc
    # vague d'eau continue des glyphes présents (amp. 4,5 px, 0,9 Hz)
    xs = np.arange(W, dtype=np.float32)[None, :]
    dy = (4.5 * np.sin(2 * math.pi * xs / 230.0 + 2 * math.pi * 0.9 * t)).round().astype(np.int32)[0]
    rr = np.arange(band_h, dtype=np.int32)[:, None]
    idx = np.clip(rr + dy[None, :], 0, band_h - 1)
    band = np.take_along_axis(band, idx[:, :, None], axis=0)
    alpha = np.take_along_axis(alpha, idx, axis=0)
    # composite + léger scrim central derrière le texte
    y0 = ytop
    y1 = min(H, ytop + band_h)
    hh = y1 - y0
    a = alpha[:hh, :, None]
    fr[y0:y1] = fr[y0:y1] * (1 - a) + band[:hh] * a
    return fr

def compose_badge(fr, vp, song_t):
    start = vp["t"]
    dur = vp["dur"]
    if not (start - 0.4 <= song_t <= start + dur + 0.4):
        return fr
    a = 0.0
    if song_t < start:
        a = (song_t - (start - 0.4)) / 0.4
    elif song_t <= start + dur:
        a = 1.0
    else:
        a = max(0.0, 1.0 - (song_t - (start + dur)) / 0.4)
    a *= 0.75                                     # plafond d'opacité
    rgb, cov = BADGE
    h, w = cov.shape
    x0 = (W - w) // 2
    y0 = 150
    reg = fr[y0:y0 + h, x0:x0 + w]
    a3 = (cov * a)[:, :, None]
    fr[y0:y0 + h, x0:x0 + w] = reg * (1 - a3) + rgb * a3
    return fr

def compose_cta(fr, song_t, t):
    for (a0, a1) in CTA_WINDOWS:
        if a0 <= song_t < a1:
            elapsed = song_t - a0
            seq_t = elapsed % 4.0
            if seq_t < 3.0:
                lay = make_cta_layer(seq_t, min(elapsed, 0.35) if elapsed < 0.35 else 1.0)
                if lay is not None:
                    rgb, cov = lay
                    a3 = cov[:, :, None]
                    fr = fr * (1 - a3) + rgb * a3
            return fr
    return fr

# ------------------------------------------------------------------ rendu
def main():
    os.makedirs(os.path.dirname(args.sortie), exist_ok=True)
    wav = "/tmp/maquette_audio.wav"
    subprocess.run([FFMPEG, "-v", "error", "-y", "-ss", str(T0), "-t", str(DUR), "-i", AUDIO,
                    "-map", "0:a:0", "-vn", "-ar", "48000", "-ac", "2",
                    "-af", f"afade=t=out:st={max(0.0, DUR-0.6):.2f}:d=0.6", wav], check=True)
    cmd = [FFMPEG, "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
           "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", args.sortie]
    pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    check_frames = {}
    for i in range(N):
        t = i / FPS
        song_t = T0 + t
        fr = render_bg(song_t, t)
        for vp in VERSES_PREP:
            fr = compose_badge(fr, vp, song_t)
            fr = compose_verse(fr, vp, song_t)
        fr = compose_cta(fr, song_t, t)
        # bandeau Bénin
        fr[H - 54:H] = BAND
        # étiquette de maquette (retirée du clip final)
        img = Image.fromarray(np.clip(fr, 0, 255).astype(np.uint8))
        d = ImageDraw.Draw(img)
        d.text((24, 40), "MAQUETTE — validation interne (retirée du clip final)", font=font(26, ui=True),
               fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
        if i in (60, 200, 330, 420):
            check_frames[i] = os.path.join(PROD, "apercu", f"MAQUETTE_frame_{i:04d}.jpg")
            img.save(check_frames[i], quality=92)
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=90)
        pipe.stdin.write(buf.getvalue())
        if i % 60 == 0:
            print(f"  frame {i}/{N}", flush=True)
    pipe.stdin.close()
    pipe.wait()
    print("vidéo:", args.sortie)
    for k, v in check_frames.items():
        print("frame de contrôle:", v)

if __name__ == "__main__":
    main()
