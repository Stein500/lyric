from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "mama-tche"
PORTRAIT = PROJECT / "assets" / "raw" / "9x16"
LANDSCAPE = PROJECT / "assets" / "raw" / "16x9"

W, H = 1920, 1080


def fit_cover(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    scale = max(target_w / img.width, target_h / img.height)
    new_size = (int(img.width * scale), int(img.height * scale))
    resized = img.resize(new_size, Image.Resampling.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def build_derivative(src: Path, dst: Path) -> None:
    img = Image.open(src).convert("RGB")
    bg = fit_cover(img, W, H).filter(ImageFilter.GaussianBlur(30))
    bg = ImageEnhance.Brightness(bg).enhance(0.72)
    bg = ImageEnhance.Color(bg).enhance(1.06)

    fg_h = H
    fg_w = int(img.width * (fg_h / img.height))
    fg = img.resize((fg_w, fg_h), Image.Resampling.LANCZOS)

    canvas = bg.convert("RGBA")
    shadow = Image.new("RGBA", (fg_w + 80, fg_h + 80), (0, 0, 0, 0))
    sh = Image.new("RGBA", (fg_w, fg_h), (0, 0, 0, 170))
    shadow.alpha_composite(sh, (40, 40))
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    canvas.alpha_composite(shadow, ((W - shadow.width) // 2, (H - shadow.height) // 2 + 10))

    # Soft feather on the vertical insert.
    mask = Image.linear_gradient("L").rotate(90, expand=True).resize((fg_w, fg_h))
    mask = ImageOps.autocontrast(mask)
    left_fade = mask.crop((0, 0, fg_w // 8, fg_h)).resize((fg_w // 8, fg_h))
    right_fade = left_fade.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    alpha = Image.new("L", (fg_w, fg_h), 255)
    alpha.paste(left_fade, (0, 0))
    alpha.paste(right_fade, (fg_w - right_fade.width, 0))

    fg_rgba = fg.convert("RGBA")
    fg_rgba.putalpha(alpha)
    canvas.alpha_composite(fg_rgba, ((W - fg_w) // 2, 0))

    # Bottom dark gradient to help future subtitles.
    gradient = Image.new("RGBA", (W, 280), (0, 0, 0, 0))
    px = gradient.load()
    for y in range(280):
        a = int(155 * (y / 279))
        for x in range(W):
            px[x, y] = (0, 0, 0, a)
    canvas.alpha_composite(gradient, (0, H - 280))

    dst.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(dst, quality=94)


def main() -> None:
    created = 0
    for src in sorted(PORTRAIT.glob("session*/*.png")):
        rel = src.relative_to(PORTRAIT)
        dst = LANDSCAPE / rel.parent / f"{src.stem}_16x9.jpg"
        if dst.exists():
            continue
        build_derivative(src, dst)
        created += 1
        print(f"Created {dst.relative_to(PROJECT)}")
    print(f"Done. Created {created} derivative landscape images.")


if __name__ == "__main__":
    main()
