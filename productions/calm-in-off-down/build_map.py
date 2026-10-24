#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construit timings_source.lrc, verses_map.json, CARTE-VERS.md et livrables/paroles_clean.txt
depuis 'Calm in off down.txt'.
PROMPT_UNIVERSEL v6.0 §5.6 / §10.3-10.4 + directive bilingue de l'artiste :
- Horodatages de l'artiste gardés tels quels.
- Durée du clip = durée décodée de l'audio (183.61 s) + 5.00 s de carte finale (188.61 s).
- Paroles originales (anglais / espagnol / signature WTBW) peintes dans l'image en style graffiti ordonné.
- Traduction en français (`traduction_fr`) défilant mot à mot dans la bande basse dédiée (y 1350 -> 1510)
  pour tous les passages non français.
- `disponible` est recalculé avec os.path.exists, jamais saisi à la main.
- CARTE-VERS.md est dérivée automatiquement de verses_map.json.
"""
import json, os, re

RAC = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(RAC))
SRC = os.path.join(REPO, "Calm in off down.txt")
ANALYSE = os.path.join(RAC, "analyse.json")
LRC_OUT = os.path.join(RAC, "timings_source.lrc")
JSON_OUT = os.path.join(RAC, "verses_map.json")
CARTE_OUT = os.path.join(RAC, "CARTE-VERS.md")
CLEAN_OUT = os.path.join(RAC, "livrables", "paroles_clean.txt")

def strip_zw(s):
    return s.replace("\u200f", "").replace("\u200e", "").replace("\u200b", "").strip()

analyse = json.load(open(ANALYSE, encoding="utf-8"))
SONG_END = float(analyse["duree_decodee_s"])  # 183.61 s

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
    f.write("[ti:Calm in off down]\n[ar:Daïsky]\n[length:03:03]\n\n")
    for r in rows:
        mm = int(r["t"] // 60)
        ss = r["t"] - mm * 60
        f.write(f"[{mm:02d}:{ss:05.2f}] {r['texte']}\n")

# Write paroles_clean.txt (without timestamps, for ID3 USLT §11)
os.makedirs(os.path.dirname(CLEAN_OUT), exist_ok=True)
with open(CLEAN_OUT, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(r["texte"] + "\n")

# (plan_rel_path, reprise_bool, langue, traduction_fr_defilante, note)
PLAN_MAP = {
    1:  ("fonds/scene-02.png", False, "WTBW", "",
         "Intro signature producteur (battle cypher nocturne, platines, cœur love & vinyle) — contrôlé OK"),
    2:  ("fonds/scene-03.png", False, "EN", "J'ai coupé le bruit, éteint les lumières à la porte,",
         "Couplet 1 — hand-slice hip-hop coupant le bruit, projecteurs éteints, cœur love & lampe — contrôlé OK"),
    3:  ("fonds/scene-04.png", False, "EN", "Ni public, ni applaudissements — juste le sol de béton froid.",
         "Couplet 1 — low-stance footwork sur béton froid sans public, cœur love & sneaker — contrôlé OK"),
    4:  ("fonds/scene-05.png", False, "EN", "Ils parlaient si fort, mec j'ai coupé le son,",
         "Couplet 1 — isolation d'épaule balayant les ondes sonores, cœur love & mute — contrôlé OK"),
    5:  ("fonds/scene-06.png", False, "EN", "Calme dans l'ombre — c'est là que je me suis trouvé.",
         "Couplet 1 — freeze sous faisceau vertical, main sur le cœur, cœur love & étoile boussole — contrôlé OK"),
    6:  ("fonds/scene-07.png", False, "EN", "Chaque guerre que j'ai menée, je l'ai livrée au fond du silence,",
         "Couplet 1 — garde krump puissante dans le silence, cœur love & bouclier — contrôlé OK"),
    7:  ("fonds/scene-08.png", False, "EN", "Tu veux la vérité sur moi — viens t'asseoir dans la tempête.",
         "Couplet 1 — spin freestyle au cœur du tourbillon d'étincelles, cœur love & éclair — contrôlé OK"),
    8:  ("fonds/scene-09.png", False, "EN", "Je n'ai pas besoin de la foule — j'ai besoin du silence pour parler,",
         "Couplet 1 — pop-and-lock doigt près de la joue devant gradins vides, cœur love & micro — contrôlé OK"),
    9:  ("fonds/scene-10.png", False, "EN", "Sept jours d'immobilité et j'ai atteint mon sommet.",
         "Couplet 1 — pose d'élévation au sommet devant verrière nocturne, cœur love & sommet — contrôlé OK"),
    10: ("fonds/scene-01-ancre.png", False, "EN+ES", "Calme dans l'ombre — j'éteins le bruit,",
         "Refrain 1/4 (ANCRE) — isolation Wandance, regard calme magnétique, cœur love & haut-parleur coupé — contrôlé OK"),
    11: ("fonds/scene-11.png", False, "EN+ES", "Tout est immobile mais mon âme reste embrasée.",
         "Refrain 2/4 — freeze immobile entouré de braises dorées intérieures, cœur love & flamme"),
    12: ("fonds/scene-12.png", False, "EN", "Calme dans l'ombre — sans lumières, sans scène,",
         "Refrain 3/4 — pas de battle dans l'entrepôt brut sans estrade, cœur love & projecteur éteint"),
    13: ("fonds/scene-13.png", False, "ES+EN", "Seul avec l'obscurité — nous avons tous deux le même âge.",
         "Refrain 4/4 — duo d'ombres chorégraphique avec sa propre silhouette, cœur love & croissant nocturne"),
    14: ("fonds/scene-14.png", False, "ES", "J'ai éteint les voix qui me disaient non,",
         "Couplet 2 (ES) — geste de balayage puissant dispersant les ombres, cœur love & croix sonore"),
    15: ("fonds/scene-15.png", False, "ES", "J'ai fait taire les peurs — je les ai brûlées une à une.",
         "Couplet 2 (ES) — pas de danse ardent faisant voler des étincelles d'or, cœur love & torche"),
    16: ("fonds/scene-16.png", False, "ES", "Au fond du silence j'ai trouvé ma vraie version,",
         "Couplet 2 (ES) — reflet pur au sol révélant son vrai visage dégagé, cœur love & miroir"),
    17: ("fonds/scene-17.png", False, "ES", "Pas celle que le monde voulait — celle qui fut toujours loyale.",
         "Couplet 2 (ES) — posture droite et loyale, main sur le torse, cœur love & couronne fidèle"),
    18: ("fonds/scene-18.png", False, "EN+ES", "Calme dans l'ombre, mais le feu brûle encore,",
         "Couplet 2 (ES) — groove calme traversé d'une aura de feu doré, cœur love & brasier"),
    19: ("fonds/scene-19.png", False, "ES", "Le calme est mon armure quand le monde s'écroule.",
         "Couplet 2 (ES) — posture de titan imperturbable sous les éclats, cœur love & armure"),
    20: ("fonds/scene-20.png", False, "ES", "Je ne parle pas pour qu'on m'écoute — je parle pour que ça résonne,",
         "Couplet 2 (ES) — stomp de battle faisant vibrer le sol en ondes d'or, cœur love & onde de choc"),
    21: ("fonds/scene-21.png", False, "ES", "Chaque mot que je lâche est un impact qui frappe juste.",
         "Couplet 2 (ES) — punch chorégraphique précis en rythme, cœur love & impact électrique"),
    22: ("fonds/scene-22.png", False, "EN", "Parfois la chose la plus forte que tu entendras",
         "Pont 1/4 — silence suspendu sous les premières lueurs d'aube, cœur love & onde pure"),
    23: ("fonds/scene-22.png", True,  "EN", "c'est un homme qui a choisi de disparaître.",
         "Pont 2/4 — suite de la phrase sur le même plan d'aube naissante, traduction FR défilante 2/2"),
    24: ("fonds/scene-24.png", False, "EN", "Je me suis retiré des radars pour trouver ma force intérieure,",
         "Pont 3/4 — toit urbain hors-réseau face à l'horizon naissant, cœur love & boussole interne"),
    25: ("fonds/scene-25.png", False, "EN", "Je suis revenu transformé — que le vrai moi commence.",
         "Pont 4/4 — ouverture des bras face aux premières lueurs dorées, cœur love & phénix"),
    26: ("fonds/scene-02.png", True,  "WTBW", "",
         "Reprise signature producteur WTBW"),
    27: ("fonds/scene-27.png", False, "EN", "Regarde comment je bouge — calme mais calculé,",
         "Couplet 3 — footwork millimétré dans la lumière matinale, cœur love & compas"),
    28: ("fonds/scene-28.png", False, "EN", "Chaque pas délibéré, rien n'a été gâché.",
         "Couplet 3 — glissé précis sur le sol baigné d'aube, cœur love & empreinte dorée"),
    29: ("fonds/scene-29.png", False, "EN", "Ils voulaient le drame — je leur ai donné la distance,",
         "Couplet 3 — pas de retrait élégant et souverain, cœur love & horizon"),
    30: ("fonds/scene-30.png", False, "EN", "J'ai refusé chaque offre qui manquait de substance.",
         "Couplet 3 — main levée en refus calme et digne, cœur love & diamant pur"),
    31: ("fonds/scene-31.png", False, "EN", "Le calme dans l'ombre est une arme, pas une faiblesse,",
         "Couplet 3 — posture d'arts martiaux / street-dance maîtrisée, cœur love & lame de lumière"),
    32: ("fonds/scene-32.png", False, "EN", "Ceux qui parlent le moins portent les choses les plus profondes.",
         "Couplet 3 — regard profond et serein sous l'aube claire, cœur love & ancre marine"),
    33: ("fonds/scene-33.png", False, "EN", "Je suis l'œil du cyclone — je suis ce que tu ne peux atteindre,",
         "Couplet 3 — spin central immobile au milieu du vent lumineux, cœur love & spirale"),
    34: ("fonds/scene-34.png", False, "EN", "Quand le monde hurle — le silence devient ma parole.",
         "Couplet 3 — pose magistrale face à la ville qui s'éveille, cœur love & couronne d'ondes"),
    35: ("fonds/v-140-13-aube.png", True, "EN+ES", "Calme dans l'ombre — j'éteins le bruit,",
         "Refrain final 1/4 — variante AUBE dédiée (§9, rayons dorés du matin sur le cypher)"),
    36: ("fonds/scene-11.png", True, "EN+ES", "Tout est immobile mais mon âme reste embrasée.",
         "Refrain final 2/4 — reprise du freeze embrasé d'or (déjà lumineux) — contrôlé OK"),
    37: ("fonds/v-146-60-aube.png", True, "EN", "Calme dans l'ombre — sans lumières, sans scène,",
         "Refrain final 3/4 — variante AUBE dédiée (§9, toit ouvert sous le ciel d'or)"),
    38: ("fonds/v-149-86-aube.png", True, "ES+EN", "Seul avec l'obscurité — nous avons tous deux le même âge.",
         "Refrain final 4/4 — variante AUBE dédiée (§9, l'ombre vaincue par le matin doré)"),
    39: ("fonds/scene-35.png", False, "EN", "Calme dans l'ombre — mais le feu ne s'est jamais éteint,",
         "Outro 1/4 — danse solaire ardente face au soleil levant, cœur love & flamme éternelle"),
    40: ("fonds/scene-36.png", False, "EN", "TechStein dans le noir — regarde-nous surgir de l'intérieur.",
         "Outro 2/4 — élévation victorieuse en pleine clarté d'aube, cœur love & flèche montante"),
    41: ("fonds/scene-37-final.png", False, "EN", "Calme dans l'ombre",
         "Outro 3/4 (Plan final) — freeze final iconique devant le grand soleil levant doré, cœur love & couronne"),
    42: ("fonds/v-164-33-aube.png", True, "WTBW", "",
         "Outro 4/4 (Signature finale) — variante AUBE dédiée (§9, salut WTBW en plein soleil levant)"),
}

n = len(rows)
verses = []
for k, r in enumerate(rows):
    i = k + 1
    t = r["t"]
    fin = rows[k + 1]["t"] if k + 1 < n else SONG_END
    mots = len(r["texte"].split())
    disp = min(fin - t, max(2.2, 0.30 * mots))  # §5.6 provisoire
    rel_img, rep, lang, trad_fr, note = PLAN_MAP[i]
    abs_img = os.path.join(RAC, rel_img)
    dispo = bool(os.path.exists(abs_img))       # §10.3 recalculé avec os.path.exists
    verses.append({
        "i": i,
        "t": round(t, 2),
        "fin": round(fin, 2),
        "affichage_s": round(disp, 2),
        "texte": r["texte"],
        "langue": lang,
        "traduction_fr": trad_fr,
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
    "chanson": "Calm in off down",
    "titre": "Calm in off down",
    "artiste": "Daïsky",
    "langues": "anglais + espagnol + signature WTBW (paroles originales peintes en graffiti dans l'image + traduction française défilant mot à mot dans y 1350->1510)",
    "mode": "PEINT_VO_GRAFFITI + DEFILEMENT_TRADUCTION_FR",
    "recette": "WANDANCE BATTLE & GRAFFITI LOVES — ORDONNÉ & VISAGE DÉGAGÉ",
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
    "affichage_formule": "affichage = min(fin_vers - debut_vers, max(2.2 s, 0.30 s * nombre_de_mots)) — PROVISOIRE (§5.6)",
    "continuite_aube": "reprises finales 140.13 / 143.66 / 146.60 / 149.86 / 164.33 = 5 variantes aube dédiées (aucun retour en pleine nuit après l'aube, §9)",
    "regle_clochettes": "fin d'affichage du vers + 0,15 s -> début du vers suivant ; seuil 4,00 s (MODE PEINT) ; jamais sur une carte d'accueil ni pendant un vers en cours de lecture",
    "verses": verses,
}

with open(JSON_OUT, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)

# Generate CARTE-VERS.md from JSON (§10.4)
L = [
    "# Carte des vers — « Calm in off down » (Daïsky · WTBW)",
    "",
    f"Générée automatiquement depuis `verses_map.json` (§10.4) — **{n} vers** de `Calm in off down.txt`, horodatages de l'artiste non retouchés (durée décodée mesurée : **{SONG_END:.2f} s**, accueil & finale **WTBW sans code**).",
    "",
    f"- **Mode verrouillé** : **PEINT (paroles originales EN/ES en style graffiti ordonné dans l'image)** + **DÉFILEMENT (traduction française mot à mot dans `y 1350 → 1510`)**.",
    f"- **Recette** : **WANDANCE BATTLE & GRAFFITI LOVES — ORDONNÉ & VISAGE DÉGAGÉ**.",
    f"- **Plans distincts prévus** : **{doc['plans_distinctes']}** (dont 5 variantes d'aube dédiées pour le refrain final et la signature finale §9).",
    f"- **Plans présents sur disque (`os.path.exists`)** : **{doc['plans_disponibles']} / {doc['plans_distinctes']}** ({sum(1 for v in verses if v['disponible'])}/{n} vers couverts après Salve 1).",
    f"- **Contrôle QC Salve 1** : **10 / 10 plans validés au zoom 1:1 sans aucune faute d'orthographe**.",
    "",
    "| # | t (s) | fin (s) | aff. (s) | langue | vers peint (VO graffiti) | traduction FR défilante | plan | dispo | reprise |",
    "|---|---:|---:|---:|:---:|---|---|---|:---:|:---:|",
]
for v in verses:
    dispo_str = "oui" if v["disponible"] else "non"
    rep_str = "↻" if v["reprise"] else "—"
    trad_str = v["traduction_fr"] if v["traduction_fr"] else "*(signature WTBW)*"
    L.append(f"| {v['i']} | {v['t']:.2f} | {v['fin']:.2f} | {v['affichage_s']:.2f} | `{v['langue']}` | {v['texte']} | {trad_str} | `{v['image']}` | {dispo_str} | {rep_str} |")

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
