from __future__ import annotations

import json
from pathlib import Path

import render_video as base
from mama_tche_bilingual import build_ass_text, get_bilingual_cues

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "mama-tche"
SRC_DIR = PROJECT / "src"
OUT_DIR = PROJECT / "livrables"


def build_manifest(segments) -> dict:
    cues = get_bilingual_cues()
    return {
        "title": base.TITLE,
        "artist": base.ARTIST,
        "audio": base.AUDIO.name,
        "duration": base.VIDEO_DURATION,
        "format": "9x16",
        "subtitle_mode": "original_plus_french_when_available",
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
                "debut": cue.start,
                "fin": cue.end,
                "original": cue.original,
                "traduction_fr": cue.french,
                "style": cue.style,
                "section": cue.section,
            }
            for cue in cues
        ],
    }


def write_ass_translated(dest: Path) -> None:
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {base.WIDTH}
PlayResY: {base.HEIGHT}
ScaledBorderAndShadow: yes
WrapStyle: 2
YCbCr Matrix: TV.601

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: IntroSerif,DejaVu Serif,54,&H00F8F2E7,&H000000FF,&H002A714C,&H65000000,1,1,0,0,100,100,0.3,0,1,3.6,1.3,2,110,110,380,1
Style: IntroSerifFr,DejaVu Sans,36,&H00F6E6C8,&H000000FF,&H00145A3B,&H62000000,0,1,0,0,100,100,0.2,0,1,2.8,0.8,2,110,110,380,1
Style: VerseMono,DejaVu Serif,52,&H00F8F2E7,&H000000FF,&H00145A3B,&H62000000,1,0,0,0,100,100,0.2,0,1,3.6,1.3,2,90,90,370,1
Style: VerseMonoFr,DejaVu Sans,35,&H00F8EEDC,&H000000FF,&H00145A3B,&H62000000,0,1,0,0,100,100,0.15,0,1,2.7,0.8,2,90,90,370,1
Style: VerseSans,DejaVu Sans,50,&H00F8F2E7,&H000000FF,&H00145A3B,&H62000000,1,0,0,0,100,100,0.3,0,1,3.4,1.2,2,90,90,370,1
Style: VerseSansFr,DejaVu Serif,35,&H00F8EEDC,&H000000FF,&H00145A3B,&H62000000,0,1,0,0,100,100,0.15,0,1,2.7,0.8,2,90,90,370,1
Style: RefrainGold,DejaVu Sans,60,&H00F4C95D,&H000000FF,&H00145A3B,&H68000000,1,0,0,0,100,100,0.8,0,1,4.2,1.5,2,86,86,390,1
Style: RefrainGoldFr,DejaVu Serif,38,&H00F8F2E7,&H000000FF,&H00145A3B,&H65000000,1,1,0,0,100,100,0.2,0,1,3.0,0.9,2,86,86,390,1
Style: FinalRefrainGold,DejaVu Sans,66,&H00F4C95D,&H000000FF,&H00145A3B,&H6E000000,1,0,0,0,100,100,1.0,0,1,4.4,1.7,2,82,82,400,1
Style: FinalRefrainGoldFr,DejaVu Serif,40,&H00F8F2E7,&H000000FF,&H00145A3B,&H68000000,1,1,0,0,100,100,0.2,0,1,3.1,0.9,2,82,82,400,1
Style: BridgeSerifCenter,DejaVu Serif,58,&H00F8F2E7,&H000000FF,&H002A714C,&H68000000,1,1,0,0,100,100,0.4,0,1,3.8,1.3,5,110,110,0,1
Style: BridgeSerifCenterFr,DejaVu Sans,38,&H00F8EEDC,&H000000FF,&H00145A3B,&H64000000,0,1,0,0,100,100,0.15,0,1,2.8,0.8,5,110,110,0,1
Style: HookGold,DejaVu Sans,64,&H00F4C95D,&H000000FF,&H00145A3B,&H70000000,1,0,0,0,100,100,1.2,0,1,4.4,1.6,2,94,94,390,1
Style: HookGoldFr,DejaVu Serif,38,&H00F8F2E7,&H000000FF,&H00145A3B,&H68000000,1,1,0,0,100,100,0.2,0,1,3.0,0.9,2,94,94,390,1
Style: OutroSerif,DejaVu Serif,52,&H00F8F2E7,&H000000FF,&H002A714C,&H68000000,1,1,0,0,100,100,0.3,0,1,3.8,1.3,2,100,100,390,1
Style: OutroSerifFr,DejaVu Sans,34,&H00F8EEDC,&H000000FF,&H00145A3B,&H64000000,0,1,0,0,100,100,0.15,0,1,2.7,0.8,2,100,100,390,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for cue in get_bilingual_cues():
        text = build_ass_text(cue, width_main=34, width_fr=38)
        lines.append(
            f"Dialogue: 0,{base.ass_time(cue.start)},{base.ass_time(cue.end)},{cue.style},,0,0,0,,{{\\fad(140,140)}}{text}"
        )
    dest.write_text(ass + "\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    segments = base.build_segments()
    manifest_path = SRC_DIR / "manifest_trad.json"
    ass_path = SRC_DIR / "mama_tche_subtitles_trad.ass"
    bg_video = OUT_DIR / "Mama_tche_Daïsky_Lyrics_9x16_TRAD_bg.mp4"
    final_video = OUT_DIR / "Mama_tche_Daïsky_Lyrics_9x16_TRAD.mp4"

    manifest_path.write_text(json.dumps(build_manifest(segments), indent=2, ensure_ascii=False), encoding="utf-8")
    write_ass_translated(ass_path)
    base.render_silent_video(segments, bg_video)
    base.burn_subtitles_and_audio(bg_video, ass_path, final_video)
    if bg_video.exists():
        bg_video.unlink()
    print(f"Done: {final_video}")


if __name__ == "__main__":
    main()
