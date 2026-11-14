# PROMPT 3 / 6 — FILM « ANNIVERSAIRE » · 9:16 · 16 s

> Prompt autonome.

---

## 1. Mission
Produire un film vertical de **16 secondes** pour **DSKY WTBW** qui vend la **chanson
d'anniversaire personnalisée** (prénom + âge + private joke), à envoyer en story ou en cadeau.

Public : 18–40 ans, Bénin + diaspora. Achat impulsif, prix cadeau (< 50 €).
Rythme : plus rapide que le film mariage, coupes toutes les 3,2 s.

## 2. Spécifications du livrable
| Élément | Valeur |
|---|---|
| Format | 1080 × 1920, H.264 yuv420p bt709, 30 fps |
| Durée | 16,00 s (5 cartes × 3,2 s, fondu 0,34 s) |
| Son | AAC 192 kbps, −14,1 LUFS, crête −1,5 dBFS |
| Série | « laiton » (#0E0B08 / #F4E7CC / #C8A16B / #F6EFE3), grain σ 0,006 |

## 3. Découpage
| # | Visuel | Titre | Micro-ligne |
|---|---|---|---|
| 1 | bougies, mains, gâteau | **UN ANNIVERSAIRE** / *ÇA SE CHANTE.* | PAS LE MÊME « JOYEUX » POUR TOUT LE MONDE |
| 2 | enfants qui courent dans une cour | **UN MORCEAU QU'ILS ÉCOUTERONT** / *DANS VINGT ANS.* | POUR UN ENFANT, POUR TOUJOURS |
| 3 | salle, confettis, dos | **TOUTE LA SALLE** / *CHANTERA TON NOM.* | LE PRÉNOM DANS LE REFRAIN |
| 4 | charbon | **DE 1 À 100 ANS,** / *UN MORCEAU POUR CHAQUE ÂGE.* | 34 MORCEAUX DÉJÀ ÉCRITS |
| 5 | charbon | **TON ANNIVERSAIRE** / *MÉRITE SA CHANSON.* | TIKTOK & YOUTUBE — @DSKYWTBW |

## 4. Musique (audio de l'artiste uniquement)
4 extraits de 4,4 s, fondu 0,4 s, −14 LUFS — uniquement des morceaux où la joie s'entend :
**Noukiko tché wê** (0:06,8) → **Ça monte, ça descend** (0:08,4) →
**Gbètché vivi** (0:08,9) → **Le goût bon de la vie** (0:10,0).

## 5. Commande de régénération
```bash
python3 build_bed.py --anniversaire     # → cache/bed_anniversaire.m4a (16,4 s)
python3 film_service.py anniversaire    # → livrables/FILM-ANNIVERSAIRE-9x16.mp4
```

## 6. Contrôles
- durée 16,00 s, −14,1 LUFS ;
- le mot « anniversaire » dans la première seconde ;
- la carte 4 doit rendre l'échelle du catalogue évidente (34) ;
- lisible sans son, exporté aussi en couverture 1080 × 1350 si besoin pour le feed.
