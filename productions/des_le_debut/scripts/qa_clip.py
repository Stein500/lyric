#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QA du clip final — « Dès le début » (vérifications réelles, pas d'estimation)."""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LIVR = os.path.join(ROOT, "livrables")
WORK = os.path.join(HERE, "..", "work")
FFMPEG = os.environ.get("FFMPEG", "/tmp/lyric-venv/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2")
CLIP = os.path.join(LIVR, "Des_le_debut_9x16.mp4")

def run(args, capture=True):
    return subprocess.run(args, capture_output=capture, text=True)

def probe(path):
    p = run([FFMPEG, "-hide_banner", "-i", path])
    info = {"durée": None, "flux": []}
    for line in p.stderr.splitlines():
        if "Duration:" in line:
            d = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = d.split(":")
            info["durée"] = round(int(h) * 3600 + int(m) * 60 + float(s), 3)
        if "Stream #" in line:
            info["flux"].append(line.split("Stream #")[1].strip())
    return info

def main():
    os.makedirs(WORK, exist_ok=True)
    rep = {"clip": os.path.basename(CLIP)}
    info = probe(CLIP)
    rep["duree_s"] = info["durée"]
    rep["flux"] = info["flux"]
    # frames comptées
    p = run([FFMPEG, "-v", "error", "-i", CLIP, "-map", "0:v:0", "-f", "null", "-"])
    # blackdetect + freezedetect
    p = run([FFMPEG, "-hide_banner", "-i", CLIP, "-vf",
             "blackdetect=d=0.15:pix_th=0.06,freezedetect=n=-70dB:d=2.5", "-an", "-f", "null", "-"])
    blacks, freezes = [], []
    for line in p.stderr.splitlines():
        if "black_start" in line:
            blacks.append(line.strip())
        if "freeze_start" in line:
            freezes.append(line.strip())
    rep["frames_noires"] = blacks
    rep["gels"] = freezes
    # images de contrôle aux moments clés (clochettes, vers, endcard)
    t_hook = 6.85
    checks = {
        "01_intro_clochettes": 2.0,
        "02_debut_chanson": 8.0,
        "03_clochettes_2": 22.56,
        "04_clochettes_3": 105.85 + t_hook,
        "05_clochettes_4": 130.73 + t_hook,
        "06_endcard": t_hook + 199.99 + 1.5,
    }
    frames = {}
    for name, t in checks.items():
        out = os.path.join(WORK, f"qa_{name}.jpg")
        run([FFMPEG, "-v", "error", "-y", "-ss", str(t), "-i", CLIP, "-frames:v", "1", out])
        frames[name] = out
    # planche
    ims = [(k, Image.open(v).convert("RGB")) for k, v in frames.items() if os.path.exists(v)]
    th = 460
    ims = [(k, im.resize((int(im.width * th / im.height), th), Image.LANCZOS)) for k, im in ims]
    W = sum(im.width for _, im in ims) + 20 * (len(ims) + 1)
    c = Image.new("RGB", (W, th + 96), (12, 12, 16))
    d = ImageDraw.Draw(c)
    f = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", s)
    d.text((20, 16), "QA « Dès le début » — moments clés du clip final", font=f(26), fill=(255, 196, 78))
    d.text((20, 50), f"durée {rep['duree_s']} s · frames noires : {len(blacks)} · gels : {len(freezes)}",
           font=f(18), fill=(200, 200, 210))
    x = 20
    for k, im in ims:
        c.paste(im, (x, 84)); d.rectangle([x, 84, x + im.width, 84 + th], outline=(80, 80, 90))
        d.text((x + im.width // 2, 84 + th + 10), k, font=f(15), fill=(235, 235, 235), anchor="ma")
        x += im.width + 20
    qa = os.path.join(WORK, "qa_clip_9x16.jpg")
    c.save(qa, quality=90)
    rep["planche_qa"] = qa
    rep["resultat"] = "OK" if (not blacks and not freezes and abs((rep["duree_s"] or 0) - 211.84) < 0.3) else "À VÉRIFIER"
    json.dump(rep, open(os.path.join(WORK, "qa_clip_9x16.json"), "w"), ensure_ascii=False, indent=2)
    print(json.dumps({k: v for k, v in rep.items() if k != "flux"}, ensure_ascii=False, indent=2))
    for f_ in rep["flux"]:
        print("  flux:", f_)

if __name__ == "__main__":
    main()
