#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FILM CATALOGUE 9:16 — les 34 pochettes une par une, calées sur le montage audio.
Sortie : livrables/FILM-CATALOGUE-34-9x16.mp4  (1080x1920, 30 fps, audio = cache/pub.m4a)
Usage : python3 film_catalogue.py [--stills]
"""
import glob
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, "/home/user/lyric/productions/imelda-13-novembre")
sys.path.insert(0, "/home/user/lyric/productions/pub-wtbw")
import engine as E  # noqa: E402
from covers import ALL  # noqa: E402

OUT = "/home/user/lyric/productions/pub-wtbw"
POC = f"{OUT}/livrables/pochettes/catalogue"
LIV = f"{OUT}/livrables"
FF = __import__("imageio_ffmpeg").get_ffmpeg_exe()

W, H, FPS = 1080, 1920, 30
DUR = 28.86
INTRO, OUTRO = 1.5, 1.5
SEG = (DUR - INTRO - OUTRO) / len(ALL)

SH = np.array([0.055, 0.043, 0.030], dtype=np.float32)
ACC = np.array([0.784, 0.631, 0.420], dtype=np.float32)
INK = np.array([0.965, 0.940, 0.890], dtype=np.float32)


def base():
    f = np.ones((H, W, 3), dtype=np.float32) * SH
    yy = np.linspace(-1, 1, H, dtype=np.float32)[:, None]
    xx = np.linspace(-1, 1, W, dtype=np.float32)[None, :]
    r = np.sqrt(xx ** 2 + yy ** 2) / 1.42
    f *= (1.0 - 0.55 * r ** 1.6)[..., None]
    return f


BG = base()


def text(txt, kind, size, track_r=0.16, maxw=0.80, color=INK, op=1.0):
    s = size
    while s > 12:
        fnt = E.font(kind, s)
        if E.tracked_width(fnt, txt, s * track_r) <= W * maxw:
            break
        s = int(s * 0.95)
    fnt = E.font(kind, s)
    im = Image.new("L", (W, int(s * 1.6)), 0)
    d = ImageDraw.Draw(im)
    tw = E.tracked_width(fnt, txt, s * track_r)
    E.draw_tracked(d, ((W - tw) / 2, s * 0.9), txt, fnt, s * track_r, fill=255)
    a = np.asarray(im, dtype=np.float32) / 255.0
    return a * op, color


def blit(f, a, color, y):
    h, w = a.shape
    ya, yb = max(0, int(y)), min(H, int(y) + h)
    if ya >= yb:
        return
    sub = (a[ya - int(y):yb - int(y)])[..., None]
    f[ya:yb] = f[ya:yb] * (1 - sub) + np.array(color, dtype=np.float32) * sub


def cover_thumb(path, box=860):
    im = Image.open(path).convert("RGB").resize((box, box), Image.LANCZOS)
    return np.asarray(im, dtype=np.float32) / 255.0


def frame_card(i, title, path):
    f = BG.copy()
    box, x0, y0 = 860, (W - 860) // 2, 360
    # ombre
    sh = np.zeros((H, W), dtype=np.float32)
    sh[y0 + 14:y0 + box + 14, x0 + 10:x0 + box + 10] = 0.55
    sh = np.asarray(Image.fromarray((sh * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(26)), dtype=np.float32) / 255.0
    f *= (1 - sh[..., None] * 0.8)
    f[y0:y0 + box, x0:x0 + box] = cover_thumb(path)
    # filet
    f[y0 - 1:y0 + box + 1, x0 - 1:x0] = ACC * 0.5
    f[y0 - 1:y0 + box + 1, x0 + box:x0 + box + 1] = ACC * 0.5

    a, c = text(f"{i:02d} / {len(ALL)}", "m", 24, 0.34, 0.4, ACC, 0.85)
    blit(f, a, c, 190)
    a, c = text("CATALOGUE", "m", 22, 0.42, 0.4, INK, 0.45)
    blit(f, a, c, 110)

    a, c = text(title, "pf", 74, 0.10, 0.84)
    blit(f, a, c, 1310)
    f[1436:1438, (W - 150) // 2:(W + 150) // 2] = ACC * 0.55
    a, c = text("DSKY · WTBW", "m", 22, 0.40, 0.4, ACC, 0.80)
    blit(f, a, c, 1470)
    from logo import sigil
    g = sigil(64)
    put_sig(f, g, (W - 64) // 2, 1746)
    return f


def put_sig(f, a, x, y):
    h, w = a.shape
    sub = a[..., None]
    f[y:y + h, x:x + w] = f[y:y + h, x:x + w] * (1 - sub) + ACC * sub


def frame_intro(inp):
    from logo import sigil
    f = BG.copy()
    if inp:
        a, c = text("LE CATALOGUE", "m", 24, 0.44, 0.5, ACC, 0.85)
        blit(f, a, c, 700)
        a, c = text("34", "pf", 360, 0.02, 0.62)
        blit(f, a, c, 760)
        a, c = text("MORCEAUX", "pfi", 66, 0.26, 0.7)
        blit(f, a, c, 1180)
        a, c = text("ÉCRITS · COMPOSÉS · MIXÉS", "m", 24, 0.30, 0.7, INK, 0.55)
        blit(f, a, c, 1300)
    else:
        a, c = text("TOUT EST LÀ.", "pf", 96, 0.06, 0.8)
        blit(f, a, c, 820)
        a, c = text("@DSKYWTBW", "m", 30, 0.34, 0.6, ACC, 0.9)
        blit(f, a, c, 1010)
        a, c = text("TIKTOK · YOUTUBE · WHATSAPP", "m", 20, 0.30, 0.7, INK, 0.4)
        blit(f, a, c, 1090)
    put_sig(f, sigil(64), (W - 64) // 2, 1746)
    return f


def build():
    paths = sorted(glob.glob(f"{POC}/*.jpg"))
    assert len(paths) == len(ALL), f"{len(paths)} pochettes pour {len(ALL)} titres"
    cards = [frame_intro(True)]
    for i, (t, p) in enumerate(zip(ALL, paths), 1):
        cards.append(frame_card(i, t, p))
    cards.append(frame_intro(False))
    # durées : intro, 34 x SEG, outro
    cuts = [0.0, INTRO]
    for _ in range(len(ALL)):
        cuts.append(cuts[-1] + SEG)
    cuts.append(cuts[-1] + OUTRO)

    if "--stills" in sys.argv:
        os.makedirs(f"{OUT}/stills", exist_ok=True)
        for k in (0, 1, 9, 22, 34, 35):
            Image.fromarray((np.clip(cards[k], 0, 1) * 255 + .5).astype(np.uint8)).save(
                f"{OUT}/stills/c{k}.jpg", quality=90)
        print("stills ok", len(cards))
        return

    dst = f"{LIV}/FILM-CATALOGUE-34-9x16.mp4"
    cmd = [FF, "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", f"{OUT}/cache/pub.m4a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", dst]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    rng = np.random.default_rng(7)
    idx = 0
    for k in range(n):
        t = k / FPS
        while idx < len(cuts) - 2 and t >= cuts[idx + 1]:
            idx += 1
        f = cards[idx]
        f = f * (1 - 0.02 * np.exp(-(t - cuts[idx]) * 9))  # micro-pop à la coupe
        fade = min(1.0, t / 0.5, (DUR - t) / 0.5)
        f = np.clip(f, 0, 1) * fade
        f = np.clip(f + rng.normal(0, 0.005, (H, W, 1)), 0, 1)
        p.stdin.write((f * 255 + 0.5).astype(np.uint8).tobytes())
        if k % 120 == 0:
            print(k, n, flush=True)
    p.stdin.close()
    p.wait()
    print("exit", p.returncode, dst)


if __name__ == "__main__":
    build()
