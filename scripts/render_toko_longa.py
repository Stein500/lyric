#!/usr/bin/env python3
"""Render the Toko Longa vertical lyric package.

The five AI-generated frames are deliberately reused as five narrative chapters:
- dry earth, night digging, unity, shining after hardship, and triumph.
The video itself is rendered as one continuous frame-accurate stream. No clips are
concatenated, so the lyric clock cannot accumulate segment drift.
"""
from __future__ import annotations

import io
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
from mutagen.id3 import APIC, COMM, ID3, TALB, TCON, TDRC, TIT2, TPE1, TPE2, TPUB, TXXX, USLT
from mutagen.mp3 import MP3
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
AUDIO_SOURCE = ROOT / "Nass'M RB__--TOKO-LONGA--__(Official Music Audio).mp3"
LRC_SOURCE = ROOT / "Nass'M RB__--TOKO-LONGA--__(Official Music Audio).lrc"
IMAGE_DIR = ROOT / "assets" / "generated" / "toko_longa"
LIVRABLES = ROOT / "livrables"
WORK = ROOT / "work" / "tmp" / "toko_longa"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 1080, 1920
FPS = 30
BASE_W, BASE_H = 1200, 2133
QUALITY = 88
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

IMAGE_FILES = [
    IMAGE_DIR / "teaser_01_terre_seche.png",
    IMAGE_DIR / "teaser_02_creuser_nuit.png",
    IMAGE_DIR / "teaser_03_unis.png",
    IMAGE_DIR / "teaser_04_on_brille.png",
    IMAGE_DIR / "teaser_05_triomphe.png",
]

# The five full-video chapters follow the song's narrative arc. Each caption still
# follows the exact timestamp in the supplied LRC; these are background chapters,
# not independent clips.
FULL_SCENES = [(0.0, 30.5), (30.5, 61.0), (61.0, 105.0), (105.0, 146.0), (146.0, 10_000.0)]
TEASER_START = 21.64
TEASER_DURATION = 27.0
TEASER_SCENES = [(0.0, 5.4), (5.4, 10.8), (10.8, 16.2), (16.2, 21.6), (21.6, 10_000.0)]
CROSSFADE = 0.8


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def load_lrc(path: Path) -> list[tuple[float, str]]:
    # The repository file is a legacy Windows-1252 LRC. Decode it once and write a
    # clean UTF-8 copy so all rendered accents remain correct.
    raw = path.read_bytes()
    text = raw.decode("cp1252")
    clean_path = ROOT / "lyrics" / "toko_longa_utf8.lrc"
    clean_path.parent.mkdir(parents=True, exist_ok=True)
    clean_path.write_text(text, encoding="utf-8")
    rows: list[tuple[float, str]] = []
    pattern = re.compile(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)$")
    for line in text.splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        minutes = int(match.group(1))
        seconds = float(match.group(2))
        lyric = match.group(3).strip()
        if lyric:
            rows.append((minutes * 60 + seconds, lyric))
    rows.sort(key=lambda row: row[0])
    return rows


def duration_seconds(path: Path) -> float:
    return float(MP3(path).info.length)


def prepare_image(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGB")
    # Fit, rather than stretch. The generated assets are near 9:16 but not exact.
    return ImageOps.fit(im, (BASE_W, BASE_H), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def scene_index(t: float, scenes: list[tuple[float, float]]) -> int:
    for index, (_, end) in enumerate(scenes):
        if t < end:
            return index
    return len(scenes) - 1


def crop_scene(im: Image.Image, t_in_scene: float, scene_number: int, scene_duration: float) -> Image.Image:
    # Gentle continuous Ken Burns motion. The image remains animated for its full
    # hold, while the frame clock stays exactly at i/FPS.
    duration = max(1.0, scene_duration)
    progress = max(0.0, min(1.0, t_in_scene / duration))
    zoom = 1.02 + 0.045 * progress
    crop_w = max(W, int(W / zoom))
    crop_h = max(H, int(H / zoom))
    max_x = BASE_W - crop_w
    max_y = BASE_H - crop_h
    phase = scene_number * 0.85
    x_center = max_x / 2 + max_x * 0.35 * math.sin(2 * math.pi * (0.12 * progress) + phase)
    y_center = max_y / 2 + max_y * 0.20 * math.cos(2 * math.pi * (0.09 * progress) + phase)
    x = int(max(0, min(max_x, x_center - crop_w / 2)))
    y = int(max(0, min(max_y, y_center - crop_h / 2)))
    return im.crop((x, y, x + crop_w, y + crop_h)).resize((W, H), Image.Resampling.LANCZOS)


def frame_background(t: float, scenes: list[tuple[float, float]], images: list[Image.Image]) -> Image.Image:
    index = scene_index(t, scenes)
    start, end = scenes[index]
    current = crop_scene(images[index], t - start, index, end - start)
    # Blend at scene boundaries instead of cutting to a black frame.
    if index > 0 and t - start < CROSSFADE:
        previous_start, previous_end = scenes[index - 1]
        previous = crop_scene(images[index - 1], max(0.0, previous_end - previous_start), index - 1, previous_end - previous_start)
        amount = max(0.0, min(1.0, (t - start) / CROSSFADE))
        return Image.blend(previous, current, amount)
    return current


def make_vertical_gradient(top_alpha: int, bottom_alpha: int, start_y: int = 0, end_y: int = H) -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for y in range(max(0, start_y), min(H, end_y)):
        p = (y - start_y) / max(1, end_y - start_y - 1)
        alpha = int(top_alpha + (bottom_alpha - top_alpha) * p)
        draw.line((0, y, W, y), fill=(0, 0, 0, alpha))
    return layer


TOP_SHADE = make_vertical_gradient(100, 0, 0, 430)
BOTTOM_SHADE = make_vertical_gradient(0, 178, 1160, H)


def rounded_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt: ImageFont.FreeTypeFont,
                 fill: tuple[int, int, int, int], stroke: int = 0, stroke_fill=(0, 0, 0, 0)) -> None:
    draw.text(xy, text, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def centered_text(draw: ImageDraw.ImageDraw, y: int, text: str, fnt: ImageFont.FreeTypeFont,
                  fill=(245, 249, 255, 255), stroke=2, stroke_fill=(0, 0, 0, 220)) -> None:
    box = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke)
    x = (W - (box[2] - box[0])) // 2
    draw.text((x, y), text, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def draw_badge(im: Image.Image) -> None:
    # Fixed, discreet top-center brand mark. It is drawn after every background and
    # never participates in the Ken Burns transform.
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    fnt = font(25)
    text = "DSKY✓"
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 17, 8
    x0 = (W - tw - 2 * pad_x) // 2
    y0 = 28
    draw.rounded_rectangle((x0, y0, x0 + tw + 2 * pad_x, y0 + th + 2 * pad_y), radius=16,
                           fill=(5, 6, 10, 190), outline=(77, 210, 255, 225), width=2)
    draw.text((x0 + pad_x, y0 + pad_y - 2), text, font=fnt, fill=(245, 249, 255, 255))
    im.alpha_composite(overlay)


def icon_base() -> Image.Image:
    """Build the three CTA icons once; fade is applied per frame."""
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    centers = [(350, 250), (540, 250), (730, 250)]
    colors = [(255, 75, 92, 230), (232, 163, 61, 235), (77, 210, 255, 235)]
    for (cx, cy), color in zip(centers, colors):
        gd.ellipse((cx - 58, cy - 58, cx + 58, cy + 58), fill=(*color[:3], 130))
    glow = glow.filter(ImageFilter.GaussianBlur(25))
    base.alpha_composite(glow)
    draw = ImageDraw.Draw(base)
    # Three discreet circles echo like / subscribe / comment without adding words.
    for (cx, cy), color in zip(centers, colors):
        draw.ellipse((cx - 48, cy - 48, cx + 48, cy + 48), fill=(5, 6, 10, 175), outline=color, width=3)
    # Like: a clean heart.
    cx, cy = centers[0]
    draw.polygon([(cx, cy + 27), (cx - 30, cy - 3), (cx - 30, cy - 18), (cx - 18, cy - 30),
                  (cx, cy - 18), (cx + 18, cy - 30), (cx + 30, cy - 18), (cx + 30, cy - 3)],
                 fill=(255, 75, 92, 255))
    # Subscribe: rounded device / plus mark.
    cx, cy = centers[1]
    draw.rounded_rectangle((cx - 25, cy - 18, cx + 25, cy + 18), radius=7,
                           fill=(232, 163, 61, 255))
    draw.line((cx - 11, cy, cx + 11, cy), fill=(5, 6, 10, 255), width=5)
    draw.line((cx, cy - 11, cx, cy + 11), fill=(5, 6, 10, 255), width=5)
    # Comment: speech bubble.
    cx, cy = centers[2]
    draw.rounded_rectangle((cx - 27, cy - 21, cx + 27, cy + 16), radius=9,
                           fill=(77, 210, 255, 255))
    draw.polygon([(cx - 13, cy + 13), (cx - 24, cy + 28), (cx - 2, cy + 14)], fill=(77, 210, 255, 255))
    draw.ellipse((cx - 14, cy - 4, cx - 7, cy + 3), fill=(5, 6, 10, 255))
    draw.ellipse((cx - 3, cy - 4, cx + 4, cy + 3), fill=(5, 6, 10, 255))
    draw.ellipse((cx + 8, cy - 4, cx + 15, cy + 3), fill=(5, 6, 10, 255))
    return base


CTA_ICONS = icon_base()


def draw_share_icon(im: Image.Image, alpha: int) -> None:
    if alpha <= 0:
        return
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx, cy = 900, 840
    nodes = [(cx - 34, cy - 28), (cx - 34, cy + 34), (cx + 36, cy + 4)]
    gd.line((nodes[0][0], nodes[0][1], nodes[2][0], nodes[2][1]), fill=(77, 210, 255, 230), width=11)
    gd.line((nodes[1][0], nodes[1][1], nodes[2][0], nodes[2][1]), fill=(232, 163, 61, 230), width=11)
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    glow.putalpha(glow.getchannel("A").point(lambda p: p * alpha // 255))
    overlay.alpha_composite(glow)
    draw = ImageDraw.Draw(overlay)
    draw.line((nodes[0][0], nodes[0][1], nodes[2][0], nodes[2][1]), fill=(77, 210, 255, alpha), width=5)
    draw.line((nodes[1][0], nodes[1][1], nodes[2][0], nodes[2][1]), fill=(232, 163, 61, alpha), width=5)
    for x, y in nodes:
        draw.ellipse((x - 17, y - 17, x + 17, y + 17), fill=(5, 6, 10, alpha), outline=(245, 249, 255, alpha), width=3)
    im.alpha_composite(overlay)


def wrap_text(text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    scratch = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if scratch.textbbox((0, 0), trial, font=fnt)[2] <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [text]


def caption_at(source_t: float, captions: list[tuple[float, str]]) -> tuple[str, float, float] | None:
    chosen = None
    for index, (start, text) in enumerate(captions):
        if start <= source_t:
            end = captions[index + 1][0] if index + 1 < len(captions) else source_t + 3.0
            chosen = (text, start, end)
        else:
            break
    return chosen


def draw_caption(im: Image.Image, source_t: float, captions: list[tuple[float, str]]) -> None:
    selected = caption_at(source_t, captions)
    if selected is None:
        return
    text, start, end = selected
    alpha = 255
    if source_t - start < 0.12:
        alpha = int(255 * max(0.0, min(1.0, (source_t - start) / 0.12)))
    if end - source_t < 0.14:
        alpha = min(alpha, int(255 * max(0.0, min(1.0, (end - source_t) / 0.14))))
    fnt = font(56)
    lines = wrap_text(text, fnt, 900)
    if len(lines) > 2:
        fnt = font(48)
        lines = wrap_text(text, fnt, 900)
    line_h = 68 if fnt.size >= 56 else 59
    box_h = 30 + line_h * len(lines)
    y0 = 1480 - (len(lines) - 1) * 30
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle((48, y0 - 19, W - 48, y0 + box_h), radius=24, fill=(3, 7, 14, int(155 * alpha / 255)))
    for i, line in enumerate(lines):
        bbox = d.textbbox((0, 0), line, font=fnt, stroke_width=2)
        x = (W - (bbox[2] - bbox[0])) // 2
        # A small continuous wave, never a letter-by-letter jump.
        y = y0 + i * line_h + int(3 * math.sin(source_t * 2.4))
        color = (245, 249, 255, alpha) if i == 0 else (232, 163, 61, alpha)
        d.text((x, y), line, font=fnt, fill=color, stroke_width=2, stroke_fill=(0, 0, 0, int(225 * alpha / 255)))
    im.alpha_composite(overlay)


def draw_intro_title(im: Image.Image, local_t: float, teaser: bool) -> None:
    # Clean title card in the negative space; it fades before the first lyric.
    if local_t > (4.0 if teaser else 4.8):
        return
    fade = max(0.0, min(1.0, 1.0 - max(0.0, local_t - 2.7) / 1.3))
    if local_t < 0.25:
        fade = min(fade, local_t / 0.25)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    a = int(255 * fade)
    title = "TOKO LONGA"
    fnt = font(82)
    bbox = d.textbbox((0, 0), title, font=fnt, stroke_width=2)
    x = (W - (bbox[2] - bbox[0])) // 2
    d.text((x, 145), title, font=fnt, fill=(232, 163, 61, a), stroke_width=2, stroke_fill=(0, 0, 0, a))
    sub = "NASS'M RODYBOY"
    sf = font(27)
    sb = d.textbbox((0, 0), sub, font=sf)
    d.text(((W - (sb[2] - sb[0])) // 2, 245), sub, font=sf, fill=(245, 249, 255, a))
    im.alpha_composite(overlay)


def draw_endcard(im: Image.Image, local_t: float, duration: float) -> None:
    if local_t < duration - 4.2:
        return
    progress = max(0.0, min(1.0, (local_t - (duration - 4.2)) / 4.2))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, int(105 * progress)))
    d = ImageDraw.Draw(overlay)
    a = int(255 * min(1.0, progress * 1.8))
    title = "TOKO LONGA"
    fnt = font(76)
    bb = d.textbbox((0, 0), title, font=fnt, stroke_width=2)
    d.text(((W - (bb[2] - bb[0])) // 2, 670), title, font=fnt, fill=(232, 163, 61, a), stroke_width=2, stroke_fill=(0, 0, 0, a))
    sf = font(32)
    for y, text in [(780, "NASS'M RODYBOY"), (838, "LYRIC VIDEO  ·  TECHSTEIN / DSKY PROD")]:
        box = d.textbbox((0, 0), text, font=sf)
        d.text(((W - (box[2] - box[0])) // 2, y), text, font=sf, fill=(245, 249, 255, a))
    im.alpha_composite(overlay)


def make_frame(local_t: float, source_start: float, duration: float, teaser: bool,
               captions: list[tuple[float, str]], images: list[Image.Image]) -> Image.Image:
    scenes = TEASER_SCENES if teaser else FULL_SCENES
    frame = frame_background(local_t, scenes, images).convert("RGBA")
    frame.alpha_composite(TOP_SHADE)
    frame.alpha_composite(BOTTOM_SHADE)
    draw_intro_title(frame, local_t, teaser)
    draw_caption(frame, source_start + local_t, captions)
    draw_endcard(frame, local_t, duration) if not teaser else None
    draw_badge(frame)
    if local_t < 2.0:
        alpha = int(255 * max(0.0, min(1.0, local_t / 0.22)))
        icons = CTA_ICONS.copy()
        icons.putalpha(icons.getchannel("A").point(lambda p: p * alpha // 255))
        frame.alpha_composite(icons)
    if teaser:
        midpoint = duration / 2
        fade = min(1.0, max(0.0, (local_t - midpoint + 0.55) / 0.35), max(0.0, (midpoint + 1.8 - local_t) / 0.35))
        draw_share_icon(frame, int(255 * fade))
    else:
        midpoint = duration / 2
        fade = min(1.0, max(0.0, (local_t - midpoint + 0.8) / 0.4), max(0.0, (midpoint + 2.0 - local_t) / 0.4))
        draw_share_icon(frame, int(255 * fade))
    return frame.convert("RGB")


def make_audio_master(path: Path, cover: Path) -> Path:
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / "toko_longa_master.mp3"
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", str(path),
           "-af", "highpass=f=30,lowpass=f=18000,loudnorm=I=-14:TP=-1.8:LRA=11",
           "-ar", "48000", "-c:a", "libmp3lame", "-b:a", "320k", "-id3v2_version", "4", str(out)]
    subprocess.run(cmd, check=True)
    tags = ID3()
    tags.add(TIT2(encoding=3, text="Toko Longa"))
    tags.add(TPE1(encoding=3, text="Nass'M Rodyboy"))
    tags.add(TALB(encoding=3, text="Toko Longa"))
    tags.add(TPE2(encoding=3, text="TechStein / DSKY Prod"))
    tags.add(TPUB(encoding=3, text="TechStein / DSKY Prod"))
    tags.add(TCON(encoding=3, text="Afro / World / Rap"))
    tags.add(TDRC(encoding=3, text="2026"))
    tags.add(TXXX(encoding=3, desc="producer", text="TechStein"))
    tags.add(TXXX(encoding=3, desc="label", text="DSKY Prod"))
    tags.add(TXXX(encoding=3, desc="credits", text="Lyrics video réalisé par TechStein / DSKY Prod"))
    tags.add(COMM(encoding=3, lang="fra", desc="Commentaire", text="Bénin × Congo — lyric video vertical 9:16"))
    lyrics = LRC_SOURCE.read_bytes().decode("cp1252")
    tags.add(USLT(encoding=3, lang="fra", desc="Lyrics", text=lyrics))
    tags.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=cover.read_bytes()))
    tags.save(out, v2_version=4)
    return out


def make_audio_clip(master: Path, start: float, duration: float, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{start:.3f}", "-t", f"{duration:.3f}",
           "-i", str(master), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out)]
    subprocess.run(cmd, check=True)


def render_video(output: Path, audio: Path, duration: float, source_start: float,
                 captions: list[tuple[float, str]], teaser: bool, images: list[Image.Image]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    frame_count = math.ceil(duration * FPS)
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
           "-f", "image2pipe", "-vcodec", "mjpeg", "-framerate", str(FPS), "-i", "-",
           "-i", str(audio), "-map", "0:v:0", "-map", "1:a:0",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
           "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
           "-af", f"afade=t=out:st={max(0.0, duration - (1.5 if teaser else 3.0)):.3f}:d={(1.5 if teaser else 3.0):.3f}",
           "-t", f"{duration:.3f}", "-movflags", "+faststart", str(output)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None
    try:
        for index in range(frame_count):
            local_t = index / FPS
            frame = make_frame(local_t, source_start, duration, teaser, captions, images)
            buf = io.BytesIO()
            frame.save(buf, format="JPEG", quality=QUALITY, optimize=False)
            proc.stdin.write(buf.getvalue())
            if index and index % (FPS * 10) == 0:
                print(f"  {output.name}: {index / FPS:6.1f}s / {duration:.1f}s", flush=True)
        proc.stdin.close()
    except BrokenPipeError:
        proc.stdin.close()
        proc.wait()
        raise RuntimeError(f"ffmpeg stopped while rendering {output}")
    code = proc.wait()
    if code:
        raise RuntimeError(f"ffmpeg exited with status {code} while rendering {output}")


def make_contact_sheet(images: list[Image.Image]) -> None:
    sheet = Image.new("RGB", (5 * 216, 430), (5, 6, 10))
    draw = ImageDraw.Draw(sheet)
    labels = ["01 TERRE", "02 NUIT", "03 UNIS", "04 BRILLE", "05 TRIOMPHE"]
    for i, (im, label) in enumerate(zip(images, labels)):
        thumb = ImageOps.fit(im, (216, 384), method=Image.Resampling.LANCZOS)
        sheet.paste(thumb, (i * 216, 0))
        draw.text((i * 216 + 8, 395), label, font=font(16), fill=(245, 249, 255))
    sheet.save(IMAGE_DIR / "contact_sheet.jpg", quality=90, optimize=True)


def make_cover(source: Image.Image, output: Path, accent: tuple[int, int, int], variant: str) -> None:
    cover = ImageOps.fit(source, (W, H), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5)).convert("RGBA")
    # Reserve a calm, legible title zone without hiding the generated scene.
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for y in range(0, 520):
        a = int(205 * (1 - y / 560))
        d.line((0, y, W, y), fill=(3, 5, 9, max(0, a)))
    for y in range(1320, H):
        a = int(180 * ((y - 1320) / (H - 1320)))
        d.line((0, y, W, y), fill=(3, 5, 9, max(0, a)))
    cover.alpha_composite(overlay)
    draw_badge(cover)
    d = ImageDraw.Draw(cover)
    title_f = font(90)
    title = "TOKO LONGA"
    box = d.textbbox((0, 0), title, font=title_f, stroke_width=2)
    d.text(((W - (box[2] - box[0])) // 2, 150), title, font=title_f,
            fill=(*accent, 255), stroke_width=2, stroke_fill=(0, 0, 0, 235))
    artist = "NASS'M RODYBOY"
    af = font(31)
    ab = d.textbbox((0, 0), artist, font=af)
    d.text(((W - (ab[2] - ab[0])) // 2, 264), artist, font=af, fill=(245, 249, 255, 255))
    # Accent rule + concise producer credit; no AI-generated spelling risk.
    d.rounded_rectangle((W // 2 - 95, 332, W // 2 + 95, 338), radius=3, fill=(*accent, 255))
    small = font(24)
    label = "BÉNIN × CONGO  ·  " + variant
    lb = d.textbbox((0, 0), label, font=small)
    d.text(((W - (lb[2] - lb[0])) // 2, 365), label, font=small, fill=(245, 249, 255, 235))
    credit = "LYRIC VIDEO  ·  TECHSTEIN / DSKY PROD"
    cb = d.textbbox((0, 0), credit, font=font(25))
    d.text(((W - (cb[2] - cb[0])) // 2, 1748), credit, font=font(25), fill=(245, 249, 255, 240))
    cover.convert("RGB").save(output, quality=92, optimize=True)


def probe(path: Path) -> None:
    cmd = [FFMPEG, "-hide_banner", "-i", str(path)]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # ffmpeg writes probe information to stderr. Keep the concise stream summary.
    print(result.stderr.split("At least one output file must be specified")[0].strip()[-1400:])


def main() -> int:
    if not AUDIO_SOURCE.exists() or not LRC_SOURCE.exists():
        print("Missing Toko Longa source files", file=sys.stderr)
        return 2
    if not all(path.exists() for path in IMAGE_FILES):
        missing = [str(p) for p in IMAGE_FILES if not p.exists()]
        print("Missing generated images:\n" + "\n".join(missing), file=sys.stderr)
        return 2
    LIVRABLES.mkdir(exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    captions = load_lrc(LRC_SOURCE)
    duration = duration_seconds(AUDIO_SOURCE)
    print(f"Audio duration: {duration:.3f}s; captions: {len(captions)}")
    images = [prepare_image(path) for path in IMAGE_FILES]
    make_contact_sheet(images)

    # Covers are built before the master so the exact cover can be embedded in ID3.
    covers = [
        LIVRABLES / "toko_longa_cover_01_9x16.jpg",
        LIVRABLES / "toko_longa_cover_02_9x16.jpg",
        LIVRABLES / "toko_longa_cover_03_9x16.jpg",
    ]
    make_cover(images[4], covers[0], (232, 163, 61), "TRIOMPHE")
    make_cover(images[1], covers[1], (77, 210, 255), "LA NUIT")
    make_cover(images[2], covers[2], (245, 249, 255), "LE CLAN")

    master = make_audio_master(AUDIO_SOURCE, covers[0])
    master_copy = LIVRABLES / "toko_longa_master_320k.mp3"
    master_copy.write_bytes(master.read_bytes())
    teaser_audio = WORK / "teaser.m4a"
    make_audio_clip(master, TEASER_START, TEASER_DURATION, teaser_audio)

    teaser = LIVRABLES / "toko_longa_teaser_9x16.mp4"
    lyric = LIVRABLES / "toko_longa_lyrics_9x16.mp4"
    print("Rendering teaser…")
    render_video(teaser, teaser_audio, TEASER_DURATION, TEASER_START, captions, True, images)
    print("Rendering full lyric video…")
    render_video(lyric, master, duration, 0.0, captions, False, images)
    print("\nFinal probes:")
    probe(teaser)
    probe(lyric)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
