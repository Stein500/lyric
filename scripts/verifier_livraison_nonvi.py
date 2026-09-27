#!/usr/bin/env python3
"""Contrôles reproductibles de la livraison finale Nonvi Konou."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

import imageio_ffmpeg
from mutagen.mp3 import MP3
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'livrables'
WORK = ROOT / 'work' / 'final_nonvi' / 'qa'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
CLIP = OUT / 'Nonvi_Konou_9x16_v1.mp4'
MASTER = OUT / 'Nonvi_Konou_master_320k.mp3'
EXPECTED_TAGS = {'TIT2', 'TPE1', 'TALB', 'TPE2', 'TPUB', 'TCOM', 'TCON', 'TDRC',
                 'TXXX:contact', 'TXXX:email', 'TXXX:producer', 'TXXX:label',
                 'USLT::fra', 'APIC:Cover'}


def capture(args):
    p = subprocess.run(args, text=True, capture_output=True, check=True)
    return p.stdout + p.stderr


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    log = capture([FFMPEG, '-hide_banner', '-i', str(CLIP), '-map', '0:v:0',
                   '-vf', 'blackdetect=d=0.30:pix_th=0.10,freezedetect=d=0.50',
                   '-an', '-f', 'null', '-'])
    duration = float(re.search(r'Duration: \d\d:\d\d:(\d+\.\d+)', log).group(1))
    # Le clip fait moins d'une heure : minutes intégrées séparément dans le log.
    dparts = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', log).groups()
    duration = int(dparts[0]) * 3600 + int(dparts[1]) * 60 + float(dparts[2])
    frame_matches = re.findall(r'frame=\s*(\d+)', log)
    frames = int(frame_matches[-1])
    video = re.search(r'Video: h264 .*?, (\d+)x(\d+).*?, ([\d.]+) fps', log)
    audio = re.search(r'Audio: aac .*?, (\d+) Hz, (\w+)', log)
    assert video and audio
    # Image de référence décodée pour le bandeau géométrique et le petit pictogramme.
    frame = WORK / 'reference_1s.png'
    subprocess.run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-ss', '1.0', '-i', str(CLIP),
                    '-frames:v', '1', '-y', str(frame)], check=True)
    im = Image.open(frame).convert('RGB')
    refs = {
        'footer_green': (im.getpixel((80, 1880)), (0, 135, 81)),
        'footer_yellow': (im.getpixel((800, 1880)), (252, 209, 22)),
        'footer_red': (im.getpixel((800, 1905)), (232, 17, 45)),
        'badge_green': (im.getpixel((600, 190)), (0, 135, 81)),
        'badge_yellow': (im.getpixel((640, 190)), (252, 209, 22)),
        'badge_red': (im.getpixel((640, 214)), (232, 17, 45)),
    }
    color_deltas = {k: max(abs(a - b) for a, b in zip(got, expected))
                    for k, (got, expected) in refs.items()}
    mp3 = MP3(MASTER)
    tag_keys = set(mp3.tags.keys())
    loud_log = capture([FFMPEG, '-hide_banner', '-v', 'info', '-i', str(MASTER),
                        '-map', '0:a:0', '-vn',
                        '-af', 'loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json',
                        '-f', 'null', '-'])
    loud = json.loads(re.findall(r'\{\s*"input_i".*?\}', loud_log, re.S)[-1])
    cover_dims = {}
    for name in ('cover_nonvi_konou_9x16.jpg', 'cover_nonvi_konou_1080.jpg',
                 'cover_nonvi_konou_universelle_3000.jpg'):
        with Image.open(OUT / name) as cover:
            cover_dims[name] = list(cover.size)
    files = [CLIP, MASTER, OUT / 'cover_nonvi_konou_9x16.jpg',
             OUT / 'cover_nonvi_konou_1080.jpg',
             OUT / 'cover_nonvi_konou_universelle_3000.jpg']
    checks = {
        'clip_duration_tolerance_0_05s': abs(duration - 204.48) <= .05,
        'clip_frame_duration_tolerance_0_05s': abs(frames / 30 - 204.48) <= .05,
        'clip_dimensions_1080x1920': video.group(1, 2) == ('1080', '1920'),
        'clip_fps_30': abs(float(video.group(3)) - 30) < .001,
        'clip_audio_48k_stereo': audio.group(1, 2) == ('48000', 'stereo'),
        'blackdetect_zero': 'black_start' not in log,
        'freezedetect_zero_default_threshold': 'freeze_start' not in log,
        'flag_and_badge_color_delta_le_8': max(color_deltas.values()) <= 8,
        'master_duration_tolerance_0_05s': abs(mp3.info.length - 193.48) <= .05,
        'master_320k': mp3.info.bitrate == 320000,
        'master_48k': mp3.info.sample_rate == 48000,
        'master_lufs_tolerance_0_2': abs(float(loud['input_i']) - (-14)) <= .2,
        'master_true_peak_le_minus_1_5': float(loud['input_tp']) <= -1.5,
        'id3_required_tags': EXPECTED_TAGS <= tag_keys,
        'covers_dimensions': cover_dims == {
            'cover_nonvi_konou_9x16.jpg': [1080, 1920],
            'cover_nonvi_konou_1080.jpg': [1080, 1080],
            'cover_nonvi_konou_universelle_3000.jpg': [3000, 3000],
        },
    }
    report = {
        'status': 'PASS' if all(checks.values()) else 'FAIL',
        'checks': checks,
        'clip': {'duration_seconds': duration, 'frames': frames,
                 'frame_duration_seconds': round(frames / 30, 6),
                 'width': int(video.group(1)), 'height': int(video.group(2)),
                 'fps': float(video.group(3)), 'audio_hz': int(audio.group(1)),
                 'audio_channels': audio.group(2), 'black_events': log.count('black_start'),
                 'freeze_events_default_threshold': log.count('freeze_start')},
        'flag_badge_max_channel_delta': color_deltas,
        'master': {'duration_seconds': round(mp3.info.length, 6),
                   'bitrate': mp3.info.bitrate, 'sample_rate': mp3.info.sample_rate,
                   'loudness_lufs': float(loud['input_i']),
                   'true_peak_dbtp': float(loud['input_tp']),
                   'tag_keys': sorted(tag_keys)},
        'covers': cover_dims,
        'files': {p.name: {'bytes': p.stat().st_size, 'sha256': sha256(p)} for p in files},
    }
    path = OUT / 'CONTROLES_NONVI_KONOU.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
