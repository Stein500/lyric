#!/usr/bin/env python3
"""Medley des 3 refrains (Noukiko tché wê / Ayon dèkpè / Tu es trop belle)
pour « IMELDA · 13 NOVEMBRE » — audio de l'artiste intact, aucun son généré.

Coupes posées sur les onsets/beats mesurés avec librosa :
  Noukiko 136 BPM     -> 10.70 .. 28.84
  Ayon    117.45 BPM  -> 65.53 .. 79.99
  Tropbelle 143.55 BPM-> 79.71 .. 105.30
Fondu enchaîné égal-puissance 0,12 s (anti-clic, pas de chevauchement audible).
"""
import json
import subprocess
import sys
import numpy as np
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
SR = 48000
ROOT = "/home/user/lyric"
OUT = f"{ROOT}/productions/imelda-13-novembre"

SEGMENTS = [
    ("Noukiko tché wê.mp3", 10.70, 28.84),
    ("Ayon dèkpè.mp3", 65.53, 79.99),
    ("Tu es trop belle.mp3", 79.71, 105.30),
]
XFADE = 0.12


def decode(path, start, dur, sr=SR):
    cmd = [FF, "-hide_banner", "-loglevel", "error", "-i", f"{ROOT}/{path}",
           "-ss", f"{start:.4f}", "-t", f"{dur:.4f}", "-vn",
           "-ac", "2", "-ar", str(sr), "-f", "f32le", "-acodec", "pcm_f32le", "pipe:1"]
    raw = subprocess.run(cmd, check=True, capture_output=True).stdout
    x = np.frombuffer(raw, dtype="<f4").reshape(-1, 2).astype(np.float32)
    return x


def main():
    parts = []
    for f, a, b in SEGMENTS:
        x = decode(f, a, b - a)
        print(f"{f}: {len(x)/SR:.3f}s  peak={np.abs(x).max():.3f}")
        parts.append(x)

    # chaîne avec fondus enchaînés égal-puissance
    mix = parts[0]
    for nxt in parts[1:]:
        n = int(round(XFADE * SR))
        p = np.linspace(0, 1, n, endpoint=False, dtype=np.float32)[:, None]
        a = mix[-n:] * np.cos(p * np.pi / 2)
        b = nxt[:n] * np.sin(p * np.pi / 2)
        mix = np.concatenate([mix[:-n], a + b, nxt[n:]])

    # sécurité : silence anti-clic 5 ms + fondu de sortie doux
    mix = np.concatenate([np.zeros((int(0.005 * SR), 2), np.float32), mix])
    mix[: int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR), dtype=np.float32)[:, None]

    dur = len(mix) / SR
    with open(f"{OUT}/cache/medley-raw.f32", "wb") as fh:
        fh.write(mix.astype("<f4").tobytes())

    # WAV 48k stéréo 24 bits
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error",
                    "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", f"{OUT}/cache/medley-raw.f32",
                    "-c:a", "pcm_s24le", f"{OUT}/cache/medley.wav"], check=True)

    # 1re passe loudnorm
    p1 = subprocess.run([FF, "-hide_banner", "-i", f"{OUT}/cache/medley.wav",
                         "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                         "-f", "null", "-"], capture_output=True, text=True, check=True)
    txt = p1.stderr
    js = json.loads(txt[txt.rindex("{"): txt.rindex("}") + 1])
    print("mesure 1re passe:", js)

    fade_st = max(0.0, dur - 2.4)
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}"
          f":measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}"
          f":offset={js['target_offset']}:linear=true,"
          f"afade=t=out:st={fade_st:.3f}:d=2.4,aresample=48000")

    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error",
                    "-i", f"{OUT}/cache/medley.wav", "-af", af,
                    "-c:a", "pcm_s24le", f"{OUT}/cache/medley-final.wav"], check=True)
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error",
                    "-i", f"{OUT}/cache/medley-final.wav",
                    "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
                    f"{OUT}/cache/medley-final.m4a"], check=True)

    info = subprocess.run([FF, "-hide_banner", "-i", f"{OUT}/cache/medley-final.m4a"],
                          capture_output=True, text=True).stderr
    print("\n".join(l for l in info.splitlines() if "Duration" in l or "Stream" in l))
    print("durée =", round(dur, 4))
    with open(f"{OUT}/cache/audio_duration.json", "w") as fh:
        json.dump({"duration": round(dur, 4), "segments": SEGMENTS, "xfade": XFADE}, fh, indent=2)


if __name__ == "__main__":
    main()
