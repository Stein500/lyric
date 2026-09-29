#!/usr/bin/env python3
"""Master deux passes, MP3 audio seul puis tags/APIC, et PCM unique pour la vidéo."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

import imageio_ffmpeg
from mutagen.mp3 import MP3
from mutagen.id3 import (ID3, TIT2, TPE1, TALB, TPE2, TDRC, TXXX, USLT, APIC,
                        TSSE, WOAS, COMM, TLEN)

from build_timeline import ROOT, DURATION, HOOK, HOOK_START, HOOK_END

WORK = ROOT/'work/concentre_sur_le_chemin'
DELIVERY = ROOT/'livrables'
SOURCE = ROOT/'Concentré sur le chemin.mp3'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def run(args, log):
    p = subprocess.run([FFMPEG, '-hide_banner', '-nostdin', '-y', *args],
                       capture_output=True, text=True, timeout=240)
    (WORK/log).write_text(p.stderr)
    if p.returncode:
        raise RuntimeError(p.stderr[-4000:])
    return p


def measure(path, log):
    output = run(['-v', 'info', '-i', str(path), '-map', '0:a:0', '-vn',
                  '-af', 'loudnorm=I=-14:TP=-1.8:LRA=11:print_format=json', '-f', 'null', '-'], log)
    return json.loads(re.search(r'\{\s*"input_i".*?\}', output.stderr, re.S)[0])


def decoded_duration(path, log):
    p = run(['-v', 'info', '-progress', 'pipe:1', '-i', str(path),
             '-map', '0:a:0', '-vn', '-f', 'null', '-'], log)
    return int(re.findall(r'^out_time_us=(\d+)$', p.stdout, re.M)[-1])/1e6


def tag_master(path, cover, timeline):
    original = ID3(SOURCE)
    tags = ID3()
    tags.add(TIT2(encoding=3, text='Concentré sur le chemin'))
    tags.add(TPE1(encoding=3, text='Daïsky'))
    tags.add(TALB(encoding=3, text='Concentré sur le chemin — Single'))
    tags.add(TPE2(encoding=3, text='Daïsky'))
    tags.add(TDRC(encoding=3, text='2026'))
    tags.add(TLEN(encoding=3, text=str(round(DURATION*1000))))
    tags.add(TSSE(encoding=3, text='FFmpeg loudnorm 2-pass / libmp3lame 320 kb/s'))
    contacts = '+229 01 61 16 24 08 / +229 01 49 11 49 51'
    for key, value in [('contact', contacts), ('email', 'daiskyproduction@gmail.com'),
                       ('source_artist', str(original.get('TPE1', ''))),
                       ('producer', 'Non renseigné'), ('label', 'Non renseigné'),
                       ('source_audio_sha256', hashlib.sha256(SOURCE.read_bytes()).hexdigest())]:
        tags.add(TXXX(encoding=3, desc=key, text=value))
    tags.add(USLT(encoding=3, lang='fra', desc='', text='\n'.join(v['text'] for v in timeline['verses'])))
    tags.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover universelle', data=cover.read_bytes()))
    # Keep source provenance without copying a C2PA signature invalidated by re-encoding.
    for key in ('WOAS', 'COMM::eng'):
        if key in original:
            tags.add(original[key])
    tags.save(path, v2_version=4)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cover', type=Path, default=DELIVERY/'cover_concentre_sur_le_chemin_1080x1080.jpg')
    args = p.parse_args()
    if not args.cover.is_file():
        raise SystemExit('Créer la cover carrée avant le MP3/APIC.')
    WORK.mkdir(parents=True, exist_ok=True)
    DELIVERY.mkdir(exist_ok=True)
    timeline = json.loads((ROOT/'productions/concentre_sur_le_chemin/timings_render.json').read_text())
    analysis = json.loads((WORK/'analyse.json').read_text())
    first = analysis['loudnorm_pass1']
    norm = (f"highpass=f=30,lowpass=f=18000,loudnorm=I=-14:TP=-1.8:LRA=11:"
            f"measured_I={first['input_i']}:measured_TP={first['input_tp']}:"
            f"measured_LRA={first['input_lra']}:measured_thresh={first['input_thresh']}:"
            f"offset={first['target_offset']}:linear=false:print_format=json,aresample=48000,asetpts=N/SR/TB,apad=whole_len={round(DURATION*48000)},atrim=end_sample={round(DURATION*48000)}")
    initial = WORK/'song_master_initial.wav'
    run(['-v', 'info', '-i', str(SOURCE), '-map', '0:a:0', '-vn', '-af', norm,
         '-ar', '48000', '-ac', '2', '-t', str(DURATION), '-c:a', 'pcm_s24le', str(initial)],
        'master_pass2.log')
    destination = DELIVERY/'Concentre_sur_le_chemin_master_320k.mp3'
    gain = 0.0
    for attempt in range(3):
        run(['-i', str(initial), '-map', '0:a:0', '-vn', '-af', f'volume={gain}dB',
             '-ar', '48000', '-ac', '2', '-t', str(DURATION), '-c:a', 'libmp3lame', '-b:a', '320k',
             '-map_metadata', '-1', '-id3v2_version', '4', str(destination)], 'master_encode.log')
        measurement = measure(destination, 'master_measure.log')
        if float(measurement['input_tp']) <= -1.5:
            break
        gain += -1.68-float(measurement['input_tp'])
    else:
        raise RuntimeError('Crête MP3 trop élevée après trois contrôles.')
    if not -14.8 <= float(measurement['input_i']) <= -13.5:
        raise RuntimeError(f"Loudness MP3 inattendue : {measurement['input_i']}")
    duration = decoded_duration(destination, 'master_duration.log')
    if abs(duration-DURATION) > 0.025:
        raise RuntimeError(f'Durée MP3 {duration} différente de la source.')
    safe = WORK/'song_master.wav'
    run(['-i', str(initial), '-map', '0:a:0', '-vn', '-af', f'volume={gain}dB',
         '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s24le', str(safe)], 'master_safe_wav.log')
    end = timeline['encoded_duration']
    filters = (f'[0:a]asplit=2[full][hsrc];'
               f'[hsrc]atrim=start={HOOK_START}:end={HOOK_END},asetpts=PTS-STARTPTS,'
               f'afade=t=in:st=0:d=0.008,afade=t=out:st={HOOK-0.02}:d=0.02[hook];'
               f'[full]afade=t=out:st={DURATION-3}:d=3[music];'
               f'[hook][music]concat=n=2:v=0:a=1,apad,atrim=end_sample={round(end*48000)},asetpts=PTS-STARTPTS[out]')
    run(['-i', str(safe), '-filter_complex', filters, '-map', '[out]', '-vn',
         '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s16le', str(WORK/'video_audio.wav')],
        'video_audio.log')
    tag_master(destination, args.cover, timeline)
    mp3 = MP3(destination)
    final_duration = decoded_duration(destination, 'master_tagged_duration.log')
    assert abs(final_duration-DURATION) < 0.025
    assert mp3.info.sample_rate == 48000 and mp3.info.bitrate == 320000
    assert mp3.tags.getall('APIC') and mp3.tags.getall('USLT')
    report = {'source_duration': DURATION, 'decoded_master_duration': final_duration,
              'mp3_sample_rate': mp3.info.sample_rate, 'mp3_bitrate': mp3.info.bitrate,
              'channels': mp3.info.channels, 'pass1_prefilter': 'highpass=30,lowpass=18000',
              'pass1': first, 'pass2_target_tp': -1.8, 'codec_peak_compensation_db': gain,
              'duration_guard': 'loudnorm tail padded/trimmed to exact source duration (40 ms filter flush loss corrected)',
              'master_mp3_measurement': measurement, 'id3_version': list(mp3.tags.version),
              'tag_frames': sorted(mp3.tags.keys()),
              'unconfirmed_metadata_not_invented': ['composer', 'genre', 'publisher', 'producer', 'label'],
              'video_audio_duration': decoded_duration(WORK/'video_audio.wav', 'video_audio_duration.log'),
              'cover': str(args.cover.relative_to(ROOT)), 'file': str(destination.relative_to(ROOT)),
              'sha256': hashlib.sha256(destination.read_bytes()).hexdigest()}
    (ROOT/'productions/concentre_sur_le_chemin/audio_master_report.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
