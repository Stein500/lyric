#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Films « universels » 9:16 — CITATIONS (20 s) et SERVICES (13 s).
Aucun visage imposé. Zoom lent, fondu enchaîné 0,3 s, grain léger, lit musical du catalogue.
"""
import json
import math
import subprocess
import sys

import imageio_ffmpeg
import numpy as np
from PIL import Image

sys.path.insert(0, "/home/user/lyric/productions/pub-wtbw")
sys.path.insert(0, "/home/user/lyric/productions/imelda-13-novembre")
import universel as U  # noqa: E402
import engine as E  # noqa: E402
import logo as L  # noqa: E402

FF = imageio_ffmpeg.get_ffmpeg_exe()
OUT = "/home/user/lyric/productions/pub-wtbw"
FPS = 30
W, H = 1080, 1920
MODE = "services" if "--services" in sys.argv else "citations"


def manifesto():
    f = U.charcoal()
    U.chrome(f, "MANIFESTE", None)
    blk = L.type_block(int(W * 0.70))
    U.put(f, blk, (W - blk.shape[1]) // 2, 470, 1.0, 1.0)
    U.rule(f, 1420, 160)
    a, _ = U.fit("POUR TOUT LE MONDE.", "pfi", 54, 0.03, maxw=0.86)
    U.put(f, a, 0, 1470, 1.0, 0.95)
    a2, _ = U.fit("COMME UNE CHANSON.", "pfi", 54, 0.03, maxw=0.86)
    U.put(f, a2, 0, 1542, 1.0, 0.95)
    return f


def cards():
    U.H = H            # les cartes sont calculées en 9:16
    if MODE == "services":
        seq = [
            (U.photo("uni-phone.jpg", dark=0.46), [("TON MORCEAU", "pf", 116, 0.03),
                                                   ("TON CLIP 9:16", "pfi", 116, 0.03)],
             "SERVICES", "ÉCRIT · COMPOSÉ · ENREGISTRÉ · FILMÉ", 0.42),
            (U.photo("uni-studio.jpg", dark=0.46), [("TON HISTOIRE", "pf", 112, 0.03),
                                                    ("DANS TA POCHE.", "pfi", 112, 0.03)],
             "SUR MESURE", "UN MORCEAU QUI T'APPARTIENT", 0.42),
            (U.photo("uni-memoire.jpg", dark=0.46), [("ON NE CHOISIT PAS SA MÉMOIRE.", "pf", 84, 0.02),
                                                     ("ON CHOISIT SA CHANSON.", "pfi", 84, 0.02)],
             "MÉMOIRE", "POUR CEUX QUI RESTENT", 0.44),
            (U.photo("uni-hands.jpg", dark=0.52), [("FÊTE. CÉLÉBRATION.", "pf", 96, 0.03),
                                                   ("ANNIVERSAIRE.", "pfi", 96, 0.03)],
             "TES MOMENTS", "TOUT CE QUI SE FÊTE", 0.44),
        ]
        out = []
        for bg, lines, kicker, sub, y in seq:
            f, _ = U.quote_card(bg, lines, kicker, None, sub=sub, y=y)
            out.append(f)
        out.append(manifesto())
        return out
    seq = [
        (U.photo("uni-wall.jpg", dark=0.30), [("TOUT LE MONDE A UNE HISTOIRE.", "pf", 92, 0.02),
                                              ("PEU DE GENS ONT SON MORCEAU.", "pf", 92, 0.02)],
         "CITATIONS", "DSKY · WTBW", 0.46),
        (U.photo("uni-memoire.jpg", dark=0.46), [("ON NE CHOISIT PAS SA MÉMOIRE.", "pf", 86, 0.02),
                                                 ("ON CHOISIT SA CHANSON.", "pfi", 86, 0.02)],
         "MÉMOIRE", "POUR CEUX QUI RESTENT", 0.44),
        (U.photo("uni-hands.jpg", dark=0.52), [("LA MUSIQUE NE DEMANDE PAS TON NOM.", "pf", 82, 0.02),
                                               ("ELLE DEMANDE TON CŒUR.", "pfi", 82, 0.02)],
         "FÊTE", "DSKY · WTBW", 0.44),
        (U.photo("uni-silhouette.jpg", dark=0.58), [("HOMME. FEMME. ENFANT.", "pf", 96, 0.04),
                                                    ("LA MÊME ÉMOTION.", "pfi", 96, 0.04)],
         "UNIVERSEL", "UNE CHANSON POUR CHACUN", 0.27),
        (U.photo("uni-hands.jpg", dark=0.48, zoom=1.25), [("8 ANS OU 80 ANS.", "pf", 100, 0.03),
                                                          ("LE MÊME FRISSON.", "pfi", 100, 0.03)],
         "UNIVERSEL", "DE LA PREMIÈRE FÊTE À LA DERNIÈRE", 0.44),
        (U.photo("uni-phone.jpg", dark=0.46), [("TON MORCEAU", "pf", 116, 0.03),
                                               ("TON CLIP 9:16", "pfi", 116, 0.03)],
         "SERVICES", "ÉCRIT · COMPOSÉ · ENREGISTRÉ · FILMÉ", 0.42),
        (U.photo("uni-studio.jpg", dark=0.46), [("TON HISTOIRE", "pf", 112, 0.03),
                                                ("DANS TA POCHE.", "pfi", 112, 0.03)],
         "SUR MESURE", "UN MORCEAU QUI T'APPARTIENT", 0.42),
    ]
    out = []
    for bg, lines, kicker, sub, y in seq:
        f, _ = U.quote_card(bg, lines, kicker, None, sub=sub, y=y)
        out.append(f)
    out.append(manifesto())
    return out


def build():
    base = [Image.fromarray((np.clip(c, 0, 1) * 255 + 0.5).astype(np.uint8)) for c in cards()]
    n = len(base)
    dur = 20.4 if MODE == "citations" else 13.0
    seg = dur / n
    xf = 0.32

    def frame_at(i, tl, scale_hint=0.0):
        p = min(1.0, max(0.0, (tl + scale_hint) / seg))
        s = 1.015 + 0.045 * p
        cw, ch = int(W / s), int(H / s)
        cx = (W - cw) // 2
        cy = int((H - ch) / 2 + (p - 0.5) * 12)
        im = base[i].crop((cx, cy, cx + cw, cy + ch)).resize((W, H), Image.BILINEAR)
        return np.asarray(im, dtype=np.float32) / 255.0

    def render(t):
        i = min(int(t // seg), n - 1)
        tl = t - i * seg
        f = frame_at(i, tl)
        if tl > seg - xf and i < n - 1:
            a = E.smoothstep((tl - (seg - xf)) / xf)
            f = f * (1 - a) + frame_at(i + 1, 0.0) * a
        f = E.clamp01(f + np.random.default_rng(int(t * FPS)).normal(0, 0.0075, (H, W)))
        if t < 0.5:
            f *= 0.35 + 0.65 * E.smoothstep(t / 0.5)
        if t > dur - 1.0:
            f *= 1 - 0.55 * E.smoothstep((t - (dur - 1.0)) / 1.0)
        return f

    name = "FILM-CITATIONS-9x16" if MODE == "citations" else "FILM-SERVICES-9x16"
    out = f"{OUT}/livrables/{name}.mp4"
    cmd = [FF, "-y", "-hide_banner", "-loglevel", "warning",
           "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0",
           "-i", f"{OUT}/cache/bed.m4a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
           "-c:a", "copy", "-shortest", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    frames = int(round(dur * FPS))
    for k in range(frames):
        p.stdin.write((render(k / FPS) * 255 + 0.5).astype(np.uint8).tobytes())
        if k % 150 == 0:
            print(k, frames, flush=True)
    p.stdin.close()
    print("exit", p.wait(), out)


if __name__ == "__main__":
    if "--stills" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--stills") + 1].split(",")]
        b = [Image.fromarray((np.clip(c, 0, 1) * 255 + 0.5).astype(np.uint8)) for c in cards()]
        for k, t in enumerate(ts):
            b[min(k, len(b) - 1)].resize((W, H), Image.LANCZOS).save(f"{OUT}/stills/u{k:02d}.jpg", quality=90)
        print("stills ok")
    else:
        build()
