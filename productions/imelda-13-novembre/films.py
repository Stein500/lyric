#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les trois films « IMELDA · 13 NOVEMBRE » — un refrain, un film, des photos distinctes.
Usage : python3 films.py v1|v2|v3 [--stills t1,t2,...]
"""
import json
import os
import sys

from PIL import Image

import engine as E

P = "IMG-20261111-WA"
AUDIO = json.load(open(f"{E.OUT}/cache/audio_songs.json"))

BRAND = dict(eyebrow="JOYEUX ANNIVERSAIRE", word="Imelda", thanks="MERCI D'EXISTER", brand="WTBW")


def shot(photo, t0, t1, items, **kw):
    d = dict(photo=f"{P}{photo}.jpg", t0=t0, t1=t1, items=items)
    d.update(kw)
    return d


def eyebrow(t, size=32, tracking=9.2):
    return dict(kind="eyebrow", text=t, size=size, tracking=tracking, stroke=0.6, gap_before=0)


def line(t, size=60, gap=42, lh=None):
    d = dict(kind="line", font="pfi", text=t, size=size, tracking=0.2, stroke=0.45, gap_before=gap)
    if lh:
        d["lh"] = lh
    return d


# --------------------------------------------------------------------------- V1
def v1():
    dur = AUDIO["v1"]["duration"]
    return dict(
        slug="v1", duration=dur, audio=f"{E.CACHE}/v1.m4a",
        file="IMELDA-01-NOUKIKO-TCHE-WE-WTBW-9x16.mp4",
        title=dict(t1=3.60, eyebrow="13 · 11 · 2026", word="IMELDA", sub="NOUKIKO TCHÉ WÊ"),
        finale_t0=dur - 6.41,
        finale=dict(BRAND, wish=("Que cette année te rende", "tout ce que ton sourire donne.")),
        cuts=[dur - 6.41],
        shots=[
            shot("0031", 3.60, 10.20, [eyebrow("NOUKIKO TCHÉ WÊ"), line("« c'est mon sourire à moi »")],
                 zoom=(1.12, 1.02), pan=(0.10, -0.05), text_center=1355,
                 ornaments=[("sparkle", dict(x=190, y=1150, size=34, alpha=150, delay=0.6)),
                            ("sparkle", dict(x=862, y=1050, size=26, alpha=120, delay=1.0))]),
            shot("0041", 10.20, 16.60, [eyebrow("TON SOURIRE"), line("Personne ne te l'enlèvera.")],
                 zoom=(1.03, 1.17), pan=(-0.06, 0.10), text_center=1360,
                 ornaments=[("heart", dict(x=888, y=1150, size=44, alpha=170, delay=0.7))]),
            shot("0036", 16.60, 23.20,
                 [line("Il y a des sourires", gap=0), line("qui réparent une journée.", lh=78, gap=6)],
                 zoom=(1.02, 1.12), pan=(0.04, -0.09), text_center=1375,
                 ornaments=[("sparkle", dict(x=168, y=1130, size=30, alpha=140, delay=0.7))]),
            shot("0039", 23.20, 29.80,
                 [line("Le tien répare", gap=0), line("des années.", lh=78, gap=6)],
                 zoom=(1.06, 1.22), pan=(0.06, 0.08), text_center=1375,
                 ornaments=[("flower", dict(x=166, y=1120, size=46, alpha=150, delay=0.6)),
                            ("flower", dict(x=876, y=1170, size=36, alpha=130, delay=0.9, rot=0.7))]),
            shot("0048", 29.80, 36.20,
                 [line("Alors aujourd'hui,", gap=0), line("on le célèbre.", lh=78, gap=6)],
                 zoom=(1.03, 1.15), pan=(0.0, -0.06), text_center=1375,
                 ornaments=[("arrow", dict(x=560, y=1010, w=330, h=250, alpha=150, flip=True, delay=0.9))]),
        ],
    )


# --------------------------------------------------------------------------- V2
def v2():
    dur = AUDIO["v2"]["duration"]
    return dict(
        slug="v2", duration=dur, audio=f"{E.CACHE}/v2.m4a",
        file="IMELDA-02-AYON-DEKPE-WTBW-9x16.mp4",
        title=dict(t1=3.40, eyebrow="13 · 11 · 2026", word="IMELDA", sub="AYON DÈKPÈ"),
        finale_t0=dur - 6.97,
        finale=dict(BRAND, wish=("Que la lumière te suive", "partout où tu danses.")),
        cuts=[dur - 6.97],
        shots=[
            shot("0043", 3.40, 9.90,
                 [line("Tu ne marches pas :", gap=0), line("tu fais danser la lumière.", lh=78, gap=6)],
                 zoom=(1.03, 1.15), pan=(0.06, -0.06), text_center=1375,
                 ornaments=[("sparkle", dict(x=170, y=1140, size=32, alpha=150, delay=0.7)),
                            ("sparkle", dict(x=880, y=1070, size=24, alpha=120, delay=1.0))]),
            shot("0030", 9.90, 16.40, [eyebrow("AYON DÈKPÈ"), line("tu es trop jolie.")],
                 zoom=(1.14, 1.03), pan=(-0.08, 0.02), text_center=1355,
                 ornaments=[("flower", dict(x=158, y=1120, size=52, alpha=160, delay=0.5)),
                            ("flower", dict(x=214, y=1176, size=34, alpha=130, delay=0.8, rot=0.6)),
                            ("flower", dict(x=872, y=1146, size=42, alpha=150, delay=1.0, rot=-0.4))]),
            shot("0046", 16.40, 22.90,
                 [line("Le monde s'arrête", gap=0), line("quand tu passes.", lh=78, gap=6)],
                 zoom=(1.02, 1.13), pan=(0.04, 0.04), text_center=1375,
                 ornaments=[("heart", dict(x=182, y=1140, size=40, alpha=160, delay=0.8))]),
            shot("0033", 22.90, 29.40, [line("Et moi, je reste", gap=0), line("à regarder.", lh=78, gap=6)],
                 zoom=(1.12, 1.03), pan=(-0.05, -0.02), text_center=1375),
            shot("0037", 29.40, 33.40, [line("Merci d'être toi.", size=56)],
                 zoom=(1.02, 1.10), pan=(0.0, -0.06), text_center=1355,
                 ornaments=[("arrow", dict(x=560, y=1010, w=330, h=250, alpha=150, flip=True, delay=0.5))]),
        ],
    )


# --------------------------------------------------------------------------- V3
def v3():
    dur = AUDIO["v3"]["duration"]
    return dict(
        slug="v3", duration=dur, audio=f"{E.CACHE}/v3.m4a",
        file="IMELDA-03-TU-ES-TROP-BELLE-WTBW-9x16.mp4",
        title=dict(t1=3.20, eyebrow="13 · 11 · 2026", word="IMELDA", sub="TU ES TROP BELLE"),
        finale_t0=dur - 7.51,
        finale=dict(BRAND, wish=("Alors je ne tremble plus :", "je te célèbre.")),
        cuts=[dur - 7.51],
        shots=[
            shot("0049", 3.20, 9.40, [line("Il y avait déjà", gap=0), line("ce sourire.", lh=78, gap=6)],
                 zoom=(1.02, 1.10), pan=(0.0, -0.03), text_center=1375, fit="contain",
                 ornaments=[("heart", dict(x=474, y=1178, size=40, alpha=150, delay=0.8))]),
            shot("0067", 9.40, 16.20, [eyebrow("TU ES TROP BELLE"), line("j'ai la trouille, c'est fou.")],
                 zoom=(1.14, 1.03), pan=(-0.04, -0.04), text_center=1385,
                 ornaments=[("heart", dict(x=182, y=1130, size=38, alpha=150, delay=0.8))]),
            shot("0066", 16.20, 23.00, [line("Je n'ai jamais eu", gap=0), line("peur du monde.", lh=78, gap=6)],
                 zoom=(1.02, 1.11), pan=(0.0, -0.05), text_center=1375,
                 ornaments=[("flower", dict(x=160, y=1108, size=46, alpha=150, delay=0.6)),
                            ("flower", dict(x=876, y=1160, size=38, alpha=140, delay=0.9, rot=0.8))]),
            shot("0042", 23.00, dur - 7.51, [line("Seulement de", gap=0), line("ton regard.", lh=78, gap=6)],
                 zoom=(1.02, 1.14), pan=(0.0, -0.05), text_center=1375,
                 ornaments=[("sparkle", dict(x=172, y=1150, size=30, alpha=140, delay=0.7))]),
        ],
    )


FILMS = {"v1": v1, "v2": v2, "v3": v3}

if __name__ == "__main__":
    key = sys.argv[1]
    cfg = FILMS[key]()
    proj = E.Project(cfg)
    if "--stills" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--stills") + 1].split(",")]
        os.makedirs(f"{E.OUT}/stills", exist_ok=True)
        for t in ts:
            f = E.render_frame_p(proj, t)
            Image.fromarray((E.clamp01(f) * 255).astype("uint8")).save(
                f"{E.OUT}/stills/{key}-t{t:06.2f}.png")
        print("stills ok", cfg["duration"])
    else:
        print("durée", cfg["duration"], "frames", proj.frames)
        E.encode(proj)
