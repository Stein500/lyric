#!/usr/bin/env python3
"""
Rendu clip 16:9 (1920x1080, 30 fps) — « Ça monte, ça descend » (Daïsky)

Reprend les MÊMES 5 fonds recadrés en 1376x768 paysage, mêmes timings, même audio.
Paroles base = H-170 = 910, endcard cx=0.38*W = 729.6.
"""
import json, os, subprocess, io, shutil
from pathlib import Path
import imageio_ffmpeg, numpy as np
from PIL import Image, ImageDraw, ImageFont

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

def load_fonds():
    files = sorted((ROOT / "assets/raw/landscape").glob("s*.png"))[:6]
    assert len(files) >= 6, f"6 fonds paysage attendus, trouvé {len(files)}"
    return [Image.open(f).convert("RGB") for f in files[:6]]

def recadre_fond(img, t_norm, phase):
    src_w, src_h = img.size
    scale = max(W / src_w, H / src_h)
    nw, nh = int(src_w * scale), int(src_h * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    z = 1.02 + 0.06 * (0.5 + 0.5 * np.sin(2 * np.pi * t_norm * 0.167))
    cw, ch = int(W * z), int(H * z)
    cx = (nw - cw) // 2 + int(40 * np.sin(2 * np.pi * t_norm * 0.083 + phase))
    cy = (nh - ch) // 2
    return img.crop((max(0, cx), max(0, cy), min(nw, cx + cw), min(nh, cy + ch))).resize((W, H), Image.LANCZOS)

def _font(name, size):
    for cand in [name, "/usr/share/fonts/truetype/dejavu/" + name, name.replace("ttf", "TTF")]:
        try: return ImageFont.truetype(cand, size)
        except: pass
    return ImageFont.load_default()

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

def scene_pour_t(t_audio):
    # 6 scènes ordonnées : porte (0-14) -> entree (14-46) -> danse (46-78) -> dj (78-106) -> pause (106-152) -> drop (152-fin)
    if 0 <= t_audio < 14.29: return 0          # s01 porte
    if 14.29 <= t_audio < 46.78: return 1      # s02 entrée
    if 46.78 <= t_audio < 78.69: return 2      # s03 danse
    if 78.69 <= t_audio < 106.72: return 3     # s04 dj
    if 106.72 <= t_audio < 152.25: return 4    # s05 pause
    return 5                                    # s06 drop (152.25 -> fin)

def render_frame(t_global, fonds, timings, fonts):
    t_audio = t_global - HOOK
    if t_global < HOOK:
        bg = recadre_fond(fonds[2], (t_global / HOOK) % 1.0, 0.0)  # danse = énergie hook
    elif t_audio >= DUREE_AUDIO:
        bg = recadre_fond(fonds[4], 1.0, 0.0)  # pause = endcard
    else:
        bg = recadre_fond(fonds[scene_pour_t(t_audio)], (t_global - HOOK) / DUREE_AUDIO, 0.5)
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for y in range(0, H, 4):
        dy = abs(y - (H - 170))
        a = max(0, min(110, int(110 * (1 - dy / 260))))
        sd.rectangle((0, y, W, y + 4), fill=(0, 0, 0, a))
    bg = Image.alpha_composite(bg.convert("RGBA"), scrim)
    draw = ImageDraw.Draw(bg)
    vers = timings["vers"]
    va = vers_actifs(vers, t_audio) if t_global >= HOOK else None
    if va is not None:
        idx, k, n, mots, t_deb, t_fin = va
        vers_dur = t_fin - t_deb
        # wrap à 1640 px de large
        max_w = 1640
        lines, cur = [], []
        for m in mots:
            test = " ".join(cur + [m])
            if draw.textlength(test, font=fonts["paroles"]) <= max_w and len(cur) < 8:
                cur.append(m)
            else:
                if cur: lines.append(" ".join(cur)); cur = [m]
        if cur: lines.append(" ".join(cur))
        line_h = 50
        # base y = H - 170 = 910
        y0 = H - 170 - line_h * len(lines)
        for li, line in enumerate(lines):
            mots_l = line.split()
            offsets = [0]
            for m in mots_l:
                offsets.append(offsets[-1] + draw.textlength(m + " ", font=fonts["paroles"]))
            for mi, m in enumerate(mots_l):
                global_idx = li * 8 + mi
                actif = global_idx == k
                col = (255, 215, 0, 255) if actif else (245, 230, 200, 220)
                t_in_vers = t_audio - t_deb
                y_wave = int(4.5 * np.sin(2 * np.pi * 0.9 * t_in_vers + mi * 0.4))
                draw.text((W//2 - int(draw.textlength(line, font=fonts["paroles"]))//2 + offsets[mi],
                           y0 + li * line_h + y_wave), m, font=fonts["paroles"], fill=col)
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
        draw.text((W//2 - int(w_)//2, H//2 - 30), msg, font=fi, fill=(255, 255, 255, int(255*a)))
    # Endcard paysage : cx = 0.38*W
    if t_audio >= DUREE_AUDIO:
        a = min(1.0, (t_audio - DUREE_AUDIO) / 0.5)
        dim = Image.new("RGBA", (W, H), (0, 0, 0, int(180 * a)))
        bg = Image.alpha_composite(bg.convert("RGBA"), dim)
        d3 = ImageDraw.Draw(bg)
        cx = int(0.38 * W)
        fti = fonts["ui_cursive"]
        titre = "Ça monte, ça descend"
        wt = d3.textlength(titre, font=fti)
        d3.text((cx - int(wt)//2, 320), titre, font=fti, fill=(255, 230, 180, int(255*a)))
        fm = fonts["ui_big"]
        merci = "Merci d'avoir regardé"
        wm = d3.textlength(merci, font=fm)
        d3.text((cx - int(wm)//2, 510), merci, font=fm, fill=(255, 255, 255, int(255*a)))
        fc = fonts["ui_code"]
        code = "9 - 7 - 6 - 1"
        wc = d3.textlength(code, font=fc)
        d3.text((cx - int(wc)//2, 590), code, font=fc, fill=(0, 230, 255, int(255*a)))
        sub = "la courbe qui monte, qui descend"
        ws = d3.textlength(sub, font=fonts["ui"])
        d3.text((cx - int(ws)//2, 740), sub, font=fonts["ui"], fill=(255, 255, 255, int(220*a)))
    return bg.convert("RGB")

def main():
    print(f"=== Rendu 16:9 — {N_FRAMES} frames, {TOTAL:.2f}s ===")
    (ROOT / "work").mkdir(exist_ok=True)
    (ROOT / "livrables").mkdir(exist_ok=True)
    fonds = load_fonds()
    with open(ROOT / "productions/ca_monte_ca_descend/timings_audited.json", encoding="utf-8") as f:
        timings = json.load(f)
    fonts = {
        "paroles": _font("BarlowCondensed-Bold.ttf", 48) or _font("DejaVuSans-Bold.ttf", 44),
        "ui": _font("DejaVuSans-Bold.ttf", 28),
        "ui_big": _font("DejaVuSans-Bold.ttf", 36),
        "ui_code": _font("DejaVuSans-Bold.ttf", 90),
        "ui_cursive": _font("GreatVibes-Regular.ttf", 110) or _font("DejaVuSans-Bold.ttf", 70),
    }
    proc = subprocess.Popen(
        [FFMPEG, "-y", "-f", "image2pipe", "-vcodec", "mjpeg", "-framerate", str(FPS), "-i", "-",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium",
         "-movflags", "+faststart", "work/rendu_16x9_silent.mp4"],
        stdin=subprocess.PIPE
    )
    for i in range(N_FRAMES):
        t = i / FPS
        if i % 60 == 0: print(f"  frame {i}/{N_FRAMES}  t={t:.2f}s")
        img = render_frame(t, fonds, timings, fonts)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=88)
        proc.stdin.write(buf.getvalue())
    proc.stdin.close()
    proc.wait()
    # Audio master déjà produit par rendu_9x16.py -> on le réutilise
    src = ROOT / "work/audio_master.wav"
    if not src.exists():
        # fallback : concat brute
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-ss", "53.32", "-t", "6.0",
                        "-i", "Ça monte_ ça descend.mp3", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", "work/hook.wav"], check=True)
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", "Ça monte_ ça descend.mp3",
                        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", "work/audio.wav"], check=True)
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
                        "-t", "5.0", "-c:a", "pcm_s16le", "work/silence.wav"], check=True)
        with open("work/audio_concat.txt", "w") as f:
            f.write("file 'hook.wav'\nfile 'audio.wav'\nfile 'silence.wav'\n")
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                        "-i", "work/audio_concat.txt", "-c:a", "pcm_s16le", "work/audio_final.wav"], check=True)
        # loudnorm 2 passes
        r1 = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-i", "work/audio_final.wav",
                            "-af", "loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json", "-f", "null", "-"],
                           capture_output=True, text=True)
        j = r1.stderr[r1.stderr.rfind("{"): r1.stderr.rfind("}")+1]
        info = json.loads(j)
        offset = float(info["target_offset"])
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", "work/audio_final.wav",
                        "-af", f"loudnorm=I=-14:TP=-1.8:LRA=11:measured_I={info['input_i']}:"
                               f"measured_TP={info['input_tp']}:measured_LRA={info['input_lra']}:"
                               f"measured_thresh={info['input_thresh']}:offset={offset}:linear=true",
                        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", "work/audio_master.wav"], check=True)
    fade_start = TOTAL - 3.0
    out_mp4 = "livrables/Ca_monte_ca_descend_16x9_v1.mp4"
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
    qa = {"frames": N_FRAMES, "fps": FPS, "duree_s": round(N_FRAMES/FPS, 3), "total_s": round(TOTAL, 3)}
    with open("work/qa_landscape.json", "w", encoding="utf-8") as f:
        json.dump(qa, f, indent=2, ensure_ascii=False)
    print("QA :", qa)

if __name__ == "__main__":
    main()
