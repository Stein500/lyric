#!/usr/bin/env python3
"""Reproductible : inspecte Nonvi Konou (MP3 avec image APIC) et prépare les minutages.

Dépendances temporaires : pip install imageio-ffmpeg numpy scipy
Usage: python scripts/analyse_nonvi.py
La détection spectrale est un contrôle indicatif, pas une transcription vocale.
"""
from __future__ import annotations
import json
import re
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from scipy.signal import find_peaks

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "Nonvi Konou.mp3"
SOURCE = ROOT / "Nonvi konou.txt"
WORK = ROOT / "work"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def run(*args):
    return subprocess.run([FFMPEG, *map(str, args)], capture_output=True, check=True)


def main():
    WORK.mkdir(exist_ok=True)
    probe = run('-hide_banner', '-i', AUDIO, '-map', '0:a:0', '-vn', '-f', 'null', '-')
    stderr = probe.stderr.decode(errors='replace')
    source_duration = re.search(r'Duration: (\d\d):(\d\d):(\d\d\.\d+)', stderr)
    decoded_duration = re.findall(r'time=(\d\d):(\d\d):(\d\d\.\d+)', stderr)[-1]
    duration = int(decoded_duration[0])*3600 + int(decoded_duration[1])*60 + float(decoded_duration[2])
    info = re.search(r'Stream #0:\d+: Audio: mp3 .*?(\d+) Hz, (\w+)', stderr)
    loud = run('-hide_banner', '-v', 'info', '-i', AUDIO, '-map', '0:a:0', '-vn',
               '-af', 'highpass=f=30,lowpass=f=18000,loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json', '-f', 'null', '-')
    measured = json.loads(re.findall(r'\{\s*"input_i".*?\}', loud.stderr.decode(errors='replace'), re.S)[-1])

    raw = run('-v', 'error', '-i', AUDIO, '-map', '0:a:0', '-vn', '-ac', '1', '-ar', '12000',
              '-f', 'f32le', '-').stdout
    samples = np.frombuffer(raw, dtype='<f4')
    actual_duration = len(samples) / 12000
    sr, hop, win = 12000, 256, 1024
    # Sliding FFT; spectrogram retained only in memory.
    windows = np.lib.stride_tricks.sliding_window_view(samples, win)[::hop]
    spec = np.abs(np.fft.rfft(windows * np.hanning(win).astype('f4'), axis=1)).astype('f4')
    flux = np.maximum(0, np.diff(spec, axis=0)).sum(axis=1)
    flux = np.pad(flux, (1, 0))
    times = np.arange(len(flux)) * hop / sr
    local = np.maximum(0.001, np.convolve(flux, np.ones(187)/187, mode='same'))  # ~4s
    peaks, _ = find_peaks(flux, height=1.15*local, distance=int(.16*sr/hop), prominence=.18*local)
    # Onset autocorrelation 70-180 BPM and its half/double-time ambiguity.
    smooth = np.convolve(flux / local, np.ones(5)/5, mode='same')
    smooth -= smooth.mean()
    lo, hi = round((60/180)*sr/hop), round((60/70)*sr/hop)
    correlation = [(lag, np.dot(smooth[lag:], smooth[:-lag])) for lag in range(lo, hi+1)]
    candidates = sorted(correlation, key=lambda x: x[1], reverse=True)[:8]
    bpm = round(60*sr/(hop*candidates[0][0]), 1)
    # RMS per 4-second section (not classification of vocals).
    rms = np.array([np.sqrt(np.mean(samples[j:j+sr*4].astype('f8')**2))
                    for j in range(0, len(samples), sr*4)])
    db = 20*np.log10(np.maximum(rms, 1e-9))
    lines = []
    for match in re.finditer(r'^\[(\d+):(\d+(?:\.\d+)?)\](.+)$', SOURCE.read_text(encoding='utf-8'), re.M):
        minute, second, text = match.groups()
        start = int(minute)*60 + float(second)
        text = text.lstrip('\u200e').strip()
        lines.append(dict(start=round(start, 2), text=text))
    if any(lines[i]['start']-lines[i-1]['start'] < 1.2 for i in range(1,len(lines))):
        raise ValueError('Fenêtres entre vers insuffisantes (<1,2 s)')
    if lines[-1]['start'] >= actual_duration:
        raise ValueError('Dernier vers hors de la durée audio')
    # Respecter les timestamps de l'artiste : un pic instrumental n'est pas une entrée chantée.
    for i, line in enumerate(lines):
        line['end'] = round(lines[i+1]['start'] if i+1<len(lines) else actual_duration, 2)
        nearby = peaks[np.abs(times[peaks] - line['start']) <= .35]
        line['spectral_peak'] = round(float(times[nearby[np.argmin(np.abs(times[nearby]-line['start']))]]), 2) if len(nearby) else None
        line['spectral_delta'] = round(line['spectral_peak']-line['start'], 2) if len(nearby) else None
        line['section'] = ('intro' if line['start'] < 15 else
                           'refrain' if 15 <= line['start'] < 29 or 59 <= line['start'] < 72 or 135 <= line['start'] < 148 else
                           'outro' if line['start'] >= 153 else
                           'pont' if 119 <= line['start'] < 135 else 'couplet')
    unique = list(dict.fromkeys(l['text'] for l in lines))
    duplicates = {t: [l['start'] for l in lines if l['text'] == t] for t in unique
                  if sum(l['text'] == t for l in lines)>1}
    # Mesure de l'énergie dans les fenêtres contenant le titre ; cold-open 2 vers (~5,5s).
    title_windows = []
    for i, line in enumerate(lines[:-1]):
        if 'nonvi konou' in line['text'].lower():
            a = int(line['start']/4); b = min(len(rms), max(a+1, int(lines[i+2]['start']/4) if i+2<len(lines) else a+1))
            title_windows.append(dict(start=line['start'], energy_db=round(float(np.mean(db[a:b])), 1)))
    report = dict(audio=str(AUDIO.name), duration_decoded_seconds=round(actual_duration, 3),
                  duration_ffmpeg_log_seconds=duration, duration_container_seconds=source_duration.group(0) if source_duration else None,
                  source_sample_rate=int(info[1]) if info else None,
                  source_channels=info[2] if info else None, rms_db_by_4_seconds=np.round(db,1).tolist(),
                  bpm_estimate=bpm, bpm_ambiguity=[round(60*sr/(hop*l),1) for l,_ in candidates[:5]],
                  loudnorm_pass1=measured, text_lines=len(lines), unique_lines=len(unique),
                  image_budget_vertical=len(unique)+2, repeated_verses=duplicates,
                  cold_open_candidates=title_windows, lines=lines,
                  timing_policy='Conservation des timestamps fournis ; pics spectraux dans ±0,35s informatifs, non substitués aux voix.' )
    (WORK/'timings_validated.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
    # Version corrigée UTF-8 : suppression des caractères U+200E invisibles, préservation des temps.
    lrc = '[ti:Nonvi Konou]\n[ar:Daïsky]\n'
    for line in lines:
        start=line['start']; mm=int(start//60); ss=start-mm*60
        lrc += f'[{mm:02d}:{ss:05.2f}]{line["text"]}\n'
    (ROOT/'Nonvi Konou.lrc').write_text(lrc,encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['duration_decoded_seconds','source_sample_rate','source_channels','bpm_estimate','bpm_ambiguity','loudnorm_pass1','text_lines','unique_lines','image_budget_vertical','cold_open_candidates']},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
