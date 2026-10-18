#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_lyric_video.py — « On est réel » (Dsky) · 1080x1920 @ 30 fps
Moteur v5.9 « Ça bouge, sans voiler la parole » (MODE PEINT).

Principe : la parole est DÉJÀ peinte dans chaque plan -> aucun sous-titre incrusté.
Le moteur n'ajoute que : carte d'accueil (2 temps), carte finale (5 s après la fin),
badge « Dsky » (liseré sombre, fondu 0,4 s par vers, jamais permanent), clochettes premium
dans les fenêtres sans lecture (>= 4,0 s après disp + 0,15 s), filet de progression,
grain 35 mm cyclé (4 variantes) et vignette masque L.

Usage :
  python render_lyric_video.py --preview 60     # 60 s de test (couvre carte d'accueil + v-01..v-11)
  python render_lyric_video.py                  # rendu complet (quand les 46 plans sont présents)
  python render_lyric_video.py --no-audio       # vidéo seule (debug)
"""
import argparse, json, math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

RAC = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
FONT = os.path.join(RAC, "fonts")
FONDS = os.path.join(RAC, "fonds")
OUT = os.path.join(RAC, "livrables")
BADGE_ALPHA = 0.72            # <= 75 % (v5.9 §7)
FADE = 0.35                   # fondu inter-plans / état éteint / entrée-sortie clochettes (§5.3-5.4, §6)
BELL = 4.0                    # période de la séquence clochette (§6)
SONG_END = 244.99             # durée décodée mesurée (§5.6 / §11)
CARD_END = SONG_END + 5.0     # carte finale = 5,00 s après la fin de la chanson (§7)
CODE = "0405"                 # code de fin, lié à la durée 4 min 05 s (§2 / §7)
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

def card(bg, lines, scrim=118, head=None):
    """Fabrication des cartes (§7) : GaussianBlur 9, Brightness 0.74, Color 1.06, scrim #0B1B2A α 118, fit() <= 740 px."""
    im = bg.filter(ImageFilter.GaussianBlur(9))
    im = ImageEnhance.Brightness(im).enhance(0.74)
    im = ImageEnhance.Color(im).enhance(1.06)
    ov = Image.new("RGBA", im.size, (11, 27, 42, scrim))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(im)
    htot = sum(int(s * 1.42) for _, s, _ in lines) + (86 if head else 0) + 40
    y = max(360, (H - htot) // 2)
    d.line([(170, y - 26), (910, y - 26)], fill=(217, 164, 65, 255), width=3)

    def fit(txt, size):
        bold = size >= 90
        while size > 26 and d.textlength(txt, font=fnt("ExtraBold" if bold else "SemiBold", size)) > 740:
            size -= 2
        return fnt("ExtraBold" if bold else "SemiBold", size), size

    if head:
        fh, _ = fit(head, 40)
        w = d.textlength(head, font=fh)
        d.text(((W - w) / 2, y), head, fill=(232, 163, 61, 255), font=fh)
        y += 86
    for txt, size, col in lines:
        f, size = fit(txt, size)
        w = d.textlength(txt, font=f)
        if "ExtraBold" in f.path:  # halo or 3 px sur les très gros titres (§7)
            for o in ((3, 0), (-3, 0), (0, 3), (0, -3)):
                d.text(((W - w) / 2 + o[0], y + o[1]), txt, fill=(217, 164, 65, 120), font=f)
        d.text(((W - w) / 2, y), txt, fill=col, font=f)
        y += int(size * 1.42)
    d.line([(170, y + 6), (910, y + 6)], fill=(217, 164, 65, 255), width=3)
    return im

# ---------- clochette premium (§6 : dessinée, 36 angles supersamplés x3) ----------
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
        d.polygon(pts, fill=(226, 183, 96, 250), outline=(255, 232, 170, 255))
        d.line([(cx - 44 * S, cy + 26 * S), (cx + 44 * S, cy + 26 * S)], fill=(150, 104, 38, 255), width=3 * S)
        d.ellipse([cx - 11 * S, cy + 26 * S, cx + 11 * S, cy + 48 * S], fill=(196, 138, 52, 255))
        d.arc([cx - 22 * S, cy - 122 * S, cx + 22 * S, cy - 78 * S], 180, 360, fill=(240, 210, 140, 255), width=6 * S)
        img = img.rotate(ang, resample=Image.BICUBIC, center=(cx, cy - 60 * S))
        out.append(img.resize((R * 2, R * 2), Image.LANCZOS))
    return out

def clochette_tile(ph, bells, layers):
    T = 720
    tile = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    plate = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    dp = ImageDraw.Draw(plate)
    dp.rounded_rectangle([34, 8, T - 34, T - 8], radius=54, fill=(7, 13, 21, 158),
                         outline=(217, 164, 65, 70), width=3)
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
        d.ellipse([cx - r, 150 - r * 0.55, cx + r, 150 + r * 0.55], outline=(120, 220, 255, a), width=4)
    bell = bells[bi]
    bs = int(300 * pulse)
    bell = bell.resize((bs, bs), Image.LANCZOS)
    halo = Image.new("RGBA", (bs + 60, bs + 60), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([10, 10, bs + 50, bs + 50], fill=(255, 214, 120, 46))
    halo = halo.filter(ImageFilter.GaussianBlur(18))
    tile.alpha_composite(halo, (cx - bs // 2 - 30, 40 - 30))
    tile.alpha_composite(bell, (cx - bs // 2, 40 - 20))
    for j, (sx, sy) in enumerate([(120, 90), (600, 130), (540, 300)]):
        a = int(200 * max(0.0, math.sin(2 * math.pi * (ph * 2 + j / 3.0))))
        r = 7
        d.polygon([(sx, sy - r), (sx + r // 3, sy - r // 3), (sx + r, sy), (sx + r // 3, sy + r // 3),
                   (sx, sy + r), (sx - r // 3, sy + r // 3), (sx - r, sy), (sx - r // 3, sy - r // 3)],
                  fill=(255, 240, 190, a))
    tile.alpha_composite(layers["txt"])
    if int(ph * BELL * 2) % 2 == 0:
        ImageDraw.Draw(tile).line([(cx + 200, 250), (cx + 120, 190)], fill=(255, 240, 190, 220), width=7)
        ImageDraw.Draw(tile).polygon([(cx + 120, 190), (cx + 152, 196), (cx + 138, 224)], fill=(255, 240, 190, 220))
    return tile

def clochette_text_layers():
    T = 720
    lay = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fA = fnt("ExtraBold", 62)
    fB = fnt("ExtraBold", 62)
    fR = fnt("SemiBold", 34)
    yA = 400
    txtA = "ABONNE-TOI"
    sp = 7
    twA = sum(d.textlength(c, font=fA) for c in txtA) + sp * (len(txtA) - 1)
    x0 = (T - twA) / 2
    for i, ch in enumerate(txtA):
        d.text((x0 + 2, yA + 3), ch, font=fA, fill=(90, 200, 255, 110))
        d.text((x0, yA), ch, font=fA, fill=(255 - i * 11, 252, 255, 245))
        x0 += d.textlength(ch, font=fA) + sp
    yB = 500
    f = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    dd = ImageDraw.Draw(f)
    pw, ph = 360, 96
    px, py = (T - pw) / 2, yB
    dd.rounded_rectangle([px, py, px + pw, py + ph], radius=ph / 2, fill=(10, 16, 26, 168))
    for i in range(4):
        fr = (px - i, py - i, px + pw + i, py + ph + i)
        col = (90 + i * 34, 210 - i * 30, 255 - i * 12, 220 - i * 40)
        dd.rounded_rectangle(fr, radius=ph / 2, outline=col, width=2)
    txt = "PARTAGE"
    tw = dd.textlength(txt, font=fB)
    for i, ch in enumerate(txt):
        xx = px + (pw - tw) / 2 + dd.textlength(txt[:i], font=fB)
        g = int(120 + 135 * i / max(1, len(txt) - 1))
        dd.text((xx, yB + 12), ch, font=fB, fill=(140 + g // 2, g, 255 - g // 3, 250))
    lay = Image.alpha_composite(lay, Image.composite(f, Image.new("RGBA", (T, T), (0, 0, 0, 0)),
                                                     f.split()[-1].filter(ImageFilter.GaussianBlur(0))))
    d = ImageDraw.Draw(lay)
    rem = "Clique sur la cloche, puis PARTAGE"
    w = d.textlength(rem, font=fR)
    d.text(((T - w) / 2, 636), rem, font=fR, fill=(243, 231, 211, 235))
    return lay

def build_timeline(m):
    seg = []
    t0 = m["verses"][0]["t"]  # 10.70 s
    t_mid = round(t0 / 2.0, 2)  # 5.35 s
    seg.append(dict(kind="card", a=0.0, b=t_mid, head="ON EST RÉEL · DSKY",
                    lines=[("Regarde jusqu'à la fin", 88, (243, 231, 211, 255)),
                           ("(4 min 05, c'est le code)", 38, (232, 163, 61, 255))]))
    seg.append(dict(kind="card", a=t_mid, b=t0, head="ON EST RÉEL · DSKY",
                    lines=[("pour découvrir comment proposer", 54, (232, 163, 61, 255)),
                           ("un son ou des lyrics", 54, (243, 231, 211, 255)),
                           ("à réaliser pour toi !", 54, (243, 231, 211, 255))]))
    for v in m["verses"]:
        a, b = v["t"], v["fin"]
        disp = min(b, a + v["affichage_s"])
        seg.append(dict(kind="verse", a=a, b=b, img=v["image"], disp=disp,
                        dim=(b - disp > 1.0), txt=v["texte"]))
    seg.append(dict(kind="card", a=SONG_END, b=CARD_END, head="Wolof TechStein beat wê !",
                    lines=[("Merci d'avoir regardé", 96, (243, 231, 211, 255)),
                           ("Tu veux un son ou des lyrics", 46, (232, 163, 61, 255)),
                           ("à réaliser pour toi ?", 46, (232, 163, 61, 255)),
                           ("Commente le code", 40, (243, 231, 211, 255)),
                           (CODE, 210, (217, 164, 65, 255))]))
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
    cards = {}
    for i, s in enumerate(seg):
        if s["kind"] == "card" and s["a"] < t_end:
            bgk = m["verses"][0]["image"] if s["a"] < SONG_END else m["verses"][-1]["image"]
            cards[i] = card(slide(base(bgk)[0], 0.5, 0.06),
                            [(t, z, c[:3]) for t, z, c in s["lines"]], head=s.get("head"))
    if 0 in cards and not a.preview:
        cards[0].save(os.path.join(OUT, "carte-accueil.jpg"), quality=94)
    if (len(seg) - 1) in cards and not a.preview:
        cards[len(seg) - 1].save(os.path.join(OUT, "carte-finale.jpg"), quality=94)

    # Vignette : masque L = 0 au centre, ~86 aux coins, flou 34 (§5.5)
    vmask = Image.new("L", (W, H), 0)
    dm = ImageDraw.Draw(vmask)
    for k in range(60):
        dm.rectangle([k * 5.0, k * 8.0, W - k * 5.0, H - k * 8.0], outline=int(86 - k * 1.4), width=9)
    vmask = vmask.filter(ImageFilter.GaussianBlur(34))
    noir = Image.new("RGB", (W, H), (4, 10, 18))

    # Grain 35 mm : 4 variantes pré-calculées, cyclées (§5.5)
    import random
    random.seed(405)
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
        src = os.path.join(OUT, "On est réel - master 320k.mp3")
        if not os.path.exists(src):
            src = os.path.join(OUT, "_master_noart.mp3")
        aud = os.path.join(OUT, "_audio_pad.m4a")
        subprocess.run([ff, "-y", "-hide_banner", "-loglevel", "error", "-i", src, "-vn",
                        "-map", "0:a:0", "-af", "apad=pad_dur=6.00",
                        "-t", "%.3f" % exact_dur, "-c:a", "aac", "-b:a", "256k", "-ar", "48000", aud], check=True)
    out = os.path.join(OUT, "on-est-reel-916%s.mp4" % ("-preview" if a.preview else ""))
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
            cur = cards[si].copy()
            u = (t - s["a"]) / max(1e-6, s["b"] - s["a"])
            cur = ImageEnhance.Brightness(cur).enhance(0.92 + 0.08 * math.sin(math.pi * u))
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
                        dd.text((x0 + ox, 40 + oy), "Dsky", font=fB, fill=(6, 12, 20, int(a_val * 0.72)))
                    dd.text((x0 + 2, 42), "Dsky", font=fB, fill=(217, 164, 65, int(120 * key / 8)))
                    dd.text((x0, 40), "Dsky", font=fB, fill=(243, 231, 211, a_val))
                    dd.line([((W - w0) / 2, 100), ((W + w0) / 2, 100)], fill=(217, 164, 65, int(180 * key / 8)), width=3)
                    badge_cache[key] = bd
                cur.alpha_composite(badge_cache[key], (0, 160))

        if s["kind"] == "verse":
            fr = max(0.0, min(1.0, (t - t_first) / (SONG_END - t_first)))  # filet de progression y=1560 (§7)
            d = ImageDraw.Draw(cur)
            d.rectangle([170, 1560, 910, 1564], fill=(243, 231, 211, 46))
            d.rectangle([170, 1558, 170 + int(740 * fr), 1566], fill=(217, 164, 65, 205))

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
               segments=len(seg), plans=len(cache), clochettes=len(windows), code=CODE,
               drapeau=bool(FLAG), crf=24, presets="veryfast", fondu_s=FADE, badge_alpha_max=BADGE_ALPHA)
    if not a.preview:
        json.dump(rep, open(os.path.join(OUT, "rendu_stats.json"), "w"), indent=2)
    print(json.dumps(rep, indent=2))
    sys.exit(p.returncode)

if __name__ == "__main__":
    main()
