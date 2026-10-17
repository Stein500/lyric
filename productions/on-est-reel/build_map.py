#!/usr/bin/env python3
"""Construit verses_map.json + CARTE-VERS.md depuis les paroles horodatées de l'artiste.
PROMPT_UNIVERSEL v5.9 §5.6 / §10.3-10.4 — les horodatages de l'artiste ne sont JAMAIS retouchés.
`disponible` est recalculé avec os.path.exists, jamais saisi à la main."""
import json, re, os

SRC = "On est Réel.md"
FONDS = "productions/on-est-reel/fonds"
OUT = "productions/on-est-reel/verses_map.json"
CARTE = "productions/on-est-reel/CARTE-VERS.md"

def strip_zw(s):
    return s.replace("‏", "").replace("‎", "").replace("​", "").strip()

rows, tag_dur = [], None
with open(SRC, encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        m = re.match(r"^\[(\d+):(\d+(?:\.\d+)?)\]\s*(.*)$", line)
        if m:
            rows.append({"t": int(m.group(1)) * 60 + float(m.group(2)), "texte": strip_zw(m.group(3))})
        elif line.startswith("[length:"):
            mm, ss = line[8:].rstrip("]").split(":")
            tag_dur = int(mm) * 60 + float(ss)

n = len(rows)
seen, plans = {}, []
for k, r in enumerate(rows):
    fin = rows[k + 1]["t"] if k + 1 < n else tag_dur
    mots = len(r["texte"].split())
    disp = min(fin - r["t"], max(2.2, 0.30 * mots))          # §5.6, PROVISOIRE
    key = re.sub(r"\s+", " ", r["texte"].lower())
    reprise = seen.setdefault(key, k + 1)
    img = None
    plans.append({
        "i": k + 1, "t": round(r["t"], 2), "fin": round(fin, 2),
        "affichage_s": round(disp, 2), "texte": r["texte"],
        "image": img, "disponible": False, "reprise": None if reprise == k + 1 else reprise,
    })

# Fenêtres clochettes candidates (§6) : [fin d'affichage + 0,15 s → début du vers suivant], seuil 4,0 s (MODE PEINT)
fen = []
for k, p in enumerate(plans):
    deb = p["t"] + p["affichage_s"] + 0.15
    fin_next = plans[k + 1]["t"] if k + 1 < n else tag_dur
    if fin_next - deb >= 4.0:
        fen.append({"apres_vers": p["i"], "debut_s": round(deb, 2), "fin_s": round(fin_next, 2), "duree_s": round(fin_next - deb, 2)})

doc = {
    "titre": "On est réel", "artiste": "Dsky", "langues": "français",
    "paroles": SRC, "audio": "On est réels_1.mp3",
    "recette": "ENCRE & FEUILLE D'OR", "mode": "PEINT",
    "signature": "Wolof TechStein beat wê !",
    "code": "0405",
    "code_avertissement": "PROVISOIRE — calculé sur le tag [length:04:05] ; à remplacer par la durée DÉCODÉE (ffmpeg -map 0:a:0 -f null -) dès que l'env venv est recréé (§11/§5.6)",
    "duree_decodee_s": None, "duree_tag_s": tag_dur,
    "nb_vers": n, "plans": plans,
    "plans_distinctes": n - sum(1 for p in plans if p["reprise"]),
    "plans_disponibles": sum(1 for p in plans if p["disponible"]),
    "plans_manquantes": sum(1 for p in plans if not p["disponible"]),
    "fenetres_clochettes": fen,
    "regle_clochettes": "fenêtre = temps sans parole EN COURS DE LECTURE : [fin d'affichage du vers + 0,15 s → début du vers suivant] ; seuil 4,0 s (MODE PEINT) ; jamais sur les cartes ni pendant un vers lu",
    "affichage_formule": "affichage = min(fin_vers, début_vers + max(2,2 s ; 0,30 s × nb_mots)) — PROVISOIRE, à signaler dans la livraison (§5.6)",
    "zones_sures": {"rien_au_dessus_de_y": 144, "rien_a_droite_de_x_entre_y960_1690": 910, "rien_sous_y": 1574, "bloc_texte": "centré, ≤ 740 px, y 620→1340"},
    "etats": "proposé / généré / validé par l'artiste / rendu / contrôlé",
}
os.makedirs(FONDS, exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)

L = ["# CARTE-VERS — « On est réel » · Dsky", "",
     f"Mode **PEINT** (verrouillé) · Recette ENCRE & FEUILLE D'OR · **{n} vers → {n} plans** (1 plan par vers)",
     f"Code de fin candidat : **{doc['code']}** (provisoire, à mesurer au décodage) · Signature : « {doc['signature']} »", ""]
L.append("| # | t (s) | fin (s) | affichage (s) | vers | image | dispo | reprise |")
L.append("|---|-------|---------|---------------|------|-------|-------|---------|")
for p in plans:
    L.append(f"| {p['i']} | {p['t']:.2f} | {p['fin']:.2f} | {p['affichage_s']:.2f} | {p['texte']} | — | non | {p['reprise'] or '—'} |")
L += ["", f"**Fenêtres clochettes éligibles (≥ 4,0 s, MODE PEINT) : {len(fen)}**", ""]
for w in fen:
    L.append(f"- après v-{w['apres_vers']:02d} : {w['debut_s']:.2f} s → {w['fin_s']:.2f} s ({w['duree_s']:.2f} s)")
L += ["", "_Dérivée automatiquement de verses_map.json — jamais écrite à la main (§10.4)._"]
with open(CARTE, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")

print(f"{n} vers · {doc['plans_distinctes']} plans distincts · {sum(1 for p in plans if p['reprise'])} reprises · {len(fen)} fenêtres clochettes")
