#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carres + pochette integree au master — Gbetché vivi.

Le fond est un portrait 9:16 ne rogne JAMAIS le visage : pour passer au carre 1080x1080 on
compose (image recadree sur le buste + fond floute etire) au lieu de rogner le haut et le bas.
Puis APIC embedde dans le master MP3 (ID3v2.4). Le USLT (paroles) se pose cote Termux avec
eyeD3 : ffmpeg n'expose pas d'ecriture USLT fiable, on ne le declare donc pas fait ici.
"""
import os, subprocess, sys, glob
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PERS = os.path.join(HERE, "personnages")
OUT = os.path.join(HERE, "livrables")
COV = os.path.join(HERE, "covers")
os.makedirs(COV, exist_ok=True)
S = 1080


def square(src, dst, band=(0.06, 0.62), title=None):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    y0, y1 = int(h * band[0]), int(h * band[1])
    fg = im.crop((0, y0, w, y1))
    r = S / fg.width
    fg = fg.resize((S, int(fg.height * r)), Image.LANCZOS)
    if fg.height < S:
        pad = (S - fg.height) // 2
        bg = im.resize((S, S), Image.LANCZOS).filter(ImageFilter.GaussianBlur(34))
        canvas = bg
        canvas.paste(fg, (0, pad))
    else:
        canvas = fg.crop((0, (fg.height - S) // 2, S, (fg.height - S) // 2 + S))
    if title:
        sys.path.insert(0, HERE)
        from render_intro_cta import font, draw_spaced
        d = ImageDraw.Draw(canvas)
        f, sk = font(64, 900)
        lay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)
        dl.rounded_rectangle((48, S - 232, S - 48, S - 96), radius=40, fill=(6, 8, 12, 150))
        draw_spaced(dl, S / 2, S - 186, title, f, (255, 255, 255, 250), spacing=1, stroke=sk,
                    stroke_fill=(0, 0, 0, 190))
        f2, s2 = font(34, 700)
        draw_spaced(dl, S / 2, S - 124, "Dsky · Bandit Positif", f2, (255, 236, 190, 255), spacing=2,
                    stroke=s2, stroke_fill=(0, 0, 0, 170))
        canvas = Image.alpha_composite(canvas.convert("RGBA"), lay).convert("RGB")
    canvas.save(dst, quality=92)
    return canvas.size


def embed(cover, mp3, out):
    ff = subprocess.run([sys.executable, "-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"],
                        capture_output=True, text=True).stdout.strip().splitlines()[-1]
    cmd = [ff, "-v", "error", "-y", "-i", mp3, "-i", cover,
           "-map", "0:a", "-map", "1:0", "-c:a", "copy", "-c:v", "copy",
           "-id3v2_version", "3", "-metadata:s:v", "title=Album cover", "-metadata:s:v", "comment=Cover (front)",
           "-metadata", "title=Gbètché vivi", "-metadata", "artist=Dsky",
           "-metadata", "album=Bandit Positif", "-metadata", "genre=Afro-fusion",
           "-metadata", "year=2026", "-metadata", "comment=Wolof TechStein beat wê ! | visuels et clip generes par IA (parole : artiste)", out]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stderr or "")[-500:]


if __name__ == "__main__":
    a30 = os.path.join(PERS, "anim-30.png")
    cov = os.path.join(COV, "gbetché-vivi-1080.jpg")
    print("cover:", square(a30, cov, title="Gbètché vivi"))
    for n, name in ((12, "carré-A12"), (28, "carré-A28"), (5, "carré-A05")):
        square(os.path.join(PERS, f"anim-{n:02d}.png"), os.path.join(COV, f"{name}.jpg"))
    mp3 = os.path.join(OUT, "Gbetché vivi - master.mp3")
    tagged = os.path.join(OUT, "Gbetché vivi - master - tagué.mp3")
    if os.path.exists(mp3):
        rc, err = embed(cov, mp3, tagged)
        print("embed APIC rc=", rc, err if rc else "")
        if rc == 0:
            os.replace(tagged, mp3)
            print("-> pochette ID3v2.4 integree dans", mp3, os.path.getsize(mp3) // 1024, "KB")
    print("covers:", sorted(os.path.basename(p) for p in glob.glob(os.path.join(COV, "*.jpg"))))
