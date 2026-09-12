#!/usr/bin/env python3
"""Render the Toko Longa vertical package.

This renderer deliberately keeps the video as one continuous frame stream. It
uses the five requested teaser plates, complementary lyric plates, PIL overlays
and the source MP3. ffmpeg is supplied by imageio-ffmpeg in the local ignored
work/ environment; no binary is stored in the repository.
"""
from __future__ import annotations

import argparse
import io
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from mutagen.id3 import APIC, COMM, ID3, TALB, TCON, TDRC, TIT2, TPE1, TPE2, TXXX, USLT
from mutagen.mp3 import MP3
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "Nass'M RB__--TOKO-LONGA--__(Official Music Audio).mp3"
LRC = ROOT / "Nass'M RB__--TOKO-LONGA--__(Official Music Audio).lrc"
OUT = ROOT / "livrables"
RAW_TEASER = ROOT / "assets" / "raw" / "teaser"
RAW_COVERS = ROOT / "assets" / "raw" / "covers"

W, H = 1080, 1920
FPS = 30
ADVANCE = 0.03
TEASER_START = 112.73
TEASER_END = 140.68
TEASER_DURATION = TEASER_END - TEASER_START

FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

# All source plates are intentionally text-free. The identity mark and all
# typography are applied here, in post, so they remain exact and static.
PLATE_PATHS = {
    "dry": RAW_TEASER / "01_terre_dure.png",
    "walk": RAW_TEASER / "01_pas_de_pluie.png",
    "mine": RAW_TEASER / "02_creuse_la_nuit.png",
    "mine_group": RAW_TEASER / "02_creuser_la_nuit.png",
    "water": RAW_TEASER / "03_goutte_lingot.png",
    "clan": RAW_TEASER / "03_clan_uni.png",
    "village": RAW_TEASER / "04_clan_soude.png",
    "diamonds": RAW_TEASER / "04_recolte_diamants.png",
    "triumph": RAW_TEASER / "05_triomphe.png",
}

# The complete lyric visual uses a small number of narrative plates to keep
# this first package practical. Each switch is aligned to a lyrical section;
# the 5-image teaser itself is kept separate and exact.
FULL_SEGMENTS = [
    (0.00, 21.64, "dry"),
    (21.64, 32.97, "walk"),
    (32.97, 40.11, "mine"),
    (40.11, 52.82, "mine_group"),
    (52.82, 59.80, "water"),
    (59.80, 76.75, "dry"),
    (76.75, 94.00, "clan"),
    (94.00, 112.73, "village"),
    (112.73, 124.00, "diamonds"),
    (124.00, 140.68, "triumph"),
    (140.68, 156.13, "village"),
    (156.13, 164.77, "diamonds"),
    (164.77, 179.328, "triumph"),
]
TEASER_SEGMENTS = [
    (TEASER_START, 116.14, "walk"),
    (116.14, 119.60, "mine"),
    (119.60, 124.00, "water"),
    (124.00, 130.00, "village"),
    (130.00, TEASER_END, "triumph"),
]


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def parse_lrc() -> list[dict]:
    """Parse the Latin-1 LRC and repair the one source typo in cSurs."""
    raw = LRC.read_bytes().decode("latin1")
    rows: list[dict] = []
    rx = re.compile(r"^\[(\d+):(\d+(?:\.\d+)?)\](.*)$")
    for line in raw.splitlines():
        match = rx.match(line.strip())
        if not match:
            continue
        minute = int(match.group(1))
        second = float(match.group(2))
        text = match.group(3).strip()
        # The file is mostly ISO-8859-1, but this word was typed as ASCII S.
        text = text.replace("cSurs", "cœurs")
        rows.append({"start": minute * 60 + second, "text": text})
    rows.sort(key=lambda row: row["start"])
    for index, row in enumerate(rows):
        row["end"] = rows[index + 1]["start"] if index + 1 < len(rows) else AUDIO_DURATION
    return rows


def wrap_lines(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        box = font.getbbox(candidate, stroke_width=0)
        if box[2] - box[0] <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_lyric(text: str, max_width: int = 930) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    for size in (60, 56, 52, 48, 44, 40):
        font = load_font(FONT_BOLD, size)
        lines = wrap_lines(text, font, max_width)
        if len(lines) <= 2 and all(font.getbbox(line)[2] - font.getbbox(line)[0] <= max_width for line in lines):
            return font, lines
    font = load_font(FONT_BOLD, 38)
    return font, wrap_lines(text, font, max_width)


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, stroke: int = 0) -> int:
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    return box[2] - box[0]


def centered_text(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str,
                  font: ImageFont.FreeTypeFont, fill, stroke_fill=None, stroke_width=0,
                  anchor="mm") -> None:
    draw.text(xy, text, font=font, fill=fill, anchor=anchor,
              stroke_width=stroke_width, stroke_fill=stroke_fill)


def cover_badge(draw: ImageDraw.ImageDraw) -> None:
    font = load_font(FONT_BOLD, 32)
    label = "DSKY✓"
    box = draw.textbbox((0, 0), label, font=font, stroke_width=0)
    bw = box[2] - box[0] + 38
    bh = box[3] - box[1] + 22
    x0 = (W - bw) // 2
    y0 = 34
    draw.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), radius=bh // 2,
                           fill=(5, 6, 10, 205), outline=(77, 210, 255, 230), width=2)
    centered_text(draw, (W / 2, y0 + bh / 2 - 1), label, font,
                  fill=(245, 249, 255, 255), stroke_fill=(5, 6, 10, 255), stroke_width=1)


def make_cover(source: Path, output: Path) -> None:
    base = ImageOps.fit(Image.open(source).convert("RGB"), (W, H), method=Image.Resampling.LANCZOS)
    canvas = base.convert("RGBA")
    veil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(veil, "RGBA")
    # A soft top veil keeps exact cover text readable without flattening the art.
    for y in range(0, 480, 4):
        alpha = int(210 * (1 - y / 520))
        vd.rectangle((0, y, W, y + 4), fill=(3, 7, 16, max(0, alpha)))
    for y in range(1530, H, 4):
        alpha = int(165 * ((y - 1530) / (H - 1530)))
        vd.rectangle((0, y, W, y + 4), fill=(3, 7, 16, max(0, alpha)))
    canvas = Image.alpha_composite(canvas, veil)
    draw = ImageDraw.Draw(canvas, "RGBA")
    cover_badge(draw)
    title_font = load_font(FONT_SERIF_BOLD, 88)
    artist_font = load_font(FONT_BOLD, 36)
    small_font = load_font(FONT_BOLD, 26)
    centered_text(draw, (W / 2, 175), "TOKO LONGA", title_font,
                  fill=(255, 222, 142, 255), stroke_fill=(5, 6, 10, 230), stroke_width=4)
    centered_text(draw, (W / 2, 278), "Nass'M Rodyboy", artist_font,
                  fill=(245, 249, 255, 255), stroke_fill=(5, 6, 10, 230), stroke_width=2)
    centered_text(draw, (W / 2, H - 130), "LYRIC VISUAL  ·  TECHSTEIN / DSKY PROD", small_font,
                  fill=(245, 249, 255, 245), stroke_fill=(5, 6, 10, 220), stroke_width=2)
    centered_text(draw, (W / 2, H - 82), "BÉNIN × CONGO", small_font,
                  fill=(77, 210, 255, 245), stroke_fill=(5, 6, 10, 220), stroke_width=2)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, quality=92, optimize=True, progressive=True)


def make_bottom_gradient() -> Image.Image:
    gradient = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gradient, "RGBA")
    start = H - 620
    for y in range(start, H, 4):
        ratio = (y - start) / (H - start)
        gd.rectangle((0, y, W, y + 4), fill=(0, 0, 0, int(170 * ratio)))
    return gradient


BOTTOM_GRADIENT = make_bottom_gradient()


def prepare_plate(path: Path) -> Image.Image:
    if not path.exists():
        raise FileNotFoundError(f"Missing image plate: {path}")
    # 1.10x canvas gives Ken Burns room while preserving the 9:16 frame.
    return ImageOps.fit(Image.open(path).convert("RGB"), (int(W * 1.10), int(H * 1.10)),
                        method=Image.Resampling.LANCZOS)


PLATES = {name: prepare_plate(path) for name, path in PLATE_PATHS.items()}
# Small precomputed grain tiles add a restrained 35 mm texture and prevent a
# long still-looking hold from being encoded as a frozen frame. The tiles are
# local procedural texture, not generated image assets.
NOISE_TILES = [Image.effect_noise((135, 240), 128).convert("L") for _ in range(12)]


def plate_frame(name: str, t: float, phase: float = 0.0) -> Image.Image:
    source = PLATES[name]
    extra_x = source.width - W
    extra_y = source.height - H
    # Slow, continuous movement: no held static frame.
    x = int(extra_x * (0.50 + 0.40 * math.sin(t * 0.115 + phase)))
    y = int(extra_y * (0.50 + 0.40 * math.sin(t * 0.083 + phase * 1.37)))
    return source.crop((x, y, x + W, y + H))


def segment_name(t: float, segments: list[tuple[float, float, str]]) -> tuple[int, str]:
    for index, (start, end, name) in enumerate(segments):
        if start <= t < end:
            return index, name
    return len(segments) - 1, segments[-1][2]


def background_at(t: float, segments: list[tuple[float, float, str]]) -> Image.Image:
    index, name = segment_name(t, segments)
    current = plate_frame(name, t, index * 0.91)
    # Short crossfade at every narrative boundary avoids a hard black or a
    # visually jarring discontinuity while keeping one continuous frame stream.
    for boundary_index in (index, index + 1):
        if not (0 < boundary_index < len(segments)):
            continue
        boundary = segments[boundary_index][0]
        distance = t - boundary
        if abs(distance) < 0.24:
            if distance < 0:
                next_name = segments[boundary_index][2]
                other = plate_frame(next_name, t, boundary_index * 0.91)
                ratio = (distance + 0.24) / 0.24
                return Image.blend(current, other, max(0.0, min(1.0, ratio)))
            prev_name = segments[boundary_index - 1][2]
            other = plate_frame(prev_name, t, (boundary_index - 1) * 0.91)
            ratio = distance / 0.24
            return Image.blend(other, current, max(0.0, min(1.0, ratio)))
    return current


def draw_heart(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: int, color) -> None:
    r = scale // 2
    draw.ellipse((cx - r, cy - r // 2, cx, cy + r // 2), fill=color)
    draw.ellipse((cx, cy - r // 2, cx + r, cy + r // 2), fill=color)
    draw.polygon([(cx - r, cy), (cx + r, cy), (cx, cy + scale)], fill=color)


def draw_comment(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: int, color) -> None:
    w = scale + 8
    h = int(scale * 0.72)
    x0, y0 = cx - w // 2, cy - h // 2
    draw.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=scale // 5,
                           outline=color, width=max(3, scale // 8))
    draw.polygon([(x0 + scale // 4, y0 + h - 2), (x0 + scale // 4 - 2, y0 + h + scale // 5),
                  (x0 + scale // 2, y0 + h - 2)], fill=color)


def draw_subscribe(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: int, color) -> None:
    r = scale // 2
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=max(3, scale // 9))
    draw.polygon([(cx - scale // 5, cy - scale // 7), (cx - scale // 5, cy + scale // 7),
                  (cx + scale // 6, cy)], fill=color)
    draw.line((cx + scale // 3, cy - scale // 2, cx + scale // 3, cy - scale // 5), fill=color, width=3)
    draw.line((cx + scale // 3 - scale // 7, cy - scale // 5 - scale // 7,
               cx + scale // 3 + scale // 7, cy - scale // 5 - scale // 7), fill=color, width=3)


def draw_cta(draw: ImageDraw.ImageDraw) -> None:
    # Fixed-position CTA for the first two seconds, with no movement or wobble.
    panel_w, panel_h = 360, 92
    x0, y0 = (W - panel_w) // 2, 132
    draw.rounded_rectangle((x0, y0, x0 + panel_w, y0 + panel_h), radius=30,
                           fill=(5, 6, 10, 185), outline=(77, 210, 255, 190), width=2)
    centers = [x0 + 78, x0 + panel_w // 2, x0 + panel_w - 78]
    draw_heart(draw, centers[0], y0 + panel_h // 2, 34, (255, 90, 105, 255))
    draw_subscribe(draw, centers[1], y0 + panel_h // 2, 36, (255, 222, 142, 255))
    draw_comment(draw, centers[2], y0 + panel_h // 2, 38, (77, 210, 255, 255))


def draw_share(draw: ImageDraw.ImageDraw, alpha: int = 235) -> None:
    # A compact, high-contrast share network shown at the temporal midpoint.
    cx, cy = W - 124, 260
    color = (77, 210, 255, alpha)
    amber = (255, 222, 142, alpha)
    draw.ellipse((cx - 65, cy - 65, cx + 65, cy + 65), outline=(77, 210, 255, min(130, alpha)), width=3)
    a = (cx - 25, cy + 19)
    b = (cx + 26, cy - 26)
    c = (cx + 29, cy + 38)
    draw.line((a[0], a[1], b[0], b[1]), fill=color, width=7)
    draw.line((a[0], a[1], c[0], c[1]), fill=amber, width=7)
    for px, py, fill in ((a[0], a[1], amber), (b[0], b[1], color), (c[0], c[1], color)):
        draw.ellipse((px - 16, py - 16, px + 16, py + 16), fill=(5, 6, 10, 230), outline=fill, width=5)


def line_for_time(lyrics: list[dict], global_t: float) -> dict | None:
    lookup_t = global_t + ADVANCE
    for row in lyrics:
        if row["start"] <= lookup_t < row["end"]:
            return row
    return None


def draw_lyrics(draw: ImageDraw.ImageDraw, row: dict | None) -> None:
    if not row or not row["text"]:
        return
    font, lines = fit_lyric(row["text"])
    line_gap = 12
    heights = [font.getbbox(line, stroke_width=2)[3] - font.getbbox(line, stroke_width=2)[1] for line in lines]
    total_h = sum(heights) + line_gap * max(0, len(lines) - 1)
    top = H - 318 - total_h
    pad_x, pad_y = 28, 20
    max_line_w = max(text_width(draw, line, font, 2) for line in lines)
    draw.rounded_rectangle((W // 2 - max_line_w // 2 - pad_x, top - pad_y,
                            W // 2 + max_line_w // 2 + pad_x, top + total_h + pad_y),
                           radius=22, fill=(3, 7, 16, 128))
    lower = row["text"].lower()
    is_hook = any(key in lower for key in ("toko", "longa", "réuss", "réussi", "triomphe", "courageux"))
    fill = (255, 222, 142, 255) if is_hook else (245, 249, 255, 255)
    y = top
    for index, line in enumerate(lines):
        centered_text(draw, (W / 2, y + heights[index] / 2), line, font, fill=fill,
                      stroke_fill=(3, 7, 16, 255), stroke_width=3)
        y += heights[index] + line_gap


def draw_intro(draw: ImageDraw.ImageDraw, local_t: float) -> None:
    if local_t > 5.5:
        return
    title = load_font(FONT_SERIF_BOLD, 72)
    sub = load_font(FONT_BOLD, 28)
    centered_text(draw, (W / 2, 520), "TOKO LONGA", title,
                  fill=(255, 222, 142, 235), stroke_fill=(3, 7, 16, 230), stroke_width=4)
    centered_text(draw, (W / 2, 610), "Nass'M Rodyboy", sub,
                  fill=(245, 249, 255, 235), stroke_fill=(3, 7, 16, 230), stroke_width=2)
    centered_text(draw, (W / 2, 664), "LYRIC VISUAL · TECHSTEIN / DSKY PROD", load_font(FONT_BOLD, 20),
                  fill=(77, 210, 255, 230), stroke_fill=(3, 7, 16, 220), stroke_width=1)


def render_frame(global_t: float, local_t: float, mode: str, lyrics: list[dict]) -> Image.Image:
    segments = TEASER_SEGMENTS if mode == "teaser" else FULL_SEGMENTS
    canvas = background_at(global_t, segments).convert("RGBA")
    canvas = Image.alpha_composite(canvas, BOTTOM_GRADIENT)
    # A barely perceptible 0.9 Hz luminance pulse keeps every frame alive in
    # addition to the Ken Burns crop. It is applied before the post overlays,
    # so DSKY✓ and the CTA remain mathematically static and readable.
    pulse = (1.0
             + 0.012 * math.sin(local_t * 2.0 * math.pi * 0.9)
             + 0.006 * math.sin(local_t * 2.0 * math.pi * 2.37)
             + 0.004 * math.sin(local_t * 2.0 * math.pi * 7.31)
             + 0.003 * math.sin(local_t * 2.0 * math.pi * 11.13))
    canvas = ImageEnhance.Brightness(canvas).enhance(pulse)
    tile = NOISE_TILES[int(local_t * FPS) % len(NOISE_TILES)]
    tile = ImageChops.offset(tile, int(local_t * FPS * 7) % tile.width,
                             int(local_t * FPS * 5) % tile.height)
    grain = tile.resize((W, H), Image.Resampling.BILINEAR)
    grain_rgb = Image.merge("RGB", (grain, grain, grain))
    canvas = Image.blend(canvas.convert("RGB"), grain_rgb, 0.018).convert("RGBA")
    draw = ImageDraw.Draw(canvas, "RGBA")
    cover_badge(draw)
    draw_intro(draw, local_t if mode == "lyrics" else 99.0)
    draw_lyrics(draw, line_for_time(lyrics, global_t))
    if local_t < 2.0:
        draw_cta(draw)
    midpoint = (TEASER_DURATION if mode == "teaser" else AUDIO_DURATION) / 2
    if abs(local_t - midpoint) <= 1.65:
        draw_share(draw)
    return canvas.convert("RGB")


def render_video(output: Path, duration: float, audio_start: float, mode: str, lyrics: list[dict]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    fade_start = max(0.0, duration - 1.4)
    command = [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo", "-pix_fmt", "rgb24",
        "-s:v", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-ss", f"{audio_start:.3f}", "-t", f"{duration:.3f}", "-i", str(AUDIO),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-af", f"afade=t=in:st=0:d=0.18,afade=t=out:st={fade_start:.3f}:d=1.35",
        "-t", f"{duration:.3f}", "-movflags", "+faststart", "-shortest", str(output),
    ]
    print(f"Rendering {mode}: {output.name} ({duration:.3f}s, {math.ceil(duration * FPS)} frames)", flush=True)
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    assert process.stdin is not None
    try:
        for frame_number in range(math.ceil(duration * FPS)):
            local_t = frame_number / FPS
            global_t = audio_start + local_t
            frame = render_frame(global_t, local_t, mode, lyrics)
            process.stdin.write(frame.tobytes())
        process.stdin.close()
    except Exception:
        process.kill()
        process.wait()
        raise
    return_code = process.wait()
    if return_code != 0:
        error = (process.stderr.read() if process.stderr else b"").decode("utf-8", "replace")
        raise RuntimeError(f"ffmpeg failed for {output}: {error[-4000:]}")


def clean_lyrics_text(lyrics: list[dict]) -> str:
    return "\n".join(row["text"] for row in lyrics if row["text"])


def build_master_mp3(output: Path, cover: Path, lyrics: list[dict]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    temp = output.with_suffix(".tmp.mp3")
    command = [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(AUDIO),
        "-af", "highpass=f=30,lowpass=f=18000,loudnorm=I=-14:TP=-1.8:LRA=11:linear=true",
        "-ar", "48000", "-ac", "2", "-c:a", "libmp3lame", "-b:a", "320k", "-map_metadata", "-1",
        str(temp),
    ]
    print(f"Mastering MP3: {output.name}", flush=True)
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", "replace")[-4000:])
    temp.replace(output)

    tags = ID3()
    tags.add(TIT2(encoding=3, text="Toko Longa"))
    tags.add(TPE1(encoding=3, text="Nass'M Rodyboy"))
    tags.add(TALB(encoding=3, text="Toko Longa"))
    tags.add(TPE2(encoding=3, text="Techstein / DSKY Prod"))
    tags.add(TCON(encoding=3, text="Afro / World / Rap"))
    tags.add(TDRC(encoding=3, text="2026"))
    tags.add(TXXX(encoding=3, desc="producer", text="Techstein"))
    tags.add(TXXX(encoding=3, desc="label", text="DSKY Prod"))
    tags.add(TXXX(encoding=3, desc="realisation", text="Techstein / DSKY Prod"))
    tags.add(TXXX(encoding=3, desc="contact", text="Tel: 2290161162408 / 2290149114951"))
    tags.add(TXXX(encoding=3, desc="email", text="daiskypro@proton.me; daiskyproduction@gmail.com; techsteinsecureway@gmail.com"))
    tags.add(USLT(encoding=3, lang="fra", desc="Lyrics", text=clean_lyrics_text(lyrics)))
    tags.add(COMM(encoding=3, lang="fra", desc="Production", text="Lyric visual réalisé par Techstein / DSKY Prod"))
    tags.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=cover.read_bytes()))
    tags.save(output, v2_version=3)


def write_manifest(lyrics: list[dict]) -> None:
    manifest = {
        "title": "Toko Longa",
        "artist": "Nass'M Rodyboy",
        "realization": "Techstein / DSKY Prod",
        "audio_duration_seconds": AUDIO_DURATION,
        "fps": FPS,
        "resolution": [W, H],
        "badge": "DSKY✓",
        "teaser": {
            "audio_start": TEASER_START,
            "audio_end": TEASER_END,
            "duration": round(TEASER_DURATION, 3),
            "image_count": 5,
            "images": [str((RAW_TEASER / name).relative_to(ROOT)) for name in (
                "01_pas_de_pluie.png", "02_creuse_la_nuit.png", "03_goutte_lingot.png",
                "04_clan_soude.png", "05_triomphe.png")],
        },
        "lyrics_count": len(lyrics),
        "lyric_source": "assets/lyrics/Toko_Longa_clean.lrc",
    }
    (OUT / "Toko_Longa_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--covers", action="store_true")
    parser.add_argument("--teaser", action="store_true")
    parser.add_argument("--lyrics", action="store_true")
    parser.add_argument("--mp3", action="store_true")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    if not any((args.covers, args.teaser, args.lyrics, args.mp3, args.all)):
        args.all = True

    global AUDIO_DURATION
    AUDIO_DURATION = float(MP3(AUDIO).info.length)
    lyrics = parse_lrc()
    OUT.mkdir(parents=True, exist_ok=True)

    cover_sources = [
        (RAW_COVERS / "toko_longa_cover_01_terre.png", OUT / "cover_toko_longa_01_terre_9x16.jpg"),
        (RAW_COVERS / "toko_longa_cover_02_lampe.png", OUT / "cover_toko_longa_02_lampe_9x16.jpg"),
        (RAW_COVERS / "toko_longa_cover_03_clan.png", OUT / "cover_toko_longa_03_clan_9x16.jpg"),
    ]
    if args.covers or args.all:
        for source, target in cover_sources:
            make_cover(source, target)

    chosen_cover = OUT / "cover_toko_longa_01_terre_9x16.jpg"
    if args.teaser or args.all:
        render_video(OUT / "Toko_Longa_teaser_9x16_v1.mp4", TEASER_DURATION, TEASER_START, "teaser", lyrics)
    if args.lyrics or args.all:
        render_video(OUT / "Toko_Longa_lyrics_9x16_v1.mp4", AUDIO_DURATION, 0.0, "lyrics", lyrics)
    if args.mp3 or args.all:
        if not chosen_cover.exists():
            make_cover(cover_sources[0][0], chosen_cover)
        build_master_mp3(OUT / "Toko_Longa_master.mp3", chosen_cover, lyrics)
    write_manifest(lyrics)
    print("Done.", flush=True)


if __name__ == "__main__":
    main()
