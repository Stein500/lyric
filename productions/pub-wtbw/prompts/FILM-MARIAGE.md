# PROMPT 1 / 6 — FILM « MARIAGE » · 9:16 · 20 s

> Prompt autonome. Colle-le tel quel dans une IA vidéo/code ou donne-le à un monteur :
> tout ce qui est nécessaire est ici, sans dépendre d'un autre document.

---

## 1. Mission
Produire un film vertical de **20 secondes** pour **DSKY WTBW** (C. Jésutondji Samuel Stein,
auteur-compositeur béninois, 34 morceaux) qui vend le service **chanson de mariage sur mesure**.

Public : futurs mariés au Bénin et dans la diaspora (25–40 ans), budget cadeau 100–300 €.
Promesse : une chanson écrite pour *leur* histoire, livrée en audio + clip vertical.

## 2. Spécifications du livrable
| Élément | Valeur |
|---|---|
| Format | 1080 × 1920 (9:16), H.264, yuv420p, bt709, 30 fps |
| Durée | 20,00 s exactement |
| Son | AAC 192 kbps, −14 LUFS, crête ≤ −1,0 dBFS |
| Découpage | 6 cartes × 3,33 s, fondu enchaîné 0,34 s |
| Mouvement | push-in lent 1,015 → 1,065, grain σ 0,006 |
| Texte | Playfair Display (romain + italique) + Montserrat pour les micro-lignes |
| Interdits | visage identifiable, main d'IA, texte inventé par le modèle d'image |

## 3. Direction artistique — série « laiton »
Duotone chaud, extraction noir & blanc puis colorisation :
`ombre #0E0B08` · `lumière #F4E7CC` · `accent #C8A16B` · `encre #F6EFE3`.
Photos documentaires (mains, dos, silhouettes, objets), jamais de visage net.
La typographie est **toujours composée en code (PIL)**, jamais générée par un modèle d'image.

## 4. Découpage carte par carte
| # | Visuel | Titre (Playfair) | Sous-titre / micro-ligne |
|---|---|---|---|
| 1 | salle de fête floue, lumières | **LE PLUS BEAU JOUR** / *MÉRITE SA CHANSON.* | MARIAGE · BÉNIN |
| 2 | robe, mains, premiers pas de danse | **PREMIER REGARD** / **PREMIÈRE DANSE** / *PREMIÈRE CHANSON* | UN SEUL MORCEAU POUR TOUTE UNE VIE |
| 3 | entrée de la mariée, dos, contre-jour | **LE MOMENT OÙ ELLE ENTRE,** / *TOUT LE MONDE PLEURE.* | L'IMAGE QU'ON GARDE |
| 4 | mains sur une guitare, alliance | **TON NOM** / *DANS LE REFRAIN* | ÉCRIT POUR EUX |
| 5 | charbon (fond noir) | **34 MORCEAUX ÉCRITS.** / *LE VÔTRE SERA LE 35e.* | CATALOGUE DISPONIBLE |
| 6 | charbon (fond noir) | **TON MARIAGE** / *MÉRITE SA CHANSON.* | TIKTOK & YOUTUBE — @DSKYWTBW |

## 5. Musique (audio de l'artiste uniquement, jamais de voix IA)
Lit de 4 extraits, 5,5 s chacun, fondu 0,5 s, normalisé −14 LUFS :
1. **Ayon dèkpè** — 4,0 s
2. **Tu es trop belle** — 3,0 s
3. **Vivi O O R** — 5,0 s
4. **Le goût bon de la vie** — 4,0 s

## 6. Commande de régénération
```bash
python3 build_bed.py --mariage     # → cache/bed_mariage.m4a (20,5 s)
python3 film_service.py mariage    # → livrables/FILM-MARIAGE-9x16.mp4
```

## 7. Contrôles avant livraison
- durée 20,00 s (`ffprobe`), LUFS −14 ±0,5, crête ≤ −1,0 ;
- aucun texte hors marge (12 % de chaque côté) ;
- lisibilité au pouce sur un écran de téléphone, son coupé : chaque carte doit se comprendre seule ;
- le mot « mariage » apparaît dans les 2 premières secondes.
