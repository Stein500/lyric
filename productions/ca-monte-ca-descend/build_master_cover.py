#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Master MP3 320 kb/s + covers 9:16 et 1080×1080 — « Ça monte, ça descend ».

- Loudnorm deux passes (mesures de la passe 1 réutilisées) : cible −14 LUFS, TP −1,5 dBTP,
  puis limiteur de crête à −1,5 dBTP (filet de sécurité pour les intersample).
- MP3 320 kb/s, 48 kHz, stéréo, ID3v2.4 : titre, artiste, pochette APIC carrée, paroles USLT.
- Covers : 9:16 1080×1920 (titre en post, zones de sécurité) et carrée 1080×1080.
Aucun genre ni producteur inventé. Le commentaire source « made with suno » est conservé.
"""
import os
import re
import json
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from mutagen.id3 import ID3, ID3NoHeaderError, APIC, USLT, TIT2, TPE1, TXXX, COMM, TSSE
from mutagen.mp3 import MP3

REPO = '/home/user/lyric'
ROOT = os.path.join(REPO, 'productions/ca-monte-ca-descend')
SRC = os.path.join(REPO, 'Ça monte_ ça descend.mp3')
FF = os.environ.get('FFMPEG', '/tmp/lyric-venv/bin/ffmpeg')
FONT = os.path.join(REPO, 'dsky-quotes/assets/fonts/Montserrat.ttf')
LIV = os.path.join(REPO, 'livrables')
TMP = '/tmp/work'
TITLE = 'Ça monte, ça descend'
ARTIST = 'Dsky'
MASTER = os.path.join(LIV, 'Ca_monte_ca_descend_master_320k.mp3')
COVER_916 = os.path.join(LIV, 'cover_ca_monte_ca_descend_9x16.jpg')
COVER_SQ = os.path.join(LIV, 'cover_ca_monte_ca_descend_1080x1080.jpg')
ANCRE = os.path.join(ROOT, 'personnages/ancre-couple-v2.jpg')
LRC = os.path.join(ROOT, 'timings_source.lrc')


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr[-2000:])
    return r


def measure(path):
    """Passe 1 loudnorm : valeurs mesurées (JSON émis en niveau info)."""
    r = subprocess.run([FF, '-hide_banner', '-i', path, '-map', '0:a:0', '-vn',
                        '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True)
    txt = r.stderr
    js = txt[txt.rfind('{'):txt.rfind('}') + 1]
    return json.loads(js)


def build_master():
    m1 = measure(SRC)
    print('passe 1 :', {k: m1[k] for k in ('input_i', 'input_tp', 'input_lra', 'input_thresh', 'target_offset')})
    os.makedirs(TMP, exist_ok=True)
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11"
          f":measured_I={m1['input_i']}:measured_TP={m1['input_tp']}"
          f":measured_LRA={m1['input_lra']}:measured_thresh={m1['input_thresh']}"
          f":offset={m1['target_offset']}:linear=false,"
          f"alimiter=limit=0.79:attack=5:release=50:level=disabled")
    run([FF, '-hide_banner', '-loglevel', 'error', '-y', '-i', SRC, '-map', '0:a:0', '-vn',
         '-af', af, '-ar', '48000', '-ac', '2',
         '-c:a', 'libmp3lame', '-b:a', '320k', '-id3v2_version', '0', '-write_xing', '1',
         MASTER])
    m2 = measure(MASTER)
    print('master mesuré :', {k: m2[k] for k in ('input_i', 'input_tp', 'input_lra')})
    return m2


def lyrics_plain():
    out = []
    for raw in open(LRC, encoding='utf-8'):
        s = raw.replace('\u200e', '').replace('\u200f', '').strip()
        m = re.match(r'\[(\d+):(\d+(?:\.\d+)?)\](.*)$', s)
        if m:
            out.append(m.group(3).strip())
    return '\n'.join(out)


def tag_master(cover_path):
    try:
        t = ID3(MASTER)
    except ID3NoHeaderError:
        t = ID3()
    t.delall('APIC'); t.delall('USLT'); t.delall('TIT2'); t.delall('TPE1'); t.delall('COMM')
    t.add(TIT2(encoding=3, text=TITLE))
    t.add(TPE1(encoding=3, text=ARTIST))
    t.add(TSSE(encoding=3, text='ffmpeg libmp3lame 320k, loudnorm -14 LUFS / TP -1.5 dBTP'))
    t.add(USLT(encoding=3, lang='fra', desc='', text=lyrics_plain()))
    t.add(COMM(encoding=3, lang='eng', desc='', text='Source : commentaire d\'origine « made with suno » conservé'))
    t.add(TXXX(encoding=3, desc='contenu IA', text='généré avec Suno (commentaire source)'))
    with open(cover_path, 'rb') as fh:
        t.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=fh.read()))
    t.save(MASTER, v2_version=4)


def font(size, weight):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([weight])
    return f


def gold_text(canvas, text, size, weight, cx, cy, tracking=0):
    f = font(size, weight)
    ws = [f.getlength(c) for c in text]
    tw = sum(ws) + tracking * (len(text) - 1)
    asc, desc = f.getmetrics()
    w, h = int(tw) + 60, asc + desc + 60
    mask = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(mask)
    x = 30
    for c, wc in zip(text, ws):
        d.text((x, 30 + asc), c, font=f, fill=255, anchor='ls')
        x += wc + tracking
    # ombre
    sh = Image.new('L', (w, h), 0)
    sh.paste(mask, (0, 8))
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    black = Image.new('RGBA', (w, h), (0, 0, 0, 255))
    black.putalpha(sh.point(lambda v: int(v * 0.7)))
    # dégradé or
    t = np.linspace(0, 1, h)[:, None]
    c1, c2 = np.array((255, 242, 178.)), np.array((255, 170, 50.))
    arr = np.broadcast_to((c1 * (1 - t) + c2 * t)[:, None, :], (h, w, 3))
    col = Image.fromarray(np.dstack([arr, np.full((h, w), 255.)]).astype(np.uint8), 'RGBA')
    col.putalpha(mask)
    layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    layer.alpha_composite(black)
    layer.alpha_composite(col)
    canvas.alpha_composite(layer, (int(cx - w / 2), int(cy - h / 2)))


def cover_916():
    base = Image.open(ANCRE).convert('RGB')
    r = max(1080 / base.width, 1920 / base.height)
    base = base.resize((int(base.width * r) + 1, int(base.height * r) + 1), Image.LANCZOS)
    x0, y0 = (base.width - 1080) // 2, (base.height - 1920) // 2
    img = base.crop((x0, y0, x0 + 1080, y0 + 1920)).convert('RGBA')
    # voile bas pour le titre (zone lisible, hors zones UI)
    y = np.arange(1920)[:, None].astype(float)
    a = np.clip((y - 1150) / 500.0, 0, 1) * 185
    arr = np.zeros((1920, 1080, 4), np.uint8)
    arr[:, :, 3] = np.broadcast_to(a, (1920, 1080)).astype(np.uint8)
    img.alpha_composite(Image.fromarray(arr, 'RGBA'))
    # badge sans drapeau
    bf = font(40, 800)
    bw, bh = 220, 92
    badge = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
    ImageDraw.Draw(badge).rounded_rectangle([0, 0, bw - 1, bh - 1], radius=46,
                                            fill=(8, 6, 18, 150), outline=(255, 255, 255, 70), width=2)
    ImageDraw.Draw(badge).text((bw / 2, bh / 2), 'DSKY', font=bf, fill=(255, 255, 255, 230), anchor='mm')
    img.alpha_composite(badge, (430, 160))
    # titre : deux lignes, centré, zone 1330–1520
    gold_text(img, 'Ça monte,', 118, 900, 540, 1365)
    gold_text(img, 'ça descend', 118, 900, 540, 1490)
    img.convert('RGB').save(COVER_916, quality=92, subsampling=0, optimize=True)


def cover_square():
    base = Image.open(COVER_916).convert('RGB')
    sq = base.crop((0, 380, 1080, 1460)).resize((1080, 1080), Image.LANCZOS)
    sq.save(COVER_SQ, quality=92, subsampling=0, optimize=True)


def main():
    os.makedirs(LIV, exist_ok=True)
    cover_916()
    cover_square()
    build_master()
    tag_master(COVER_SQ)
    mp3 = MP3(MASTER)
    print('MP3 :', round(mp3.info.length, 2), 's', mp3.info.bitrate // 1000, 'kb/s', mp3.info.sample_rate, 'Hz')
    print('fichiers :', MASTER, COVER_916, COVER_SQ, sep='\n')


if __name__ == '__main__':
    main()
