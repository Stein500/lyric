import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = Path(__file__).resolve().parent
LYRICS_FILE = ROOT / "Ghost u see.txt"

TRANSLATIONS = {
    "00:54.66": "Ne m’appelle pas par ce nom que j’ai laissé derrière moi.",
    "00:59.26": "Le fantôme que tu as bâti vit dans ton esprit.",
    "01:02.51": "Toutes les histoires que tu racontais n’ont jamais été les miennes.",
    "01:06.03": "Je réécris chaque ligne brisée et effacée.",
    "01:10.75": "Le fantôme que tu vois, ce n’est pas moi.",
    "01:24.62": "Le fantôme que tu vois, ce n’est pas moi.",
    "01:38.87": "Je ne suis ni l’ombre, ni le silence.",
    "01:42.39": "Je ne suis pas la blessure derrière ta violence.",
    "01:45.48": "Le fantôme que tu vois, ce n’est pas moi.",
    "01:53.48": "J’ai construit mon monde loin de ton regard.",
    "01:56.41": "Chaque pas que j’ai fait fut une nouvelle flamme.",
    "01:59.98": "Tu m’as peint en gris, mais je suis un arc-en-ciel.",
    "02:03.32": "Mes racines sont fortes, même si le vent dévie ma route.",
    "02:07.07": "Je ne suis pas le fantôme que tu as laissé derrière toi.",
    "02:10.43": "Je ne suis pas le miroir brisé que tu ne veux plus.",
    "02:13.96": "Il y a du feu dans mes veines, de la lumière dans ma voix.",
    "02:17.46": "L’âme que tu cherches ne vit plus en deux.",
    "02:49.13": "Le fantôme que tu vois, ce n’est pas moi.",
    "02:55.00": "J’ai brûlé l’ancienne peau que tu voulais garder.",
    "03:02.85": "Le fantôme que tu vois, ce n’est pas moi.",
    "03:17.11": "Je ne suis ni l’ombre, ni le silence.",
    "03:20.74": "Je ne suis pas la blessure derrière ta violence.",
    "03:23.76": "Le fantôme que tu vois, ce n’est pas moi.",
}

SCENE_PLAN = [
    {"start": 0.0, "end": 27.20, "image": "scene01_cold_stage.png"},
    {"start": 27.20, "end": 54.66, "image": "scene02_reflection_hall.png"},
    {"start": 54.66, "end": 70.75, "image": "scene04_studio_window.png"},
    {"start": 70.75, "end": 98.87, "image": "scene03_rooftop_dawn.png"},
    {"start": 98.87, "end": 113.48, "image": "scene04_studio_window.png"},
    {"start": 113.48, "end": 140.81, "image": "scene05_gallery_woman.png"},
    {"start": 140.81, "end": 169.13, "image": "scene02_reflection_hall.png"},
    {"start": 169.13, "end": 197.11, "image": "scene06_morning_crossing.png"},
    {"start": 197.11, "end": 211.87, "image": "scene03_rooftop_dawn.png"},
    {"start": 211.87, "end": 250.01, "image": "scene06_morning_crossing.png"},
]


def main():
    verses = []
    pattern = re.compile(r"\[(\d{2}):(\d{2})\.(\d{2})\](.*)")
    for raw in LYRICS_FILE.read_text(encoding="utf-8").splitlines():
        match = pattern.match(raw)
        if not match:
            continue
        minute, second, centisecond, text = match.groups()
        timestamp = f"{minute}:{second}.{centisecond}"
        start = int(minute) * 60 + int(second) + int(centisecond) / 100
        verses.append({"id": f"v{len(verses) + 1:02d}", "start": round(start, 2),
                       "timestamp": timestamp, "text": text.strip(),
                       "type": "humming" if text.strip().startswith("(Humming") else "lyric"})
    for i, verse in enumerate(verses):
        verse["end"] = verses[i + 1]["start"] if i + 1 < len(verses) else 245.006
        if verse["timestamp"] in TRANSLATIONS:
            verse["fr"] = TRANSLATIONS[verse["timestamp"]]
    data = {
        "title": "Ghost u see", "artist": "Daïsky", "badge": "DSKY",
        "series": "WTBW · Wolof TechStein beat wê",
        "mode": "B — paroles originales peintes + traduction française karaoke en pilule",
        "audio": "../../Ghost'u_see- Daïsky.m4a", "audio_duration": 245.006,
        "video_duration": 250.006, "resolution": [1080, 1920], "fps": 30,
        "transition_seconds": 0.35, "scene_plan": SCENE_PLAN, "verses": verses,
    }
    (PROJECT / "verses_map.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    translated = sum("fr" in verse for verse in verses)
    print(f"Mapped {len(verses)} timed lines; {translated} French translations; {data['audio_duration']:.3f}s master.")


if __name__ == "__main__":
    main()
