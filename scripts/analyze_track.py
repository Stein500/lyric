#!/usr/bin/env python3
import json
import math
import subprocess
import numpy as np
from scipy.signal import find_peaks

AUDIO_FILE = "Nan yi a ga djin wê.mp3"
LYRICS_FILE = "Nan yi a ga djin wê.txt"

def analyze_audio():
    # 1. Loudnorm pass 1
    cmd = [
        "ffmpeg", "-v", "info", "-i", AUDIO_FILE,
        "-af", "loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    err = res.stderr
    # Extract JSON between { and }
    json_start = err.rfind("{")
    json_end = err.rfind("}") + 1
    loudnorm_data = json.loads(err[json_start:json_end])

    # 2. Decode raw PCM to analyze RMS, onsets, BPM
    cmd_pcm = [
        "ffmpeg", "-v", "quiet", "-i", AUDIO_FILE,
        "-f", "s16le", "-ac", "1", "-ar", "22050", "-"
    ]
    proc = subprocess.Popen(cmd_pcm, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    raw, _ = proc.communicate()
    samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    sr = 22050
    duration = len(samples) / sr

    # Frame-level RMS energy (hop 512, frame 2048)
    frame_len = 2048
    hop_len = 512
    num_frames = 1 + (len(samples) - frame_len) // hop_len
    
    # Vectorized framing
    shape = (num_frames, frame_len)
    strides = (samples.strides[0] * hop_len, samples.strides[0])
    frames = np.lib.stride_tricks.as_strided(samples, shape=shape, strides=strides)
    rms = np.sqrt(np.mean(frames**2, axis=1) + 1e-12)
    times = np.arange(num_frames) * (hop_len / sr)

    # Spectral flux / onset envelope
    window = np.hanning(frame_len)
    stft = np.fft.rfft(frames * window, axis=1)
    mag = np.abs(stft)
    diff = np.diff(mag, axis=0)
    diff[diff < 0] = 0
    spectral_flux = np.sum(diff, axis=1)
    spectral_flux = np.pad(spectral_flux, (1, 0), mode='constant')

    # Normalize spectral flux
    spectral_flux = (spectral_flux - np.mean(spectral_flux)) / (np.std(spectral_flux) + 1e-6)
    spectral_flux[spectral_flux < 0] = 0

    # BPM estimation via autocorrelation of spectral flux
    # target 60 to 180 BPM
    fps_env = sr / hop_len
    min_lag = int(60.0 / 200.0 * fps_env)
    max_lag = int(60.0 / 60.0 * fps_env)
    autocorr = np.correlate(spectral_flux, spectral_flux, mode='full')
    autocorr = autocorr[len(spectral_flux)-1:]
    valid_lags = autocorr[min_lag:max_lag]
    best_lag = min_lag + np.argmax(valid_lags)
    estimated_bpm = 60.0 * fps_env / best_lag

    return {
        "duration": duration,
        "sample_rate": 48000,
        "channels": 2,
        "loudnorm": loudnorm_data,
        "bpm": round(estimated_bpm, 1),
        "times": times,
        "rms": rms,
        "spectral_flux": spectral_flux,
        "fps_env": fps_env
    }

print("Running audio analysis...")
data = analyze_audio()
print(f"Duration: {data['duration']:.2f} s")
print(f"Loudnorm: I={data['loudnorm']['input_i']}, TP={data['loudnorm']['input_tp']}, LRA={data['loudnorm']['input_lra']}, target_offset={data['loudnorm']['target_offset']}")
print(f"BPM: {data['bpm']}")
