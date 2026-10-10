#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Intro « clochette » — Gbètché vivi (Dsky), 9:16 1080x1920.

But demande par l'artiste le 2026-10-10 : le debut est LIBRE (aucune parole affichee),
il invite a regarder jusqu'a la fin ET on affiche des maintenant la sequence clochette
avec les appels a l'action  S'ABONNER / PARTAGE / COMMENTE / ENREGISTRE.

Contraintes heritees de PROMPT_UNIVERSEL_v5.7 :
  - zone sure : rien dans y 0->144, rien sous y 1574, rien a droite de x 910 entre y 960 et 1690
  - cloche et textes de CTA dans la bande y 620 -> 1340
  - cloche vectorielle supersamoplee x3, or -> bronze, anse, battant, halo
  - balancement +/-12 degres amorti, periode 1,2 s ; pulsation 0,8 s
  - 2 ondes concentriques (0,9 s), 3 etincelles, fleche clignotante
  - entree / sortie en fondu 0,35 s ; lecture <= 4 mots/s
  - typographie Montserrat (jamais de cursive), jamais de drapeau

Sorties : livrables/intro-clochette-916.mp4 + livrables/QC-intro/*.png
"""
import math, os, subprocess, sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
PERS = os.path.join(ROOT, "personnages")
OUT = os.path.join(ROOT, "livrables")
QC = os.path.join(OUT, "QC-intro")
FONTS = os.path.join(ROOT, "..", "..", "dsky-quotes", "assets", "fonts")

W, H, FPS = 1080, 1920, 30
T0, T1 = 0.0, 5.867            # 1er vers a 5,87 s -> l'intro s'arrete juste avant
SS = 3                          # supersampling de la cloche (x3)
FADE = 0.35

# --- zones sures -------------------------------------------------------------
SAFE_TOP, SAFE_BOT, SAFE_RIGHT_X, SAFE_RIGHT_Y = 144, 1574, 910, (960, 1690)
BELL_Y = (620, 1340)
LINE_W = 740

BG = os.path.join(PERS, "anim-01.png")
if not os.path.exists(BG):
    sys.exit("fond d'intro manquant : " + BG)


# --- typographie -------------------------------------------------------------
def font(size, weight=700):
    for name in ("Montserrat.ttf", "Montserrat-Italic.ttf"):
        p = os.path.join(FONTS, name)
        if not os.path.exists(p):
            continue
        try:
            f = ImageFont.truetype(p, size)
            try:
                f.set_variation_by_axes([weight])
                fake = 0
            except Exception:
                fake = 2 if weight >= 800 else 1 if weight >= 600 else 0
            return f, fake
        except Exception:
            continue
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    return ImageFont.truetype(p, size), 0


def text_w(dr, s, f, spacing=0, stroke=0):
    tot = 0
    for ch in s:
        l, t, r, b = dr.textbbox((0, 0), ch, font=f, stroke_width=stroke)
        tot += (r - l) + spacing
    return tot - (spacing if s else 0)


def draw_spaced(dr, cx, cy, s, f, fill, spacing=0, stroke=0, stroke_fill=None):
    """Texte centre horizontalement avec interlettrage explicite (px)."""
    tot = text_w(dr, s, f, spacing, stroke)
    x = cx - tot / 2
    for ch in s:
        l, t, r, b = dr.textbbox((0, 0), ch, font=f, stroke_width=stroke)
        dr.text((x - l, cy - (t + b) / 2), ch, font=f, fill=fill,
                stroke_width=stroke, stroke_fill=stroke_fill if stroke_fill is not None else fill)
        x += (r - l) + spacing
    return tot


def grad_mask(dr, size, cx, cy, s, f, spacing=0, stroke=0):
    """Masque L du texte (pour le remplir avec un degrade)."""
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    draw_spaced(d, cx, cy, s, f, 255, spacing, stroke)
    return m


# --- cloche vectorielle ------------------------------------------------------
def bell_layer(t):
    """Retourne (RGBA, (w,h)) : cloche balancee, halo, ondes, etincelles, fleche."""
    size = 400
    ss = size * SS
    img = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))

    # pulsations
    pulse = 0.5 + 0.5 * math.sin(2 * math.pi * t / 0.8)
    ring = math.exp(-0.85 * (t % 1.7))
    ang = 12.0 * ring * math.sin(2 * math.pi * t / 1.2)

    # --- halo ---
    halo = Image.new("L", (ss, ss), 0)
    hd = ImageDraw.Draw(halo)
    rr = int(ss * (0.40 + 0.045 * pulse))
    hd.ellipse((ss / 2 - rr, ss / 2 - rr, ss / 2 + rr, ss / 2 + rr), fill=int(120 + 70 * pulse))
    halo = halo.filter(ImageFilter.GaussianBlur(ss * 0.06))
    glow = Image.new("RGBA", (ss, ss), (90, 215, 255, 0))
    glow.putalpha(halo)
    img = Image.alpha_composite(img, glow)

    # --- ondes concentriques (periode 0,9 s) ---
    for k in range(2):
        ph = ((t / 0.9) + k * 0.5) % 1.0
        r0 = ss * (0.20 + 0.22 * ph)
        a = int(200 * (1 - ph))
        d = ImageDraw.Draw(img)
        d.ellipse((ss / 2 - r0, ss * 0.52 - r0 * 0.62, ss / 2 + r0, ss * 0.52 + r0 * 0.62),
                  outline=(150, 230, 255, a), width=int(ss * 0.012))

    # --- corps de la cloche (profil evase) ---
    cx = ss / 2
    top = ss * 0.235
    bot = ss * 0.665
    hw_top, hw_bot = ss * 0.085, ss * 0.215
    pts = []
    N = 60
    for i in range(N + 1):
        u = i / N
        y = top + (bot - top) * u
        hw = hw_top + (hw_bot - hw_top) * (u ** 1.9)
        pts.append((cx - hw, y))
    for i in range(N, -1, -1):
        u = i / N
        y = top + (bot - top) * u
        hw = hw_top + (hw_bot - hw_top) * (u ** 1.9)
        pts.append((cx + hw, y))
    mask = Image.new("L", (ss, ss), 0)
    md = ImageDraw.Draw(mask)
    md.polygon(pts, fill=255)
    md.rounded_rectangle((cx - hw_bot * 1.14, bot - ss * 0.012, cx + hw_bot * 1.14, bot + ss * 0.036),
                         radius=ss * 0.024, fill=255)          # rebord
    md.ellipse((cx - ss * 0.045, bot + ss * 0.036, cx + ss * 0.045, bot + ss * 0.118), fill=255)  # battant
    md.arc((cx - ss * 0.052, top - ss * 0.075, cx + ss * 0.052, top + ss * 0.030), 180, 360, fill=255,
           width=int(ss * 0.022))                              # anse
    md.ellipse((cx - ss * 0.022, top - ss * 0.085, cx + ss * 0.022, top - ss * 0.041), fill=255)

    # gradient or -> bronze + relief
    yy = np.linspace(0, 1, ss, dtype=np.float32)[:, None, None]
    g1 = np.array([255, 226, 130], np.float32)
    g2 = np.array([138, 84, 22], np.float32)
    grad = np.clip(g1 + (g2 - g1) * yy, 0, 255).astype(np.uint8)
    bell = Image.fromarray(np.repeat(grad.astype(np.uint8), ss, axis=1), "RGB")
    body = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    body.paste(bell, (0, 0), mask)
    # reflexus
    hi = Image.new("L", (ss, ss), 0)
    hd2 = ImageDraw.Draw(hi)
    hd2.polygon([(cx - hw_bot * 0.62, top + ss * 0.05), (cx - hw_bot * 0.30, top + ss * 0.03),
                 (cx - hw_bot * 0.05, bot - ss * 0.02), (cx - hw_bot * 0.42, bot - ss * 0.02)], fill=90)
    hi = hi.filter(ImageFilter.GaussianBlur(ss * 0.02))
    white = Image.new("RGBA", (ss, ss), (255, 252, 235, 255))
    white.putalpha(hi)
    body = Image.alpha_composite(body, white)
    img = Image.alpha_composite(img, body)

    # --- etincelles ---
    d = ImageDraw.Draw(img)
    for k, (dx, dy, ph) in enumerate(((-0.30, 0.06, 0.0), (0.31, -0.02, 0.37), (0.06, 0.40, 0.71))):
        a = max(0.0, math.sin(2 * math.pi * ((t / 0.8) + ph))) ** 3
        if a < 0.02:
            continue
        x, y = cx + dx * ss, ss * 0.5 + dy * ss
        r = ss * 0.030 * (0.6 + 0.4 * a)
        col = (255, 250, 220, int(230 * a))
        d.polygon([(x, y - r), (x + r * 0.26, y - r * 0.26), (x + r, y), (x + r * 0.26, y + r * 0.26),
                   (x, y + r), (x - r * 0.26, y + r * 0.26), (x - r, y), (x - r * 0.26, y - r * 0.26)], fill=col)

    # --- fleche clignotante vers la cloche ---
    blink = 1 if int(t * 2.5) % 2 == 0 else 0
    if blink:
        ax, ay = cx + ss * 0.30, ss * 0.80
        col = (255, 236, 170, 235)
        d.line((ax, ay, ax - ss * 0.10, ay - ss * 0.10), fill=col, width=int(ss * 0.020))
        d.polygon([(ax - ss * 0.10, ay - ss * 0.10), (ax - ss * 0.020, ay - ss * 0.085),
                   (ax - ss * 0.075, ay - ss * 0.020)], fill=col)

    # pivot en haut de l'anse, puis reduction
    img = img.rotate(ang, center=(cx, top - ss * 0.06), resample=Image.BICUBIC)
    return img.resize((size, size), Image.LANCZOS)


# --- pillules CTA ------------------------------------------------------------
def pill(size, txt, f, t, c_out=((0, 225, 255), (255, 60, 190)), fill=(9, 12, 17, 168),
         gtxt=((255, 255, 255), (176, 232, 255)), halo=True, spacing=4):
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rad = h // 2
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=rad, fill=fill)
    # contour degrade
    om = Image.new("L", (w, h), 0)
    ImageDraw.Draw(om).rounded_rectangle((2, 2, w - 3, h - 3), radius=rad - 2, outline=255, width=6)
    xs = np.linspace(0, 1, w, dtype=np.float32)[None, :, None]
    g = np.array(c_out[0], np.float32) + (np.array(c_out[1], np.float32) - np.array(c_out[0], np.float32)) * xs
    gimg = Image.fromarray(np.repeat(g.astype(np.uint8), h, axis=0), "RGB")
    img = Image.alpha_composite(img, Image.composite(gimg.convert("RGBA"), Image.new("RGBA", (w, h)), om))
    # halo pulse
    if halo:
        p = 0.5 + 0.5 * math.sin(2 * math.pi * t / 0.8)
        hm = om.filter(ImageFilter.GaussianBlur(9))
        glow = Image.new("RGBA", (w, h), (int(c_out[0][0]), int(c_out[0][1]), int(c_out[0][2]), int(150 * p)))
        glow.putalpha(hm.point(lambda v: int(v * p)))
        img = Image.alpha_composite(glow, img)
    # texte degrade
    tm = Image.new("L", (w, h), 0)
    td = ImageDraw.Draw(tm)
    draw_spaced(td, w / 2, h / 2 + 1, txt, f, 255, spacing=spacing)
    xs = np.linspace(0, 1, w, dtype=np.float32)[None, :, None]
    g2 = np.array(gtxt[0], np.float32) + (np.array(gtxt[1], np.float32) - np.array(gtxt[0], np.float32)) * xs
    timg = Image.fromarray(np.repeat(g2.astype(np.uint8), h, axis=0), "RGB").convert("RGBA")
    timg.putalpha(tm)
    return Image.alpha_composite(img, timg)


# --- fonds ------------------------------------------------------------------
base_bg = Image.open(BG).convert("RGB").resize((W, H), Image.LANCZOS)
scrim = Image.new("L", (W, H), 0)
sd = ImageDraw.Draw(scrim)
sd.rectangle((0, 0, W, 620), fill=120)
sd.rectangle((0, 620, W, 1180), fill=150)
sd.rectangle((0, 1180, W, H), fill=90)
scrim = scrim.filter(ImageFilter.GaussianBlur(90))
dark = Image.new("RGB", (W, H), (6, 8, 12))
BG_DONE = Image.composite(dark, base_bg, scrim.point(lambda v: int(v * 0.72)))

F_CARD, F_CARD_S = font(58, 900)
F_SUB, F_SUB_S = font(48, 700)
F_ABO, F_ABO_S = font(64, 900)
F_PILL, F_PILL_S = font(38, 800)
F_NOTE, F_NOTE_S = font(40, 600)
F_IDX, F_IDX_S = font(30, 700)


def fade(t, a, b, f=FADE):
    if t <= a or t >= b:
        return 0.0
    return min(1.0, min((t - a) / f, (b - t) / f))


def frame(t):
    img = BG_DONE.convert("RGBA")
    d = ImageDraw.Draw(img)

    # --- carte 1 : invitation (sous le badge, au-dessus de la bande CTA) ----
    a1 = fade(t, 0.30, 2.05)
    if a1 > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        bd = ImageDraw.Draw(lay)
        bd.rounded_rectangle((92, 232, W - 92, 322), radius=48, fill=(4, 6, 10, 132))
        lay = lay.filter(ImageFilter.GaussianBlur(26))
        dl = ImageDraw.Draw(lay)
        draw_spaced(dl, W / 2, 268, "REGARDE JUSQU'À LA FIN", F_CARD, (255, 255, 255, 255),
                    spacing=3, stroke=F_CARD_S, stroke_fill=(0, 0, 0, 170))
        dl.rounded_rectangle((W / 2 - 132, 306, W / 2 + 132, 312), radius=3,
                             fill=(0, 225, 255, int(220 * a1)))
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a1)))
        img = Image.alpha_composite(img, lay)

    # --- carte 2 : ce qu'on peut proposer (<= 4 mots/s) ----------------------
    a2 = fade(t, 1.95, 5.62)
    if a2 > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        bd = ImageDraw.Draw(lay)
        bd.rounded_rectangle((92, 348, W - 92, 492), radius=52, fill=(4, 6, 10, 126))
        lay = lay.filter(ImageFilter.GaussianBlur(26))
        dl = ImageDraw.Draw(lay)
        y = 404
        for ln in ("pour découvrir comment", "proposer un son ou des lyrics", "à réaliser pour toi !"):
            draw_spaced(dl, W / 2, y, ln, F_SUB, (255, 246, 224, 255), spacing=1,
                        stroke=F_SUB_S, stroke_fill=(0, 0, 0, 155))
            y += 60
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a2)))
        img = Image.alpha_composite(img, lay)

    # --- sequence clochette : tout dans la bande y 620 -> 1340 --------------
    ac = fade(t, 0.35, 5.80, 0.30)
    if ac > 0:
        bell = bell_layer(t)
        bw, bh = bell.size
        if ac < 1:
            bell = bell.copy()
            bell.putalpha(bell.getchannel("A").point(lambda v: int(v * ac)))
        img.alpha_composite(bell, (int(W / 2 - bw / 2), 612))

        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)

        # ABONNE-TOI : blanc -> bleu pale, espacement 7 px, halo cyan leger
        m = grad_mask(dl, (W, H), W / 2, 1002, "ABONNE-TOI", F_ABO, spacing=7, stroke=F_ABO_S)
        xs = np.linspace(0, 1, W, dtype=np.float32)[None, :, None]
        g1, g2 = np.array([255, 255, 255], np.float32), np.array([168, 226, 255], np.float32)
        gt = Image.fromarray(np.repeat((g1 + (g2 - g1) * xs).astype(np.uint8), H, axis=0), "RGB")
        glow = m.filter(ImageFilter.GaussianBlur(10))
        gl = Image.new("RGBA", (W, H), (60, 200, 255, 0))
        gl.putalpha(glow.point(lambda v: int(v * 0.5)))
        lay = Image.alpha_composite(lay, gl)
        tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tmp.paste(gt.convert("RGBA"), (0, 0), m)
        lay = Image.alpha_composite(lay, tmp)

        # pillules PARTAGE / COMMENTE / ENREGISTRE : largeur mesuree, bord droit <= x 900
        labels = ["PARTAGE", "COMMENTE", "ENREGISTRE"]
        PH, GAP, MAXW = 78, 18, 730
        for fsize in (38, 34, 31, 28, 25):
            fp, sk = font(fsize, 800)
            sp = int(PH * 0.10)
            ws = [int(text_w(d, s, fp, spacing=sp, stroke=sk)) + 44 for s in labels]
            if sum(ws) + GAP * (len(ws) - 1) <= MAXW:
                break
        else:
            ws = [int(text_w(d, s, fp, spacing=sp, stroke=sk)) + 40 for s in labels]
        tot = sum(ws) + GAP * (len(ws) - 1)
        x = int(W / 2 - tot / 2)
        ytop = 1044
        for txt, wd in zip(labels, ws):
            lay.alpha_composite(pill((wd, PH), txt, fp, t, spacing=sp,
                                     gtxt=((255, 255, 255), (188, 236, 255))), (x, ytop))
            x += wd + GAP

        dl = ImageDraw.Draw(lay)
        draw_spaced(dl, W / 2, 1168, "Clique sur la cloche, puis PARTAGE", F_NOTE,
                    (255, 244, 214, 255), spacing=1, stroke=F_NOTE_S, stroke_fill=(0, 0, 0, 155))
        draw_spaced(dl, W / 2, 1236, "commente · partage · enregistre", F_IDX,
                    (206, 226, 244, 255), spacing=1, stroke=F_IDX_S, stroke_fill=(0, 0, 0, 140))
        if ac < 1:
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * ac)))
        img = Image.alpha_composite(img, lay)

    # --- badge Dsky (sans drapeau), y = 160 ---------------------------------
    ab = fade(t, 0.20, 5.86, 0.40)
    if ab > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)
        bw2 = 250
        dl.rounded_rectangle((W / 2 - bw2 / 2, 152, W / 2 + bw2 / 2, 204), radius=26,
                             fill=(8, 10, 14, 130))
        f_i, s_i = font(34, 800)
        draw_spaced(dl, W / 2, 178, "Dsky", f_i, (255, 255, 255, int(255 * 0.75 * ab)),
                    spacing=2, stroke=s_i, stroke_fill=(0, 0, 0, 120))
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * ab)))
        img = Image.alpha_composite(img, lay)

    return img.convert("RGB")


def main():
    os.makedirs(QC, exist_ok=True)
    n = int(round((T1 - T0) * FPS))
    ff = subprocess.run([sys.executable, "-c", "import imageio_ffmpeg,sys;print(imageio_ffmpeg.get_ffmpeg_exe())"],
                        capture_output=True, text=True).stdout.strip().splitlines()[-1]
    out = os.path.join(OUT, "intro-clochette-916.mp4")
    audio = os.path.join(ROOT, "..", "..", "Gbètché vivi.mp3")
    if not os.path.exists(audio):
        import glob
        cand = glob.glob(os.path.join(ROOT, "..", "..", "Gb*tch* vivi.mp3"))
        audio = cand[0] if cand else None
    cmd = [ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-"]
    if audio:
        cmd += ["-ss", "0", "-t", f"{T1:.3f}", "-i", audio]
    cmd += ["-map", "0:v", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
            "-color_trc", "bt709", "-movflags", "+faststart"]
    if audio:
        cmd += ["-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest"]
    cmd += [out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    for i in range(n):
        t = T0 + i / FPS
        f = frame(t)
        p.stdin.write(f.tobytes())
        if i in (int(1.2 * FPS), int(2.6 * FPS), int(4.8 * FPS)):
            f.save(os.path.join(QC, f"intro-t{t:05.2f}.png"))
    p.stdin.close()
    err = p.stderr.read().decode(errors="ignore")
    rc = p.wait()
    print(f"frames={n} duree={n/FPS:.3f}s rc={rc}")
    if rc:
        print(err[-1200:])
        return 1
    print("ok ->", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
