# -*- coding: utf-8 -*-
"""Rendu du CLIP COMPLET MESÍAS — 1080x1920, 30 i/s.

Structure temporelle (source unique : data/verses_map.json + mesures ffmpeg) :
  intro   : 0,00 → debut_vers1            carte titre/artiste (WTBW), fond flouté
  paroles : debut_vers1 → 739,349 s       vers 1..190, offset d'affichage -0,25 s
  carte   : 739,349 → 744,705 s           fin musicale réelle (silence), carte finale
  total   : 744,705 s + 5,00 s            soit 749,705 s = 22 491 frames à 30 i/s

Le son n'est PAS modifié dans ce script : il est calé sur le master normalisé, et la
carte finale prolonge la dernière seconde par un fondu au silence (pas d'audio ajouté).

Usage :
  python3 scripts/render_clip.py --seg 0 3 --out work/clip_seg0.mp4
  python3 scripts/render_clip.py --assemble
"""
import argparse, json, math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import render as R
from render_video import (big_background, camera_window, text_overlay, band_overlay,
                          hud_overlay, progress_overlay, FPS, W, H, FF)

DATA = os.path.join(ROOT, "data", "verses_map.json")
LIV = os.path.join(ROOT, "livrables")
WORK = os.path.join(ROOT, "work")

DUR_AUDIO = 744.705        # durée décodée mesurée du master
TAIL = 5.00                # carte finale v7.0
T_END = DUR_AUDIO + TAIL   # 749,705 s
N_FRAMES = int(round(T_END * FPS))

CREAM = (246, 240, 228)
AMBER = (232, 163, 61)
INDIGO = (10, 14, 30)


# ------------------------------------------------------------------ cartes
_CARD_BG = {}


def card_background(img_name, blur=28, dark=0.58, scale=1.14):
    """Fond de carte : le seul endroit où le flou est autorisé (règle v7.0).

    Calculé UNE seule fois puis mémorisé : le flou gaussien de 1080x1920 est cher,
    et la carte est statique (seuls les alphas bougent).
    """
    key = (img_name, blur, dark, scale)
    if key in _CARD_BG:
        return _CARD_BG[key]
    path = os.path.join(ROOT, "work", "base", img_name)
    im = Image.open(path).convert("RGB")
    big = im.resize((int(W * scale), int(H * scale)), Image.LANCZOS)
    ox, oy = (big.width - W) // 2, (big.height - H) // 2
    bg = big.crop((ox, oy, ox + W, oy + H)).filter(ImageFilter.GaussianBlur(blur))
    bg = Image.blend(bg, Image.new("RGB", (W, H), INDIGO), dark)
    _CARD_BG[key] = bg
    return bg


def centered(rows, y0, width_line=0):
    """Calque RGBA de texte centré.

    rows = [(texte, taille, couleur, avance_verticale), ...] — l'avance est donnée
    explicitement pour chaque ligne, les lignes vides servant d'interlignes.
    """
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    y = y0
    for text, size, colour, adv in rows:
        f = R.font(size)
        d = ImageDraw.Draw(lay)
        tw = d.textlength(text, font=f)
        x = (W - tw) / 2
        if text:
            sh = Image.new("L", (W, H), 0)
            ImageDraw.Draw(sh).text((x, y), text, font=f, fill=255)
            sh = sh.filter(ImageFilter.GaussianBlur(10))
            lay.paste(Image.new("RGBA", (W, H), (4, 6, 16, 255)), (0, 0),
                      sh.point(lambda v: int(v * 0.8)))
            d.text((x, y), text, font=f, fill=colour,
                   stroke_width=5 if size < 60 else 7, stroke_fill=(8, 10, 22, 235))
        y += adv
    return lay


def badge_layer(lay):
    d = ImageDraw.Draw(lay)
    d.line([(170, 186), (910, 186)], fill=(96, 102, 120, 200), width=2)
    d.text((46, 46), "AVERLY MORILLO", font=R.font(44), fill=(240, 236, 226, 255))
    d.text((46, 100), "WTBW", font=R.font(34), fill=(232, 163, 61, 255))
    return lay


_INTRO = {}


def intro_layers():
    """Calques statiques de la carte d'intro (le fondu est appliqué par frame)."""
    if "layers" in _INTRO:
        return _INTRO["layers"]
    bg = card_background("pool_20_aube_horizon.png", blur=30, dark=0.58)
    head = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    head.paste(bg, (0, 0))
    badge_layer(head)
    title = centered([("MESÍAS", 168, CREAM + (255,), 190),
                      ("AVERLY MORILLO", 54, AMBER + (255,), 96),
                      ("EN DIRECT", 40, (198, 204, 220, 255), 0)], y0=690)
    fr = centered([("« Je prépare mon temple,", 42, (236, 232, 222, 255), 54),
                   ("ma lampe allumée »", 42, (236, 232, 222, 255), 0)], y0=1150)
    foot = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(foot).text((46, 1790), "LYRICS WTBW", font=R.font(30),
                              fill=(150, 156, 172, 255))
    _INTRO["layers"] = (head, title, fr, foot)
    return _INTRO["layers"]


def intro_card(m, t_local, dur):
    """Carte titre : fondu d'entrée, sortie rapide, fond flouté (autorisé ici)."""
    head, title, fr, foot = intro_layers()
    a = max(0.0, min(1.0, t_local / 1.2)) * max(0.0, min(1.0, (dur - t_local) / 0.8))
    lay = head.copy()
    t2 = title.copy()
    t2.putalpha(t2.getchannel("A").point(lambda v: int(v * a)))
    lay.alpha_composite(t2)
    a2 = max(0.0, min(1.0, (t_local - 3.0) / 1.4)) * max(0.0, min(1.0, (dur - t_local) / 0.8))
    if a2 > 0:
        f2 = fr.copy()
        f2.putalpha(f2.getchannel("A").point(lambda v: int(v * a2)))
        lay.alpha_composite(f2)
    a3 = max(0.0, min(1.0, (t_local - 2.0) / 1.5)) * max(0.0, min(1.0, (dur - t_local) / 0.8))
    f3 = foot.copy()
    f3.putalpha(f3.getchannel("A").point(lambda v: int(v * a3)))
    lay.alpha_composite(f3)
    return lay


_END = {}


def end_card(m, t_local, dur):
    """Carte finale 5,00 s : titre, artiste, remerciement, mention de production."""
    if "layers" not in _END:
        bg = card_background("pool_18_tempete_ciel.png", blur=28, dark=0.62)
        head = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        head.paste(bg, (0, 0))
        badge_layer(head)
        title = centered([("MESÍAS", 150, CREAM + (255,), 176),
                          ("AVERLY MORILLO", 52, AMBER + (255,), 120),
                          ("Gracias por escuchar", 42, (214, 212, 206, 255), 0)], y0=660)
        foot = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(foot)
        d.line([(170, 1690), (910, 1690)], fill=(96, 102, 120, 180), width=2)
        d.text((46, 1706), "PAROLES ORIGINALES · TRADUCTION FR AFFICHÉE",
               font=R.font(28), fill=(170, 176, 192, 255))
        d.text((46, 1750), "LYRICS WTBW", font=R.font(28), fill=(232, 163, 61, 220))
        _END["layers"] = (head, title, foot)
    head, title, foot = _END["layers"]
    a = max(0.0, min(1.0, t_local / 0.9))
    lay = head.copy()
    t2 = title.copy()
    t2.putalpha(t2.getchannel("A").point(lambda v: int(v * a)))
    lay.alpha_composite(t2)
    a2 = max(0.0, min(1.0, (t_local - 1.0) / 1.0))
    f2 = foot.copy()
    f2.putalpha(f2.getchannel("A").point(lambda v: int(v * a2)))
    lay.alpha_composite(f2)
    return lay


# ------------------------------------------------------------------ rendu d'un segment
def segment_bounds(m, s, nseg):
    """Découpe en nseg segments d'égale durée sur [0, T_END]."""
    step = T_END / nseg
    return s * step, (s + 1) * step if s < nseg - 1 else T_END


def render_segment(m, s, nseg, out, crf=22):
    """Rend [t0,t1) en un MP4 muet.

    Optimisation : les calques de texte ne bougent pas d'un frame à l'autre, donc
      - HUD (badge + filet) et bloc paroles (traduction + espagnol) sont fusionnés
        en UN calque chacun par vers, collé via sa seule boîte englobante ;
      - la barre de progression est tracée directement sur le frame (une ligne),
        au lieu de composer un calque plein écran de 1080x1920.
    """
    t0, t1 = segment_bounds(m, s, nseg)
    f0, f1 = int(round(t0 * FPS)), int(round(t1 * FPS))
    verses = m["verses"]
    OFF = m.get("calage", {}).get("offset_affichage_s", 0.0)
    v_first_start = verses[0]["debut_source"]
    SIL = m["calage"].get("silence_final_s", 739.349)

    # fenêtre du segment : les vers dont l'intervalle croise [t0, t1]
    sel = [v for v in verses
           if v["debut_source"] - 5 <= t1 and (v["fin"] or 9e9) >= t0 - 1]
    cache, text_box, hud_box = {}, {}, {}
    for v in sel:
        if v["image"] not in cache:
            cache[v["image"]] = big_background(v["image"])
        if v["i"] in text_box:
            continue
        # bloc paroles : traduction (y 959-1180) + bandeau espagnol (y 1252-1452)
        blk = Image.new("RGBA", (W, 540), (0, 0, 0, 0))
        tl = text_overlay(v["traduction_fr"])[0].crop((0, 940, W, 1210))
        band = band_overlay(R.lines_until(verses, v["debut_source"])).crop((0, 1200, W, 1480))
        blk.alpha_composite(tl, (0, 0))
        blk.alpha_composite(band, (0, 260))
        text_box[v["i"]] = (blk, (0, 940))
        hd = hud_overlay(m, v).crop((0, 0, W, 210))
        hud_box[v["i"]] = (hd, (0, 0))

    cmd = [FF, "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "pipe:0",
           "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
           "-pix_fmt", "yuv420p", "-x264-params", "keyint=60:min-keyint=30",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-an", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = f1 - f0
    prog_x0, prog_x1, prog_y = 170, 910, 186

    for f in range(f0, f1):
        t = f / FPS
        if t < v_first_start:
            frame = intro_card(m, t, v_first_start).convert("RGB")
        elif t >= SIL:
            frame = end_card(m, t - SIL, T_END - SIL).convert("RGB")
        else:
            v = sel[0]
            for cand in sel:
                if cand["debut_source"] + OFF <= t:
                    v = cand
            k = ((t - (v["debut_source"] + OFF)) /
                 max(0.4, (v["fin"] or v["debut_source"] + 3) - v["debut_source"]))
            frame = camera_window(cache[v["image"]], k % 1.0).copy()
            hd, hpos = hud_box[v["i"]]
            frame.paste(hd, hpos, hd)
            blk, bpos = text_box[v["i"]]
            frame.paste(blk, bpos, blk)
            pstd = max(0.0, min(1.0, (t - v_first_start) / (SIL - v_first_start)))
            ImageDraw.Draw(frame).line(
                [(prog_x0, prog_y), (int(prog_x0 + (prog_x1 - prog_x0) * pstd), prog_y)],
                fill=AMBER, width=3)
        p.stdin.write(frame.tobytes())
        if (f - f0) % 250 == 0:
            print(f"\r  seg{s} {f - f0}/{n}", end="", flush=True)
    p.stdin.close()
    p.wait()
    print(f"\r  seg{s} {n} frames -> {os.path.basename(out)}          ", flush=True)
    return out


def render_window(m, t0, t1, out, crf=22):
    """Rend une fenêtre temporelle explicite [t0,t1) — utilisé par le teaser."""
    verses = m["verses"]
    OFF = m.get("calage", {}).get("offset_affichage_s", 0.0)
    SIL = m["calage"].get("silence_final_s", 739.349)
    sel = [v for v in verses if v["debut_source"] - 5 <= t1 and (v["fin"] or 9e9) >= t0 - 1]
    cache, text_box, hud_box = {}, {}, {}
    for v in sel:
        if v["image"] not in cache:
            cache[v["image"]] = big_background(v["image"])
        blk = Image.new("RGBA", (W, 540), (0, 0, 0, 0))
        tl = text_overlay(v["traduction_fr"])[0].crop((0, 940, W, 1210))
        band = band_overlay(R.lines_until(verses, v["debut_source"])).crop((0, 1200, W, 1480))
        blk.alpha_composite(tl, (0, 0))
        blk.alpha_composite(band, (0, 260))
        text_box[v["i"]] = (blk, (0, 940))
        hud_box[v["i"]] = (hud_overlay(m, v).crop((0, 0, W, 210)), (0, 0))
    f0, f1 = int(round(t0 * FPS)), int(round(t1 * FPS))
    cmd = [FF, "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "pipe:0",
           "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
           "-pix_fmt", "yuv420p", "-x264-params", "keyint=60:min-keyint=30",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-an", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(f0, f1):
        t = f / FPS
        v = sel[0]
        for cand in sel:
            if cand["debut_source"] + OFF <= t:
                v = cand
        k = ((t - (v["debut_source"] + OFF)) /
             max(0.4, (v["fin"] or v["debut_source"] + 3) - v["debut_source"]))
        frame = camera_window(cache[v["image"]], k % 1.0).copy()
        hd, hpos = hud_box[v["i"]]
        frame.paste(hd, hpos, hd)
        blk, bpos = text_box[v["i"]]
        frame.paste(blk, bpos, blk)
        pstd = max(0.0, min(1.0, (t - verses[0]["debut_source"]) / (SIL - verses[0]["debut_source"])))
        ImageDraw.Draw(frame).line([(170, 186), (int(170 + 740 * pstd), 186)],
                                   fill=AMBER, width=3)
        p.stdin.write(frame.tobytes())
    p.stdin.close()
    p.wait()
    print("  fenêtre", round(t0, 2), "->", round(t1, 2), ":", f1 - f0, "frames")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seg", nargs=2, type=int, metavar=("S", "NSEG"))
    ap.add_argument("--crf", type=int, default=22)
    ap.add_argument("--out", default=None)
    ap.add_argument("--assemble", action="store_true")
    ap.add_argument("--teaser", action="store_true")
    ap.add_argument("--teaser-start", type=float, default=464.13)
    ap.add_argument("--audio", default=os.path.join(LIV, "Averly Morillo - MESIAS (master normalise -14LUFS).mp3"))
    args = ap.parse_args()
    m = json.load(open(DATA, encoding="utf8"))
    m["calage"]["silence_final_s"] = 739.349

    if args.seg:
        s, nseg = args.seg
        out = args.out or os.path.join(WORK, f"clip_seg{s}.mp4")
        render_segment(m, s, nseg, out, crf=args.crf)
        return

    if args.teaser:
        # extrait réel du maître, 15,00 s = 450 frames à 30 i/s
        t0 = args.teaser_start
        t1 = t0 + 15.0
        verses = m["verses"]
        idx = [v["i"] for v in verses if t0 - 5 <= v["debut_source"] <= t1]
        i0, i1 = min(idx), max(idx)
        tmp = os.path.join(WORK, "teaser_body.mp4")
        # render_segment travaille sur des bornes calculées ; on passe par une
        # variante explicite pour garder exactement 15,00 s
        render_window(m, t0, t1, tmp, crf=args.crf)
        audio = os.path.join(LIV, "Averly Morillo - MESIAS (master normalise -14LUFS).mp3")
        out = os.path.join(LIV, "MESIAS_teaser_15s_1080x1920.mp4")
        subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error",
                        "-i", tmp, "-ss", str(t0), "-t", "15", "-i", audio,
                        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
                        "-shortest", "-movflags", "+faststart", out], check=True)
        print("teaser :", out, "(vers", i0, "->", i1, ")")
        return

    if args.assemble:
        segs = sorted([f for f in os.listdir(WORK) if f.startswith("clip_seg") and f.endswith(".mp4")],
                      key=lambda x: int(x[8:-4]))
        print("segments :", segs)
        lst = os.path.join(WORK, "clip_seg_list.txt")
        with open(lst, "w") as fh:
            for s in segs:
                fh.write(f"file '{os.path.join(WORK, s)}'\n")
        out = os.path.join(LIV, "Averly Morillo - MESIAS (clip lyrics 1080x1920).mp4")
        cmd = [FF, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
               "-i", lst, "-i", args.audio,
               "-map", "0:v:0", "-map", "1:a:0",
               "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
               "-shortest", "-movflags", "+faststart", out]
        subprocess.run(cmd, check=True)
        print("clip assemblé :", out)


if __name__ == "__main__":
    main()
