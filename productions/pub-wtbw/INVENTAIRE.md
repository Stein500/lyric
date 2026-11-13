# INVENTAIRE — DSKY · WTBW

Tout ce qui existe, où c'est, et à quoi ça sert. Dernière mise à jour : après la salve affiches.

## Vidéos (`livrables/`)

| Fichier | Durée | Format | Contenu |
|---|---|---|---|
| `PUB-WTBW-CATALOGUE-9x16.mp4` | 28,87 s | 1080×1920 | 20 cartons, les 34 titres cités, refrains du catalogue |
| `PUB-WTBW-BUMPER-5s-9x16.mp4` | 5,00 s | 1080×1920 | signature → morceau → promesse |
| `FILM-CITATIONS-9x16.mp4` | 20,40 s | 1080×1920 | 8 citations, lit musical calme |
| `FILM-SERVICES-9x16.mp4` | 13,00 s | 1080×1920 | 4 services + manifeste |

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
| `pub_video.py` / `--bumper` | pubs 28,9 s / 5 s |
| `film_uni.py` / `--services` | films 20,4 s / 13 s |
| `logo.py` | 4 déclinaisons + fichiers imprimeur |
| `brand_kit.py` | 10 visuels merch |
| `universel.py` / `--story` | 10 cartes + versions story |
| `affiches.py` / `--story` | 10 affiches + versions story |
| `covers.py` / `--all` | 10 pochettes / 34 |

## Reste à faire (films, un par un)

1. Film **MARIAGE** — 20 s à partir de l'affiche 01 + mains + pochettes.
2. Film **MÉMOIRE** — 25 s, le plus délicat : pas de deepfake, pas de voix clonée.
3. Film **ANNIVERSAIRE** — 15 s, rythmé.
4. Film **ÉDUCATION / ateliers** — 20 s, ton documentaire.
5. Film **CATALOGUE par pochettes** — 30 s, générique des 34 pochettes.
