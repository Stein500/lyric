#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RENDU COMPLET — « Dès le début » (Daïsky)
Timeline = cold-open (refrain-titre) + chanson 199,99 s + 5 s de fin (endcard).
· paroles : centrées, mot à mot hybride, badge Dsky + drapeau en fondu par vers
· clochettes CTA dans toutes les fenêtres ≥ 5 s sans parole (fenêtres auditées)
· bandeau Bénin 54 px, Ken Burns + respiration sur les fonds
· endcard : titre + artiste + WhatsApp + e-mail + badge
Sortie : livrables/Des_le_debut_9x16.mp4 (+ audio master 48 k)

Usage : rendu_complet.py [--format 9x16|16x9] [--debut 0] [--duree 20] [--sortie chemin]
"""
import argparse, io, json, math, os, re, subprocess, sys, time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moteur_maquette as mm

HERE = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.abspath(os.path.join(HERE, ".."))
ROOT = mm.ROOT
FFMPEG = mm.FFMPEG

HOOK_A, HOOK_B = 52.11, 58.96          # coupe naturelle sur le refrain-titre
SONG = 199.99
APAD = 5.0
HOOK = round(HOOK_B - HOOK_A, 3)       # 6,85 s

# --- musique : quelle scène à quel moment de la chanson
SCENES_SONG = [
    (0.00,   5.68, "s01_piece_vide_aube"),
    (5.68,  19.43, "s02_homme_entre_croix"),
    (19.43, 29.03, "s03_croix_posee_tabouret"),
    (29.03, 40.87, "s04_mains_tatouees_jointes"),
    (40.87, 48.60, "s05_femme_rai_de_lumiere"),
    (48.60, 62.56, "s06_duo_dans_les_rayons"),
    (62.56, 68.25, "s01_piece_vide_aube"),
    (68.25, 78.89, "s07_femme_leve_les_yeux"),
    (78.89, 89.75, "s08_mains_vers_la_lumiere"),
    (89.75,100.16, "s09_elle_marche_vers_la_lumiere"),
    (100.16,105.85,"s06_duo_dans_les_rayons"),
    (105.85,116.54,"s11_poussiere_silhouettes_de_dos"),
    (116.54,126.61,"s12_agenouilles_ensemble"),
    (126.61,140.00,"s13_mains_serrees_ensemble"),
    (140.00,151.82,"s14_ils_se_relevent_lumiere_doree"),
    (151.82,169.18,"s15_bras_leves_paumes_ciel"),
    (169.18,171.65,"s18_croix_au_sol_dust_mote"),
    (171.65,183.00,"s17_immobiles_lumiere_decline"),
    (183.00,193.00,"s19_porte_se_referme"),
    (193.00,199.99,"s18_croix_au_sol_dust_mote"),
]
SCENES_HOOK = [("s15_bras_leves_paumes_ciel", HOOK_A, HOOK_B)]
SCENE_ENDCARD = "s20_endcard_piece_sombre"

# fenêtres clochettes (issues de l'audit : ≥ 5 s sans parole) — mise à jour au démarrage
def build_cta_windows():
    p = os.path.join(PROD, "timings_audited.json")
    wins = []
    if os.path.exists(p):
        d = json.load(open(p, encoding="utf-8"))
        wins = [(w["debut"], w["fin"]) for w in d.get("fenetres_cta_5s", [])]
    # fenêtre finale (outro) ajoutée par le moteur complet
    last = mm.VERSES[-1]
    fin = last[0] + mm.display_duration(len(last[1].split()))
    if SONG - fin >= 5.0:
        wins.append((round(fin, 2), SONG))
    return wins

CTA_WINDOWS = build_cta_windows()
mm.CTA_WINDOWS = CTA_WINDOWS


def scene_at_song(song_t):
    for k, (a, b, slot) in enumerate(SCENES_SONG):
        if a <= song_t < b:
            return k, slot, (song_t - a) / max(1e-6, b - a)
    k = len(SCENES_SONG) - 1
    return k, SCENES_SONG[-1][2], 1.0


def load_canvases(w, h, scenes):
    os.makedirs("/tmp/canvas_cache", exist_ok=True)
    cache = {}
    for slot in scenes:
        for fmt in ("portrait", "paysage") if (w, h) == (1080, 1920) or True else ("paysage",):
            p = os.path.join(PROD, "fonds", fmt, slot + ".jpg")
            if not os.path.exists(p):
                continue
            key = (slot, w, h)
            if key in cache:
                continue
            cw, ch = int(w * mm.CANVAS), int(h * mm.CANVAS)
            im = Image.open(p).convert("RGB").resize((cw, ch), Image.LANCZOS)
            cache[key] = np.asarray(im, dtype=np.uint8)
            break
    return cache


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--format", default="9x16", choices=["9x16", "16x9"])
    ap.add_argument("--debut", type=float, default=0.0, help="début sur la timeline finale (s)")
    ap.add_argument("--duree", type=float, default=None)
    ap.add_argument("--sortie", default=None)
    ap.add_argument("--crf", type=int, default=21)
    ap.add_argument("--sans-audio", action="store_true")
    a = ap.parse_args()

    W, H = (1080, 1920) if a.format == "9x16" else (1920, 1080)
    mm.W, mm.H = W, H
    mm.CENTRE_Y = H // 2
    # recompute des sprites à la bonne largeur
    mm.MAXW = 720 if a.format == "9x16" else 1300
    mm.BAND = mm.benin_band(54 if a.format == "9x16" else 30)
    mm.SCRIM = mm.make_scrim()

    total = HOOK + SONG + APAD
    t_start = a.debut
    t_end = total if a.duree is None else min(total, a.debut + a.duree)
    n_frames = int(round((t_end - t_start) * mm.FPS))
    out = a.sortie or os.path.join(ROOT, "livrables", f"Des_le_debut_{a.format}.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)

    all_slots = [s for _, _, s in SCENES_SONG] + [s for s, _, _ in SCENES_HOOK] + [SCENE_ENDCARD]
    canvases = load_canvases(W, H, set(all_slots))
    print(f"{a.format} · {n_frames} frames · scènes {len(canvases)} · clochettes {len(CTA_WINDOWS)} fenêtres", flush=True)

    # ---------------------------------------------------------------- audio
    wav = "/tmp/rendu_audio.wav"
    if not a.sans_audio:
        def seg(ss, t, dst):
            subprocess.run([FFMPEG, "-v", "error", "-y", "-ss", f"{ss}", "-t", f"{t}", "-i", mm.AUDIO,
                            "-map", "0:a:0", "-vn", "-ar", "48000", "-ac", "2", dst], check=True)
        seg(HOOK_A, HOOK, "/tmp/hook.wav")
        seg(0, SONG, "/tmp/song.wav")
        subprocess.run([FFMPEG, "-v", "error", "-y", "-f", "lavfi", "-t", f"{APAD}",
                        "-i", "anullsrc=r=48000:cl=stereo", "-ar", "48000", "-ac", "2", "/tmp/apad.wav"], check=True)
        subprocess.run([FFMPEG, "-v", "error", "-y", "-i", "/tmp/hook.wav", "-i", "/tmp/song.wav", "-i", "/tmp/apad.wav",
                        "-filter_complex", "[0:a][1:a][2:a]concat=n=3:v=0:a=1[a]", "-map", "[a]", wav], check=True)
        # loudnorm 2 passes + fondu final 3 s
        p1 = subprocess.run([FFMPEG, "-hide_banner", "-i", wav, "-af",
                             "highpass=30,lowpass=18000,loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json",
                             "-f", "null", "-"], capture_output=True, text=True)
        m = re.search(r"\{[^{}]*input_i[^{}]*\}", p1.stderr, re.S)
        off = 0.0
        if m:
            try:
                off = float(json.loads(m.group(0)).get("target_offset", 0.0))
            except Exception:
                off = 0.0
        fade = f"afade=t=out:st={max(0.0,total-3.0):.2f}:d=3"
        subprocess.run([FFMPEG, "-v", "error", "-y", "-i", wav, "-af",
                        f"highpass=30,lowpass=18000,loudnorm=I=-14:TP=-1.8:LRA=11:offset={off:.2f},{fade}",
                        "-ar", "48000", "-ac", "2", "/tmp/audio_final.wav"], check=True)
        print(f"audio prêt (offset loudnorm {off:+.2f})", flush=True)

    # ---------------------------------------------------------------- encodage
    cmd = [FFMPEG, "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(mm.FPS), "-i", "-"]
    if not a.sans_audio:
        cmd += ["-i", "/tmp/audio_final.wav"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", str(a.crf), "-pix_fmt", "yuv420p",
            "-profile:v", "high", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
    cmd += ["-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out]
    pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    t0 = time.time()
    for i in range(n_frames):
        g = t_start + i / mm.FPS
        if g < HOOK:
            song_t = HOOK_A + g
            kind = "hook"
        elif g < HOOK + SONG:
            song_t = g - HOOK
            kind = "song"
        else:
            song_t = SONG
            kind = "end"
        # fond
        if kind == "hook":
            k, slot, u = 0, SCENE_ENDCARD if False else SCENES_HOOK[0][0], (song_t - HOOK_A) / HOOK
        elif kind == "song":
            k, slot, u = scene_at_song(song_t)
        else:
            k, slot, u = 99, SCENE_ENDCARD, (g - HOOK - SONG) / APAD
        arr = canvases[(slot, mm.W, mm.H)]
        fr = mm.render_bg_from(arr, u, k, g)          # Ken Burns + pan + respiration
        # textes + badge
        if kind != "end":
            for vp in mm.VERSES_PREP:
                fr = mm.compose_badge(fr, vp, song_t)
                fr = mm.compose_verse(fr, vp, song_t)
            fr = mm.compose_cta(fr, song_t, g)
        else:
            fr = mm.compose_endcard(fr, (g - HOOK - SONG) / APAD)
        # bandeau Bénin (pas sur l'endcard : le bandeau y est aussi, règle v5.5)
        band = mm.BAND
        fr[mm.H - band.shape[0]:mm.H] = band
        # fondu final vidéo (3 s)
        rem = total - g
        if rem < 3.0:
            f = max(0.0, rem / 3.0)
            fr = fr * f
        img = Image.fromarray(np.clip(fr, 0, 255).astype(np.uint8))
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=92)
        pipe.stdin.write(buf.getvalue())
        if i % 150 == 0:
            el = time.time() - t0
            eta = el / max(1, i + 1) * (n_frames - i - 1)
            print(f"  {i}/{n_frames}  ({el:5.0f}s écoulées, ~{eta/60:4.1f} min restantes)", flush=True)
    pipe.stdin.close()
    pipe.wait()
    print("rendu:", out, os.path.getsize(out) // 1024 // 1024, "Mo", flush=True)


if __name__ == "__main__":
    main()
