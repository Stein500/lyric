#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_lyric_video.py — « Goinfres » (Dsky) · 1080x1920 @ 30 fps
Moteur v6.0 « WTBW Salut & Stickers Doux — Ça bouge, sans voiler la parole » (MODE PEINT, Animé N&B).

Nouveautés v6.0 (directives artiste) :
- RETRAIT TOTAL du système de code de fin et de l'accroche « Regarde jusqu'à la fin pour voir le code ».
- Début (0,00 -> 10,60 s) en mode « Salut · Wolof TechStein beat wê (WTBW) » avec animations fluides
  et douces de 3 stickers vectoriels :
    1) LIKE (cœur vectoriel + « Like »)
    2) CLIQUE SUR + POUR T'ABONNER (badge « + » vectoriel)
    3) COMMENTE SI TU AIMES (bulle de commentaire vectorielle)
- Carte finale (222,92 -> 227,92 s) en mode WTBW (« Merci d'avoir écouté ! » + les 3 stickers animés
  fluides et doux), sans code, sans contact, sans lien, sans logo.
- Palette Noir & Blanc / Argent / Blanc pur harmonisée avec le style STUDIO ANIME SEINEN N&B.
"""
import argparse, json, math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

RAC = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
FONT = os.path.join(RAC, "fonts")
FONDS = os.path.join(RAC, "fonds")
OUT = os.path.join(RAC, "livrables")
BADGE_ALPHA = 0.72            # <= 75 % (§7)
FADE = 0.35                   # fondu inter-plans / état éteint / entrée-sortie clochettes (§5.3-5.4, §6)
BELL = 4.0                    # période de la séquence clochette (§6)
SONG_END = 222.92             # durée décodée mesurée (§5.6 / §11)
CARD_END = SONG_END + 5.0     # carte finale = 5,00 s après la fin de la chanson (§7)
FLAG = False                  # aucun drapeau (§3 / §14)

def ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

def fnt(name, size):
    return ImageFont.truetype(os.path.join(FONT, "Montserrat-%s.ttf" % name), size)

SC = 1.10   # §5.1 : source surdimensionnée de 10 % (LANCZOS une seule fois par plan),
            # le travelling est une fenêtre qui glisse -> aucun resize par frame, zéro ghosting.

def prep(path):
    """768x1376 -> (1080*SC)x(1920*SC+) ancré EN HAUT : on rogne le bas, jamais le crâne (§3, §5.1)."""
    im = Image.open(path).convert("RGB")
    s = (W * SC) / im.width
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)

def slide(big, ax, ay):
    """Fenêtre 1080x1920 qui glisse dans le moule -> mouvement net, sans resize (§5.2)."""
    dx = big.width - W
    dy = big.height - H
    return big.crop((int(dx * ax), int(dy * ay), int(dx * ax) + W, int(dy * ay) + H))

def dim(im):
    """État éteint d'un vers déjà lu (§5.4) : Brightness 0.40 + GaussianBlur 2."""
    return ImageEnhance.Brightness(im).enhance(0.40).filter(ImageFilter.GaussianBlur(2))

def fit_font(d, txt, size, max_w=720, bold=True):
    style = "ExtraBold" if bold else "SemiBold"
    while size > 22 and d.textlength(txt, font=fnt(style, size)) > max_w:
        size -= 2
    return fnt(style, size), size

# ---------- Icônes vectorielles supersamplées x3 pour les stickers WTBW ----------
def make_sticker_icons():
    S = 3
    B = 110 * S
    icons = {}

    # 1. Cœur « LIKE » vectoriel
    im_like = Image.new("RGBA", (B, B), (0, 0, 0, 0))
    d = ImageDraw.Draw(im_like)
    cx, cy = B // 2, B // 2
    d.ellipse([8 * S, 8 * S, B - 8 * S, B - 8 * S], fill=(18, 22, 28, 235), outline=(255, 255, 255, 230), width=3 * S)
    pts = []
    for k in range(120):
        th = 2 * math.pi * k / 120.0
        x = 16 * (math.sin(th) ** 3)
        y = -(13 * math.cos(th) - 5 * math.cos(2 * th) - 2 * math.cos(3 * th) - math.cos(4 * th))
        pts.append((cx + x * 1.65 * S, cy + (y - 1.5) * 1.65 * S))
    d.polygon(pts, fill=(255, 255, 255, 250), outline=(210, 220, 235, 255))
    icons["like"] = im_like.resize((110, 110), Image.LANCZOS)

    # 2. Badge « + » (Clique sur + pour t'abonner) vectoriel
    im_plus = Image.new("RGBA", (B, B), (0, 0, 0, 0))
    d = ImageDraw.Draw(im_plus)
    d.ellipse([8 * S, 8 * S, B - 8 * S, B - 8 * S], fill=(245, 248, 255, 245), outline=(255, 255, 255, 255), width=3 * S)
    bar_w, bar_l = 9 * S, 26 * S
    d.rounded_rectangle([cx - bar_l, cy - bar_w, cx + bar_l, cy + bar_w], radius=4 * S, fill=(10, 14, 20, 255))
    d.rounded_rectangle([cx - bar_w, cy - bar_l, cx + bar_w, cy + bar_l], radius=4 * S, fill=(10, 14, 20, 255))
    icons["plus"] = im_plus.resize((110, 110), Image.LANCZOS)

    # 3. Bulle de commentaire « COMMENTE » vectorielle
    im_comm = Image.new("RGBA", (B, B), (0, 0, 0, 0))
    d = ImageDraw.Draw(im_comm)
    d.ellipse([8 * S, 8 * S, B - 8 * S, B - 8 * S], fill=(18, 22, 28, 235), outline=(255, 255, 255, 230), width=3 * S)
    d.rounded_rectangle([cx - 28 * S, cy - 22 * S, cx + 28 * S, cy + 14 * S], radius=12 * S,
                        fill=(255, 255, 255, 248))
    d.polygon([(cx - 12 * S, cy + 12 * S), (cx - 22 * S, cy + 27 * S), (cx + 2 * S, cy + 12 * S)],
              fill=(255, 255, 255, 248))
    for dx in (-13, 0, 13):
        d.ellipse([cx + (dx - 3.5) * S, cy - 7.5 * S, cx + (dx + 3.5) * S, cy - 0.5 * S], fill=(14, 18, 24, 255))
    icons["comm"] = im_comm.resize((110, 110), Image.LANCZOS)

    return icons

def prepare_card_bg(bg, scrim=142):
    """Fond de carte flouté et assombri en N&B (§7)."""
    im = bg.filter(ImageFilter.GaussianBlur(9))
    im = ImageEnhance.Brightness(im).enhance(0.62)
    ov = Image.new("RGBA", im.size, (8, 10, 14, scrim))
    return Image.alpha_composite(im.convert("RGBA"), ov)

def render_wtbw_card(base_rgba, mode, t_local, dur, icons):
    """
    Rendu image par image des cartes d'accueil et de fin en mode WTBW (Wolof TechStein beat wê)
    avec animations fluides et douces des 3 stickers (Like, Clique sur + pour t'abonner, Commente si tu aimes).
    Strictement dans les zones sûres : x in [170, 910], y in [260, 1520].
    """
    im = base_rgba.copy()
    d = ImageDraw.Draw(im)

    # Respiration douce globale
    u = max(0.0, min(1.0, t_local / max(1e-6, dur)))
    fade_in = min(1.0, t_local / 0.45)

    # Filets horizontaux haut et bas dans la zone sûre (x=170..910)
    y_top_line = 310
    y_bot_line = 1470
    d.line([(170, y_top_line), (910, y_top_line)], fill=(235, 240, 248, 210), width=3)
    d.line([(170, y_bot_line), (910, y_bot_line)], fill=(235, 240, 248, 210), width=3)

    # En-tête permanent de la carte
    head_txt = "WTBW · WOLOF TECHSTEIN BEAT WÊ !"
    fh, _ = fit_font(d, head_txt, 34, max_w=720, bold=True)
    wh = d.textlength(head_txt, font=fh)
    d.text(((W - wh) / 2, 336), head_txt, fill=(215, 222, 232, 245), font=fh)

    if mode == "intro_1":
        # Temps 1 (0,00 -> 5,30 s) : Salut en mode WTBW + Titre + 3 badges stickers flottants doux
        f_wtbw, _ = fit_font(d, "SALUT · WTBW", 84, max_w=720, bold=True)
        txt1 = "SALUT · WTBW"
        w1 = d.textlength(txt1, font=f_wtbw)
        y1 = 420 + int(6 * math.sin(2 * math.pi * t_local / 2.6))
        for ox, oy in ((3, 0), (-3, 0), (0, 3), (0, -3)):
            d.text(((W - w1) / 2 + ox, y1 + oy), txt1, fill=(255, 255, 255, 70), font=f_wtbw)
        d.text(((W - w1) / 2, y1), txt1, fill=(255, 255, 255, 255), font=f_wtbw)

        txt2 = "Wolof TechStein beat wê"
        f2, _ = fit_font(d, txt2, 46, max_w=720, bold=False)
        w2 = d.textlength(txt2, font=f2)
        d.text(((W - w2) / 2, 540), txt2, fill=(220, 226, 236, 245), font=f2)

        # Plaque centrale du titre de la chanson
        d.rounded_rectangle([210, 625, 870, 795], radius=32, fill=(14, 18, 24, 210),
                            outline=(255, 255, 255, 185), width=2)
        txt3 = "GOINFRES — DSKY"
        f3, _ = fit_font(d, txt3, 58, max_w=620, bold=True)
        w3 = d.textlength(txt3, font=f3)
        d.text(((W - w3) / 2, 675), txt3, fill=(255, 255, 255, 255), font=f3)

    elif mode == "intro_2":
        # Temps 2 (5,30 -> 10,60 s) : Invitation fluide et douce aux 3 actions
        txt1 = "BIENVENUE SUR WTBW"
        f1, _ = fit_font(d, txt1, 66, max_w=720, bold=True)
        w1 = d.textlength(txt1, font=f1)
        y1 = 430 + int(5 * math.sin(2 * math.pi * t_local / 2.4))
        d.text(((W - w1) / 2, y1), txt1, fill=(255, 255, 255, 255), font=f1)

        txt2 = "Soutiens le son en douceur :"
        f2, _ = fit_font(d, txt2, 44, max_w=720, bold=False)
        w2 = d.textlength(txt2, font=f2)
        d.text(((W - w2) / 2, 535), txt2, fill=(220, 226, 236, 245), font=f2)

        txt3 = "GOINFRES · DSKY"
        f3, _ = fit_font(d, txt3, 42, max_w=720, bold=True)
        w3 = d.textlength(txt3, font=f3)
        d.text(((W - w3) / 2, 615), txt3, fill=(255, 255, 255, 220), font=f3)

    else:
        # Carte finale (222,92 -> 227,92 s) : Merci sans code + les 3 stickers doux
        txt1 = "MERCI D'AVOIR ÉCOUTÉ !"
        f1, _ = fit_font(d, txt1, 68, max_w=720, bold=True)
        w1 = d.textlength(txt1, font=f1)
        y1 = 430 + int(5 * math.sin(2 * math.pi * t_local / 2.4))
        d.text(((W - w1) / 2, y1), txt1, fill=(255, 255, 255, 255), font=f1)

        txt2 = "Wolof TechStein beat wê (WTBW)"
        f2, _ = fit_font(d, txt2, 44, max_w=720, bold=False)
        w2 = d.textlength(txt2, font=f2)
        d.text(((W - w2) / 2, 535), txt2, fill=(220, 226, 236, 245), font=f2)

        txt3 = "GOINFRES · DSKY"
        f3, _ = fit_font(d, txt3, 42, max_w=720, bold=True)
        w3 = d.textlength(txt3, font=f3)
        d.text(((W - w3) / 2, 615), txt3, fill=(255, 255, 255, 220), font=f3)

    # ---------- Les 3 stickers animés (mouvement fluide et doux, y = 835 .. 1420) ----------
    sticker_specs = [
        ("like", "LIKE LA VIDÉO", "Laisse un cœur si tu valides", 0.0),
        ("plus", "CLIQUE SUR + POUR T'ABONNER", "Rejoins Wolof TechStein beat wê", 0.85),
        ("comm", "COMMENTE SI TU AIMES !", "Dis-nous ton vers préféré", 1.70),
    ]
    base_ys = [845, 1045, 1245]
    pw, ph = 700, 152

    for idx, (k_ico, title_s, sub_s, phase) in enumerate(sticker_specs):
        # Flottement sinusoïdal doux (vertical ±8 px, horizontal ±5 px) + pulsation douce
        dy = int(round(8.0 * math.sin(2 * math.pi * (t_local / 2.2) + phase)))
        dx = int(round(5.0 * math.cos(2 * math.pi * (t_local / 2.8) + phase)))
        pulse = 1.0 + 0.045 * math.sin(2 * math.pi * (t_local / 1.6) + phase)

        px = (W - pw) // 2 + dx
        py = base_ys[idx] + dy

        # Pilule du sticker
        pill = Image.new("RGBA", (pw + 24, ph + 24), (0, 0, 0, 0))
        dp = ImageDraw.Draw(pill)
        glow_a = int(165 + 65 * math.sin(2 * math.pi * (t_local / 1.6) + phase))
        dp.rounded_rectangle([12, 12, 12 + pw, 12 + ph], radius=42,
                             fill=(12, 16, 22, 224), outline=(255, 255, 255, glow_a), width=3)

        # Icône vectorielle animée (pulsation douce)
        ico_base = icons[k_ico]
        isz = int(round(104 * pulse))
        ico = ico_base.resize((isz, isz), Image.LANCZOS)
        pill.alpha_composite(ico, (30 - (isz - 104) // 2, 12 + (ph - isz) // 2))

        # Textes du sticker (auto-ajustés pour rester dans la pilule)
        ft, _ = fit_font(dp, title_s, 34, max_w=510, bold=True)
        fs, _ = fit_font(dp, sub_s, 25, max_w=510, bold=False)
        dp.text((156, 36), title_s, fill=(255, 255, 255, 252), font=ft)
        dp.text((156, 88), sub_s, fill=(205, 214, 226, 235), font=fs)

        if fade_in < 0.999:
            a_ch = pill.split()[-1].point(lambda v: int(v * fade_in))
            pill.putalpha(a_ch)

        im.alpha_composite(pill, (px - 12, py - 12))

    return im.convert("RGB")

# ---------- clochette premium (§6 : dessinée en N&B/argent, 36 angles supersamplés x3) ----------
def bell_frames(n=36):
    S = 3
    R = 150
    out = []
    for i in range(n):
        ang = -30 + 60 * i / (n - 1)
        img = Image.new("RGBA", (R * 2 * S, R * 2 * S), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        cx, cy = R * S, R * S + 24 * S
        pts = []
        for k in range(41):
            t = k / 40.0
            yy = cy - 92 * S + t * 118 * S
            ww = (18 + 62 * (t ** 1.75)) * S
            pts.append((cx - ww, yy))
        for k in range(40, -1, -1):
            t = k / 40.0
            yy = cy - 92 * S + t * 118 * S
            ww = (18 + 62 * (t ** 1.75)) * S
            pts.append((cx + ww, yy))
        d.polygon(pts, fill=(235, 240, 248, 250), outline=(255, 255, 255, 255))
        d.line([(cx - 44 * S, cy + 26 * S), (cx + 44 * S, cy + 26 * S)], fill=(120, 130, 145, 255), width=3 * S)
        d.ellipse([cx - 11 * S, cy + 26 * S, cx + 11 * S, cy + 48 * S], fill=(200, 208, 220, 255))
        d.arc([cx - 22 * S, cy - 122 * S, cx + 22 * S, cy - 78 * S], 180, 360, fill=(245, 248, 255, 255), width=6 * S)
        img = img.rotate(ang, resample=Image.BICUBIC, center=(cx, cy - 60 * S))
        out.append(img.resize((R * 2, R * 2), Image.LANCZOS))
    return out

def clochette_tile(ph, bells, layers):
    T = 720
    tile = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    plate = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    dp = ImageDraw.Draw(plate)
    dp.rounded_rectangle([34, 8, T - 34, T - 8], radius=54, fill=(8, 11, 16, 178),
                         outline=(240, 244, 250, 95), width=3)
    tile = Image.alpha_composite(tile, plate.filter(ImageFilter.GaussianBlur(5)))
    d = ImageDraw.Draw(tile)
    cx = T // 2
    swing = math.sin(2 * math.pi * ph * (BELL / 1.2))
    damp = 0.45 + 0.55 * abs(math.cos(math.pi * ph * (BELL / 2.4)))
    ang = 12 * swing * damp
    bi = max(0, min(len(bells) - 1, int(round((ang / 30 + 1) * (len(bells) - 1) / 2))))
    pulse = 1 + 0.05 * math.sin(2 * math.pi * ph * (BELL / 0.8))
    for k in range(2):
        t = (ph * (BELL / 0.9) + k * 0.5) % 1.0
        r = 120 + 150 * t
        a = int(150 * (1 - t))
        d.ellipse([cx - r, 150 - r * 0.55, cx + r, 150 + r * 0.55], outline=(230, 238, 250, a), width=4)
    bell = bells[bi]
    bs = int(300 * pulse)
    bell = bell.resize((bs, bs), Image.LANCZOS)
    halo = Image.new("RGBA", (bs + 60, bs + 60), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([10, 10, bs + 50, bs + 50], fill=(255, 255, 255, 42))
    halo = halo.filter(ImageFilter.GaussianBlur(18))
    tile.alpha_composite(halo, (cx - bs // 2 - 30, 40 - 30))
    tile.alpha_composite(bell, (cx - bs // 2, 40 - 20))
    for j, (sx, sy) in enumerate([(120, 90), (600, 130), (540, 300)]):
        a = int(200 * max(0.0, math.sin(2 * math.pi * (ph * 2 + j / 3.0))))
        r = 7
        d.polygon([(sx, sy - r), (sx + r // 3, sy - r // 3), (sx + r, sy), (sx + r // 3, sy + r // 3),
                   (sx, sy + r), (sx - r // 3, sy + r // 3), (sx - r, sy), (sx - r // 3, sy - r // 3)],
                  fill=(255, 255, 255, a))
    tile.alpha_composite(layers["txt"])
    if int(ph * BELL * 2) % 2 == 0:
        ImageDraw.Draw(tile).line([(cx + 200, 250), (cx + 120, 190)], fill=(255, 255, 255, 220), width=7)
        ImageDraw.Draw(tile).polygon([(cx + 120, 190), (cx + 152, 196), (cx + 138, 224)], fill=(255, 255, 255, 220))
    return tile

def clochette_text_layers():
    T = 720
    lay = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fA = fnt("ExtraBold", 56)
    fB = fnt("ExtraBold", 58)
    fR = fnt("SemiBold", 30)
    yA = 398
    txtA = "CLIQUE SUR +"
    sp = 5
    twA = sum(d.textlength(c, font=fA) for c in txtA) + sp * (len(txtA) - 1)
    x0 = (T - twA) / 2
    for ch in txtA:
        d.text((x0 + 2, yA + 3), ch, font=fA, fill=(160, 175, 195, 110))
        d.text((x0, yA), ch, font=fA, fill=(255, 255, 255, 248))
        x0 += d.textlength(ch, font=fA) + sp
    yB = 496
    f = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    dd = ImageDraw.Draw(f)
    pw, ph = 420, 96
    px, py = (T - pw) / 2, yB
    dd.rounded_rectangle([px, py, px + pw, py + ph], radius=ph / 2, fill=(14, 18, 26, 210))
    for i in range(4):
        fr = (px - i, py - i, px + pw + i, py + ph + i)
        col = (240 - i * 25, 244 - i * 25, 255 - i * 20, 225 - i * 40)
        dd.rounded_rectangle(fr, radius=ph / 2, outline=col, width=2)
    txt = "LIKE & PARTAGE"
    tw = dd.textlength(txt, font=fB)
    dd.text((px + (pw - tw) / 2, yB + 14), txt, font=fB, fill=(255, 255, 255, 252))
    lay = Image.alpha_composite(lay, f)
    d = ImageDraw.Draw(lay)
    rem = "Commente si tu aimes · WTBW"
    w = d.textlength(rem, font=fR)
    d.text(((T - w) / 2, 632), rem, font=fR, fill=(230, 235, 242, 238))
    return lay

def build_timeline(m):
    seg = []
    t0 = m["verses"][0]["t"]      # 10.60 s
    t_mid = round(t0 / 2.0, 2)    # 5.30 s
    seg.append(dict(kind="card", a=0.0, b=t_mid, card_mode="intro_1"))
    seg.append(dict(kind="card", a=t_mid, b=t0, card_mode="intro_2"))
    for v in m["verses"]:
        a, b = v["t"], v["fin"]
        disp = min(b, a + v["affichage_s"])
        seg.append(dict(kind="verse", a=a, b=b, img=v["image"], disp=disp,
                        dim=(b - disp > 1.0), txt=v["texte"]))
    seg.append(dict(kind="card", a=SONG_END, b=CARD_END, card_mode="outro"))
    return seg

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", type=float, default=0.0)
    ap.add_argument("--no-audio", action="store_true")
    a = ap.parse_args()
    m = json.load(open(os.path.join(RAC, "verses_map.json"), encoding="utf-8"))
    seg = build_timeline(m)
    t_end = a.preview if a.preview else CARD_END
    os.makedirs(OUT, exist_ok=True)

    cache = {}
    def base(p):
        if p not in cache:
            full = os.path.join(RAC, p)
            if not os.path.exists(full):
                full = os.path.join(RAC, "fonds/scene-01-ancre.png")
            b = prep(full)
            cache[p] = (b, dim(b))
        return cache[p]

    for s in seg:
        if s["kind"] == "verse" and s["a"] < t_end:
            base(s["img"])
    bells = bell_frames(36)
    layers = {"txt": clochette_text_layers()}
    icons = make_sticker_icons()

    card_bgs = {}
    for i, s in enumerate(seg):
        if s["kind"] == "card" and s["a"] < t_end:
            bgk = m["verses"][0]["image"] if s["a"] < SONG_END else m["verses"][-1]["image"]
            card_bgs[i] = prepare_card_bg(slide(base(bgk)[0], 0.5, 0.06))

    if 0 in card_bgs and not a.preview:
        render_wtbw_card(card_bgs[0], "intro_1", 1.5, 5.30, icons).save(os.path.join(OUT, "carte-accueil.jpg"), quality=94)
    if (len(seg) - 1) in card_bgs and not a.preview:
        render_wtbw_card(card_bgs[len(seg) - 1], "outro", 2.0, 5.00, icons).save(os.path.join(OUT, "carte-finale.jpg"), quality=94)

    # Vignette : masque L = 0 au centre, ~86 aux coins, flou 34 (§5.5)
    vmask = Image.new("L", (W, H), 0)
    dm = ImageDraw.Draw(vmask)
    for k in range(60):
        dm.rectangle([k * 5.0, k * 8.0, W - k * 5.0, H - k * 8.0], outline=int(86 - k * 1.4), width=9)
    vmask = vmask.filter(ImageFilter.GaussianBlur(34))
    noir = Image.new("RGB", (W, H), (4, 8, 12))

    # Grain 35 mm : 4 variantes pré-calculées, cyclées (§5.5)
    import random
    random.seed(342)
    grains = []
    for _ in range(4):
        g = Image.new("L", (W // 2, H // 2))
        gg = g.load()
        for i in range(0, (W // 2) * (H // 2), 2):
            gg[i % (W // 2), i // (W // 2)] = 128 + random.randint(-22, 22)
        grains.append(g.resize((W, H), Image.BILINEAR))

    def apply_grain(img, k):
        return Image.composite(ImageEnhance.Brightness(img).enhance(1.09), img, grains[k % 4])

    # Fenêtres de clochette : [disp + 0,15 s -> fin_vers], seuil 4,0 s (§6)
    SEUIL = 4.0
    windows = []
    for s in seg:
        if s["kind"] == "verse" and s["dim"] and s["b"] - s["disp"] >= SEUIL and s["b"] <= SONG_END + 0.01:
            windows.append([round(s["disp"] + 0.15, 2), round(min(s["b"], SONG_END), 2)])

    n = int(round(t_end * FPS))
    exact_dur = n / FPS
    ff = ffmpeg()
    aud = None
    if not a.no_audio:
        src = os.path.join(OUT, "Goinfres - master 320k.mp3")
        if not os.path.exists(src):
            src = os.path.join(OUT, "_master_noart.mp3")
        aud = os.path.join(OUT, "_audio_pad.m4a")
        subprocess.run([ff, "-y", "-hide_banner", "-loglevel", "error", "-i", src, "-vn",
                        "-map", "0:a:0", "-af", "apad=pad_dur=6.00",
                        "-t", "%.3f" % exact_dur, "-c:a", "aac", "-b:a", "256k", "-ar", "48000", aud], check=True)
    out = os.path.join(OUT, "goinfres-916%s.mp4" % ("-preview" if a.preview else ""))
    cmd = [ff, "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", "%dx%d" % (W, H), "-r", str(FPS), "-i", "-"]
    if aud:
        cmd += ["-i", aud, "-map", "0:v", "-map", "1:a"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-pix_fmt", "yuv420p",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            "-movflags", "+faststart"] + (["-c:a", "copy"] if aud else []) + [out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    si = 0
    prev = None
    badge_cache = {}
    fB = fnt("ExtraBold", 44)
    t_first = m["verses"][0]["t"]

    for k in range(n):
        t = k / FPS
        while si + 1 < len(seg) and t >= seg[si + 1]["a"]:
            si += 1
        s = seg[si]
        if s["kind"] == "card":
            cur = render_wtbw_card(card_bgs[si], s["card_mode"], t - s["a"], s["b"] - s["a"], icons)
        else:
            big, dmbig = base(s["img"])
            u = min(1.0, (t - s["a"]) / max(1e-6, s["b"] - s["a"]))
            ax0, ax1, ay0, ay1 = ((0.0, 1.0, 0.02, 0.98), (1.0, 0.0, 0.02, 0.98),
                                  (0.18, 0.82, 0.98, 0.02), (0.82, 0.18, 0.02, 0.98))[si % 4]
            ax = ax0 + (ax1 - ax0) * u
            ay = ay0 + (ay1 - ay0) * u
            cur = slide(big, ax, ay)
            if s["dim"] and t > s["disp"]:
                g = min(1.0, (t - s["disp"]) / FADE)
                cur = Image.blend(cur, slide(dmbig, ax, ay), g)
        if prev is not None and (t - s["a"]) < FADE and si > 0:
            cur = Image.blend(prev, cur, min(1.0, (t - s["a"]) / FADE))
        cur = cur.convert("RGBA")

        in_cta = any(wa - FADE <= t <= wb + FADE for wa, wb in windows)
        if s["kind"] == "verse" and not in_cta:  # Badge « Dsky » (§7 : jamais pendant les cartes ni pendant un CTA)
            ai = min(1.0, (t - s["a"]) / 0.4, (s["b"] - t) / 0.4)
            if ai > 0.01:
                key = int(round(ai * 8))
                if key not in badge_cache:
                    bd = Image.new("RGBA", (W, 120), (0, 0, 0, 0))
                    dd = ImageDraw.Draw(bd)
                    w0 = dd.textlength("Dsky", font=fB)
                    x0 = (W - w0) / 2
                    a_val = int(255 * BADGE_ALPHA * key / 8)
                    for ox, oy in ((-2, -2), (2, -2), (-2, 2), (2, 2), (0, 3)):
                        dd.text((x0 + ox, 40 + oy), "Dsky", font=fB, fill=(6, 10, 16, int(a_val * 0.78)))
                    dd.text((x0, 40), "Dsky", font=fB, fill=(255, 255, 255, a_val))
                    dd.line([((W - w0) / 2, 100), ((W + w0) / 2, 100)], fill=(235, 240, 248, int(185 * key / 8)), width=3)
                    badge_cache[key] = bd
                cur.alpha_composite(badge_cache[key], (0, 160))

        if s["kind"] == "verse":
            fr = max(0.0, min(1.0, (t - t_first) / (SONG_END - t_first)))  # filet de progression y=1560 (§7)
            d = ImageDraw.Draw(cur)
            d.rectangle([170, 1560, 910, 1564], fill=(235, 240, 248, 48))
            d.rectangle([170, 1558, 170 + int(740 * fr), 1566], fill=(255, 255, 255, 210))

        for wa, wb in windows:
            if wa - FADE <= t <= wb + FADE:
                al = min(1.0, (t - (wa - FADE)) / FADE, ((wb + FADE) - t) / FADE)
                ph = ((t - wa) % BELL) / BELL
                tl = clochette_tile(ph, bells, layers)
                if al < 0.999:
                    aa = tl.split()[-1].point(lambda v: int(v * al))
                    tl.putalpha(aa)
                cur.alpha_composite(tl, (int((W - 720) / 2), 620))

        cur = cur.convert("RGB")
        cur = Image.composite(noir, cur, vmask)
        cur = apply_grain(cur, k // 2)
        p.stdin.write(cur.tobytes())
        prev = cur
        if k % 300 == 0:
            print("frame %d/%d  t=%.2f s" % (k, n, t), flush=True)
    p.stdin.close()
    p.wait()
    if aud and os.path.exists(aud):
        os.remove(aud)
    rep = dict(fichier=os.path.basename(out), frames=n, fps=FPS, duree_s=round(n / FPS, 3),
               segments=len(seg), plans=len(cache), clochettes=len(windows),
               accueil_mode="WTBW_SALUT_STICKERS_DOUX", systeme_code=False,
               drapeau=bool(FLAG), crf=24, presets="veryfast", fondu_s=FADE, badge_alpha_max=BADGE_ALPHA)
    if not a.preview:
        json.dump(rep, open(os.path.join(OUT, "rendu_stats.json"), "w"), indent=2)
    print(json.dumps(rep, indent=2))
    sys.exit(p.returncode)

if __name__ == "__main__":
    main()
