#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_reel2.py — REEL viral n°2 (extrait 1:40 → 2:14 = 34,0 s).
Coups secs + zoom punch. Sortie : livrables/Reel2_Heritage_MamanPapa_9x16.mp4
"""
import os, subprocess, sys
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "livrables", "Reel2_Heritage_MamanPapa_9x16.mp4")

FPS, W, H = 30, 1080, 1920
AUDIO_START, DUR = 100.0, 34.0
MP3 = "/home/user/lyric/Héritage de mes parents-Daïsky.mp3"
ASS = os.path.join(ROOT, "reel2.ass")
FONTDIR = "/usr/share/fonts/truetype/dejavu"
DOSSIER = "reel2"

SEG = [
    ("r201_maman_etudes", 0.0,  3.0),
    ("r202_papa_pays",    3.0,  5.0),
    ("r203_annees",       5.0,  8.0),
    ("r204_abri",         8.0, 10.8),
    ("r205_debout",      10.8, 13.0),
    ("r206_pas",         13.0, 16.0),
    ("r207_jamais",      16.0, 19.0),
    ("r208_heritage",    19.0, 21.0),
    ("r209_dos",         21.0, 26.0),
    ("r210_envol",       26.0, 34.0),
]

inputs, filters, labels = [], [], []
for i, (n, d0, d1) in enumerate(SEG):
    img = os.path.join(ROOT, "assets", "images", DOSSIER, n + ".jpg")
    inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d1-d0:.3f}", "-i", img]
    frames = (d1 - d0) * FPS
    r = 0.10 / frames
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
print("Encodage REEL 2 en cours…", flush=True)
log = open(os.path.join(ROOT, "livrables", "build_reel2.log"), "w")
sys.exit(subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT).wait())
