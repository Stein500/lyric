#!/usr/bin/env python3
"""9:16 lyric clip — Ken Burns + water-wave cursive + crossfades.
Artist face is never generated: plates are the 3 graded photos + empty atmospheres.
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work"
ASSETS = ROOT / "assets"
LIV = ROOT / "livrables"
FONDS = WORK / "fonds_9x16"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 1080, 1920
CW, CH = 1188, 2112
FPS = 24
ADVANCE = 0.03
XFADE = 0.55

CREAM = (255, 246, 232, 255)
GOLD = (240, 193, 90, 255)
GOLD_DEEP = (232, 163, 61, 255)
INK = (18, 8, 2, 255)
UI = (255, 236, 210, 255)


def load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    p = ASSETS / "fonts" / name
    return ImageFont.truetype(str(p), size)


FONT_LYRIC = None
FONT_LYRIC_SM = None
FONT_TITLE = None
FONT_UI = None
FONT_UI_SM = None
FONT_UI_LG = None


def init_fonts() -> None:
    global FONT_LYRIC, FONT_LYRIC_SM, FONT_TITLE, FONT_UI, FONT_UI_SM, FONT_UI_LG
    FONT_LYRIC = load_font("GreatVibes-Regular.ttf", 86)
    FONT_LYRIC_SM = load_font("GreatVibes-Regular.ttf", 72)
    FONT_TITLE = load_font("GreatVibes-Regular.ttf", 118)
    FONT_UI = load_font("DejaVuSans-Bold.ttf", 40)
    FONT_UI_SM = load_font("DejaVuSans-Bold.ttf", 28)
    FONT_UI_LG = load_font("DejaVuSans-Bold.ttf", 32)


def load_plate(stem: str) -> np.ndarray:
    p = FONDS / f"{stem}.jpg"
    im = Image.open(p).convert("RGB")
    if im.size != (CW, CH):
        im = im.resize((CW, CH), Image.Resampling.LANCZOS)
    return np.array(im)


def ken_burns(plate: np.ndarray, t: float, slot: int) -> np.ndarray:
    direction = 1 if slot % 2 == 0 else -1
    z0, z1 = (1.02, 1.085) if direction == 1 else (1.085, 1.02)
    u = 0.5 + 0.5 * math.sin(t * 0.11 + slot * 1.37)
    zoom = z0 + (z1 - z0) * u
    crop_w = int(round(W * (CW / W) / zoom * (W / 1080)))
    # Keep 9:16 crop inside canvas
    crop_w = int(round(CW / zoom))
    crop_h = int(round(crop_w * 16 / 9))
    if crop_h > CH:
        crop_h = CH
        crop_w = int(round(crop_h * 9 / 16))
    crop_w = min(crop_w, CW)
    crop_h = min(crop_h, CH)
    max_x = max(0, CW - crop_w)
    max_y = max(0, CH - crop_h)
    pan_x = 0.5 + 0.40 * math.sin(t * 0.23 + slot * 0.9)
    pan_y = 0.5 + 0.28 * math.sin(t * 0.17 + slot * 0.6 + 1.1)
    x = int(np.clip(pan_x, 0, 1) * max_x)
    y = int(np.clip(pan_y, 0, 1) * max_y)
    crop = plate[y : y + crop_h, x : x + crop_w]
    im = Image.fromarray(crop).resize((W, H), Image.Resampling.BILINEAR)
    return np.array(im)


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    dummy = ImageDraw.Draw(Image.new("L", (4, 4)))
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        bbox = dummy.textbbox((0, 0), trial, font=font)
        if bbox[2] - bbox[0] <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [text]


def fit_font(text: str) -> ImageFont.FreeTypeFont:
    dummy = ImageDraw.Draw(Image.new("L", (4, 4)))
    bbox = dummy.textbbox((0, 0), text, font=FONT_LYRIC)
    if bbox[2] - bbox[0] <= 860 or len(wrap_text(text, FONT_LYRIC, 860)) <= 2:
        return FONT_LYRIC
    return FONT_LYRIC_SM


def render_line_rgba(text: str, font: ImageFont.FreeTypeFont, fill: tuple) -> np.ndarray:
    dummy = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    bbox = dummy.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = 18
    im = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ox, oy = pad - bbox[0], pad - bbox[1]
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2), (-2, 2), (2, -2)):
        d.text((ox + dx, oy + dy), text, font=font, fill=INK)
    d.text((ox, oy), text, font=font, fill=fill)
    glow = im.filter(ImageFilter.GaussianBlur(3.5))
    base = Image.new("RGBA", im.size, (0, 0, 0, 0))
    gold_glow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(gold_glow)
    gd.text((ox, oy), text, font=font, fill=(240, 180, 70, 90))
    gold_glow = gold_glow.filter(ImageFilter.GaussianBlur(6))
    base = Image.alpha_composite(base, gold_glow)
    base = Image.alpha_composite(base, glow)
    base = Image.alpha_composite(base, im)
    return np.array(base)


def wave_line(src: np.ndarray, t: float, local: float, dur: float) -> np.ndarray:
    h, w = src.shape[:2]
    pad = 10
    dst = np.zeros((h + 2 * pad, w, 4), dtype=np.uint8)
    xs = np.arange(w, dtype=np.float64)
    yoff = (4.5 * np.sin(2 * math.pi * 0.9 * t + xs / 28.0)).astype(np.int32)
    appear = 0.90
    if dur < 2.0:
        appear = max(0.35, dur * 0.35)
    if local < appear:
        reveal = max(0.0, min(1.0, local / appear))
        edge = reveal * w
        mode = "in"
    elif local > dur - appear:
        reveal = max(0.0, min(1.0, (dur - local) / appear))
        edge = reveal * w
        mode = "out"  # reverse cascade: hide from the right
    else:
        edge = float(w)
        mode = "full"
        reveal = 1.0
    feather = 36.0
    for x in range(w):
        if mode == "in":
            a = np.clip((edge - x) / feather, 0.0, 1.0)
        elif mode == "out":
            a = np.clip((edge - (w - 1 - x)) / feather, 0.0, 1.0)
        else:
            a = 1.0
        if a <= 0:
            continue
        yo = int(yoff[x])
        col = src[:, x, :].astype(np.float32)
        col[:, 3] *= a
        dst[pad + yo : pad + yo + h, x, :] = np.clip(col, 0, 255).astype(np.uint8)
    return dst


class LineCache:
    def __init__(self) -> None:
        self.cache: dict[tuple, np.ndarray] = {}

    def get(self, text: str, kind: str) -> list[np.ndarray]:
        key = (text, kind)
        if key in self.cache:
            return self.cache[key]
        fill = GOLD if kind in ("hook", "sig", "outro") else CREAM
        font = fit_font(text)
        lines = wrap_text(text, font, 860)
        imgs = [render_line_rgba(ln, font, fill) for ln in lines]
        self.cache[key] = imgs
        return imgs


def make_scrim() -> np.ndarray:
    scrim = np.zeros((H, W, 4), dtype=np.uint8)
    cy = H // 2
    band = 270
    ys = np.arange(H)
    d = np.abs(ys - cy).astype(np.float64)
    a = np.where(d < band, 118.0 * (1.0 - (d / band) ** 1.35), 0.0)
    scrim[:, :, 0] = 22
    scrim[:, :, 1] = 10
    scrim[:, :, 2] = 4
    scrim[:, :, 3] = a.astype(np.uint8)[:, None]
    return scrim


def alpha_over(bg: np.ndarray, fg: np.ndarray, x: int, y: int) -> np.ndarray:
    fh, fw = fg.shape[:2]
    if fg.shape[2] == 3:
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(W, x + fw), min(H, y + fh)
        if x1 <= x0 or y1 <= y0:
            return bg
        bg[y0:y1, x0:x1] = fg[y0 - y : y1 - y, x0 - x : x1 - x]
        return bg
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + fw), min(H, y + fh)
    if x1 <= x0 or y1 <= y0:
        return bg
    f = fg[y0 - y : y1 - y, x0 - x : x1 - x].astype(np.float32)
    a = f[:, :, 3:4] / 255.0
    sl = bg[y0:y1, x0:x1].astype(np.float32)
    bg[y0:y1, x0:x1] = np.clip(sl * (1 - a) + f[:, :, :3] * a, 0, 255).astype(np.uint8)
    return bg


def draw_badge(frame: np.ndarray, alpha: float) -> np.ndarray:
    if alpha <= 0.01:
        return frame
    text = "DSKY✓"
    im = Image.new("RGBA", (280, 70), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    bbox = d.textbbox((0, 0), text, font=FONT_UI)
    tw = bbox[2] - bbox[0]
    d.text(((280 - tw) // 2, 12), text, font=FONT_UI, fill=(240, 193, 90, int(255 * min(alpha, 0.75))))
    arr = np.array(im)
    x = (W - 280) // 2
    return alpha_over(frame, arr, x, 130)


def draw_lyrics(frame: np.ndarray, imgs: list[np.ndarray], t: float, local: float, dur: float) -> np.ndarray:
    waved = [wave_line(im, t, local, dur) for im in imgs]
    total_h = sum(w.shape[0] for w in waved) + 8 * (len(waved) - 1)
    y = H // 2 - total_h // 2
    for wimg in waved:
        x = (W - wimg.shape[1]) // 2
        frame = alpha_over(frame, wimg, x, y)
        y += wimg.shape[0] + 8
    return frame


def draw_endcard(frame: np.ndarray, t_local: float, cfg: dict) -> np.ndarray:
    # fade in 0.6s
    a = min(1.0, t_local / 0.6)
    title = "Le goût bon de la vie"
    artist = "Daïsky"
    lines_ui = [
        cfg["contacts"]["whatsapp"][0],
        cfg["contacts"]["whatsapp"][1],
        cfg["contacts"]["email"],
    ]
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    # title
    bbox = d.textbbox((0, 0), title, font=FONT_TITLE)
    tw = bbox[2] - bbox[0]
    tx = (W - tw) // 2
    ty = int(H * 0.30)
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
        d.text((tx + dx, ty + dy), title, font=FONT_TITLE, fill=(18, 8, 2, int(255 * a)))
    d.text((tx, ty), title, font=FONT_TITLE, fill=(240, 193, 90, int(255 * a)))
    bbox2 = d.textbbox((0, 0), artist, font=FONT_UI_LG)
    tw2 = bbox2[2] - bbox2[0]
    d.text(((W - tw2) // 2, ty + 140), artist, font=FONT_UI_LG, fill=(255, 236, 210, int(230 * a)))
    yy = int(H * 0.52)
    for ln in lines_ui:
        bb = d.textbbox((0, 0), ln, font=FONT_UI_SM)
        twl = bb[2] - bb[0]
        d.text(((W - twl) // 2, yy), ln, font=FONT_UI_SM, fill=(255, 236, 210, int(210 * a)))
        yy += 44
    badge = "DSKY✓"
    bb = d.textbbox((0, 0), badge, font=FONT_UI)
    twb = bb[2] - bb[0]
    d.text(((W - twb) // 2, yy + 24), badge, font=FONT_UI, fill=(240, 193, 90, int(180 * a)))
    return alpha_over(frame, np.array(overlay), 0, 0)


def draw_hook_title(frame: np.ndarray, t: float) -> np.ndarray:
    # first 2.2s of cold-open: big title
    if t > 2.4:
        fade = max(0.0, 1.0 - (t - 2.4) / 0.5)
    else:
        fade = min(1.0, t / 0.45)
    if fade <= 0:
        return frame
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    title = "Le goût bon de la vie"
    bbox = d.textbbox((0, 0), title, font=FONT_TITLE)
    tw = bbox[2] - bbox[0]
    tx = (W - tw) // 2
    ty = 300
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
        d.text((tx + dx, ty + dy), title, font=FONT_TITLE, fill=(18, 8, 2, int(255 * fade)))
    d.text((tx, ty), title, font=FONT_TITLE, fill=(240, 193, 90, int(255 * fade)))
    art = "Daïsky"
    bb = d.textbbox((0, 0), art, font=FONT_UI_LG)
    d.text(((W - (bb[2] - bb[0])) // 2, ty + 140), art, font=FONT_UI_LG, fill=(255, 236, 210, int(230 * fade)))
    return alpha_over(frame, np.array(overlay), 0, 0)


def slot_index(stem: str) -> int:
    order = ["s00_intro", "s01_tee", "s02_vest", "s03_seated", "s04_lagoon", "s05_endcard", "s06_coverplate"]
    return order.index(stem) if stem in order else 1


def active_photo(t_music: float, verses: list, instrumentals: list, default: str) -> str:
    for v in verses:
        if v["start"] - 0.15 <= t_music < v["end"] + 0.12:
            return v["photo"]
    for ins in instrumentals:
        if ins["start"] <= t_music < ins["end"]:
            return ins["photo"]
    return default


def active_verse(t_music: float, verses: list):
    for v in verses:
        if v["start"] - ADVANCE <= t_music < v["end"]:
            return v
    return None


def prepare_audio(cfg: dict) -> Path:
    src = ROOT / "Le goût bon de la vie.mp3"
    song_wav = WORK / "song.wav"
    song_ln = WORK / "song_ln.wav"
    hook_wav = WORK / "hook.wav"
    full_wav = WORK / "full.wav"
    WORK.mkdir(exist_ok=True)

    def run(cmd):
        print("+", " ".join(cmd[:6]), "...")
        subprocess.check_call(cmd)

    run(
        [
            FFMPEG,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(src),
            "-map",
            "0:a:0",
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(song_wav),
        ]
    )
    ln = (
        "highpass=f=30,lowpass=f=18000,"
        "loudnorm=I=-14:TP=-1.8:LRA=11:"
        "measured_I=-14.46:measured_TP=0.01:measured_LRA=8.50:"
        "measured_thresh=-24.62:offset=-0.81:linear=true"
    )
    run(
        [
            FFMPEG,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(song_wav),
            "-af",
            ln,
            str(song_ln),
        ]
    )
    run(
        [
            FFMPEG,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(song_ln),
            "-ss",
            str(cfg["hook_src_start"]),
            "-t",
            str(cfg["hook"]),
            "-acodec",
            "pcm_s16le",
            str(hook_wav),
        ]
    )
    # concat hook + song, then pad 5s
    lst = WORK / "concat_audio.txt"
    # Use filter_complex concat of two wavs
    total_song = cfg["song_duration"]
    fade_st = cfg["hook"] + total_song + cfg["apad"] - 3.0
    filt = (
        f"[0:a]aformat=sample_fmts=s16:sample_rates=48000:channel_layouts=stereo[h];"
        f"[1:a]aformat=sample_fmts=s16:sample_rates=48000:channel_layouts=stereo,atrim=0:{total_song},asetpts=PTS-STARTPTS[s];"
        f"[h][s]concat=n=2:v=0:a=1,apad=pad_dur={cfg['apad']},"
        f"afade=t=out:st={fade_st}:d=3[a]"
    )
    run(
        [
            FFMPEG,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(hook_wav),
            "-i",
            str(song_ln),
            "-filter_complex",
            filt,
            "-map",
            "[a]",
            "-t",
            str(cfg["total"]),
            str(full_wav),
        ]
    )
    return full_wav


def render_video(cfg: dict, audio: Path) -> Path:
    init_fonts()
    plates = {
        stem: load_plate(stem)
        for stem in ["s00_intro", "s01_tee", "s02_vest", "s03_seated", "s04_lagoon", "s05_endcard"]
    }
    scrim = make_scrim()
    cache = LineCache()
    verses = cfg["verses"]
    hook_lines = cfg["hook_lines"]
    instrumentals = cfg["instrumentals"]
    nframes = cfg["nframes"]
    total = cfg["total"]
    hook = cfg["hook"]
    song_dur = cfg["song_duration"]
    out_mp4 = LIV / "Le_gout_bon_de_la_vie_9x16_v1.mp4"
    LIV.mkdir(exist_ok=True)

    cmd = [
        FFMPEG,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{W}x{H}",
        "-r",
        str(FPS),
        "-i",
        "pipe:0",
        "-i",
        str(audio),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "21",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-shortest",
        "-movflags",
        "+faststart",
        str(out_mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None

    prev_stem = "s01_tee"
    prev_frame = None
    fade_left = 0.0

    for i in range(nframes):
        t = i / FPS
        if t < hook:
            t_music = cfg["hook_src_start"] + t
            in_hook = True
            in_end = False
        else:
            t_music = t - hook
            in_hook = False
            in_end = t_music >= song_dur

        if in_end:
            stem = "s05_endcard"
        elif in_hook:
            # hook visual follows hook_lines photos
            stem = "s01_tee"
            for hl in hook_lines:
                if hl["start"] <= t < hl["end"]:
                    stem = hl["photo"]
                    break
        else:
            stem = active_photo(t_music, verses, instrumentals, "s01_tee")

        slot = slot_index(stem)
        kb_t = t_music if not in_hook else t
        frame = ken_burns(plates[stem], kb_t, slot)

        if stem != prev_stem and prev_frame is not None:
            fade_left = XFADE
            fade_from = prev_frame
        if fade_left > 0 and prev_frame is not None:
            u = fade_left / XFADE
            frame = (frame.astype(np.float32) * (1 - u) + fade_from.astype(np.float32) * u).astype(np.uint8)
            fade_left -= 1.0 / FPS
        prev_stem = stem
        prev_frame = frame

        # scrim + lyrics
        badge_a = 0.0
        if in_end:
            frame = draw_endcard(frame, t_music - song_dur, cfg)
            badge_a = 0.55
        elif in_hook:
            frame = draw_hook_title(frame, t)
            verse = None
            for hl in hook_lines:
                if hl["start"] <= t < hl["end"]:
                    verse = hl
                    break
            if verse and t > 0.3:
                frame = alpha_over(frame, scrim, 0, 0)
                imgs = cache.get(verse["text"], verse["kind"])
                local = t - verse["start"]
                dur = verse["end"] - verse["start"]
                frame = draw_lyrics(frame, imgs, t, local, dur)
                badge_a = min(0.75, local / 0.4, (dur - local) / 0.4)
        else:
            verse = active_verse(t_music, verses)
            if verse:
                frame = alpha_over(frame, scrim, 0, 0)
                imgs = cache.get(verse["text"], verse["kind"])
                local = (t_music + ADVANCE) - verse["start"]
                dur = verse["end"] - verse["start"]
                frame = draw_lyrics(frame, imgs, t, max(0.0, local), dur)
                badge_a = min(0.75, max(0.0, local) / 0.4, (dur - local) / 0.4)

        frame = draw_badge(frame, max(0.0, badge_a))

        # final 3s video fade
        if t > total - 3.0:
            fade = max(0.0, (total - t) / 3.0)
            frame = (frame.astype(np.float32) * fade).astype(np.uint8)

        if frame.dtype != np.uint8:
            frame = frame.astype(np.uint8)
        if not frame.flags["C_CONTIGUOUS"]:
            frame = np.ascontiguousarray(frame)
        proc.stdin.write(frame.tobytes())
        if i % 48 == 0:
            print(f"frame {i}/{nframes} t={t:.2f}s plate={stem}", flush=True)

    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise SystemExit(f"ffmpeg failed {rc}")
    print("wrote", out_mp4, "size", out_mp4.stat().st_size)
    return out_mp4


def make_covers() -> None:
    init_fonts()
    LIV.mkdir(exist_ok=True)
    src = Image.open(ROOT / "work" / "gen_cover.png").convert("RGB")

    def overlay_title(im: Image.Image, portrait: bool) -> Image.Image:
        im = im.convert("RGBA")
        dlayer = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(dlayer)
        w, h = im.size
        title = "Le goût bon de la vie"
        artist = "Daïsky"
        font_t = load_font("GreatVibes-Regular.ttf", 92 if not portrait else 100)
        font_a = load_font("DejaVuSans-Bold.ttf", 36 if not portrait else 34)
        font_b = load_font("DejaVuSans-Bold.ttf", 28)
        bbox = d.textbbox((0, 0), title, font=font_t)
        tw = bbox[2] - bbox[0]
        tx = (w - tw) // 2
        ty = int(h * (0.12 if portrait else 0.08))
        for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2)):
            d.text((tx + dx, ty + dy), title, font=font_t, fill=(20, 8, 0, 220))
        d.text((tx, ty), title, font=font_t, fill=(240, 193, 90, 255))
        bb = d.textbbox((0, 0), artist, font=font_a)
        d.text(((w - (bb[2] - bb[0])) // 2, ty + (110 if portrait else 100)), artist, font=font_a, fill=(255, 236, 210, 255))
        badge = "DSKY✓"
        bb = d.textbbox((0, 0), badge, font=font_b)
        d.text(((w - (bb[2] - bb[0])) // 2, h - 70), badge, font=font_b, fill=(240, 193, 90, 200))
        # Benin stripe
        bh = 10
        d.rectangle((0, h - bh, w // 3, h), fill=(0, 135, 81, 255))
        d.rectangle((w // 3, h - bh, 2 * w // 3, h), fill=(252, 209, 22, 255))
        d.rectangle((2 * w // 3, h - bh, w, h), fill=(232, 17, 45, 255))
        return Image.alpha_composite(im, dlayer).convert("RGB")

    sq = src.copy()
    # already square-ish
    side = min(sq.size)
    left = (sq.size[0] - side) // 2
    top = (sq.size[1] - side) // 2
    sq = sq.crop((left, top, left + side, top + side)).resize((1080, 1080), Image.Resampling.LANCZOS)
    sq = overlay_title(sq, portrait=False)
    sq_path = LIV / "cover_le_gout_bon_de_la_vie_1080x1080.jpg"
    sq.save(sq_path, quality=92, subsampling=0)

    # 9:16 cover from still life + extra canvas
    port = Image.new("RGB", (1080, 1920), (12, 6, 2))
    # fit cover into portrait keeping subject
    cw, ch = src.size
    scale = 1080 / cw
    nw, nh = 1080, int(ch * scale)
    fitted = src.resize((nw, nh), Image.Resampling.LANCZOS)
    yoff = (1920 - nh) // 2
    port.paste(fitted, (0, max(0, yoff)))
    if yoff < 0:
        port = fitted.crop((0, -yoff, 1080, -yoff + 1920))
    port = overlay_title(port, portrait=True)
    p_path = LIV / "cover_le_gout_bon_de_la_vie_9x16.jpg"
    port.save(p_path, quality=92, subsampling=0)
    print("covers", sq_path, p_path)


def make_master_mp3(cfg: dict) -> Path:
    src_wav = WORK / "song_ln.wav"
    out = LIV / "Le_gout_bon_de_la_vie_master_320k.mp3"
    cover = LIV / "cover_le_gout_bon_de_la_vie_1080x1080.jpg"
    tmp = WORK / "master_notags.mp3"
    subprocess.check_call(
        [
            FFMPEG,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(src_wav),
            "-map",
            "0:a:0",
            "-vn",
            "-t",
            str(cfg["song_duration"]),
            "-c:a",
            "libmp3lame",
            "-b:a",
            "320k",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(tmp),
        ]
    )
    from mutagen.id3 import (
        APIC,
        ID3,
        TALB,
        TCOM,
        TCON,
        TDRC,
        TIT2,
        TPE1,
        TPE2,
        TPUB,
        TXXX,
        USLT,
        ID3NoHeaderError,
    )

    try:
        tags = ID3(str(tmp))
    except ID3NoHeaderError:
        tags = ID3()
    tags.clear()
    tags["TIT2"] = TIT2(encoding=3, text=cfg["title"])
    tags["TPE1"] = TPE1(encoding=3, text=cfg["artist"])
    tags["TALB"] = TALB(encoding=3, text="Daïsky Prod")
    tags["TPE2"] = TPE2(encoding=3, text=cfg["artist"])
    tags["TPUB"] = TPUB(encoding=3, text="Daïsky Prod / TechStein")
    tags["TCOM"] = TCOM(encoding=3, text=cfg["artist"])
    tags["TCON"] = TCON(encoding=3, text="Afro-pop")
    tags["TDRC"] = TDRC(encoding=3, text="2026")
    tags.add(TXXX(encoding=3, desc="contact", text=" / ".join(cfg["contacts"]["whatsapp"])))
    tags.add(TXXX(encoding=3, desc="email", text=cfg["contacts"]["email"]))
    tags.add(TXXX(encoding=3, desc="producer", text="Daïsky"))
    tags.add(TXXX(encoding=3, desc="label", text="Daïsky Prod / TechStein"))
    lyrics = "\n".join(v["text"] for v in cfg["verses"])
    tags["USLT::fra"] = USLT(encoding=3, lang="fra", desc="Paroles", text=lyrics)
    if cover.exists():
        tags["APIC"] = APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="Cover",
            data=cover.read_bytes(),
        )
    tags.save(str(tmp), v2_version=4)
    Path(tmp).replace(out)
    print("master", out, out.stat().st_size)
    return out


def main() -> None:
    cfg = json.loads((WORK / "timings_validated.json").read_text(encoding="utf-8"))
    step = sys.argv[1] if len(sys.argv) > 1 else "all"
    if step in ("audio", "all"):
        prepare_audio(cfg)
    if step in ("covers", "all"):
        make_covers()
    if step in ("video", "all"):
        render_video(cfg, WORK / "full.wav")
    if step in ("master", "all"):
        make_master_mp3(cfg)


if __name__ == "__main__":
    main()
