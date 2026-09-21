#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
DSKY LYRIC VIDEOS — moteur de clips karaoké (projet TechStein/Daïsky)
================================================================================
Rend un clip vertical 1080x1920 (9:16) :  fonds (photos RÉELLES de l'auteur
+ fonds IA d'ambiance)  +  paroles karaoké synchronisées sur le .lrc  +  master
mp3 du repo, puis exporte la vidéo MP4 + le .srt (sous-titres YouTube).

Charte DSKY  : badge « DSKY 🇧🇯 » discret qui vit avec les paroles, liseré
tricolore béninois, signature, scrim central.  Paroles rendues PAR CODE
(jamais par l'IA) — le visage de l'auteur n'est JAMAIS retouché.

USAGE RAPIDE
  python3 lyricvideo.py --song "Seul dans ma tête"              # clip complet
  python3 lyricvideo.py --song "Seul dans ma tête" --preview    # 4 PNG de contrôle
  python3 lyricvideo.py --song "Noukiko" --limit 25             # extrait 25 s
  python3 lyricvideo.py --song "Seul dans ma tête" --hook 6     # cold-open 6 s

Le dossier de sortie est  lyric-videos/<slug>/  (créé automatiquement).

Dépendances : pillow, numpy, imageio-ffmpeg  →  voir setup_env.sh
================================================================================
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass, field

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# --------------------------------------------------------------------------- #
#  CHEMINS & CONSTANTES
# --------------------------------------------------------------------------- #
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # racine du repo lyric
FONTS_REPO = os.path.join(ROOT, "dsky-quotes", "assets", "fonts")
FONTS_SYS = "/usr/share/fonts/truetype/dejavu"

W, H = 1080, 1920
KEN = 1.10                                        # canvas Ken Burns
FPS_DEF = 30

# --- charte DSKY (reprise du projet quotes) -------------------------------- #
C_TEXT = (247, 242, 231)
C_ACCENT = (201, 162, 39)
BENIN_GREEN = (0, 135, 81)
BENIN_YELLOW = (252, 209, 22)
BENIN_RED = (232, 17, 45)

BADGE_LABEL = "DSKY"
EMAIL = "daiskyproduction@gmail.com"
WHATSAPP = "+229 01 61 16 24 08"
SIGNATURE = "C. JÉSUTONDJI SAMUEL STEIN"
SIGN_SUB = "LYRICISTE  ·  BÉNIN"

# styles (§G du prompt universel) ------------------------------------------- #
STYLES = {
    "dark": {"accent": (201, 162, 39), "scrim": (6, 9, 18), "glow": (255, 205, 120)},
    "gold": {"accent": (232, 178, 58), "scrim": (22, 14, 8), "glow": (255, 196, 110)},
    "neon": {"accent": (255, 86, 190), "scrim": (12, 6, 30), "glow": (120, 240, 255)},
    "ink":  {"accent": (216, 132, 60),  "scrim": (8, 8, 10), "glow": (255, 170, 90)},
    "retro": {"accent": (226, 176, 110), "scrim": (18, 14, 12), "glow": (255, 200, 150)},
}
LEXIQUE = {
    "gold":  ["amour", "coeur", "cœur", "soleil", "espoir", "aime", "belle", "rire", "joie", "sourire"],
    "neon":  ["fete", "fête", "danse", "bouge", "club", "ville", "foule", "dance", "djo", "afro"],
    "ink":   ["mort", "deuil", "perdu", "larme", "pleure", "silence", "vide", "adieu", "tombe"],
    "retro": ["souvenir", "hier", "enfance", "autrefois", "vieux", "temps", "annees", "années"],
    "dark":  ["nuit", "seul", "peur", "combat", "guerre", "sombre", "demon", "démon", "pression",
              "doute", "crie", "tomber", "chaine", "chaîne", "ego", "égo", "pauvre"],
}

JPEG_Q = 90
CACHE_SPRITES: dict = {}


def log(*a):
    print("[dsky]", *a, flush=True)


# --------------------------------------------------------------------------- #
#  OUTILS TEXTE / ENCODAGE
# --------------------------------------------------------------------------- #
def smart_decode(data: bytes) -> str:
    """Décode un fichier dont l'encodage est mixte (cp1252 majoritaire + séquences
    UTF-8 isolées, cas réel des .lrc du repo)."""
    out, i, n = [], 0, len(data)
    while i < n:
        b = data[i]
        if b in (0xC2, 0xC3) and i + 1 < n and 0x80 <= data[i + 1] <= 0xBF:
            out.append(bytes(data[i:i + 2]).decode("utf-8"))
            i += 2
            continue
        if b < 0x80:
            out.append(chr(b))
            i += 1
            continue
        try:
            out.append(bytes([b]).decode("cp1252"))
        except UnicodeDecodeError:
            out.append(bytes([b]).decode("latin-1"))
        i += 1
    return "".join(out).replace("\r\n", "\n").replace("\r", "\n")


def norm_key(s: str) -> str:
    """Clé de comparaison : minuscules, sans accents, sans ponctuation ni suffixe
    d'artiste (ex. « Seul dans ma tête _ Daïsky » → « seul dans ma tete »)."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[_*]+", " ", s)
    s = re.sub(r"\((?:official|audio|lyrics?|clip|video)[^)]*\)", " ", s)
    s = re.sub(r"\b(?:daisky|da sky|dsky|techstein|nass ?'?m ?rb)\b", " ", s)
    s = re.sub(r"\b(?:lrc|txt|mp3|timing|paroles|lyrics)\b", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


# --------------------------------------------------------------------------- #
#  SOURCES (paroles + master audio)
# --------------------------------------------------------------------------- #
def scan_sources() -> tuple[list[str], list[str]]:
    lyrics, audios = [], []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "work", "fonds",
                                                "lyric-videos", "__pycache__"}]
        for f in files:
            p = os.path.join(base, f)
            low = f.lower()
            if low.endswith((".lrc", ".txt")) and not low.startswith(("prompt", "readme", "indication")):
                if os.path.getsize(p) < 400_000:
                    lyrics.append(p)
            elif low.endswith((".mp3", ".wav", ".m4a", ".opus")):
                audios.append(p)
    return lyrics, audios


def find_pair(song: str) -> tuple[str, str]:
    lyrics, audios = scan_sources()
    key = norm_key(song)

    def score(path, is_lyric):
        k = norm_key(os.path.splitext(os.path.basename(path))[0])
        s = 0
        if k == key:
            s += 100
        elif key and (k.startswith(key) or key.startswith(k)):
            s += 70
        elif key and (key in k or k in key):
            s += 45
        if is_lyric:
            s += 12 if path.lower().endswith(".lrc") else 0
        return s

    ls = sorted(((score(p, True), p) for p in lyrics), reverse=True)
    au = sorted(((score(p, False), p) for p in audios), reverse=True)
    if not ls or ls[0][0] < 45:
        raise SystemExit(f"[dsky] Aucune parole trouvée pour « {song} ».\n"
                         f"       Candidats : {[os.path.basename(p) for p in lyrics]}")
    if not au or au[0][0] < 45:
        raise SystemExit(f"[dsky] Aucun master audio trouvé pour « {song} ».\n"
                         f"       Candidats : {[os.path.basename(p) for p in audios]}")
    return ls[0][1], au[0][1]


# --------------------------------------------------------------------------- #
#  PARSE LRC  +  NORMALISATION DES TIMINGS
# --------------------------------------------------------------------------- #
TAG_META = re.compile(r"^\[(ti|ar|al|by|offset|re|ve|length|au|id):(.*)\]$", re.I)
TAG_TIME = re.compile(r"^\[(\d{1,3}):(\d{2})(?:[.:](\d{1,3}))?\]\s*(.*)$")


@dataclass
class Entry:
    t: float
    text: str
    kind: str = "lyric"          # lyric | jingle | didascalie | meta | blank
    sub: list[str] = field(default_factory=list)


def parse_lyrics(path: str) -> tuple[list[Entry], float | None, list[str]]:
    raw = smart_decode(open(path, "rb").read())
    entries: list[Entry] = []
    sections: list[str] = []
    length = None
    for line in raw.split("\n"):
        s = line.strip()
        if not s:
            continue
        m = TAG_META.match(s)
        if m:
            if m.group(1).lower() == "length":
                try:
                    mm, ss = m.group(2).split(":")
                    length = int(mm) * 60 + float(ss)
                except Exception:
                    pass
            continue
        if s.startswith("[") and not TAG_TIME.match(s):
            sections.append(s.strip("[]"))
            continue
        m = TAG_TIME.match(s)
        if not m:
            continue
        mm, ss, frac, txt = m.groups()
        t = int(mm) * 60 + int(ss)
        if frac is not None:
            t += int(frac) / (1000.0 if len(frac) == 3 else 100.0)
        txt = txt.strip()
        if not txt:
            entries.append(Entry(t, "", "blank"))
            continue
        entries.append(Entry(t, txt, classify(txt)))
    entries.sort(key=lambda e: e.t)
    return entries, length, sections


def classify(txt: str) -> str:
    t = txt.strip()
    if re.match(r"^\(?wolof\s+techstein", t, re.I) or re.match(r"^wolof\s+techstein.*beat", t, re.I):
        return "jingle"
    if t.startswith("(") and t.endswith(")"):
        return "didascalie"
    if t.startswith("[") and t.endswith("]"):
        return "didascalie"
    return "lyric"


def clean_display(txt: str) -> str:
    """Retire les didascalies inline en début de ligne : « (Voix 1) Mmh… » → « Mmh… »"""
    m = re.match(r"^(\([^)]{1,40}\)|\[[^]]{1,40}\])\s*(.+)$", txt.strip())
    if m and len(m.group(2)) >= 3:
        return m.group(2).strip()
    return txt.strip()


def normalize_timings(entries: list[Entry], min_gap=1.2, tolerance=0.0) -> list[Entry]:
    """Monotonie stricte + fenêtre mini entre vers consécutifs (§A.3)."""
    out = []
    for e in entries:
        if out and e.t <= out[-1].t:
            e.t = out[-1].t + min_gap
        out.append(e)
    return out


@dataclass
class Cue:
    start: float
    end: float
    text: str
    kind: str
    lines: list[str] = field(default_factory=list)
    size: int = 0
    section: str = "couplet"
    slot: int = 0


def detect_refrains(entries: list[Entry], hook_line: str | None) -> None:
    """Marque les lignes de refrain (répétition ≥ 2 de la même ligne, ou titre)."""
    counts: dict[str, int] = {}
    for e in entries:
        if e.kind == "lyric":
            counts[norm_key(e.text)] = counts.get(norm_key(e.text), 0) + 1
    for e in entries:
        k = norm_key(e.text)
        if e.kind != "lyric":
            continue
        if counts.get(k, 0) >= 2 or (hook_line and hook_line in k):
            e.kind = "refrain"


def build_cues(entries: list[Entry], duration: float, ctx_before: float = 0.25,
               min_dur=0.9, max_dur=8.0, hide_didascalie=False) -> list[Cue]:
    items = [e for e in entries if e.kind in ("lyric", "refrain", "jingle", "didascalie")]
    cues: list[Cue] = []
    n = len(items)
    for i, e in enumerate(items):
        nxt = items[i + 1].t if i + 1 < n else duration - 0.2
        if e.kind == "blank":
            continue
        start = max(0.0, e.t - ctx_before * 0.4)
        end = min(duration, max(nxt - 0.10, start + min_dur))
        end = min(end, start + max_dur)
        cues.append(Cue(start, end, e.text, e.kind))
    # slots de fonds : un plan par « bloc » (intro, couplet, refrain, pont, outro)
    for i, c in enumerate(cues):
        prev = cues[i - 1] if i else None
        same = prev and prev.kind == c.kind and (c.start - prev.start) < 9.0
        c.section = c.kind
        c.slot = (prev.slot if same else (prev.slot + 1 if prev else 0))
    return cues


# --------------------------------------------------------------------------- #
#  POLICES
# --------------------------------------------------------------------------- #
def font_path(which: str) -> str:
    cands = {
        "playfair": [os.path.join(FONTS_REPO, "PlayfairDisplay.ttf")],
        "playfair_it": [os.path.join(FONTS_REPO, "PlayfairDisplay-Italic.ttf")],
        "mont": [os.path.join(FONTS_REPO, "Montserrat.ttf")],
        "mont_it": [os.path.join(FONTS_REPO, "Montserrat-Italic.ttf")],
        "dejavu": [os.path.join(FONTS_SYS, "DejaVuSans-Bold.ttf")],
        "dejavu_r": [os.path.join(FONTS_SYS, "DejaVuSans.ttf")],
    }[which]
    for c in cands:
        if os.path.exists(c):
            return c
    return cands[0]


def load_font(which: str, size: int, weight: int | None = None) -> ImageFont.FreeTypeFont:
    """Charge une police (Montserrat / Playfair sont VARIABLES : poids réglable)."""
    key = ("font", which, size, weight)
    if key not in CACHE_SPRITES:
        try:
            f = ImageFont.truetype(font_path(which), size)
            if weight:
                try:
                    f.set_variation_by_axes([weight])
                except Exception:
                    pass
            CACHE_SPRITES[key] = f
        except Exception:
            CACHE_SPRITES[key] = ImageFont.load_default()
    return CACHE_SPRITES[key]


# --------------------------------------------------------------------------- #
#  TEXTE : mesure, wrap, sprites
# --------------------------------------------------------------------------- #
def text_w(draw, txt, f):
    return draw.textlength(txt, font=f)


def wrap_text(draw, txt, f, max_w) -> list[str]:
    words, lines, cur = txt.split(), [], ""
    for wd in words:
        test = (cur + " " + wd).strip()
        if text_w(draw, test, f) <= max_w or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def fit_wrap(draw, txt, font_name, max_w, max_lines, size0, size_min, lh=1.22):
    size = size0
    while size > size_min:
        f = load_font(font_name, size)
        if text_w(draw, txt, f) <= max_w:
            return [txt], size, lh
        size -= 2
    f = load_font(font_name, size_min)
    lines = wrap_text(draw, txt, f, max_w)
    while len(lines) > max_lines and size_min > 40:
        size_min -= 4
        f = load_font(font_name, size_min)
        lines = wrap_text(draw, txt, f, max_w)
    return lines, size_min, lh


def make_text_sprite(lines: list[str], font_name: str, size: int, lh: float,
                     color, pad=48, glow=None, glow_strength=0.0,
                     weight: int | None = None, stroke: int = 0):
    """Rend un bloc de texte en RGBA (couleur unie ou avec halo)."""
    f = load_font(font_name, size, weight)
    tmp = ImageDraw.Draw(Image.new("L", (10, 10)))
    widths = [text_w(tmp, ln, f) for ln in lines]
    step = int(size * lh)
    asc, desc = f.getmetrics()
    bw = int(max(widths)) + pad * 2
    bh = step * (len(lines) - 1) + asc + desc + pad * 2
    img = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ys = []
    y = pad
    for ln in lines:
        ys.append(y)
        y += step
    if glow and glow_strength > 0:
        gl = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        gd = ImageDraw.Draw(gl)
        for ln, yy in zip(lines, ys):
            gd.text(((bw - text_w(gd, ln, f)) / 2, yy), ln, font=f, fill=glow + (255,))
        gl = gl.filter(ImageFilter.GaussianBlur(max(3, size // 12)))
        img.alpha_composite(Image.blend(Image.new("RGBA", (bw, bh), (0, 0, 0, 0)), gl, glow_strength))
    for ln, yy in zip(lines, ys):
        x = (bw - text_w(d, ln, f)) / 2
        d.text((x + max(2, size // 40), yy + max(2, size // 34)), ln, font=f, fill=(0, 0, 0, 150))
        if stroke:
            d.text((x, yy), ln, font=f, fill=color, stroke_width=stroke,
                   stroke_fill=(4, 5, 9, 215))
        else:
            d.text((x, yy), ln, font=f, fill=color)
    return img, ys, step


# --------------------------------------------------------------------------- #
#  SCENE : fonds, scrim, cadre fixe (badge + liseré), bruit
# --------------------------------------------------------------------------- #
class Scene:
    """Fonds (photos réelles / images IA) + traitement DSKY : cadrage intelligent
    (visage de l'auteur dans le haut du cadre), scrim adaptatif, flou doux de la
    bande de paroles, cadre fixe (liseré tricolore), grain cinéma.

    Modèle : chaque fond a un canevas agrandi (E×) dans lequel une fenêtre (viewport
    k×W, k×H) se déplace -> zoom Ken Burns + pan, sans jamais sortir du canevas.
    """

    E_PHOTO, E_IA = 1.17, 1.22         # marge du canevas (Ken Burns + pan)
    K_MIN, K_MAX = 1.015, 1.085        # taille du viewport (× W)
    FACE_ANCHOR = 0.30                 # visage placé à 30 % du haut du cadre

    def __init__(self, style: str, fonds: list[tuple[str, str]], seed=7, blur_band=True):
        self.style = style if style in STYLES else "dark"
        self.pal = STYLES[self.style]
        self.rng = random.Random(seed)
        self.blur_band = blur_band
        self.items = []
        for path, origin in fonds:
            is_photo = not (os.path.basename(origin).startswith("f")
                            and not os.path.basename(origin).startswith("fond"))
            self.items.append(self.prepare(path, os.path.basename(origin), is_photo))
        if not self.items:
            base = Image.new("RGB", (int(W * self.E_IA), int(H * self.E_IA)), self.pal["scrim"])
            self.items = [{"img": base, "blur": None, "overlay": self._make_scrim(1.0),
                           "E": self.E_IA, "ax": 0.5, "ay": 0.5, "is_photo": False,
                           "name": "(uni)"}]
        self.band_mask = self._make_band_mask()
        self.overlay_frame = self._make_frame_base()
        self.noise = self._make_noise()

    # ---- détections ----------------------------------------------------- #
    @staticmethod
    def _skin_centroid(im: Image.Image):
        """Centre (x, y) normalisé de la peau (= visage) dans une image, ou None."""
        gw = 140
        gh = max(8, int(gw * im.height / im.width))
        a = np.asarray(im.resize((gw, gh), Image.BILINEAR), dtype=np.float32)
        r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
        mx, mn = a.max(axis=2), a.min(axis=2)
        skin = (r > 95) & (g > 40) & (b > 15) & (mx - mn > 18) & (r > g) & (r > b)
        if skin.mean() < 0.02:
            return None
        rows = skin.sum(axis=1).astype(np.float32)
        cols = skin.sum(axis=0).astype(np.float32)
        cy = float(np.searchsorted(np.cumsum(rows), rows.sum() / 2)) / gh
        cx = float(np.searchsorted(np.cumsum(cols), cols.sum() / 2)) / gw
        return cx, cy

    @staticmethod
    def _detail_band(gray: np.ndarray, y0f: float, th_f: float) -> float:
        gh = gray.shape[0]
        y0 = (gh - th_f) * y0f
        lo = int(y0 + th_f * ((H / 2 - 340) / H))
        hi = int(y0 + th_f * ((H / 2 + 340) / H))
        lo, hi = max(1, min(lo, gh - 2)), max(2, min(hi, gh - 1))
        band = gray[lo:hi]
        gv = float(np.abs(np.diff(band, axis=0)).mean()) if band.shape[0] > 2 else 0.0
        gg = float(np.abs(np.diff(band, axis=1)).mean()) if band.shape[1] > 2 else 0.0
        return 0.6 * gv + 0.4 * gg

    def _best_yfrac(self, im: Image.Image, th: int) -> float:
        gw = 160
        gh = max(8, int(gw * im.height / im.width))
        gray = np.asarray(im.convert("L").resize((gw, gh), Image.BILINEAR), dtype=np.float32)
        th_f = gh * th / im.height
        grids = np.arange(0.0, 1.0001, 0.05)
        sc = [self._detail_band(gray, f, th_f) + 0.06 * abs(f - 0.35) for f in grids]
        f0 = float(grids[int(np.argmin(sc))])
        fine = np.clip(np.arange(f0 - 0.05, f0 + 0.0501, 0.0125), 0, 1)
        sc = [self._detail_band(gray, f, th_f) + 0.06 * abs(f - 0.35) for f in fine]
        return float(fine[int(np.argmin(sc))])

    # ---- préparation d'un fond ------------------------------------------ #
    def prepare(self, path: str, name: str, is_photo=True):
        im = Image.open(path).convert("RGB")
        E = self.E_PHOTO if is_photo else self.E_IA
        cw, ch = int(W * E), int(H * E)
        r = max(cw / im.width, ch / im.height)
        im = im.resize((max(cw, int(im.width * r) + 1), max(ch, int(im.height * r) + 1)),
                       Image.LANCZOS)
        # fenêtre nominale
        k = (self.K_MIN + self.K_MAX) / 2
        vw, vh = k * W, k * H
        ax, ay = 0.5, 0.5
        info = ""
        if is_photo:
            c = self._skin_centroid(im)
            if c:
                fx, fy = c[0] * im.width, c[1] * im.height
                x0 = fx - 0.48 * vw
                y0 = fy - self.FACE_ANCHOR * vh
                x0 = float(np.clip(x0, 0, im.width - vw))
                y0 = float(np.clip(y0, 0, im.height - vh))
                ax, ay = (x0 + vw / 2) / im.width, (y0 + vh / 2) / im.height
                info = f" · visage={c[1]:.2f}"
            else:
                info = " · visage non détecté"
        else:
            yf = self._best_yfrac(im, int(vh))
            y0 = (im.height - vh) * yf
            ay = (y0 + vh / 2) / im.height
            info = f" · cadrage y={yf:.2f}"
        x0, y0 = int(ax * im.width - vw / 2), int(ay * im.height - vh / 2)
        x0 = max(0, min(x0, im.width - int(vw)))
        y0 = max(0, min(y0, im.height - int(vh)))
        nom = im.crop((x0, y0, x0 + int(vw), y0 + int(vh)))
        g = np.asarray(nom.convert("L").resize((60, int(60 * vh / vw))), dtype=np.float32)
        lo = int(g.shape[0] * ((H / 2 - 340) / H))
        hi = int(g.shape[0] * ((H / 2 + 340) / H))
        lum = float(g[max(0, lo):max(1, hi)].mean())
        kk = min(2.4, max(0.95, lum / 100.0)) + (0.35 if is_photo else 0.0)
        blur = im.filter(ImageFilter.GaussianBlur(11)) if (self.blur_band and not is_photo) else None
        log(f"   fond {name} : E={E} · ax={ax:.2f} ay={ay:.2f} · lum={lum:.0f} · "
            f"scrim×{kk:.2f}{info}")
        return {"img": im, "blur": blur, "overlay": self._make_scrim(kk), "E": E,
                "ax": ax, "ay": ay, "is_photo": is_photo, "name": name}

    # ---- scrim + masques ------------------------------------------------- #
    def _make_scrim(self, k=1.0) -> Image.Image:
        s = self.pal["scrim"]
        ov = Image.new("RGBA", (W, H), s + (min(120, int(30 * k)),))
        d = ImageDraw.Draw(ov)
        mid, band = H // 2, 360
        for i in range(H):
            a = 0
            if abs(i - mid) < band:
                t = 1 - abs(i - mid) / band
                a = int(min(238, 152 * k) * (t ** 0.75))
            elif i < H * 0.30:
                t = (H * 0.30 - i) / (H * 0.30)
                a = int(min(150, 105 * k) * t ** 1.25)
            elif i > H * 0.78:
                t = (i - H * 0.78) / (H * 0.22)
                a = int(min(190, 120 * k) * t ** 1.15)
            if a:
                d.line([(0, i), (W, i)], fill=s + (a,))
        return ov

    def _make_band_mask(self) -> Image.Image:
        m = Image.new("L", (1, H), 0)
        d = ImageDraw.Draw(m)
        mid, inner, outer = H // 2, 250, 470
        for i in range(H):
            dd = abs(i - mid)
            v = 205 if dd <= inner else (int(205 * (1 - (dd - inner) / (outer - inner)) ** 1.4)
                                         if dd < outer else 0)
            d.point((0, i), fill=v)
        return m.resize((W, H), Image.BILINEAR)

    def _make_frame_base(self) -> Image.Image:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        sh = 10
        third = W // 3
        d.rectangle([0, H - sh, third, H], fill=BENIN_GREEN + (255,))
        d.rectangle([third, H - sh, W, H - sh // 2], fill=BENIN_YELLOW + (255,))
        d.rectangle([third, H - sh // 2, W, H], fill=BENIN_RED + (255,))
        return ov

    def _make_noise(self) -> list[np.ndarray]:
        tiles = []
        for k in range(6):
            rng = np.random.default_rng(1000 + k)
            arr = rng.normal(0, 4.6, (H, W)).astype(np.int16)
            tiles.append(np.repeat(arr[:, :, None], 3, axis=2))
        return tiles

    # ---- viewport Ken Burns --------------------------------------------- #
    def _crop(self, src: Image.Image, it: dict, idx: int, ts: float) -> Image.Image:
        E = it["E"]
        k = self.K_MIN + (self.K_MAX - self.K_MIN) * (0.5 + 0.5 * math.sin(ts * 0.35 + idx))
        vw, vh = k * W, k * H
        mx, my = max(0.0, (src.width - vw) / 2), max(0.0, (src.height - vh) / 2)
        cx = it["ax"] * src.width + math.sin(ts * 0.21 + idx * 1.7) * mx
        cy = it["ay"] * src.height + math.sin(ts * 0.17 + idx * 0.9) * my
        x0 = int(max(0, min(cx - vw / 2, src.width - vw)))
        y0 = int(max(0, min(cy - vh / 2, src.height - vh)))
        return src.crop((x0, y0, x0 + int(vw), y0 + int(vh))).resize((W, H), Image.BILINEAR)

    def background(self, slot: int, t_slot: float, t_next: float | None = None,
                   mix: float = 0.0, slot_next: int | None = None) -> Image.Image:
        i = slot % len(self.items)
        it = self.items[i]
        img = self._crop(it["img"], it, i, t_slot)
        blur = self._crop(it["blur"], it, i, t_slot) if it["blur"] is not None else None
        if t_next is not None and slot_next is not None and mix > 0:
            j = slot_next % len(self.items)
            jt = self.items[j]
            m = min(1.0, max(0.0, mix))
            img = Image.blend(img, self._crop(jt["img"], jt, j, t_next), m)
            if blur is not None and jt["blur"] is not None:
                blur = Image.blend(blur, self._crop(jt["blur"], jt, j, t_next), m)
        if blur is not None:
            img = img.copy()
            img.paste(blur, (0, 0), self.band_mask)
        return img

    # ---- composition d'une frame --------------------------------------- #
    def frame(self, img: Image.Image, t: float, slot: int = 0) -> Image.Image:
        img = img.convert("RGBA")
        img.alpha_composite(self.items[slot % len(self.items)]["overlay"])
        img.alpha_composite(self.overlay_frame)
        arr = np.asarray(img.convert("RGB"), dtype=np.int16)
        arr += self.noise[int(t * FPS_DEF) % len(self.noise)]
        np.clip(arr, 0, 255, out=arr)
        return Image.fromarray(arr.astype(np.uint8), "RGB").convert("RGBA")

# --------------------------------------------------------------------------- #
#  BADGE DSKY 🇧🇯  (discret, ≤75 % opacité, vit avec les paroles)
# --------------------------------------------------------------------------- #
def draw_flag(d, x, y, w, h):
    third = int(w / 3)
    d.rectangle([x, y, x + third, y + h], fill=BENIN_GREEN)
    d.rectangle([x + third, y, x + w, y + h // 2], fill=BENIN_YELLOW)
    d.rectangle([x + third, y + h // 2, x + w, y + h], fill=BENIN_RED)


def make_badge(scale=1.0, opacity=0.72) -> Image.Image:
    key = ("badge", round(scale, 2), round(opacity, 2))
    if key in CACHE_SPRITES:
        return CACHE_SPRITES[key]
    f = load_font("mont", int(26 * scale))
    txt = BADGE_LABEL
    tmp = ImageDraw.Draw(Image.new("L", (8, 8)))
    tw = text_w(tmp, txt, f)
    fw, fh = int(30 * scale), int(22 * scale)
    pad = int(18 * scale)
    wpx, hpx = int(tw + fw + pad * 3.4), int(fh + pad * 1.5)
    img = Image.new("RGBA", (wpx, hpx), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    alpha = int(255 * opacity)
    d.rounded_rectangle([1, 1, wpx - 2, hpx - 2], radius=hpx // 2,
                        fill=(8, 8, 12, int(alpha * 0.62)),
                        outline=C_ACCENT + (int(alpha * 0.95),), width=max(2, int(2.4 * scale)))
    ax = pad
    ay = (hpx - fh) // 2
    d.rectangle([ax - 1, ay - 1, ax + fw + 1, ay + fh + 1], fill=(247, 242, 231, int(alpha * 0.85)))
    draw_flag(d, ax, ay, fw, fh)
    asc, desc = f.getmetrics()
    d.text((ax + fw + pad, (hpx - (asc + desc)) / 2 + 1), txt, font=f,
           fill=C_TEXT + (alpha,))
    CACHE_SPRITES[key] = img
    return img


# --------------------------------------------------------------------------- #
#  CALCUL DES SPRITES DE PAROLES (cache par cue)
# --------------------------------------------------------------------------- #
def cue_sprites(cue: Cue, text_font: str, color_active=C_TEXT,
                color_idle=(214, 208, 198), max_w=None, size0=78, size_min=46):
    """Retourne (sprite_idle, sprite_active, ligne_hauteur) pour une cue."""
    key = (cue.text, text_font, max_w, cue.kind)
    if key in CACHE_SPRITES:
        return CACHE_SPRITES[key]
    max_w = max_w or int(W * 0.76)
    tmp = ImageDraw.Draw(Image.new("L", (8, 8)))
    txt = clean_display(cue.text) if cue.kind == "lyric" or cue.kind == "refrain" else cue.text
    if cue.kind == "jingle":
        f = load_font("mont", 44, 800)
        lines, size = wrap_text(tmp, txt.upper(), f, max_w), 44
        sprite_idle, ys, step = make_text_sprite(lines, "mont", size, 1.2, C_ACCENT + (255,), weight=800)
        sprite_act = sprite_idle
    elif cue.kind == "didascalie":
        f = load_font("mont_it", 40)
        lines = wrap_text(tmp, txt, f, max_w)
        sprite_idle, ys, step = make_text_sprite(lines, "mont_it", 40, 1.2, (225, 221, 214, 230),
                                                 weight=600, stroke=2)
        sprite_act = sprite_idle
    else:
        s0 = size0
        if len(txt) > 62:
            s0 = int(size0 * 0.82)
        lines, size, lh = fit_wrap(tmp, txt, text_font, max_w, 3, s0, size_min)
        cue.lines, cue.size = lines, size
        weight = 700 if text_font == "mont" else 600
        stroke = 3 if text_font == "mont" else 4
        sprite_idle, ys, step = make_text_sprite(lines, text_font, size, lh, (232, 228, 220, 175),
                                                 weight=weight, stroke=stroke)
        sprite_act, _, _ = make_text_sprite(lines, text_font, size, lh, color_active + (255,),
                                            glow=(255, 214, 140), glow_strength=0.7,
                                            weight=weight, stroke=stroke)
    CACHE_SPRITES[key] = (sprite_idle, sprite_act, step)
    return CACHE_SPRITES[key]


STYLES_STYLE_GLOW = {"mont": (255, 214, 140), "playfair": (255, 214, 140), "dejavu": None}


# --------------------------------------------------------------------------- #
#  LAYOUT : position des blocs dans le cadre (§0 paroles centrées H/2)
# --------------------------------------------------------------------------- #
LYR_CY = 0.52          # centre vertical du bloc de paroles (réglable --cy)


def place_center(img, sprite, cx, cy, alpha=1.0):
    if alpha <= 0.01:
        return
    x, y = int(cx - sprite.width / 2), int(cy - sprite.height / 2)
    if alpha < 0.999:
        s = sprite.copy()
        a = s.getchannel("A").point(lambda v: int(v * alpha))
        s.putalpha(a)
        img.alpha_composite(s, (x, y))
    else:
        img.alpha_composite(sprite, (x, y))


def ctx_sprite(cue: Cue, text_font: str):
    """Sprite « ligne voisine » : réduit, flouté, faible opacité (cache)."""
    key = ("ctx", cue.text, text_font)
    if key in CACHE_SPRITES:
        return CACHE_SPRITES[key]
    idle, _, step = cue_sprites(cue, text_font)
    fs = idle.resize((max(1, int(idle.width * 0.60)), max(1, int(idle.height * 0.60))), Image.LANCZOS)
    fs = fs.filter(ImageFilter.GaussianBlur(2.6))
    a = fs.getchannel("A").point(lambda v: int(v * 0.46))
    fs.putalpha(a)
    CACHE_SPRITES[key] = (fs, step)
    return CACHE_SPRITES[key]


def render_lyrics(img, cue, prev_cue, next_cue, t, text_font, karaoke="wipe"):
    """Dessine la ligne courante centrée H/2 + contexte (précédente / suivante)."""
    cx, cy = W / 2, H * LYR_CY
    idle, act, step = cue_sprites(cue, text_font)

    # contexte (lignes voisines, très discrètes)
    for c, oy in ((prev_cue, -1), (next_cue, +1)):
        if c is None:
            continue
        fs, st = ctx_sprite(c, text_font)
        if oy < 0:
            yy = cy - step * 0.95 - fs.height / 2
        else:
            yy = cy + step * 1.30 + fs.height / 2
        place_center(img, fs, cx, yy, 1.0)

    # apparition douce (0,30 s)
    appear = min(1.0, max(0.0, (t - cue.start + 0.30) / 0.30))
    yoff = int((1 - appear) * 22)
    if cue.kind in ("jingle", "didascalie"):
        place_center(img, idle, cx, cy + yoff, 0.55 + 0.45 * appear)
        return
    place_center(img, idle, cx, cy + yoff, 0.85)
    prog = 0.0
    if cue.end > cue.start:
        prog = min(1.0, max(0.0, (t - cue.start) / (cue.end - cue.start)))
    prog = prog ** 0.92
    if prog <= 0.001:
        return
    if karaoke == "mot" and cue.lines:
        prog = min(1.0, prog * 1.06)
    mask = Image.new("L", (act.width, act.height), 0)
    md = ImageDraw.Draw(mask)
    xw = int(act.width * prog)
    if xw > 0:
        md.rectangle([0, 0, xw, act.height], fill=255)
        if prog < 1.0:
            md.rectangle([max(0, xw - 26), 0, xw, act.height], fill=140)
    filled = Image.new("RGBA", (act.width, act.height), (0, 0, 0, 0))
    filled.paste(act, (0, 0), mask)
    place_center(img, filled, cx, cy + yoff, 1.0)


# --------------------------------------------------------------------------- #
#  AUDIO : master normalisé
# --------------------------------------------------------------------------- #
def ffmpeg_exe() -> str:
    """ffmpeg : variable FFMPEG > binaire du système (Termux : pkg install ffmpeg)
    > binaire embarqué fourni par imageio-ffmpeg."""
    import shutil
    env = os.environ.get("FFMPEG")
    if env and os.path.exists(env):
        return env
    sys_ff = shutil.which("ffmpeg")
    if sys_ff:
        return sys_ff
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def run(cmd, **kw):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kw)
    if p.returncode != 0:
        tail = p.stdout.decode("utf-8", "replace")[-1800:]
        raise SystemExit(f"[dsky] échec commande : {' '.join(cmd[:6])}…\n{tail}")
    return p.stdout.decode("utf-8", "replace")


def probe_duration(path: str) -> float:
    out = run([ffmpeg_exe(), "-hide_banner", "-i", path, "-f", "null", "-"])
    m = re.findall(r"time=(\d+):(\d+):([\d.]+)", out)
    if not m:
        raise SystemExit(f"[dsky] durée indécodable : {path}")
    h, mi, s = m[-1]
    return int(h) * 3600 + int(mi) * 60 + float(s)


def master_audio(src: str, out_wav: str, target_i=-14.0, tp=-1.8):
    ff = ffmpeg_exe()
    p1 = run([ff, "-hide_banner", "-i", src, "-af",
              f"loudnorm=I={target_i}:TP={tp}:LRA=11:print_format=json",
              "-f", "null", "-"])
    blob = re.findall(r"\{[^{}]*input_i[^{}]*\}", p1, re.S)
    meas = json.loads(blob[-1]) if blob else {}
    af = (f"loudnorm=I={target_i}:TP={tp}:LRA=11"
          f":measured_I={meas.get('input_i', -24)}:measured_TP={meas.get('input_tp', -2)}"
          f":measured_LRA={meas.get('input_lra', 7)}:measured_thresh={meas.get('input_thresh', -34)}"
          f":offset={meas.get('target_offset', 0)}:linear=true,highpass=30,lowpass=18000")
    run([ff, "-y", "-hide_banner", "-i", src, "-af", af, "-ar", "48000", "-ac", "2", out_wav])
    return meas


# --------------------------------------------------------------------------- #
#  SRT
# --------------------------------------------------------------------------- #
def fmt_ts(t: float) -> str:
    t = max(0.0, t)
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        s, ms = s + 1, 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(path: str, cues: list[Cue], offset=0.0):
    lines, n = [], 0
    for c in cues:
        if c.kind == "didascalie" and len(clean_display(c.text)) < 4:
            continue
        n += 1
        txt = clean_display(c.text)
        lines += [str(n), f"{fmt_ts(c.start + offset)} --> {fmt_ts(c.end + offset)}", txt, ""]
    open(path, "w", encoding="utf-8").write("\n".join(lines))


# --------------------------------------------------------------------------- #
#  RENDU
# --------------------------------------------------------------------------- #
def render_frames(scene: Scene, cues: list[Cue], duration: float,
                  text_font="mont", karaoke="wipe", endcard: dict | None = None,
                  intro: dict | None = None, t_from: float = 0.0):
    """Générateur de frames PIL (t, image).  t_from évite de recalculer un préambule."""
    n_frames = int(math.ceil(duration * FPS_DEF))
    i0 = int(t_from * FPS_DEF)
    slots = [(c.slot, c.start, c.end) for c in cues]
    for i in range(i0, n_frames):
        t = i / FPS_DEF
        # plan courant (dernier cue commencé) + crossfade 0,55 s
        idx = 0
        for k, (s, a, b) in enumerate(slots):
            if t >= a - 0.55:
                idx = k
        slot, s_start, s_end = slots[idx] if slots else (0, 0, duration)
        prev_slot = slots[max(0, idx - 1)][0] if slots else 0
        mix = 0.0
        if idx > 0 and t < s_start:
            mix = 1.0 - max(0.0, (t - (s_start - 0.55)) / 0.55)
        img = scene.background(slot, t - s_start, t - s_start, mix, prev_slot)
        cur = prev = nxt = None
        for k, c in enumerate(cues):
            if c.start <= t < c.end:
                cur = c
                prev = cues[k - 1] if k else None
                nxt = cues[k + 1] if k + 1 < len(cues) else None
                break
        img = scene.frame(img, t, slot)
        if cur is not None:
            render_lyrics(img, cur, prev, nxt, t, text_font, karaoke)
        # badge discret : vivant avec les paroles
        if cur is not None:
            b = make_badge()
            fade = 0.4
            a = min(1.0, max(0.0, (t - cur.start) / fade), max(0.0, (cur.end - t) / fade))
            place_center(img, b, W / 2, 150, a * 0.95)
        if intro and intro["start"] <= t <= intro["end"]:
            fade = min(1.0, (t - intro["start"]) / 0.8, (intro["end"] - t) / 0.8 + 0.25)
            place_center(img, intro["sprite"], W / 2, intro["cy"], min(1.0, max(0.0, fade)))
        if endcard and t >= endcard["start"] - 0.6:
            eapp = min(1.0, max(0.0, (t - (endcard["start"] - 0.6)) / 0.6))
            place_center(img, endcard["sprite"], W / 2, endcard["cy"], eapp)
            b = make_badge()
            place_center(img, b, W / 2, 150, 0.8)
        # fondu final
        if duration - t < 1.6:
            k = max(0.0, (duration - t) / 1.6)
            black = Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - k))))
            img.alpha_composite(black)
        yield t, img.convert("RGB")


def make_intro_card(title: str) -> Image.Image:
    """Carte de titre pendant l'intro instrumentale (sans texte des paroles)."""
    img = Image.new("RGBA", (W, 420), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = 40
    f = load_font("playfair_it", 92, 500)
    for ln in wrap_text(d, title, f, int(W * 0.80)):
        d.text(((W - text_w(d, ln, f)) / 2 + 2, y + 2), ln, font=f, fill=(0, 0, 0, 150))
        d.text(((W - text_w(d, ln, f)) / 2, y), ln, font=f, fill=C_TEXT + (255,))
        y += 104
    d.rectangle([W / 2 - 44, y + 22, W / 2 + 44, y + 26], fill=C_ACCENT + (255,))
    fs = load_font("mont", 27, 700)
    for txt, dy, col in ((SIGNATURE, y + 62, C_TEXT + (240,)),
                         (SIGN_SUB, y + 108, C_ACCENT + (235,))):
        d.text(((W - text_w(d, txt, fs)) / 2, dy), txt, font=fs, fill=col)
    return img


def make_endcard(title: str) -> tuple[Image.Image, float]:
    """Carte finale : titre cursif + contacts + badge (contacts §0.3)."""
    img = Image.new("RGBA", (W, 900), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = 30
    f = load_font("playfair_it", 124)
    lines = wrap_text(d, title, f, int(W * 0.82))
    for ln in lines:
        d.text(((W - text_w(d, ln, f)) / 2, y), ln, font=f, fill=C_TEXT + (255,))
        y += 132
    y += 26
    d.rectangle([W / 2 - 40, y, W / 2 + 40, y + 4], fill=C_ACCENT + (255,))
    y += 44
    for txt, fnt, col in ((SIGNATURE, ("mont", 34), C_TEXT + (240,)),
                          (SIGN_SUB, ("mont", 26), C_ACCENT + (235,)),
                          (f"WhatsApp {WHATSAPP}", ("mont", 24), (225, 220, 210, 225)),
                          (EMAIL, ("mont", 24), (225, 220, 210, 225))):
        ff = load_font(fnt[0], fnt[1])
        d.text(((W - text_w(d, txt, ff)) / 2, y), txt, font=ff, fill=col)
        y += int(fnt[1] * 1.7) + 10
    b = make_badge(scale=1.0)
    img.alpha_composite(b, (int(W / 2 - b.width / 2), y + 10))
    return img, sum(img.getchannel("A").getbbox()[3:]) / 2


# --------------------------------------------------------------------------- #
#  DETECTION AUTO DU STYLE
# --------------------------------------------------------------------------- #
def auto_style(entries: list[Entry]) -> str:
    txt = " ".join(e.text.lower() for e in entries)
    scores = {k: sum(txt.count(w) for w in ws) for k, ws in LEXIQUE.items()}
    return max(scores, key=scores.get) if max(scores.values()) > 0 else "dark"


# --------------------------------------------------------------------------- #
#  MAIN
# --------------------------------------------------------------------------- #
def main(argv=None):
    global FPS_DEF
    ap = argparse.ArgumentParser(description="DSKY lyric videos (karaoké 9:16)")
    ap.add_argument("--song", required=True, help="titre du morceau (approx.)")
    ap.add_argument("--fonds", default=None, help="dossier d'images (IA + photos réelles)")
    ap.add_argument("--photo", action="append", default=[], help="photo réelle (répétable)")
    ap.add_argument("--style", default="auto", choices=["auto", *STYLES.keys()])
    ap.add_argument("--texte", default="droit", choices=["droit", "cursive"])
    ap.add_argument("--karaoke", default="wipe", choices=["wipe", "mot"])
    ap.add_argument("--cy", type=float, default=0.52,
                    help="position verticale du bloc de paroles (0.30 haut … 0.66 bas)")
    ap.add_argument("--limit", type=float, default=0.0, help="rendu partiel (secondes)")
    ap.add_argument("--start", type=float, default=0.0, help="début du rendu partiel")
    ap.add_argument("--fps", type=int, default=FPS_DEF)
    ap.add_argument("--crf", type=int, default=19)
    ap.add_argument("--preview", action="store_true", help="4 PNG de contrôle, pas de vidéo")
    ap.add_argument("--no-endcard", action="store_true")
    ap.add_argument("--no-srt", action="store_true")
    args = ap.parse_args(argv)
    FPS_DEF = args.fps
    global LYR_CY
    LYR_CY = args.cy

    lyr_path, mp3_path = find_pair(args.song)
    log("paroles :", os.path.basename(lyr_path))
    log("master  :", os.path.basename(mp3_path))

    entries, length, sections = parse_lyrics(lyr_path)
    duration = probe_duration(mp3_path)
    log(f"durée audio : {duration:.2f} s · {len(entries)} lignes · {len(sections)} sections")

    title_key = norm_key(args.song)
    detect_refrains(entries, title_key)
    entries = normalize_timings(entries)
    cus = build_cues(entries, duration)
    # le titre (hook) : chercher une ligne qui contient le titre du morceau
    hook_cue = next((c for c in cus if c.kind == "refrain"), cus[min(4, len(cus) - 1)] if cus else None)
    log(f"{len(cus)} cues · refrain « {hook_cue.text if hook_cue else '—'} »")

    style = auto_style(entries) if args.style == "auto" else args.style
    log("style retenu :", style)

    # ---------- dossier de sortie ---------- #
    slug = re.sub(r"[^a-z0-9]+", "-", norm_key(args.song)).strip("-") or "clip"
    outdir = os.path.join(HERE, slug)
    workdir = os.path.join(outdir, "work")
    fondsdir = os.path.join(outdir, "fonds")
    os.makedirs(workdir, exist_ok=True)
    os.makedirs(fondsdir, exist_ok=True)

    # ---------- collecte des fonds ---------- #
    imgs: list[str] = []
    if args.fonds:
        d = args.fonds if os.path.isabs(args.fonds) else os.path.join(ROOT, args.fonds)
        if os.path.isdir(d):
            imgs += [os.path.join(d, f) for f in sorted(os.listdir(d))
                     if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
        elif os.path.isfile(d):
            imgs.append(d)
    for p in args.photo:
        imgs.append(p if os.path.isabs(p) else os.path.join(ROOT, p))
    if os.path.isdir(fondsdir):
        imgs += [os.path.join(fondsdir, f) for f in sorted(os.listdir(fondsdir))
                 if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
    seen, fonds_src = set(), []
    for p in imgs:
        if p not in seen and os.path.exists(p):
            seen.add(p)
            fonds_src.append(p)
    if not fonds_src:
        raise SystemExit(f"[dsky] aucun fond : dépose des images dans {fondsdir} "
                         f"ou passe --fonds DOSSIER / --photo FICHIER")
    log(f"{len(fonds_src)} fonds :", [os.path.basename(p) for p in fonds_src])

    text_font = "mont" if args.texte == "droit" else "playfair"
    scene = Scene(style, [(p, os.path.basename(p)) for p in fonds_src])

    # ---------- endcard + carte de titre (intro) ---------- #
    last_end = max((c.end for c in cus), default=duration - 5)
    end_start = max(duration - 4.6, last_end + 0.5)
    if end_start > duration - 1.0:                      # pas la place : on décale la fin
        end_start = min(duration - 0.8, last_end + 0.3)
    endcard = None
    if not args.no_endcard:
        title_txt = args.song.split(" - ")[0].strip()
        if title_txt.islower():
            title_txt = title_txt[0].upper() + title_txt[1:]
        sp, _ = make_endcard(title_txt)
        endcard = {"start": end_start, "sprite": sp, "cy": H * 0.5 - 30}
        log(f"endcard à {end_start:.1f} s")

    # carte de titre pendant l'intro instrumentale
    intro = None
    if cus and cus[0].start >= 5.5:
        intro = {"start": 1.2, "end": cus[0].start - 0.35,
                 "sprite": make_intro_card(title_txt), "cy": H * 0.44}
        log(f"intro {intro['start']:.1f} → {intro['end']:.1f} s")

    total = duration
    # ---------- preview ---------- #
    if args.preview:
        tmax = (args.start + args.limit) if args.limit else duration
        tmin = args.start
        picks = [tmin + 0.4,
                 hook_cue.start + 0.8 if hook_cue else tmin,
                 (cus[len(cus) // 2].start + 0.6) if cus else tmin,
                 min(duration - 2.2, tmax - 0.4),
                 min(duration - 1.6, tmax - 0.2)]
        picks = sorted({round(min(max(t, tmin), tmax), 2) for t in picks})
        for k, t in enumerate(picks):
            for tt, im in render_frames(scene, cus, duration, text_font=text_font,
                                        karaoke=args.karaoke, endcard=endcard, intro=intro,
                                        t_from=max(0.0, t - 0.05)):
                if tt >= t - 0.001:
                    outp = os.path.join(workdir, f"preview_{k+1}_t{t:06.1f}s.png")
                    im.save(outp)
                    log("preview →", os.path.basename(outp))
                    break
        return

    # ---------- rendu vidéo ---------- #
    start = max(0.0, args.start)
    dur = (min(total, start + args.limit) - start) if args.limit else total - start
    n_frames = int(math.ceil(dur * args.fps))
    video_raw = os.path.join(workdir, "video.mp4")
    ff = ffmpeg_exe()
    cmd = [ff, "-y", "-hide_banner", "-loglevel", "error",
           "-f", "image2pipe", "-framerate", str(args.fps), "-vcodec", "mjpeg", "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", str(args.crf),
           "-pix_fmt", "yuv420p", "-r", str(args.fps), video_raw]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                            stderr=subprocess.PIPE)
    log(f"rendu {n_frames} frames ({dur:.1f} s @ {args.fps} fps)…")
    import time as _time
    t0 = _time.time()
    for k, (t, im) in enumerate(render_frames(scene, cus, total, text_font=text_font,
                                              karaoke=args.karaoke, endcard=endcard,
                                              intro=intro)):
        if t < start:
            continue
        if t > start + dur:
            break
        im.save(proc.stdin, "JPEG", quality=JPEG_Q, optimize=False, subsampling=0)
        if k % 150 == 0 and k:
            el = _time.time() - t0
            log(f"  {t:6.1f} s  ({k / max(el, .01):4.1f} fps, reste "
                f"~{(n_frames - k) / max(k / max(el, .01), .01) / 60:4.1f} min)")
    proc.stdin.close()
    err = proc.stderr.read().decode("utf-8", "replace")
    if proc.wait() != 0:
        raise SystemExit("[dsky] ffmpeg vidéo KO:\n" + err[-1500:])

    # ---------- audio master ---------- #
    wav = os.path.join(workdir, "master.wav")
    master_audio(mp3_path, wav)
    title = re.sub(r"[^\w \-'’()À-ÿ]+", "", args.song.split(" - ")[0]).strip()
    mp3_out = os.path.join(outdir, f"{title}_master_320k.mp3")
    run([ff, "-y", "-hide_banner", "-i", wav, "-c:a", "libmp3lame", "-b:a", "320k",
         "-ar", "48000", "-metadata", f"title={title}", "-metadata", "artist=Daïsky",
         "-metadata", "album=DSKY Lyric Videos", "-metadata", f"TXXX=contact:{WHATSAPP}",
         mp3_out])

    # ---------- mux final ---------- #
    mp4_out = os.path.join(outdir, f"{title}_9x16.mp4")
    af = "afade=t=out:st={:.2f}:d=1.4,afade=t=in:st=0:d=0.5".format(max(0, dur - 1.6))
    run([ff, "-y", "-hide_banner", "-loglevel", "error", "-i", video_raw, "-i", wav,
         "-filter_complex", f"[1:a]{af}[a]", "-map", "0:v", "-map", "[a]",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
         "-shortest", mp4_out])
    log("vidéo →", mp4_out, f"({os.path.getsize(mp4_out)/1e6:.1f} Mo)")

    if not args.no_srt:
        srt = os.path.join(outdir, f"{title}.srt")
        write_srt(srt, cus)
        log("srt   →", srt)

    json.dump({"song": args.song, "style": style, "texte": text_font, "fps": args.fps,
               "duration": duration, "cues": [{"s": c.start, "e": c.end, "t": c.text,
                                               "k": c.kind, "slot": c.slot} for c in cus]},
              open(os.path.join(outdir, "timings.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    log("terminé.")


if __name__ == "__main__":
    main()
