# INVENTAIRE — DSKY · WTBW

Tout ce qui existe, où c'est, et à quoi ça sert. Dernière mise à jour : après la salve affiches.

## Vidéos (`livrables/`)

| Fichier | Durée | Format | Contenu |
|---|---|---|---|
| `PUB-WTBW-CATALOGUE-9x16.mp4` | 28,87 s | 1080×1920 | 20 cartons, les 34 titres cités, refrains du catalogue |
| `PUB-WTBW-BUMPER-5s-9x16.mp4` | 5,00 s | 1080×1920 | signature → morceau → promesse |
| `FILM-CITATIONS-9x16.mp4` | 20,40 s | 1080×1920 | 8 citations, lit musical calme |
| `FILM-SERVICES-9x16.mp4` | 13,00 s | 1080×1920 | 4 services + manifeste |
| `FILM-MARIAGE-9x16.mp4` | 20,00 s | 1080×1920 | série laiton : mariée, danse, cérémonie, refrain, catalogue, promesse |
| `FILM-MEMOIRE-9x16.mp4` | 24,00 s | 1080×1920 | noir et blanc : cadre, mains, album, chorale, la règle (pas de voix imitée), promesse |
| `FILM-ANNIVERSAIRE-9x16.mp4` | 16,00 s | 1080×1920 | série laiton : bougies, enfants, salle, tous les âges, promesse |

## Images

| Dossier | Nombre | Format | Quoi |
|---|---|---|---|
| `livrables/brand/` | 10 | 1080×1350 | planche logo + t-shirt, sweat, tote, casquette, baskets, sac, stickers, cartes, vinyle |
| `livrables/brand/print/` | 6 | PNG 2400 px + SVG | fichiers imprimeur (lockup, lettrage, badge, sigle) |
| `livrables/universel/` | 10 (+10 story) | 1080×1350 / 1080×1920 | citations, mains, silhouettes, services, manifeste |
| `livrables/variations/` | 10 | 1080×1350 | série laiton : duotone chaud, citation à gauche, « 34 », frise de commande, annonce |
| `livrables/affiches/` | 10 (+10 story) | 1080×1350 / 1080×1920 | mariage, anniversaire, mémoire, fête, clip, écriture, éducation, événement, église, partout |
| `livrables/pochettes/` | 10 + planche | 1080×1080 | pochettes vedettes |
| `livrables/pochettes/catalogue/` | 34 | 1080×1080 | tout le catalogue |

Plans de contrôle : `PLANCHE-10.jpg` (universel, pochettes), `PLANCHE-10-FEED.jpg` (affiches).

## Prompts

- `PROMPT-MAITRE.md` — l'IA interroge, tu valides, elle produit.
- `PROMPT-PUB-5-30s.md` — 15 / 30 / 60 s, couplet catalogue.
- `PROMPT-MARQUE.md` — sigle, lettrage, règles merch.

## Scripts

| Script | Sortie |
|---|---|
| `build_pub_audio.py` | `cache/pub.m4a` (28,86 s) |
| `build_bed.py` | `cache/bed.m4a` (21 s) |
| `build_bed.py --mariage` | `cache/bed_mariage.m4a` (20,5 s) |
| `film_service.py mariage` | `FILM-MARIAGE-9x16.mp4` (20 s) |
| `build_bed.py --memoire` / `--anniversaire` | lits graves 24,2 s / festif 16,4 s |
| `film_service.py memoire` / `anniversaire` | `FILM-MEMOIRE` (24 s) / `FILM-ANNIVERSAIRE` (16 s) |
| `pub_video.py` / `--bumper` | pubs 28,9 s / 5 s |
| `film_uni.py` / `--services` | films 20,4 s / 13 s |
| `logo.py` | 4 déclinaisons + fichiers imprimeur |
| `brand_kit.py` | 10 visuels merch |
| `universel.py` / `--story` | 10 cartes + versions story |
| `affiches.py` / `--story` | 10 affiches + versions story |
| `covers.py` / `--all` | 10 pochettes / 34 |

## Reste à faire (films, un par un)

1. ~~Film **MARIAGE**~~ ✅ `FILM-MARIAGE-9x16.mp4` (lit : Ayon dèkpè / Tu es trop belle / Vivi O O R / Le goût bon de la vie)
2. ~~Film **MÉMOIRE**~~ ✅ `FILM-MEMOIRE-9x16.mp4` (Mahu ti tè gbè / Entre tes mains / Calm in off down / Le goût bon de la vie)
3. ~~Film **ANNIVERSAIRE**~~ ✅ `FILM-ANNIVERSAIRE-9x16.mp4` (Noukiko / Ça monte ça descend / Gbètché vivi / Le goût bon de la vie)
4. Film **ÉDUCATION / ateliers** — 20 s, ton documentaire.
5. Film **CATALOGUE par pochettes** — 30 s, générique des 34 pochettes.
