#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_video.py — Montage de la vidéo lyrics verticale 9:16.
Ken Burns léger par segment + fondus enchaînés xfade (0,8 s) + sous-titres ASS brûlés.
Sortie : out/Heritage_DaiskyPro_Lyrics_9x16.mp4 (durée = MP3 source).
"""
import json, os, shutil, subprocess, sys
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_MP4 = os.path.join(ROOT, "livrables", "Heritage_DaiskyPro_Lyrics_9x16.mp4")

with open(os.path.join(ROOT, "manifest.json"), encoding="utf-8") as fp:
    M = json.load(fp)

SEG = M["segments"]
FPS = M["format"]["fps"]
W, H = M["format"]["largeur"], M["format"]["hauteur"]
F = float(M["fondu_entre_segments_s"])
DUR = float(M["duree_audio_s"])
MP3 = os.path.join(ROOT, M["audio_source"])
if not os.path.exists(MP3):  # tolérance chemin relatif
    MP3 = os.path.join(os.path.dirname(ROOT), os.path.basename(M["audio_source"]))
ASS = os.path.join(ROOT, "lyrics.ass")
FONTDIR = "/usr/share/fonts/truetype/dejavu"

lens = [s["fin"] - s["debut"] for s in SEG]
n = len(SEG)
# durées brutes de chaque flux (crossfade de F s entre segments, centré sur la frontière)
draws = [l + F for l in lens[:-1]] + [lens[-1] + F / 2]
# offsets xfade (début de chaque transition)
offsets = []
acc = 0.0
for k in range(n - 1):
    acc += lens[k]
    offsets.append(acc - F / 2)

inputs, filters = [], []
for i, s in enumerate(SEG):
    img = os.path.join(ROOT, s["image"])
    inputs += ["-loop", "1", "-framerate", str(FPS), "-i", img]
    frames = draws[i] * FPS
    r = 0.05 / frames
    if s["ken_burns"] == "in":
        z = f"1+{r:.8f}*on"
    else:
        z = f"1.05-{r:.8f}*on"
    filters.append(
        f"[{i}:v]format=rgb24,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":d=1:s={W}x{H}:fps={FPS},format=yuv420p,setsar=1[v{i}]"
    )

cur = "v0"
for k in range(1, n):
    out = f"x{k}"
    filters.append(
        f"[{cur}][v{k}]xfade=transition=fade:duration={F}:offset={offsets[k-1]:.3f}[{out}]"
    )
    cur = out

filters.append(
    f"[{cur}]subtitles='{ASS}':fontsdir={FONTDIR},format=yuv420p,setsar=1[vfinal]"
)

cmd = [FFMPEG, "-y", *inputs, "-i", MP3,
       "-filter_complex", ";".join(filters),
       "-map", "[vfinal]", "-map", f"{n}:a",
       "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000",
       "-ar", "48000",
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
       "-r", str(FPS), "-c:a", "aac", "-b:a", "192k",
       "-movflags", "+faststart", "-t", f"{DUR:.2f}", OUT_MP4]

print(" ".join(cmd)[:600], "…", flush=True)
log = open(os.path.join(ROOT, "livrables", "build.log"), "w")
proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
print("Encodage en cours (log: out/build.log)…", flush=True)
sys.exit(proc.wait())
