# PROMPT 5 / 6 — FILM « CATALOGUE 34 » · 9:16 · 28,9 s

> Prompt autonome. C'est la preuve : les 34 pochettes défilent une par une,
> calées sur le montage des hooks. Sert de bande de démonstration et de preuve de volume.

---

## 1. Mission
Produire un film vertical de **28,86 secondes** qui montre **les 34 morceaux** du catalogue
DSKY WTBW, une pochette à la fois, sur un montage de 20 hooks issus des morceaux eux-mêmes.

Public : programmateurs, journalistes, nouveaux auditeurs. Objectif : en 29 secondes, on doit
comprendre qu'il y a un catalogue réel, produit, et pas trois singles.

## 2. Spécifications du livrable
| Élément | Valeur |
|---|---|
| Format | 1080 × 1920, H.264 yuv420p bt709, 30 fps, faststart |
| Durée | 28,86 s (= durée exacte du montage audio) |
| Son | AAC 192 kbps, −14 LUFS (montage `build_pub_audio.py`, 20 segments de 1,50 s) |
| Structure | carton d'ouverture 1,50 s · **34 pochettes × 0,76 s** · carton de fin 1,50 s |
| Rythme | coupes franches (pas de fondu entre pochettes), micro-flash à chaque coupe (2 %) |
| Fond | charbon #0E0B08, vignettage, grain σ 0,005 |

## 3. Gabarit d'une pochette à l'écran
- pochette carrée **860 × 860** centrée, x = 110, y = 360, filet laiton 1 px ;
- ombre portée douce (flou 26 px, opacité 0,55) ;
- en haut : `CATALOGUE` (Montserrat 22, interlettrage 0,42, opacité 0,45) et `NN / 34` (laiton) ;
- sous la pochette : titre en Playfair Display 74 px, ajusté à 84 % de largeur ;
- filet laiton 150 px, puis `DSKY · WTBW` (Montserrat 22, laiton 0,80) ;
- sigle « W » en bas, y = 1746.

## 4. Cartons
| Moment | Contenu |
|---|---|
| 0,0 – 1,5 s | `LE CATALOGUE` / **34** (360 px) / `MORCEAUX` / `ÉCRITS · COMPOSÉS · MIXÉS` |
| 1,5 – 27,4 s | les 34 pochettes dans l'ordre du catalogue (POCHE-01 → POCHE-34) |
| 27,4 – 28,9 s | **TOUT EST LÀ.** / `@DSKYWTBW` / `TIKTOK · YOUTUBE · WHATSAPP` |

Ordre : NOUKIKO TCHÉ WÊ · AYON DÈKPÈ · TU ES TROP BELLE · MONSTER POSITIVE ·
JE ME RELÈVE TOUJOURS · GBÈTCHÉ VIVI · NAN YI A GA DJIN WÊ · CONCENTRÉ SUR LE CHEMIN ·
SANGUIN · ON NOUS A VOLÉ NOTRE ÉDUCATION · ÇA MONTE, ÇA DESCEND · LE GOÛT BON DE LA VIE ·
MAHU TI TÈ GBÈ · VIVI O O R · GLACE · GOINFRES · GRAND MARCHEUR · MASQUE · GHOST U SEE ·
NONVI KONOU · YAFOY · LE SURVIVANT · JE SUIS PAUVRE ET RICHE · TESTOSTÉRONE ·
JE CRACHE LES DÉMONS · DÈS LE DÉBUT · ENTRE TES MAINS · CALM IN OFF DOWN · DRAGUE MOI ·
JE M'AIME TELLEMENT · SEUL DANS MA TÊTE · L'AMOUR EST LA RÉPONSE · MOTIVÉ ·
WOLOF TECHSTEIN — ESSAIE.

## 5. Commande de régénération
```bash
python3 build_pub_audio.py        # → cache/pub.m4a (28,86 s, 20 segments)
python3 film_catalogue.py         # → livrables/FILM-CATALOGUE-34-9x16.mp4
python3 film_catalogue.py --stills   # contrôle visuel dans stills/c*.jpg
```

## 6. Contrôles
- 34 pochettes présentes et dans le bon ordre (assert dans le script) ;
- 0,76 s par pochette : vérifier qu'un titre long (« ON NOUS A VOLÉ NOTRE ÉDUCATION »)
  reste lisible — sinon passer le titre à 64 px ;
- audio non modifié : montage + normalisation seulement, aucun traitement de voix ;
- conserver la version 1080 × 1920 et exporter une version 1080 × 1080 pour le feed.
