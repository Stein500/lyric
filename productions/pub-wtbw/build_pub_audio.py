#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PUB WTBW — montage des hooks du catalogue (30 s).
Chaque segment = 1,50 s pris sur le premier hook chanté du morceau.
Audio de l'artiste intact, simple montage + normalisation -14 LUFS.
"""
import json
import subprocess

import numpy as np
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = "/home/user/lyric"
OUT = f"{ROOT}/productions/pub-wtbw"
SR = 48000
SEG = 1.50

# (fichier, départ, titre affiché)
SEGMENTS = [
    ("Noukiko tché wê.mp3", 6.82, "WOLOF TECHSTEIN BEAT WÊ"),
    ("Monster _ Daïsky.m4a", 3.77, "MONSTER POSITIVE"),
    ("Noukiko tché wê.mp3", 10.61, "NOUKIKO TCHÉ WÊ"),
    ("Ayon dèkpè.mp3", 11.78, "AYON DÈKPÈ"),
    ("Tu es trop belle.mp3", 10.52, "TU ES TROP BELLE"),
    ("Gbètché vivi.mp3", 8.87, "GBÈTCHÉ VIVI"),
    ("Nan yi a ga djin wê.mp3", 8.43, "NAN YI A GA DJIN WÊ"),
    ("Concentré sur le chemin.mp3", 11.42, "CONCENTRÉ SUR LE CHEMIN"),
    ("Sanguin.mp3", 8.31, "SANGUIN"),
    ("On a nous volé notre éducation.mp3", 7.51, "ON NOUS A VOLÉ NOTRE ÉDUCATION"),
    ("Ça monte_ ça descend.mp3", 8.43, "ÇA MONTE, ÇA DESCEND"),
    ("Le goût bon de la vie.mp3", 9.95, "LE GOÛT BON DE LA VIE"),
    ("Mahu ti tebe Eng.mp3", 17.24, "MAHU TI TÈ GBÈ"),
    ("VIVI OOR.mp3", 8.63, "VIVI O O R"),
    ("Glace - Daïsky.mp3", 14.17, "GLACE"),
    ("Goinfres.mp3", 14.54, "GOINFRES"),
    ("Drague moi 1.mp3", 14.12, "DRAGUE MOI"),
    ("Dès le début.mp3", 12.56, "DÈS LE DÉBUT"),
    ("Calm_in _off_down Daïsky.m4a", 24.82, "CALM IN OFF DOWN"),
    ("Nonvi Konou.mp3", 6.29, "NONVI KONOU"),
]
XF = 0.06


def decode(path, start, dur):
    raw = subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-i", f"{ROOT}/{path}",
                          "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-vn", "-ac", "2",
                          "-ar", str(SR), "-f", "f32le", "-acodec", "pcm_f32le", "pipe:1"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype="<f4").reshape(-1, 2).astype(np.float32)


def main():
    parts = []
    for f, s, title in SEGMENTS:
        x = decode(f, s, SEG)
        if len(x) < int(SEG * SR):
            x = np.pad(x, ((0, int(SEG * SR) - len(x)), (0, 0)))
        parts.append(x[: int(SEG * SR)])

    mix = np.zeros((0, 2), dtype=np.float32)
    n = int(XF * SR)
    for part in parts:
        if len(mix) == 0:
            mix = part
            continue
        p = np.linspace(0, 1, n, endpoint=False, dtype=np.float32)[:, None]
        a = mix[-n:] * np.cos(p * np.pi / 2)
        b = part[:n] * np.sin(p * np.pi / 2)
        mix = np.concatenate([mix[:-n], a + b, part[n:]])

    dur = len(mix) / SR
    mix = np.concatenate([np.zeros((int(0.004 * SR), 2), np.float32), mix])
    n_out = int(0.8 * SR)
    mix[-n_out:] *= np.linspace(1, 0, n_out, dtype=np.float32)[:, None] ** 1.3

    open(f"{OUT}/cache/pub.f32", "wb").write(mix.astype("<f4").tobytes())
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-f", "f32le", "-ar", str(SR),
                    "-ac", "2", "-i", f"{OUT}/cache/pub.f32", "-c:a", "pcm_s24le",
                    f"{OUT}/cache/pub.wav"], check=True)

    p1 = subprocess.run([FF, "-hide_banner", "-i", f"{OUT}/cache/pub.wav", "-af",
                         "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                        capture_output=True, text=True, check=True)
    t = p1.stderr
    js = json.loads(t[t.rindex("{"): t.rindex("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}"
          f":measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}"
          f":offset={js['target_offset']}:linear=true,aresample=48000")
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-i", f"{OUT}/cache/pub.wav",
                    "-af", af, "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
                    f"{OUT}/cache/pub.m4a"], check=True)
    json.dump({"duration": round(dur, 3), "seg": SEG, "titles": [t for _, _, t in SEGMENTS]},
              open(f"{OUT}/cache/pub.json", "w"), ensure_ascii=False, indent=2)
    print("durée", round(dur, 3), "| segments", len(SEGMENTS))


if __name__ == "__main__":
    main()
