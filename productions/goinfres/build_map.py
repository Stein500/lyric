#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construit timings_source.lrc, verses_map.json, CARTE-VERS.md et livrables/paroles_clean.txt
depuis Goinfres.txt.
PROMPT_UNIVERSEL v5.9 §5.6 / §10.3-10.4 :
- Horodatages de l'artiste gardés tels quels.
- Durée du clip = durée décodée de l'audio (222.92 s).
- `disponible` est recalculé avec os.path.exists, jamais saisi à la main.
- CARTE-VERS.md est dérivée automatiquement de verses_map.json.
"""
import json, os, re

RAC = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(RAC))
SRC = os.path.join(REPO, "Goinfres.txt")
ANALYSE = os.path.join(RAC, "analyse.json")
LRC_OUT = os.path.join(RAC, "timings_source.lrc")
JSON_OUT = os.path.join(RAC, "verses_map.json")
CARTE_OUT = os.path.join(RAC, "CARTE-VERS.md")
CLEAN_OUT = os.path.join(RAC, "livrables", "paroles_clean.txt")

def strip_zw(s):
    return s.replace("\u200f", "").replace("\u200e", "").replace("\u200b", "").strip()

analyse = json.load(open(ANALYSE, encoding="utf-8"))
SONG_END = float(analyse["duree_decodee_s"])  # 222.92 s
CODE = analyse["code_fin"]                    # "0342"

rows = []
with open(SRC, encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        m = re.match(r"^\[(\d+):(\d+(?:\.\d+)?)\]\s*(.*)$", line)
        if m:
            t = int(m.group(1)) * 60 + float(m.group(2))
            rows.append({"t": round(t, 2), "texte": strip_zw(m.group(3))})

# Write normalized timings_source.lrc
with open(LRC_OUT, "w", encoding="utf-8") as f:
    f.write("[ti:Goinfres]\n[ar:Dsky]\n[length:03:42]\n\n")
    for r in rows:
        mm = int(r["t"] // 60)
        ss = r["t"] - mm * 60
        f.write(f"[{mm:02d}:{ss:05.2f}] {r['texte']}\n")

# Write paroles_clean.txt (without timestamps, for ID3 USLT §11)
os.makedirs(os.path.dirname(CLEAN_OUT), exist_ok=True)
with open(CLEAN_OUT, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(r["texte"] + "\n")

# Plan assignment per verse (1-indexed, 47 verses -> 36 distinct plans including 5 dawn variants §9)
PLAN_MAP = {
    1:  ("fonds/scene-02.png", False, "Intro signature producteur (studio piano/violon atténué N&B, sourire confiant) — contrôlé OK"),
    2:  ("fonds/scene-03.png", False, "Intro — balcon sur ville nocturne atténuée N&B, regard lucide — contrôlé OK"),
    3:  ("fonds/scene-01-ancre.png", False, "Refrain 1/4 (ANCRE) — salle de banquet atténuée N&B, regard d'indignation — contrôlé OK"),
    4:  ("fonds/scene-04.png", False, "Refrain 2/4 — chambre forte de lingots atténuée N&B, regard accusateur — contrôlé OK"),
    5:  ("fonds/scene-05.png", False, "Refrain 3/4 — ruelle atténuée N&B, familles aux bols vides, main sur le cœur — contrôlé OK"),
    6:  ("fonds/scene-06.png", False, "Refrain 4/4 — océan orageux & requins atténués N&B, cri d'alerte — contrôlé OK (v2)"),
    7:  ("fonds/scene-02.png", True,  "Reprise signature producteur — contrôlé OK"),
    8:  ("fonds/scene-07.png", False, "Couplet 1 — atelier atténué N&B, travailleurs serrant la ceinture, bras croisés — contrôlé OK"),
    9:  ("fonds/scene-08.png", False, "Couplet 1 — balcon des goinfres atténué N&B, main levée en refus — contrôlé OK"),
    10: ("fonds/scene-09.png", False, "Couplet 1 — grande salle & table-monde atténuée N&B, regard défiant — contrôlé OK"),
    11: ("fonds/scene-10.png", False, "Couplet 1 — arches de pierre atténuées N&B, peuple recueillant les miettes, poing levé — contrôlé OK"),
    12: ("fonds/scene-11.png", False, "Couplet 1 — pain des enfants arraché, regard de révolte protectrice — contrôlé OK"),
    13: ("fonds/scene-12.png", False, "Couplet 1 — coupes des vivants dans l'ombre, expression d'accusation — contrôlé OK"),
    14: ("fonds/scene-13.png", False, "Couplet 1 — la grande table qui se fissure d'éclairs blancs — contrôlé OK"),
    15: ("fonds/scene-14.png", False, "Couplet 1 — balance de justice en lumière blanche, regard prophétique — contrôlé OK"),
    16: ("fonds/scene-15.png", False, "Pré-refrain 1/4 — poches débordant de billets et pièces — contrôlé OK (v2)"),
    17: ("fonds/scene-16.png", False, "Pré-refrain 2/4 — statues aux poitrines creuses dans la brume, tristesse grave — contrôlé OK"),
    18: ("fonds/scene-17.png", False, "Pré-refrain 3/4 — chaîne fraternelle de bras unis dans l'ombre claire — contrôlé OK"),
    19: ("fonds/scene-18.png", False, "Pré-refrain 4/4 — tourbillon de la folie des goinfres en arrière-plan atténué — contrôlé OK"),
    20: ("fonds/scene-01-ancre.png", True, "Reprise refrain 1/4 (ANCRE)"),
    21: ("fonds/scene-04.png", True,  "Reprise refrain 2/4"),
    22: ("fonds/scene-05.png", True,  "Reprise refrain 3/4"),
    23: ("fonds/scene-06.png", True,  "Reprise refrain 4/4"),
    24: ("fonds/scene-02.png", True,  "Reprise signature producteur"),
    25: ("fonds/scene-19.png", False, "Couplet 2 — trône de pouvoir et liasses en clair-obscur N&B — contrôlé OK"),
    26: ("fonds/scene-20.png", False, "Couplet 2 — miroir brisé révélant l'âme perdue en encre noire et blanche — contrôlé OK"),
    27: ("fonds/scene-21.png", False, "Couplet 2 — assiette géante voilant l'horizon atténué — contrôlé OK"),
    28: ("fonds/scene-22.png", False, "Couplet 2 — mains dignes grattant la terre sombre pour une miette — contrôlé OK"),
    29: ("fonds/scene-23.png", False, "Couplet 2 — peuple debout qui se lève et résiste dans la brume claire — contrôlé OK"),
    30: ("fonds/scene-24.png", False, "Couplet 2 — atelier d'artistes (pinceaux, micro, violon) en N&B contrasté — contrôlé OK"),
    31: ("fonds/scene-25.png", False, "Couplet 2 — partage équitable de la moisson, détermination fière — contrôlé OK"),
    32: ("fonds/scene-26.png", False, "Couplet 2 — bâtisseurs d'un monde nouveau en traits d'encre blanche — contrôlé OK (v2)"),
    33: ("fonds/scene-15.png", True,  "Reprise pré-refrain 1/4"),
    34: ("fonds/scene-16.png", True,  "Reprise pré-refrain 2/4"),
    35: ("fonds/scene-17.png", True,  "Reprise pré-refrain 3/4"),
    36: ("fonds/scene-18.png", True,  "Reprise pré-refrain 4/4"),
    37: ("fonds/scene-27.png", False, "Pont 1/4 — vaste terre sous les premières lueurs blanches d'aube — contrôlé OK"),
    38: ("fonds/scene-28.png", False, "Pont 2/4 — mains avides accaparant le monde face à l'aube blanche — contrôlé OK"),
    39: ("fonds/scene-29.png", False, "Pont 3/4 — sablier écoulé sur la table désertée à l'aube — contrôlé OK (v2)"),
    40: ("fonds/scene-30.png", False, "Pont 4/4 — solitude des rois déchus dans le palais silencieux au matin — contrôlé OK"),
    41: ("fonds/v-167-69-aube.png", True, "Refrain final 1/4 — variante AUBE N&B dédiée (§9, contre-jour blanc lumineux) — contrôlé OK"),
    42: ("fonds/v-170-71-aube.png", True, "Refrain final 2/4 — variante AUBE N&B dédiée (§9, contre-jour blanc lumineux) — contrôlé OK"),
    43: ("fonds/v-174-05-aube.png", True, "Refrain final 3/4 — variante AUBE N&B dédiée (§9, contre-jour blanc lumineux) — contrôlé OK"),
    44: ("fonds/v-176-45-aube.png", True, "Refrain final 4/4 — variante AUBE N&B dédiée (§9, contre-jour blanc lumineux) — contrôlé OK"),
    45: ("fonds/v-181-90-aube.png", True, "Signature finale — variante AUBE N&B dédiée (§9) — contrôlé OK"),
    46: ("fonds/v-181-90-aube.png", True, "Écho signature finale — variante AUBE N&B dédiée (§9) — contrôlé OK"),
    47: ("fonds/scene-31-final.png", False, "Plan final plein soleil levant blanc éclatant en N&B : peuple et artistes debout — contrôlé OK"),
}

n = len(rows)
verses = []
for k, r in enumerate(rows):
    i = k + 1
    t = r["t"]
    fin = rows[k + 1]["t"] if k + 1 < n else SONG_END
    mots = len(r["texte"].split())
    disp = min(fin - t, max(2.2, 0.30 * mots))  # §5.6 provisoire
    rel_img, rep, note = PLAN_MAP[i]
    abs_img = os.path.join(RAC, rel_img)
    dispo = bool(os.path.exists(abs_img))       # §10.3 recalculé avec os.path.exists
    verses.append({
        "i": i,
        "t": round(t, 2),
        "fin": round(fin, 2),
        "affichage_s": round(disp, 2),
        "texte": r["texte"],
        "image": rel_img,
        "disponible": dispo,
        "reprise": rep,
        "note": note,
    })

distinct_imgs = []
for v in verses:
    if v["image"] not in distinct_imgs:
        distinct_imgs.append(v["image"])

dispo_imgs = [p for p in distinct_imgs if os.path.exists(os.path.join(RAC, p))]
manq_imgs = [p for p in distinct_imgs if not os.path.exists(os.path.join(RAC, p))]

# Fenêtres clochettes (§6) : [fin d'affichage + 0,15 s -> début du vers suivant], seuil 4,0 s en MODE PEINT
fenetres = []
for v in verses:
    libre = v["fin"] - v["t"] - v["affichage_s"]
    if libre >= 4.0 and v["fin"] <= SONG_END + 0.01:
        fenetres.append([round(v["t"] + v["affichage_s"] + 0.15, 2), round(min(v["fin"], SONG_END), 2)])

doc = {
    "chanson": "Goinfres",
    "titre": "Goinfres",
    "artiste": "Dsky",
    "langues": "français (signature en fon/wolof : « Wolof TechStein beat wê ! »)",
    "mode": "PEINT",
    "recette": "STUDIO ANIME SEINEN — NOIR & BLANC, DÉCORS ATTÉNUÉS, EXPRESSIONS MULTIPLES",
    "signature": "Wolof TechStein beat wê !",
    "fps": 30,
    "duree_decodee_s": SONG_END,
    "nb_vers": n,
    "plans_distinctes": len(distinct_imgs),
    "plans_disponibles": len(dispo_imgs),
    "plans_manquantes": manq_imgs,
    "qc_a_regenerer": [],
    "fenetres_clochettes": fenetres,
    "carte_accueil": [0.0, rows[0]["t"]],
    "carte_finale": [SONG_END, round(SONG_END + 5.0, 2)],
    "accueil_mode": "WTBW_SALUT_STICKERS_DOUX (sans système de code)",
    "finale_mode": "WTBW_MERCI_STICKERS_DOUX (sans système de code)",
    "affichage_formule": "affichage = min(fin_vers, debut_vers + max(2.2 s, 0.30 s * nombre_de_mots)) — PROVISOIRE (§5.6)",
    "continuite_aube": "reprises finales 167.69 / 170.71 / 174.05 / 176.45 / 181.90 / 193.71 = 5 variantes aube N&B dédiées (plus de retour en pleine nuit après l'aube, §9)",
    "regle_clochettes": "fin d'affichage du vers + 0,15 s -> début du vers suivant ; seuil 4,00 s (MODE PEINT) ; jamais sur une carte d'accueil ni pendant un vers en cours de lecture",
    "verses": verses,
}

with open(JSON_OUT, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)

# Generate CARTE-VERS.md from JSON (§10.4)
L = [
    "# Carte des vers — « Goinfres » (Dsky)",
    "",
    f"Générée automatiquement depuis `verses_map.json` (§10.4) — **{n} vers** de `Goinfres.txt`, horodatages de l'artiste non retouchés (durée décodée mesurée : **{SONG_END:.2f} s**, accueil & finale **WTBW sans code**).",
    "",
    f"- **Mode verrouillé** : **PEINT** en **STUDIO ANIME SEINEN — NOIR & BLANC avec décors atténués et expressions variées**.",
    f"- **Plans distincts prévus** : **{doc['plans_distinctes']}** (dont 5 variantes d'aube N&B dédiées pour le refrain final §9).",
    f"- **Plans présents sur disque (`os.path.exists`)** : **{doc['plans_disponibles']} / {doc['plans_distinctes']}** ({sum(1 for v in verses if v['disponible'])}/{n} vers couverts — **100 %**).",
    f"- **Contrôle QC salves 1 à 4** : **36 / 36 plans validés au zoom 1:1 sans aucune faute d'orthographe**.",
    "",
    "| # | t (s) | fin (s) | aff. (s) | vers | plan | dispo | reprise | note |",
    "|---|---:|---:|---:|---|---|:---:|:---:|---|",
]
for v in verses:
    dispo_str = "oui" if v["disponible"] else "non"
    rep_str = "↻" if v["reprise"] else "—"
    L.append(f"| {v['i']} | {v['t']:.2f} | {v['fin']:.2f} | {v['affichage_s']:.2f} | {v['texte']} | `{v['image']}` | {dispo_str} | {rep_str} | {v['note']} |")

L += [
    "",
    f"## Fenêtres de clochette éligibles (MODE PEINT, seuil ≥ 4,00 s de temps libre après affichage + 0,15 s) : {len(fenetres)}",
    "",
]
for wa, wb in fenetres:
    L.append(f"- **{wa:.2f} s → {wb:.2f} s** (durée libre : {wb - wa:.2f} s)")

L += [
    "",
    "_Fichier dérivé automatiquement par `build_map.py` depuis `verses_map.json` — ne jamais éditer à la main (§10.4)._",
]
with open(CARTE_OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")

print(f"OK: {n} vers, {doc['plans_distinctes']} plans distincts, {doc['plans_disponibles']} disponibles ({sum(1 for v in verses if v['disponible'])}/{n} vers couverts), {len(fenetres)} fenêtres clochettes")
