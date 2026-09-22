#!/usr/bin/env python3
"""Render Noukiko as one continuous 9:16 image pipe.

The script follows the current prompt: one continuous frame stream, lyric
windows from PLAN_9x16_Noukiko.md, centered lyrics, and a vector Benin flag
plus DSKY badge immediately above the lyric block. It needs ffmpeg for the
final MP4; --dry-run prepares the ASS and cached frames without encoding.
"""
from __future__ import annotations

import argparse
import math
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "PLAN_9x16_Noukiko.md"
IMAGE_DIR = ROOT / "assets" / "raw" / "portrait"
DEFAULT_AUDIO = ROOT / "Noukiko tché wê.mp3"
DEFAULT_OUT = ROOT / "livrables" / "Noukiko_tche_we_9x16_v1.mp4"
FPS = 30
W, H = 1080, 1920

@dataclass(frozen=True)
class Row:
    start: float
    end: float
    text: str
    image: Path


def ass_time(seconds: float) -> str:
    cs = int(round(seconds * 100))
    h, rem = divmod(cs, 360000)
    m, rem = divmod(rem, 6000)
    s, c = divmod(rem, 100)
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"


def parse_plan() -> list[Row]:
    rows: list[Row] = []
    pattern = re.compile(
        r"^\|\s*\d+\s*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*(.*?)\s*\|\s*`([^`]+\.png)`\s*\|$"
    )
    for line in PLAN.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if not match:
            continue
        start, end = float(match.group(1)), float(match.group(2))
        text = match.group(3).replace("\\|", "|")
        image = IMAGE_DIR / match.group(4)
        if end <= start:
            raise ValueError(f"Invalid timing window: {line}")
        if not image.is_file():
            raise FileNotFoundError(image)
        rows.append(Row(start, end, text, image))
    if not rows:
        raise ValueError(f"No rows found in {PLAN}")
    return rows


def ass_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


def badge_events(row: Row) -> list[str]:
    """Return a vector flag, pill, and readable DSKY✓ text.

    The lyrics are centered at y=960. The badge baseline is computed from the
    estimated lyric sprite height, keeping the lock-up above the words rather
    than at the top of the frame.
    """
    line_count = max(1, math.ceil(len(row.text) / 28))
    lyric_top = H / 2 - (line_count * 84) / 2
    lock_bottom = int(lyric_top - 20)
    lock_h = 60
    lock_y = max(150, lock_bottom - lock_h)
    begin, end = ass_time(row.start), ass_time(row.end)
    fade = r"\fad(400,400)"
    # ASS drawing colors are BGR: green 518700, yellow 16D1FC, red 2D11E8.
    pill = (
        f"Dialogue: 0,{begin},{end},Badge,,0,0,0,,"
        f"{{\\an7\\pos(430,{lock_y})\\alpha&H40&\\p1\\bord2\\c&H0C0C12&}}"
        f"m 0 0 l 220 0 l 220 60 l 0 60{{\\p0}}"
    )
    flag_green = (
        f"Dialogue: 0,{begin},{end},Badge,,0,0,0,,"
        f"{{\\an7\\pos(445,{lock_y + 15}){fade}\\p1\\bord0\\c&H518700&}}"
        f"m 0 0 l 18 0 l 18 30 l 0 30{{\\p0}}"
    )
    flag_yellow = (
        f"Dialogue: 0,{begin},{end},Badge,,0,0,0,,"
        f"{{\\an7\\pos(463,{lock_y + 15}){fade}\\p1\\bord0\\c&H16D1FC&}}"
        f"m 0 0 l 27 0 l 27 15 l 0 15{{\\p0}}"
    )
    flag_red = (
        f"Dialogue: 0,{begin},{end},Badge,,0,0,0,,"
        f"{{\\an7\\pos(463,{lock_y + 30}){fade}\\p1\\bord0\\c&H2D11E8&}}"
        f"m 0 0 l 27 0 l 27 15 l 0 15{{\\p0}}"
    )
    label = (
        f"Dialogue: 0,{begin},{end},Badge,,0,0,0,,"
        + "{\\an4\\pos(486," + str(lock_y + 17) + ")" + fade + "}DSKY✓"
    )
    return [pill, flag_green, flag_yellow, flag_red, label]


def write_ass(rows: list[Row], path: Path) -> None:
    lines = [
        "[Script Info]", "ScriptType: v4.00+", "WrapStyle: 1",
        f"PlayResX: {W}", f"PlayResY: {H}", "ScaledBorderAndShadow: yes", "",
        "[V4+ Styles]",
        "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour, Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
        "Style: Lyric,DejaVu Sans,76,&H00F5F9FF,&H00F5F9FF,&H0005060A,&H8805060A,1,0,0,0,100,100,0,0,1,3,2,5,70,70,0,1",
        "Style: Badge,DejaVu Sans,40,&H00F5F9FF,&H00F5F9FF,&H0005060A,&H0005060A,1,0,0,0,100,100,0,0,1,1,1,4,0,0,0,1", "",
        "[Events]", "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text",
    ]
    for row in rows:
        begin, end = ass_time(row.start), ass_time(row.end)
        text = ass_escape(row.text)
        lines.append(
            f"Dialogue: 0,{begin},{end},Lyric,,0,0,0,,{{\\an5\\pos(540,960)\\fad(80,120)}}{text}"
        )
        lines.extend(badge_events(row))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def prepare_images(rows: list[Row], cache: Path) -> dict[Path, bytes]:
    cache.mkdir(parents=True, exist_ok=True)
    unique = {row.image for row in rows}
    output: dict[Path, bytes] = {}
    for source in unique:
        target = cache / (source.stem + ".jpg")
        if not target.exists():
            subprocess.run([
                "convert", str(source), "-resize", f"{W}x{H}^", "-gravity", "center",
                "-extent", f"{W}x{H}", "-sampling-factor", "4:2:0", "-quality", "92", str(target)
            ], check=True)
        output[source] = target.read_bytes()
    return output


def get_ffmpeg() -> str:
    system = shutil.which("ffmpeg")
    if system:
        return system
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as exc:
        raise RuntimeError("ffmpeg is unavailable; install imageio-ffmpeg or system ffmpeg") from exc


def audio_duration(audio: Path, ffmpeg: str) -> float:
    """Read duration through ffmpeg itself; ffprobe is not required."""
    proc = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", str(audio), "-f", "null", "-"],
        text=True, capture_output=True, check=False,
    )
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", proc.stderr)
    if not match:
        raise RuntimeError(f"Could not read audio duration from ffmpeg for {audio}")
    hours, minutes, seconds = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def render(rows: list[Row], frames: dict[Path, bytes], ass: Path, audio: Path, out: Path, duration: float, ffmpeg: str) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        ffmpeg, "-y", "-f", "image2pipe", "-vcodec", "mjpeg", "-framerate", str(FPS), "-i", "pipe:0",
        "-i", str(audio), "-filter_complex", f"[0:v]ass={ass},format=yuv420p[v];[1:a]afade=t=in:st=0:d=0.3,afade=t=out:st={max(0.0, duration - 3.0):.3f}:d=3[a]",
        "-map", "[v]", "-map", "[a]", "-t", f"{duration:.3f}", "-r", str(FPS), "-c:v", "libx264", "-preset", "medium",
        "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
        "-movflags", "+faststart", str(out),
    ]
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert process.stdin is not None
    total = math.ceil(duration * FPS)
    for index in range(total):
        t = index / FPS
        row = next((item for item in rows if item.start <= t < item.end), rows[-1])
        process.stdin.write(frames[row.image])
    process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError("ffmpeg failed while encoding the 9:16 render")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="prepare ASS and cached 1080x1920 frames only")
    parser.add_argument("--audio", type=Path, default=DEFAULT_AUDIO)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    rows = parse_plan()
    ffmpeg = get_ffmpeg()
    duration = audio_duration(args.audio, ffmpeg)
    work = ROOT / "work" / "noukiko_9x16"
    ass = work / "Noukiko_9x16.ass"
    write_ass(rows, ass)
    frames = prepare_images(rows, work / "prep")
    print(f"Audio duration from ffmpeg: {duration:.3f}s")
    print(f"Prepared {len(frames)} unique 1080x1920 backgrounds")
    print(f"Prepared ASS subtitles and vector Benin lock-up: {ass}")
    if args.dry_run:
        return 0
    render(rows, frames, ass, args.audio, args.out, duration, ffmpeg)
    print(f"Rendered {args.out}")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
