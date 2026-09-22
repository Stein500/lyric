#!/usr/bin/env python3
"""Validate the Noukiko 9:16 lyric/image plan without external media packages."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "PLAN_9x16_Noukiko.md"
IMAGE_DIR = ROOT / "assets" / "raw" / "portrait"

text = PLAN.read_text(encoding="utf-8")
rows = re.findall(
    r"\|\s*\d+\s*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|.*?\|\s*`([^`]+\.png)`\s*\|",
    text,
)
if not rows:
    raise SystemExit("No lyric/image rows found")

previous = -1.0
missing = []
for start, end, image in rows:
    start, end = float(start), float(end)
    if start < previous:
        raise SystemExit(f"Non-monotonic timing at {start}")
    if end <= start:
        raise SystemExit(f"Invalid window {start} -> {end}")
    path = IMAGE_DIR / image
    if not path.is_file():
        missing.append(str(path))
    previous = start

if missing:
    raise SystemExit("Missing mapped images:\n" + "\n".join(missing))

print(f"OK: {len(rows)} timed lyric occurrences mapped")
print(f"OK: {len({image for _, _, image in rows})} distinct image files used")
print(f"OK: final provisional end = {float(rows[-1][1]):.2f}s")
