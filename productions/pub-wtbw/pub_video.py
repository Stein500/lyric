#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PUB WTBW · 30 s · 1080x1920 — typographie cinétique, catalogue des titres.
Aucune photo, aucune image générée : lettrage moteur uniquement.
"""
import json
import math
import subprocess
import sys

import numpy as np
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, "/home/user/lyric/productions/imelda-13-novembre")
import engine as E  # helpers typo / grain / ornements

FF = imageio_ffmpeg.get_ffmpeg_exe()
OUT = "/home/user/lyric/productions/pub-wtbw"
W, H = 1080, 1920
FPS = 30

META = json.load(open(f"{OUT}/cache/pub.json"))
BUMPER = "--bumper" in sys.argv
DUR = 5.0 if BUMPER else META["duration"]

CARDS = [
    dict(kind="brand", title="WOLOF TECHSTEIN BEAT WÊ", sub="DSKY · WTBW · BÉNIN"),
    dict(kind="song", title="MONSTER POSITIVE", quote="They called it a curse. I called it power."),
    dict(kind="song", title="NOUKIKO TCHÉ WÊ", quote="c'est mon sourire à moi"),
    dict(kind="song", title="AYON DÈKPÈ", quote="tu es trop jolie"),
    dict(kind="song", title="TU ES TROP BELLE", quote="j'ai la trouille, c'est fou"),
    dict(kind="song", title="GBÈTCHÉ VIVI", quote="ma vie me plaît, je suis béni"),
    dict(kind="song", title="NAN YI A GA DJIN WÊ", quote="j'irai au sommet, rien ne peut m'arrêter"),
    dict(kind="song", title="CONCENTRÉ SUR LE CHEMIN", quote="je regarde plus en arrière"),
    dict(kind="song", title="SANGUIN", quote="le sang dans les veines"),
    dict(kind="song", title="ON NOUS A VOLÉ NOTRE ÉDUCATION", quote="on se relève"),
    dict(kind="song", title="ÇA MONTE, ÇA DESCEND", quote="ça monte, ça descend"),
    dict(kind="song", title="LE GOÛT BON DE LA VIE", quote="la nuit est à nous"),
    dict(kind="song", title="MAHU TI TÈ GBÈ", quote="God is always there"),
    dict(kind="song", title="VIVI O O R", quote="ton goût est si doux"),
    dict(kind="song", title="GLACE", quote="si tu veux toucher mon cœur"),
    dict(kind="song", title="GOINFRES", quote="vous mangez trop"),
    dict(kind="services", title="TES MOMENTS", words=["MARIAGE", "ANNIVERSAIRE", "HOMMAGE", "FÊTE"]),
    dict(kind="craft", title="SUR MESURE", words=["ÉCRITURE", "COMPOSITION", "CLIP LYRICS", "9:16"]),
    dict(kind="catalog", title="TOUT UN CATALOGUE"),
    dict(kind="end", title="TON HISTOIRE MÉRITE", sub="SON MORCEAU.", brand="DSKY · WTBW"),
]

CATALOG = [
    "NOUKIKO TCHÉ WÊ", "AYON DÈKPÈ", "TU ES TROP BELLE", "MONSTER POSITIVE",
    "JE ME RELÈVE TOUJOURS", "GBÈTCHÉ VIVI", "NAN YI A GA DJIN WÊ", "CONCENTRÉ SUR LE CHEMIN",
    "SANGUIN", "ON NOUS A VOLÉ NOTRE ÉDUCATION", "ÇA MONTE, ÇA DESCEND", "LE GOÛT BON DE LA VIE",
    "MAHU TI TÈ GBÈ", "VIVI O O R", "GLACE", "GOINFRES", "GRAND MARCHEUR", "MASQUE",
    "GHOST U SEE", "NONVI KONOU", "YAFOY", "LE SURVIVANT", "JE SUIS PAUVRE ET RICHE",
    "TESTOSTÉRONE", "JE CRACHE LES DÉMONS", "DÈS LE DÉBUT", "ENTRE TES MAINS",
    "CALM IN OFF DOWN", "DRAGUE MOI", "JE M'AIME TELLEMENT", "SEUL DANS MA TÊTE",
    "L'AMOUR EST LA RÉPONSE", "MOTIVÉ", "WOLOF TECHSTEIN — ESSAIE",
]

rng = np.random.default_rng(11)
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
RAD = np.sqrt((XX - W / 2) ** 2 + (YY - H / 2) ** 2) / (W * 0.9)


def tracked_mask(text, fnt, tracking, y, cx=W / 2, alpha=255, stroke=0.0):
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    tw = E.tracked_width(fnt, text, tracking)
    E.draw_tracked(d, (cx - tw / 2, y), text, fnt, tracking, fill=alpha, stroke=stroke)
    return E.mask_to_float(im)


def fit_font(kind, text, size, tracking, maxw=920):
    fnt = E.font(kind, size)
    tw = E.tracked_width(fnt, text, tracking)
    if tw > maxw:
        fnt = E.font(kind, max(18, int(size * maxw / tw)))
    return fnt


def int_card(i, t_local, card, seg=1.443):
    """carte typographique ; t_local = temps dans le segment."""
    frame = np.full((H, W), 0.035, dtype=np.float32)
    frame += 0.06 * np.exp(-(RAD ** 2) * 2.2) * (0.8 + 0.2 * math.sin(i * 0.7 + t_local * 1.2))

    # monogramme en filigrane, très discret
    if i < 16:
        wm = tracked_mask("WTBW", E.font("m", 26), 9.0, 1668, alpha=255)
        frame = E.composite(frame, wm, 1.0, 0.22)

    # index
    idx = tracked_mask(f"{i+1:02d}", E.font("m", 24), 3.0, 232, cx=140, alpha=255)
    frame = E.composite(frame, idx, 1.0, 0.55)
    hdr = tracked_mask("WTBW · CATALOGUE", E.font("m", 22), 5.0, 232, cx=W - 300, alpha=255)
    frame = E.composite(frame, hdr, 1.0, 0.35)

    # entrée animée
    ain = E.smoothstep(t_local / 0.14)
    aout = 1 - E.smoothstep((t_local - seg + 0.13) / 0.13)
    alpha = ain * aout
    rise = (1 - ain) * 26

    def put(mask, a, color=1.0):
        if a <= 0.004:
            return
        if rise:
            dy = int(round(rise))
            m = np.zeros_like(mask)
            m[dy:] = mask[:H - dy]
            mask = m
        nonlocal frame
        frame = E.composite(frame, mask, color, a)

    kind = card["kind"]
    if kind == "brand":
        f1 = fit_font("pf", "WTBW", 260, 40)
        put(tracked_mask("WTBW", f1, 40, 980), alpha)
        f2 = fit_font("m", card["title"], 34, 10)
        put(tracked_mask(card["title"], f2, 10, 1082), alpha * 0.92)
        f3 = fit_font("m", card["sub"], 26, 7)
        put(tracked_mask(card["sub"], f3, 7, 1160), alpha * 0.7)
        # filet
        p = E.ease_out(min(1, t_local / 0.5))
        frame[1030, int(W / 2 - 220 * p):int(W / 2 + 220 * p)] = 0.55
    elif kind in ("song", "services", "craft"):
        # gros titre
        f = fit_font("pf", card["title"], 116, 8)
        m = tracked_mask(card["title"], f, 8, 900)
        sh = E.gauss(m, 14) * 0.85
        frame *= (1 - 0.0 * sh)
        put(m, alpha)
        # filet
        p = E.ease_out(min(1, max(0, (t_local - 0.05) / 0.45)))
        if p > 0.01:
            frame[944, int(W / 2 - 250 * p):int(W / 2 + 250 * p)] = 0.60
        # sous-ligne
        if card.get("quote"):
            fq = E.font("pfi", 52)
            fq = fit_font("pfi", card["quote"], 52, 0.4, maxw=860)
            aq = E.smoothstep((t_local - 0.12) / 0.28) * alpha
            put(tracked_mask(card["quote"], fq, 0.4, 1010), aq * 0.95)
        if card.get("words"):
            for k, wd in enumerate(card["words"]):
                col, row = k % 2, k // 2
                cxw = W * (0.30 if col == 0 else 0.70)
                fw = fit_font("m", wd, 34, 7, maxw=420)
                aw = E.smoothstep((t_local - 0.10 - k * 0.09) / 0.25) * alpha
                put(tracked_mask(wd, fw, 7, 1015 + row * 86, cx=cxw, alpha=255), aw * 0.95)
    elif kind == "catalog":
        f = fit_font("pf", card["title"], 104, 10)
        put(tracked_mask(card["title"], f, 10, 720), alpha)
        # mur des titres : tout le catalogue, deux colonnes
        n = len(CATALOG)
        half = (n + 1) // 2
        fy = E.font("m", 26)
        drift = int(round(10 * (t_local / seg)))
        for k, title in enumerate(CATALOG):
            col, row = (0, k) if k < half else (1, k - half)
            cxw = W * (0.27 if col == 0 else 0.73)
            y = 830 + row * 40 - drift
            if y > 1540:
                continue
            a = alpha * (0.80 if y < 1440 else 0.55)
            ft = fit_font("m", title, 26, 1.8, maxw=440)
            put(tracked_mask(title, ft, 1.8, y, cx=cxw, alpha=255), max(0.0, a))
    elif kind == "end":
        f = fit_font("pf", card["title"], 104, 6, maxw=900)
        put(tracked_mask(card["title"], f, 6, 820), alpha)
        f2 = fit_font("pfi", card["sub"], 118, 3, maxw=900)
        put(tracked_mask(card["sub"], f2, 3, 960), alpha)
        fb = fit_font("m", card["brand"], 46, 16)
        ab = E.smoothstep((t_local - 0.35) / 0.4) * alpha
        put(tracked_mask(card["brand"], fb, 16, 1210), ab)
        frame[1070, int(W / 2 - 200 * E.ease_out(min(1, t_local / 0.5))):
              int(W / 2 + 200 * E.ease_out(min(1, t_local / 0.5)))] = 0.55

    # barre de progression du catalogue
    prog = (i + min(1, t_local / seg)) / (len(BUMPER_CARDS) if BUMPER else len(CARDS))
    frame[1780, 100:100 + int((W - 200) * prog)] = 0.5

    # flash de coupe
    if t_local < 0.06:
        frame = 1 - (1 - frame) * (1 - 0.30 * (1 - t_local / 0.06))
    return frame


BUMPER_CARDS = [
    dict(kind="brand", title="DES CHANSONS POUR TES MOMENTS", sub="DSKY · WTBW · BÉNIN"),
    dict(kind="song", title="NOUKIKO TCHÉ WÊ", quote="c'est mon sourire à moi"),
    dict(kind="end", title="TON HISTOIRE MÉRITE", sub="SON MORCEAU.", brand="DSKY · WTBW"),
]


def render(t):
    cards = BUMPER_CARDS if BUMPER else CARDS
    seg = DUR / len(cards)
    i = int(t // seg)
    i = min(i, len(cards) - 1)
    tl = t - i * seg
    frame = int_card(i, tl, cards[i], seg)
    # grain + scintillement pellicule
    frame = E.clamp01(frame * (1.0 + 0.012 * math.sin(t * 41)) + rng.normal(0, 0.012, (H, W)))
    if t < 0.3:
        frame *= 0.4 + 0.6 * E.smoothstep(t / 0.3)
    end = DUR - 0.8
    if t > end:
        frame *= 1 - 0.65 * E.smoothstep((t - end) / 0.8)
    return frame


def main():
    frames = int(round(DUR * FPS))
    out = (f"{OUT}/livrables/PUB-WTBW-BUMPER-5s-9x16.mp4" if BUMPER
           else f"{OUT}/livrables/PUB-WTBW-CATALOGUE-9x16.mp4")
    audio = f"{OUT}/cache/bumper.m4a" if BUMPER else f"{OUT}/cache/pub.m4a"
    cmd = [FF, "-y", "-hide_banner", "-loglevel", "warning",
           "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0",
           "-i", audio,
           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
           "-c:a", "copy", "-shortest", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(frames):
        p.stdin.write((E.clamp01(render(k / FPS)) * 255 + 0.5).astype(np.uint8).tobytes())
        if k % 150 == 0:
            print(k, frames, flush=True)
    p.stdin.close()
    print("exit", p.wait(), out)


if __name__ == "__main__":
    if "--stills" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--stills") + 1].split(",")]
        import os
        os.makedirs(f"{OUT}/stills", exist_ok=True)
        for t in ts:
            Image.fromarray((E.clamp01(render(t)) * 255).astype("uint8")).save(f"{OUT}/stills/p{t:06.2f}.png")
        print("ok")
    else:
        main()
