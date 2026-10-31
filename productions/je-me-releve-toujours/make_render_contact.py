#!/usr/bin/env python3
"""Extract a frame of each rendered lyric, then make contact sheets (QC only)."""
from __future__ import annotations

import json
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parent
VIDEO = ROOT / "livrables/Je_me_releve_toujours_9x16.mp4"
MAP = ROOT / "verses_map.json"
WORK = ROOT / "work/video_frames"
FPS = 30
THUMB_W = 480
FONT = ROOT / "fonts/DejaVuSans.ttf"


def main() -> None:
    rows = json.loads(MAP.read_text(encoding="utf-8"))
    if not VIDEO.exists() or len(rows) != 58:
        raise SystemExit("Missing video or verse map")
    selected = [{"label": "CARTE ACCUEIL", "t": 2.5, "kind": "extra"}]
    for r in rows:
        t = float(r["t"]) + min(0.50, (float(r["fin"]) - float(r["t"])) * 0.4)
        selected.append({"label": f"VERS {r['i']:02d}  {r['source_timestamp']}",
                         "t": t, "kind": "verse", "i": r["i"]})
    selected.extend([
        {"label": "CLOCHETTE 03:30", "t": 210.0, "kind": "extra"},
        {"label": "CARTE FINALE", "t": 232.0, "kind": "extra"},
    ])
    for item in selected:
        item["frame"] = math.ceil(item["t"] * FPS - 1e-9)
    selected.sort(key=lambda x: x["frame"])
    if len({it["frame"] for it in selected}) != len(selected):
        raise ValueError("Two sample times selected the same frame")
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    expression = "+".join(f"eq(n,{item['frame']})" for item in selected)
    vf = f"select='{expression}',scale={THUMB_W}:-2:flags=lanczos"
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", str(VIDEO),
           "-map", "0:v:0", "-vf", vf, "-fps_mode", "vfr", "-q:v", "2",
           "-start_number", "0", str(WORK / "frame-%03d.jpg")]
    subprocess.run(cmd, check=True)
    for idx, item in enumerate(selected):
        item["image"] = str(WORK / f"frame-{idx:03d}.jpg")
        if not Path(item["image"]).exists():
            raise RuntimeError(f"Frame {item['frame']} was not extracted")

    f = ImageFont.truetype(str(FONT), 21)
    def sheet(items: list[dict], name: str, columns: int = 2) -> None:
        sample = Image.open(items[0]["image"])
        tile_h = sample.height + 36
        canvas = Image.new("RGB", (columns * THUMB_W, math.ceil(len(items) / columns) * tile_h), (15, 20, 26))
        d = ImageDraw.Draw(canvas)
        for j, item in enumerate(items):
            x, y = (j % columns) * THUMB_W, (j // columns) * tile_h
            d.text((x + 9, y + 7), item["label"], font=f, fill=(244, 224, 190))
            canvas.paste(Image.open(item["image"]).convert("RGB"), (x, y + 36))
        canvas.save(ROOT / name, "JPEG", quality=78, optimize=True, progressive=True)

    verses = [it for it in selected if it["kind"] == "verse"]
    for batch in range(math.ceil(len(verses) / 10)):
        sheet(verses[batch * 10:(batch + 1) * 10], f"CONTROLE-rendu-{batch+1:02d}.jpg")
    extras = [it for it in selected if it["kind"] == "extra"]
    sheet(extras, "CONTROLE-rendu-cartes-clochette.jpg", 3)
    (WORK / "extractions.json").write_text(json.dumps(selected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Extracted {len(selected)} actual video frames: 58 verses + intro, CTA and final card.")


if __name__ == "__main__":
    main()
