#!/usr/bin/env python3
"""Clip 9:16 — lock10 (visage intact) + mot-à-mot (gros → petit) hors visage."""
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
LOCK = ROOT / "assets" / "raw" / "portrait" / "lock10"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 1080, 1920
CW, CH = 1188, 2112
FPS = 24
ADVANCE = 0.03
XFADE = 0.45
PLATES = ["l01", "l02", "l03", "l04", "l05", "l06", "l07", "l08", "l10"]

# Lyrics sit on the hoodie / wall BELOW the face (TikTok caption starts y=1574)
Y_WORD = 1380
Y_TRAIL = 1268
Y_BADGE = 150


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(ASSETS / "fonts" / name), size)


def to_canvas(im: Image.Image) -> Image.Image:
    im = im.convert("RGB")
    w, h = im.size
    r = w / h
    tr = W / H
    if r > tr:
        nw = int(h * tr)
        left = (w - nw) // 2
        im = im.crop((left, 0, left + nw, h))
    elif r < tr:
        nh = int(w / tr)
        top = max(0, (h - nh) // 5)
        im = im.crop((0, top, w, min(h, top + nh)))
    return im.resize((CW, CH), Image.Resampling.LANCZOS)


def prepare_fonds() -> None:
    FONDS.mkdir(parents=True, exist_ok=True)
    for stem in PLATES:
        src = next(LOCK.glob(f"{stem}_*.png"), None)
        if src is None:
            raise FileNotFoundError(stem)
        canvas = to_canvas(Image.open(src))
        canvas.save(FONDS / f"{stem}.jpg", quality=94, subsampling=0)
        print("fond", stem, canvas.size)


def load_plate(stem: str) -> np.ndarray:
    im = Image.open(FONDS / f"{stem}.jpg").convert("RGB")
    if im.size != (CW, CH):
        im = im.resize((CW, CH), Image.Resampling.LANCZOS)
    return np.array(im)


def ken_burns(plate: np.ndarray, t: float, slot: int) -> np.ndarray:
    z0, z1 = (1.02, 1.08) if slot % 2 == 0 else (1.08, 1.02)
    u = 0.5 + 0.5 * math.sin(t * 0.12 + slot * 1.4)
    zoom = z0 + (z1 - z0) * u
    crop_w = min(CW, int(round(CW / zoom)))
    crop_h = min(CH, int(round(crop_w * 16 / 9)))
    if crop_h > CH:
        crop_h = CH
        crop_w = int(round(crop_h * 9 / 16))
    max_x = max(0, CW - crop_w)
    max_y = max(0, CH - crop_h)
    pan_x = 0.5 + 0.38 * math.sin(t * 0.22 + slot * 0.9)
    pan_y = 0.42 + 0.22 * math.sin(t * 0.18 + slot * 0.6)  # bias UP so face stays in
    x = int(np.clip(pan_x, 0, 1) * max_x)
    y = int(np.clip(pan_y, 0, 1) * max_y)
    crop = plate[y : y + crop_h, x : x + crop_w]
    return np.array(Image.fromarray(crop).resize((W, H), Image.Resampling.BILINEAR))


def render_word(text: str, size: int, fill, glow=True) -> np.ndarray:
    f = font("DejaVuSans-Bold.ttf", size)
    dummy = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    bb = dummy.textbbox((0, 0), text, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = 18
    im = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ox, oy = pad - bb[0], pad - bb[1]
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2)):
        d.text((ox + dx, oy + dy), text, font=f, fill=(12, 6, 2, 220))
    d.text((ox, oy), text, font=f, fill=fill)
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        gd.text((ox, oy), text, font=f, fill=(240, 180, 70, 80))
        g = g.filter(ImageFilter.GaussianBlur(7))
        im = Image.alpha_composite(g, im)
    return np.array(im)


class WordBank:
    def __init__(self) -> None:
        self.big: dict[str, np.ndarray] = {}
        self.small: dict[str, np.ndarray] = {}

    def get_big(self, w: str, hook: bool) -> np.ndarray:
        key = ("h" if hook else "v") + w
        if key not in self.big:
            fill = (240, 193, 90, 255) if hook else (255, 244, 220, 255)
            self.big[key] = render_word(w, 118, fill, glow=True)
        return self.big[key]

    def get_small(self, w: str) -> np.ndarray:
        if w not in self.small:
            self.small[w] = render_word(w, 24, (255, 230, 190, 130), glow=False)
        return self.small[w]


def alpha_over(bg: np.ndarray, fg: np.ndarray, x: int, y: int) -> np.ndarray:
    fh, fw = fg.shape[:2]
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + fw), min(H, y + fh)
    if x1 <= x0 or y1 <= y0:
        return bg
    f = fg[y0 - y : y1 - y, x0 - x : x1 - x].astype(np.float32)
    if f.shape[2] == 3:
        bg[y0:y1, x0:x1] = f.astype(np.uint8)
        return bg
    a = f[:, :, 3:4] / 255.0
    sl = bg[y0:y1, x0:x1].astype(np.float32)
    bg[y0:y1, x0:x1] = np.clip(sl * (1 - a) + f[:, :, :3] * a, 0, 255).astype(np.uint8)
    return bg


def make_scrim() -> np.ndarray:
    """Bottom scrim only — face (upper/mid) stays clear."""
    s = np.zeros((H, W, 4), dtype=np.uint8)
    for y in range(1180, 1570):
        t = (y - 1180) / 390.0
        a = int(130 * (1 - abs(t - 0.55) * 1.4))
        if a > 0:
            s[y, :, 0] = 18
            s[y, :, 1] = 8
            s[y, :, 2] = 4
            s[y, :, 3] = min(140, a)
    return s


def word_index(local: float, dur: float, words: list[str]) -> tuple[int, float]:
    if not words:
        return 0, 0.0
    weights = np.array([max(3, len(w)) for w in words], dtype=np.float64)
    weights /= weights.sum()
    acc = 0.0
    u = 0.0 if dur <= 0 else max(0.0, min(0.999, local / dur))
    for i, wt in enumerate(weights):
        if u < acc + wt:
            return i, (u - acc) / wt
        acc += wt
    return len(words) - 1, 1.0


def draw_kinetic(frame: np.ndarray, verse: dict, local: float, dur: float, bank: WordBank) -> np.ndarray:
    words = verse.get("words") or verse["text"].split()
    if not words:
        return frame
    hook = verse.get("kind") in ("hook", "sig", "outro")
    idx, phase = word_index(local, dur, words)
    # trail of past words (small) — one line, centered, truncated
    past = words[:idx]
    if past:
        chips = [bank.get_small(w) for w in past[-6:]]
        total_w = sum(c.shape[1] - 16 for c in chips) + 16
        x = (W - total_w) // 2
        for c in chips:
            frame = alpha_over(frame, c, x, Y_TRAIL)
            x += c.shape[1] - 16
    # current word pops BIG then eases
    # Attack: explodes big, then holds. Next word = this one drops to the small trail.
    if phase < 0.15:
        pop = 1.55 - 0.35 * (phase / 0.15)
    else:
        pop = 1.20 - 0.08 * min(1.0, (phase - 0.15) / 0.85)
    big = bank.get_big(words[idx], hook)
    nh = max(8, int(big.shape[0] * pop))
    nw = max(8, int(big.shape[1] * pop))
    if nw > 1000:
        s = 1000 / nw
        nw, nh = 1000, max(8, int(nh * s))
    scaled = np.array(Image.fromarray(big).resize((nw, nh), Image.Resampling.BILINEAR))
    x = (W - nw) // 2
    y = Y_WORD - nh // 2
    frame = alpha_over(frame, scaled, x, y)
    return frame


def draw_badge(frame: np.ndarray, a: float) -> np.ndarray:
    if a <= 0.02:
        return frame
    im = Image.new("RGBA", (240, 56), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font("DejaVuSans-Bold.ttf", 34)
    t = "DSKY✓"
    bb = d.textbbox((0, 0), t, font=f)
    d.text(((240 - (bb[2] - bb[0])) // 2, 8), t, font=f, fill=(240, 193, 90, int(255 * min(a, 0.72))))
    return alpha_over(frame, np.array(im), (W - 240) // 2, Y_BADGE)


def draw_endcard(frame: np.ndarray, tloc: float, cfg: dict) -> np.ndarray:
    a = min(1.0, tloc / 0.55)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    ft = font("GreatVibes-Regular.ttf", 108)
    fu = font("DejaVuSans-Bold.ttf", 30)
    title = "Le goût bon de la vie"
    bb = d.textbbox((0, 0), title, font=ft)
    tx = (W - (bb[2] - bb[0])) // 2
    ty = 520
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
        d.text((tx + dx, ty + dy), title, font=ft, fill=(18, 8, 2, int(255 * a)))
    d.text((tx, ty), title, font=ft, fill=(240, 193, 90, int(255 * a)))
    art = "Daïsky"
    bb = d.textbbox((0, 0), art, font=fu)
    d.text(((W - (bb[2] - bb[0])) // 2, ty + 130), art, font=fu, fill=(255, 236, 210, int(230 * a)))
    yy = 980
    for ln in cfg["contacts"]["whatsapp"] + [cfg["contacts"]["email"], "DSKY✓"]:
        bb = d.textbbox((0, 0), ln, font=fu)
        d.text(((W - (bb[2] - bb[0])) // 2, yy), ln, font=fu, fill=(255, 236, 210, int(210 * a)))
        yy += 48
    return alpha_over(frame, np.array(ov), 0, 0)


def draw_hook_title(frame: np.ndarray, t: float) -> np.ndarray:
    if t > 2.2:
        fade = max(0.0, 1.0 - (t - 2.2) / 0.45)
    else:
        fade = min(1.0, t / 0.4)
    if fade <= 0:
        return frame
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    ft = font("GreatVibes-Regular.ttf", 100)
    fu = font("DejaVuSans-Bold.ttf", 32)
    title = "Le goût bon de la vie"
    bb = d.textbbox((0, 0), title, font=ft)
    tx = (W - (bb[2] - bb[0])) // 2
    ty = 210  # top wall, above the head
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
        d.text((tx + dx, ty + dy), title, font=ft, fill=(18, 8, 2, int(255 * fade)))
    d.text((tx, ty), title, font=ft, fill=(240, 193, 90, int(255 * fade)))
    bb = d.textbbox((0, 0), "Daïsky", font=fu)
    d.text(((W - (bb[2] - bb[0])) // 2, ty + 120), "Daïsky", font=fu, fill=(255, 236, 210, int(220 * fade)))
    return alpha_over(frame, np.array(ov), 0, 0)


def slot_index(stem: str) -> int:
    return PLATES.index(stem) if stem in PLATES else 0


def active_photo(t_music: float, verses, instrumentals, default="l01") -> str:
    for v in verses:
        if v["start"] - 0.12 <= t_music < v["end"] + 0.1:
            return v["photo"]
    for ins in instrumentals:
        if ins["start"] <= t_music < ins["end"]:
            return ins["photo"]
    return default


def active_verse(t_music: float, verses):
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
        subprocess.check_call(cmd)

    run(
        [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(src), "-map", "0:a:0", "-vn",
            "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "2", str(song_wav),
        ]
    )
    ln = (
        "highpass=f=30,lowpass=f=18000,"
        "loudnorm=I=-14:TP=-1.8:LRA=11:"
        "measured_I=-14.46:measured_TP=0.01:measured_LRA=8.50:"
        "measured_thresh=-24.62:offset=-0.81:linear=true"
    )
    run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", str(song_wav), "-af", ln, str(song_ln)])
    run(
        [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(song_ln), "-ss", str(cfg["hook_src_start"]), "-t", str(cfg["hook"]),
            "-acodec", "pcm_s16le", str(hook_wav),
        ]
    )
    fade_st = cfg["hook"] + cfg["song_duration"] + cfg["apad"] - 3.0
    filt = (
        f"[0:a]aformat=sample_fmts=s16:sample_rates=48000:channel_layouts=stereo[h];"
        f"[1:a]aformat=sample_fmts=s16:sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{cfg['song_duration']},asetpts=PTS-STARTPTS[s];"
        f"[h][s]concat=n=2:v=0:a=1,apad=pad_dur={cfg['apad']},"
        f"afade=t=out:st={fade_st}:d=3[a]"
    )
    run(
        [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(hook_wav), "-i", str(song_ln),
            "-filter_complex", filt, "-map", "[a]", "-t", str(cfg["total"]), str(full_wav),
        ]
    )
    return full_wav


def render_video(cfg: dict, audio: Path) -> Path:
    prepare_fonds()
    plates = {s: load_plate(s) for s in PLATES}
    scrim = make_scrim()
    bank = WordBank()
    verses = cfg["verses"]
    hook_lines = cfg["hook_lines"]
    instrumentals = cfg["instrumentals"]
    nframes = cfg["nframes"]
    total = cfg["total"]
    hook = cfg["hook"]
    song_dur = cfg["song_duration"]
    LIV.mkdir(exist_ok=True)
    out_mp4 = LIV / "Le_gout_bon_de_la_vie_9x16_v1.mp4"
    cmd = [
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0",
        "-i", str(audio), "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-shortest", "-movflags", "+faststart", str(out_mp4),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert proc.stdin
    prev_stem = "l01"
    prev_frame = None
    fade_left = 0.0
    fade_from = None
    for i in range(nframes):
        t = i / FPS
        if t < hook:
            t_music = cfg["hook_src_start"] + t
            in_hook, in_end = True, False
        else:
            t_music = t - hook
            in_hook, in_end = False, t_music >= song_dur
        if in_end:
            stem = "l10"
        elif in_hook:
            stem = "l03"
            for hl in hook_lines:
                if hl["start"] <= t < hl["end"]:
                    stem = hl["photo"]
                    break
        else:
            stem = active_photo(t_music, verses, instrumentals)
        slot = slot_index(stem)
        kb_t = t if in_hook else t_music
        frame = ken_burns(plates[stem], kb_t, slot)
        if stem != prev_stem and prev_frame is not None:
            fade_left = XFADE
            fade_from = prev_frame
        if fade_left > 0 and fade_from is not None:
            u = fade_left / XFADE
            frame = (frame.astype(np.float32) * (1 - u) + fade_from.astype(np.float32) * u).astype(np.uint8)
            fade_left -= 1.0 / FPS
        prev_stem, prev_frame = stem, frame

        badge_a = 0.0
        if in_end:
            frame = draw_endcard(frame, t_music - song_dur, cfg)
            badge_a = 0.5
        elif in_hook:
            frame = draw_hook_title(frame, t)
            verse = None
            for hl in hook_lines:
                if hl["start"] <= t < hl["end"]:
                    verse = hl
                    break
            if verse and t > 0.25:
                frame = alpha_over(frame, scrim, 0, 0)
                local = t - verse["start"]
                dur = verse["end"] - verse["start"]
                frame = draw_kinetic(frame, verse, max(0.0, local), dur, bank)
                badge_a = min(0.72, max(0.0, local) / 0.35, (dur - local) / 0.35)
        else:
            verse = active_verse(t_music, verses)
            if verse:
                frame = alpha_over(frame, scrim, 0, 0)
                local = (t_music + ADVANCE) - verse["start"]
                dur = verse["end"] - verse["start"]
                frame = draw_kinetic(frame, verse, max(0.0, local), dur, bank)
                badge_a = min(0.72, max(0.0, local) / 0.35, (dur - local) / 0.35)
        frame = draw_badge(frame, max(0.0, badge_a))
        if t > total - 3.0:
            fade = max(0.0, (total - t) / 3.0)
            frame = (frame.astype(np.float32) * fade).astype(np.uint8)
        if not frame.flags["C_CONTIGUOUS"]:
            frame = np.ascontiguousarray(frame)
        proc.stdin.write(frame.tobytes())
        if i % 72 == 0:
            print(f"frame {i}/{nframes} t={t:.1f} {stem}", flush=True)
    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise SystemExit(f"ffmpeg {rc}")
    print("wrote", out_mp4, out_mp4.stat().st_size)
    return out_mp4


def main() -> None:
    cfg = json.loads((WORK / "timings_validated.json").read_text(encoding="utf-8"))
    step = sys.argv[1] if len(sys.argv) > 1 else "all"
    if step in ("fonds", "all"):
        prepare_fonds()
    if step in ("audio", "all"):
        prepare_audio(cfg)
    if step in ("video", "all"):
        render_video(cfg, WORK / "full.wav")


if __name__ == "__main__":
    main()
