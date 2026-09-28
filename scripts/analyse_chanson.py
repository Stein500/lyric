#!/usr/bin/env python3
"""Analyse reproductible, sans génération d'images ni modification des sources.

Les pics de flux spectral sont des indices musicaux, PAS un alignement vocal.
Les timestamps source restent inchangés ; les suggestions nécessitent une écoute.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess

import numpy as np
from scipy.ndimage import median_filter
from scipy.signal import correlate, find_peaks

STAMP = r"\d+:[0-5]\d(?:[.,]\d+)?"
LRC_STAMP = re.compile(rf"\[({STAMP})\]")
RANGE = re.compile(rf"(?:\s*-\s*)?({STAMP})\s*[-–→]\s*({STAMP})\s*$")
TRAILING = re.compile(rf"(?:\s*[-–]\s*|\s*)({STAMP})\s*$")
META = re.compile(r"^\[([A-Za-z]+):(.*)\]$")
DIRECTION_MARKS = dict.fromkeys(map(ord, "\u200e\u200f\ufeff"))


def seconds(stamp: str) -> float:
    minutes, sec = stamp.replace(",", ".").split(":")
    return int(minutes) * 60 + float(sec)


def timestamp(value: float) -> str:
    hundredths = round(value * 100)
    return f"{hundredths // 6000:02d}:{hundredths // 100 % 60:02d}.{hundredths % 100:02d}"


def load_lyrics(path: Path) -> dict:
    raw = path.read_bytes()
    try:
        text, encoding = raw.decode("utf-8-sig"), "utf-8-sig"
    except UnicodeDecodeError:
        text, encoding = raw.decode("cp1252"), "cp1252"
    entries, metadata = [], {}
    section = None
    removed = 0
    for number, source in enumerate(text.splitlines(), 1):
        clean = source.translate(DIRECTION_MARKS)
        removed += len(source) - len(clean)
        line = clean.strip()
        if not line:
            continue
        meta = META.fullmatch(line)
        if meta and not LRC_STAMP.match(line):
            metadata[meta[1].lower()] = meta[2]
            continue
        if line.startswith("[") and line.endswith("]") and not LRC_STAMP.match(line):
            section = line[1:-1]
            continue
        prefix = re.match(rf"^(?:\[{STAMP}\])+", line)
        if prefix:
            lyric = line[prefix.end():].strip()
            times = [seconds(m[1]) for m in LRC_STAMP.finditer(prefix[0])]
            fmt, explicit_end = "lrc", None
        else:
            span = RANGE.search(line)
            trailing = TRAILING.search(line)
            if span:
                lyric = line[:span.start()].strip()
                times, explicit_end, fmt = [seconds(span[1])], seconds(span[2]), "range"
            elif trailing:
                lyric = line[:trailing.start()].strip()
                times, explicit_end, fmt = [seconds(trailing[1])], None, "trailing"
            else:
                lyric, times, explicit_end, fmt = line, [None], None, "untimed"
        if not lyric:
            continue
        for start in times:
            entries.append({"line": number, "text": lyric, "start": start,
                            "explicit_end": explicit_end, "section": section, "format": fmt})
    # Multi-tags LRC may legitimately encode reprises out of file order.
    has_multi = any(len(LRC_STAMP.findall(l)) > 1 for l in text.splitlines())
    if has_multi and all(e["start"] is not None for e in entries):
        entries.sort(key=lambda e: e["start"])
    return {"encoding": encoding, "removed_direction_marks": removed,
            "multi_tag_lrc_sorted": has_multi, "metadata": metadata, "entries": entries}


def audit_timings(entries: list[dict], duration: float) -> list[dict]:
    issues, previous = [], None
    for e in entries:
        start = e["start"]
        if start is None:
            issues.append({"line": e["line"], "issue": "sans_timestamp"})
            continue
        if not 0 <= start < duration:
            issues.append({"line": e["line"], "issue": "hors_audio", "start": start})
        if previous is not None:
            delta = start - previous
            if delta < 1.2 - 1e-8:
                issues.append({"line": e["line"], "issue": "non_monotone" if delta <= 0 else "ecart_inferieur_1.2s",
                               "delta": round(delta, 4)})
        end = e["explicit_end"]
        if end is not None and not start < end <= duration:
            issues.append({"line": e["line"], "issue": "fin_invalide", "end": end})
        previous = start
    return issues


def run(ffmpeg: str, args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([ffmpeg, "-nostdin", "-hide_banner", *args],
                          check=True, capture_output=True, timeout=240)


def audio_features(samples: np.ndarray, sr: int) -> dict:
    nfft, hop = 2048, 256
    padded = np.pad(samples, (nfft // 2, nfft // 2))
    frames = np.lib.stride_tricks.sliding_window_view(padded, nfft)[::hop]
    spectrum = np.abs(np.fft.rfft(frames * np.hanning(nfft).astype(np.float32), axis=1))
    flux = np.maximum(np.diff(spectrum, axis=0, prepend=spectrum[:1]), 0).sum(axis=1)
    local_window = int(round(4 * sr / hop)) | 1
    median = median_filter(flux, size=local_window, mode="nearest")
    peaks, _ = find_peaks(flux, height=np.maximum(1.15 * median, 1e-7),
                          distance=max(1, round(0.09 * sr / hop)))
    peak_times = peaks * hop / sr
    # Tempo indicatif : autocorrélation du flux, recherche 60–180 BPM.
    centered = flux - np.mean(flux)
    autocorr = correlate(centered, centered, mode="full", method="fft")[len(flux)-1:]
    lag_min, lag_max = math.ceil(60 * sr / hop / 180), math.floor(60 * sr / hop / 60)
    lags, _ = find_peaks(autocorr[lag_min:lag_max + 1])
    lags = lags + lag_min
    if not len(lags):
        lags = np.array([lag_min + np.argmax(autocorr[lag_min:lag_max + 1])])
    ordered = sorted(lags, key=lambda lag: autocorr[lag], reverse=True)[:5]
    candidates = [{"bpm": round(60 * sr / hop / int(lag), 2),
                   "autocorrelation": round(float(autocorr[lag] / max(float(autocorr[0]), 1e-12)), 4)}
                  for lag in ordered]
    rms = []
    for begin in range(0, len(samples), sr):
        block = samples[begin:begin+sr]
        value = float(np.sqrt(np.mean(block.astype(np.float64) ** 2)))
        rms.append({"start": begin / sr, "end": min(begin+sr, len(samples)) / sr,
                    "rms_dbfs": round(20 * math.log10(max(value, 1e-12)), 3)})
    return {"sample_rate": sr, "fft_size": nfft, "hop": hop,
            "bpm_estimate": candidates[0]["bpm"], "tempo_candidates": candidates,
            "tempo_status": "estimation instrumentale ; ambiguïté demi/double tempo possible",
            "onset_rule": "flux positif > 1,15 × médiane locale sur 4 s",
            "onsets": [round(float(t), 5) for t in peak_times], "rms_1s": rms}


def repeated_windows(entries: list[dict], rms: list[dict], title: str) -> list[dict]:
    """Repère les suites exactes répétées de cinq vers contenant le titre."""
    candidates, seen = [], set()
    for i, row in enumerate(entries):
        if title.casefold() not in row["text"].casefold() or i + 5 > len(entries):
            continue
        words = tuple(e["text"] for e in entries[i:i+5])
        if words in seen:
            continue
        seen.add(words)
        indices = [j for j in range(len(entries)-4)
                   if tuple(e["text"] for e in entries[j:j+5]) == words]
        if len(indices) < 2:
            continue
        windows = []
        for j in indices:
            starts = [e["start"] for e in entries[j:j+5]]
            if any(t is None for t in starts) or any(b <= a for a, b in zip(starts, starts[1:])):
                continue
            end = entries[j+2]["start"]
            energy = [r["rms_dbfs"] for r in rms if starts[0] <= r["start"] < end]
            windows.append({"entry_index": j, "start": starts[0], "two_line_end": end,
                            "two_line_duration": round(end-starts[0], 3),
                            "two_line_rms_dbfs": round(float(np.mean(energy)), 3) if energy else None,
                            "relative_starts": [round(t-starts[0], 3) for t in starts]})
        candidates.append({"texts": words, "occurrences": windows})
    return candidates


def analyse(audio: Path, lyrics: Path, title: str, output: Path) -> dict:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    output.mkdir(parents=True, exist_ok=True)
    measurement = run(ffmpeg, ["-v", "info", "-progress", "pipe:1", "-i", str(audio),
                               "-map", "0:a:0", "-vn", "-f", "null", "-"])
    log = measurement.stderr.decode("utf-8", errors="replace")
    (output / "decode.log").write_text(log, encoding="utf-8")
    progress = measurement.stdout.decode()
    duration_values = re.findall(r"^out_time_us=(\d+)$", progress, re.M)
    if not duration_values:
        raise RuntimeError("FFmpeg n'a pas émis la durée décodée.")
    duration = int(duration_values[-1]) / 1e6
    info = re.search(r"Stream #0:\d+.*Audio: [^,]+, (\d+) Hz, ([^,\n]+)", log)
    loud = run(ffmpeg, ["-v", "info", "-i", str(audio), "-map", "0:a:0", "-vn",
                       "-af", "highpass=f=30,lowpass=f=18000,loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json",
                       "-f", "null", "-"])
    loud_log = loud.stderr.decode("utf-8", errors="replace")
    (output / "loudnorm_pass1.log").write_text(loud_log, encoding="utf-8")
    match = re.search(r'\{\s*"input_i".*?\}', loud_log, re.S)
    if not match:
        raise RuntimeError("Mesure loudnorm absente.")
    loudnorm = json.loads(match[0])
    raw = run(ffmpeg, ["-v", "error", "-i", str(audio), "-map", "0:a:0", "-vn",
                      "-ac", "1", "-ar", "22050", "-f", "f32le", "pipe:1"]).stdout
    features = audio_features(np.frombuffer(raw, dtype="<f4"), 22050)
    parsed = load_lyrics(lyrics)
    entries = parsed["entries"]
    issues = audit_timings(entries, duration)
    onsets = np.asarray(features["onsets"])
    proposals = []
    for e in entries:
        nearest, delta = None, None
        if e["start"] is not None and len(onsets):
            nearest = float(onsets[np.argmin(np.abs(onsets-e["start"]))])
            delta = round(nearest-e["start"], 5)
        proposals.append({**e, "nearest_musical_onset": nearest,
                          "delta": delta, "within_350ms": delta is not None and abs(delta) <= 0.35,
                          "timing_changed": False, "vocal_alignment_validated": False})
    repeats = repeated_windows(entries, features["rms_1s"], title)
    counts = Counter(e["text"] for e in entries)
    data = {"title": title, "audio_file": str(audio), "lyrics_file": str(lyrics),
            "sha256_audio": hashlib.sha256(audio.read_bytes()).hexdigest(),
            "sha256_lyrics": hashlib.sha256(lyrics.read_bytes()).hexdigest(),
            "duration_decoded_seconds": duration, "duration_method": "FFmpeg -map 0:a:0 -vn -f null, out_time_us final",
            "sample_rate": int(info[1]) if info else None, "channels": info[2] if info else None,
            "loudnorm_pass1": loudnorm, "loudnorm_prefilter": "highpass=f=30,lowpass=f=18000",
            "lyrics": {**parsed, "entries": proposals, "line_count": len(entries),
                       "distinct_count": len(counts), "issues": issues,
                       "status": "structure vérifiée ; synchronisation vocale non validée"},
            "features": features, "repeated_title_sequences": repeats}
    (output / "analyse.json").write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    # Ne jamais étiqueter « validated » un simple relevé de pics instrumentaux.
    (output / "timings_audited.json").write_text(json.dumps(proposals, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return data


def write_source_lrc(data: dict, destination: Path) -> None:
    """Copie UTF-8 des départs source, jamais un faux LRC « recalé à la voix »."""
    entries = data["lyrics"]["entries"]
    if any(e["start"] is None for e in entries):
        raise ValueError("Des vers sans heure exigent un alignement avant export LRC.")
    if data["lyrics"]["issues"]:
        raise ValueError("Corriger les anomalies source avant export LRC.")
    lines = [f'[ti:{data["title"]}]',
             f'[length:{timestamp(data["duration_decoded_seconds"])}]', '[offset:0]', '']
    previous_section = None
    for e in entries:
        if e["section"] and e["section"] != previous_section:
            lines.append(f'[{e["section"]}]')
        previous_section = e["section"]
        lines.append(f'[{timestamp(e["start"])}]{e["text"]}')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text('\n'.join(lines)+'\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--lyrics", type=Path, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--clean-lrc", type=Path, help="Copie LRC UTF-8, horaires source conservés")
    args = parser.parse_args()
    data = analyse(args.audio, args.lyrics, args.title, args.output)
    if args.clean_lrc:
        write_source_lrc(data, args.clean_lrc)
    print(json.dumps({"title": data["title"], "duration_seconds": data["duration_decoded_seconds"],
                      "bpm_estimate": data["features"]["bpm_estimate"], "loudnorm": data["loudnorm_pass1"],
                      "lines": data["lyrics"]["line_count"], "distinct_lines": data["lyrics"]["distinct_count"],
                      "timing_issues": data["lyrics"]["issues"], "reports": str(args.output)},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
