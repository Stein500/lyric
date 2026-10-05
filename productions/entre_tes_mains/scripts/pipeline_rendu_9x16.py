#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pipeline rendu 9:16 — « Entre Tes Mains » (TechStein). v5.5 / v2 artiste.
v2 : 10 scenes foi, paroles Barlow Condensed Bold grandes, contour + halo.
Un seul flux de ceil(TOTAL*FPS) frames, horloge unique musique+fonds.
Usage: python3 pipeline_rendu_9x16.py [mock|full] [out.mp4]
"""
import json, math, subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = '/home/user/lyric'
P = os.path.join(ROOT, 'productions', 'entre_tes_mains')
FF = '/tmp/lyric-venv/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'
W, H, FPS = 1080, 1920, 30
CW, CH = 1188, 2112                      # canvas Ken Burns 1,1x
FONT_C = os.path.join(P, 'assets', 'GreatVibes-Regular.ttf')
FONT_L = os.path.join(P, 'assets', 'BarlowCondensed-Bold.ttf')
FONT_UI = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
HOOK = 6.0
DUR = 107.08
TAIL = 5.0
TOTAL = HOOK + DUR + TAIL                # 118.08
NFRAMES = int(math.ceil(TOTAL * FPS))    # 3543
LEAD = 0.03
WAVE_A, WAVE_F = 4.5, 0.9
MAXW = 900                               # textes grands (demande artiste)
CY = H // 2

AUD = json.load(open(os.path.join(P, 'timings_audited.json'), encoding='utf-8'))
BLOCKS = AUD['blocks']
SCENES = AUD['scenes']

GOLD = (255, 208, 88)
CREAM = (252, 244, 226)
DIM = (250, 242, 224, 235)
INK = (26, 14, 4)

fl_cache = {}
def fl(size):
    if size not in fl_cache:
        fl_cache[size] = ImageFont.truetype(FONT_L, size)
    return fl_cache[size]
fc_cache = {}
def fc(size):
    if size not in fc_cache:
        fc_cache[size] = ImageFont.truetype(FONT_C, size)
    return fc_cache[size]
fui_cache = {}
def fui(size):
    if size not in fui_cache:
        fui_cache[size] = ImageFont.truetype(FONT_UI, size)
    return fui_cache[size]

def np_rgba(img):
    return np.array(img.convert('RGBA'), dtype=np.uint8)

def text_size(draw, txt, font):
    l, t, r, b = draw.textbbox((0, 0), txt, font=font)
    return r - l, b - t

def render_word(txt, font, fill, glow=None):
    """sprite RGBA : contour sombre + halo eventuel + texte net (marges >= 8 px)."""
    pad = 14
    tmp = Image.new('RGBA', (4, 4))
    d = ImageDraw.Draw(tmp)
    w, h = text_size(d, txt, font)
    img = Image.new('RGBA', (w + pad * 2, h + pad * 2 + 10), (0, 0, 0, 0))
    if glow:
        g = Image.new('RGBA', img.size, (0, 0, 0, 0))
        dg = ImageDraw.Draw(g)
        dg.text((pad, pad), txt, font=font, fill=glow)
        g = g.filter(ImageFilter.GaussianBlur(9))
        img = Image.alpha_composite(img, g)
    d = ImageDraw.Draw(img)
    d.text((pad, pad), txt, font=font, fill=fill,
           stroke_width=5, stroke_fill=INK + (235,))
    return np.array(img, dtype=np.uint8), w, h

def blend(dst, spr, x, y, alpha=1.0):
    h_, w_ = spr.shape[:2]
    x0, y0 = int(x), int(y)
    x1, y1 = x0 + w_, y0 + h_
    cx0, cy0 = max(0, x0), max(0, y0)
    cx1, cy1 = min(W, x1), min(H, y1)
    if cx1 <= cx0 or cy1 <= cy0:
        return
    a = spr[cy0 - y0:cy1 - y0, cx0 - x0:cx1 - x0, 3:4].astype(np.float32) / 255.0
    a *= alpha
    rgb = spr[cy0 - y0:cy1 - y0, cx0 - x0:cx1 - x0, :3].astype(np.float32)
    reg = dst[cy0:cy1, cx0:cx1].astype(np.float32)
    dst[cy0:cy1, cx0:cx1] = (rgb * a + reg * (1 - a)).astype(np.uint8)

# ---------------------------------------------------------------- canvases
canvases = {}
for s in SCENES:
    im = Image.open(os.path.join(P, s['fond'])).convert('RGB')
    sc = max(CW / im.width, (CH + 16) / im.height)
    im = im.resize((int(round(im.width * sc)), int(round(im.height * sc))), Image.LANCZOS)
    lx = (im.width - CW) // 2
    ty = (im.height - CH) // 2
    canvases[s['id']] = np.array(im.crop((lx, ty, lx + CW, ty + CH)), dtype=np.uint8)

# ---------------------------------------------------------------- scrim central
scrim = np.zeros((H, W, 1), dtype=np.float32)
ys = np.arange(H).reshape(-1, 1)
band = np.exp(-((ys - CY) ** 2) / (2 * 260 ** 2))
scrim[:, :, 0] = band * 0.55

# ---------------------------------------------------------------- banniere Benin 54 px
banner = np.zeros((54, W, 3), dtype=np.uint8)
banner[:, :W // 3] = (0, 135, 81)
banner[:27, W // 3:] = (252, 209, 22)
banner[27:, W // 3:] = (232, 17, 45)

# ---------------------------------------------------------------- badge Dsky + picto Benin
def make_badge():
    f = fui(40)
    tmp = Image.new('RGBA', (4, 4)); d = ImageDraw.Draw(tmp)
    tw, th = text_size(d, 'Dsky', f)
    pw, ph = 34, 24
    gap = 12
    wtot = tw + gap + pw
    img = Image.new('RGBA', (wtot + 8, max(th, ph) + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((4, 4 + (max(th, ph) - th) // 2 - 2), 'Dsky', font=f, fill=(250, 246, 238, 255))
    bx = 4 + tw + gap
    by = 4 + (max(th, ph) - ph) // 2
    d.rectangle([bx, by, bx + pw // 3, by + ph], fill=(0, 135, 81, 255))
    d.rectangle([bx + pw // 3, by, bx + pw, by + ph // 2], fill=(252, 209, 22, 255))
    d.rectangle([bx + pw // 3, by + ph // 2, bx + pw, by + ph], fill=(232, 17, 45, 255))
    return np.array(img, dtype=np.uint8)
BADGE = make_badge()

def make_title(txt, size, fill):
    f = fc(size)
    pad = 24
    tmp = Image.new('RGBA', (4, 4)); d = ImageDraw.Draw(tmp)
    w, h = text_size(d, txt, f)
    img = Image.new('RGBA', (w + pad * 2, h + pad * 2 + 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((pad + 3, pad + 6), txt, font=f, fill=(0, 0, 0, 190))
    d.text((pad, pad), txt, font=f, fill=fill)
    return np.array(img, dtype=np.uint8)
TITLE_HOOK = make_title('Entre Tes Mains', 116, (255, 226, 156, 255))
TITLE_END = make_title('Entre Tes Mains', 132, (255, 232, 170, 255))

# ---------------------------------------------------------------- blocs paroles
def layout_block(lines_txt):
    for size in (128, 116, 104, 96, 88):
        font = fl(size)
        d = ImageDraw.Draw(Image.new('RGBA', (4, 4)))
        if all(text_size(d, ln, font)[0] <= MAXW for ln in lines_txt):
            break
    out_lines = []
    for ln in lines_txt:
        words = ln.split(' ')
        lines, cur = [], []
        for w_ in words:
            t = ' '.join(cur + [w_])
            if cur and text_size(d, t, font)[0] > MAXW:
                lines.append(' '.join(cur)); cur = [w_]
            else:
                cur.append(w_)
        if cur:
            lines.append(' '.join(cur))
        if len(lines) > 1 and len(lines[-1].split(' ')) == 1:
            last = lines.pop()
            prev = lines.pop().split(' ')
            t = ' '.join(prev[:-1] + [last])
            if text_size(d, t, font)[0] <= MAXW:
                lines.append(t)
            else:
                lines.append(' '.join(prev)); lines.append(last)
        for t in lines:
            ws = []
            for wtxt in t.split(' '):
                act, _, _ = render_word(wtxt, font, GOLD + (255,), glow=(255, 190, 70, 210))
                pas, _, _ = render_word(wtxt, font, DIM)
                w_, h_ = text_size(d, wtxt, font)
                ws.append((wtxt, act, pas, w_, h_))
            out_lines.append(ws)
    return out_lines, size

for b in BLOCKS:
    b['lines'], b['fsize'] = layout_block(b['texte'])
    d = ImageDraw.Draw(Image.new('RGBA', (4, 4)))
    line_h, widths = [], []
    for ws in b['lines']:
        tot = hh = 0
        for (t, a, p_, w_, h_) in ws:
            tot += w_ + 18
            hh = max(hh, h_)
        widths.append(tot - 18)
        line_h.append(hh)
    gap_l = 30
    bh = sum(line_h) + gap_l * (len(line_h) - 1)
    y = CY - bh // 2
    b['words'] = []
    for li, ws in enumerate(b['lines']):
        x = W // 2 - widths[li] // 2
        for (t, a, p_, w_, h_) in ws:
            b['words'].append({'act': a, 'pas': p_, 'x': x, 'y': y + (line_h[li] - h_) // 2, 'w': w_, 'h': h_})
            x += w_ + 18
        y += line_h[li] + gap_l
    b['nw'] = len(b['words'])

# ---------------------------------------------------------------- Ken Burns
def scene_at(ts):
    for s in SCENES:
        if ts < s['fin_s']:
            return s
    return SCENES[-1]

def kb_crop(canvas, t, s, idx):
    dur = s['fin_s'] - s['debut_s']
    u = min(1.0, max(0.0, (t - s['debut_s']) / dur))
    z = 1.02 + (1.08 - 1.02) * u if idx % 2 == 0 else 1.08 - (1.08 - 1.02) * u
    cw, ch = W / z, H / z
    ph = 2 * math.pi * t / max(dur, 1)
    px = 16 * math.sin(ph)
    py = 10 * math.sin(ph * 0.5 + 1.3)
    x0 = min(max(0, (CW - cw) / 2 + px), CW - cw)
    y0 = min(max(0, (CH - ch) / 2 + py), CH - ch)
    xi, yi = int(round(x0)), int(round(y0))
    cw_i = min(int(math.floor(cw)), CW - xi)
    ch_i = min(int(math.floor(ch)), CH - yi)
    crop = canvas[yi:yi + ch_i, xi:xi + cw_i]
    if crop.shape[0] != H or crop.shape[1] != W:
        crop = np.array(Image.fromarray(crop).resize((W, H), Image.BILINEAR), dtype=np.uint8)
    return crop

def block_active(tsong):
    for b in BLOCKS:
        bs = b['onset_s'] - LEAD
        if bs <= tsong < b['fin_s'] - LEAD:
            return b, bs
    return None, None

def draw_frame(t):
    if t < HOOK:
        tsong = 85.02 + t
        s = scene_at(tsong)
        frame = kb_crop(canvases[s['id']], tsong, s, SCENES.index(s))
        blend(frame, TITLE_HOOK, (W - TITLE_HOOK.shape[1]) // 2, 330 - TITLE_HOOK.shape[0] // 2, min(1.0, t / 0.4))
        b, bs = BLOCKS[15], 85.02 - LEAD
    else:
        ts = min(t - HOOK, DUR)
        s = scene_at(ts)
        idx = SCENES.index(s)
        frame = kb_crop(canvases[s['id']], ts, s, idx)
        if idx > 0 and ts < s['debut_s'] + 0.5:
            s2 = SCENES[idx - 1]
            f2 = kb_crop(canvases[s2['id']], ts, s2, idx - 1)
            a = (ts - s['debut_s']) / 0.5
            frame = (f2.astype(np.float32) * (1 - a) + frame.astype(np.float32) * a).astype(np.uint8)
        tsong = t - HOOK
        b, bs = block_active(tsong)
    frame = (frame.astype(np.float32) * (1 - scrim)).astype(np.uint8)
    if b is not None:
        be = b['fin_s'] - LEAD
        nw = b['nw']
        stag = 0.9 / max(1, nw - 1) if nw > 1 else 0.0
        for k, wd in enumerate(b['words']):
            ap = bs + k * stag
            if tsong < ap:
                continue
            al = min(1.0, (tsong - ap) / 0.18)
            nxt = bs + (k + 1) * stag
            active = tsong < nxt if k + 1 < nw else True
            dy = WAVE_A * math.sin(2 * math.pi * WAVE_F * t + 0.6 * k)
            spr = wd['act'] if active else wd['pas']
            blend(frame, spr, wd['x'], wd['y'] + dy, al if active else al * 0.95)
        a_in = min(1.0, (tsong - bs) / 0.4)
        a_out = min(1.0, (be - tsong) / 0.4)
        alpha = 0.75 * max(0.0, min(a_in, a_out))
        if t < HOOK:
            alpha = 0.75 * min(1.0, t / 0.4) * min(1.0, (HOOK - t) / 0.4)
        blend(frame, BADGE, (W - BADGE.shape[1]) // 2, 150 - BADGE.shape[0] // 2, alpha)
    frame[H - 54:H] = banner
    if t > TOTAL - TAIL:
        u = min(1.0, (t - (TOTAL - TAIL)) / 1.0)
        frame = (frame.astype(np.float32) * (1 - 0.82 * u)).astype(np.uint8)
        blend(frame, TITLE_END, (W - TITLE_END.shape[1]) // 2, 740, u)
        f1 = fui(42)
        d = ImageDraw.Draw(Image.new('RGBA', (4, 4)))
        for txt, yy in (('WhatsApp +229 01 61 16 24 08', 990),
                        ('+229 01 49 11 49 51', 1058),
                        ('daiskyproduction@gmail.com', 1126)):
            w_, h_ = text_size(d, txt, f1)
            pad = 12
            img = Image.new('RGBA', (w_ + pad * 2, h_ + pad * 2), (0, 0, 0, 0))
            dd = ImageDraw.Draw(img)
            dd.text((pad + 2, pad + 3), txt, font=f1, fill=(0, 0, 0, 170))
            dd.text((pad, pad), txt, font=f1, fill=(250, 246, 238, 255))
            blend(frame, np.array(img, dtype=np.uint8), (W - img.width) // 2, yy, u)
        blend(frame, BADGE, (W - BADGE.shape[1]) // 2, 150 - BADGE.shape[0] // 2, 0.75 * u)
    if t > TOTAL - 3:
        f = max(0.0, 1 - (t - (TOTAL - 3)) / 3.0)
        frame = (frame.astype(np.float32) * f).astype(np.uint8)
    return frame

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'full'
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(P, 'work', 'clip_9x16.mp4')
    n = NFRAMES if mode == 'full' else int(15 * FPS)
    audio = os.path.join(P, 'work', 'audio_video.wav')
    cmd = [FF, '-y', '-hide_banner', '-loglevel', 'error',
           '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0']
    if os.path.exists(audio) and mode == 'full':
        cmd += ['-i', audio, '-af', f'afade=t=out:st={TOTAL - 3}:d=3', '-c:a', 'aac', '-b:a', '192k']
    cmd += ['-c:v', 'libx264', '-preset', 'medium', '-crf', '21', '-pix_fmt', 'yuv420p',
            '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
            '-movflags', '+faststart', '-frames:v', str(n), out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        proc.stdin.write(draw_frame(t).tobytes())
        if i % 600 == 0:
            print(f'frame {i}/{n} t={t:.2f}', flush=True)
    proc.stdin.close()
    print('ffmpeg rc=', proc.wait())

if __name__ == '__main__':
    main()
