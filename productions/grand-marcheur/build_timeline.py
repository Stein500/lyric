#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Timeline PROVISOIRE (v7.0 §3) — les fins de vers ne sont pas fournies.

Estimation DECLAREE : la fin d'un vers est prise au debut du vers suivant
(le dernier vers finit a la duree decodee du maitre). Aucune fin n'est inventee
comme mesure : `fin_estimee` reste distincte de `fin` (null) dans verses_map.json.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "verses_map.json"), encoding="utf-8"))
DUREE_DECODEE = 220.07          # mesuree ffmpeg n9.0.2 le 2026-11-15
OUTRO = 5.00
FPS = 30
vers = D["vers"]

rows = []
for k, e in enumerate(vers):
    debut = e["debut_source"]
    fin_estimee = vers[k + 1]["debut_source"] if k + 1 < len(vers) else DUREE_DECODEE
    duree_plan = round(fin_estimee - debut, 2)
    nb_mots = len(e["texte_affiche"].split())
    duree_indicative = round(min(duree_plan, max(2.2, 0.30 * nb_mots)), 2)
    rows.append({"i": e["i"], "debut_source": debut, "fin_estimee": round(fin_estimee, 2),
                 "duree_plan": duree_plan, "nb_mots": nb_mots,
                 "duree_affichage_indicative": duree_indicative,
                 "image_cuite": e["image_cuite"], "disponible": e["disponible"],
                 "texte_affiche": e["texte_affiche"], "variante_aube": e["variante_aube"]})

T = {
    "etat": "PROVISOIRE — calage estime, non ecoute humainement",
    "duree_decodee_maitre": DUREE_DECODEE,
    "intro": {"debut": 0.0, "fin": vers[0]["debut_source"],
              "duree": round(vers[0]["debut_source"], 2),
              "note": "intervalle court : rythme d'intro a adapter au temps reel"},
    "outro": {"debut": DUREE_DECODEE, "fin": round(DUREE_DECODEE + OUTRO, 2), "duree": OUTRO,
              "carte": "MERCI · WTBW"},
    "duree_clip": round(DUREE_DECODEE + OUTRO, 2),
    "frames_clip_estimees": round((DUREE_DECODEE + OUTRO) * FPS),
    "teaser": {"duree": 15.00, "frames": 450, "fps": FPS,
               "extrait_propose": [164.99, 179.99],
               "etat": "PROPOSITION provisoire, bornes a confirmer par ecoute / analyse du signal"},
    "formule_affichage": "min(fin_vers - debut_vers, max(2.2 s, 0.30 s * nombre_de_mots)) — indicative, jamais utilisee pour masquer ou eteindre les paroles (§7)",
    "vers": rows,
}
with open(os.path.join(HERE, "timeline.json"), "w", encoding="utf-8") as fh:
    json.dump(T, fh, ensure_ascii=False, indent=2)
    fh.write("\n")

out = ["# TIMELINE — « Grand Marcheur » (PROVISOIRE)", "",
       "Générée depuis `verses_map.json` · 2026-11-15. **Calage estimé, déclaré, non écouté.**", "",
       "- Durée décodée du maître : **220,07 s** (ffmpeg n9.0.2) · intro **0 → 1,34 s** · outro **5,00 s**.",
       "- Durée clip complet estimée : **225,07 s**, ~6 752 frames à 30 i/s ; teaser **15,00 s / 450 frames**.",
       "- `fin = null` dans le contrat : ici `fin_estimee` = début du vers suivant (dernier vers → 220,07 s). Ce n'est **pas** une mesure de fin de vers.",
       "- Aucune syllabe tenue ni respiration n'a été repérée à l'écoute : **partie non vérifiée**.", "",
       "| i | début | fin estimée | durée plan | mots | affichage indicatif | image cuite | dispo |",
       "|---:|---:|---:|---:|---:|---:|---|---|"]
for r in rows:
    out.append("| %d | %.2f | %.2f | %.2f | %d | %.2f | `%s` | %s |" % (
        r["i"], r["debut_source"], r["fin_estimee"], r["duree_plan"], r["nb_mots"],
        r["duree_affichage_indicative"], r["image_cuite"], "oui" if r["disponible"] else "**non**"))
with open(os.path.join(HERE, "TIMELINE.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
print("vers:", len(rows), "| duree clip:", T["duree_clip"], "| frames:", T["frames_clip_estimees"])
print("sans image:", [r["i"] for r in rows if not r["disponible"]])
print("plan le plus court:", min(r["duree_plan"] for r in rows), "s | le plus long:", max(r["duree_plan"] for r in rows), "s")
