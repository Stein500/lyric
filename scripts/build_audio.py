#!/usr/bin/env python3
"""§D.4 audio: loudnorm 2 passes, hook concat (WAV 48k first), MP3 master 320k + ID3v2.4 tags.
Usage: .venv/bin/python scripts/build_audio.py "<input.mp3>" "<Titre>" "<artiste>"
"""
import json, subprocess, sys, os, wave
import numpy as np

INP = sys.argv[1]
TITLE = sys.argv[2] if len(sys.argv) > 2 else "Ayon dèkpè"
ARTIST = sys.argv[3] if len(sys.argv) > 3 else "Daïsky"
FF = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bin", "ffmpeg"))
os.makedirs("work", exist_ok=True)
os.makedirs("livrables", exist_ok=True)

def sh(*a, **kw):
    return subprocess.run(a, capture_output=True, text=True, **kw)

# ---- pass 1 (already known) ----
r = sh(FF, "-hide_banner", "-i", INP, "-af",
       "loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json", "-f", "null", "-")
txt = r.stderr
import re
def grab(k):
    m = re.search(r'"%s"\s*:\s*"([^"]+)"' % k, txt)
    return m.group(1) if m else None
input_i, input_tp, input_lra, input_thresh, target_offset = (grab(k) for k in
    ["input_i", "input_tp", "input_lra", "input_thresh", "target_offset"])
print("PASS1:", input_i, input_tp, input_lra, input_thresh, target_offset)

# ---- pass 2 ----
# alimiter (true-peak ceiling ~ -3 dB) en fin de chaîne : l'encodage MP3/AAC
# crée des overs inter-échantillons (TP remonte), on les bride pour tenir TP <= -1.5.
wav_norm = "work/song_norm.wav"
r = sh(FF, "-y", "-i", INP,
       "-af", f"loudnorm=I=-14:TP=-1.8:LRA=11:measured_I={input_i}:measured_TP={input_tp}:measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset},highpass=f=30,lowpass=f=18000,alimiter=limit=0.7079:level=disabled",
       "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", wav_norm)
if not os.path.exists(wav_norm):
    print("PASS2 FAILED:\n", r.stderr[-2000:]); sys.exit(1)

# read duration
with wave.open(wav_norm, "rb") as w:
    sr = w.getframerate(); nf = w.getnframes()
    norm_dur = nf / sr
print(f"normalized WAV: {norm_dur:.3f}s @ {sr}Hz")

# ---- hook (cold-open 6s from title refrain, t=16.52) ----
HOOK = 6.0
hook_start = 16.52
r = sh(FF, "-y", "-i", wav_norm, "-ss", f"{hook_start:.2f}", "-t", f"{HOOK:.2f}",
       "-c:a", "pcm_s16le", "work/hook.wav")
assert os.path.exists("work/hook.wav")

# ---- silence 5s (apad) ----
r = sh(FF, "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "5",
       "-c:a", "pcm_s16le", "work/silence5.wav")
assert os.path.exists("work/silence5.wav")

# ---- concat via WAV join (decode-first rule) ----
def read_wav(p):
    with wave.open(p, "rb") as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
parts = [read_wav("work/hook.wav"), read_wav(wav_norm), read_wav("work/silence5.wav")]
full = np.concatenate(parts)
full_dur = len(full) / sr
out_wav = "work/master_audio.wav"
with wave.open(out_wav, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(full.tobytes())
print(f"master_audio.wav: {full_dur:.3f}s (hook {HOOK} + song {norm_dur:.3f} + 5s)")

# ---- MP3 master (song only, 320k, 48k) ----
mp3 = f"livrables/{TITLE}_master_320k.mp3"
r = sh(FF, "-y", "-i", wav_norm, "-codec:a", "libmp3lame", "-b:a", "320k",
       "-ar", "48000", mp3)
assert os.path.exists(mp3), r.stderr[-2000:]
print("MP3 master:", mp3)

json.dump({
    "input_i": input_i, "input_tp": input_tp, "input_lra": input_lra,
    "input_thresh": input_thresh, "target_offset": target_offset,
    "song_dur": norm_dur, "hook_start": hook_start, "hook_dur": HOOK,
    "master_dur": full_dur, "mp3": mp3, "master_wav": out_wav,
}, open("work/audio_master.json", "w"), indent=2)
print("audio_master.json written")
