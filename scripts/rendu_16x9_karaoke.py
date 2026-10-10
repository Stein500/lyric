#!/usr/bin/env python3
"""
Rendu clip 16:9 (1920x1080, 30 fps) — « Ça monte, ça descend » (Daïsky)
VERSION KARAOKÉ : paroles TRÈS GRANDES (92 px en mode actif, 78 px en inactif)
                    20 fonds portrait recadrés 16:9, action continue.
                    Héros masculin validé, AUCUN contenu sexuel.

Entrée :
  - assets/raw/portrait/s{01..20}_*.png  (20 fonds portrait 9:16, recadrés en 16:9)
  - Ça monte_ ça descend.mp3
  - productions/ca_monte_ca_descend/timings_audited.json

Sortie :
  - work/rendu_16x9_silent.mp4
  - livrables/Ca_monte_ca_descend_16x9_v2.mp4
  - work/qa_landscape.json
"""
import json, os, subprocess, io
from pathlib import Path
import imageio_ffmpeg, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

W, H = 1920, 1080
FPS = 30
DUREE_AUDIO = 197.64
HOOK = 6.0
APAD = 5.0
TOTAL = HOOK + DUREE_AUDIO + APAD
N_FRAMES = int(np.ceil(TOTAL * FPS))

# ---------- Fonds portrait 9:16 recadrés en 16:9 ----------
def load_fonds():
    files = sorted((ROOT / "assets/raw/portrait").glob("s*.png"))[:20]
    assert len(files) >= 11, f"Au moins 11 fonds attendus, trouvé {len(files)}"
    return [Image.open(f).convert("RGB") for f in files]

def recadre_fond(img, t_norm, phase):
    """Recadre une image portrait 9:16 en 16:9 (crop centre) + Ken Burns."""
    src_w, src_h = img.size
    # Pour 16:9, on garde toute la largeur et on crop verticalement
    # src = 9:16 (h > w), cible = 16:9 (w > h) -> on prend pleine largeur et on crop haut/bas
    target_ratio = W / H  # 1.778
    src_ratio = src_w / src_h
    if src_ratio < target_ratio:
        # image plus haute que large -> crop haut/bas
        new_h = int(src_w / target_ratio)
        img = img.crop((0, (src_h - new_h) // 2, src_w, (src_h + new_h) // 2))
    else:
        new_w = int(src_h * target_ratio)
        img = img.crop(((src_w - new_w) // 2, 0, (src_w + new_w) // 2, src_h))
    # Maintenant img est en 16:9
    sw, sh = img.size
    z = 1.02 + 0.06 * (0.5 + 0.5 * np.sin(2 * np.pi * t_norm * 0.167))
    nw, nh = int(sw * z), int(sh * z)
    img = img.resize((nw, nh), Image.LANCZOS)
    cx = (nw - W) // 2 + int(30 * np.sin(2 * np.pi * t_norm * 0.083 + phase))
    cy = (nh - H) // 2
    return img.crop((max(0, cx), max(0, cy),
                     min(nw, cx + W), min(nh, cy + H))).resize((W, H), Image.LANCZOS)

# ---------- Polices ----------
def _font(name, size):
    for cand in [name, "/usr/share/fonts/truetype/dejavu/" + name, name.replace("ttf", "TTF")]:
        try: return ImageFont.truetype(cand, size)
        except: pass
    return ImageFont.load_default()

# ---------- Timings ----------
def load_timings():
    with open(ROOT / "productions/ca_monte_ca_descend/timings_audited.json", encoding="utf-8") as f:
        return json.load(f)

def vers_actifs(vers, t_audio):
    if t_audio < 0: return None
    for i, v in enumerate(vers):
        t = v["t"]
        nxt = vers[i+1]["t"] if i+1 < len(vers) else t + 1.5
        if t <= t_audio < nxt:
            mots = v["texte"].split()
            if not mots: return (i, 0, 0, mots, t, nxt)
            frac = (t_audio - t) / max(1e-3, nxt - t)
            k = min(len(mots) - 1, int(frac * len(mots)))
            return (i, k, len(mots), mots, t, nxt)
    return None

# ---------- Mapping 20 fonds sur la timeline ----------
# 20 sections RMS déjà identifiées dans ANALYSE.md
# On répartit les 20 frames proportionnellement à la durée (intro 14s, etc.)
def scene_pour_t(t_audio, n_fonds=20):
    """Répartit n_fonds sur 0..DUREE_AUDIO selon les sections RMS."""
    # Sections de l'ANALYSE.md avec leur position
    sections = [
        (0.0, 14.29, 0.08),       # intro
        (14.29, 27.30, 0.15),     # couplet 1a
        (27.30, 39.30, 0.15),     # couplet 1b
        (39.30, 46.78, 0.15),     # couplet 1c
        (46.78, 64.40, 0.19),     # refrain 1a
        (64.40, 78.69, 0.19),     # refrain 1b
        (78.69, 90.40, 0.17),     # couplet 2a
        (90.40, 101.80, 0.17),    # couplet 2b
        (101.80, 107.00, 0.17),   # couplet 2c
        (107.00, 112.70, 0.20),   # refrain 2a
        (112.70, 128.10, 0.20),   # refrain 2b
        (128.10, 134.80, 0.20),   # fin refrain 2
        (134.80, 140.00, 0.15),   # pont a
        (140.00, 152.25, 0.15),   # pont b
        (152.25, 161.30, 0.21),   # refrain 3a
        (161.30, 168.40, 0.21),   # refrain 3b
        (168.40, 175.80, 0.21),   # refrain 3c
        (175.80, 187.20, 0.20),   # outro a
        (187.20, 193.30, 0.20),   # outro b
        (193.30, 197.64, 0.20),   # queue finale
    ]
    for i, (a, b, _) in enumerate(sections):
        if a <= t_audio < b:
            return min(i, n_fonds - 1)
    return n_fonds - 1

# ---------- Rendu ----------
def render_frame(t_global, fonds, timings, fonts):
    t_audio = t_global - HOOK
    n = len(fonds)
    if t_global < HOOK:
        # HOOK : on prend la scène la plus énergétique
        idx_hook = min(7, n-1)  # s08 bras levés
        bg = recadre_fond(fonds[idx_hook], (t_global / HOOK) % 1.0, 0.0)
    elif t_audio >= DUREE_AUDIO:
        # endcard : s20 aube
        idx_end = min(19, n-1)
        bg = recadre_fond(fonds[idx_end], 1.0, 0.0)
    else:
        scene_idx = scene_pour_t(t_audio, n)
        bg = recadre_fond(fonds[scene_idx], (t_global - HOOK) / DUREE_AUDIO, scene_idx * 0.3)
    # Scrim bas pour lisibilité paroles
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for y in range(0, H, 4):
        dy = abs(y - (H - 200))
        a = max(0, min(140, int(140 * (1 - dy / 280))))
        sd.rectangle((0, y, W, y + 4), fill=(0, 0, 0, a))
    bg = Image.alpha_composite(bg.convert("RGBA"), scrim)
    draw = ImageDraw.Draw(bg)
    # ---- Paroles KARAOKÉ gros mots ----
    vers = timings["vers"]
    va = vers_actifs(vers, t_audio) if t_global >= HOOK else None
    if va is not None:
        idx, k, n_mots, mots, t_deb, t_fin = va
        vers_dur = t_fin - t_deb
        # Wrap : largeur max 1700 px avec police 92 px
        max_w = 1700
        lines, cur = [], []
        for m in mots:
            test = " ".join(cur + [m])
            if draw.textlength(test, font=fonts["paroles"]) <= max_w and len(cur) < 5:
                cur.append(m)
            else:
                if cur: lines.append(" ".join(cur)); cur = [m]
        if cur: lines.append(" ".join(cur))
        line_h = 105  # 92 px de base + interligne
        y0 = H - 200 - line_h * len(lines)  # base = H-200 (safe)
        for li, line in enumerate(lines):
            mots_l = line.split()
            # Pré-calcul offsets avec la police normale
            offsets = [0]
            for m in mots_l:
                offsets.append(offsets[-1] + draw.textlength(m + " ", font=fonts["paroles"]))
            line_w = draw.textlength(line, font=fonts["paroles"])
            x0 = W//2 - int(line_w)//2
            for mi, m in enumerate(mots_l):
                global_idx = li * 5 + mi
                actif = global_idx == k
                # Taille : mot actif 110 px (1,2×), mot courant 92 px, mot passé 78 px (85%)
                if actif:
                    fnt = fonts["paroles_big"]
                    col = (255, 230, 90, 255)  # or vif
                    stroke_w = 8
                else:
                    age = k - global_idx
                    if age < 0:
                        # mot futur (pas encore arrivé)
                        fnt = fonts["paroles_future"]
                        col = (180, 180, 200, 160)
                    else:
                        # mot passé
                        fnt = fonts["paroles_past"]
                        col = (230, 230, 230, 200)
                    stroke_w = 6
                # Vague d'eau
                t_in_vers = t_audio - t_deb
                y_wave = int(4.5 * np.sin(2 * np.pi * 0.9 * t_in_vers + mi * 0.4))
                # Contour noir + texte
                for dx in range(-stroke_w, stroke_w+1, 2):
                    for dy in range(-stroke_w, stroke_w+1, 2):
                        if dx*dx + dy*dy <= stroke_w*stroke_w:
                            draw.text((x0 + offsets[mi] + dx, y0 + li * line_h + y_wave + dy),
                                      m, font=fnt, fill=(0, 0, 0, 220))
                draw.text((x0 + offsets[mi], y0 + li * line_h + y_wave), m, font=fnt, fill=col)
        # Badge top-left
        t_vers = t_audio - t_deb
        a_in = min(1.0, t_vers / 0.4)
        a_out = min(1.0, (vers_dur - t_vers) / 0.4)
        op = max(0.0, min(1.0, a_in, a_out)) * 0.75
        if op > 0.05:
            badge = Image.open(ROOT / "assets/overlays/badge_dsky.png").convert("RGBA")
            badge.putalpha(badge.split()[3].point(lambda p: int(p * op)))
            bg.paste(badge, (40, 40), badge)
    # Carton intro
    if t_global < 2.0:
        a = min(1.0, t_global / 0.3) * min(1.0, (2.0 - t_global) / 0.3)
        fi = fonts["ui"]
        msg = "Regarde jusqu'à la fin pour découvrir comment proposer un son ou un lyrics à réaliser pour toi !"
        w_ = draw.textlength(msg, font=fi)
        # contour
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                draw.text((W//2 - int(w_)//2 + dx, H//2 - 30 + dy), msg, font=fi, fill=(0, 0, 0, int(200*a)))
        draw.text((W//2 - int(w_)//2, H//2 - 30), msg, font=fi, fill=(255, 255, 255, int(255*a)))
    # Endcard
    if t_audio >= DUREE_AUDIO:
        a = min(1.0, (t_audio - DUREE_AUDIO) / 0.5)
        dim = Image.new("RGBA", (W, H), (0, 0, 0, int(200 * a)))
        bg = Image.alpha_composite(bg.convert("RGBA"), dim)
        d3 = ImageDraw.Draw(bg)
        cx = int(0.38 * W)
        fti = fonts["ui_cursive"]
        titre = "Ça monte, ça descend"
        wt = d3.textlength(titre, font=fti)
        d3.text((cx - int(wt)//2, 280), titre, font=fti, fill=(255, 230, 180, int(255*a)))
        fm = fonts["ui_big"]
        merci = "Merci d'avoir regardé"
        wm = d3.textlength(merci, font=fm)
        d3.text((cx - int(wm)//2, 480), merci, font=fm, fill=(255, 255, 255, int(255*a)))
        fc = fonts["ui_code"]
        code = "9 - 7 - 6 - 1"
        wc = d3.textlength(code, font=fc)
        d3.text((cx - int(wc)//2, 580), code, font=fc, fill=(0, 230, 255, int(255*a)))
        sub = "la courbe qui monte, qui descend"
        ws = d3.textlength(sub, font=fonts["ui"])
        d3.text((cx - int(ws)//2, 760), sub, font=fonts["ui"], fill=(255, 255, 255, int(220*a)))
    return bg.convert("RGB")

def main():
    print(f"=== Rendu 16:9 KARAOKÉ — {N_FRAMES} frames, {TOTAL:.2f}s ===")
    (ROOT / "work").mkdir(exist_ok=True)
    (ROOT / "livrables").mkdir(exist_ok=True)
    fonds = load_fonds()
    print(f"  {len(fonds)} fonds chargés")
    with open(ROOT / "productions/ca_monte_ca_descend/timings_audited.json", encoding="utf-8") as f:
        timings = json.load(f)
    # Polices KARAOKÉ : 92 px base, 110 px actif, 78 px passé, 78 px futur
    fonts = {
        "paroles": _font("DejaVuSans-Bold.ttf", 92),       # base
        "paroles_big": _font("DejaVuSans-Bold.ttf", 110),  # actif (1,2x)
        "paroles_past": _font("DejaVuSans-Bold.ttf", 78),  # passé
        "paroles_future": _font("DejaVuSans-Bold.ttf", 78),# futur
        "ui": _font("DejaVuSans-Bold.ttf", 28),
        "ui_big": _font("DejaVuSans-Bold.ttf", 44),
        "ui_code": _font("DejaVuSans-Bold.ttf", 120),
        "ui_cursive": _font("GreatVibes-Regular.ttf", 130) or _font("DejaVuSans-Bold.ttf", 80),
    }
    # Vérif police chargée
    print(f"  Police base chargée : {fonts['paroles'].font}")
    proc = subprocess.Popen(
        [FFMPEG, "-y", "-f", "image2pipe", "-vcodec", "mjpeg", "-framerate", str(FPS), "-i", "-",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium",
         "-movflags", "+faststart", "work/rendu_16x9_silent.mp4"],
        stdin=subprocess.PIPE
    )
    t0 = 0.0
    for i in range(N_FRAMES):
        t = i / FPS
        if i % 60 == 0: print(f"  frame {i}/{N_FRAMES}  t={t:.2f}s")
        img = render_frame(t, fonds, timings, fonts)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=88)
        proc.stdin.write(buf.getvalue())
    proc.stdin.close()
    proc.wait()
    print("Vidéo 16:9 muette OK")
    # ---------- Audio master (refait pour v2) ----------
    audio_path = "Ça monte_ ça descend.mp3"
    # Découpe + apad
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-ss", "53.32", "-t", "6.0",
                    "-i", audio_path, "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", "work/hook.wav"], check=True)
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", audio_path,
                    "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", "work/audio.wav"], check=True)
    subprocess.run([FFMPEG, "-y", "-loglevel", "error",
                    "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
                    "-t", "5.0", "-c:a", "pcm_s16le", "work/silence.wav"], check=True)
    with open("work/audio_concat.txt", "w") as f:
        f.write("file 'hook.wav'\nfile 'audio.wav'\nfile 'silence.wav'\n")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", "work/audio_concat.txt", "-c:a", "pcm_s16le", "work/audio_final.wav"], check=True)
    # Loudnorm 2 passes
    r1 = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-i", "work/audio_final.wav",
                        "-af", "loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    j = r1.stderr[r1.stderr.rfind("{"): r1.stderr.rfind("}")+1]
    info = json.loads(j)
    offset = float(info["target_offset"])
    print(f"  Loudnorm: input_i={info['input_i']} offset={offset}")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", "work/audio_final.wav",
                    "-af", f"loudnorm=I=-14:TP=-1.8:LRA=11:measured_I={info['input_i']}:"
                           f"measured_TP={info['input_tp']}:measured_LRA={info['input_lra']}:"
                           f"measured_thresh={info['input_thresh']}:offset={offset}:linear=true",
                    "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", "work/audio_master.wav"], check=True)
    # Mux final
    fade_start = TOTAL - 3.0
    out_mp4 = "livrables/Ca_monte_ca_descend_16x9_v2.mp4"
    subprocess.run([FFMPEG, "-y", "-loglevel", "error",
                    "-i", "work/rendu_16x9_silent.mp4", "-i", "work/audio_master.wav",
                    "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "libx264", "-crf", "19", "-preset", "medium",
                    "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k",
                    "-af", f"afade=t=out:st={fade_start}:d=3",
                    "-vf", f"fade=t=out:st={fade_start}:d=3",
                    "-movflags", "+faststart", "-shortest", out_mp4], check=True)
    print(f"Livré : {out_mp4}  taille : {os.path.getsize(out_mp4)//(1024*1024)} Mo")
    qa = {"frames": N_FRAMES, "fps": FPS, "duree_s": round(N_FRAMES/FPS, 3),
          "total_s": round(TOTAL, 3), "n_fonds": len(fonds),
          "taille_parole_base_px": 92, "taille_parole_actif_px": 110}
    with open("work/qa_landscape.json", "w", encoding="utf-8") as f:
        json.dump(qa, f, indent=2, ensure_ascii=False)
    print("QA :", qa)

if __name__ == "__main__":
    main()
