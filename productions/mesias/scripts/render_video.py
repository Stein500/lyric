# -*- coding: utf-8 -*-
"""Rendu vidéo MESÍAS — cadre 1080x1920, 30 i/s.

Principe « l'image vit, le mot reste net » :
  - le fond est agrandi UNE fois par plan, puis on fait glisser une fenêtre de
    recadrage (aucun redimensionnement par frame, aucune double exposition) ;
  - le lettrage (traduction FR) et le bandeau espagnol sont des calques RGBA
    précalculés par vers, collés à position fixe : jamais de flou ni de voile
    sur les mots.

Usage :
  python3 scripts/render_video.py --from 1 --to 12 --out out.mp4 [--audio master.mp3]
"""
import argparse, json, math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import render as R

FPS = 30
W, H = R.W, R.H
FF = imageio_ffmpeg.get_ffmpeg_exe()


def big_background(path, zoom=1.10):
    """Fond agrandi une seule fois ; la fenêtre de recadrage glisse dedans."""
    src = os.path.join(ASSETS_BASE, path)
    im = Image.open(src).convert("RGB").resize((int(W * zoom), int(H * zoom)), Image.LANCZOS)
    return im


ASSETS_BASE = os.path.join(ROOT, "work", "base")


def text_overlay(fr_text):
    """Calque RGBA de la traduction, précalculé pour un vers."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    info = R.bake_text(lay, fr_text)          # bake_text colore le calque
    return lay, info


def band_overlay(lines3):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    R.span_band(lay, lines3)
    return lay


def hud_overlay(m, v):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # badge
    mk = Image.new("L", (W, 200), 0)
    dm = ImageDraw.Draw(mk)
    dm.text((46, 46), m["artiste"].upper(), font=R.font(44), fill=255)
    dm.text((46, 100), "WTBW", font=R.font(34), fill=255)
    sh = mk.filter(ImageFilter.GaussianBlur(9)).point(lambda x: int(x * 0.85))
    lay.paste(Image.new("RGBA", (W, 200), (6, 8, 18, 255)), (0, 0), sh)
    dm2 = ImageDraw.Draw(lay)
    dm2.text((46, 46), m["artiste"].upper(), font=R.font(44), fill=(240, 236, 226, 255))
    dm2.text((46, 100), "WTBW", font=R.font(34), fill=(232, 163, 61, 255))
    dm2.line([(170, 186), (910, 186)], fill=(96, 102, 120, 200), width=2)
    return lay


def progress_overlay(p, y=186):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.line([(170, y), (170 + (910 - 170) * p, y)], fill=(232, 163, 61, 255), width=3)
    return lay


# quatre trajectoires de caméra douces et alternées
PATHS = [
    lambda k: (0.5 + 0.5 * math.sin(k * 2 * math.pi), 0.5 + 0.5 * math.cos(k * 2 * math.pi)),   # cercle
    lambda k: (1 - k, 0.35 + 0.65 * k),                                                        # diagonale
    lambda k: (k, 0.62 - 0.24 * math.sin(k * math.pi)),                                        # latéral
    lambda k: (0.72 + 0.22 * math.cos(k * 2 * math.pi), 0.72 + 0.22 * math.sin(k * 2 * math.pi)),
]


def camera_window(big, k, amp=0.06):
    """Fenêtre 1080x1920 glissant dans le fond agrandi ; jamais de bord découvert."""
    bw, bh = big.size
    sx, sy = bw - W, bh - H
    amp = min(amp, 1.0)
    # position normalisée dans [0,1] réduite à l'amplitude utile
    ux = 0.5 + (amp / 2) * (2 * (0.5 + 0.5 * math.sin(2 * math.pi * k)) - 1)
    uy = 0.5 + (amp / 2) * (2 * (0.5 + 0.5 * math.cos(2 * math.pi * k * 0.7)) - 1)
    x = int(max(0, min(sx, ux * sx)))
    y = int(max(0, min(sy, uy * sy)))
    return big.crop((x, y, x + W, y + H))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="i0", type=int, default=1)
    ap.add_argument("--to", dest="i1", type=int, default=12)
    ap.add_argument("--out", default=os.path.join(ROOT, "work", "maquette.mp4"))
    ap.add_argument("--audio", default=None)
    ap.add_argument("--crf", type=int, default=20)
    ap.add_argument("--start-offset", type=float, default=0.0)
    args = ap.parse_args()

    m = json.load(open(os.path.join(ROOT, "data", "verses_map.json"), encoding="utf8"))
    verses = m["verses"]
    sel = [v for v in verses if args.i0 <= v["i"] <= args.i1]
    t0 = sel[0]["debut_source"]
    t_end = sel[-1]["fin"] or (sel[-1]["debut_source"] + 4.0)

    # précalculs
    cache = {}
    for v in sel:
        img = v["image"]
        if img not in cache:
            cache[img] = big_background(img)
    text_lay = {}
    band_lay = {}
    for v in sel:
        text_lay[v["i"]] = text_overlay(v["traduction_fr"])[0]
        band_lay[v["i"]] = band_overlay(R.lines_until(verses, v["debut_source"]))

    frames = int(round((t_end - t0) * FPS))
    cmd = [FF, "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "pipe:0"]
    if args.audio:
        cmd += ["-ss", str(t0), "-t", str(t_end - t0), "-i", args.audio]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", str(args.crf),
            "-pix_fmt", "yuv420p", "-x264-params", "keyint=60:min-keyint=30",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
    if args.audio:
        cmd += ["-c:a", "aac", "-b:a", "256k", "-ar", "48000"]
    cmd += ["-movflags", "+faststart", args.out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    for f in range(frames):
        t = t0 + f / FPS
        v = None
        for cand in sel:
            if cand["debut_source"] <= t:
                v = cand
        if v is None:
            v = sel[0]
        k = ((t - v["debut_source"]) / max(0.4, (v["fin"] or v["debut_source"] + 3) - v["debut_source"]))
        bg = camera_window(cache[v["image"]], k % 1.0)
        frame = bg
        hud = hud_overlay(m, v)
        frame.paste(hud, (0, 0), hud)
        # bandeau espagnol : fondu de 0,35 s depuis l'état précédent
        bl = band_lay[v["i"]]
        frame.paste(bl, (0, 0), bl)
        frame.paste(text_lay[v["i"]], (0, 0), text_lay[v["i"]])
        pstd = (t - verses[0]["debut_source"]) / (verses[-1]["debut_source"] - verses[0]["debut_source"])
        pr = progress_overlay(max(0.0, min(1.0, pstd)))
        frame.paste(pr, (0, 0), pr)
        p.stdin.write(frame.tobytes())
        if f % 150 == 0:
            print(f"\r{f}/{frames}", end="", flush=True)
    p.stdin.close()
    p.wait()
    print(f"\n{args.out} — {frames} frames")


if __name__ == "__main__":
    main()
