#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vidéo TikTok 1080x1920 à partir des bases 100 % IA.
Usage : python3 build_video.py 401 410 "FRUITS"
Lit les CTA dans video-ctas.json {numero: "texte CTA"}.
Fond flouté zoomé + image recadrée (bande basse ôtée) en zone sûre + CTA PNG
+ badge DSKY WTBW clignotant + xfade + musique assets/musique-douce.mp3.
"""
import json, math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
GOLD = (212, 162, 76, 255)
WHITE = (255, 255, 255, 242)

def text_img(text, font, fill, canvas, glow=None):
    img = Image.new("RGBA", canvas, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    bb = d.textbbox((0, 0), text, font=font)
    x = (canvas[0] - (bb[2] - bb[0])) // 2 - bb[0]
    y = (canvas[1] - (bb[3] - bb[1])) // 2 - bb[1]
    if glow:
        g = Image.new("RGBA", canvas, (0, 0, 0, 0))
        ImageDraw.Draw(g).text((x, y), text, font=font, fill=glow)
        g = g.filter(ImageFilter.GaussianBlur(9))
        img.alpha_composite(g); img.alpha_composite(g)
    # ombre douce
    sh = Image.new("RGBA", canvas, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((x + 2, y + 3), text, font=font, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(2))
    img.alpha_composite(sh)
    d.text((x, y), text, font=font, fill=fill)
    return img

def main():
    n1, n2, theme = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    nums = list(range(n1, n2 + 1))
    ctas = json.load(open("video-ctas.json", encoding="utf-8"))
    work = f"videos/work-{n1}-{n2}"
    os.makedirs(work, exist_ok=True)
    os.makedirs("videos", exist_ok=True)
    out = f"videos/video-{n1}-{n2}-{theme.lower()}.mp4"
    D, FPS = 96, 30  # 3,2 s par clip
    DUR = D / FPS

    # --- 1. CTA PNG + séquence badge clignotant (1,2 s @30, boucle) ---
    cta_files, cta_inputs = [], []
    f_cta = ImageFont.truetype(SERIF, 46)
    f_badge = ImageFont.truetype(SERIF, 38)
    for n in nums:
        p = f"{work}/cta-{n}.png"
        text_img(ctas[str(n)], f_cta, WHITE, (1080, 260)).save(p)
        cta_files.append(p)
    # séquence badge (mov png + alpha), alpha sinusoïdale, boucle parfaite
    frames, badge_seq = 36, f"{work}/badge-blink.mov"
    fl = []
    for k in range(frames):
        a = 0.30 + 0.60 * (0.5 + 0.5 * math.sin(2 * math.pi * k / frames - math.pi / 2))
        img = text_img("D S K Y   W T B W", f_badge, GOLD[:3] + (int(255 * a),),
                       (1080, 160), glow=GOLD[:3] + (int(140 * a),))
        img.save(f"{work}/badge-{k:02d}.png")
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error",
                    "-framerate", str(FPS), "-i", f"{work}/badge-%02d.png",
                    "-frames:v", str(frames), "-c:v", "png", "-pix_fmt", "rgba",
                    badge_seq], check=True)

    # --- 2. inputs ffmpeg ---
    cmd = [FF, "-y", "-hide_banner", "-loglevel", "warning"]
    for n in nums:
        cmd += ["-i", f"assets/bases/base-{n}.jpg"]
    cmd += ["-stream_loop", "-1", "-i", badge_seq]
    for p in cta_files:
        cmd += ["-i", p]
    cmd += ["-i", "assets/musique-douce.mp3"]
    BADGE, CTA0, MUS = len(nums), len(nums) + 1, len(nums) + 11

    # --- 3. filter_complex ---
    parts = []
    for i in range(len(nums)):
        z = (f"min(1+{0.0005}*on,1.05)" if i % 2 == 0
             else f"max(1.05-0.0005*on,1.0)")
        parts.append(
            f"[{i}:v]split=2[ba{i}][fa{i}];"
            f"[ba{i}]scale=1080:1920:force_original_aspect_ratio=increase,"
            f"crop=1080:1920,boxblur=40:2,eq=brightness=-0.26:saturation=0.92,"
            f"zoompan=z='min(1+0.0005*on,1.05)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":d={D}:s=1080x1920:fps={FPS}[bg{i}];"
            f"[fa{i}]crop=w=iw:h=ih*0.88:x=0:y=0,scale=932:1230,"
            f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":d={D}:s=932x1230:fps={FPS}[fg{i}];"
            f"[bg{i}][fg{i}]overlay=74:290[b{i}];"
            f"[b{i}][{CTA0 + i}:v]overlay=0:1652,format=yuv420p,settb=AVTB,fps={FPS}[v{i}]")
    prev = "v0"
    for k in range(1, len(nums)):
        off = round(k * (DUR - 0.7), 2)
        lab = f"x{k}"
        parts.append(f"[{prev}][v{k}]xfade=transition=fade:duration=0.7:offset={off}[{lab}]")
        prev = lab
    total = (len(nums) - 1) * (DUR - 0.7) + DUR
    parts.append(f"[{prev}][{BADGE}:v]overlay=0:1756"
                 f",fade=t=in:d=0.8,fade=t=out:st={total - 1.3:.2f}:d=1.3,"
                 f"format=yuv420p[vout]")
    parts.append(f"[{MUS}:a]atrim=0:{total + 0.3:.2f},asetpts=PTS-STARTPTS,"
                 f"afade=t=in:d=1.2,afade=t=out:st={total - 2.5:.2f}:d=2.5[aout]")
    fc = ";".join(parts)
    cmd += ["-filter_complex", fc, "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "19",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
            "-shortest", out]
    print(f"Durée prévue : {total:.1f} s — encodage…")
    subprocess.run(cmd, check=True)
    print("✔", out, os.path.getsize(out), "octets")

if __name__ == "__main__":
    main()
