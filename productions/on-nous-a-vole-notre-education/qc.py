#!/usr/bin/env python3
"""qc.py — planches de contrôle v6.0 (§10.5)
python3 qc.py salve 1 v-01-nuit ...      -> CONTROLE-salve1.jpg + CONTROLE-salve1-typo.jpg
python3 qc.py mp4                        -> CONTROLE-mp4-final.jpg (échantillons du MP4)
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
F = lambda n: os.path.join(FONTS, f"Montserrat-{n}.ttf")


def tile_contact(paths, out, cols=4, tw=500):
    th = int(tw * 1376 / 768)
    rows = (len(paths) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 12, rows * (th + 34) + 12), (12, 14, 18))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(F("SemiBold"), 20)
    for k, p in enumerate(paths):
        im = Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS)
        x, y = 12 + (k % cols) * (tw + 12), 12 + (k // cols) * (th + 34)
        sheet.paste(im, (x, y))
        d.text((x + 4, y + th + 6), f"{k+1:02d} {os.path.basename(p)}", font=f, fill=(230, 235, 245))
    sheet.save(out, quality=90)
    print(out, sheet.size)


def tile_typo(paths, out, cols=3, cw=520):
    """crops 1:1 de la bande 600→1340 avec grille de 16 px."""
    ch = 1376 - 600
    rows = (len(paths) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw + (cols + 1) * 10, rows * (ch + 26) + 10), (8, 10, 14))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(F("SemiBold"), 18)
    for k, p in enumerate(paths):
        im = Image.open(p).convert("RGB").crop((0, 600, 768, 1376))
        x, y = 10 + (k % cols) * (cw + 10), 10 + (k // cols) * (ch + 26)
        sheet.paste(im, (x, y))
        for gx in range(0, 768, 16):
            d.line([(x + gx, y), (x + gx, y + ch)], fill=(0, 190, 255) if gx % 128 == 0 else (40, 70, 90), width=1)
        for gy in range(0, ch, 16):
            col = (255, 0, 190) if (gy + 600) % 256 == 0 else (40, 70, 90)
            d.line([(x, y + gy), (x + 768, y + gy)], fill=col, width=1)
        d.text((x + 4, y + ch + 2), os.path.basename(p), font=f, fill=(235, 240, 250))
    sheet.save(out, quality=92)
    print(out, sheet.size)


def mp4(path, out, ffmpeg, dur, n=12):
    ts = [dur * (k + 0.5) / n for k in range(n)]
    tw, th = 360, 640
    cols = 6
    rows = (n + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 8, rows * (th + 26) + 8), (10, 12, 16))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(F("SemiBold"), 16)
    for k, t in enumerate(ts):
        p = f"/tmp/_f{k}.jpg"
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", path,
                        "-frames:v", "1", "-vf", f"scale={tw}:{th}", p], check=True)
        im = Image.open(p).convert("RGB")
        x, y = 8 + (k % cols) * (tw + 8), 8 + (k // cols) * (th + 26)
        sheet.paste(im, (x, y))
        d.text((x + 3, y + th + 4), f"{t:6.2f}s", font=f, fill=(235, 240, 250))
    sheet.save(out, quality=90)
    print(out, sheet.size)


def zoom(path, out, t, ffmpeg):
    """zoom 1:1 d'un frame rendu : 1080x1920 cropé centré, échelle 1."""
    p = "/tmp/_z.png"
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", path,
                    "-frames:v", "1", p], check=True)
    im = Image.open(p).convert("RGB")
    c = im.crop((0, 560, 1080, 1600))
    c.save(out, quality=95)
    print(out, c.size)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "salve":
        n = a[1]
        paths = [os.path.join(HERE, "fonds", x if x.endswith(".png") else x + ".png") for x in a[2:]]
        tile_contact(paths, os.path.join(HERE, f"CONTROLE-salve{n}.jpg"))
        tile_typo(paths, os.path.join(HERE, f"CONTROLE-salve{n}-typo.jpg"))
    elif a[0] == "mp4":
        import imageio_ffmpeg
        ff = imageio_ffmpeg.get_ffmpeg_exe()
        dur = float(a[2])
        mp4(os.path.join(HERE, a[1]), os.path.join(HERE, "CONTROLE-mp4-final.jpg"), ff, dur)
        if len(a) > 3:
            zoom(os.path.join(HERE, a[1]), os.path.join(HERE, "CONTROLE-typo-zoom.jpg"), float(a[3]), ff)
