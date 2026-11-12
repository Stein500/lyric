#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Trois refrains, trois films : extraction propre, fondu court, -14 LUFS.
Audio de l'artiste intact (aucune voix générée, aucune retouche créative).
"""
import json
import subprocess

import numpy as np
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = "/home/user/lyric"
OUT = f"{ROOT}/productions/imelda-13-novembre"
SR = 48000

TRACKS = {
    "v1": ("Noukiko tché wê.mp3", 16.19, 58.80),   # refrain « Noukiko tché wê » + couplet 1
    "v2": ("Ayon dèkpè.mp3", 40.23, 80.60),        # couplet + refrain « Ayon dèkpè »
    "v3": ("Tu es trop belle.mp3", 86.49, 125.00),  # refrain « T'es trop belle » + couplet 2
}


def wav16(path):
    return np.frombuffer(open(path, "rb").read(), dtype="<i2")


def build(key):
    f, a, b = TRACKS[key]
    dur = b - a
    raw = subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-i", f"{ROOT}/{f}",
                          "-ss", f"{a:.4f}", "-t", f"{dur:.4f}", "-vn", "-ac", "2", "-ar", str(SR),
                          "-f", "f32le", "-acodec", "pcm_f32le", "pipe:1"],
                         check=True, capture_output=True).stdout
    x = np.frombuffer(raw, dtype="<f4").reshape(-1, 2).astype(np.float32).copy()
    # fondus courts (anti-clic + sortie douce)
    n_in = int(0.02 * SR)
    x[:n_in] *= np.linspace(0, 1, n_in, dtype=np.float32)[:, None]
    n_out = int(1.0 * SR)
    x[-n_out:] *= np.linspace(1, 0, n_out, dtype=np.float32)[:, None] ** 1.4

    with open(f"{OUT}/cache/{key}.f32", "wb") as fh:
        fh.write(x.astype("<f4").tobytes())
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-f", "f32le", "-ar", str(SR),
                    "-ac", "2", "-i", f"{OUT}/cache/{key}.f32", "-c:a", "pcm_s24le",
                    f"{OUT}/cache/{key}.wav"], check=True)

    p1 = subprocess.run([FF, "-hide_banner", "-i", f"{OUT}/cache/{key}.wav",
                         "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                         "-f", "null", "-"], capture_output=True, text=True, check=True)
    t = p1.stderr
    js = json.loads(t[t.rindex("{"): t.rindex("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}"
          f":measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}"
          f":offset={js['target_offset']}:linear=true,aresample=48000")
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error",
                    "-i", f"{OUT}/cache/{key}.wav", "-af", af,
                    "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
                    f"{OUT}/cache/{key}.m4a"], check=True)
    q = subprocess.run([FF, "-hide_banner", "-i", f"{OUT}/cache/{key}.m4a"],
                       capture_output=True, text=True).stderr
    d = [l for l in q.splitlines() if "Duration" in l][0]
    print(key, f"{dur:.3f}s", "|", d.strip())
    return round(dur, 3)


if __name__ == "__main__":
    meta = {k: {"track": TRACKS[k][0], "start": TRACKS[k][1], "end": TRACKS[k][2], "duration": build(k)}
            for k in ("v1", "v2", "v3")}
    json.dump(meta, open(f"{OUT}/cache/audio_songs.json", "w"), ensure_ascii=False, indent=2)
    print(json.dumps(meta, ensure_ascii=False, indent=2))
