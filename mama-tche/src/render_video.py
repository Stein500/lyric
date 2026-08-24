from __future__ import annotations

import json
import math
import re
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

import imageio_ffmpeg
import numpy as np
from mutagen.mp3 import MP3
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import subprocess

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "mama-tche"
RAW_ROOT = PROJECT / "assets" / "raw" / "9x16"
OUT_DIR = PROJECT / "livrables"
SRC_DIR = PROJECT / "src"
LYRICS_MD = ROOT / "mama-tche-paroles-traduites.md"
AUDIO = ROOT / "Mama_tche_Daïsky.mp3"

WIDTH = 1080
HEIGHT = 1920
FPS = 30
VIDEO_DURATION = round(MP3(AUDIO).info.length, 3)
TRANSITION = 0.8
TRANSITION_HALF = TRANSITION / 2
SAFE_SUB_MARGIN = 330

FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

TITLE = "Mama tché"
ARTIST = "Daïsky"
PROD = "Daïsky Prod"
STUDIO = "TechStein"
TAGLINE = "Wolof TechStein beat wê !"
LINK = "https://linktr.ee/daiskypro"
CONTACT = "+229 01 61 16 24 08 / 01 49 11 49 51"
EMAILS = "techsteinsecureway@gmail.com / daiskyproduction@gmail.com"

PALETTE = {
    "forest": "#145A3B",
    "emerald": "#1FAF73",
    "gold": "#F4C95D",
    "magenta": "#E85FA6",
    "ivory": "#F8F2E7",
    "deep": "#08150F",
}


@dataclass
class Segment:
    id: str
    image: Path
    start: float
    end: float
    ken_burns: str
    pan: str


@dataclass
class SubtitleEvent:
    start: float
    end: float
    text: str
    style: str
    section: str


def ts_to_seconds(ts: str) -> float:
    ts = re.sub(r"\s+", "", ts)
    m, s = ts.split(":", 1)
    return int(m) * 60 + float(s)


def ass_time(sec: float) -> str:
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - math.floor(sec)) * 100))
    if cs == 100:
        s += 1
        cs = 0
    if s == 60:
        m += 1
        s = 0
    if m == 60:
        h += 1
        m = 0
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def wrap_subtitle(text: str, width: int = 28) -> str:
    lines = textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False)
    if len(lines) <= 2:
        return "\\N".join(lines)
    first = " ".join(lines[: len(lines)//2])
    second = " ".join(lines[len(lines)//2 :])
    return f"{first}\\N{second}"


def clean_lyric_text(raw: str) -> str:
    raw = raw.strip().strip("`")
    # Keep only the lyrical part before the first timing marker.
    m = re.search(r"\d+\s*:\s*\d+(?:\.\d+)?", raw)
    if m:
        raw = raw[: m.start()].strip()
    raw = re.sub(r"\s*[-–—]+\s*$", "", raw).strip()
    # Remove translation in parentheses when the line has content before it.
    raw = re.sub(r"\s*\([^)]*\)\s*$", "", raw).strip()
    raw = re.sub(r"\s+", " ", raw)
    raw = re.sub(r"\s*[-–—]+\s*$", "", raw).strip()
    return raw


def subtitle_style_for(start: float) -> Tuple[str, str]:
    if start < 14:
        return ("HookGold" if start < 4 else "IntroSerif", "intro")
    if start < 58:
        return ("VerseMono", "verse1")
    if start < 90:
        return ("RefrainGold", "refrain1")
    if start < 131:
        return ("VerseSans", "verse2")
    if start < 162:
        return ("RefrainGold", "refrain2")
    if start < 185:
        return ("BridgeSerifCenter", "bridge")
    if start < 229:
        return ("FinalRefrainGold", "final_refrain")
    return ("OutroSerif", "outro")


def parse_lyrics() -> List[SubtitleEvent]:
    text = LYRICS_MD.read_text(encoding="utf-8")
    code = re.search(r"```(.*?)```", text, re.S)
    lines = [ln.strip() for ln in code.group(1).splitlines()] if code else []

    events: List[SubtitleEvent] = [
        SubtitleEvent(0.00, 3.80, "Wolof TechStein beat wê!", "HookGold", "intro"),
        SubtitleEvent(4.20, 13.60, 'Non vivi o - o nvi gboon mavomavo.', "IntroSerif", "intro"),
    ]

    parsed: List[Tuple[float, Optional[float], str]] = []
    time_pattern = re.compile(r"\d+\s*:\s*\d+(?:\.\d+)?")
    for ln in lines:
        if not ln or ln.startswith("Wolof TechStein beat wê!") or "nvi gboon mavomavo" in ln:
            continue
        matches = time_pattern.findall(ln)
        if not matches:
            continue
        starts = [ts_to_seconds(m) for m in matches]
        start = starts[0]
        explicit_end = starts[1] if len(starts) > 1 else None
        cleaned = clean_lyric_text(ln)
        if not cleaned:
            continue
        parsed.append((start, explicit_end, cleaned))

    parsed.sort(key=lambda x: x[0])

    # Manually insert the repeated untimed tag before the outro section.
    parsed.append((219.40, None, "Wolof TechStein beat wê!"))
    parsed.sort(key=lambda x: x[0])

    for idx, (start, explicit_end, txt) in enumerate(parsed):
        if explicit_end is not None and explicit_end > start:
            end = explicit_end
        else:
            next_start = parsed[idx + 1][0] if idx + 1 < len(parsed) else VIDEO_DURATION
            end = next_start
        style, section = subtitle_style_for(start)
        events.append(SubtitleEvent(start, max(start + 0.8, end), txt, style, section))

    # Add the final quote with exact last timing if not covered till the end.
    events = sorted(events, key=lambda e: e.start)
    trimmed: List[SubtitleEvent] = []
    for i, ev in enumerate(events):
        if i + 1 < len(events):
            hard_end = min(ev.end, events[i + 1].start)
        else:
            hard_end = ev.end
        trimmed.append(SubtitleEvent(ev.start, hard_end, wrap_subtitle(ev.text), ev.style, ev.section))

    # Ensure final subtitle reaches the song end cleanly.
    if trimmed:
        last = trimmed[-1]
        if last.end < VIDEO_DURATION:
            trimmed[-1] = SubtitleEvent(last.start, VIDEO_DURATION, last.text, last.style, last.section)

    return trimmed


def build_segments() -> List[Segment]:
    session_paths = []
    for folder in [RAW_ROOT / "session01", RAW_ROOT / "session02", RAW_ROOT / "session03"]:
        session_paths.extend(sorted(folder.glob("*.png")))
    assert len(session_paths) == 30, f"Expected 30 images, found {len(session_paths)}"

    boundaries = [
        0.0,
        14.0,
        23.9,
        31.0,
        41.9,
        52.0,
        58.0,
        65.0,
        72.0,
        80.0,
        90.0,
        97.0,
        104.0,
        111.0,
        118.0,
        125.0,
        131.0,
        138.0,
        145.0,
        153.8,
        162.0,
        167.0,
        174.0,
        181.0,
        189.0,
        195.9,
        203.0,
        210.0,
        216.0,
        229.0,
        240.0,
    ]
    pans = ["center", "up", "down", "left", "right", "center", "up", "right", "left", "down"]
    segments: List[Segment] = []
    for i in range(30):
        segments.append(
            Segment(
                id=f"S{i+1:02d}",
                image=session_paths[i],
                start=boundaries[i],
                end=boundaries[i + 1],
                ken_burns="in" if i % 2 == 0 else "out",
                pan=pans[i % len(pans)],
            )
        )
    return segments


def build_manifest(segments: List[Segment], subtitles: List[SubtitleEvent]) -> dict:
    return {
        "title": TITLE,
        "artist": ARTIST,
        "audio": AUDIO.name,
        "duration": VIDEO_DURATION,
        "segments": [
            {
                "id": seg.id,
                "image": str(seg.image.relative_to(PROJECT)),
                "debut": round(seg.start, 3),
                "fin": round(seg.end, 3),
                "ken_burns": seg.ken_burns,
                "pan": seg.pan,
            }
            for seg in segments
        ],
        "paroles": [
            {
                "debut": round(ev.start, 3),
                "fin": round(ev.end, 3),
                "texte": ev.text.replace("\\N", " "),
                "style": ev.style,
                "section": ev.section,
            }
            for ev in subtitles
        ],
    }


def write_ass(subtitles: List[SubtitleEvent], dest: Path) -> None:
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {WIDTH}
PlayResY: {HEIGHT}
ScaledBorderAndShadow: yes
WrapStyle: 2
YCbCr Matrix: TV.601

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: IntroSerif,DejaVu Serif,50,&H00F8F2E7,&H000000FF,&H002A714C,&H55000000,1,0,0,0,100,100,0,0,1,3.2,1.2,2,120,120,360,1
Style: VerseMono,DejaVu Sans Mono,50,&H00F8F2E7,&H000000FF,&H002A714C,&H55000000,1,0,0,0,100,100,0.3,0,1,3.4,1.2,2,90,90,{SAFE_SUB_MARGIN},1
Style: VerseSans,DejaVu Sans,50,&H00F8F2E7,&H000000FF,&H002A714C,&H55000000,1,0,0,0,100,100,0.3,0,1,3.4,1.2,2,90,90,{SAFE_SUB_MARGIN},1
Style: RefrainGold,DejaVu Sans,58,&H00F4C95D,&H000000FF,&H00145A3B,&H66000000,1,0,0,0,100,100,0.5,0,1,3.8,1.4,2,88,88,{SAFE_SUB_MARGIN},1
Style: FinalRefrainGold,DejaVu Sans,62,&H00F4C95D,&H000000FF,&H00145A3B,&H66000000,1,0,0,0,100,100,0.6,0,1,4.0,1.5,2,86,86,{SAFE_SUB_MARGIN},1
Style: BridgeSerifCenter,DejaVu Serif,54,&H00F8F2E7,&H000000FF,&H002A714C,&H66000000,1,0,0,0,100,100,0.2,0,1,3.6,1.2,5,110,110,0,1
Style: HookGold,DejaVu Sans,60,&H00F4C95D,&H000000FF,&H00145A3B,&H66000000,1,0,0,0,100,100,0.8,0,1,4.0,1.4,2,100,100,{SAFE_SUB_MARGIN},1
Style: OutroSerif,DejaVu Serif,50,&H00F8F2E7,&H000000FF,&H002A714C,&H66000000,1,0,0,0,100,100,0.2,0,1,3.6,1.2,2,100,100,{SAFE_SUB_MARGIN},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for ev in subtitles:
        text = ev.text.replace("{", "(").replace("}", ")")
        lines.append(
            f"Dialogue: 0,{ass_time(ev.start)},{ass_time(ev.end)},{ev.style},,0,0,0,,{{\\fad(140,140)}}{text}"
        )
    dest.write_text(ass + "\n".join(lines) + "\n", encoding="utf-8")


def load_images(segments: List[Segment]) -> dict[str, Image.Image]:
    return {seg.id: Image.open(seg.image).convert("RGB") for seg in segments}


def make_vertical_gradient(height: int, start_alpha: int = 0, end_alpha: int = 170) -> Image.Image:
    grad = Image.new("L", (1, height))
    data = []
    for y in range(height):
        alpha = int(start_alpha + (end_alpha - start_alpha) * (y / max(1, height - 1)))
        data.append(alpha)
    grad.putdata(data)
    alpha_img = grad.resize((WIDTH, height))
    overlay = Image.new("RGBA", (WIDTH, height), (0, 0, 0, 0))
    overlay.putalpha(alpha_img)
    return overlay


def rounded_rectangle(draw: ImageDraw.ImageDraw, box: Tuple[int, int, int, int], radius: int, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def fit_cover(img: Image.Image, scale: float, focus_x: float, focus_y: float) -> Image.Image:
    src_w, src_h = img.size
    base_scale = max(WIDTH / src_w, HEIGHT / src_h) * scale
    new_size = (max(WIDTH, int(src_w * base_scale)), max(HEIGHT, int(src_h * base_scale)))
    resized = img.resize(new_size, Image.Resampling.LANCZOS)
    max_x = max(0, resized.width - WIDTH)
    max_y = max(0, resized.height - HEIGHT)
    x = int(max_x * focus_x)
    y = int(max_y * focus_y)
    return resized.crop((x, y, x + WIDTH, y + HEIGHT))


def render_segment_frame(img: Image.Image, seg: Segment, t: float) -> Image.Image:
    dur = max(0.001, seg.end - seg.start)
    progress = min(1.0, max(0.0, (t - seg.start) / dur))
    if seg.ken_burns == "in":
        zoom = 1.00 + 0.05 * progress
    else:
        zoom = 1.05 - 0.05 * progress

    focus_map = {
        "center": ((0.50, 0.48), (0.52, 0.50)),
        "up": ((0.50, 0.32), (0.50, 0.48)),
        "down": ((0.50, 0.58), (0.50, 0.46)),
        "left": ((0.34, 0.50), (0.52, 0.50)),
        "right": ((0.66, 0.50), (0.48, 0.50)),
    }
    (sx, sy), (ex, ey) = focus_map.get(seg.pan, focus_map["center"])
    fx = sx + (ex - sx) * progress
    fy = sy + (ey - sy) * progress
    return fit_cover(img, zoom, fx, fy)


def add_badge(base: Image.Image) -> None:
    draw = ImageDraw.Draw(base, "RGBA")
    font = ImageFont.truetype(FONT_SANS, 34)
    text = "Daïsky Prod"
    x, y = 44, 40
    bbox = draw.textbbox((0, 0), text, font=font)
    pill_w = (bbox[2] - bbox[0]) + 56
    pill_h = 60
    rounded_rectangle(draw, (x, y, x + pill_w, y + pill_h), 28, fill=(8, 21, 15, 175), outline=(244, 201, 93, 235), width=2)
    draw.text((x + 28, y + 11), text, font=font, fill=(244, 201, 93, 255))


def draw_centered_text(draw: ImageDraw.ImageDraw, box: Tuple[int, int, int, int], text: str, font_path: str, size: int, fill, shadow=(0,0,0,120), spacing: int = 6):
    font = ImageFont.truetype(font_path, size)
    lines = text.split("\n")
    metrics = [draw.textbbox((0, 0), ln, font=font, spacing=spacing) for ln in lines]
    line_h = max(b[3] - b[1] for b in metrics)
    total_h = len(lines) * line_h + (len(lines)-1) * spacing
    x1, y1, x2, y2 = box
    y = y1 + (y2 - y1 - total_h) / 2
    for ln in lines:
        bbox = draw.textbbox((0, 0), ln, font=font)
        w = bbox[2] - bbox[0]
        x = x1 + (x2 - x1 - w) / 2
        if shadow:
            draw.text((x + 2, y + 2), ln, font=font, fill=shadow)
        draw.text((x, y), ln, font=font, fill=fill)
        y += line_h + spacing


def draw_pill(draw: ImageDraw.ImageDraw, xy: Tuple[int, int], text: str, font_path: str, size: int, fill_bg, fill_text, outline=None):
    font = ImageFont.truetype(font_path, size)
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x, y = xy
    pad_x, pad_y = 24, 16
    box = (x, y, x + w + pad_x * 2, y + h + pad_y * 2)
    rounded_rectangle(draw, box, radius=26, fill=fill_bg, outline=outline, width=2 if outline else 1)
    draw.text((x + pad_x, y + pad_y - 2), text, font=font, fill=fill_text)
    return box


def add_intro_overlay(base: Image.Image, t: float) -> None:
    fade = 1.0
    if t > 11.5:
        fade = max(0.0, 1 - (t - 11.5) / 2.0)
    if fade <= 0:
        return
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")

    title_panel = (96, 150, 984, 520)
    rounded_rectangle(draw, title_panel, radius=38, fill=(6, 12, 10, int(108 * fade)), outline=(244, 201, 93, int(120 * fade)), width=1)
    draw_centered_text(draw, (110, 180, 970, 470), TITLE, FONT_SERIF, 88, (248, 242, 231, int(255 * fade)), shadow=(0, 0, 0, int(180 * fade)))
    draw_centered_text(draw, (140, 342, 940, 470), ARTIST, FONT_SANS, 44, (244, 201, 93, int(255 * fade)), shadow=(0, 0, 0, int(180 * fade)))

    draw_pill(draw, (160, 620), "♥ LIKE", FONT_SANS, 32, (8, 21, 15, int(185 * fade)), (248, 242, 231, int(255 * fade)), outline=(244, 201, 93, int(235 * fade)))
    draw_pill(draw, (362, 620), "✚ ABONNE-TOI", FONT_SANS, 32, (8, 21, 15, int(185 * fade)), (248, 242, 231, int(255 * fade)), outline=(244, 201, 93, int(235 * fade)))
    draw_pill(draw, (715, 620), "↗ PARTAGE", FONT_SANS, 32, (8, 21, 15, int(185 * fade)), (248, 242, 231, int(255 * fade)), outline=(244, 201, 93, int(235 * fade)))

    brand_box = (110, 740, 970, 890)
    rounded_rectangle(draw, brand_box, radius=34, fill=(8, 21, 15, int(145 * fade)), outline=(31, 175, 115, int(210 * fade)), width=2)
    draw_centered_text(draw, brand_box, f"Prod : {PROD}\nStudio : {STUDIO}", FONT_SANS, 34, (248, 242, 231, int(240 * fade)))

    footer_box = (280, 1440, 800, 1540)
    rounded_rectangle(draw, footer_box, radius=28, fill=(8, 21, 15, int(135 * fade)))
    draw_centered_text(draw, footer_box, "@daiskypro", FONT_SANS, 34, (248, 242, 231, int(255 * fade)))

    base.alpha_composite(overlay)


def add_outro_overlay(base: Image.Image, t: float) -> None:
    fade = min(1.0, max(0.0, (t - 229.0) / 1.2))
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")

    panel = (70, 170, 1010, 1040)
    rounded_rectangle(draw, panel, radius=42, fill=(6, 12, 10, int(185 * fade)), outline=(244, 201, 93, int(210 * fade)), width=2)
    draw_centered_text(draw, (120, 210, 960, 360), TITLE, FONT_SERIF, 78, (248, 242, 231, int(255 * fade)))
    draw_centered_text(draw, (160, 330, 920, 425), ARTIST, FONT_SANS, 38, (244, 201, 93, int(250 * fade)))

    credits = (
        f"Signature : {TAGLINE}\n"
        f"Prod : {PROD} • Studio : {STUDIO}\n"
        f"Contact : {CONTACT}\n"
        f"Emails : {EMAILS}\n"
        f"{LINK}"
    )
    draw_centered_text(draw, (120, 430, 960, 960), credits, FONT_SANS, 28, (248, 242, 231, int(245 * fade)), spacing=10)

    draw_pill(draw, (150, 1130), "♥ LIKE", FONT_SANS, 30, (244, 201, 93, int(220 * fade)), (8, 21, 15, int(255 * fade)))
    draw_pill(draw, (355, 1130), "✚ ABONNE-TOI", FONT_SANS, 30, (244, 201, 93, int(220 * fade)), (8, 21, 15, int(255 * fade)))
    draw_pill(draw, (710, 1130), "↗ PARTAGE", FONT_SANS, 30, (244, 201, 93, int(220 * fade)), (8, 21, 15, int(255 * fade)))

    footer_box = (250, 1240, 830, 1328)
    rounded_rectangle(draw, footer_box, radius=26, fill=(8, 21, 15, int(130 * fade)))
    draw_centered_text(draw, footer_box, "@daiskypro", FONT_SANS, 32, (248, 242, 231, int(255 * fade)))

    base.alpha_composite(overlay)


def render_frame(t: float, segments: List[Segment], images: dict[str, Image.Image], bottom_gradient: Image.Image) -> np.ndarray:
    # Centered crossfade across boundaries.
    for idx in range(len(segments) - 1):
        boundary = segments[idx].end
        if boundary - TRANSITION_HALF <= t < boundary + TRANSITION_HALF:
            alpha = (t - (boundary - TRANSITION_HALF)) / TRANSITION
            frame_a = render_segment_frame(images[segments[idx].id], segments[idx], t).convert("RGBA")
            frame_b = render_segment_frame(images[segments[idx + 1].id], segments[idx + 1], t).convert("RGBA")
            frame = Image.blend(frame_a, frame_b, alpha)
            break
    else:
        seg = next((s for s in segments if s.start <= t < s.end), segments[-1])
        frame = render_segment_frame(images[seg.id], seg, t).convert("RGBA")

    # Bottom readability gradient.
    frame.alpha_composite(bottom_gradient, (0, HEIGHT - bottom_gradient.height))

    add_badge(frame)
    if t < 14.0:
        add_intro_overlay(frame, t)
    if t >= 229.0:
        add_outro_overlay(frame, t)

    # Soft global vignette for contrast.
    vignette = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette, "RGBA")
    vd.rectangle((0, 0, WIDTH, HEIGHT), fill=(0, 0, 0, 15))
    frame.alpha_composite(vignette)

    return np.asarray(frame.convert("RGB"), dtype=np.uint8)


def render_silent_video(segments: List[Segment], output_path: Path) -> None:
    images = load_images(segments)
    bottom_gradient = make_vertical_gradient(720, 0, 155)

    writer = imageio_ffmpeg.write_frames(
        str(output_path),
        size=(WIDTH, HEIGHT),
        fps=FPS,
        codec="libx264",
        pix_fmt_in="rgb24",
        pix_fmt_out="yuv420p",
        macro_block_size=1,
        ffmpeg_log_level="error",
        output_params=["-crf", "20", "-preset", "veryfast", "-movflags", "+faststart"],
    )
    writer.send(None)
    frame_count = int(round(VIDEO_DURATION * FPS))
    for i in range(frame_count):
        t = i / FPS
        frame = render_frame(t, segments, images, bottom_gradient)
        writer.send(frame)
        if i % 180 == 0:
            print(f"Rendered frame {i}/{frame_count}", flush=True)
    writer.close()


def burn_subtitles_and_audio(bg_video: Path, ass_file: Path, final_video: Path) -> None:
    cmd = [
        FFMPEG,
        "-y",
        "-i",
        str(bg_video),
        "-i",
        str(AUDIO),
        "-vf",
        f"ass={ass_file}",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-crf",
        "20",
        "-preset",
        "veryfast",
        "-movflags",
        "+faststart",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-af",
        "loudnorm=I=-14:TP=-1.5,aresample=48000",
        "-r",
        str(FPS),
        "-t",
        str(VIDEO_DURATION),
        str(final_video),
    ]
    print("Running ffmpeg burn-in...", flush=True)
    subprocess.run(cmd, check=True)


def render_cover(segments: List[Segment], output_9x16: Path, output_square: Path) -> None:
    img = Image.open(segments[0].image).convert("RGB")
    cover = fit_cover(img, 1.02, 0.50, 0.42).convert("RGBA")
    add_badge(cover)
    overlay = Image.new("RGBA", cover.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    rounded_rectangle(draw, (74, 1330, 1006, 1780), radius=42, fill=(6, 12, 10, 165), outline=(244, 201, 93, 215), width=2)
    draw_centered_text(draw, (120, 1360, 960, 1480), TITLE, FONT_SERIF, 86, (248, 242, 231, 255))
    draw_centered_text(draw, (140, 1495, 940, 1570), ARTIST, FONT_SANS, 42, (244, 201, 93, 255))
    draw_centered_text(draw, (120, 1580, 960, 1710), TAGLINE, FONT_SANS, 28, (248, 242, 231, 235), spacing=8)
    draw_centered_text(draw, (120, 1690, 960, 1765), "Prod : Daïsky Prod • Studio : TechStein", FONT_SANS, 25, (248, 242, 231, 230))
    cover.alpha_composite(overlay)
    cover.convert("RGB").save(output_9x16, quality=95)

    square_src = cover.convert("RGB")
    side = min(square_src.size)
    left = (square_src.width - side) // 2
    top = max(0, (square_src.height - side) // 2 - 60)
    square = square_src.crop((left, top, left + side, top + side)).resize((1400, 1400), Image.Resampling.LANCZOS)
    square.save(output_square, quality=95)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    segments = build_segments()
    subtitles = parse_lyrics()
    manifest = build_manifest(segments, subtitles)

    manifest_path = SRC_DIR / "manifest.json"
    ass_path = SRC_DIR / "mama_tche_subtitles.ass"
    bg_video = OUT_DIR / "Mama_tche_Daïsky_Lyrics_9x16_bg.mp4"
    final_video = OUT_DIR / "Mama_tche_Daïsky_Lyrics_9x16.mp4"
    cover_9x16 = OUT_DIR / "Cover_Mama_tche_Daïsky_1080x1920.jpg"
    cover_square = OUT_DIR / "pochette_Mama_tche_Daïsky_1400.jpg"

    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    write_ass(subtitles, ass_path)
    render_cover(segments, cover_9x16, cover_square)
    render_silent_video(segments, bg_video)
    burn_subtitles_and_audio(bg_video, ass_path, final_video)
    print(f"Done: {final_video}")


if __name__ == "__main__":
    main()
