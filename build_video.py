#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vidéo TikTok 1080x1920 PLEIN ÉCRAN à partir des bases 100 % IA.
Usage : python3 build_video.py <début> <fin> "THÈME"
Chaque image est mise en avant plein cadre (cover 1080x1920, zoom Ken Burns doux
alterné in/out), fondus xfade, badge « DSKY WTBW » doré CLIGNOTANT en bas
(il recouvre la signature gravée), musique assets/musique-douce.mp3.
Les images doivent être générées avec le texte dans la bande verticale centrale.
"""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
GOLD = (212, 162, 76, 255)

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
    sh = Image.new("RGBA", canvas, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((x + 2, y + 3), text, font=font, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(2))
    img.alpha_composite(sh)
    d.text((x, y), text, font=font, fill=fill)
    return img

def main():
    n1, n2, theme = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    nums = list(range(n1, n2 + 1))
    work = f"videos/work-{n1}-{n2}"
    os.makedirs(work, exist_ok=True)
    os.makedirs("videos", exist_ok=True)
    out = f"videos/video-{n1}-{n2}-{theme.lower()}.mp4"
    D, FPS = 96, 30
    DUR = D / FPS

    # badge clignotant (1,2 s @30, boucle parfaite) + plaque sombre qui masque
    # la signature gravée (dégradé vertical -> aucun bord visible)
    frames, badge_seq = 36, f"{work}/badge-blink.mov"
    f_badge = ImageFont.truetype(SERIF, 38)
    plate = Image.new("RGBA", (1080, 150), (16, 12, 9, 0))
    pa = plate.load()
    for y in range(150):
        a = int(250 * min(1.0, max(0.0, (y - 15) / 40)))
        for x in range(1080):
            pa[x, y] = (16, 12, 9, a)
    plate.save(f"{work}/plate.png")
    for k in range(frames):
        a = 0.30 + 0.60 * (0.5 + 0.5 * math.sin(2 * math.pi * k / frames - math.pi / 2))
        img = text_img("D S K Y   W T B W", f_badge, GOLD[:3] + (int(255 * a),),
                       (1080, 160), glow=GOLD[:3] + (int(140 * a),))
        img.save(f"{work}/badge-{k:02d}.png")
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error",
                    "-framerate", str(FPS), "-i", f"{work}/badge-%02d.png",
                    "-frames:v", str(frames), "-c:v", "png", "-pix_fmt", "rgba",
                    badge_seq], check=True)

    # inputs : N images + badge + musique
    cmd = [FF, "-y", "-hide_banner", "-loglevel", "error"]
    for n in nums:
        cmd += ["-i", f"assets/bases/base-{n}.jpg"]
    cmd += ["-stream_loop", "-1", "-i", badge_seq]
    cmd += ["-i", f"{work}/plate.png"]
    cmd += ["-i", "assets/musique-douce.mp3"]
    BADGE, PLATE, MUS = len(nums), len(nums) + 1, len(nums) + 2

    parts = []
    for i in range(len(nums)):
        z = ("min(1+0.0003*on,1.03)" if i % 2 == 0
             else "max(1.03-0.0003*on,1.0)")
        parts.append(
            f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,"
            f"crop=1080:1920,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":d={D}:s=1080x1920:fps={FPS},format=yuv420p,settb=AVTB[v{i}]")
    prev = "v0"
    for k in range(1, len(nums)):
        off = round(k * (DUR - 0.7), 2)
        lab = f"x{k}"
        parts.append(f"[{prev}][v{k}]xfade=transition=fade:duration=0.7:offset={off}[{lab}]")
        prev = lab
    total = (len(nums) - 1) * (DUR - 0.7) + DUR
    parts.append(f"[{prev}][{PLATE}:v]overlay=0:1770[bpl];"
                 f"[bpl][{BADGE}:v]overlay=0:1766"
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
    print(f"Durée prévue : {total:.1f} s — encodage plein écran…")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("STDERR:", r.stderr[-1200:]); sys.exit(1)
    print("✔", out, os.path.getsize(out), "octets")

if __name__ == "__main__":
    main()
