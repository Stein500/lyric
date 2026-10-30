#!/usr/bin/env python3
"""Build the verse map and its human-readable card from the artist's timed lyrics."""
from __future__ import annotations

import json
import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
REPO = PROJECT.parents[1]
LYRICS = REPO / "Je me relève toujours.txt"
OUTPUT_JSON = PROJECT / "verses_map.json"
OUTPUT_MD = PROJECT / "CARTE-VERS.md"

# Decoded from the supplied master with ffmpeg 7.0.2. Keep source timestamps intact.
AUDIO_DURATION_S = 229.91
FINAL_CHORUS_INDICES = {53, 54, 55, 56, 57}
OUTRO_INDICES = {58}

ENGLISH = "Yeah... I'm still standing..."
MULTILINGUAL = "Arigato, gracias, merci, monwê"
TRANSLATIONS = {
    ENGLISH: "Ouais... je suis toujours debout...",
}

TIMED_LINE = re.compile(r"^\[(\d{2}):(\d{2})\.(\d{2})\](.*)$")


def to_seconds(minutes: str, seconds: str, centiseconds: str) -> float:
    return int(minutes) * 60 + int(seconds) + int(centiseconds) / 100


def timestamp(seconds: float) -> str:
    whole_minutes = int(seconds // 60)
    remainder = seconds - whole_minutes * 60
    return f"{whole_minutes:02d}:{remainder:05.2f}"


def language_for(text: str) -> str:
    if text.startswith("Wolof TechStein beat wê"):
        return "WTBW"
    if text == ENGLISH:
        return "EN"
    if text == MULTILINGUAL:
        return "MULTILINGUE (JA+ES+FR+INCONNUE)"
    return "FR"


def read_lyrics() -> list[dict]:
    rows = []
    for raw_line in LYRICS.read_text(encoding="utf-8").splitlines():
        match = TIMED_LINE.match(raw_line)
        if not match:
            continue
        minutes, seconds, centiseconds, text = match.groups()
        rows.append(
            {
                "source_timestamp": f"{minutes}:{seconds}.{centiseconds}",
                "t": to_seconds(minutes, seconds, centiseconds),
                "texte": text,
            }
        )
    return rows


def build() -> list[dict]:
    source = read_lyrics()
    first_by_text: dict[str, tuple[int, int]] = {}
    for i, row in enumerate(source, 1):
        if row["texte"] not in first_by_text:
            first_by_text[row["texte"]] = (i, len(first_by_text) + 1)

    result = []
    for i, row in enumerate(source, 1):
        text = row["texte"]
        first_i, scene_id = first_by_text[text]
        base_name = f"scene-{scene_id:02d}"
        if scene_id == 1:
            base_name += "-ancre"
        is_final_chorus = i in FINAL_CHORUS_INDICES
        is_outro = i in OUTRO_INDICES
        image_name = base_name + ("-aube" if is_final_chorus else "") + ".png"
        image_rel = f"fonds/{image_name}"
        image_abs = PROJECT / image_rel
        next_t = source[i]["t"] if i < len(source) else AUDIO_DURATION_S
        display_s = min(next_t - row["t"], max(2.2, 0.30 * len(text.split())))
        lang = language_for(text)
        translation = TRANSLATIONS.get(text, "")
        translation_status = "sans traduction" if lang in {"FR", "WTBW"} else "provisoire"
        if text == MULTILINGUAL:
            translation = None
            translation_status = "à confirmer : sens de « monwê » non établi"
        reprise = first_i != i or is_final_chorus
        item = {
            "i": i,
            "source_timestamp": row["source_timestamp"],
            "fin_timestamp": timestamp(next_t),
            "t": round(row["t"], 2),
            "fin": round(next_t, 2),
            "affichage_s": round(display_s, 2),
            "affichage_statut": "provisoire — formule v6.0",
            "texte": text,
            "langue": lang,
            "traduction_fr": translation,
            "traduction_statut": translation_status,
            "image": image_rel,
            "disponible": image_abs.exists(),
            "reprise": reprise,
            "reprise_de": first_i if reprise else None,
            "variante": "aube" if is_final_chorus or is_outro else "standard",
        }
        # The last signature reprise after the bridge is a sunrise-specific variant.
        if i == 57:
            item["image"] = f"fonds/{base_name}-aube.png"
            item["disponible"] = (PROJECT / item["image"]).exists()
            item["variante"] = "aube"
        # The single outro line is unique and its base image itself is the dawn version.
        if is_outro:
            item["variante"] = "aube_outro"
        result.append(item)
    return result


def write_card(rows: list[dict]) -> None:
    lines = [
        "# Carte des vers — Je me relève toujours",
        "",
        "> Générée depuis `verses_map.json` et les horodatages de `Je me relève toujours.txt`.",
        "> Durée décodée du maître : 229,91 s (3:49.91). `affichage_s` reste provisoire selon la formule v6.0.",
        "> `disponible` est recalculé depuis l’existence réelle du fichier image.",
        "",
        "| # | Début | Fin | Vers source | Langue | Traduction FR | Image | Dispo. | Reprise | Affichage (s) |",
        "|---:|:---:|:---:|---|---|---|---|:---:|---|---:|",
    ]
    for row in rows:
        translation = row["traduction_fr"]
        if translation is None:
            translation = "À confirmer"
        elif not translation:
            translation = "—"
        translation = str(translation).replace("|", "\\|").replace("\n", " ")
        text = row["texte"].replace("|", "\\|").replace("\n", " ")
        reprise = f"oui (vers {row['reprise_de']})" if row["reprise"] else "non"
        lines.append(
            f"| {row['i']} | {row['source_timestamp']} | {row['fin_timestamp']} | {text} | "
            f"{row['langue']} | {translation} | `{row['image']}` | "
            f"{'oui' if row['disponible'] else 'non'} | {reprise} | {row['affichage_s']:.2f} |"
        )
    lines.extend(
        [
            "",
            "## À relire avant rendu",
            "",
            "- Traduction du vers multilingue `Arigato, gracias, merci, monwê` en attente de clarification sur `monwê`.",
            "- Les lignes non françaises gardent leurs paroles originales peintes; la traduction française défile dans la pilule basse v6.0.",
            "- Les variantes de l’ultime refrain et de l’outro suivent l’arc d’aube; aucun résultat de rendu n’est encore déclaré.",
            "",
        ]
    )
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = build()
    OUTPUT_JSON.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_card(rows)
    print(f"Vers: {len(rows)}; textes distincts: {len({r['texte'] for r in rows})}")
    print(f"Map: {OUTPUT_JSON.relative_to(REPO)}")
    print(f"Carte: {OUTPUT_MD.relative_to(REPO)}")
    available_rows = sum(r["disponible"] for r in rows)
    distinct_paths = {r["image"] for r in rows}
    available_paths = sum((PROJECT / path).exists() for path in distinct_paths)
    print(f"Occurrences avec image disponible: {available_rows}/{len(rows)}")
    print(f"Fichiers image distincts disponibles: {available_paths}/{len(distinct_paths)}")


if __name__ == "__main__":
    main()
