#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_reel.py — REEL viral 9:16 (extrait 0:43 → 1:16.8 = 33,8 s).
Coups secs (hard cuts) au rythme des punchlines + zoom punch par image.
Sortie : livrables/Reel_Heritage_Viral_9x16.mp4
"""
import os, subprocess, sys
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "livrables", "Reel_Heritage_Viral_9x16.mp4")

FPS, W, H = 30, 1080, 1920
AUDIO_START, DUR = 43.0, 33.8
MP3 = "/home/user/lyric/Héritage de mes parents-Daïsky.mp3"
ASS = os.path.join(ROOT, "reel.ass")
FONTDIR = "/usr/share/fonts/truetype/dejavu"

SEG = [  # (fichier, debut_relatif, fin) — coup sec à chaque punchline
    ("r01_pere",   0.0,  3.0),
    ("r02_mains",  3.0,  5.0),
    ("r03_mere",   5.0,  7.8),
    ("r04_sel",    7.8, 10.0),
    ("r05_reves", 10.0, 13.0),
    ("r06_poings",13.0, 16.0),
    ("r07_chance",16.0, 18.0),
    ("r08_fier",  18.0, 21.0),
    ("r09_coeur", 21.0, 24.0),
    ("r10_ciel",  24.0, 33.8),
]

inputs, filters, labels = [], [], []
for i, (n, d0, d1) in enumerate(SEG):
    img = os.path.join(ROOT, "assets", "images", "reel", n + ".jpg")
    inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d1-d0:.3f}", "-i", img]
    frames = (d1 - d0) * FPS
    r = 0.10 / frames  # zoom punch rapide (style reel)
    filters.append(
        f"[{i}:v]format=rgb24,zoompan=z='1+{r:.8f}*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":d=1:s={W}x{H}:fps={FPS},format=yuv420p,setsar=1[v{i}]"
    )
    labels.append(f"[v{i}]")

filters.append("".join(labels) + f"concat=n={len(SEG)}:v=1:a=0,subtitles='{ASS}':fontsdir={FONTDIR},format=yuv420p,setsar=1[vf]")

cmd = [FFMPEG, "-y", *inputs,
       "-ss", str(AUDIO_START), "-t", str(DUR), "-i", MP3,
       "-filter_complex", ";".join(filters),
       "-map", "[vf]", "-map", f"{len(SEG)}:a",
       "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000", "-ar", "48000",
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", str(FPS),
       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
       "-t", f"{DUR:.2f}", OUT]
print("Encodage REEL en cours…", flush=True)
log = open(os.path.join(ROOT, "livrables", "build_reel.log"), "w")
sys.exit(subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT).wait())
