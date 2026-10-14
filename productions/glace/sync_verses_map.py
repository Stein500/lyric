#!/usr/bin/env python3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "analyse.json"), "r", encoding="utf-8") as f:
    analyse = json.load(f)

# Explicit mapping of all 45 verses to their painted visual plan (1 plan per distinct verse + dedicated dawn variants for v38..v45 per v5.9 §9)
PLAN_ASSIGNMENTS = {
    1:  ("fonds/scene-02.png", False, ""),
    2:  ("fonds/scene-02.png", True,  "↻ reprise"),
    3:  ("fonds/scene-03.png", False, ""),
    4:  ("fonds/scene-04.png", False, ""),
    5:  ("fonds/scene-05.png", False, ""),
    6:  ("fonds/scene-06.png", False, ""),
    7:  ("fonds/scene-07.png", False, ""),
    8:  ("fonds/scene-08.png", False, ""),
    9:  ("fonds/scene-09.png", False, ""),
    10: ("fonds/scene-10.png", False, ""),
    11: ("fonds/scene-11.png", False, ""),
    12: ("fonds/scene-02.png", True,  "↻ reprise"),
    13: ("fonds/scene-01-ancre.png", False, "★ ancre"),
    14: ("fonds/scene-12.png", False, ""),
    15: ("fonds/scene-01-ancre.png", True,  "↻ reprise"),
    16: ("fonds/scene-13.png", False, ""),
    17: ("fonds/scene-14.png", False, ""),
    18: ("fonds/scene-15.png", False, ""),
    19: ("fonds/scene-16.png", False, ""),
    20: ("fonds/scene-17.png", False, ""),
    21: ("fonds/scene-18.png", False, ""),
    22: ("fonds/scene-19.png", False, ""),
    23: ("fonds/v-66-12.png",  False, "◆ vers dédié"),
    24: ("fonds/v-69-28.png",  False, "◆ vers dédié"),
    25: ("fonds/v-74-29.png",  False, "◆ vers dédié"),
    26: ("fonds/v-76-81.png",  False, "◆ vers dédié"),
    27: ("fonds/v-74-29.png",  True,  "↻ reprise"),
    28: ("fonds/v-84-21.png",  False, "◆ vers dédié"),
    29: ("fonds/scene-02.png", True,  "↻ reprise"),
    30: ("fonds/scene-01-ancre.png", True,  "↻ reprise"),
    31: ("fonds/scene-12.png", True,  "↻ reprise"),
    32: ("fonds/scene-01-ancre.png", True,  "↻ reprise"),
    33: ("fonds/v-105-99.png", False, "◆ vers dédié"),
    34: ("fonds/v-111-10.png", False, "◆ vers dédié"),
    35: ("fonds/v-113-80.png", False, "◆ vers dédié"),
    36: ("fonds/v-118-54.png", False, "◆ vers dédié"),
    37: ("fonds/v-121-25.png", False, "◆ vers dédié"),
    38: ("fonds/v-124-63.png", True,  "☀ variante aube dédiée"),
    39: ("fonds/v-127-95.png", True,  "☀ variante aube dédiée"),
    40: ("fonds/v-131-54.png", False, "☀ aube"),
    41: ("fonds/v-127-95.png", True,  "↻ reprise aube"),
    42: ("fonds/v-143-01.png", True,  "☀ variante aube dédiée"),
    43: ("fonds/v-150-14.png", False, "☀ aube"),
    44: ("fonds/v-157-79.png", False, "☀ aube"),
    45: ("fonds/v-165-25.png", False, "☀ aube finale"),
}

verses_out = []
distinct_plans = []
for v in analyse["verses"]:
    i = v["i"]
    img_rel, reprise, note = PLAN_ASSIGNMENTS[i]
    img_abs = os.path.join(BASE_DIR, img_rel)
    disp_ok = os.path.exists(img_abs)
    if img_rel not in distinct_plans:
        distinct_plans.append(img_rel)
    verses_out.append({
        "i": i,
        "t": v["t"],
        "fin": v["fin"],
        "affichage_s": v["affichage_s"],
        "texte": v["texte"],
        "image": img_rel,
        "disponible": disp_ok,
        "reprise": reprise,
        "note": note
    })

plans_disponibles = [p for p in distinct_plans if os.path.exists(os.path.join(BASE_DIR, p))]
plans_manquantes = [p for p in distinct_plans if not os.path.exists(os.path.join(BASE_DIR, p))]

fenetres_clochettes = [
    [w[0], w[1]] for w in analyse["fenetres_clochettes_mode_peint_ge_4s"]
]

vmap = {
    "chanson": "Glace",
    "artiste": "Dsky",
    "mode": "PEINT",
    "fps": 30,
    "duree_decodee_s": analyse["duree_decodee_s"],
    "nb_vers": len(verses_out),
    "plans_distinctes": len(distinct_plans),
    "plans_disponibles": len(plans_disponibles),
    "plans_manquantes": plans_manquantes,
    "fenetres_clochettes": fenetres_clochettes,
    "carte_accueil": [0.0, 6.03],
    "carte_finale": [180.0, 185.0],
    "code": "0300",
    "verses": verses_out,
    "continuite_aube": "reprises finales 124,63 / 127,95 / 143,01 = variantes aube dédiées (pas de retour en pleine nuit après le pont)",
    "regle_clochettes": "fin d'affichage du vers + 0,15 s -> début du vers suivant ; seuil 4,00 s (MODE PEINT) ; jamais sur une carte d'accueil ni pendant un vers en cours de lecture"
}

with open(os.path.join(BASE_DIR, "verses_map.json"), "w", encoding="utf-8") as f:
    json.dump(vmap, f, ensure_ascii=False, indent=2)

# Generate CARTE-VERS.md from verses_map.json
md = []
md.append("# Carte des vers — « Glace » (Dsky)\n")
md.append(f"Générée automatiquement depuis `verses_map.json` — **{vmap['nb_vers']} vers** de `Glace.txt`, horodatages de l'artiste non retouchés (durée décodée **{vmap['duree_decodee_s']:.2f} s**).\n")
md.append(f"**État actuel : {vmap['plans_disponibles']} / {vmap['plans_distinctes']} plans distincts disponibles dans `fonds/` ({len(plans_manquantes)} restants à générer dans les prochaines salves).** Mode verrouillé : **PEINT** (texte écrit dans l'image par le générateur ; aucune sur-typo au montage hors cartes d'accueil/finale et CTA clochettes).\n")
md.append("| # | t (s) | fin (s) | aff. (s) | vers | plan | dispo | note |")
md.append("|---|---|---|---|---|---|---|---|")
for v in verses_out:
    plan_short = os.path.splitext(os.path.basename(v["image"]))[0]
    dispo_str = "✓" if v["disponible"] else "⏳"
    md.append(f"| {v['i']} | {v['t']:.2f} | {v['fin']:.2f} | {v['affichage_s']:.2f} | {v['texte']} | `{plan_short}` | {dispo_str} | {v['note']} |")

with open(os.path.join(BASE_DIR, "CARTE-VERS.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md) + "\n")

print(f"verses_map.json & CARTE-VERS.md synced: {len(plans_disponibles)}/{len(distinct_plans)} available.")
