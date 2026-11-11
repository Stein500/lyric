#!/usr/bin/env python3
"""qc_video.py — contrôles §12 du rendu final + planche CONTROLE-mp4-final.jpg."""
import os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
FF = "/usr/local/lib/python3.13/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v9.0.2"
VID = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "livrables", "MONSTER-POSITIVE-Daïsky-9x16.mp4")
rep = {}

def run(args):
    return subprocess.run([FF] + args, capture_output=True, text=True).stderr

# durée / frames
info = run(["-hide_banner", "-i", VID])
m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info)
dur = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
m2 = re.search(r"Stream #0:0.*?(\d+) fps", info)
fps = float(m2.group(1)) if m2 else 30.0
rep["durée"] = f"{dur:.2f} s ({fps} fps)"

# blackdetect
bd = run(["-hide_banner", "-i", VID, "-vf", "blackdetect=d=0.05:pix_th=0.10", "-f", "null", "-"])
n_black = len(re.findall(r"black_start", bd))
bd2 = run(["-hide_banner", "-i", VID, "-vf", "blackdetect=d=0.05:pix_th=0.98", "-f", "null", "-"])
n_black98 = len(re.findall(r"black_start", bd2))
rep["frames noires (pix_th 0.10 / 0.98)"] = f"{n_black} / {n_black98}"

# freezedetect
fd = run(["-hide_banner", "-i", VID, "-vf", "freezedetect=n=-33dB:d=2.5", "-f", "null", "-"])
fz = re.findall(r"freeze_start:([\d.]+)", fd)
rep["gels >= 2.5 s (freezedetect -33dB)"] = str(len(fz)) + (f" @ {fz[:6]}" if fz else "")

# loudness
lb = run(["-hide_banner", "-i", VID, "-map", "0:a:0", "-af", "ebur128", "-f", "null", "-"])
mi = re.findall(r"I:\s+(-?[\d.]+) LUFS", lb)[-1:] and re.search(r"I:\s+(-?[\d.]+) LUFS", lb.split("Summary")[-1])
mlra = re.search(r"LRA:\s+(-?[\d.]+) LU", lb.split("Summary")[-1])
rep["loudness"] = f"I={mi.group(1) if mi else '?'} LUFS, LRA={mlra.group(1) if mlra else '?'} LU"

# crête
st = run(["-hide_banner", "-i", VID, "-map", "0:a:0", "-af", "astats=metadata=1", "-f", "null", "-"])
pk = re.findall(r"Peak level dB: (-?[\d.]+)", st)
rep["crête (dBTP approx)"] = f"{max(float(x) for x in pk):.2f} dB" if pk else "?"

# faststart : ordre des atomes
with open(VID, "rb") as f:
    head = f.read(200000)
moov = head.find(b"moov"); mdat = head.find(b"mdat"); ftyp = head.find(b"ftyp")
ok = (-1 < ftyp < moov) and (mdat == -1 or moov < mdat)
rep["faststart (ftyp puis moov avant mdat)"] = f"ftyp@{ftyp} moov@{moov} mdat@{mdat} -> {'OK' if ok else 'KO'}"

# taille
rep["taille fichier"] = f"{os.path.getsize(VID)/1e6:.1f} Mo"

print("=" * 60)
for k, v in rep.items():
    print(f"{k:42s} {v}")
print("=" * 60)
with open(os.path.join(ROOT, "livrables", "CONTROLES.txt"), "w") as f:
    for k, v in rep.items():
        f.write(f"{k}: {v}\n")

# planche CONTROLE-mp4-final.jpg : 12 frames réparties
tmp = os.path.join(ROOT, "livrables", "_frames")
os.makedirs(tmp, exist_ok=True)
for i, t in enumerate(np.linspace(1.0, dur - 1.0, 12)):
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", VID,
                    "-frames:v", "1", os.path.join(tmp, f"f{i:02d}.png")], capture_output=True)
tiles = []
for i in range(12):
    p = os.path.join(tmp, f"f{i:02d}.png")
    if os.path.exists(p):
        tiles.append((f"t={np.linspace(1.0, dur-1.0, 12)[i]:.0f}s", Image.open(p).convert("RGB")))
TW = 360
cols = 4
rows = (len(tiles) + cols - 1) // cols
th = int(H_ratio := 640)
sheet = Image.new("RGB", (cols * TW, rows * (th + 20)), (18, 18, 22))
d = ImageDraw.Draw(sheet)
for idx, (name, im) in enumerate(tiles):
    im = im.resize((TW, th), Image.LANCZOS)
    x = (idx % cols) * TW; y = (idx // cols) * (th + 20)
    sheet.paste(im, (x, y + 18)); d.text((x + 4, y + 3), name, fill=(255, 232, 168))
sheet.save(os.path.join(ROOT, "livrables", "CONTROLE-mp4-final.jpg"), quality=88)
print("CONTROLE-mp4-final.jpg écrite")
