#!/usr/bin/env python3
"""Grade the 3 artist photos. Face geometry is never rebuilt — only
uniform color grade + Snapchat-heart inpaint in the top-right sticker zone."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "photos-originales"
RAW = ROOT / "assets" / "raw" / "portrait"
FONDS = ROOT / "work" / "fonds_9x16"
CANVAS_W, CANVAS_H = 1188, 2112
OUT_W, OUT_H = 1080, 1920


def heart_mask(arr: np.ndarray) -> np.ndarray:
    """Hearts live in a thin top-right sticker strip, always ABOVE the head."""
    h, w = arr.shape[:2]
    y0, y1 = int(h * 0.10), int(h * 0.28)
    x0, x1 = int(w * 0.58), w
    roi = arr[y0:y1, x0:x1]
    r = roi[:, :, 0].astype(np.int16)
    g = roi[:, :, 1].astype(np.int16)
    b = roi[:, :, 2].astype(np.int16)
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    sat = mx - mn
    colored = (sat > 40) & (mx > 90)
    mask_roi = colored
    full = np.zeros((h, w), dtype=bool)
    full[y0:y1, x0:x1] = mask_roi
    mimg = Image.fromarray(full.astype(np.uint8) * 255)
    mimg = mimg.filter(ImageFilter.MaxFilter(21))
    mimg = mimg.filter(ImageFilter.MaxFilter(11))
    full = np.array(mimg) > 0
    # never touch below 30% of the frame (face lives there)
    full[int(h * 0.30) :, :] = False
    return full


def inpaint(arr: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Fill the whole heart row from a sample ABOVE/LEFT of the cluster —
    never copy from a neighbouring heart."""
    out = arr.copy()
    h, w = arr.shape[:2]
    # Always clear the canonical Snapchat heart strip (even if detect is weak)
    y0, y1 = int(h * 0.135), int(h * 0.255)
    x0, x1 = int(w * 0.62), int(w * 0.97)
    if mask.any():
        ys, xs = np.where(mask)
        y0 = min(y0, max(0, ys.min() - 10))
        y1 = max(y1, min(h, ys.max() + 10))
        x0 = min(x0, max(0, xs.min() - 10))
        x1 = max(x1, min(w, xs.max() + 10))
    y0 = max(0, y0)
    y1 = min(int(h * 0.29), y1)
    x0 = max(int(w * 0.55), x0)
    box = np.zeros((h, w), dtype=bool)
    box[y0:y1, x0:x1] = True
    # sample a strip of the same material just LEFT of the whole row
    sx1 = max(0, x0 - 8)
    sx0 = max(0, x0 - 70)
    sample = arr[y0:y1, sx0:sx1]
    if sample.size == 0:
        sample = arr[max(0, y0 - 24) : y0, x0:x1]
    if sample.size == 0:
        return out
    med = np.median(sample.reshape(-1, 3), axis=0)
    # tile the sample horizontally into the box
    sh, sw = sample.shape[:2]
    if sw < 4:
        fill = np.zeros((y1 - y0, x1 - x0, 3), dtype=np.uint8)
        fill[:, :] = med.astype(np.uint8)
    else:
        reps = int(np.ceil((x1 - x0) / sw))
        tiled = np.tile(sample, (1, reps, 1))[:, : x1 - x0, :]
        if tiled.shape[0] != (y1 - y0):
            tiled = np.array(
                Image.fromarray(tiled).resize((x1 - x0, y1 - y0), Image.Resampling.BILINEAR)
            )
        # mix with median so it doesn't look like a repeated texture
        fill = (0.55 * tiled.astype(np.float32) + 0.45 * med).astype(np.uint8)
    out[y0:y1, x0:x1] = fill
    # feather the seam
    seam_mask = Image.fromarray(box.astype(np.uint8) * 255).filter(ImageFilter.GaussianBlur(4))
    alpha = np.array(seam_mask).astype(np.float32) / 255.0
    blurred = np.array(Image.fromarray(out).filter(ImageFilter.GaussianBlur(1.6)))
    a = alpha[:, :, None]
    mixed = out.astype(np.float32) * (1 - a * 0.65) + blurred.astype(np.float32) * (a * 0.65)
    # only apply mix inside/near the box
    near = alpha > 0.02
    out[near] = np.clip(mixed[near], 0, 255).astype(np.uint8)
    return out


def to_canvas(im: Image.Image) -> Image.Image:
    im = im.convert("RGB")
    w, h = im.size
    target_ratio = OUT_W / OUT_H
    ratio = w / h
    if abs(ratio - target_ratio) > 0.01:
        if ratio > target_ratio:
            nw = int(h * target_ratio)
            left = (w - nw) // 2
            im = im.crop((left, 0, left + nw, h))
        else:
            nh = int(w / target_ratio)
            top = (h - nh) // 6  # keep head (upper third)
            im = im.crop((0, top, w, min(h, top + nh)))
    im = im.resize((OUT_W, OUT_H), Image.Resampling.LANCZOS)
    canvas = im.resize((CANVAS_W, CANVAS_H), Image.Resampling.LANCZOS)
    return canvas


def s2_grade(arr: np.ndarray) -> np.ndarray:
    """Warm golden-hour grade, uniform — does not reshape the face."""
    x = arr.astype(np.float32)
    r, g, b = x[:, :, 0], x[:, :, 1], x[:, :, 2]
    r = r * 1.05 + 8
    g = g * 1.02 + 3
    b = b * 0.93 - 2
    x[:, :, 0], x[:, :, 1], x[:, :, 2] = r, g, b
    # soft S-curve
    x = x / 255.0
    x = np.clip(x, 0, 1)
    x = 0.08 + 0.92 * (x * x * (3 - 2 * x) * 0.35 + x * 0.65)
    x = np.clip(x * 255.0, 0, 255).astype(np.uint8)
    return x


def process_one(src: Path, stem: str) -> Path:
    im = Image.open(src).convert("RGB")
    arr = np.array(im)
    mask = heart_mask(arr)
    arr = inpaint(arr, mask)
    arr = s2_grade(arr)
    im = Image.fromarray(arr)
    canvas = to_canvas(im)
    RAW.mkdir(parents=True, exist_ok=True)
    FONDS.mkdir(parents=True, exist_ok=True)
    out_png = RAW / f"{stem}.jpg"
    out_fond = FONDS / f"{stem}.jpg"
    canvas.save(out_png, quality=95, subsampling=0)
    canvas.save(out_fond, quality=95, subsampling=0)
    print(f"{stem}: hearts={int(mask.mean()*1000)/10:.1f}‰  {canvas.size} → {out_png}")
    return out_png


def process_generated(src: Path, stem: str) -> Path:
    im = Image.open(src).convert("RGB")
    canvas = to_canvas(im)
    RAW.mkdir(parents=True, exist_ok=True)
    FONDS.mkdir(parents=True, exist_ok=True)
    out_png = RAW / f"{stem}.jpg"
    out_fond = FONDS / f"{stem}.jpg"
    canvas.save(out_png, quality=95, subsampling=0)
    canvas.save(out_fond, quality=95, subsampling=0)
    print(f"{stem}: generated {canvas.size} → {out_png}")
    return out_png


def main() -> None:
    process_one(SRC / "p01_tee.jpg", "s01_tee")
    process_one(SRC / "p02_vest.jpg", "s02_vest")
    process_one(SRC / "p03_seated.jpg", "s03_seated")
    process_generated(ROOT / "work" / "gen_intro.png", "s00_intro")
    process_generated(ROOT / "work" / "gen_instrumental.png", "s04_lagoon")
    process_generated(ROOT / "work" / "gen_endcard.png", "s05_endcard")
    # also a 9:16 cover plate from the still-life
    process_generated(ROOT / "work" / "gen_cover.png", "s06_coverplate")


if __name__ == "__main__":
    main()
