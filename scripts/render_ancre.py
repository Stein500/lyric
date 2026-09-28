#!/usr/bin/env python3
"""Maquette 9:16 de l'ancre s01, pas un export final ni un alignement vocal.

Les mots sont répartis provisoirement dans les fenêtres de vers source.
Fonds sans badge ; drapeau et badge sont deux calques indépendants du Ken Burns.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from functools import lru_cache
import io
import json
import math
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
W, H, FPS = 1080, 1920, 30
CX, CY = W // 2, H // 2
SAFE_WIDTH = 720
TEXT_WIDTH = 694
LYRIC_FONT = ROOT / 'assets/fonts/BarlowCondensed-Bold.ttf'
UI_FONT = ROOT / 'assets/fonts/DejaVuSans-Bold.ttf'
FLAG_COLORS = ('#008751', '#FCD116', '#E8112D')
FOOTER_H = 54
PREVIEW_START, PREVIEW_DURATION = 113.0, 14.5
LEAD = 0.03
PAD = 12


def draw_flag(image: Image.Image, box: tuple[int, int, int, int]):
    """Géométrie vectorielle, rectangles sans anti-crénelage aux frontières."""
    x, y, width, height = box
    split_x, split_y = x + width // 3, y + height // 2
    d = ImageDraw.Draw(image)
    d.rectangle((x, y, split_x-1, y+height-1), fill=FLAG_COLORS[0])
    d.rectangle((split_x, y, x+width-1, split_y-1), fill=FLAG_COLORS[1])
    d.rectangle((split_x, split_y, x+width-1, y+height-1), fill=FLAG_COLORS[2])


def badge_alpha(t: float, start: float, end: float) -> float:
    if not start < t < end:
        return 0.0
    fade = min(0.4, (end-start) / 2)
    return max(0.0, min(0.75, 0.75*(t-start)/fade, 0.75*(end-t)/fade))


@lru_cache(maxsize=1)
def badge_sprite() -> Image.Image:
    font = ImageFont.truetype(str(UI_FONT), 40)
    width = round(font.getlength('Dsky')) + 22 + 52 + 44
    badge = Image.new('RGBA', (width, 68))
    d = ImageDraw.Draw(badge)
    d.rounded_rectangle((0, 0, width-1, 67), radius=25,
                        fill=(7, 12, 20, 245), outline=(196, 183, 153, 145), width=1)
    d.text((22, 32), 'Dsky', font=font, anchor='lm', fill=(255, 247, 230, 255))
    draw_flag(badge, (width-22-52, 17, 52, 34))
    return badge


def balanced_lines(words: list[str], font: ImageFont.FreeTypeFont, width: int) -> list[list[str]]:
    """Minimum de lignes, puis largeur équilibrée sans mot orphelin si possible."""
    n = len(words)
    widths = {(i, j): font.getlength(' '.join(words[i:j])) for i in range(n) for j in range(i+1, n+1)}
    dp = [None] * (n+1)
    dp[n] = (0, 0.0, [])
    for i in range(n-1, -1, -1):
        options = []
        for j in range(i+1, n+1):
            if widths[i, j] > width:
                break
            if dp[j] is None:
                continue
            count, cost, rest = dp[j]
            orphan_cost = width**2 * 0.7 if j-i == 1 and n > 2 else 0
            options.append((count+1, cost+(width-widths[i, j])**2+orphan_cost,
                            [words[i:j], *rest]))
        if options:
            dp[i] = min(options, key=lambda opt: (opt[0], opt[1]))
    if dp[0] is None:
        raise ValueError('Un mot dépasse la zone sûre ; ajuster la taille, jamais tronquer.')
    return dp[0][2]


@dataclass
class Word:
    text: str
    x: int
    y: int
    width: int
    mask: Image.Image


class VerseLayout:
    def __init__(self, text: str):
        self.text = text
        self.words_raw = text.split()
        for size in range(112, 87, -4):
            font = ImageFont.truetype(str(LYRIC_FONT), size)
            try:
                lines = balanced_lines(self.words_raw, font, TEXT_WIDTH)
            except ValueError:
                continue
            if len(lines) <= 4:
                break
        else:
            raise ValueError('Vers trop long : créer une mise en page approuvée, sans troncature.')
        self.size, self.font, self.lines = size, font, lines
        self.top_bearing = min(font.getbbox(word)[1] for word in self.words_raw)
        self.bottom_bearing = max(font.getbbox(word)[3] for word in self.words_raw)
        self.glyph_height = self.bottom_bearing - self.top_bearing
        self.pitch = round(size * 1.09)
        self.width = SAFE_WIDTH
        self.height = self.glyph_height + (len(lines)-1)*self.pitch + PAD*2
        self.x, self.y = CX-self.width//2, round(CY-self.height/2)
        self.words = []
        self.line_centers = []
        for i, line in enumerate(lines):
            # Use advances for each sprite and include the font's actual spaces.
            space = font.getlength(' ')
            line_width = sum(font.getlength(word) for word in line)+space*(len(line)-1)
            left = (self.width-line_width)/2
            self.line_centers.append((left, left+line_width))
            x = left
            for word in line:
                advance = font.getlength(word)
                bbox = font.getbbox(word)
                sprite = Image.new('L', (math.ceil(max(advance, bbox[2]))+PAD*2,
                                         self.glyph_height+PAD*2))
                ImageDraw.Draw(sprite).text((PAD, PAD-self.top_bearing), word, font=font, fill=255)
                self.words.append(Word(word, round(x)-PAD, i*self.pitch,
                                       math.ceil(advance), sprite))
                x += advance + space
        if [w.text for w in self.words] != self.words_raw:
            raise AssertionError('La composition a perdu ou réordonné des mots.')
        self.bounds = (self.x, self.y, self.x+self.width, self.y+self.height)
        # Colonne → déphasage spatial continu de la vague.
        self.wave_phase = np.arange(self.width, dtype=np.float32) * (2*np.pi / 320)
        self.yy, self.xx = np.indices((self.height, self.width))

    def layer(self, progress: float, t: float, force_all: bool = False) -> Image.Image:
        """Boîte complète fixe : jamais de recentrage au fur et à mesure des mots."""
        weights = np.array([max(2, len(w.text.strip('.,!?…'))) for w in self.words], dtype=float)
        ends = np.cumsum(weights) / weights.sum()
        index = min(len(self.words)-1, int(np.searchsorted(ends, min(progress, 0.999999))))
        if force_all:
            index = len(self.words)-1
        visible = Image.new('L', (self.width, self.height))
        past = Image.new('L', (self.width, self.height))
        current = Image.new('L', (self.width, self.height))
        for i, word in enumerate(self.words):
            if i > index:
                break
            (past if i < index else current).paste(word.mask, (word.x, word.y))
            visible.paste(word.mask, (word.x, word.y))
        stroke = visible.filter(ImageFilter.MaxFilter(7))
        shadow = stroke.filter(ImageFilter.GaussianBlur(3))
        layer = Image.new('RGBA', visible.size)
        ink = Image.new('RGBA', visible.size, (4, 8, 14, 0))
        ink.putalpha(shadow.point(lambda v: round(v*0.9)))
        layer.alpha_composite(ink)
        # A narrow dark outline and gentle active glow, without obscuring the face.
        outline = Image.new('RGBA', visible.size, (4, 8, 14, 0)); outline.putalpha(stroke)
        layer.alpha_composite(outline)
        glow = Image.new('RGBA', visible.size, (255, 197, 100, 0))
        glow.putalpha(current.filter(ImageFilter.GaussianBlur(4)).point(lambda v: round(v*0.38)))
        layer.alpha_composite(glow)
        old = Image.new('RGBA', visible.size, (223, 218, 208, 0))
        old.putalpha(past.point(lambda v: round(v*0.87)))
        layer.alpha_composite(old)
        active = Image.new('RGBA', visible.size, (255, 224, 164, 0)); active.putalpha(current)
        layer.alpha_composite(active)
        array = np.asarray(layer)
        shift = np.rint(4.5*np.sin(2*np.pi*0.9*t+self.wave_phase)).astype(int)
        source_y = self.yy - shift[None, :]
        valid = (source_y >= 0) & (source_y < self.height)
        warped = array[np.clip(source_y, 0, self.height-1), self.xx].copy()
        warped[~valid] = 0
        return Image.fromarray(warped)


def reframe_background(path: Path) -> Image.Image:
    image = ImageOps.fit(Image.open(path).convert('RGB'), (W, H), method=Image.Resampling.LANCZOS)
    # Lift the figure only by removing unused ceiling; never stretch the face/body.
    # Bottom extension uses only the last 8 px of empty floor, never a shoe/limb.
    shift = 120
    out = Image.new('RGB', (W, H))
    out.paste(image.crop((0, shift, W, H)), (0, 0))
    floor = image.crop((0, H-8, W, H)).resize((W, shift), Image.Resampling.BICUBIC)
    floor = floor.filter(ImageFilter.GaussianBlur(8))
    out.paste(floor, (0, H-shift))
    return out


class AnchorRenderer:
    def __init__(self, background: Path, timing_file: Path):
        self.base = reframe_background(background)
        self.canvas = self.base.resize((1188, 2112), Image.Resampling.LANCZOS)
        entries = json.loads(timing_file.read_text())
        # Third refrain: source starts at 113.28. Final displayed end is provisional.
        self.verses = []
        for i, e in enumerate(entries):
            if not 113.0 < e['start'] < 126.0:
                continue
            end = min(entries[i+1]['start'] if i+1 < len(entries) else 127.3, 127.3)
            self.verses.append({'text': e['text'], 'start': e['start']-LEAD,
                                'end': end-LEAD, 'layout': VerseLayout(e['text'])})
        if len(self.verses) != 5:
            raise ValueError('La maquette attend exactement les cinq vers du troisième refrain.')
        rows = np.arange(H, dtype=float)
        alpha = 95*np.exp(-0.5*((rows-CY)/230)**2)
        alpha *= np.clip((rows-725)/70, 0, 1)  # protect face/head above the lyric box
        scrim = np.zeros((H, W, 4), dtype=np.uint8)
        scrim[:, :, 3] = alpha[:, None].astype(np.uint8)
        self.scrim = Image.fromarray(scrim)

    def active_verse(self, t: float):
        absolute = PREVIEW_START+t
        return next((v for v in self.verses if v['start'] <= absolute < v['end']), None)

    def frame(self, t: float, force_all: bool = False) -> Image.Image:
        zoom = 1.02+0.04*min(1, t/PREVIEW_DURATION)
        cw, ch = self.canvas.width/zoom, self.canvas.height/zoom
        dx = (self.canvas.width-cw)/2*(1+0.35*math.sin(t*0.35))
        dy = (self.canvas.height-ch)/2*(1+0.25*math.sin(t*0.27))
        image = self.canvas.transform((W, H), Image.Transform.EXTENT,
                                      (dx, dy, dx+cw, dy+ch), Image.Resampling.BICUBIC).convert('RGBA')
        verse = self.active_verse(t)
        if verse:
            image.alpha_composite(self.scrim)
            absolute = PREVIEW_START+t
            progress = (absolute-verse['start']) / max(0.01, verse['end']-verse['start']-0.18)
            layout = verse['layout']
            layer = layout.layer(progress, t, force_all)
            image.alpha_composite(layer, (layout.x, layout.y))
            alpha = badge_alpha(absolute, verse['start'], verse['end'])
            badge = badge_sprite().copy()
            badge.putalpha(badge.getchannel('A').point(lambda value: round(value*alpha)))
            image.alpha_composite(badge, ((W-badge.width)//2, 156))
        draw_flag(image, (0, H-FOOTER_H, W, FOOTER_H))
        return image.convert('RGB')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, default=ROOT/'livrables/Concentre_sur_le_chemin_maquette_9x16_v1.mp4')
    p.add_argument('--still-only', action='store_true')
    args = p.parse_args()
    background = ROOT/'assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png'
    timing = ROOT/'work/concentre_sur_le_chemin/timings_audited.json'
    renderer = AnchorRenderer(background, timing)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Static approval card: complete first verse, not an invented lyric.
    still = renderer.frame(2.5, force_all=True)
    still.save(args.output.parent/'Concentre_sur_le_chemin_ancre_9x16_v1.png')
    still.save(args.output.parent/'Concentre_sur_le_chemin_ancre_9x16_v1.jpg', quality=94)
    # Clean background with only the approved footer. The clip deliberately uses raw instead.
    composed = renderer.base.copy()
    draw_flag(composed, (0, H-FOOTER_H, W, FOOTER_H))
    path = ROOT/'assets/composed/concentre_sur_le_chemin/portrait/s01_tete_lourde.png'
    path.parent.mkdir(parents=True, exist_ok=True)
    composed.save(path)
    proof = {'status': 'maquette_non_finale', 'backgrounds_generated': 1,
             'word_timing': 'provisional_character_weighted_not_forced_alignment',
             'source_audio_start': PREVIEW_START, 'duration': PREVIEW_DURATION,
             'fps': FPS, 'frames': math.ceil(PREVIEW_DURATION*FPS),
             'footer_box': [0, H-FOOTER_H, W, FOOTER_H],
             'verses': [{k: v for k, v in verse.items() if k != 'layout'} |
                       {'font_size': verse['layout'].size, 'bbox': verse['layout'].bounds,
                        'lines': [' '.join(line) for line in verse['layout'].lines]}
                       for verse in renderer.verses]}
    (ROOT/'work/concentre_sur_le_chemin/maquette_report.json').write_text(
        json.dumps(proof, ensure_ascii=False, indent=2)+'\n')
    if args.still_only:
        return
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    command = [ffmpeg, '-hide_banner', '-y', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-framerate', str(FPS),
               '-i', 'pipe:0', '-ss', str(PREVIEW_START), '-i', str(ROOT/'Concentré sur le chemin.mp3'),
               '-map', '0:v:0', '-map', '1:a:0', '-t', str(PREVIEW_DURATION),
               '-c:v', 'libx264', '-preset', 'fast', '-crf', '21', '-pix_fmt', 'yuv420p',
               '-af', 'volume=-1.6dB', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
               '-movflags', '+faststart', str(args.output)]
    log_path = ROOT/'work/concentre_sur_le_chemin/render_maquette.log'
    with log_path.open('w') as log:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=log, stderr=log)
        try:
            for i in range(math.ceil(PREVIEW_DURATION*FPS)):
                frame = renderer.frame(i/FPS)
                buffer = io.BytesIO()
                frame.save(buffer, format='JPEG', quality=94, subsampling=0)
                process.stdin.write(buffer.getbuffer())
                if i % FPS == 0:
                    print(f'Rendu {i//FPS}s / {PREVIEW_DURATION}s', flush=True)
            process.stdin.close()
            code = process.wait(timeout=180)
        except BaseException:
            process.kill()
            process.wait()
            raise
    if code:
        raise RuntimeError(log_path.read_text()[-4000:])
    print(f'Maquette créée : {args.output}', flush=True)


if __name__ == '__main__':
    main()
