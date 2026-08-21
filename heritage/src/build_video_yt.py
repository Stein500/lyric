#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_video_yt.py — Montage YouTube 16:9 1920×1080 (miroir de la version verticale).
Mêmes segments/timings que manifest.json ; images = assets/images/paysage/<même nom>.
Ken Burns ±4 % + xfade 0,8 s centré + sous-titres lyrics_yt.ass (polices variées).
Sortie : livrables/Heritage_DaiskyPro_Lyrics_16x9_YT.mp4
"""
import json, os, subprocess, sys
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_MP4 = os.path.join(ROOT, "livrables", "Heritage_DaiskyPro_Lyrics_16x9_YT.mp4")

with open(os.path.join(ROOT, "manifest.json"), encoding="utf-8") as fp:
    M = json.load(fp)

SEG = M["segments"]; FPS = 30
W, H = 1920, 1080
F = float(M["fondu_entre_segments_s"]); DUR = float(M["duree_audio_s"])
MP3 = "/home/user/lyric/Héritage de mes parents-Daïsky.mp3"
ASS = os.path.join(ROOT, "lyrics_yt.ass")
FONTDIR = "/usr/share/fonts/truetype/dejavu"

lens = [s["fin"] - s["debut"] for s in SEG]
n = len(SEG)
draws = [l + F for l in lens[:-1]] + [lens[-1] + F / 2]
offsets, acc = [], 0.0
for k in range(n - 1):
    acc += lens[k]; offsets.append(acc - F / 2)

inputs, filters = [], []
for i, s in enumerate(SEG):
    img = os.path.join(ROOT, "assets", "images", "paysage", os.path.basename(s["image"]))
    inputs += ["-loop", "1", "-framerate", str(FPS), "-i", img]
    frames = draws[i] * FPS
    r = 0.04 / frames
    z = f"1+{r:.8f}*on" if s["ken_burns"] == "in" else f"1.04-{r:.8f}*on"
    filters.append(
        f"[{i}:v]format=rgb24,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":d=1:s={W}x{H}:fps={FPS},format=yuv420p,setsar=1[v{i}]"
    )
cur = "v0"
for k in range(1, n):
    out = f"x{k}"
    filters.append(f"[{cur}][v{k}]xfade=transition=fade:duration={F}:offset={offsets[k-1]:.3f}[{out}]")
    cur = out
filters.append(f"[{cur}]subtitles='{ASS}':fontsdir={FONTDIR},format=yuv420p,setsar=1[vfinal]")

cmd = [FFMPEG, "-y", *inputs, "-i", MP3,
       "-filter_complex", ";".join(filters),
       "-map", "[vfinal]", "-map", f"{n}:a",
       "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000", "-ar", "48000",
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", str(FPS),
       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
       "-t", f"{DUR:.2f}", OUT_MP4]
print("Encodage YouTube 16:9 en cours…", flush=True)
log = open(os.path.join(ROOT, "livrables", "build_yt.log"), "w")
sys.exit(subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT).wait())
