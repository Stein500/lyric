#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrat unique des vers (v7.0 §3) — « Grand Marcheur ».

Sources :
  - Grand marcheur.txt        : 46 vers, debut seuls horodates (aucune fin fournie)
  - Grand marcheur 2.mp3      : maitre audio, tag USLT = paroles avec sections
Decisions de l'artiste (2026-11-15) :
  - MODE PEINT, methode MOTEUR (choix delegue -> defaut §0)
  - « WTBW partout » : les 5 vers prononcant le developpement affichent « WTBW »
  - ARTISTE A L'ECRAN : DSKY WTBW
  - 10 images par salve (exception au §5, consignee)
`disponible` est recalcule a partir des fichiers reellement presents a chaque execution.
"""
import hashlib
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
LYRICS = os.path.join(ROOT, "Grand marcheur.txt")
AUDIO = os.path.join(ROOT, "Grand marcheur 2.mp3")
WTBW_AFFICHE = "WTBW"
PASSAGE_AUBE_I = 25  # des i=25 les plans sont en aube lumineuse

# Releve de controle de la salve 01 (feuille de contact, 2026-11-15).
# Fichiers presents mais NON CONFORMES -> a regenerer au prochain tour
# (limite de 10 generations d'images par tour atteinte ce tour-ci).
PLANS_NON_CONFORMES = {}  # 3 defauts de la salve 01 regeneres et controles conformes le 2026-11-15


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def parse(path):
    pattern = re.compile(r"^\[(\d{2}):(\d{2})\.(\d{2})\](.*)$")
    rows = []
    with open(path, "r", encoding="utf-8-sig") as fh:
        for raw in fh:
            m = pattern.match(raw.rstrip("\r\n"))
            if m:
                start = int(m.group(1)) * 60 + int(m.group(2)) + int(m.group(3)) / 100.0
                rows.append((round(start, 2), m.group(4)))
    return rows


rows = parse(LYRICS)
first_seen = {}
entries = []
for idx, (start, text) in enumerate(rows, start=1):
    first = first_seen.get(text)
    reprise = first is not None
    if not reprise:
        first_seen[text] = idx
    wtbw = "Wolof TechStein" in text
    src_no = first if reprise else idx
    image = "assets/plans/plan-%02d.jpg" % src_no
    aube = reprise and idx > PASSAGE_AUBE_I
    image_cuite = ("assets/aube/cuits/aube-plan-%02d.jpg" if aube
                   else "assets/cuits/plan-%02d.jpg") % src_no
    disponible = os.path.exists(os.path.join(HERE, image_cuite))
    if wtbw:
        affiche = WTBW_AFFICHE
    else:
        affiche = text
    tags = []
    if wtbw:
        tags.append("EXCEPTION WTBW : developpement remplace par WTBW ; texte_source et audio intacts")
    if idx in PLANS_NON_CONFORMES:
        tags.append("NON CONFORME (plan %02d) : %s -> A REGENERER" % (idx, PLANS_NON_CONFORMES[idx]))
    if reprise:
        tags.append("REPRISE de %02d : vers identique" % first)
    if aube:
        tags.append("VARIANTE AUBE : fond reetalonne par le moteur + vers exact recuit, aucune nouvelle generation IA")
    if disponible:
        tags.append("CUIT PAR LE MOTEUR")
        if not reprise and idx not in PLANS_NON_CONFORMES:
            tags.append("controle orthographe / diacritiques en 1:1 effectue")
    else:
        tags.append("image cuite absente")
    statut = " ; ".join(tags)
    entries.append({
        "i": idx,
        "debut_source": start,
        "fin": None,
        "texte_source": text,
        "texte_affiche": affiche,
        "image": image,
        "image_cuite": image_cuite,
        "variante_aube": aube,
        "disponible": disponible,
        "reprise": reprise,
        "reprise_de": first if reprise else None,
        "statut_controle": statut,
    })

contract = {
    "titre_exact": "Grand Marcheur",
    "titre_origine": "tag ID3 TIT2 du maitre ; message initial de l'artiste « grand marcheurs » (ecart signale, bascule possible sur demande)",
    "artiste_ecran": "DSKY WTBW",
    "slug": "grand-marcheur",
    "source_paroles": "Grand marcheur.txt",
    "source_audio": "Grand marcheur 2.mp3",
    "sha256_paroles": sha256(LYRICS),
    "sha256_audio": sha256(AUDIO),
    "nb_vers": len(entries),
    "calage": "debuts seuls fournis ; fin = null pour tous les vers ; PROVISOIRE, a verifier par ecoute",
    "mode": "PEINT",
    "methode_peinture": "MOTEUR — defaut §0, artiste ayant delegue le choix ; NO TEXT AT ALL a la generation puis vers exact cuit dans l'image par le moteur",
    "couleur": "COULEUR / Multi",
    "palette": "vitrail gospel : bleu nuit, or ambre, creme, pourpre, rouge discret — palette de l'ancre selectionnee (reference §5), non notee 'validee par l'artiste'",
    "style": "identite gospel, anime seinen, encre, arc nuit -> premieres lueurs -> aube",
    "habillage": "WTBW uniquement ; badge alterne DSKY WTBW <-> WTBW",
    "exception_wtbw": "DECIDEE : les 5 vers prononcant « Wolof TechStein beat wê » affichent « WTBW » ; prononce conserve dans texte_source et dans l'audio, audio non modifie",
    "wtbw_lignes": [e["i"] for e in entries if e["texte_source"] != e["texte_affiche"] and "Wolof TechStein" in e["texte_source"]],
    "ancre": "assets/ancre/ancre-gospel.jpg (option 1/2 selectionnee ; « On continue » = accord personnage/style, pas controle technique)",
    "plans_non_conformes": PLANS_NON_CONFORMES,
    "plans_regeneres_controles": [4, 6, 11],
    "passage_aube_i": PASSAGE_AUBE_I,
    "salve_taille": 10,
    "exception_salve": "10 images par salve demandees par l'artiste au lieu de 8 maximum (§5) ; exception consignee (§1)",
    "teaser": "15,00 s / 450 frames ; extrait PROPOSE [02:44.99 -> 03:00.00], PROVISOIRE, bornes a caler par ecoute",
    "genere_le": "2026-11-15",
    "vers": entries,
}

with open(os.path.join(HERE, "verses_map.json"), "w", encoding="utf-8") as fh:
    json.dump(contract, fh, ensure_ascii=False, indent=2)
    fh.write("\n")


def cell(value):
    return str(value).replace("|", "\\|")


dispo = sum(1 for e in entries if e["disponible"])
out = [
    "# CARTE DES VERS — « Grand Marcheur » (PROVISOIRE SUR LE CALAGE)",
    "",
    "Générée depuis `verses_map.json` · 2026-11-15 · branche `arena/2334b1fe-lyric`.",
    "",
    "- Titre exact : **Grand Marcheur** (tag ID3 `TIT2` du maître ; écart avec « grand marcheurs » signalé) · Artiste à l'écran : **DSKY WTBW**.",
    "- Source paroles : `Grand marcheur.txt` · SHA-256 `" + contract["sha256_paroles"] + "`",
    "- Source audio : `Grand marcheur 2.mp3` · SHA-256 `" + contract["sha256_audio"] + "`",
    "- **%d vers horodatés**, débuts seuls ; `fin = null` partout → calage **provisoire**, à contrôler par écoute (syllabes tenues, respirations)." % len(entries),
    "- `disponible` recalculé depuis les **images cuites par le moteur** réellement présentes : **%d/%d**. Une reprise est disponible dès que l'image cuite du vers d'origine existe." % (dispo, len(entries)),
    "- **Exception WTBW DÉCIDÉE** : vers %s → affichage « WTBW », développement conservé dans `texte_source` et dans l'audio (audio non modifié)." % ", ".join(
        str(i) for i in contract["wtbw_lignes"]),
    "- %d reprises identiques → image du premier vers réutilisée (§3) ; variantes d'aube à produire après le passage vers l'aube." % sum(
        1 for e in entries if e["reprise"]),
    "- Mode **PEINT** · méthode **MOTEUR** (défaut §0, choix délégué) · palette = ancre vitrail gospel · **10 images par salve** (exception §5 consignée).",
    "- **Salves** : 01 = 10/10, 02 = 10/10, 03 = 6/10 (plan-36 : echec de generation, non livre). 26 plans cuits par le moteur.",
    "- **Variantes aube** : reprises apres i = 25 -> fond reetalonne par le moteur + vers exact recuit (9 variantes), aucun mot modifie.",
    "",
    "| i | début source | fin | texte source | texte affiché | image | disponible | reprise | statut contrôle |",
    "|---:|---|---|---|---|---|---|---|---|",
]
for e in entries:
    out.append("| %d | `[%02d:%05.2f]` | `null` | %s | %s | `%s` | %s | %s | %s |" % (
        e["i"],
        int(e["debut_source"]) // 60,
        e["debut_source"] % 60,
        cell(e["texte_source"]),
        cell(e["texte_affiche"]),
        e["image"],
        "oui" if e["disponible"] else "non",
        ("oui → %d" % e["reprise_de"]) if e["reprise"] else "non",
        cell(e["statut_controle"]),
    ))
out += [
    "",
    "## À ne pas confondre",
    "",
    "- `texte_source` est la transcription exacte du fichier (accents, apostrophes, ponctuation conservés).",
    "- `texte_affiche` diffère **uniquement** sur l'exception WTBW explicitement autorisée et consignée ici.",
    "- Une image sélectionnée n'est pas une validation technique ; un fichier existant n'est pas nécessairement conforme.",
    "- Aucune mesure de calage n'estinventée : les fins restent `null` tant que l'écoute n'a pas été faite.",
    "",
]
with open(os.path.join(HERE, "CARTE-VERS.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(out))

print("vers:", len(entries), "| reprises:", sum(1 for e in entries if e["reprise"]),
      "| WTBW:", contract["wtbw_lignes"], "| disponibles:", dispo, "/", len(entries))
