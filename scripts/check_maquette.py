#!/usr/bin/env python3
"""Contrôles de la maquette encodée : durée, mouvement, drapeau et reconstruction.

Cela ne valide ni la ressemblance ni les temps vocaux/mots, à faire approuver.
"""
import json
from pathlib import Path
import re
import subprocess

import imageio_ffmpeg
import numpy as np
from PIL import Image

from render_ancre import AnchorRenderer, ROOT, PREVIEW_START, FPS, badge_alpha


def run(ffmpeg, args):
    result = subprocess.run([ffmpeg, '-nostdin', *args], capture_output=True, timeout=180)
    if result.returncode:
        raise RuntimeError(result.stderr.decode('utf-8', errors='replace'))
    return result


def main():
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    video = ROOT/'livrables/Concentre_sur_le_chemin_maquette_9x16_v1.mp4'
    work = ROOT/'work/concentre_sur_le_chemin'
    check = run(ffmpeg, ['-hide_banner', '-v', 'info', '-progress', 'pipe:1', '-i', str(video),
                          '-map', '0:v:0', '-an', '-vf',
                          'blackdetect=d=0.1:pix_th=0.04:pic_th=0.98,freezedetect=n=-60dB:d=1',
                          '-f', 'null', '-'])
    log, progress = check.stderr.decode(), check.stdout.decode()
    (work/'qa_video.log').write_text(log)
    frames = int(re.findall(r'^frame=(\d+)$', progress, re.M)[-1])
    duration = int(re.findall(r'^out_time_us=(\d+)$', progress, re.M)[-1])/1e6
    black = [line for line in log.splitlines() if 'black_start:' in line]
    freeze = [line for line in log.splitlines() if 'freeze_start:' in line]
    streams = [line.strip() for line in log.splitlines() if 'Stream #0:' in line][:2]
    if frames != 435 or abs(duration-14.5) >= 0.05 or black or freeze:
        raise AssertionError((frames, duration, black, freeze))
    indices = [0, 20, 100, 118, 119, 130, 214, 215, 217, 270, 274, 360, 362, 434]
    # FFmpeg filter parser treats an unescaped comma as a filter separator.
    selection = '+'.join(f'eq(n\\,{i})' for i in indices)
    raw = run(ffmpeg, ['-v', 'error', '-i', str(video), '-vf', f'select={selection}',
                       '-vsync', '0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1']).stdout
    pixels = np.frombuffer(raw, dtype=np.uint8).reshape((-1, 1920, 1080, 3))
    if len(pixels) != len(indices):
        raise AssertionError('Nombre de frames de contrôle incorrect.')
    renderer = AnchorRenderer(ROOT/'assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png',
                              work/'timings_audited.json')
    comparisons = []
    for index, decoded in zip(indices, pixels):
        t = index/FPS
        expected = np.asarray(renderer.frame(t)).astype(np.int16)
        mae = float(np.mean(np.abs(decoded.astype(np.int16)-expected)))
        verse = renderer.active_verse(t)
        opacity = badge_alpha(PREVIEW_START+t, verse['start'], verse['end']) if verse else 0
        flags = [decoded[y, x].tolist() for x, y in [(180, 1893), (720, 1879), (720, 1906)]]
        comparisons.append({'frame': index, 'time': round(t, 5), 'mean_abs_rgb_error': round(mae, 4),
                            'expected_badge_opacity': round(opacity, 4), 'flag_pixels': flags})
        if mae >= 6:
            raise AssertionError(('Reconstruction trop différente', index, mae))
        for pixel, expected_color in zip(flags, [(0, 135, 81), (252, 209, 22), (232, 17, 45)]):
            if max(abs(a-b) for a, b in zip(pixel, expected_color)) > 8:
                raise AssertionError(('Drapeau incorrect', index, pixel, expected_color))
    Image.fromarray(pixels[2]).resize((360, 640), Image.Resampling.LANCZOS).save(
        work/'frame_video_mobile.jpg', quality=95)
    report = {'frames': frames, 'duration_seconds': duration, 'size_bytes': video.stat().st_size,
              'streams': streams, 'black_intervals': black, 'freeze_intervals': freeze,
              'frame_checks': comparisons, 'status': 'maquette_pending_artist_approval',
              'word_timing': 'provisional'}
    (work/'qa_maquette.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
