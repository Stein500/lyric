#!/usr/bin/env python3
"""Compare MP4 audio timing against the MP3 derivative, not against sung words.

For each of six non-faded 2 s excerpts, decode both audio streams to 8 kHz mono,
search +/-0.4 s by FFT cross-correlation and report the strongest offset. This
cannot establish whether an artist's lyric timestamps align with the actual voice.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work"
SR = 8000
TIMES = (10, 60, 120, 180, 210, 220)


def decode(source: Path, output: Path) -> None:
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", str(source),
                    "-map", "0:a:0", "-ar", str(SR), "-ac", "1", "-f", "f32le", "-y", str(output)], check=True)


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    a_path, b_path = WORK / "source-8k.f32", WORK / "video-8k.f32"
    decode(ROOT / "livrables/Je_me_releve_toujours_Dsky.mp3", a_path)
    decode(ROOT / "livrables/Je_me_releve_toujours_9x16.mp4", b_path)
    src = np.memmap(a_path, dtype="<f4", mode="r")
    dst = np.memmap(b_path, dtype="<f4", mode="r")
    length, pad = SR * 2, int(SR * 0.4)
    print(f"Decoded samples at {SR} Hz: MP3={len(src)}, MP4={len(dst)}")
    for t in TIMES:
        center = int(t * SR)
        a = np.array(src[center:center + length], dtype=np.float64)
        b = np.array(dst[center - pad:center + length + pad], dtype=np.float64)
        if len(a) != length or len(b) != length + 2 * pad:
            raise RuntimeError(f"Audio too short for t={t}s")
        a -= a.mean()
        b -= b.mean()
        n = 1 << (len(a) + len(b) - 2).bit_length()
        c = np.fft.irfft(np.fft.rfft(b, n) * np.fft.rfft(a[::-1], n), n)
        valid = c[len(a) - 1:len(b)]
        k = int(np.argmax(valid))
        segment = b[k:k + length]
        score = valid[k] / np.sqrt(np.dot(a, a) * np.dot(segment, segment) + 1e-30)
        offset = (k - pad) / SR
        print(f"t={t:3d}s delta={offset:+.6f}s corr={score:.5f}")
        if abs(offset) > 0.005 or score < 0.95:
            raise RuntimeError(f"Audio alignment failed at t={t}s")


if __name__ == "__main__":
    main()
