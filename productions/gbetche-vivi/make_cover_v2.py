#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carrés v2 + master v2 taggé — Gbètché vivi.

v2 = le moteur ecrit DIRECTEMENT sur l'image : bandeau de titre peint a la main, scotch,
souligne au feutre, etiquette de code, icones vectorielles (cloche / partage / signet),
etoiles decoupees. Comme pour le clip, le portrait n'est jamais rogne en haut ni en bas :
on compose buste + fond floute.

APIC (pochette) ecrit par ffmpeg en ID3v2.3, puis USLT (paroles) remis par eyed3 -
dans cet ordre, car ffmpeg ne recopie pas les frames de paroles existantes.
"""
import glob
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
PERS = os.path.join(HERE, "personnages")
OUT = os.path.join(HERE, "livrables")
COV = os.path.join(HERE, "covers")
os.makedirs(COV, exist_ok=True)
S = 1080

from make_cover import square, embed          # reuse: meme pipeline, meme gabarit
import stickers as ST
from render_intro_cta import font, draw_spaced, text_w

GOLD = (255, 211, 90)
CREME = (255, 243, 214)


def decorate(canvas, titre, sous, code, note=""):
    """ecriture + stickers poses par l'outil sur la pochette."""
    cv = canvas.convert("RGBA")
    lay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    # 1) feuille de papier scotchee en bas, titre ecrit dessus au marqueur
    ph = 232
    y0 = S - ph - 44
    paper = Image.new("RGBA", (S - 116, ph), (246, 240, 226, 246))
    pd = ImageDraw.Draw(paper)
    for _ in range(220):                       # grain papier
        x, y = pd.im.size[0] * 0, 0
    f_t, sk = font(96, 900)
    w_t = text_w(pd, titre, f_t, spacing=2, stroke=sk)
    while w_t > S - 190:
        f_t, sk = font(max(40, int(f_t.size * (S - 190) / w_t)), 900)
        w_t = text_w(pd, titre, f_t, spacing=2, stroke=sk)
    pd.text(((paper.width - w_t) / 2 + 4, 26), titre, font=f_t, fill=(24, 22, 26, 255), stroke_width=sk,
            stroke_fill=(24, 22, 26, 90))
    f_s, sk2 = font(40, 700)
    draw_spaced(pd, paper.width / 2, 152, sous, f_s, (60, 52, 40, 255), spacing=3, stroke=sk2,
                stroke_fill=(255, 255, 255, 120))
    if note:
        f_n, _ = font(30, 600)
        draw_spaced(pd, paper.width / 2, 196, note, f_n, (96, 78, 40, 255), spacing=2)
    ST.squiggle(pd, paper.width / 2 - w_t / 2 - 6, 128, paper.width / 2 + w_t / 2 + 6, col=GOLD, width=8,
                wob=6.0, seed=31)
    lay.paste(paper, (58, y0), paper)
    d = ImageDraw.Draw(lay)
    ST.tape(d, 96, y0 + 6, 132, 40, ang=-13)
    ST.tape(d, S - 96, y0 + 2, 132, 40, ang=9)
    ST.tape(d, S / 2, y0 + ph - 4, 150, 38, ang=-2)
    # 2) etiquette du code, en haut a droite, legerement tournee
    f_c, _ = font(52, 900)
    ST.tag(d, S - 190, 150, code, f_c, bg=(18, 16, 14), fg=GOLD, rot=7, pad=(20, 12), alpha=235)
    ST.dashed(d, (S - 300, 96, S - 80, 206), col=CREME, width=3, dash=12, gap=9, rad=8, alpha=150)
    # 3) icones dessinees + etoiles
    ST.icon(d, 152, 150, "bell", s=42, col=GOLD, width=6)
    ST.icon(d, 262, 158, "share", s=30, col=(240, 236, 226), width=5, alpha=225)
    ST.icon(d, 348, 150, "bookmark", s=30, col=(240, 236, 226), width=5, alpha=225)
    ST.star(d, 96, y0 - 42, 44, points=9, rot=12, alpha=235)
    ST.star(d, S - 108, y0 - 26, 30, points=8, rot=-16, alpha=210)
    sp, off = ST.sparkles(None, 1.9, [(70, 92, 420, 210)], rng_seed=5, n=3)
    lay.alpha_composite(sp, dest=off)
    return Image.alpha_composite(cv, lay).convert("RGB")


def main():
    plan = [("anim-v2-30", "gbetché-vivi-v2-1080", "Gbètché vivi", "Bandit Positif", "0314",
             "Wolof TechStein beat wê !"),
            ("anim-v2-12", "cover-v2-neon", "Gbètché vivi", "Wanyiyi dans mon cœur", "0314", ""),
            ("anim-v2-05", "cover-v2-libre", "Gbètché vivi", "Libre · chaîne cassée", "0314", ""),
            ("anim-v2-01", "cover-v2-regarde", "Gbètché vivi", "Regarde jusqu'à la fin", "0314", "")]
    made = []
    for src, name, t1, t2, code, note in plan:
        p = os.path.join(PERS, f"{src}.png")
        if not os.path.exists(p):
            print("  manque", src)
            continue
        base = square(p, os.path.join(COV, f"_tmp_{name}.jpg"), band=(0.05, 0.60))
        im = Image.open(os.path.join(COV, f"_tmp_{name}.jpg")).convert("RGB")
        out = decorate(im, t1, t2, code, note)
        dst = os.path.join(COV, f"{name}.jpg")
        out.save(dst, quality=93)
        os.remove(os.path.join(COV, f"_tmp_{name}.jpg"))
        made.append(dst)
        print("cover:", dst, out.size)
    mp3_v1 = os.path.join(OUT, "Gbetché vivi - master.mp3")
    mp3_v2 = os.path.join(OUT, "Gbetché vivi - master v2.mp3")
    if made and os.path.exists(mp3_v1):
        import shutil
        shutil.copyfile(mp3_v1, mp3_v2)                       # audio identique, seule la pochette change
        tmp = os.path.join(OUT, "_v2_tag.mp3")
        rc, err = embed(made[0], mp3_v2, tmp)
        print("embed APIC rc=", rc, err if rc else "")
        if rc == 0:
            os.replace(tmp, mp3_v2)
        lrc = os.path.join(os.path.abspath(os.path.join(HERE, "..", "..")), "Gbètché vivi - Bandit positif.txt")
        e3 = os.path.join(os.path.dirname(sys.executable), "eyeD3")
        r = subprocess.run([e3, f"--add-lyrics={lrc}:Paroles:fre", mp3_v2],
                           capture_output=True, text=True)
        print("USLT rc=", r.returncode)
        import eyed3
        tg = eyed3.load(mp3_v2).tag
        print("-> master v2:", os.path.basename(mp3_v2), os.path.getsize(mp3_v2) // 1024, "KB |",
              tg.title, "/", tg.artist, "| images:", len(list(tg.images)), "| lyrics:",
              [(l.description, len(l.text)) for l in tg.lyrics])
    print("covers v2:", [os.path.basename(p) for p in made])
    return made


if __name__ == "__main__":
    main()
