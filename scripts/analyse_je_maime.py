#!/usr/bin/env python3
"""Audit reproductible des sources ; ne masterise, ne réécrit et ne recale rien.

Usage : bash scripts/setup_env.sh
        .venv/bin/python scripts/analyse_je_maime.py
Les sources originales restent intactes. Les données de travail sont ignorées.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from mutagen.mp3 import MP3
from scipy import ndimage, signal
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projets/je_maime_tellement"
WORK = ROOT / "work/je_maime_tellement"
CUE = re.compile(r"^\[(\d{2}):(\d{2})\.(\d{2})\](.+)$")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def audit_lrc(source: Path, fps: int) -> dict:
    raw = source.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
        encoding = "utf-8-sig"
    except UnicodeDecodeError:
        text = raw.decode("cp1252")
        encoding = "cp1252 (compatible Latin-1 pour les octets de cette source)"

    # Correction graphique attestée par le texte fourni en conversation.
    # Aucune modification du fichier source, de mots chantés ni de timestamps.
    corrected = text.replace("cSur", "cœur")
    (PROJECT / "paroles_utf8.lrc").write_text(corrected, encoding="utf-8")
    cues = []
    directions = []
    previous_cs = -1
    for line_number, line in enumerate(corrected.splitlines(), 1):
        match = CUE.fullmatch(line)
        if not match:
            if line.strip() and not re.fullmatch(r"\[[a-z]+:.*\]", line):
                raise ValueError(f"Entrée LRC inconnue, ligne {line_number}: {line!r}")
            continue
        minutes, seconds, centiseconds, content = match.groups()
        if int(seconds) >= 60:
            raise ValueError(f"Secondes invalides, ligne {line_number}")
        t_cs = int(minutes) * 6000 + int(seconds) * 100 + int(centiseconds)
        if t_cs <= previous_cs:
            raise ValueError("Les timestamps doivent être strictement croissants.")
        previous_cs = t_cs
        row = {
            "source_line": line_number,
            "timestamp": line[:10],
            "start_centiseconds": t_cs,
            "start_seconds": t_cs / 100,
            # Entiers : première frame à t >= timestamp, sans avance ni arrondi flottant.
            "first_frame_30fps": (t_cs * fps + 99) // 100,
            "source_text": content,
        }
        if content.startswith("[INTRO-"):
            directions.append(row)
        else:
            row["slot"] = len(cues) + 1
            cues.append(row)

    metadata = dict(re.findall(r"^\[([a-z]+):(.*)\]$", corrected, re.M))
    return {
        "source": str(source.relative_to(ROOT)),
        "sha256": digest(source),
        "decoded_with": encoding,
        "production_copy": "projets/je_maime_tellement/paroles_utf8.lrc",
        "production_copy_changes": [
            "Encodage UTF-8.",
            f"cSur → cœur ({text.count('cSur')} occurrences), conformément au texte fourni dans la conversation.",
            "Aucune modification des timestamps ni de la phrase si belle,si dure,si lui.",
        ],
        "metadata": metadata,
        "timed_entries": len(cues) + len(directions),
        "sung_lines": len(cues),
        "images_per_format": len(cues) + 2,
        "text_advance_seconds": 0.0,
        "frame_rule": "ceil(timestamp × 30), sans offset : quantification tardive < 1 frame, jamais anticipée.",
        "stage_directions": directions,
        "lyrics": cues,
        "vocal_sync_status": "NON VALIDÉ : cet audit structurel ne vérifie pas les onsets vocaux à ±0,35 s.",
    }


def estimate_tempo(wav: Path) -> dict:
    sr, audio = wavfile.read(wav)
    audio = audio.astype(np.float32) / 32768
    hop = 160
    _, _, spectrum = signal.stft(audio, fs=sr, nperseg=1024, noverlap=1024 - hop, boundary=None)
    magnitude = np.abs(spectrum)
    magnitude /= np.mean(magnitude, axis=1, keepdims=True) + 1e-5
    onset = np.maximum(np.diff(np.log1p(magnitude), axis=1), 0).mean(axis=0)
    onset = np.maximum(onset - ndimage.uniform_filter1d(onset, size=101), 0)
    rate = sr / hop
    windows = []
    for start, end in [(30, 175), (45, 87), (100, 162)]:
        part = onset[int(start * rate):int(end * rate)]
        ac = signal.fftconvolve(part, part[::-1], mode="full")[len(part) - 1:]
        ac /= np.arange(len(part), 0, -1)
        lo, hi = int(60 * rate / 180), int(60 * rate / 60)
        peaks, _ = signal.find_peaks(ac[lo:hi])
        peaks = sorted(peaks + lo, key=lambda p: ac[p], reverse=True)[:5]
        candidates = []
        for peak in peaks:
            denominator = ac[peak - 1] - 2 * ac[peak] + ac[peak + 1]
            delta = 0.5 * (ac[peak - 1] - ac[peak + 1]) / denominator if denominator else 0
            lag = peak + np.clip(delta, -0.5, 0.5)
            candidates.append({"bpm": round(float(60 * rate / lag), 3), "relative_score": round(float(ac[peak] / ac[0]), 4)})
        windows.append({"window_seconds": [start, end], "candidates": candidates})
    return {
        "method": "Autocorrélation du flux spectral positif comprimé et blanchi par bande.",
        "status": "ESTIMATION : ambiguïté simple/double tempo ; ne pas utiliser pour déplacer les vers.",
        "windows": windows,
    }


def main() -> None:
    PROJECT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    config = json.loads((PROJECT / "cadrage.json").read_text(encoding="utf-8"))
    approved = config["approved"]
    if approved["text_advance_seconds"] != 0 or approved["fps"] != 30:
        raise ValueError("Ce titre impose 0 s d'avance et 30 fps.")
    audio_path = ROOT / config["source_audio"]
    lrc_path = ROOT / config["source_lrc"]
    source_hashes = {audio_path: digest(audio_path), lrc_path: digest(lrc_path)}
    audio = MP3(audio_path)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    lrc = audit_lrc(lrc_path, approved["fps"])

    decoded = subprocess.run(
        [ffmpeg, "-hide_banner", "-nostdin", "-v", "warning", "-i", str(audio_path), "-vn", "-c:a", "pcm_f32le", "-f", "f32le", "-"],
        capture_output=True, check=True,
    )
    samples = np.frombuffer(decoded.stdout, dtype="<f4").reshape(-1, audio.info.channels)
    n_samples = len(samples)
    duration = n_samples / audio.info.sample_rate
    peak = float(20 * np.log10(np.max(np.abs(samples))))
    decode_warnings = decoded.stderr.decode("utf-8", errors="replace")
    del samples, decoded
    if lrc["lyrics"][-1]["start_seconds"] >= duration:
        raise ValueError("Le dernier vers débute au-delà de l'audio.")

    measured = subprocess.run(
        [ffmpeg, "-hide_banner", "-nostdin", "-i", str(audio_path), "-af", "loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    )
    (WORK / "loudnorm_source.log").write_text(measured.stderr, encoding="utf-8")
    loudnorm = json.loads(measured.stderr[measured.stderr.rfind("{"):measured.stderr.rfind("}") + 1])
    wav = WORK / "source_16k.wav"
    subprocess.run(
        [ffmpeg, "-hide_banner", "-nostdin", "-v", "warning", "-y", "-i", str(audio_path), "-vn", "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(wav)],
        check=True,
    )
    report = {
        "source_audio": str(audio_path.relative_to(ROOT)),
        "sha256": source_hashes[audio_path],
        "ffmpeg_version": imageio_ffmpeg.get_ffmpeg_version(),
        "sample_rate_hz": audio.info.sample_rate,
        "channels": audio.info.channels,
        "bitrate_bps_estimated": audio.info.bitrate,
        "bitrate_mode": str(audio.info.bitrate_mode),
        "container_duration_seconds": audio.info.length,
        "decoded_samples_per_channel": n_samples,
        "decoded_duration_seconds": duration,
        "decode_warnings": decode_warnings,
        "sample_peak_dbfs": round(peak, 4),
        "source_loudness_lufs": float(loudnorm["input_i"]),
        "source_true_peak_dbtp": float(loudnorm["input_tp"]),
        "source_loudness_range_lu": float(loudnorm["input_lra"]),
        "measurement_note": "Source intacte, sans filtres de mastering. Ce n'est PAS une passe de mastering validée ni un MP3 masterisé.",
        "source_tags": {key: str(audio.tags.get(key, "")) if audio.tags else "" for key in ("TIT2", "TPE1", "TALB", "TPE2", "TCON", "TDRC")},
        "tempo": estimate_tempo(wav),
        "lrc": lrc,
        "sources_unchanged": all(digest(path) == expected for path, expected in source_hashes.items()),
    }
    if not report["sources_unchanged"]:
        raise RuntimeError("Une source a changé pendant l'analyse.")
    dump(PROJECT / "analyse_audio.json", report)
    print(f"Durée décodée : {duration:.6f} s ; {audio.info.sample_rate} Hz ; {audio.info.channels} canaux")
    print(f"Source : {report['source_loudness_lufs']} LUFS ; {report['source_true_peak_dbtp']} dBTP")
    print(f"LRC : {lrc['sung_lines']} vers, {lrc['images_per_format']} images par format ; avance 0,00 s")
    print("Sources inchangées. Texte/minutage utilisateur conservés ; audit technique seulement, sans certification indépendante des onsets.")


if __name__ == "__main__":
    main()
