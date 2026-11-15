# -*- coding: utf-8 -*-
"""Génère CARTE-VERS.md depuis data/verses_map.json (source unique de vérité)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m = json.load(open(os.path.join(ROOT, "data", "verses_map.json"), encoding="utf8"))
def ts(t):
    return f"{int(t//60)}:{t%60:06.3f}" if t is not None else "—"
out = ["# CARTE DES VERS — MESÍAS (Live) · Averly Morillo", "",
       f"Contrat généré depuis `data/verses_map.json` — {len(m['verses'])} occurrences.", "",
       "| # | début (s) | fin (s) | espagnol (source) | français (affiché) | image | dispo | reprise | contrôle |",
       "|---|---|---|---|---|---|---|---|---|"]
for v in m["verses"]:
    out.append("| {i} | {d} | {f} | {es} | {fr} | {im} | {dis} | {rep} | {st} |".format(
        i=v["i"], d=ts(v["debut_source"]), f=ts(v["fin"]),
        es=v["texte_source"].replace("|", "\\|"),
        fr=v["traduction_fr"].replace("|", "\\|"),
        im=v["image"] or "—", dis="oui" if v["disponible"] else "non",
        rep=v["reprise"] or "—", st=v["statut_controle"]))
out += ["", "## Limites de ce calage", "",
        "- Les débuts viennent de la source (lrclib.net id 7723062). Aucune écoute n'a pu être faite :",
        "  **l'audio maître n'est pas encore fourni**, donc les *fins* sont les débuts suivants et non",
        "  des fins mesurées. Le calage est **provisoire** jusqu'à écoute sur le master.",
        "- Les syllabes tenues et respirations ne sont pas identifiées : aucun CTA n'est placé sur un vers",
        "  tant que les fins réelles ne sont pas vérifiées.",
        "- 190 occurrences, 117 textes distincts ; une image dédiée par texte distinct, réutilisée sur reprise."]
open(os.path.join(ROOT, "CARTE-VERS.md"), "w", encoding="utf8").write("\n".join(out) + "\n")
print("CARTE-VERS.md", len(m["verses"]), "lignes")
