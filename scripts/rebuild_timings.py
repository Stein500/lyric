"""§A.1/A.3 — Analyse audio + validation timings 'Nan yi a ga djin wê'."""
import json, re, subprocess, sys
import numpy as np
from scipy.io import wavfile

MP3 = "Nan yi a ga djin wê.mp3"
FFMPEG = "work/ffmpeg"
WAV = "work/analyse.wav"

# --- décodage mono 22050 Hz ---
subprocess.run([FFMPEG, "-v", "error", "-y", "-i", MP3, "-ac", "1", "-ar", "22050", WAV], check=True)
sr, x = wavfile.read(WAV)
x = x.astype(np.float32) / 32768.0
dur = len(x) / sr
print(f"durée décodée: {dur:.3f} s")

# --- STFT / flux spectral ---
HOP, NFFT = 512, 2048
frames = []
for i in range(0, len(x) - NFFT, HOP):
    f = x[i:i+NFFT] * np.hanning(NFFT)
    frames.append(np.abs(np.fft.rfft(f)))
S = np.array(frames)
tfr = np.arange(len(S)) * HOP / sr
diff = np.maximum(0, np.diff(S, axis=0))
flux = diff.sum(axis=1)
flux = np.r_[flux[0], flux]
flux = flux / (np.median(flux) + 1e-9)

# --- BPM par autocorrélation du flux (60-180) ---
env = flux - flux.mean()
ac = np.correlate(env, env, "full")[len(env)-1:]
lags = np.arange(len(ac))
fps = sr / HOP
bpms = np.where(lags > 0, 60.0 * fps / np.maximum(lags, 1), 0)
mask = (lags >= 1) & (bpms >= 60) & (bpms <= 180)
acm = ac[mask]
lagm = lags[mask]
pk = lagm[np.argmax(acm)]
bpm = 60.0 * fps / pk
print(f"BPM estimé: {bpm:.1f}")

# --- RMS par 5 s pour la structure ---
win = int(5 * sr)
rms = []
for i in range(0, len(x) - win, win):
    seg = x[i:i+win]
    rms.append((i/sr, float(np.sqrt(np.mean(seg**2)))))
med = np.median([r for _, r in rms])
print("\nstructure énergie (5 s):")
for t, r in rms:
    bar = "#" * int(r / med * 8)
    tag = "FORT" if r > 1.25*med else ("faible" if r < 0.8*med else "")
    print(f"  {t:6.1f}s  {r:.4f}  {bar} {tag}")

# --- timings du lrc ---
lines = []
for ln in open("Nan yi a ga djin wê.txt", encoding="utf-8"):
    m = re.match(r"\[(\d+):(\d+\.\d+)\](.*)", ln.strip())
    if m:
        lines.append([int(m.group(1))*60 + float(m.group(2)), m.group(3).strip()])

# --- détection onsets : pic flux > 1.15 × médiane locale (fenêtre 4 s) ---
def local_median(t, half=2.0):
    a, b = t - half, t + half
    m = (tfr >= a) & (tfr <= b)
    return np.median(flux[m]) + 1e-9

def nearest_peak(t, tol=0.6):
    a, b = t - tol, t + tol
    m = (tfr >= a) & (tfr <= b)
    idx = np.where(m)[0]
    if len(idx) == 0: return t, 0.0
    vals = flux[idx]
    k = idx[np.argmax(vals)]
    return tfr[k], float(flux[k])

validated, log = [], []
prev = -10.0
for t, txt in lines:
    medl = local_median(t)
    tp, fv = nearest_peak(t, tol=0.35)
    thr = 1.15 * medl
    if fv > thr:
        nt = tp
        why = f"pic flux {fv:.2f}>{thr:.2f} à {tp:.2f} (Δ{tp-t:+.2f})"
    else:
        nt, fv2 = nearest_peak(t, tol=0.6)
        if fv2 > thr:
            why = f"pic flux tol.6s {fv2:.2f} à {nt:.2f} (Δ{nt-t:+.2f})"
        else:
            nt = t
            why = f"pas de pic net → conservé {t:.2f} (flux {fv:.2f})"
    if nt <= prev:
        nt = prev + 1.2
        why += " → MONOTONIE corrigée"
    if validated and nt - prev < 1.2:
        nt = prev + 1.2
        why += " → fenêtre mini 1.2s"
    log.append({"t_lrc": round(t,2), "t_valide": round(nt,2), "texte": txt, "note": why})
    validated.append([nt, txt])
    prev = nt

json.dump(log, open("work/timings_validated.json", "w"), ensure_ascii=False, indent=1)
ndiff = sum(1 for e in log if abs(e["t_valide"] - e["t_lrc"]) > 0.02)
print(f"\n{len(lines)} vers validés, {ndiff} décalés (>0.02 s).")
big = [e for e in log if abs(e["t_valide"] - e["t_lrc"]) > 0.15]
for e in big: print(f"  Δ gros: {e['t_lrc']} → {e['t_valide']}  {e['texte'][:40]}")

# --- sortie lrc corrigée ---
def fmt(t):
    m, s = divmod(t, 60)
    return f"[{int(m):02d}:{s:05.2f}]"
with open("Nan yi a ga djin wê.lrc", "w", encoding="utf-8") as f:
    f.write("[length:02:42]\n\n")
    for t, txt in validated:
        f.write(f"{fmt(t)}{txt}\n")
print("→ Nan yi a ga djin wê.lrc écrit")
