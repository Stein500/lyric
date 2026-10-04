#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDIT DES TIMINGS — « Dès le début »
Compare les départs de vers du fichier de paroles aux onsets détectés sur l'audio réel
(pics de flux spectral). Règle v5.5 : un pic spectral est un INDICE, pas une preuve d'attaque
vocale ; on ne déplace jamais automatiquement un départ valable.

Sorties : timings_audited.json (+ rapport console)
"""
import json, os, re, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(PROD, "..", ".."))
FFMPEG = os.environ.get("FFMPEG", "/tmp/lyric-venv/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2")
AUDIO = os.path.join(ROOT, "Dès le début.mp3")
PAROLES = os.path.join(ROOT, "Dès le début- Jésus-Christ sauveur.txt")

SR, HOP = 22050, 256
TOL = 0.35          # tolérance admissible (v5.5 §6)
MAX_SHIFT = 0.45    # fenêtre de recherche autour du départ déclaré


def verses():
    out = []
    for line in open(PAROLES, encoding="utf-8").read().splitlines():
        m = re.match(r"\[(\d+):(\d+\.\d+)\]\u200e?(.*)", line)
        if m:
            out.append([int(m.group(1)) * 60 + float(m.group(2)), m.group(3).strip()])
    return out


def load_mono():
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", AUDIO, "-map", "0:a:0", "-vn",
                          "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def spectral_flux(x, n=1024):
    win = np.hanning(n).astype(np.float32)
    nfr = 1 + (len(x) - n) // HOP
    idx = np.arange(n)[None, :] + HOP * np.arange(nfr)[:, None]
    frames = x[idx] * win
    S = np.abs(np.fft.rfft(frames, axis=1))
    S = np.log1p(S * 20.0)
    flux = np.diff(S, axis=0).clip(min=0).sum(axis=1)
    times = (np.arange(1, nfr) * HOP) / SR
    return flux, times


def main():
    x = load_mono()
    flux, times = spectral_flux(x)
    # normalisation locale (fenêtre 4 s) pour comparer équitablement
    med = np.median(flux)
    V = verses()
    report, shifted, kept, ambigus = [], 0, 0, 0
    for i, (t, txt) in enumerate(V):
        m = (times >= t - MAX_SHIFT) & (times <= t + MAX_SHIFT)
        if not m.any():
            report.append(dict(i=i, t=t, txt=txt, delta=0.0, status="hors_fenetre"))
            kept += 1
            continue
        seg, tt = flux[m], times[m]
        k = int(np.argmax(seg))
        peak_ratio = float(seg[k] / max(1e-6, med))
        delta = float(tt[k] - t)
        if abs(delta) <= TOL:
            status = "conservé"
            kept += 1
        elif peak_ratio >= 1.30:
            status = "candidat_décalage"
            shifted += 1
        else:
            status = "ambigu_conservé"
            ambigus += 1
        report.append(dict(i=i, t=round(t, 3), txt=txt, delta=round(delta, 3),
                           peak_ratio=round(peak_ratio, 2), status=status))
    # contrôle de monotonie et d'intervalle mini
    mono = all(report[i]["t"] < report[i + 1]["t"] for i in range(len(report) - 1))
    mini = min((report[i + 1]["t"] - report[i]["t"]) for i in range(len(report) - 1))
    out = dict(
        audio=AUDIO, vers=len(V), tolerance_s=TOL,
        conserves=kept, candidats_decalage=shifted, ambigus_conserves=ambigus,
        monotonie_stricte=bool(mono), intervalle_mini_s=round(mini, 3),
        fenetres_cta_5s=[],
        detail=report,
        note="Audit indicatif : aucun départ n'est déplacé automatiquement (règle v5.5 §6)."
    )
    # fenêtres CTA : intervalle sans parole entre la fin d'affichage d'un vers et le suivant
    for i in range(len(V) - 1):
        t, txt = V[i]
        dur = min(4.5, max(2.2, 1.15 + 0.33 * len(txt.split())))
        nxt = V[i + 1][0]
        fin = min(t + dur, nxt - 0.12)
        gap = nxt - fin
        if gap >= 5.0:
            out["fenetres_cta_5s"].append(dict(debut=round(fin, 2), fin=round(nxt, 2), duree=round(gap, 2),
                                              apres=txt[:40]))
    t0 = V[0][0]
    if t0 >= 5.0:
        out["fenetres_cta_5s"].insert(0, dict(debut=0.0, fin=round(t0, 2), duree=round(t0, 2), apres="intro"))
    path = os.path.join(PROD, "timings_audited.json")
    json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"vers {len(V)} | conservés {kept} | candidats décalage {shifted} | ambigus {ambigus}")
    print(f"monotonie stricte: {mono} | intervalle mini: {mini:.2f} s")
    print("fenêtres clochettes (≥5 s sans parole) :")
    tot = 0
    for w in out["fenetres_cta_5s"]:
        tot += w["duree"]
        print(f"   {w['debut']:7.2f} → {w['fin']:7.2f}  ({w['duree']:5.2f} s) après {w['apres']!r}")
    print(f"   total clochettes : {tot:.1f} s")
    print("→", path)


if __name__ == "__main__":
    main()
