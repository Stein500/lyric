#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Films « service » DSKY · WTBW — un film par occasion, 9:16.
Série laiton (mariage, anniversaire) : duotone chaud. Chaque film a son lit musical.
Usage : python3 film_service.py mariage [--stills 0,3]
"""
import subprocess
import sys

import imageio_ffmpeg
import numpy as np
from PIL import Image

sys.path.insert(0, "/home/user/lyric/productions/pub-wtbw")
sys.path.insert(0, "/home/user/lyric/productions/imelda-13-novembre")
import variations as V  # noqa: E402
import engine as E  # noqa: E402

FF = imageio_ffmpeg.get_ffmpeg_exe()
OUT = "/home/user/lyric/productions/pub-wtbw"
FPS = 30
W, H = 1080, 1920


def mariage():
    V.H = H
    P = V.photo
    cards = [
        V.center_card(P("srv-mariage", 0.44), [
            ("LE PLUS BEAU JOUR", "pf", 84),
            ("MÉRITE SA CHANSON.", "pfi", 84),
        ], "MARIAGE", "01", sub="ÉCRIT POUR VOUS DEUX", y=0.46, depth=0.55),
        V.center_card(P("var-danse", 0.50), [
            ("PREMIER REGARD.", "pf", 78),
            ("PREMIÈRE DANSE.", "pf", 78),
            ("PREMIÈRE CHANSON.", "pfi", 78),
        ], "SUR MESURE", "02", sub="LE PRÉNOM, LA DATE, L'HISTOIRE", y=0.47, depth=0.55),
        V.center_card(P("srv-event", 0.42), [
            ("LE MOMENT OÙ ELLE ENTRE,", "pf", 72),
            ("TOUT LE MONDE PLEURE.", "pfi", 72),
        ], "CÉRÉMONIE", "03", sub="C'EST LÀ QUE TA CHANSON PASSE", y=0.42, depth=0.5),
        V.center_card(P("var-guitare", 0.44), [
            ("TON NOM", "pf", 96),
            ("DANS LE REFRAIN.", "pfi", 96),
        ], "SUR MESURE", "04", sub="PAS UN TEXTE GÉNÉRIQUE. LE VÔTRE.", y=0.46, depth=0.58),
        V.center_card(V.charcoal(), [
            ("34 MORCEAUX ÉCRITS.", "pf", 80),
            ("LE VÔTRE SERA LE 35e.", "pfi", 80),
        ], "LE CATALOGUE", "05", sub="WOLOF TECHSTEIN BEAT WÊ", y=0.47),
        V.center_card(V.charcoal(), [
            ("TON MARIAGE MÉRITE", "pf", 82),
            ("SA CHANSON.", "pfi", 82),
        ], "DSKY · WTBW", "06", sub="TIKTOK & YOUTUBE — @DSKYWTBW", y=0.47),
    ]
    return cards, 20.0, f"{OUT}/cache/bed_mariage.m4a", "FILM-MARIAGE-9x16"


FILMS = {"mariage": mariage}


def build(name):
    cards, dur, audio, outname = FILMS[name]()
    base = [Image.fromarray((np.clip(np.clip(c, 0, 1), 0, 1) * 255 + 0.5).astype(np.uint8)) for c in cards]
    n = len(base)
    seg = dur / n
    xf = 0.34

    def frame_at(i, tl):
        p = min(1.0, max(0.0, tl / seg))
        s = 1.015 + 0.05 * p
        cw, ch = int(W / s), int(H / s)
        cx = (W - cw) // 2
        cy = int((H - ch) / 2 + (p - 0.5) * 10)
        im = base[i].crop((cx, cy, cx + cw, cy + ch)).resize((W, H), Image.BILINEAR)
        return np.asarray(im, dtype=np.float32) / 255.0

    def render(t):
        i = min(int(t // seg), n - 1)
        tl = t - i * seg
        f = frame_at(i, tl)
        if tl > seg - xf and i < n - 1:
            a = E.smoothstep((tl - (seg - xf)) / xf)
            f = f * (1 - a) + frame_at(i + 1, 0.0) * a
        f = E.clamp01(f + np.random.default_rng(int(t * FPS)).normal(0, 0.006, (H, W, 3)))
        if t < 0.5:
            f *= (0.35 + 0.65 * E.smoothstep(t / 0.5))
        if t > dur - 1.0:
            f *= 1 - 0.6 * E.smoothstep((t - (dur - 1.0)) / 1.0)
        return f

    out = f"{OUT}/livrables/{outname}.mp4"
    cmd = [FF, "-y", "-hide_banner", "-loglevel", "warning",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0",
           "-i", audio,
           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
           "-c:a", "copy", "-shortest", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    frames = int(round(dur * FPS))
    for k in range(frames):
        p.stdin.write((render(k / FPS) * 255 + 0.5).astype(np.uint8).tobytes())
        if k % 120 == 0:
            print(k, frames, flush=True)
    p.stdin.close()
    print("exit", p.wait(), out)


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "mariage"
    if "--stills" in sys.argv:
        cards, _, _, _ = FILMS[name]()
        for k, c in enumerate(cards):
            Image.fromarray((np.clip(c, 0, 1) * 255).astype(np.uint8)).save(f"{OUT}/stills/m{k}.jpg", quality=90)
        print("stills ok", len(cards))
    else:
        build(name)
