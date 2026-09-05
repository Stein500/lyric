#!/usr/bin/env python3
"""Master PCM commun au clip/MP3, deux passes EBU R128, ID3 et cover locale."""
from __future__ import annotations
import copy
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TPE2, TPUB, TCOM, TCON, TDRC, TXXX, USLT, APIC, TLEN, TSSE
from mutagen.mp3 import MP3

from je_maime_common import *
from maquette_je_maime import make_badge

BASE_FILTERS = 'highpass=f=30,lowpass=f=18000'
PCM = WORK / 'master_48k_f32.wav'
MP3_OUT = DELIVER / 'Je_maime_tellement_master_v1.mp3'
COVER = DELIVER / 'cover_Je_maime_tellement_1080.jpg'


def make_cover():
    asset = assets_by_slot()[21]
    path = resolve_asset(asset['render_source'], asset.get('sha256'))
    image = ImageOps.fit(Image.open(path).convert('RGB'), (1080, 1080), Image.Resampling.LANCZOS, centering=(.5, .19)).convert('RGBA')
    shade = Image.new('RGBA', (1, 1080))
    for y in range(1080):
        alpha = int(225 * max(0, min(1, (y - 610) / 400)))
        shade.putpixel((0, y), (6, 13, 18, alpha))
    image = Image.alpha_composite(image, shade.resize((1080, 1080)))
    letters, glow = Image.new('RGBA', image.size), Image.new('RGBA', image.size)
    d, g = ImageDraw.Draw(letters), ImageDraw.Draw(glow)
    title = "Je m'aime tellement"
    size = 122
    while font(size, cursive=True).getlength(title) > 990:
        size -= 2
    f = font(size, cursive=True)
    for canvas in (d, g):
        canvas.text((540, 765), title, font=f, anchor='mt', fill=(255, 218, 151, 255))
    image = Image.alpha_composite(image, glow.filter(ImageFilter.GaussianBlur(8)))
    image = Image.alpha_composite(image, letters)
    d = ImageDraw.Draw(image)
    d.text((540, 932), 'Daïsky Pro · Success', font=font(35, True), anchor='mt', fill='#fff4dd')
    d.text((540, 994), 'Daïsky Prod / TechStein · Rap · 2026', font=font(23), anchor='mt', fill='#c5d9d9')
    image.alpha_composite(make_badge(), (36, 36))
    image.convert('RGB').save(COVER, quality=92, subsampling=0)
    with Image.open(COVER) as check:
        assert check.size == (1080, 1080)


def encode_mp3():
    subprocess.run([FFMPEG, '-hide_banner', '-nostdin', '-v', 'error', '-y', '-i', str(PCM), '-map_metadata', '-1', '-c:a', 'libmp3lame', '-b:a', '320k', '-ar', '48000', '-ac', '2', str(MP3_OUT)], check=True)


def tag_mp3(config, audit):
    approved = config['approved']
    tags = ID3()
    fields = [(TIT2, approved['title']), (TPE1, approved['artist']), (TALB, approved['album']),
              (TPE2, 'Daïsky Prod'), (TPUB, 'TechStein / Daïsky Prod'),
              (TCOM, 'TechStein · Daïsky'), (TCON, 'Rap'), (TDRC, '2026'),
              (TLEN, str(round(audit['decoded_duration_seconds'] * 1000))),
              (TSSE, 'FFmpeg ' + imageio_ffmpeg.get_ffmpeg_version() + ' / libmp3lame')]
    for cls, value in fields:
        tags.add(cls(encoding=3, text=[value]))
    for key, value in {
        'contact':'Tel: 2290161162408 / 2290149114951',
        'email':'daiskypro@proton.me; daiskyproduction@gmail.com; techsteinsecureway@gmail.com',
        'producer':'TechStein', 'label':'Daïsky Prod',
        'source_sha256':audit['sha256'],
    }.items():
        tags.add(TXXX(encoding=3, desc=key, text=[value]))
    lyrics = '\n'.join(typography(cue['source_text']) for cue in audit['lrc']['lyrics'])
    tags.add(USLT(encoding=3, lang='fra', desc='Paroles', text=lyrics))
    tags.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=COVER.read_bytes()))
    # Préserver les informations de provenance et de piste de l'original.
    original = MP3(ROOT / config['source_audio']).tags
    if original:
        for key in ('COMM', 'WOAS', 'TCOP', 'TRCK', 'TPOS'):
            for frame in original.getall(key):
                tags.add(copy.deepcopy(frame))
        for frame in original.getall('TXXX'):
            if frame.desc.lower() == 'comment':
                tags.add(copy.deepcopy(frame))
    tags.save(MP3_OUT, v2_version=4)
    saved = ID3(MP3_OUT)
    mandatory = ['TIT2','TPE1','TALB','TPE2','TPUB','TCOM','TCON','TDRC','APIC','USLT']
    assert all(saved.getall(key) for key in mandatory)
    assert str(saved['TIT2']) == approved['title']
    assert str(saved['TPE1']) == approved['artist']
    assert str(saved['TALB']) == approved['album']
    assert saved.getall('USLT')[0].text == lyrics
    assert all(saved.getall('TXXX:' + key) for key in ('contact','email','producer','label'))
    return {'artist':str(saved['TPE1']), 'album':str(saved['TALB']), 'genre':str(saved['TCON']),
            'year':str(saved['TDRC']), 'lyrics_lines':len(lyrics.splitlines()), 'cover_dimensions':[1080,1080],
            'id3_version':list(saved.version), 'mandatory_fields':mandatory,
            'original_provenance_comments_preserved':bool(original and original.getall('COMM'))}


def main():
    config, audit = assert_sources_unchanged()
    WORK.mkdir(parents=True, exist_ok=True)
    DELIVER.mkdir(parents=True, exist_ok=True)
    source = ROOT / config['source_audio']
    n_samples = audit['decoded_samples_per_channel']
    print('Master : mesure de la source filtrée (passe 1).', flush=True)
    first, log = measure_loudness(source, BASE_FILTERS)
    (WORK / 'master_pass1.log').write_text(log)
    dump(WORK / 'master_pass1.json', first)
    loudnorm = ('loudnorm=I=-14:TP=-1.8:LRA=11:'
                f"measured_I={first['input_i']}:measured_TP={first['input_tp']}:"
                f"measured_LRA={first['input_lra']}:measured_thresh={first['input_thresh']}:"
                f"offset={first['target_offset']}:linear=true:print_format=json")
    # loudnorm peut suréchantillonner : retour à 48 kHz AVANT l'atrim en échantillons.
    filters = f'{BASE_FILTERS},{loudnorm},aresample=48000,atrim=end_sample={n_samples},asetpts=N/SR/TB'
    print('Master : application en deux passes et contrôle du PCM.', flush=True)
    process = subprocess.run([FFMPEG, '-hide_banner', '-nostdin', '-y', '-i', str(source), '-map_metadata', '-1', '-vn', '-af', filters, '-ar', '48000', '-ac', '2', '-c:a', 'pcm_f32le', str(PCM)], capture_output=True, text=True, check=True)
    (WORK / 'master_pass2.log').write_text(process.stderr)
    second = json.loads(process.stderr[process.stderr.rfind('{'):process.stderr.rfind('}')+1])
    pcm_info = decoded_audio_info(PCM)
    if pcm_info['samples_per_channel'] != n_samples:
        raise ValueError(f'Durée PCM modifiée : {pcm_info}')
    adjustments = []
    final = None
    for attempt in range(3):
        encode_mp3()
        final, _ = measure_loudness(MP3_OUT)
        print(f"MP3 décodé : {final['input_i']} LUFS / {final['input_tp']} dBTP", flush=True)
        if float(final['input_tp']) <= -1.5:
            break
        gain_db = -1.65 - float(final['input_tp'])
        adjusted = WORK / 'master_guard.wav'
        subprocess.run([FFMPEG, '-hide_banner', '-nostdin', '-v', 'error', '-y', '-i', str(PCM), '-af', f'volume={gain_db:.4f}dB', '-c:a', 'pcm_f32le', str(adjusted)], check=True)
        adjusted.replace(PCM)
        adjustments.append(gain_db)
    else:
        raise ValueError('La crête MP3 dépasse encore −1,5 dBTP')
    if abs(float(final['input_i']) + 14) > .6:
        raise ValueError('Niveau final hors de la tolérance ±0,6 LU')
    make_cover()
    metadata = tag_mp3(config, audit)
    decoded = decoded_audio_info(MP3_OUT)
    if decoded['samples_per_channel'] != n_samples:
        raise ValueError('Le MP3 final ne conserve pas exactement la durée décodée')
    assert_sources_unchanged()
    report = {
        'source':config['source_audio'], 'source_sha256':audit['sha256'],
        'output':str(MP3_OUT.relative_to(ROOT)), 'sha256':sha256(MP3_OUT),
        'pcm_for_video':str(PCM.relative_to(ROOT)), 'base_filters':BASE_FILTERS,
        'target_lufs':-14,'target_true_peak_before_mp3_dbtp':-1.8,'max_final_true_peak_dbtp':-1.5,
        'pass1':first, 'pass2':second, 'normalization_mode_actual':second.get('normalization_type'),
        'post_codec_peak_guard_gain_db':adjustments,
        'final_lufs':float(final['input_i']), 'final_true_peak_dbtp':float(final['input_tp']),
        'final_lra_lu':float(final['input_lra']), 'decoded':decoded,
        'encoded_bitrate_bps':MP3(MP3_OUT).info.bitrate, 'metadata':metadata,
        'source_audio_unchanged':True, 'lyrics_from_user_not_embedded_original_uslt':True,
    }
    dump(PROJECT / 'controle_master_v1.json', report)
    print('MP3 master et tags validés : ' + str(MP3_OUT.relative_to(ROOT)), flush=True)


if __name__ == '__main__':
    main()
