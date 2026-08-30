#!/usr/bin/env python3
"""Create a transparent end-screen/contact overlay for Daïsky lyric videos."""
from __future__ import annotations

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PHONES = "+229 01 61 16 24 08 / +229 01 49 11 49 51"
EMAILS = [
    "daiskypro@proton.me",
    "daiskyproduction@gmail.com",
    "techsteinsecureway@gmail.com",
]


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def centered(draw: ImageDraw.ImageDraw, xy, text, fnt, fill, stroke_width=0, stroke_fill=(0, 0, 0, 255)):
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke_width)
    w = bbox[2] - bbox[0]
    draw.text((x - w / 2, y), text, font=fnt, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--title", default="CONTACT / BOOKING")
    parser.add_argument("--genre", default="Heavy Metal / Rock")
    parser.add_argument("--year", default="2026")
    parser.add_argument("--font-script", type=Path, default=Path("assets/fonts/Pacifico-Regular.ttf"))
    parser.add_argument("--font-text", type=Path, default=Path("assets/fonts/GreatVibes-Regular.ttf"))
    args = parser.parse_args()

    W, H = args.width, args.height
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)

    # Contact panel at the end of the video: large, readable, static.
    margin = int(W * 0.075)
    panel_h = int(H * 0.37) if H > W else int(H * 0.58)
    panel_y = int(H * 0.56) if H > W else int(H * 0.31)
    radius = int(W * 0.035)
    panel = (margin, panel_y, W - margin, min(H - margin, panel_y + panel_h))

    for expand, alpha in [(26, 38), (12, 70)]:
        p = (panel[0] - expand, panel[1] - expand, panel[2] + expand, panel[3] + expand)
        g.rounded_rectangle(p, radius + expand, fill=(232, 163, 61, alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    img.alpha_composite(glow)

    d = ImageDraw.Draw(img)
    d.rounded_rectangle(panel, radius, fill=(5, 6, 10, 205), outline=(232, 163, 61, 235), width=max(3, W // 220))

    pacifico = args.font_script
    great = args.font_text
    title_font = font(pacifico, int(W * (0.060 if H > W else 0.043)))
    head_font = font(pacifico, int(W * (0.040 if H > W else 0.029)))
    text_font = font(pacifico, int(W * (0.032 if H > W else 0.023)))
    small_font = font(pacifico, int(W * (0.027 if H > W else 0.020)))

    cyan = (77, 210, 255, 255)
    amber = (232, 163, 61, 255)
    white = (245, 249, 255, 255)

    center_x = W / 2
    y = panel[1] + int(panel_h * 0.08)
    line = int(panel_h * 0.115)
    centered(d, (center_x, y), args.title, title_font, amber, 3)
    y += line
    centered(d, (center_x, y), "Techstein · Daïsky Prod · Daïsky", head_font, white, 3)
    y += int(line * 0.90)
    centered(d, (center_x, y), f"Genre : {args.genre}   •   Année : {args.year}", small_font, cyan, 2)
    y += int(line * 0.92)
    centered(d, (center_x, y), f"Tél. : {PHONES}", small_font, white, 2)
    y += int(line * 0.90)
    for email in EMAILS:
        centered(d, (center_x, y), email, text_font, white, 2)
        y += int(line * 0.78)
    centered(d, (center_x, y + int(line * 0.08)), "@daiskypro", head_font, amber, 3)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    img.save(args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
