#!/usr/bin/env python3
"""Render the strict per-unique-lyric-line Toko Longa vertical visual.

The source LRC has 63 unique lyric lines. Repeated lines reuse the image slot
of their first occurrence, as required by prompt v4.8.2. This renderer uses
one continuous 30 fps frame stream, 63 line plates, an intro, an endcard and a
five-second padded audio tail.
"""
from __future__ import annotations

import bisect
import json
import math
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps
from mutagen.mp3 import MP3
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "Nass'M RB__--TOKO-LONGA--__(Official Music Audio).mp3"
LRC = ROOT / "Nass'M RB__--TOKO-LONGA--__(Official Music Audio).lrc"
INDEX = ROOT / "assets/raw/portrait/verse_index.json"
OUTPUT = ROOT / "livrables/Toko_Longa_lyrics_9x16_v2.mp4"

W, H = 1080, 1920
FPS = 30
ADVANCE = 0.03
APAD_SECONDS = 5.0
AUDIO_DURATION = float(MP3(AUDIO).info.length)
FADE_START = AUDIO_DURATION - 3.0
TOTAL_DURATION = AUDIO_DURATION + APAD_SECONDS

FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path: str, size: int):
    return ImageFont.truetype(path, size=size)


def parse_lrc() -> list[dict]:
    raw = LRC.read_bytes().decode("latin1").replace("cSurs", "cœurs")
    rx = re.compile(r"^\[(\d+):(\d+(?:\.\d+)?)\](.*)$")
    rows: list[dict] = []
    for line in raw.splitlines():
        match = rx.match(line.strip())
        if not match:
            continue
        start = int(match.group(1)) * 60 + float(match.group(2))
        rows.append({"start": start, "text": match.group(3).strip()})
    rows.sort(key=lambda x: x["start"])
    for i, row in enumerate(rows):
        row["end"] = rows[i + 1]["start"] if i + 1 < len(rows) else AUDIO_DURATION
    return rows


def build_image_map() -> tuple[list[dict], dict[str, Path], Path, Path]:
    rows = parse_lrc()
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    by_text: dict[str, Path] = {}
    for item in index["lines"]:
        if item["image"]:
            by_text[item["text"]] = ROOT / item["image"]
    intro = ROOT / index["intro_image"]
    endcard = ROOT / index["endcard_image"]
    missing = [row["text"] for row in rows if row["text"] not in by_text]
    missing_files = [str(path) for path in by_text.values() if not path.exists()]
    for path in (intro, endcard):
        if not path.exists():
            missing_files.append(str(path))
    if missing or missing_files:
        raise FileNotFoundError(f"missing lyric map={missing}; missing files={missing_files}")
    return rows, by_text, intro, endcard


ROWS, IMAGE_MAP, INTRO_PATH, ENDCARD_PATH = build_image_map()
STARTS = [row["start"] for row in ROWS]
IMAGE_CACHE: dict[Path, Image.Image] = {}
IMAGE_PHASE: dict[Path, float] = {}


def source_plate(path: Path) -> Image.Image:
    if path not in IMAGE_CACHE:
        IMAGE_CACHE[path] = ImageOps.fit(
            Image.open(path).convert("RGB"),
            (int(W * 1.10), int(H * 1.10)),
            method=Image.Resampling.LANCZOS,
        )
        IMAGE_PHASE[path] = (len(IMAGE_CACHE) * 0.83) % 6.28
    return IMAGE_CACHE[path]


def row_at(global_t: float) -> dict | None:
    lookup = global_t + ADVANCE
    index = bisect.bisect_right(STARTS, lookup) - 1
    if index < 0 or lookup >= AUDIO_DURATION:
        return None
    return ROWS[index]


def image_key_at(global_t: float) -> Path:
    if global_t < ROWS[0]["start"] - ADVANCE:
        return INTRO_PATH
    if global_t >= FADE_START:
        return ENDCARD_PATH
    row = row_at(global_t)
    if row is None:
        return INTRO_PATH
    return IMAGE_MAP[row["text"]]


def plate_frame(path: Path, t: float) -> Image.Image:
    source = source_plate(path)
    extra_x = source.width - W
    extra_y = source.height - H
    phase = IMAGE_PHASE[path]
    x = int(extra_x * (0.50 + 0.42 * math.sin(t * 0.115 + phase)))
    y = int(extra_y * (0.50 + 0.42 * math.sin(t * 0.083 + phase * 1.31)))
    return source.crop((x, y, x + W, y + H))


def background_at(t: float) -> Image.Image:
    current_key = image_key_at(t)
    current = plate_frame(current_key, t)

    # Smoothly bridge the 0.18 seconds after each line begins, while keeping
    # the lyric itself on the exact LRC clock.
    for row in ROWS:
        cut = row["start"] - ADVANCE
        if cut <= t < cut + 0.18:
            previous_key = INTRO_PATH if row is ROWS[0] else IMAGE_MAP[ROWS[ROWS.index(row) - 1]["text"]]
            previous = plate_frame(previous_key, t)
            return Image.blend(previous, current, max(0.0, min(1.0, (t - cut) / 0.18)))

    if FADE_START <= t < FADE_START + 0.24:
        previous_row = row_at(FADE_START - ADVANCE - 0.001)
        if previous_row:
            previous = plate_frame(IMAGE_MAP[previous_row["text"]], t)
            return Image.blend(previous, plate_frame(ENDCARD_PATH, t), (t - FADE_START) / 0.24)
    return current


def text_width(draw, text, fnt, stroke=0):
    box = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke)
    return box[2] - box[0]


def wrap_text(text: str, fnt, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if not current or text_width(ImageDraw.Draw(Image.new("RGB", (1, 1))), candidate, fnt) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def lyric_layout(text: str):
    dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for size in (60, 56, 52, 48, 44, 40):
        fnt = font(FONT_BOLD, size)
        lines = wrap_text(text, fnt, 930)
        if len(lines) <= 2 and all(text_width(dummy, line, fnt, 2) <= 930 for line in lines):
            return fnt, lines
    fnt = font(FONT_BOLD, 38)
    return fnt, wrap_text(text, fnt, 930)


def centered(draw, xy, text, fnt, fill, stroke_fill=(3, 7, 16, 255), stroke_width=0):
    draw.text(xy, text, font=fnt, fill=fill, anchor="mm", stroke_width=stroke_width, stroke_fill=stroke_fill)


def draw_badge(draw):
    fnt = font(FONT_BOLD, 32)
    label = "DSKY✓"
    box = draw.textbbox((0, 0), label, font=fnt)
    bw, bh = box[2] - box[0] + 38, box[3] - box[1] + 22
    x0, y0 = (W - bw) // 2, 34
    draw.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), radius=bh // 2,
                           fill=(5, 6, 10, 210), outline=(77, 210, 255, 235), width=2)
    centered(draw, (W / 2, y0 + bh / 2 - 1), label, fnt, (245, 249, 255, 255), stroke_width=1)


def draw_cta(draw):
    x0, y0, pw, ph = (W - 360) // 2, 132, 360, 92
    draw.rounded_rectangle((x0, y0, x0 + pw, y0 + ph), radius=30,
                           fill=(5, 6, 10, 188), outline=(77, 210, 255, 195), width=2)
    centers = [x0 + 78, x0 + pw // 2, x0 + pw - 78]
    cx, cy = centers[0], y0 + ph // 2
    r = 17
    draw.ellipse((cx - r, cy - 9, cx, cy + 9), fill=(255, 90, 105, 255))
    draw.ellipse((cx, cy - 9, cx + r, cy + 9), fill=(255, 90, 105, 255))
    draw.polygon([(cx - r, cy), (cx + r, cy), (cx, cy + 31)], fill=(255, 90, 105, 255))
    cx = centers[1]
    draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), outline=(255, 222, 142, 255), width=4)
    draw.polygon([(cx - 7, cy - 9), (cx - 7, cy + 9), (cx + 10, cy)], fill=(255, 222, 142, 255))
    draw.line((cx + 18, cy - 18, cx + 18, cy - 8), fill=(255, 222, 142, 255), width=3)
    draw.line((cx + 12, cy - 13, cx + 24, cy - 13), fill=(255, 222, 142, 255), width=3)
    cx = centers[2]
    draw.rounded_rectangle((cx - 22, cy - 16, cx + 22, cy + 13), radius=8,
                           outline=(77, 210, 255, 255), width=4)
    draw.polygon([(cx - 11, cy + 11), (cx - 14, cy + 25), (cx + 2, cy + 11)], fill=(77, 210, 255, 255))


def draw_share(draw):
    cx, cy = W - 124, 260
    cyan, amber = (77, 210, 255, 240), (255, 222, 142, 240)
    draw.ellipse((cx - 65, cy - 65, cx + 65, cy + 65), outline=(77, 210, 255, 130), width=3)
    a, b, c = (cx - 25, cy + 19), (cx + 26, cy - 26), (cx + 29, cy + 38)
    draw.line((a[0], a[1], b[0], b[1]), fill=cyan, width=7)
    draw.line((a[0], a[1], c[0], c[1]), fill=amber, width=7)
    for px, py, color in ((a[0], a[1], amber), (b[0], b[1], cyan), (c[0], c[1], cyan)):
        draw.ellipse((px - 16, py - 16, px + 16, py + 16), fill=(5, 6, 10, 235), outline=color, width=5)


def draw_lyric(draw, row):
    if row is None:
        return
    fnt, lines = lyric_layout(row["text"])
    heights = [draw.textbbox((0, 0), line, font=fnt, stroke_width=2)[3] for line in lines]
    gap = 12
    total_h = sum(heights) + gap * (len(lines) - 1)
    top = H - 318 - total_h
    max_w = max(text_width(draw, line, fnt, 2) for line in lines)
    draw.rounded_rectangle((W // 2 - max_w // 2 - 28, top - 20,
                            W // 2 + max_w // 2 + 28, top + total_h + 20),
                           radius=22, fill=(3, 7, 16, 132))
    lower = row["text"].lower()
    hook = any(word in lower for word in ("toko", "longa", "réuss", "triomphe", "courageux", "brille"))
    color = (255, 222, 142, 255) if hook else (245, 249, 255, 255)
    y = top
    for i, line in enumerate(lines):
        centered(draw, (W / 2, y + heights[i] / 2), line, fnt, color, stroke_width=3)
        y += heights[i] + gap


def draw_intro_title(draw, t):
    if t > 5.5:
        return
    centered(draw, (W / 2, 520), "TOKO LONGA", font(FONT_SERIF_BOLD, 72), (255, 222, 142, 235), stroke_width=4)
    centered(draw, (W / 2, 610), "Nass'M Rodyboy", font(FONT_BOLD, 28), (245, 249, 255, 235), stroke_width=2)
    centered(draw, (W / 2, 664), "LYRIC VISUAL · TECHSTEIN / DSKY PROD", font(FONT_BOLD, 20), (77, 210, 255, 230), stroke_width=1)


def draw_endcard(draw):
    centered(draw, (W / 2, 510), "TOKO LONGA", font(FONT_SERIF_BOLD, 72), (255, 222, 142, 255), stroke_width=4)
    centered(draw, (W / 2, 610), "Nass'M Rodyboy", font(FONT_BOLD, 34), (245, 249, 255, 255), stroke_width=2)
    centered(draw, (W / 2, 690), "LYRIC VISUAL", font(FONT_BOLD, 25), (77, 210, 255, 255), stroke_width=1)
    centered(draw, (W / 2, 750), "TECHSTEIN / DSKY PROD", font(FONT_BOLD, 28), (245, 249, 255, 255), stroke_width=2)
    centered(draw, (W / 2, 820), "Wolof TechStein beat wê !", font(FONT_REGULAR, 24), (255, 222, 142, 245), stroke_width=1)


def bottom_gradient() -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    start = H - 620
    for y in range(start, H, 4):
        d.rectangle((0, y, W, y + 4), fill=(0, 0, 0, int(170 * ((y - start) / (H - start)))))
    return layer


BOTTOM = bottom_gradient()
NOISE_TILES = [Image.effect_noise((135, 240), 128).convert("L") for _ in range(12)]


def frame_at(t: float, frame_no: int) -> Image.Image:
    canvas = background_at(t).convert("RGBA")
    canvas = Image.alpha_composite(canvas, BOTTOM)
    pulse = (1.0 + 0.012 * math.sin(t * 2 * math.pi * 0.9)
             + 0.006 * math.sin(t * 2 * math.pi * 2.37)
             + 0.004 * math.sin(t * 2 * math.pi * 7.31)
             + 0.003 * math.sin(t * 2 * math.pi * 11.13))
    canvas = ImageEnhance.Brightness(canvas).enhance(pulse)
    tile = ImageChops.offset(NOISE_TILES[frame_no % len(NOISE_TILES)],
                             (frame_no * 7) % 135, (frame_no * 5) % 240)
    grain = tile.resize((W, H), Image.Resampling.BILINEAR)
    canvas = Image.blend(canvas.convert("RGB"), Image.merge("RGB", (grain, grain, grain)), 0.018).convert("RGBA")
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw_badge(draw)
    if t < 2.0:
        draw_cta(draw)
    if abs(t - AUDIO_DURATION / 2) <= 1.65:
        draw_share(draw)
    if t >= FADE_START:
        draw_endcard(draw)
    else:
        draw_intro_title(draw, t)
        draw_lyric(draw, row_at(t))
    return canvas.convert("RGB")


def render() -> None:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frames = math.ceil(TOTAL_DURATION * FPS)
    fade = f"afade=t=out:st={FADE_START:.3f}:d=3,apad=pad_dur={APAD_SECONDS:.3f}"
    command = [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo", "-pix_fmt", "rgb24",
        "-s:v", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", str(AUDIO), "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-af", fade, "-t", f"{TOTAL_DURATION:.3f}", "-movflags", "+faststart", str(OUTPUT),
    ]
    print(f"Rendering {OUTPUT.name}: {frames} frames, {TOTAL_DURATION:.3f}s", flush=True)
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    assert process.stdin is not None
    try:
        for frame_no in range(frames):
            process.stdin.write(frame_at(frame_no / FPS, frame_no).tobytes())
        process.stdin.close()
    except Exception:
        process.kill()
        process.wait()
        raise
    code = process.wait()
    if code:
        error = process.stderr.read().decode("utf-8", "replace") if process.stderr else ""
        raise RuntimeError(error[-4000:])
    print(f"Wrote {OUTPUT}", flush=True)


if __name__ == "__main__":
    render()
