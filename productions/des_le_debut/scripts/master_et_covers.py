#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER MP3 + COVERS — « Dès le début »

· Master : chanson seule (sans cold-open), 48 kHz, MP3 320 kb/s
  loudnorm 2 passes (I=-14 LUFS, TP=-1.8) — la source mesurait +0,25 dBTP (risque de saturation)
· ID3v2.4 : TIT2/TPE1/TALB/TPE2/TCON/TDRC + TXXX contact,email + USLT paroles propres + APIC cover carrée
· Covers : 1080×1080 (APIC), 1080×1920, 1920×1080 — base IA (scène validée), texte incrusté en post
"""
import json, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from mutagen.id3 import ID3, APIC, USLT, TIT2, TPE1, TALB, TPE2, TCON, TDRC, TXXX, ID3NoHeaderError
from mutagen.mp3 import MP3

HERE = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(PROD, "..", ".."))
LIV = os.path.join(ROOT, "livrables")
FFMPEG = os.environ.get("FFMPEG", "/tmp/lyric-venv/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2")
FONT_LYR = os.path.join(ROOT, "assets", "fonts", "BarlowCondensed-Bold.ttf")
FONT_UI = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
AUDIO = os.path.join(ROOT, "Dès le début.mp3")
PAROLES = os.path.join(ROOT, "Dès le début- Jésus-Christ sauveur.txt")
os.makedirs(LIV, exist_ok=True)

TITRE, ARTISTE = "Dès le début", "Daïsky"
TEL = ["+229 01 61 16 24 08", "+229 01 49 11 49 51"]
MAIL = "daiskyproduction@gmail.com"
BENIN = ((0, 135, 81), (252, 209, 22), (232, 17, 45))
GOLD = (255, 196, 78)


def clean_lyrics():
    out = []
    for line in open(PAROLES, encoding="utf-8").read().splitlines():
        line = line.replace("\u200e", "").strip()
        line = re.sub(r"^\[\d+:\d+\.\d+\]\s*", "", line)
        if line:
            out.append(line)
    return "\n".join(out)


def benin_band(im, h):
    d = ImageDraw.Draw(im)
    W, H = im.size
    third = W // 3
    y = H - h
    d.rectangle([0, y, third, H], fill=BENIN[0])
    d.rectangle([third, y, W, y + h // 2], fill=BENIN[1])
    d.rectangle([third, y + h // 2, W, H], fill=BENIN[2])
    return im


def badge(im, x=None, y=None, scale=1.0):
    W, H = im.size
    f = ImageFont.truetype(FONT_UI, int(40 * scale))
    txt = "Dsky"
    box = f.getbbox(txt)
    fw, fh = int(48 * scale), int(34 * scale)
    w = (box[2] - box[0]) + int(22 * scale) + fw + int(32 * scale)
    h = int(72 * scale)
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=(8, 12, 22, 215),
                        outline=GOLD + (230,), width=2)
    d.text((int(16 * scale) - box[0], (h - (box[3] - box[1])) // 2 - box[1]), txt, font=f, fill=(255, 240, 205, 255))
    fh2 = int(34 * scale)
    third = int(fw * 0.34)
    fx = int(16 * scale) - box[0] + (box[2] - box[0]) + int(20 * scale)
    fy = (h - fh2) // 2
    d.rectangle([fx, fy, fx + third, fy + fh2], fill=BENIN[0] + (255,))
    d.rectangle([fx + third, fy, fx + fw, fy + fh2 // 2], fill=BENIN[1] + (255,))
    d.rectangle([fx + third, fy + fh2 // 2, fx + fw, fy + fh2], fill=BENIN[2] + (255,))
    d.rectangle([fx, fy, fx + fw - 1, fy + fh2 - 1], outline=(10, 10, 10, 170), width=2)
    X = x if x is not None else (W - w) // 2
    Y = y if y is not None else int(150 * scale)
    im.paste(lay, (X, Y), lay)
    return im


def cover(base_path, size, titre_size, out, safe=0.08):
    """Cover : base IA recadrée, voile dégradé, titre + artiste + badge + bandeau Bénin."""
    W, H = size
    im = Image.open(base_path).convert("RGB")
    # recadrage « cover » sur le point focal (centre)
    r = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * r + 0.5), int(im.height * r + 0.5)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = (im.height - H) // 2
    im = im.crop((x, y, x + W, y + H))
    # voile : sombre en haut et en bas, image préservée au centre
    arr = np.asarray(im, dtype=np.float32)
    yy = np.arange(H, dtype=np.float32)[:, None]
    top = np.clip(1.0 - yy / (H * 0.45), 0, 1) ** 1.5 * 0.55
    bot = np.clip((yy - H * 0.55) / (H * 0.45), 0, 1) ** 1.5 * 0.65
    mask = np.clip(top + bot, 0, 1)
    arr = arr * (1 - mask[:, :, None]) + (arr * 0.25) * mask[:, :, None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im, "RGBA")
    cx = W // 2
    ft = ImageFont.truetype(FONT_LYR, titre_size)
    fa = ImageFont.truetype(FONT_UI, int(titre_size * 0.34))
    fc = ImageFont.truetype(FONT_UI, int(titre_size * 0.20))
    # titre (retour à la ligne si trop large)
    maxw = W * (1 - 2 * safe)
    words, lines = TITRE.split(), []
    cur = ""
    for wd in words:
        test = (cur + " " + wd).strip()
        if ft.getbbox(test)[2] - ft.getbbox(test)[0] <= maxw:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = wd
    lines.append(cur)
    lh = int(titre_size * 1.04)
    ty = int(H * 0.33)
    for i, ln in enumerate(lines):
        d.text((cx, ty + i * lh), ln, font=ft, fill=(255, 245, 225, 255), anchor="mm",
               stroke_width=4, stroke_fill=(0, 0, 0, 200))
    d.text((cx, ty + len(lines) * lh + int(titre_size * 0.42)), ARTISTE, font=fa, fill=GOLD + (255,), anchor="mm",
           stroke_width=3, stroke_fill=(0, 0, 0, 190))
    d.line([cx - int(W * 0.12), ty + len(lines) * lh + int(titre_size * 0.80),
            cx + int(W * 0.12), ty + len(lines) * lh + int(titre_size * 0.80)],
           fill=GOLD + (200,), width=3)
    d.text((cx, H - int(H * 0.115)), f"WhatsApp {TEL[0]}", font=fc, fill=(245, 245, 245, 235), anchor="mm")
    d.text((cx, H - int(H * 0.082)), MAIL, font=fc, fill=(245, 245, 245, 235), anchor="mm")
    im = badge(im, y=int(H * 0.032), scale=max(0.8, W / 1500.0))
    im = benin_band(im, max(18, int(H * 0.028)))
    im.save(out, quality=94, optimize=True)
    print("cover:", out, im.size)
    return out


def main():
    # ---------------------------------------------------------- master MP3
    src = AUDIO
    p1 = subprocess.run([FFMPEG, "-hide_banner", "-i", src, "-map", "0:a:0", "-vn", "-af",
                         "highpass=30,lowpass=18000,loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json",
                         "-f", "null", "-"], capture_output=True, text=True)
    m = re.search(r"\{[^{}]*input_i[^{}]*\}", p1.stderr, re.S)
    off = float(json.loads(m.group(0)).get("target_offset", 0.0)) if m else 0.0
    tmp = "/tmp/master_audio.wav"
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", src, "-map", "0:a:0", "-vn",
                    "-af", f"highpass=30,lowpass=18000,loudnorm=I=-14:TP=-1.8:LRA=11:offset={off:.2f}",
                    "-ar", "48000", "-ac", "2", tmp], check=True)
    master = os.path.join(LIV, "Des_le_debut_master_320k.mp3")
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", tmp, "-map", "0:a:0", "-c:a", "libmp3lame",
                    "-b:a", "320k", "-ar", "48000", "-write_id3v2", "0", master], check=True)
    # contrôle réel du master
    p2 = subprocess.run([FFMPEG, "-hide_banner", "-i", master, "-map", "0:a:0", "-af",
                         "loudnorm=I=-14:TP=-1.8:print_format=json", "-f", "null", "-"],
                        capture_output=True, text=True)
    m2 = re.search(r"\{[^{}]*input_i[^{}]*\}", p2.stderr, re.S)
    meas = json.loads(m2.group(0)) if m2 else {}
    print("master mesuré :", {k: meas.get(k) for k in ("input_i", "input_tp", "input_lra")})

    # ---------------------------------------------------------- covers
    base = os.path.join(PROD, "fonds", "portrait", "s15_bras_leves_paumes_ciel.jpg")
    c_sq = cover(base, (1080, 1080), 190, os.path.join(LIV, "cover_des_le_debut_1080x1080.jpg"))
    c_v = cover(base, (1080, 1920), 210, os.path.join(LIV, "cover_des_le_debut_9x16.jpg"))
    c_h = cover(base, (1920, 1080), 200, os.path.join(LIV, "cover_des_le_debut_16x9.jpg"))

    # ---------------------------------------------------------- tags ID3
    try:
        tags = ID3(master)
    except ID3NoHeaderError:
        tags = ID3()
    tags.delall("APIC")
    tags.add(TIT2(encoding=3, text=TITRE))
    tags.add(TPE1(encoding=3, text=ARTISTE))
    tags.add(TPE2(encoding=3, text=ARTISTE))
    tags.add(TALB(encoding=3, text=TITRE))
    tags.add(TCON(encoding=3, text="Gospel / Louange"))
    tags.add(TDRC(encoding=3, text="2026"))
    tags.add(TXXX(encoding=3, desc="contact", text="WhatsApp " + " / ".join(TEL)))
    tags.add(TXXX(encoding=3, desc="email", text=MAIL))
    tags.add(USLT(encoding=3, lang="fra", desc="paroles", text=clean_lyrics()))
    with open(c_sq, "rb") as fh:
        tags.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=fh.read()))
    tags.save(master, v2_version=4)
    mp3 = MP3(master)
    print(f"ID3v2.4 écrit · durée {mp3.info.length:.2f} s · {mp3.info.bitrate//1000} kb/s · {mp3.info.sample_rate} Hz")
    print("APIC:", [a.mime + f" {len(a.data)//1024} ko" for a in tags.getall("APIC")])
    print("USLT:", len(tags.getall("USLT")[0].text), "caractères")
    print("taille master:", os.path.getsize(master) // 1024, "ko")


if __name__ == "__main__":
    main()
