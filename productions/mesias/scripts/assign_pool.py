# -*- coding: utf-8 -*-
"""Assigne une image polyvalente à chaque vers 31→190 (les vers 1→30 gardent leur plan dédié).

Règles sémantiques sur les mots espagnols, puis lissage :
  - jamais deux fois de suite la même image quand une alternative existe ;
  - une même image ne revient pas avant 2 vers d'écart sur les refrains serrés ;
  - le pool réutilise aussi les plans dédiés des vers 1→30 (ancre, nef, cierges, porte…).
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# thème -> images candidates (ordre = préférence)
THEMES = [
    # salve 5 — plans ajoutés
    (r"manos|abre|recibe|ofrenda|entreg", ["pool_11_mains_ouvertes.png", "pool_19_deux_mains_serrees.png"]),
    (r"oraci[oó]n|oraba|silencio|esperando|conf[ií]o|descans", ["pool_12_yeux_fermes_priere.png", "pool_15_autel_bougies.png"]),
    (r"llor|llanto|l[aá]grima|clamor|grito|dolor|quebrant", ["pool_13_larmes_lumiere.png", "pool_12_yeux_fermes_priere.png"]),
    (r"multitud|pueblos|naciones|todos|juntos|adoran|adoraci[oó]n", ["pool_14_foule_mains.png", "pool_06_assemblee.png"]),
    (r"fuego|altar|incienso|santo|sacrificio|sangre", ["pool_15_autel_bougies.png", "pool_16_fenetre_lumiere.png"]),
    (r"puerta abierta|luz|ventana|resplandor|amanec", ["pool_16_fenetre_lumiere.png", "pool_20_aube_horizon.png"]),
    (r"agua|mar|r[ií]o|camina|sobre las aguas|profund", ["pool_17_marche_eau.png", "pool_05_couloir.png"]),
    (r"tormenta|nube|viento|cielo se abre|trueno|tempestad", ["pool_18_tempete_ciel.png", "pool_07_ciel.png"]),
    (r"nuevo|principio|mañana|d[ií]a nuevo|alba|renacer|aunqu", ["pool_20_aube_horizon.png", "pool_18_tempete_ciel.png"]),
    (r"templo|l[aá]mpara|coraz[oó]n|gimiendo|tierra", ["pool_09_eglise_vide.png", "plan_04.png"]),
    (r"esper|amado|te llamo", ["pool_01_nave.png", "pool_02_visage_calme.png", "plan_06.png"]),
    (r"vencido|batalla|ganado|ganar[aá]", ["pool_03_bras_leves.png", "plan_09.png"]),
    (r"aleluya|profec[ií]a|cumplir|prometido", ["pool_07_ciel.png", "plan_08.png"]),
    (r"como ahora|hoy|preparado|pronto", ["pool_02_visage_calme.png", "pool_05_couloir.png"]),
    (r"cu[aá]ntos|pueblo|iglesia|generaci[oó]n|desesperados|dile", ["pool_06_assemblee.png", "pool_01_nave.png"]),
    (r"todo ojo|humill|creaci[oó]n|rey de gloria|gloria|majestad|victoria|poder", ["pool_07_ciel.png", "pool_03_bras_leves.png"]),
    (r"entra|abran puertas|viene", ["pool_04_silhouette_porte.png", "plan_07.png"]),
    (r"ven\b|mes[ií]as|ll[aá]malo|llamo", ["pool_04_silhouette_porte.png", "pool_03_bras_leves.png", "plan_05.png"]),
    (r"sediento|ll[eé]name|resc[aá]tame|llena|deseo|hambre|hermosura|belleza|santidad|rostro|verte",
     ["pool_08_mains.png", "plan_03.png", "pool_02_visage_calme.png"]),
]
DEFAULT = ["pool_01_nave.png", "pool_05_couloir.png", "pool_10_colline.png", "pool_02_visage_calme.png",
           "pool_09_eglise_vide.png", "plan_04.png", "plan_06.png", "pool_16_fenetre_lumiere.png",
           "pool_20_aube_horizon.png", "pool_14_foule_mains.png", "pool_11_mains_ouvertes.png",
           "pool_17_marche_eau.png"]

def pick(text, last, recent, counts):
    """Choisit dans le thème, à égalité de pertinence, l'image la moins employée."""
    def best(imgs):
        free = [im for im in imgs if im != last and im not in recent]
        pool = free or [im for im in imgs if im != last] or imgs
        return min(pool, key=lambda im: (counts.get(im, 0), imgs.index(im)))
    for pat, imgs in THEMES:
        if re.search(pat, text, re.I):
            return best(imgs)
    return best(DEFAULT)

def main():
    path = os.path.join(ROOT, "data", "verses_map.json")
    m = json.load(open(path, encoding="utf8"))
    last, recent = None, []
    counts = {}
    for v in m["verses"]:
        if v["i"] <= 30:
            counts[v["image"]] = counts.get(v["image"], 0) + 1
            last, recent = v["image"], ([v["image"]] + recent)[:2]
            continue
        im = pick(v["texte_source"], last, recent, counts)
        v["image"] = im
        v["disponible"] = True
        v["statut_controle"] = "non_controle"
        counts[im] = counts.get(im, 0) + 1
        last = im
        recent = ([im] + recent)[:2]
    json.dump(m, open(path, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print("images utilisées :", len(counts))
    for k, c in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {k:28s} {c:3d} vers")

if __name__ == "__main__":
    main()
