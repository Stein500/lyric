#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construit timings_source.lrc, verses_map.json et CARTE-VERS.md depuis On est Réel.md.
PROMPT_UNIVERSEL v5.9 §5.6 / §10.3-10.4 :
- Horodatages de l'artiste gardés tels quels.
- Durée du clip = durée décodée de l'audio (244.99 s).
- `disponible` est recalculé avec os.path.exists, jamais saisi à la main.
- CARTE-VERS.md est dérivée automatiquement de verses_map.json.
"""
import json, os, re

RAC = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(RAC))
SRC = os.path.join(REPO, "On est Réel.md")
ANALYSE = os.path.join(RAC, "analyse.json")
LRC_OUT = os.path.join(RAC, "timings_source.lrc")
JSON_OUT = os.path.join(RAC, "verses_map.json")
CARTE_OUT = os.path.join(RAC, "CARTE-VERS.md")

def strip_zw(s):
    return s.replace("\u200f", "").replace("\u200e", "").replace("\u200b", "").strip()

analyse = json.load(open(ANALYSE, encoding="utf-8"))
SONG_END = float(analyse["duree_decodee_s"])  # 244.99 s
CODE = analyse["code_fin"]                    # "0405"

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
    f.write("[ti:On est réel]\n[ar:Dsky]\n[length:04:05]\n\n")
    for r in rows:
        mm = int(r["t"] // 60)
        ss = r["t"] - mm * 60
        f.write(f"[{mm:02d}:{ss:05.2f}] {r['texte']}\n")

# Plan assignment per verse (1-indexed)
PLAN_MAP = {
    1:  ("fonds/scene-02.png", False, "Signature producteur (nuit) — WOLOF TECHSTEIN BEAT WÊ! (contrôlé OK)"),
    2:  ("fonds/scene-03.png", False, "Celui qui veut abandonner interpellé par la lumière"),
    3:  ("fonds/scene-04.png", False, "Refrain 1/4 — poussière, pluie et famille relevée"),
    4:  ("fonds/scene-05.png", False, "Refrain 2/4 — course dans la nuit, refus d'abandonner"),
    5:  ("fonds/scene-06.png", False, "Refrain 3/4 — poings serrés sous le regard de Béhanzin et Bio Guéra"),
    6:  ("fonds/scene-01-ancre.png", False, "Refrain 4/4 (ANCRE) — on se relève + fresque Sankara, Béhanzin, Bio Guéra"),
    7:  ("fonds/scene-02.png", True,  "Reprise signature producteur"),
    8:  ("fonds/scene-07.png", False, "Le père éprouvé relevé par la main de son fils"),
    9:  ("fonds/scene-08.png", False, "La mère en prière la nuit, rameau et fruit d'or"),
    10: ("fonds/scene-09.png", False, "Frères dont les barreaux se fendent, sœurs qui s'en sortent"),
    11: ("fonds/scene-10.png", False, "Stylo qui brûle + fresque des leaders de l'AES"),
    12: ("fonds/scene-11.png", False, "Rêves volés, voix coupée"),
    13: ("fonds/scene-12.png", False, "Refus de rester à sa place / refus d'abandonner"),
    14: ("fonds/scene-13.png", False, "Garder la flamme et le feu"),
    15: ("fonds/scene-14.png", False, "Le feu des ancêtres : Sankara, Béhanzin, Bio Guéra"),
    16: ("fonds/scene-15.png", False, "Enfants des tempêtes, héritiers des guerres : Roi Bio Guéra"),
    17: ("fonds/scene-16.png", False, "Porter la douleur et la terre : famille relevée"),
    18: ("fonds/scene-17.png", False, "Dignité face au jugement sur la peau et le nom"),
    19: ("fonds/scene-18.png", False, "Roi Béhanzin : racines d'or plus profondes que les canons"),
    20: ("fonds/scene-19.png", False, "Marcher sur des braises, danser dans le feu"),
    21: ("fonds/scene-20.png", False, "Traverser l'orage"),
    22: ("fonds/scene-21.png", False, "Regarde-moi maintenant"),
    23: ("fonds/scene-22.png", False, "Un combattant, un survivant (Thomas Sankara & Camara, contrôlé OK)"),
    24: ("fonds/scene-04.png", True,  "Reprise refrain 1/4"),
    25: ("fonds/scene-05.png", True,  "Reprise refrain 2/4"),
    26: ("fonds/scene-06.png", True,  "Reprise refrain 3/4"),
    27: ("fonds/scene-01-ancre.png", True, "Reprise refrain 4/4 (ANCRE)"),
    28: ("fonds/scene-02.png", True,  "Reprise signature producteur"),
    29: ("fonds/scene-23.png", False, "Refus d'être effacés ou de plier"),
    30: ("fonds/scene-24.png", False, "Cœurs volcans, âmes épées"),
    31: ("fonds/scene-25.png", False, "Rupture avec la trahison"),
    32: ("fonds/scene-26.png", False, "Frères levés pour se battre et danser"),
    33: ("fonds/scene-27.png", False, "Nouvelle génération & présidents de l'AES (sans drapeau)"),
    34: ("fonds/scene-28.png", False, "Blues des banlieues, force des villages : familles relevées"),
    35: ("fonds/scene-29.png", False, "Souveraineté : ni aumône ni tutelle"),
    36: ("fonds/scene-30.png", False, "Justice et destin : héritage Sankara & AES"),
    37: ("fonds/scene-31.png", False, "Mots missiles, rimes boucliers"),
    38: ("fonds/scene-32.png", False, "Né pour briller — à régénérer en salve 5 (texte de l'ancre repris)"),
    39: ("fonds/scene-33.png", False, "Tenir et survivre quand on veut abandonner"),
    40: ("fonds/scene-34.png", False, "Fils du soleil, première lueur de l'aube"),
    41: ("fonds/scene-19.png", True,  "Reprise pré-refrain 1/4"),
    42: ("fonds/scene-20.png", True,  "Reprise pré-refrain 2/4"),
    43: ("fonds/scene-21.png", True,  "Reprise pré-refrain 3/4"),
    44: ("fonds/scene-22.png", True,  "Reprise pré-refrain 4/4"),
    45: ("fonds/scene-35.png", False, "Pont — la nuit est longue (tentation d'abandonner)"),
    46: ("fonds/scene-36.png", False, "La foi, le son, les miens : famille unie"),
    47: ("fonds/scene-37.png", False, "On tombe, on se relève, on recommence (abandonner n'est pas une option)"),
    48: ("fonds/scene-38.png", False, "Rois de l'épreuve : Béhanzin, Bio Guéra, Sankara & famille"),
    49: ("fonds/scene-39.png", False, "Chaînes brisées dans la brume d'aube"),
    50: ("fonds/scene-40.png", False, "Debout à l'aube, né pour chanter"),
    51: ("fonds/v-193-01-aube.png", True, "Refrain final 1/4 — variante AUBE dédiée (§9)"),
    52: ("fonds/v-198-28-aube.png", True, "Refrain final 2/4 — variante AUBE dédiée (§9)"),
    53: ("fonds/v-205-01-aube.png", True, "Refrain final 3/4 — variante AUBE dédiée (§9)"),
    54: ("fonds/v-210-37-aube.png", True, "Refrain final 4/4 — variante AUBE dédiée (§9)"),
    55: ("fonds/v-216-73-aube.png", True, "Signature finale — variante AUBE dédiée (§9)"),
    56: ("fonds/v-216-73-aube.png", True, "Écho signature finale — variante AUBE dédiée (§9)"),
    57: ("fonds/scene-41-final.png", False, "Plan final plein soleil levant : famille relevée & héros"),
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
    "chanson": "On est réel",
    "titre": "On est réel",
    "artiste": "Dsky",
    "langues": "français (signature en fon/wolof : « Wolof TechStein beat wê ! »)",
    "mode": "PEINT",
    "recette": "ENCRE & FEUILLE D'OR",
    "signature": "Wolof TechStein beat wê !",
    "fps": 30,
    "duree_decodee_s": SONG_END,
    "nb_vers": n,
    "plans_distinctes": len(distinct_imgs),
    "plans_disponibles": len(dispo_imgs),
    "plans_manquantes": manq_imgs,
    "qc_a_regenerer": ["fonds/scene-32.png (JE VIENS DE LA STREET / J'SUIS NÉ POUR BRILLER, priorité n°1 salve 5)"],
    "fenetres_clochettes": fenetres,
    "carte_accueil": [0.0, rows[0]["t"]],
    "carte_finale": [SONG_END, round(SONG_END + 5.0, 2)],
    "code": CODE,
    "affichage_formule": "affichage = min(fin_vers, debut_vers + max(2.2 s, 0.30 s * nombre_de_mots)) — PROVISOIRE (§5.6)",
    "continuite_aube": "reprises finales 193.01 / 198.28 / 205.01 / 210.37 / 216.73 / 222.76 = variantes aube dédiées (plus de retour en pleine nuit après l'aube, §9)",
    "regle_clochettes": "fin d'affichage du vers + 0,15 s -> début du vers suivant ; seuil 4,00 s (MODE PEINT) ; jamais sur une carte d'accueil ni pendant un vers en cours de lecture",
    "verses": verses,
}

with open(JSON_OUT, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)

# Generate CARTE-VERS.md from JSON (§10.4)
L = [
    "# Carte des vers — « On est réel » (Dsky)",
    "",
    f"Générée automatiquement depuis `verses_map.json` (§10.4) — **{n} vers** de `On est Réel.md`, horodatages de l'artiste non retouchés (durée décodée mesurée : **{SONG_END:.2f} s**, code de fin : **`{CODE}`**).",
    "",
    f"- **Mode verrouillé** : **PEINT** (le modèle peint la parole et 1 à 3 icônes/stickers dorés dans l'image ; aucune sur-typo au montage hors cartes d'accueil/finale).",
    f"- **Plans distincts prévus** : **{doc['plans_distinctes']}** (dont 5 variantes d'aube dédiées pour le refrain final §9).",
    f"- **Plans présents sur disque (`os.path.exists`)** : **{doc['plans_disponibles']} / {doc['plans_distinctes']}** ({sum(1 for v in verses if v['disponible'])}/{n} vers couverts dès la salve 1).",
    f"- **Contrôle QC salves 1 à 4** : **37 / 38 plans présents validés au zoom 1:1 sans faute** (`scene-22.png` corrigé et validé) ; `fonds/scene-32.png` est programmé en priorité n°1 de la salve 5 finale avec prompt court (§4).",
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

print(f"OK: {n} vers, {doc['plans_distinctes']} plans distincts, {doc['plans_disponibles']} disponibles, {len(fenetres)} fenêtres clochettes")
