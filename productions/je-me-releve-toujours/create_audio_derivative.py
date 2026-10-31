#!/usr/bin/env python3
"""Create the retagged/loudness-normalized derivative without touching the supplied master."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
from mutagen.id3 import APIC, COMM, ID3, TALB, TCON, TIT2, TPE1, TPE2, TRCK, TXXX, USLT, WOAS
from mutagen.mp3 import MP3
import imageio_ffmpeg

PROJECT = Path(__file__).resolve().parent
REPO = PROJECT.parents[1]
MASTER = REPO / "je me relève toujours 3.mp3"
LYRICS = REPO / "Je me relève toujours.txt"
DELIVERABLES = PROJECT / "livrables"
COVER = DELIVERABLES / "cover-dsky-1080.jpg"
OUTPUT = DELIVERABLES / "Je_me_releve_toujours_Dsky.mp3"
TITLE = "Je me relève toujours"
ARTIST = "Dsky"
SIGNATURE = "WTBW"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def create_cover() -> None:
    source = Image.open(PROJECT / "fonds/scene-31.png").convert("RGB")
    # Crop above the lyric line, then fit square so no fragment of painted text survives on the cover.
    square = ImageOps.fit(source.crop((0, 0, 768, 720)), (1080, 1080),
                          method=Image.Resampling.LANCZOS).convert("RGBA")
    overlay = Image.new("RGBA", square.size, (0, 0, 0, 0))
    pix = overlay.load()
    for y in range(680, 1080):
        a = int(205 * min(1.0, (y - 680) / 190))
        for x in range(1080):
            pix[x, y] = (4, 11, 18, a)
    square = Image.alpha_composite(square, overlay)
    draw = ImageDraw.Draw(square)
    serif_path = str(PROJECT / "fonts/DejaVuSerif-Bold.ttf")
    sans_path = str(PROJECT / "fonts/DejaVuSans-Bold.ttf")
    title_font = font(serif_path, 64)
    artist_font = font(sans_path, 43)
    title = TITLE
    box = draw.textbbox((0, 0), title, font=title_font, stroke_width=1)
    while box[2] - box[0] > 980 and title_font.size > 36:
        title_font = font(serif_path, title_font.size - 2)
        box = draw.textbbox((0, 0), title, font=title_font, stroke_width=1)
    x = (1080 - (box[2] - box[0])) // 2
    draw.text((x, 820), title, font=title_font, fill=(249, 237, 215, 255),
              stroke_width=2, stroke_fill=(4, 11, 18, 230))
    artist = ARTIST
    box = draw.textbbox((0, 0), artist, font=artist_font)
    x = (1080 - (box[2] - box[0])) // 2
    draw.text((x, 930), artist, font=artist_font, fill=(226, 175, 93, 255),
              stroke_width=1, stroke_fill=(4, 11, 18, 220))
    square.convert("RGB").save(COVER, "JPEG", quality=94, subsampling=0, optimize=True)


def read_lyrics() -> str:
    rows = []
    rx = re.compile(r"^\[(\d{2}):(\d{2})\.(\d{2})\](.*)$")
    for line in LYRICS.read_text(encoding="utf-8").splitlines():
        m = rx.match(line)
        if m:
            rows.append(m.group(4))
    return "\n".join(rows)


def first_pass(ffmpeg: str) -> dict[str, str]:
    cmd = [ffmpeg, "-hide_banner", "-nostats", "-i", str(MASTER), "-map", "0:a:0",
           "-af", "loudnorm=I=-14:TP=-2.0:LRA=11:print_format=json", "-f", "null", "-"]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    text = p.stderr
    end = text.rfind("}")
    start = text.rfind("{", 0, end)
    if start < 0 or end < 0:
        raise RuntimeError("Could not parse first-pass loudnorm JSON")
    metrics = json.loads(text[start:end + 1])
    return {k: str(metrics[k]) for k in ("input_i", "input_tp", "input_lra", "input_thresh", "target_offset")}


def build_audio(ffmpeg: str) -> dict[str, str]:
    source_tags = ID3(str(MASTER))
    source_sha = sha256(MASTER)
    source_comment = ""
    source_url = ""
    source_id = ""
    if "TXXX:comment" in source_tags:
        source_comment = str(source_tags["TXXX:comment"].text[0])
        m = re.search(r"id=([0-9a-f-]+)", source_comment, re.I)
        if m:
            source_id = m.group(1)
    if "WOAS" in source_tags:
        source_url = source_tags["WOAS"].url
    measurements = first_pass(ffmpeg)
    loudnorm = (
        # Extra 0.5 dB headroom anticipates inter-sample peaks introduced by the MP3/AAC encoders.
        "loudnorm=I=-14:TP=-2.0:LRA=11:"
        f"measured_I={measurements['input_i']}:"
        f"measured_TP={measurements['input_tp']}:"
        f"measured_LRA={measurements['input_lra']}:"
        f"measured_thresh={measurements['input_thresh']}:"
        f"offset={measurements['target_offset']}:linear=true:print_format=summary"
    )
    cmd = [ffmpeg, "-y", "-hide_banner", "-i", str(MASTER), "-map", "0:a:0", "-map_metadata", "-1",
           "-map_chapters", "-1", "-vn", "-af", loudnorm, "-ar", "48000", "-ac", "2",
           "-c:a", "libmp3lame", "-q:a", "0", "-id3v2_version", "4", "-write_id3v1", "0", str(OUTPUT)]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    clean_log = "\n".join(line.rstrip() for line in p.stderr.splitlines()) + "\n"
    (DELIVERABLES / "loudnorm-second-pass.txt").write_text(clean_log, encoding="utf-8")

    tags = ID3()
    tags.add(TIT2(encoding=3, text=[TITLE]))
    tags.add(TALB(encoding=3, text=[TITLE]))
    tags.add(TPE1(encoding=3, text=[ARTIST]))
    tags.add(TPE2(encoding=3, text=[ARTIST]))
    tags.add(TCON(encoding=3, text=["Hip-Hop/Rap"]))
    tags.add(TRCK(encoding=3, text=["1/1"]))
    tags.add(USLT(encoding=3, lang="fra", desc="Paroles", text=read_lyrics()))
    tags.add(TXXX(encoding=3, desc="SIGNATURE", text=[SIGNATURE]))
    tags.add(TXXX(encoding=3, desc="MASTER_SOURCE", text=[MASTER.name]))
    tags.add(TXXX(encoding=3, desc="MASTER_SHA256", text=[source_sha]))
    tags.add(TXXX(encoding=3, desc="IA_AUDIO", text=["OUI — audio généré avec Suno; master source fourni par l’artiste"]))
    if source_comment:
        tags.add(TXXX(encoding=3, desc="SUNO_SOURCE_COMMENT", text=[source_comment]))
    if source_id:
        tags.add(TXXX(encoding=3, desc="SUNO_TRACK_ID", text=[source_id]))
    if source_url:
        tags.add(WOAS(url=source_url))
        tags.add(TXXX(encoding=3, desc="SUNO_SOURCE_URL", text=[source_url]))
    # Preserve the exact Suno comment(s) from the source as well as the new explanatory note.
    for original_comment in source_tags.getall("COMM"):
        if any("suno" in str(part).lower() for part in original_comment.text):
            tags.add(COMM(encoding=3, lang=original_comment.lang, desc=original_comment.desc,
                          text=list(original_comment.text)))
    tags.add(COMM(encoding=3, lang="fra", desc="Provenance",
                  text=[f"Audio généré avec Suno. Master source non modifié; SHA-256 {source_sha}."]))
    cover_data = COVER.read_bytes()
    tags.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="Pochette", data=cover_data))
    tags.save(str(OUTPUT), v2_version=4)

    reread = MP3(str(OUTPUT))
    if abs(reread.info.sample_rate - 48000) > 0:
        raise RuntimeError(f"Unexpected output sample rate: {reread.info.sample_rate}")
    if reread.tags["TPE1"].text != [ARTIST] or reread.tags["TIT2"].text != [TITLE]:
        raise RuntimeError("ID3 title/artist verification failed")
    if "GEOB:c2pa manifest store" in reread.tags:
        raise RuntimeError("Stale master C2PA manifest unexpectedly copied into the derivative")
    if reread.tags["APIC:Pochette"].data != cover_data:
        raise RuntimeError("Cover verification failed")
    lyric_frames = reread.tags.getall("USLT")
    if len(lyric_frames) != 1 or lyric_frames[0].text != read_lyrics():
        raise RuntimeError("Clean lyric metadata verification failed")
    if sha256(MASTER) != source_sha:
        raise RuntimeError("The source master hash changed")
    return {
        "first_pass": measurements,
        "second_pass": clean_log[-2500:],
        "master_sha256": source_sha,
        "derivative_sha256": sha256(OUTPUT),
        "duration_mutagen_s": f"{reread.info.length:.3f}",
        "sample_rate": str(reread.info.sample_rate),
        "bitrate_bps": str(reread.info.bitrate),
        "file_bytes": str(OUTPUT.stat().st_size),
        "suno_source_url": source_url,
        "suno_track_id": source_id,
    }


def main() -> None:
    DELIVERABLES.mkdir(parents=True, exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    before = sha256(MASTER)
    create_cover()
    report = build_audio(ffmpeg)
    assert sha256(MASTER) == before
    report_path = DELIVERABLES / "audio-derivative-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
