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

# 11,036,159 decoded samples at 48 kHz (229.919979… s), rounded to centiseconds.
# This changes only the inferred end of the final segment, never a source timestamp.
AUDIO_DURATION_S = round(11_036_159 / 48_000, 2)
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
        return "MULTILINGUE (JA+ES+FR+MONWÊ)"
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
            translation = "Merci, merci, merci — c'est confirmé."
            translation_status = "traduction retenue selon gloss artiste : monwê = « c'est ça / c'est confirmé »"
        reprise = first_i != i or is_final_chorus
        item = {
            "i": i,
            "source_timestamp": row["source_timestamp"],
            "fin_timestamp": timestamp(next_t),
            "t": round(row["t"], 2),
            "fin": round(next_t, 2),
            "affichage_s": round(display_s, 2),
            "affichage_statut": "provisoire — formule v6.0",
            # No sung-end or word alignment was supplied. Keep lyrics legible through
            # the next source start, except the exceptionally long final signature gap.
            "rendu_affichage_s": round(display_s if i == 57 else next_t - row["t"], 2),
            "rendu_affichage_statut": ("provisoire — signature, longue pause supposée" if i == 57
                                      else "provisoire — jusqu'au début source suivant"),
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
        "> Durée décodée : 11 036 159 échantillons / 48 000 Hz = 229,919979 s, soit 3:49.92 au centième.",
        "> L’heuristique `affichage_s` v6.0 et la durée réellement retenue au rendu restent provisoires, faute de calage mot à mot.",
        "> `disponible` est recalculé depuis l’existence réelle du fichier image.",
        "",
        "| # | Début | Fin | Vers source | Langue | Traduction FR | Image | Dispo. | Reprise | Heuristique (s) | Rendu (s) |",
        "|---:|:---:|:---:|---|---|---|---|:---:|---|---:|---:|",
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
            f"{'oui' if row['disponible'] else 'non'} | {reprise} | {row['affichage_s']:.2f} | {row['rendu_affichage_s']:.2f} |"
        )
    lines.extend(
        [
            "",
            "## À relire avant rendu",
            "",
            "- Traduction FR retenue pour le vers multilingue `Arigato, gracias, merci, monwê` : `Merci, merci, merci — c'est confirmé.` (gloss artiste : monwê = « c'est ça / c'est confirmé »).",
            "- Les lignes non françaises gardent leurs paroles originales peintes; la traduction française défile dans la pilule basse v6.0.",
            "- Les variantes de l’ultime refrain et de l’outro suivent l’arc d’aube.",
            "- Au montage, on maintient chaque vers lisible jusqu’au début source du suivant plutôt que de l’éteindre au seul calcul de vitesse de lecture. Exception provisoire : signature n°57, extinction après 2,20 s dans la longue pause supposée. La clochette prévue entre 3:28 et 3:32,5 reste à vérifier à l’écoute.",
            "- Le montage utilise des coupes nettes entre vers pour ne pas superposer ni dédoubler les lettrages peints; le calage fin reste à valider à l’écoute.",
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
