#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lit d'ambiance « calme » : 5 extraits posés du catalogue, 4,6 s chacun, fondus 0,5 s.
Sert de musique aux films CITATIONS / SERVICES (pas de voix off, pas d'IA vocale)."""
import json
import subprocess
import sys

import numpy as np

sys.path.insert(0, "/home/user/lyric/productions/pub-wtbw")
from build_pub_audio import FF, OUT, SR, decode  # noqa: E402

PRESET = ("mariage" if "--mariage" in sys.argv
          else "memoire" if "--memoire" in sys.argv
          else "anniversaire" if "--anniversaire" in sys.argv
          else "education" if "--education" in sys.argv else "calme")
SEG = {"mariage": 5.5, "memoire": 6.5, "anniversaire": 4.4, "education": 5.4}.get(PRESET, 4.6)
XF = 0.6 if PRESET == "memoire" else 0.4 if PRESET == "anniversaire" else 0.5
PARTS_MARIAGE = [
    ("Ayon dèkpè.mp3", 11.78),
    ("Tu es trop belle.mp3", 10.52),
    ("VIVI OOR.mp3", 8.63),
    ("Le goût bon de la vie.mp3", 9.95),
]
PARTS_MEMOIRE = [
    ("Mahu ti tebe Eng.mp3", 17.24),
    ("Entre tes mains.mp3", 5.14),
    ("Calm_in _off_down Daïsky.m4a", 24.82),
    ("Le goût bon de la vie.mp3", 9.95),
]
PARTS_ANNIV = [
    ("Noukiko tché wê.mp3", 6.82),
    ("Ça monte_ ça descend.mp3", 8.43),
    ("Gbètché vivi.mp3", 8.87),
    ("Le goût bon de la vie.mp3", 9.95),
]
PARTS_EDUC = [
    ("On a nous volé notre éducation.mp3", 7.51),
    ("Nan yi a ga djin wê.mp3", 8.43),
    ("Concentré sur le chemin.mp3", 11.42),
    ("je me relève toujours 3.mp3", 6.00),
]
PARTS = (PARTS_MARIAGE if PRESET == "mariage"
         else PARTS_MEMOIRE if PRESET == "memoire"
         else PARTS_ANNIV if PRESET == "anniversaire"
         else PARTS_EDUC if PRESET == "education" else [
    ("Mahu ti tebe Eng.mp3", 17.24),
    ("Calm_in _off_down Daïsky.m4a", 24.82),
    ("Le goût bon de la vie.mp3", 9.95),
    ("VIVI OOR.mp3", 8.63),
    ("Nonvi Konou.mp3", 6.29),
])


def main():
    parts = []
    for f, s in PARTS:
        x = decode(f, s, SEG)
        n = int(SEG * SR)
        if len(x) < n:
            x = np.pad(x, ((0, n - len(x)), (0, 0)))
        parts.append(x[:n])

    mix = np.zeros((0, 2), dtype=np.float32)
    n = int(XF * SR)
    for part in parts:
        if len(mix) == 0:
            mix = part
            continue
        p = np.linspace(0, 1, n, endpoint=False, dtype=np.float32)[:, None]
        mix = np.concatenate([mix[:-n],
                              mix[-n:] * np.cos(p * np.pi / 2) + part[:n] * np.sin(p * np.pi / 2),
                              part[n:]])

    dur = len(mix) / SR
    fade = int(1.2 * SR)
    mix[-fade:] *= np.linspace(1, 0, fade, dtype=np.float32)[:, None] ** 1.3
    mix[:int(0.4 * SR)] *= np.linspace(0, 1, int(0.4 * SR), dtype=np.float32)[:, None]

    base = {"mariage": "bed_mariage", "memoire": "bed_memoire", "anniversaire": "bed_anniversaire", "education": "bed_education"}.get(PRESET, "bed")
    open(f"{OUT}/cache/{base}.f32", "wb").write(mix.astype("<f4").tobytes())
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-f", "f32le", "-ar", str(SR),
                    "-ac", "2", "-i", f"{OUT}/cache/{base}.f32", "-c:a", "pcm_s24le",
                    f"{OUT}/cache/{base}.wav"], check=True)
    p1 = subprocess.run([FF, "-hide_banner", "-i", f"{OUT}/cache/{base}.wav", "-af",
                         "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                        capture_output=True, text=True, check=True)
    t = p1.stderr
    js = json.loads(t[t.rindex("{"): t.rindex("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}"
          f":measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}"
          f":offset={js['target_offset']}:linear=true,aresample=48000")
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-i", f"{OUT}/cache/{base}.wav",
                    "-af", af, "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
                    f"{OUT}/cache/{base}.m4a"], check=True)
    json.dump({"duration": round(dur, 3)}, open(f"{OUT}/cache/{base}.json", "w"))
    print(base, round(dur, 3), "s")


if __name__ == "__main__":
    main()
