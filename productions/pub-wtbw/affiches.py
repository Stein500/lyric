#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Affiches « services » DSKY · WTBW — 1080x1350 (feed) et 1080x1920 (story).
Texte ancré en bas, photo pleine page en haut : plus « affiche » que les cartes citations.
"""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, "/home/user/lyric/productions/imelda-13-novembre")
sys.path.insert(0, "/home/user/lyric/productions/pub-wtbw")
import engine as E  # noqa: E402
import universel as U  # noqa: E402
import logo as L  # noqa: E402

OUT = "/home/user/lyric/productions/pub-wtbw"

AFFICHES = [
    ("srv-mariage", "SERVICE 01", "MARIAGE", "la chanson de votre premier regard"),
    ("srv-anniversaire", "SERVICE 02", "ANNIVERSAIRE", "un morceau pour ceux qui t'aiment"),
    ("srv-memoire", "SERVICE 03", "MÉMOIRE", "faire vivre sa voix, pas seulement son nom"),
    ("srv-fete", "SERVICE 04", "FÊTE", "le son de ta soirée, écrit pour toi"),
    ("srv-clip", "SERVICE 05", "CLIP 9:16", "ton morceau en image"),
    ("srv-ecriture", "SERVICE 06", "ÉCRITURE", "tes mots, ma plume"),
    ("srv-education", "SERVICE 07", "ÉDUCATION", "ateliers d'écriture et de scène"),
    ("srv-event", "SERVICE 08", "ÉVÉNEMENT", "l'hymne de ta cérémonie"),
    ("srv-voix", "SERVICE 09", "ÉGLISE", "louange, gospel, action de grâce"),
    ("srv-ville", "SERVICE 10", "PARTOUT", "Cotonou — et partout où tu m'écoutes"),
]


def build(story=False):
    H = 1920 if story else 1350
    U.H = H
    W = 1080
    suffix = "-STORY" if story else ""
    folder = f"{OUT}/livrables/affiches"
    os.makedirs(folder, exist_ok=True)
    out = []
    pad = int(H * 0.075)
    for i, (photo, kicker, title, sub) in enumerate(AFFICHES, 1):
        f = U.photo(f"{photo}.jpg", dark=0.50)
        # dégradé bas pour asseoir le texte
        yy = np.arange(H, dtype=np.float32)[:, None] / H
        f = f * np.clip(0.42 + 1.05 * np.abs(yy - 0.22), 0.42, 1.0)

        U.chrome(f, kicker, f"{i:02d} / 10")

        ta, ts = U.fit(title, "pf", 168 if story else 148, 0.05, maxw=0.86)
        cta_y = H - pad
        sub_y = cta_y - 92
        rule_y = sub_y - 40
        y_title = rule_y - int(ts * 1.92)
        U.put(f, ta, 0, y_title, 1.0, 1.0)
        U.rule(f, rule_y, 150)
        sa, _ = U.fit(sub, "pfi", 46, 0.02, maxw=0.80)
        U.put(f, sa, 0, sub_y, 1.0, 0.95)
        ca, _ = U.fit("TIKTOK & YOUTUBE — @DSKYWTBW", "m", 24, 0.24, maxw=0.78)
        U.put(f, ca, 0, cta_y, 1.0, 0.9)

        sg = L.sigil(64)
        U.put(f, sg, W // 2 - 32, 86, 1.0, 0.55)

        f = E.clamp01(f + np.random.default_rng(200 + i).normal(0, 0.006, f.shape))
        p = f"{folder}/AFFICHE-{i:02d}-{title.replace(' ', '-').replace(':', '')}{suffix}.jpg"
        Image.fromarray((np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)).save(p, quality=94, subsampling=1)
        out.append(p)
    return out


if __name__ == "__main__":
    for p in build(story="--story" in sys.argv):
        print(p)
