#!/usr/bin/env python3
"""§A.1 audio analysis: duration, SR/channels, BPM estimate, energy structure, loudnorm pass 1.
Usage: .venv/bin/python scripts/analyse_audio.py "<file.mp3>"
Writes work/audio_analysis.json (cache) and prints a summary.
"""
import json, subprocess, sys, os
import numpy as np
from scipy import signal

AUDIO = sys.argv[1] if len(sys.argv) > 1 else "Ayon dèkpè.mp3"
FF = os.path.join(os.path.dirname(__file__), "..", "bin", "ffmpeg")
os.makedirs("work", exist_ok=True)

def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)

# --- decode to mono low-SR WAV for analysis ---
wav = "work/_analyse_mono.wav"
sh(FF, "-y", "-i", AUDIO, "-ac", "1", "-ar", "12000", wav)

# read WAV via scipy
sr, x = signal.wavread(wav) if hasattr(signal, "wavread") else (None, None)
# scipy>=1.11 removed wavread; use wave + numpy
import wave
with wave.open(wav, "rb") as w:
    n = w.getnframes()
    sr = w.getframerate()
    raw = w.readframes(n)
x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
if x.ndim > 1:
    x = x.mean(axis=1)

dur = len(x) / sr

# --- onset envelope (spectral flux-ish: use half-wave rectified energy flux) ---
frame = int(sr * 0.010)  # 10 ms hop
hop = int(sr * 0.005)
env = np.array([np.sqrt(np.mean(x[i:i+frame]**2)) for i in range(0, len(x)-frame, hop)])
flux = np.diff(env)
flux = np.clip(flux, 0, None)  # half-wave rectified
# smooth
b = np.ones(3)/3
flux = np.convolve(flux, b, "same")

# --- BPM via autocorrelation of onset envelope (60..180 bpm window) ---
def bpm_estimate(flux, sr_hz):
    # flux is per hop
    corr = signal.correlate(flux, flux, mode="full")
    corr = corr[len(corr)//2:]
    corr[:1] = 0
    bpm_range = np.arange(60, 181, 0.5)
    lags = (60.0 / bpm_range) * (sr_hz / hop)
    vals = []
    for lag in lags:
        li = int(round(lag))
        if 0 <= li < len(corr):
            vals.append(corr[li])
        else:
            vals.append(0)
    vals = np.array(vals)
    return float(bpm_range[np.argmax(vals)])

bpm = bpm_estimate(flux, sr)

# --- energy structure (RMS per 4 s window) ---
win = int(sr * 4)
starts = np.arange(0, len(x)-win, win)
rms = [float(np.sqrt(np.mean(x[s:s+win]**2))) for s in starts]
rms = np.array(rms)
if len(rms):
    thresh = np.median(rms) * 1.1
    loud = rms > thresh
    secs = starts / sr

res = {
    "duration_s": round(dur, 3),
    "sample_rate": 48000,
    "channels": 2,
    "bpm_estimate": bpm,
    "energy_windows_4s": [{"t": round(float(t),2), "rms": round(float(r),4), "loud": bool(l)} for t,r,l in zip(secs, rms, loud)],
}
with open("work/audio_analysis.json", "w") as f:
    json.dump(res, f, indent=2)

print(json.dumps(res, indent=2))
