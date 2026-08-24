from __future__ import annotations

import json
import math
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import imageio_ffmpeg
import numpy as np
from mutagen.mp3 import MP3
from PIL import Image, ImageDraw, ImageFont

import render_video as rv

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "mama-tche"
RAW_ROOT = PROJECT / "assets" / "raw" / "16x9"
OUT_DIR = PROJECT / "livrables"
SRC_DIR = PROJECT / "src"
AUDIO = ROOT / "Mama_tche_Daïsky.mp3"

WIDTH = 1920
HEIGHT = 1080
FPS = 30
VIDEO_DURATION = round(MP3(AUDIO).info.length, 3)
TRANSITION = 0.8
TRANSITION_HALF = TRANSITION / 2
SAFE_SUB_MARGIN = 88

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


@dataclass
class Segment:
    id: str
    image: Path
    start: float
    end: float
    ken_burns: str
    pan: str


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


def build_segments() -> List[Segment]:
    session_paths = []
    for folder in [RAW_ROOT / "session01", RAW_ROOT / "session02", RAW_ROOT / "session03"]:
        session_paths.extend(sorted(folder.glob("*.jpg")))
    assert len(session_paths) == 30, f"Expected 30 images, found {len(session_paths)}"
    boundaries = [
        0.0, 14.0, 23.9, 31.0, 41.9, 52.0, 58.0, 65.0, 72.0, 80.0,
        90.0, 97.0, 104.0, 111.0, 118.0, 125.0, 131.0, 138.0, 145.0,
        153.8, 162.0, 167.0, 174.0, 181.0, 189.0, 195.9, 203.0, 210.0,
        216.0, 229.0, 240.0,
    ]
    pans = ["center", "left", "right", "up", "down", "center"]
    return [
        Segment(
            id=f"S{i+1:02d}",
            image=session_paths[i],
            start=boundaries[i],
            end=boundaries[i + 1],
            ken_burns="in" if i % 2 == 0 else "out",
            pan=pans[i % len(pans)],
        )
        for i in range(30)
    ]


def build_manifest(segments: List[Segment], subtitles: list[rv.SubtitleEvent]) -> dict:
    return {
        "title": TITLE,
        "artist": ARTIST,
        "audio": AUDIO.name,
        "duration": VIDEO_DURATION,
        "format": "16x9",
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


def write_ass(subtitles: list[rv.SubtitleEvent], dest: Path) -> None:
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {WIDTH}
PlayResY: {HEIGHT}
ScaledBorderAndShadow: yes
WrapStyle: 2
YCbCr Matrix: TV.601

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: IntroSerif,DejaVu Serif,44,&H00F8F2E7,&H000000FF,&H002A714C,&H55000000,1,0,0,0,100,100,0,0,1,3.0,1.2,2,120,120,90,1
Style: VerseMono,DejaVu Sans Mono,44,&H00F8F2E7,&H000000FF,&H002A714C,&H55000000,1,0,0,0,100,100,0.3,0,1,3.2,1.2,2,120,120,{SAFE_SUB_MARGIN},1
Style: VerseSans,DejaVu Sans,44,&H00F8F2E7,&H000000FF,&H002A714C,&H55000000,1,0,0,0,100,100,0.3,0,1,3.2,1.2,2,120,120,{SAFE_SUB_MARGIN},1
Style: RefrainGold,DejaVu Sans,52,&H00F4C95D,&H000000FF,&H00145A3B,&H66000000,1,0,0,0,100,100,0.4,0,1,3.6,1.4,2,110,110,{SAFE_SUB_MARGIN},1
Style: FinalRefrainGold,DejaVu Sans,56,&H00F4C95D,&H000000FF,&H00145A3B,&H66000000,1,0,0,0,100,100,0.5,0,1,3.8,1.5,2,100,100,{SAFE_SUB_MARGIN},1
Style: BridgeSerifCenter,DejaVu Serif,46,&H00F8F2E7,&H000000FF,&H002A714C,&H66000000,1,0,0,0,100,100,0.2,0,1,3.4,1.2,5,100,100,0,1
Style: HookGold,DejaVu Sans,48,&H00F4C95D,&H000000FF,&H00145A3B,&H66000000,1,0,0,0,100,100,0.6,0,1,3.8,1.4,2,110,110,{SAFE_SUB_MARGIN},1
Style: OutroSerif,DejaVu Serif,44,&H00F8F2E7,&H000000FF,&H002A714C,&H66000000,1,0,0,0,100,100,0.2,0,1,3.4,1.2,2,120,120,{SAFE_SUB_MARGIN},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [
        f"Dialogue: 0,{ass_time(ev.start)},{ass_time(ev.end)},{ev.style},,0,0,0,,{{\\fad(140,140)}}{ev.text.replace('{','(').replace('}',')')}"
        for ev in subtitles
    ]
    dest.write_text(ass + "\n".join(lines) + "\n", encoding="utf-8")


def load_images(segments: List[Segment]) -> dict[str, Image.Image]:
    return {seg.id: Image.open(seg.image).convert("RGB") for seg in segments}


def make_vertical_gradient(height: int, start_alpha: int = 0, end_alpha: int = 165) -> Image.Image:
    grad = Image.new("L", (1, height))
    grad.putdata([int(start_alpha + (end_alpha - start_alpha) * (y / max(1, height - 1))) for y in range(height)])
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
    zoom = 1.00 + 0.05 * progress if seg.ken_burns == "in" else 1.05 - 0.05 * progress
    focus_map = {
        "center": ((0.50, 0.50), (0.52, 0.52)),
        "left": ((0.42, 0.50), (0.55, 0.50)),
        "right": ((0.58, 0.50), (0.45, 0.50)),
        "up": ((0.50, 0.38), (0.50, 0.52)),
        "down": ((0.50, 0.60), (0.50, 0.48)),
    }
    (sx, sy), (ex, ey) = focus_map.get(seg.pan, focus_map["center"])
    fx = sx + (ex - sx) * progress
    fy = sy + (ey - sy) * progress
    return fit_cover(img, zoom, fx, fy)


def add_badge(base: Image.Image) -> None:
    draw = ImageDraw.Draw(base, "RGBA")
    font = ImageFont.truetype(FONT_SANS, 32)
    text = "Daïsky Prod"
    x, y = 36, 30
    bbox = draw.textbbox((0, 0), text, font=font)
    pill_w = (bbox[2] - bbox[0]) + 48
    pill_h = 52
    rounded_rectangle(draw, (x, y, x + pill_w, y + pill_h), 24, fill=(8, 21, 15, 175), outline=(244, 201, 93, 235), width=2)
    draw.text((x + 24, y + 9), text, font=font, fill=(244, 201, 93, 255))


def draw_centered_text(draw: ImageDraw.ImageDraw, box: Tuple[int, int, int, int], text: str, font_path: str, size: int, fill, shadow=(0,0,0,120), spacing: int = 6):
    font = ImageFont.truetype(font_path, size)
    lines = text.split("\n")
    metrics = [draw.textbbox((0, 0), ln, font=font, spacing=spacing) for ln in lines]
    line_h = max(b[3] - b[1] for b in metrics)
    total_h = len(lines) * line_h + (len(lines) - 1) * spacing
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
    pad_x, pad_y = 18, 12
    box = (x, y, x + w + pad_x * 2, y + h + pad_y * 2)
    rounded_rectangle(draw, box, radius=22, fill=fill_bg, outline=outline, width=2 if outline else 1)
    draw.text((x + pad_x, y + pad_y - 2), text, font=font, fill=fill_text)


def add_intro_overlay(base: Image.Image, t: float) -> None:
    fade = 1.0 if t <= 11.5 else max(0.0, 1 - (t - 11.5) / 2.0)
    if fade <= 0:
        return
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    panel = (120, 90, 860, 340)
    rounded_rectangle(draw, panel, radius=34, fill=(6, 12, 10, int(120 * fade)), outline=(244, 201, 93, int(120 * fade)), width=1)
    draw_centered_text(draw, (140, 110, 840, 240), TITLE, FONT_SERIF, 70, (248, 242, 231, int(255 * fade)), shadow=(0, 0, 0, int(180 * fade)))
    draw_centered_text(draw, (140, 220, 840, 300), ARTIST, FONT_SANS, 34, (244, 201, 93, int(255 * fade)), shadow=(0, 0, 0, int(180 * fade)))
    draw_pill(draw, (145, 370), "♥ LIKE", FONT_SANS, 24, (8, 21, 15, int(185 * fade)), (248, 242, 231, int(255 * fade)), outline=(244, 201, 93, int(235 * fade)))
    draw_pill(draw, (325, 370), "✚ ABONNE-TOI", FONT_SANS, 24, (8, 21, 15, int(185 * fade)), (248, 242, 231, int(255 * fade)), outline=(244, 201, 93, int(235 * fade)))
    draw_pill(draw, (630, 370), "↗ PARTAGE", FONT_SANS, 24, (8, 21, 15, int(185 * fade)), (248, 242, 231, int(255 * fade)), outline=(244, 201, 93, int(235 * fade)))
    brand_box = (120, 460, 860, 560)
    rounded_rectangle(draw, brand_box, radius=26, fill=(8, 21, 15, int(145 * fade)), outline=(31, 175, 115, int(210 * fade)), width=2)
    draw_centered_text(draw, brand_box, f"Prod : {PROD}\nStudio : {STUDIO}", FONT_SANS, 26, (248, 242, 231, int(240 * fade)))
    base.alpha_composite(overlay)


def add_outro_overlay(base: Image.Image, t: float) -> None:
    fade = min(1.0, max(0.0, (t - 229.0) / 1.2))
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    panel = (965, 80, 1840, 720)
    rounded_rectangle(draw, panel, radius=34, fill=(6, 12, 10, int(185 * fade)), outline=(244, 201, 93, int(210 * fade)), width=2)
    draw_centered_text(draw, (1000, 100, 1805, 195), TITLE, FONT_SERIF, 62, (248, 242, 231, int(255 * fade)))
    draw_centered_text(draw, (1000, 180, 1805, 245), ARTIST, FONT_SANS, 30, (244, 201, 93, int(250 * fade)))
    credits = (
        f"Signature : {TAGLINE}\n"
        f"Prod : {PROD} • Studio : {STUDIO}\n"
        f"Contact : {CONTACT}\n"
        f"Emails : {EMAILS}\n"
        f"{LINK}"
    )
    draw_centered_text(draw, (1010, 250, 1800, 650), credits, FONT_SANS, 24, (248, 242, 231, int(245 * fade)), spacing=8)
    draw_pill(draw, (1030, 760), "♥ LIKE", FONT_SANS, 22, (244, 201, 93, int(220 * fade)), (8, 21, 15, int(255 * fade)))
    draw_pill(draw, (1190, 760), "✚ ABONNE-TOI", FONT_SANS, 22, (244, 201, 93, int(220 * fade)), (8, 21, 15, int(255 * fade)))
    draw_pill(draw, (1465, 760), "↗ PARTAGE", FONT_SANS, 22, (244, 201, 93, int(220 * fade)), (8, 21, 15, int(255 * fade)))
    footer = (1160, 845, 1635, 910)
    rounded_rectangle(draw, footer, radius=20, fill=(8, 21, 15, int(130 * fade)))
    draw_centered_text(draw, footer, "@daiskypro", FONT_SANS, 24, (248, 242, 231, int(255 * fade)))
    base.alpha_composite(overlay)


def render_frame(t: float, segments: List[Segment], images: dict[str, Image.Image], bottom_gradient: Image.Image) -> np.ndarray:
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
    frame.alpha_composite(bottom_gradient, (0, HEIGHT - bottom_gradient.height))
    add_badge(frame)
    if t < 14.0:
        add_intro_overlay(frame, t)
    if t >= 229.0:
        add_outro_overlay(frame, t)
    return np.asarray(frame.convert("RGB"), dtype=np.uint8)


def render_silent_video(segments: List[Segment], output_path: Path) -> None:
    images = load_images(segments)
    bottom_gradient = make_vertical_gradient(250, 0, 150)
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
        writer.send(render_frame(t, segments, images, bottom_gradient))
        if i % 300 == 0:
            print(f"Rendered frame {i}/{frame_count}", flush=True)
    writer.close()


def mux_audio(bg_video: Path, ass_file: Path, final_video: Path) -> None:
    cmd = [
        FFMPEG, "-y", "-i", str(bg_video), "-i", str(AUDIO),
        "-vf", f"ass={ass_file}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "veryfast",
        "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k",
        "-af", "loudnorm=I=-14:TP=-1.5,aresample=48000", "-r", str(FPS), "-t", str(VIDEO_DURATION), str(final_video),
    ]
    subprocess.run(cmd, check=True)


def render_covers(segments: List[Segment], cover_16x9: Path, thumb_1280: Path) -> None:
    img = Image.open(segments[0].image).convert("RGB")
    cover = fit_cover(img, 1.02, 0.48, 0.46).convert("RGBA")
    add_badge(cover)
    overlay = Image.new("RGBA", cover.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    rounded_rectangle(draw, (1120, 90, 1830, 470), radius=34, fill=(6, 12, 10, 170), outline=(244, 201, 93, 215), width=2)
    draw_centered_text(draw, (1160, 120, 1790, 225), TITLE, FONT_SERIF, 64, (248, 242, 231, 255))
    draw_centered_text(draw, (1160, 215, 1790, 275), ARTIST, FONT_SANS, 30, (244, 201, 93, 255))
    draw_centered_text(draw, (1160, 275, 1790, 355), TAGLINE, FONT_SANS, 22, (248, 242, 231, 235), spacing=6)
    draw_centered_text(draw, (1160, 355, 1790, 430), "Prod : Daïsky Prod • Studio : TechStein", FONT_SANS, 22, (248, 242, 231, 230))
    cover.alpha_composite(overlay)
    cover_rgb = cover.convert("RGB")
    cover_rgb.save(cover_16x9, quality=95)
    cover_rgb.resize((1280, 720), Image.Resampling.LANCZOS).save(thumb_1280, quality=95)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    segments = build_segments()
    subtitles = rv.parse_lyrics()
    manifest = build_manifest(segments, subtitles)

    manifest_path = SRC_DIR / "manifest_16x9.json"
    ass_path = SRC_DIR / "mama_tche_subtitles_16x9.ass"
    bg_video = OUT_DIR / "Mama_tche_Daïsky_Lyrics_16x9_bg.mp4"
    final_video = OUT_DIR / "Mama_tche_Daïsky_Lyrics_16x9_YT.mp4"
    cover_16x9 = OUT_DIR / "Cover_Mama_tche_Daïsky_1920x1080.jpg"
    thumb_1280 = OUT_DIR / "Thumbnail_Mama_tche_Daïsky_1280x720.jpg"

    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    write_ass(subtitles, ass_path)
    render_covers(segments, cover_16x9, thumb_1280)
    render_silent_video(segments, bg_video)
    mux_audio(bg_video, ass_path, final_video)
    print(f"Done: {final_video}")


if __name__ == "__main__":
    main()
