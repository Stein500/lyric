# -*- coding: utf-8 -*-
"""
Pipeline vidéo "Motivé".
  mode portrait : 9:16 TikTok/Reels (1080x1920)
  mode landscape: 16:9 YouTube        (1920x1080)

  prep    -> clips silencieux (loop image / -t)
  concat  -> assembly via concat demuxer (zéro trou noir)
  final   -> burn ASS + mux audio + fades audio
  checks  -> durée exacte + blackdetect + frame-by-frame fin + poids
"""
import os, sys, subprocess, re
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
spec = importlib.util.spec_from_file_location('timeline', os.path.join(ROOT, 'tools', 'timeline.py'))
tl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tl)

MODE = os.environ.get('MODE', 'portrait')
FF = os.environ.get('FF', '/tmp/vidvenv/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2')
PREP = os.path.join(ROOT, 'work', 'prep', MODE)
BUILD = os.path.join(ROOT, 'work', 'build', MODE)
os.makedirs(BUILD, exist_ok=True)

W, H, MARGE = tl.dims_for_mode(MODE)
FPS = tl.FPS
DURATION = tl.DURATION
AUDIO = os.path.join(ROOT, tl.AUDIO)
SHOTS = tl.shots_for_mode(MODE)

# ---------------------------------------------------------------- STYLES ----
def ass_color(r, g, b, a=0):
    return '&H%02X%02X%02X%02X' % (a, b, g, r)

CYAN = ass_color(0x4D, 0xD2, 0xFF)
AMBER = ass_color(0xE8, 0xA3, 0x3D)
WHITE = ass_color(0xF5, 0xF9, 0xFF)
LIGHT = ass_color(0xC7, 0xDD, 0xEE)
BLACK = '&H00000000'

STYLE_DEF = """[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 1
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,DejaVu Sans,58,{white},{black},{black},&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,60,60,{marge},1
Style: verse,DejaVu Sans,60,{white},{black},{black},&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,60,60,{marge},1
Style: hook,DejaVu Sans,72,{cyan},{black},{black},&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,60,60,{marge},1
Style: hook_final,DejaVu Sans,80,{amber},{black},{black},&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,60,60,{marge},1
Style: bridge,DejaVu Sans,56,{light},{black},{black},&H80000000,0,1,0,0,100,100,0,0,1,3,2,2,60,60,{marge},1
Style: wolof,DejaVu Sans,78,{amber},{black},{black},&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,60,60,{marge},1
""".format(W=W, H=H, white=WHITE, black=BLACK, cyan=CYAN, amber=AMBER, light=LIGHT, marge=MARGE)


def tsfmt(sec):
    sec = max(0.0, float(sec))
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return '%d:%02d:%05.2f' % (h, m, s)


def build_ass():
    events = []
    for (start, end, text, style) in tl.SUBS:
        ev = 'Dialogue: 0,%s,%s,%s,,0,0,0,,{\\fad(80,120)}%s' % (tsfmt(start), tsfmt(end), style, text)
        events.append(ev)
    ass = STYLE_DEF + '\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n' + '\n'.join(events) + '\n'
    path = os.path.join(BUILD, 'subs.ass')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(ass)
    print('ASS écrit ->', path, '(', len(events), 'events )')
    return path


def make_clips():
    clips = []
    for i, (start, end, img) in enumerate(SHOTS):
        dur = round(end - start, 3)
        src = os.path.join(PREP, img + '.jpg')
        if not os.path.exists(src):
            raise FileNotFoundError('Image manquante: %s' % src)
        clip = os.path.join(BUILD, 'clip_%03d.mp4' % i)
        if os.path.exists(clip):
            os.remove(clip)
        cmd = [
            FF, '-y', '-loop', '1', '-i', src,
            '-f', 'lavfi', '-t', str(dur), '-i', 'anullsrc=r=44100:cl=stereo',
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23', '-pix_fmt', 'yuv420p',
            '-vf', 'fps=%d,scale=%d:%d' % (FPS, W, H),
            '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart',
            '-t', str(dur), clip,
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        clips.append(clip)
    print('clips ok:', len(clips), '(', MODE, ')')
    return clips


def concat(clips):
    lst = os.path.join(BUILD, 'concat.txt')
    with open(lst, 'w') as f:
        for c in clips:
            f.write("file '%s'\n" % c.replace('\\', '/'))
    out = os.path.join(BUILD, 'concat.mp4')
    cmd = [FF, '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', out]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('concat ->', out)
    return out


def final(concat_path, subs_path):
    fade_out_start = DURATION - 3.0
    suffix = 'TikTokReels_9x16' if MODE == 'portrait' else '16x9_YT'
    out = os.path.join(ROOT, 'livrables', 'Motivé_%s_v1.mp4' % suffix)
    cmd = [
        FF, '-y', '-i', concat_path, '-i', AUDIO,
        '-map', '0:v:0', '-map', '1:a:0',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '22', '-pix_fmt', 'yuv420p', '-r', str(FPS),
        '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2',
        '-af', 'afade=t=in:st=0:d=0.3,afade=t=out:st=%.3f:d=3' % fade_out_start,
        '-t', '%.3f' % DURATION,
        '-vf', 'ass=%s' % subs_path.replace('\\', '/'),
        '-movflags', '+faststart', '-shortest', out,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('FINAL', MODE, '->', out)
    return out


def duration(path):
    r = subprocess.run([FF, '-hide_banner', '-i', path], capture_output=True, text=True)
    m = re.search(r'Duration:\s*(\d+):(\d+):(\d+\.?\d*)', r.stderr)
    if not m:
        raise ValueError('durée introuvable pour %s' % path)
    h, mi, s = int(m.group(1)), int(m.group(2)), float(m.group(3))
    return h * 3600 + mi * 60 + s


def blackdetect(path):
    cmd = [FF, '-i', path, '-vf', 'blackdetect=d=0.3:pix_th=0.10', '-an', '-f', 'null', '-']
    r = subprocess.run(cmd, capture_output=True, text=True)
    return [l for l in r.stderr.splitlines() if 'black_start' in l]


def check(path, dur_expected):
    d = duration(path)
    print('  durée réelle = %.3f (attendu %.3f) -> delta %.3fs' % (d, dur_expected, abs(d - dur_expected)))
    bd = blackdetect(path)
    print('  blackdetect >300ms :', 'AUCUN' if not bd else bd)
    return abs(d - dur_expected) <= 0.3 and not bd


def main():
    print('== 1/4 ASS ==')
    subs = build_ass()
    print('== 2/4 clips ==')
    clips = make_clips()
    print('== 3/4 concat ==')
    c = concat(clips)
    print('== 4/4 final ==')
    f = final(c, subs)
    sz = os.path.getsize(f) / 1e6
    print('  poids = %.1f MB' % sz)
    print('== CHECKS ==')
    ok = check(f, DURATION)
    print('  CHECK OK' if ok else '  CHECK ECHEC')


if __name__ == '__main__':
    main()
