#!/usr/bin/env python3
"""Render the Ghost u see vertical lyric film from the artist's master and timed lyric map.

Requirements (local only): Pillow, mutagen, imageio-ffmpeg.
Run from any directory: python3 projects/ghost-u-see/render.py
"""
from __future__ import annotations

import json
import math
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
import imageio_ffmpeg
from mutagen.mp4 import MP4

ROOT = Path(__file__).resolve().parents[2]
PROJECT = Path(__file__).resolve().parent
ASSETS = PROJECT / "assets"
MAP_FILE = PROJECT / "verses_map.json"
OUTPUT_DIR = ROOT / "livrables"
VIDEO = OUTPUT_DIR / "GHOST-U-SEE-DAISKY-9x16.mp4"
COVER = OUTPUT_DIR / "COVER-GHOST-U-SEE-1080x1920.jpg"
ASS_FILE = PROJECT / "ghost_u_see.ass"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FONT_REG = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
FONT_BOLD = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
FONT_GOTHIC = ASSETS / "fonts" / "UnifrakturCook-Bold.ttf"

GOLD_ASS = "&H00A8E8FF&"       # ASS is AABBGGRR
PALE_ASS = "&H00F4FBFF&"
CYAN_ASS = "&H00E0CD96&"
INK_ASS = "&H00100A06&"
PILL_BG_ASS = "&H25080C12&"
OUTLINE_GOLD_ASS = "&H003EA8E8&"


def run(cmd: list[str], *, capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, text=True, stdout=subprocess.PIPE if capture else None,
                          stderr=subprocess.PIPE if capture else None)


def ass_time(seconds: float) -> str:
    cs = max(0, round(seconds * 100))
    h, rem = divmod(cs, 360000)
    m, rem = divmod(rem, 6000)
    s, centi = divmod(rem, 100)
    return f"{h}:{m:02d}:{s:02d}.{centi:02d}"


def ass_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


def split_to_fit(text: str, font_path: Path, px: int, max_width: int, max_lines: int = 2) -> tuple[str, int]:
    font = ImageFont.truetype(str(font_path), px)
    words = text.split()
    rows: list[str] = []
    current = ""
    for word in words:
        attempt = f"{current} {word}".strip()
        if font.getlength(attempt) <= max_width or not current:
            current = attempt
        else:
            rows.append(current)
            current = word
    if current:
        rows.append(current)
    while len(rows) > max_lines and px > 42:
        px -= 2
        return split_to_fit(text, font_path, px, max_width, max_lines)
    return r"\N".join(ass_escape(row) for row in rows), px


def karaoke(text: str, duration: float) -> str:
    words = text.split()
    if not words:
        return ass_escape(text)
    weights = [max(1, len(re.sub(r"[^\wÀ-ÿ]", "", w))) for w in words]
    total_cs = max(len(words), round(duration * 100))
    raw = [total_cs * w / sum(weights) for w in weights]
    centis = [max(1, int(x)) for x in raw]
    centis[-1] += total_cs - sum(centis)
    return "".join(f"{{\\kf{n}}}{ass_escape(word)} " for n, word in zip(centis, words)).rstrip()


def make_ass(data: dict) -> None:
    header = r'''[Script Info]
Title: Ghost u see — lyric video
ScriptType: v4.00+
WrapStyle: 2
ScaledBorderAndShadow: yes
PlayResX: 1080
PlayResY: 1920
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,UnifrakturCook,76,&H00A8E8FF&,&H00E0CD96&,&H00100A06&,&H00000000&,-1,0,1,4,1,5,170,170,0,1
Style: Pill,DejaVu Sans,30,&H00F4FBFF&,&H007AE0FF&,&H00100A06&,&H00000000&,-1,0,1,3,0,5,186,186,0,1
Style: Card,UnifrakturCook,88,&H00A8E8FF&,&H00F4FBFF&,&H00100A06&,&H00000000&,-1,0,1,4,2,5,80,80,0,1
Style: SubCard,DejaVu Sans,32,&H00F4FBFF&,&H00A8E8FF&,&H00100A06&,&H00000000&,-1,0,1,3,1,5,90,90,0,1
Style: Badge,DejaVu Sans,32,&H00A8E8FF&,&H00F4FBFF&,&H00100A06&,&H00000000&,-1,0,1,3,1,8,30,30,174,1
Style: EndTitle,DejaVu Sans,72,&H00A8E8FF&,&H00F4FBFF&,&H00100A06&,&H00000000&,-1,0,1,4,2,5,80,80,0,1
Style: EndSub,DejaVu Sans,30,&H00F4FBFF&,&H00A8E8FF&,&H00100A06&,&H00000000&,-1,0,1,3,1,5,90,90,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    events: list[str] = []

    def add(start: float, end: float, style: str, text: str, layer: int = 2) -> None:
        if end <= start:
            return
        events.append(f"Dialogue: {layer},{ass_time(start)},{ass_time(end)},{style},,0,0,0,,{text}")

    # Two-beat welcome card during the opening hum.
    add(0.35, 4.2, "Card", r"{\an5\pos(540,850)\fad(280,180)}SALUT · WTBW")
    add(0.45, 4.2, "SubCard", r"{\an5\pos(540,965)\fad(280,180)}Wolof TechStein beat wê")
    add(4.2, 8.4, "Card", r"{\an5\pos(540,850)\fad(180,220)}GHOST U SEE")
    add(4.2, 8.4, "SubCard", r"{\an5\pos(540,965)\fad(180,220)}DAÏSKY · une histoire de regards et d’identités")

    # Original lines are painted into the generated images; overlay only French translations when provided.
    for verse in data["verses"]:
        if verse["type"] != "lyric":
            continue
        start = float(verse["start"])
        end = min(float(verse["end"]), 245.006) - 0.08
        if end <= start:
            continue
        # The original lyric is already part of the generated illustration. Do not print it again.
        if verse.get("fr"):
            line_duration = end - start
            translated = verse["fr"]
            translated_display, pill_size = split_to_fit(translated, FONT_BOLD, 30, 700, 2)
            # Karaoke paints the translated words one at a time; the French audio lines remain pill-free.
            timing = max(0.2, line_duration - 0.25)
            karaoke_text = karaoke(translated, timing)
            # Keep translation line spacing compact inside the safe lower pill.
            if r"\N" in translated_display:
                # Long French phrases use two balanced rows; retain word-level timing across both rows.
                words = translated.split()
                mid = (len(words) + 1) // 2
                cut = sum(max(1, len(re.sub(r"[^\wÀ-ÿ]", "", w))) for w in words[:mid]) / max(1, sum(max(1, len(re.sub(r"[^\wÀ-ÿ]", "", w))) for w in words))
                first_duration = max(0.1, timing * cut)
                karaoke_text = karaoke(" ".join(words[:mid]), first_duration) + r"\N" + karaoke(" ".join(words[mid:]), timing-first_duration)
            pill_bg = (r"{\an7\pos(186,150)\p1\bord3\shad0\1c&H180C0A08&\3c&H003EA8E8&}"
                       r"m 24 0 l684 0 b 697 0 708 11 708 24 l708 69 b708 82 697 93 684 93 "
                       r"l24 93 b11 93 0 82 0 69 l0 24 b0 11 11 0 24 0 c{\p0}")
            add(start + 0.12, end, "Pill", pill_bg, 2)
            pill = f"{{\\an5\\pos(540,197)\\fs{pill_size}\\bord3\\3c&H00100A06&\\shad0\\fad(90,100)}}{karaoke_text}"
            add(start + 0.12, end, "Pill", pill, 4)

    # Warm, minimal end card; the artist's audio ends at 245.006s and the visual holds five seconds.
    add(245.006, 250.006, "EndTitle", r"{\an5\pos(540,1120)\fad(250,300)}MERCI · WTBW", 4)
    add(245.006, 250.006, "EndSub", r"{\an5\pos(540,1230)\fad(250,300)}Merci d’avoir écouté · Wolof TechStein beat wê", 4)
    add(245.006, 250.006, "EndSub", r"{\an5\pos(540,1340)\fad(250,300)}GHOST U SEE · DAÏSKY", 4)

    ASS_FILE.write_text(header + "\n".join(events) + "\n", encoding="utf-8")


def make_cover() -> None:
    source = Image.open(ASSETS / "scene01_cold_stage.png").convert("RGB")
    source = source.resize((1080, 1920), Image.Resampling.LANCZOS)
    overlay = Image.new("RGBA", source.size, (0, 0, 0, 0))
    pix = overlay.load()
    for y in range(1000, 1710):
        a = int(6 + 176 * (y - 1000) / 710)
        for x in range(1080):
            pix[x, y] = (4, 8, 14, a)
    source = Image.alpha_composite(source.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(source)
    f_title = ImageFont.truetype(str(FONT_GOTHIC), 150)
    f_artist = ImageFont.truetype(str(FONT_BOLD), 58)
    f_series = ImageFont.truetype(str(FONT_REG), 34)

    def centered(text: str, y: int, font: ImageFont.FreeTypeFont, fill: tuple[int, int, int, int], sw: int = 0,
                 font_path: Path = FONT_BOLD):
        box = draw.textbbox((0, 0), text, font=font, stroke_width=sw)
        width = box[2] - box[0]
        # The title must remain within the TikTok safe width x=90..990.
        while width > 900 and font.size > 68:
            font = ImageFont.truetype(str(font_path), font.size - 2)
            box = draw.textbbox((0, 0), text, font=font, stroke_width=sw)
            width = box[2] - box[0]
        x = (1080 - width) // 2
        draw.text((x, y), text, font=font, fill=fill, stroke_width=sw, stroke_fill=(3, 7, 12, 255))

    centered("GHOST U SEE", 1260, f_title, (255, 232, 168, 255), 5, FONT_GOTHIC)
    centered("DSKY", 1416, f_artist, (242, 249, 255, 255), 3, FONT_BOLD)
    draw.line((250, 1513, 830, 1513), fill=(232, 168, 62, 220), width=3)
    centered("Wolof TechStein beat wê", 1532, f_series, (240, 247, 255, 255), 1, FONT_REG)
    source.convert("RGB").save(COVER, "JPEG", quality=95, subsampling=0, optimize=True)


def prepare_motion_plate(source_path: Path) -> Path:
    """Precompose a blurred extension so gentle camera motion never clips baked-in lyrics."""
    cache_dir = ROOT / ".cache" / "ghost-u-see" / "motion-plates"
    cache_dir.mkdir(parents=True, exist_ok=True)
    target = cache_dir / f"{source_path.stem}.jpg"
    if target.exists() and target.stat().st_mtime >= source_path.stat().st_mtime:
        return target
    source = Image.open(source_path).convert("RGB")
    backdrop = ImageOps.fit(source, (1080, 1920), method=Image.Resampling.LANCZOS)
    backdrop = backdrop.filter(ImageFilter.GaussianBlur(24))
    backdrop = ImageEnhance.Brightness(backdrop).enhance(0.78)
    backdrop = ImageEnhance.Color(backdrop).enhance(1.12)
    foreground = ImageOps.contain(source, (940, 1680), method=Image.Resampling.LANCZOS)
    x = (1080 - foreground.width) // 2
    y = (1920 - foreground.height) // 2
    backdrop.paste(foreground, (x, y))
    backdrop.save(target, "JPEG", quality=94, subsampling=0, optimize=True)
    return target


def loudnorm_measure(audio: Path) -> dict[str, float]:
    proc = run([FFMPEG, "-hide_banner", "-nostats", "-i", str(audio), "-af",
                "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture=True)
    text = (proc.stderr or "")
    matches = re.findall(r"\{\s*\n\s*\"input_i\".*?\n\s*\}", text, flags=re.S)
    if not matches:
        raise RuntimeError("Could not parse first-pass loudnorm measurement from ffmpeg")
    return json.loads(matches[-1])


def render() -> None:
    data = json.loads(MAP_FILE.read_text(encoding="utf-8"))
    audio = (PROJECT / data["audio"]).resolve()
    if not audio.is_file():
        raise FileNotFoundError(audio)
    duration = MP4(str(audio)).info.length
    if abs(duration - data["audio_duration"]) > 0.3:
        raise RuntimeError(f"Master duration changed: {duration:.3f}s, map says {data['audio_duration']:.3f}s")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    make_ass(data)
    make_cover()

    if any(not verse.get("image") for verse in data["verses"] if verse["type"] == "lyric"):
        raise RuntimeError("A lyric cue has no generated image mapping")
    lyric_scenes = [
        {"start": float(verse["start"]), "end": float(verse["end"]), "image": verse["image"]}
        for verse in data["verses"] if verse["type"] == "lyric"
    ]
    scenes = [data["scene_plan"][0], *lyric_scenes, data["scene_plan"][1]]
    missing_images = [str(ASSETS / scene["image"]) for scene in scenes if not (ASSETS / scene["image"]).is_file()]
    if missing_images:
        raise FileNotFoundError("Missing image assets: " + ", ".join(missing_images))
    transition = float(data["transition_seconds"])
    total = float(data["video_duration"])
    plate_paths = [prepare_motion_plate(ASSETS / scene["image"]) for scene in scenes]
    cmd = [FFMPEG, "-hide_banner", "-y", "-filter_complex_threads", "1"]
    for plate in plate_paths:
        cmd += ["-loop", "1", "-framerate", "30", "-i", str(plate)]
    audio_index = len(scenes)
    cmd += ["-i", str(audio)]

    filters: list[str] = []
    for i, scene in enumerate(scenes):
        seg_len = float(scene["end"]) - float(scene["start"])
        source_len = seg_len + (transition if i < len(scenes) - 1 else 0)
        # A slow, oscillating push and drift over the precomposed plate keeps lettering safe and motion continuous.
        zoom = "1.08+0.012*sin(on/210)"
        xexpr = "iw/2-(iw/zoom/2)+18*sin(on/44)"
        yexpr = "ih/2-(ih/zoom/2)+24*cos(on/54)"
        filters.append(
            f"[{i}:v]zoompan=z='{zoom}':x='{xexpr}':y='{yexpr}':d=1:s=1080x1920:fps=30,"
            f"trim=duration={source_len:.6f},setpts=PTS-STARTPTS,setsar=1,format=yuv420p,settb=AVTB[v{i}]"
        )
    prev = "v0"
    elapsed = float(scenes[0]["end"]) - float(scenes[0]["start"])
    for i in range(1, len(scenes)):
        out = f"x{i}"
        filters.append(f"[{prev}][v{i}]xfade=transition=fade:duration={transition:.3f}:offset={elapsed:.6f}[{out}]")
        prev = out
        elapsed += float(scenes[i]["end"]) - float(scenes[i]["start"])
    ass_path = str(ASS_FILE.resolve()).replace("\\", "\\\\").replace(":", r"\:").replace("'", r"\'")
    fonts_dir = str((ASSETS / 'fonts').resolve()).replace("'", r"\'")
    filters.append(f"[{prev}]subtitles='{ass_path}':fontsdir='{fonts_dir}',format=yuv420p,noise=alls=8:allf=t+u:all_seed=42[vout]")

    measured = loudnorm_measure(audio)
    af = ("loudnorm=I=-14:TP=-1.5:LRA=11:linear=true:"
          f"measured_I={measured['input_i']}:measured_TP={measured['input_tp']}:"
          f"measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}:"
          f"offset={measured['target_offset']}:print_format=summary,"
          "apad=pad_dur=5,atrim=duration=250.006,aresample=48000")
    graph = ";".join(filters)
    cmd += ["-filter_complex", graph, "-map", "[vout]", "-map", f"{audio_index}:a:0",
            "-af", af, "-t", f"{total:.3f}", "-r", "30", "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "24", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
            "-color_trc", "bt709", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart", str(VIDEO)]
    print("First-pass loudness:", json.dumps(measured, ensure_ascii=False))
    print(f"Rendering {len(scenes)} image segments ({len(lyric_scenes)} individual lyric illustrations), French translation karaoke, and the original master audio...")
    run(cmd)
    print(f"Created {VIDEO} ({VIDEO.stat().st_size / 1_000_000:.1f} MB)")
    print(f"Created {COVER} ({COVER.stat().st_size / 1_000_000:.1f} MB)")


if __name__ == "__main__":
    try:
        render()
    except Exception as exc:
        print(f"Render failed: {exc}", file=sys.stderr)
        raise
