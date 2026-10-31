#!/usr/bin/env python3
"""Montage PEINT 9:16. Source timestamps stay unchanged; visual validation is still needed.

Requires: Pillow, imageio-ffmpeg, the fonts in fonts/, the verse map, and the audio
created by create_audio_derivative.py. A short non-deliverable test can be made with
--start 5 --duration 12 --output work/test.mp4.
"""
from __future__ import annotations

import argparse
import bisect
from functools import lru_cache
import json
import math
import os
import subprocess
import time
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

PROJECT = Path(__file__).resolve().parent
ASSETS = PROJECT / "fonds"
MAP = PROJECT / "verses_map.json"
AUDIO = PROJECT / "livrables/Je_me_releve_toujours_Dsky.mp3"
OUT = PROJECT / "livrables/Je_me_releve_toujours_9x16.mp4"
WORK = PROJECT / "work"
WIDTH, HEIGHT, FPS = 1080, 1920, 30
# Counted from the decoded 48 kHz, stereo PCM stream (44,144,636 bytes of s16le).
AUDIO_SAMPLES = 11_036_159
AUDIO_DURATION = AUDIO_SAMPLES / 48_000
INTRO_END = 5.03
FINAL_CARD_S = 5.0
VIDEO_END = AUDIO_DURATION + FINAL_CARD_S
N_FRAMES = round(VIDEO_END * FPS)
CTA_START, CTA_END = 208.0, 212.5  # conservative late window in the 200.80–225.02 source gap

SERIF = str(PROJECT / "fonts/DejaVuSerif-Bold.ttf")
MONTSERRAT = str(PROJECT / "fonts/Montserrat-variable.ttf")
CREAM = (249, 239, 221)
GOLD = (229, 183, 104)
NAVY = (7, 15, 25)


@lru_cache(maxsize=80)
def font(path: str, size: int, weight: str = "Regular") -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(path, size)
    if path == MONTSERRAT:
        f.set_variation_by_name(weight)
    return f


def center_text(draw: ImageDraw.ImageDraw, text: str, y: int, fnt: ImageFont.FreeTypeFont,
                fill: tuple[int, int, int, int], stroke: int = 2,
                stroke_fill: tuple[int, int, int, int] = (3, 8, 14, 230)) -> None:
    box = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke)
    x = (WIDTH - (box[2] - box[0])) // 2 - box[0]
    draw.text((x, y), text, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def fit_font(text: str, path: str, max_size: int, max_width: int,
             min_size: int = 28, weight: str = "Regular") -> ImageFont.FreeTypeFont:
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for size in range(max_size, min_size - 1, -2):
        f = font(path, size, weight)
        box = d.textbbox((0, 0), text, font=f, stroke_width=2)
        if box[2] - box[0] <= max_width:
            return f
    raise ValueError(f"Text does not fit the safe area: {text!r}")


def card_background(image_name: str) -> Image.Image:
    source = Image.open(ASSETS / image_name).convert("RGB")
    # Only the upper, text-free 720 px are used; painted lyric fragments never leak into cards.
    crop = source.crop((0, 0, 768, 720))
    background = ImageOps.fit(crop, (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS)
    background = background.filter(ImageFilter.GaussianBlur(36))
    background = Image.blend(ImageEnhance.Brightness(background).enhance(0.32),
                             Image.new("RGB", (WIDTH, HEIGHT), NAVY), 0.52)
    portrait_height = round(720 * WIDTH / 768)
    portrait = crop.resize((WIDTH, portrait_height), Image.Resampling.LANCZOS)
    portrait = ImageEnhance.Brightness(portrait).enhance(0.82)
    mask = Image.new("L", portrait.size, 255)
    d = ImageDraw.Draw(mask)
    fade_start = portrait_height - 190
    for y in range(150):
        d.line((0, y, WIDTH, y), fill=round(255 * y / 150))
    for y in range(fade_start, portrait_height):
        d.line((0, y, WIDTH, y), fill=round(255 * (portrait_height - y - 1) / 190))
    background.paste(portrait, (0, 170), mask)
    return background.convert("RGBA")


def draw_wtbw_sticker(draw: ImageDraw.ImageDraw) -> None:
    # The only text in this hand-composited sticker is the explicit label WTBW.
    draw.ellipse((436, 171, 644, 259), fill=(12, 24, 30, 224),
                 outline=(244, 209, 154, 255), width=4)
    draw.ellipse((442, 177, 638, 253), outline=(202, 150, 76, 230), width=2)
    center_text(draw, "WTBW", 184, font(MONTSERRAT, 39, "ExtraBold"), (249, 224, 175, 255), 2)


def make_intro_card() -> Image.Image:
    card = card_background("scene-01-ancre.png")
    draw = ImageDraw.Draw(card)
    draw_wtbw_sticker(draw)
    # All card strings are explicit; no code, URL, contact, flag or other logo is used.
    title = "Je me relève toujours"
    center_text(draw, title, 1160, fit_font(title, SERIF, 67, 740, 40), (*CREAM, 255), 2)
    heading = "Regarde jusqu'à la fin"
    center_text(draw, heading, 1270,
                fit_font(heading, MONTSERRAT, 42, 740, 30, "ExtraBold"), (*CREAM, 255), 2)
    lines = ["pour découvrir comment proposer", "un son ou des lyrics à réaliser", "pour toi !"]
    for j, line in enumerate(lines):
        center_text(draw, line, 1340 + j * 50,
                    fit_font(line, MONTSERRAT, 31, 740, 25, "Medium"), (*CREAM, 255), 2)
    return card.convert("RGB")


def make_final_card() -> Image.Image:
    card = card_background("scene-43.png")
    draw = ImageDraw.Draw(card)
    draw_wtbw_sticker(draw)
    message = "Merci d'avoir regardé"
    center_text(draw, message, 1240, fit_font(message, SERIF, 63, 740, 40), (*CREAM, 255), 2)
    return card.convert("RGB")


def prepare_assets(rows: list[dict]) -> tuple[dict[str, Image.Image], Image.Image, Image.Image]:
    # Resize once. Subsequent frames slide a small crop: no per-frame scaling of painted letters.
    prep_size = (1145, 2035)
    cache: dict[str, Image.Image] = {}
    for rel in sorted({r["image"] for r in rows}):
        src = Image.open(PROJECT / rel).convert("RGB")
        cache[rel] = ImageOps.fit(src, prep_size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    dim = ImageEnhance.Brightness(cache["fonds/scene-06-aube.png"]).enhance(0.40)
    dim = dim.filter(ImageFilter.GaussianBlur(2))
    # A word-free crop of the same scene gives the long presumed instrumental
    # space a brighter, gently moving image without showing the next lyric early.
    instrumental = card_background("scene-06-aube.png").convert("RGB")
    instrumental = instrumental.resize(prep_size, Image.Resampling.LANCZOS)
    return cache, dim, instrumental


def camera_crop(image: Image.Image, row_i: int, u: float) -> Image.Image:
    max_x, max_y = image.width - WIDTH, image.height - HEIGHT
    paths = [((2, 34), (12, 82)), ((34, 2), (12, 82)),
             ((8, 40), (82, 16)), ((40, 8), (16, 82))]
    (x0, x1), (y0, y1) = paths[(row_i - 1) % len(paths)]
    x = int(max(0, min(max_x, x0 + (x1 - x0) * u)))
    y = int(max(0, min(max_y, y0 + (y1 - y0) * u)))
    return image.crop((x, y, x + WIDTH, y + HEIGHT))


def faded(layer: Image.Image, step: int) -> Image.Image:
    if step >= 10:
        return layer
    layer = layer.copy()
    layer.putalpha(layer.getchannel("A").point(lambda a: (a * step) // 10))
    return layer


@lru_cache(maxsize=32)
def badge_layer(label: str, step: int) -> Image.Image:
    layer = Image.new("RGBA", (270, 75), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = font(MONTSERRAT, 44, "ExtraBold")
    box = d.textbbox((0, 0), label, font=f, stroke_width=3)
    x = (270 - (box[2] - box[0])) // 2 - box[0]
    d.text((x, 4), label, font=f, fill=(249, 239, 220, 210),
           stroke_width=3, stroke_fill=(5, 11, 18, 205))
    return faded(layer, step)


def wrap_by_width(text: str, f: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = word if not current else current + " " + word
        if d.textbbox((0, 0), candidate, font=f, stroke_width=2)[2] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


@lru_cache(maxsize=32)
def translation_layer(text: str, step: int) -> Image.Image:
    # The original lyric remains painted; the sole overlay in the low band is its FR translation.
    layer = Image.new("RGBA", (740, 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = fit_font(text, MONTSERRAT, 35, 700, 25, "Bold")
    lines = wrap_by_width(text, f, 700)
    if len(lines) != 1:
        raise ValueError(f"Translation does not fit in the safe low band: {text!r}")
    d.rounded_rectangle((0, 5, 739, 70), radius=30, fill=(5, 11, 18, 155))
    box = d.textbbox((0, 0), text, font=f, stroke_width=2)
    x = (740 - (box[2] - box[0])) // 2 - box[0]
    d.text((x, 18), text, font=f, fill=(249, 239, 222, 255),
           stroke_width=2, stroke_fill=(4, 9, 15, 225))
    return faded(layer, step)


@lru_cache(maxsize=40)
def cta_layer(step: int, bell_angle: int) -> Image.Image:
    # Small, explicitly authored clochette + exact words; it never covers the tomato's face.
    layer = Image.new("RGBA", (740, 175), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f1, f2 = font(MONTSERRAT, 39, "ExtraBold"), font(MONTSERRAT, 33, "Bold")
    d.text((235, 24), "ABONNE-TOI", font=f1, fill=(249, 239, 221, 255),
           stroke_width=3, stroke_fill=(5, 11, 18, 240))
    d.text((235, 91), "PARTAGE", font=f2, fill=(229, 183, 104, 255),
           stroke_width=3, stroke_fill=(5, 11, 18, 240))
    bell = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
    b = ImageDraw.Draw(bell)
    b.ellipse((51, 12, 69, 31), fill=(238, 191, 107, 255), outline=(12, 19, 26, 230), width=3)
    b.pieslice((27, 24, 93, 100), 180, 360, fill=(239, 190, 97, 255),
               outline=(12, 19, 26, 230), width=3)
    b.polygon(((27, 62), (25, 83), (19, 91), (101, 91), (95, 83), (93, 62)),
              fill=(229, 178, 83, 255), outline=(12, 19, 26, 230), width=3)
    b.ellipse((49, 91, 71, 111), fill=(226, 169, 75, 255), outline=(12, 19, 26, 230), width=3)
    bell = bell.rotate(bell_angle, resample=Image.Resampling.BICUBIC)
    layer.alpha_composite(bell, (78, 28))
    return faded(layer, step)


def verse_frame(t: float, row: dict, assets: dict[str, Image.Image], dim_asset: Image.Image,
                instrumental_asset: Image.Image) -> Image.Image:
    start, end = float(row["t"]), float(row["fin"])
    span = max(0.001, end - start)
    u = max(0.0, min(1.0, (t - start) / span))
    frame = camera_crop(assets[row["image"]], row["i"], u)

    # Do not dim a sung line based solely on a reading-speed heuristic. Its known
    # start is exact, but the map gives no word-level or sung-end timestamp. The
    # exceptionally long final signature interval is the one provisional exception.
    dim_mix = 0.0
    if row["i"] == 57:
        disp = float(row["rendu_affichage_s"])
        dim_mix = min(1.0, max(0.0, (t - start - disp) / 0.35))
        if dim_mix > 0:
            frame = Image.blend(frame, camera_crop(dim_asset, row["i"], u), dim_mix)
        instrumental_start = start + disp + 0.35
        if t >= instrumental_start:
            travel = max(0.0, min(1.0, (t - instrumental_start) / (end - instrumental_start)))
            x = int(travel * (instrumental_asset.width - WIDTH))
            y = int(travel * (instrumental_asset.height - HEIGHT))
            instrumental = instrumental_asset.crop((x, y, x + WIDTH, y + HEIGHT))
            transition = min(1.0, (t - instrumental_start) / 0.45)
            frame = Image.blend(frame, instrumental, transition)

    label = "WTBW" if row["i"] % 2 == 1 else "DSKY"
    badge_in = min(1.0, max(0.0, (t - start) / 0.25))
    badge_out = min(1.0, max(0.0, (end - t) / 0.25))
    badge_step = round(10 * min(badge_in, badge_out) * (1.0 - dim_mix))
    if badge_step > 0:
        layer = badge_layer(label, badge_step)
        frame.paste(layer, (405, 155), layer)

    translation = row.get("traduction_fr") or ""
    if translation:
        elapsed = t - start
        opacity = min(1.0, max(0.0, elapsed / 0.18), max(0.0, (end - t) / 0.18))
        step = round(10 * opacity)
        if step > 0:
            layer = translation_layer(translation, step)
            frame.paste(layer, (170, 1470), layer)

    if CTA_START <= t < CTA_END and row["i"] == 57 and dim_mix >= 1.0:
        opacity = min(1.0, (t - CTA_START) / 0.35, (CTA_END - t) / 0.35)
        step = max(0, min(10, round(10 * opacity)))
        angle = round(10 * math.sin(2 * math.pi * (t - CTA_START) / 1.2))
        if step > 0:
            layer = cta_layer(step, angle)
            frame.paste(layer, (170, 1350), layer)
    return frame


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--start", type=float, default=0.0, help="global start (test renders only)")
    p.add_argument("--duration", type=float, default=None, help="duration in seconds (test renders only)")
    p.add_argument("--output", type=Path, default=OUT)
    p.add_argument("--crf", type=int, default=25)
    args = p.parse_args()
    if args.start < 0 or args.start >= VIDEO_END:
        p.error("--start must be inside the video")
    if args.duration is not None and args.duration <= 0:
        p.error("--duration must be positive")
    if (args.start != 0 or args.duration is not None) and args.output == OUT:
        p.error("short renders require a separate --output")
    return args


def main() -> None:
    args = parse_args()
    if not AUDIO.exists():
        raise SystemExit(f"Missing normalized audio: {AUDIO}")
    rows = json.loads(MAP.read_text(encoding="utf-8"))
    if len(rows) != 58 or any(not r["disponible"] or not (PROJECT / r["image"]).exists() for r in rows):
        raise SystemExit("Verse map must contain 58 rows with all artwork available")
    starts = [float(r["t"]) for r in rows]
    assets, dim_asset, instrumental_asset = prepare_assets(rows)
    intro, final = make_intro_card(), make_final_card()
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    WORK.mkdir(parents=True, exist_ok=True)
    output = args.output if args.output.is_absolute() else PROJECT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_name(output.stem + ".part.mp4")
    log_path = WORK / (output.stem + "-ffmpeg.log")
    if temp.exists():
        temp.unlink()
    duration = min(args.duration if args.duration is not None else VIDEO_END - args.start,
                   VIDEO_END - args.start)
    n_frames = round(duration * FPS)
    if args.start == 0 and args.duration is None:
        n_frames = N_FRAMES
    cmd = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "warning",
        "-f", "rawvideo", "-vcodec", "rawvideo", "-pix_fmt", "rgb24",
        "-s:v", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "pipe:0",
        "-ss", f"{args.start:.6f}", "-i", str(AUDIO), "-map", "0:v:0", "-map", "1:a:0",
        "-vf", "format=yuv420p",
    ]
    if args.start == 0 and args.duration is None:
        cmd += ["-af", f"afade=t=in:st=0:d=0.30,afade=t=out:st={AUDIO_DURATION-3:.6f}:d=3,apad=pad_dur={FINAL_CARD_S+0.1:.3f}"]
    else:
        cmd += ["-af", "apad=pad_dur=5.1"]
    cmd += [
        "-frames:v", str(n_frames), "-t", f"{n_frames / FPS:.6f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", str(args.crf), "-threads", "4",
        "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-metadata", "title=Je me relève toujours", "-metadata", "artist=Dsky",
        "-metadata", "comment=Visuels générés par IA; audio généré avec Suno; master source préservé",
        "-movflags", "+faststart", str(temp),
    ]
    with log_path.open("wb") as log:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=log)
        assert proc.stdin is not None
        try:
            t0 = time.time()
            for frame_n in range(n_frames):
                t = args.start + frame_n / FPS
                if t < INTRO_END:
                    frame = intro
                elif t >= AUDIO_DURATION:
                    frame = final
                else:
                    idx = max(0, min(bisect.bisect_right(starts, t) - 1, len(rows) - 1))
                    frame = verse_frame(t, rows[idx], assets, dim_asset, instrumental_asset)
                proc.stdin.write(frame.tobytes())
                if (frame_n + 1) % 300 == 0:
                    elapsed = time.time() - t0
                    print(f"Frames {frame_n+1}/{n_frames} ({(frame_n+1)/n_frames:.1%}); {elapsed:.1f}s", flush=True)
            proc.stdin.close()
        except BrokenPipeError:
            proc.stdin.close()
            rc = proc.wait()
            raise RuntimeError(f"ffmpeg closed its rawvideo pipe (exit {rc}); inspect {log_path}")
        rc = proc.wait()
        if rc:
            raise RuntimeError(f"ffmpeg failed with exit {rc}; inspect {log_path}")
    os.replace(temp, output)
    print(f"Rendered {output} ({output.stat().st_size} bytes); {n_frames} frames at {FPS} fps = {n_frames/FPS:.3f}s")


if __name__ == "__main__":
    main()
