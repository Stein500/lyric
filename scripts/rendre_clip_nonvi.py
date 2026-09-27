#!/usr/bin/env python3
"""Rend le clip lyrics vertical approuvé de « Nonvi Konou ».

Architecture légère et reproductible : concat de fonds validés, lent mouvement
photographique, puis paroles ASS. Chaque mot garde sa place finale ; la couleur
progresse mot à mot pendant qu'une onde d'eau anime simultanément les mots.
Le badge n'est PAS redessiné : il est déjà incrusté sur chaque fond validé.
"""
from __future__ import annotations

import argparse
import bisect
import json
import math
import shutil
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'nonvi_konou'
FONTS = ROOT / 'assets' / 'fonts'
WORK = ROOT / 'work' / 'final_nonvi'
OUT = ROOT / 'livrables'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
HOOK_START = 135.56
HOOK_DURATION = 6.0
SONG_DURATION = 193.48
ENDCARD_DURATION = 5.0
TOTAL_DURATION = HOOK_DURATION + SONG_DURATION + ENDCARD_DURATION
FPS = 30


def ts(seconds: float) -> str:
    centis = max(0, round(seconds * 100))
    h, r = divmod(centis, 360000)
    m, r = divmod(r, 6000)
    s, cs = divmod(r, 100)
    return f'{h}:{m:02d}:{s:02d}.{cs:02d}'


def ass_escape(text: str) -> str:
    return text.replace('\\', r'\\').replace('{', r'\{').replace('}', r'\}')


def rgba_to_ass(rgb):
    r, g, b = rgb
    return f'&H{b:02X}{g:02X}{r:02X}&'


def split_lines(words, font, max_width=850):
    lines = []
    current = []
    for word in words:
        candidate = current + [word]
        width = font.getlength(' '.join(candidate))
        if current and width > max_width:
            lines.append(current)
            current = [word]
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def layout(text: str):
    # 86 px garde les vers longs dans 2–3 lignes sans troncature.
    font = ImageFont.truetype(FONTS / 'GreatVibes-latin.ttf', 86)
    words = text.split()
    lines = split_lines(words, font)
    row_gap = 108
    block_h = len(lines) * row_gap
    top = 960 - block_h / 2
    entries = []
    flat = 0
    for row, line in enumerate(lines):
        widths = [font.getlength(w) for w in line]
        spaces = [font.getlength(' ')] * max(0, len(line) - 1)
        total = sum(widths) + sum(spaces)
        x = (1080 - total) / 2
        for i, (word, width) in enumerate(zip(line, widths)):
            entries.append({'word': word, 'x': x, 'y': top + row * row_gap, 'index': flat})
            x += width + (spaces[i] if i < len(spaces) else 0)
            flat += 1
    return entries, top, top + block_h


def dialogue(layer, start, end, style, text):
    return f'Dialogue: {layer},{ts(start)},{ts(end)},{style},,0,0,0,,{text}'


def wave_polygon(y: float, phase: float):
    xs = list(range(260, 821, 28))
    upper = [(x, y + 4 * math.sin(x / 51 + phase)) for x in xs]
    lower = [(x, yy + 2.2) for x, yy in reversed(upper)]
    pts = upper + lower
    return 'm ' + ' l '.join(f'{round(x)} {round(yy)}' for x, yy in pts)


def lyric_events(start, end, text):
    entries, top, bottom = layout(text)
    words = [e['word'] for e in entries]
    weights = [max(1.0, len(w.strip(".,!?…()'\"")) ** .58) for w in words]
    accum = []
    running = 0.0
    for weight in weights:
        running += weight
        accum.append(running)
    total_weight = running
    events = []
    # Scrim central unique, doux et indépendant du changement de mot.
    y0, y1 = max(660, top - 46), min(1280, bottom + 34)
    rect = (r'{\an7\pos(0,0)\p1\bord0\blur16\1c&H07101A&\1a&H58&}'
            f'm 82 {round(y0)} l 998 {round(y0)} l 998 {round(y1)} l 82 {round(y1)}')
    events.append(dialogue(0, start, end, 'Vector', rect))
    step = .10
    t = start
    while t < end - .001:
        stop = min(end, t + step)
        p = min(.999999, max(0.0, ((t + stop) * .5 - start) / max(.01, end - start)))
        active = bisect.bisect_right(accum, p * total_weight)
        active = min(active, len(words) - 1)
        phase = 2 * math.pi * .62 * (t - start)
        for entry in entries:
            i = entry['index']
            dy = 5.2 * math.sin(entry['x'] / 82 + phase)
            if i < active:
                color, alpha, border, blur = (255, 248, 232), '18', 2.2, .35
            elif i == active:
                color, alpha, border, blur = (255, 214, 122), '00', 3.1, 1.15
            else:
                color, alpha, border, blur = (226, 234, 235), '48', 2.0, .25
            tag = (r'{\an7'
                   f'\\pos({entry["x"]:.1f},{entry["y"] + dy:.1f})'
                   f'\\1c{rgba_to_ass(color)}\\1a&H{alpha}&'
                   f'\\bord{border:.1f}\\blur{blur:.2f}\\shad0}}')
            events.append(dialogue(2, t, stop, 'Lyric', tag + ass_escape(entry['word'])))
        poly = wave_polygon(bottom + 5, phase)
        tag = (r'{\an7\pos(0,0)\p1\bord0\blur1.8\1c&H7AD6FF&\1a&H55&}' + poly)
        events.append(dialogue(1, t, stop, 'Vector', tag))
        t = stop
    return events


def make_ass(report):
    header = """[Script Info]
Title: Nonvi Konou — paroles vague et progression mot à mot
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes
WrapStyle: 2
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Lyric,Great Vibes,86,&H00E8F8FF,&H000000FF,&H00201008,&H00000000,0,0,0,0,100,100,0,0,1,2.3,0,7,0,0,0,1
Style: Vector,DejaVu Sans,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Title,Great Vibes,148,&H009CDEFF,&H000000FF,&H00201508,&H90000000,0,0,0,0,100,100,0,0,1,3,1,8,80,80,0,1
Style: Artist,DejaVu Sans,43,&H00F3F5F7,&H000000FF,&H00130C06,&H80000000,-1,0,0,0,100,100,2,0,1,2,0,8,80,80,0,1
Style: UI,DejaVu Sans,34,&H00E3D8BE,&H000000FF,&H00130C06,&H80000000,-1,0,0,0,100,100,1,0,1,2,0,8,80,80,0,1
Style: Badge,DejaVu Sans,48,&H00FAFAFF,&H000000FF,&H00120A04,&H00000000,-1,0,0,0,100,100,0,0,1,1,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = report['lines']
    events = []
    # Incrustations statiques APRÈS le Ken Burns : jamais de badge ni bandeau mobile.
    # Pied de page exact, 54 px : tiers vert puis jaune au-dessus du rouge.
    def shape(color, path, layer=8, border=0, border_color='&H000000&', alpha='00'):
        tag = (r'{\an7\pos(0,0)\p1'
               f'\\bord{border}\\1c{color}\\3c{border_color}\\1a&H{alpha}&}}')
        events.append(dialogue(layer, 0, TOTAL_DURATION, 'Vector', tag + path))
    shape('&H65C2EC&', 'm 0 1864 l 1080 1864 l 1080 1866 l 0 1866')
    shape('&H518700&', 'm 0 1866 l 360 1866 l 360 1920 l 0 1920')
    shape('&H16D1FC&', 'm 360 1866 l 1080 1866 l 1080 1893 l 360 1893')
    shape('&H2D11E8&', 'm 360 1893 l 1080 1893 l 1080 1920 l 360 1920')
    # Badge sombre arrondi, libellé Dsky et pictogramme béninois vectoriel.
    rounded = ('m 395 160 l 685 160 b 702 160 715 173 715 190 l 715 209 '
               'b 715 226 702 239 685 239 l 395 239 b 378 239 365 226 365 209 '
               'l 365 190 b 365 173 378 160 395 160')
    shape('&H1A1203&', rounded, layer=8, border=2, border_color='&H9ADAF8&', alpha='18')
    shape('&H518700&', 'm 587 177 l 613 177 l 613 225 l 587 225', layer=9)
    shape('&H16D1FC&', 'm 613 177 l 666 177 l 666 201 l 613 201', layer=9)
    shape('&H2D11E8&', 'm 613 201 l 666 201 l 666 225 l 613 225', layer=9)
    events.append(dialogue(10, 0, TOTAL_DURATION, 'Badge',
                           r'{\an7\pos(391,164)}Dsky'))
    # Cold-open : seulement les deux vers retenus, sur six secondes.
    events.append(dialogue(3, 0, 6, 'UI', r'{\an8\pos(540,325)\fad(180,260)}REFRAIN'))
    events.append(dialogue(3, 0, 6, 'Title', r'{\an8\pos(540,390)\fad(180,260)}Nonvi Konou'))
    events += lyric_events(0, lines[41]['end'] - lines[41]['start'], lines[41]['text'])
    hook_second_end = min(6.0, lines[42]['end'] - lines[41]['start'])
    events += lyric_events(lines[41]['end'] - lines[41]['start'], hook_second_end, lines[42]['text'])
    # Titre dans l'intro de la chanson complète.
    events.append(dialogue(3, 6.20, 9.50, 'Title', r'{\an8\pos(540,710)\fad(350,350)}Nonvi Konou'))
    events.append(dialogue(3, 6.35, 9.50, 'Artist', r'{\an8\pos(540,885)\fad(450,350)}DAÏSKY'))
    for line in lines:
        events += lyric_events(HOOK_DURATION + line['start'], HOOK_DURATION + line['end'], line['text'])
    end = HOOK_DURATION + SONG_DURATION
    # Endcard simple : titre cursif, artiste, WhatsApp et email seulement.
    events.append(dialogue(3, end + .15, end + 4.80, 'Title',
                           r'{\an8\pos(540,600)\fad(350,450)}Nonvi Konou'))
    events.append(dialogue(3, end + .25, end + 4.75, 'Artist',
                           r'{\an8\pos(540,800)\fad(420,450)}DAÏSKY'))
    events.append(dialogue(3, end + .55, end + 4.65, 'UI',
                           r'{\an8\pos(540,1030)\fad(500,450)}WhatsApp  +229 01 61 16 24 08  /  +229 01 49 11 49 51'))
    events.append(dialogue(3, end + .75, end + 4.60, 'UI',
                           r'{\an8\pos(540,1110)\fad(500,450)}daiskyproduction@gmail.com'))
    ass = WORK / 'nonvi_konou.ass'
    ass.write_text(header + '\n'.join(events) + '\n', encoding='utf-8')
    return ass, len(events)


def make_clean_fonds(plan):
    """Retire les incrustations des copies de travail avant mouvement caméra.

    Les éléments exacts seront reposés une seule fois, immobiles, après le Ken Burns.
    Le remplissage interpolé reste invisible sous l'incrustation.
    """
    clean_dir = WORK / 'fonds_clean'
    clean_dir.mkdir(exist_ok=True)
    names = {x['image'] for x in plan}
    for name in sorted(names):
        source = ASSETS / name
        target = clean_dir / name
        if target.exists() and target.stat().st_mtime >= source.stat().st_mtime:
            continue
        arr = np.array(Image.open(source).convert('RGB'))
        # Interpolation dans les rectangles badge + bandeau, contour inclus.
        # Badge : interpolation verticale entre le ciel juste au-dessus et au-dessous.
        for y in range(148, 252):
            p = (y - 147) / (252 - 147)
            arr[y, 352:728] = ((1 - p) * arr[147, 352:728].astype('f4') +
                               p * arr[252, 352:728].astype('f4')).astype('uint8')
        # Bas : prolonger naturellement la dernière rangée photographique valide.
        arr[1862:1920] = arr[1861:1862]
        Image.fromarray(arr).save(target, optimize=True)
    return clean_dir


def make_concat(report, plan, clean_dir):
    by_text = {x['text']: x for x in plan}
    lines = report['lines']
    seq = []
    # Hook 6 s : premier fond 2,18 s, second fond jusqu'à 6 s.
    first_dur = lines[41]['end'] - lines[41]['start']
    seq.append((by_text[lines[41]['text']]['image'], first_dur))
    seq.append((by_text[lines[42]['text']]['image'], HOOK_DURATION - first_dur))
    # Chanson complète, avec fond d'intro jusqu'au premier timestamp.
    seq.append(('s00_intro_habillee.png', lines[0]['start']))
    for line in lines:
        seq.append((by_text[line['text']]['image'], line['end'] - line['start']))
    seq.append(('s36_endcard_habillee.png', ENDCARD_DURATION))
    assert abs(sum(d for _, d in seq) - TOTAL_DURATION) < .001
    path = WORK / 'fonds_concat.txt'
    chunks = []
    for image, duration in seq:
        full = (clean_dir / image).resolve()
        if not full.exists():
            raise FileNotFoundError(full)
        chunks += [f"file '{full}'", f'duration {duration:.5f}']
    chunks.append(f"file '{(clean_dir / seq[-1][0]).resolve()}'")
    path.write_text('\n'.join(chunks) + '\n')
    return path, len(seq)


def make_clip_audio(normalized):
    output = WORK / 'nonvi_konou_clip_audio.wav'
    graph = (
        f'[0:a]atrim=start={HOOK_START}:end={HOOK_START + HOOK_DURATION},asetpts=PTS-STARTPTS,'
        'afade=t=in:st=0:d=0.12,afade=t=out:st=5.65:d=0.35[hook];'
        f'[1:a]atrim=start=0:end={SONG_DURATION},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.15[song];'
        f'[hook][song]concat=n=2:v=0:a=1,apad=pad_dur={ENDCARD_DURATION}[a]'
    )
    subprocess.run([FFMPEG, '-hide_banner', '-y', '-v', 'warning', '-i', str(normalized),
                    '-i', str(normalized), '-filter_complex', graph, '-map', '[a]', '-ar', '48000', '-ac', '2',
                    '-c:a', 'pcm_s24le', '-t', f'{TOTAL_DURATION:.3f}', str(output)], check=True)
    return output


def render(concat, ass, audio, output, seconds):
    duration = min(TOTAL_DURATION, seconds) if seconds else TOTAL_DURATION
    runtime_fonts = WORK / 'fonts'
    runtime_fonts.mkdir(exist_ok=True)
    for name in ('GreatVibes-latin.ttf', 'DejaVuSans-Bold.ttf'):
        shutil.copy2(FONTS / name, runtime_fonts / name)
    vf = (
        "fps=30,scale=1120:1992:flags=lanczos,"
        "crop=1080:1920:x='20+20*sin(t*0.16)':y='36+30*sin(t*0.11+1)',"
        "noise=alls=8:allf=t+u,"
        f"ass=filename={ass}:fontsdir={runtime_fonts},format=yuv420p"
    )
    cmd = [FFMPEG, '-hide_banner', '-y', '-v', 'warning', '-f', 'concat', '-safe', '0',
           '-i', str(concat), '-i', str(audio), '-vf', vf, '-map', '0:v:0', '-map', '1:a:0',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '21', '-maxrate', '2600k', '-bufsize', '5200k',
           '-r', str(FPS), '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
           '-movflags', '+faststart', '-t', f'{duration:.3f}', str(output)]
    print('+', ' '.join(cmd))
    subprocess.run(cmd, check=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--preview-seconds', type=float, default=0,
                   help='Rend seulement les premières secondes dans work/.')
    p.add_argument('--prepare-only', action='store_true')
    args = p.parse_args()
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(exist_ok=True)
    report = json.loads((ROOT / 'work' / 'timings_validated.json').read_text())
    plan = json.loads((ASSETS / 'plan_images.json').read_text())
    if len(plan) != 37 or any(x['status'] != 'created' for x in plan):
        raise RuntimeError('Le manifeste visuel n’est pas complet et validé (37/37 attendu).')
    ass, events = make_ass(report)
    clean_dir = make_clean_fonds(plan)
    concat, segments = make_concat(report, plan, clean_dir)
    normalized = WORK / 'nonvi_konou_normalise_48k.wav'
    if not normalized.exists():
        raise FileNotFoundError('Lancer d’abord scripts/finaliser_audio_covers_nonvi.py')
    audio = make_clip_audio(normalized)
    print(f'Préparation : {events} événements ASS, {segments} segments, {TOTAL_DURATION:.2f} s')
    if args.prepare_only:
        return
    if args.preview_seconds:
        output = WORK / f'preview_{args.preview_seconds:g}s.mp4'
    else:
        output = OUT / 'Nonvi_Konou_9x16_v1.mp4'
    render(concat, ass, audio, output, args.preview_seconds)
    print('Clip rendu :', output)


if __name__ == '__main__':
    main()
