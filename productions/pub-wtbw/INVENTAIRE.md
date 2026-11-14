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
| `FILM-EDUCATION-9x16.mp4` | 20,00 s | 1080×1920 | série laiton : atelier, écriture, chaîne écriture→master, transmission, 4 métiers, CTA |
| `FILM-CATALOGUE-34-9x16.mp4` | 28,83 s | 1080×1920 | les 34 pochettes une par une (0,76 s), cartons ouverture/fermeture, lit = montage des hooks |

## Images

| Dossier | Nombre | Format | Quoi |
|---|---|---|---|
| `livrables/brand/` | 10 | 1080×1350 | planche logo + t-shirt, sweat, tote, casquette, baskets, sac, stickers, cartes, vinyle |
| `livrables/brand/logo/` | 26 | PNG (250 / 1080 / 2000 transparent) + planche | **LOGO WTBW SEUL** : sigle, lettrage, sigle+lettrage · 3 coloris · avatar 250 prêt TikTok |
| `livrables/brand/story/` | 4 | 1080×1920 | stories à publier : marque, lettrage géant, nouveau son, service |
| `livrables/brand/print/` | 11 | PNG 2400 px + **3 SVG vectoriels** (`WTBW-sigle`, `WTBW-lettrage`, `WTBW-sigle-lettrage`) | fichiers imprimeur (lockup, lettrage, badge, sigle) + 2 variantes **état civil STEIN** |
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
- `prompts/FILM-MARIAGE.md`, `FILM-MEMOIRE.md`, `FILM-ANNIVERSAIRE.md`, `FILM-EDUCATION.md`,
  `FILM-CATALOGUE-34.md`, `MARQUE-LOGO.md` — **6 prompts autonomes** : chacun contient tout
  (brief, découpage, textes exacts, musique, specs techniques, commande, contrôles).
- `README.md` racine : `PROMPT_UNIVERSEL_v7.0.md` (prompt maître v7.0, marque GitHub incluse)
- `TERMUX.md` — installation Termux + script `get-livrables.sh` (tout en une commande).
- `COMMANDES.md` — **un `curl` par fichier** (126 fichiers), copiable ligne par ligne.
- `LEGENDES.md` — **une légende par vidéo** : TikTok/Reels, Statut WhatsApp, hashtags.

## Scripts

| Script | Sortie |
|---|---|
| `build_pub_audio.py` | `cache/pub.m4a` (28,86 s) |
| `build_bed.py` | `cache/bed.m4a` (21 s) |
| `build_bed.py --mariage` | `cache/bed_mariage.m4a` (20,5 s) |
| `film_service.py mariage` | `FILM-MARIAGE-9x16.mp4` (20 s) |
| `build_bed.py --memoire` / `--anniversaire` | lits graves 24,2 s / festif 16,4 s |
| `film_service.py memoire` / `anniversaire` | `FILM-MEMOIRE` (24 s) / `FILM-ANNIVERSAIRE` (16 s) |
| `build_bed.py --education` | `cache/bed_education.m4a` (20,1 s) |
| `film_service.py education` | `FILM-EDUCATION-9x16.mp4` (20 s) |
| `film_catalogue.py` / `--stills` | `FILM-CATALOGUE-34-9x16.mp4` (28,8 s) — 34 pochettes |
| `logo_wtbw.py` | `livrables/brand/logo/` (27) + `livrables/brand/story/` (4) — logo WTBW seul, 250/1080/2000 |
| `logo_svg.py` | 3 SVG vectoriels (contours de glyphes, aucune IA) |
| `make_termux.py` | `TERMUX.md` (curl de tous les livrables) |
| `brand_kit.py print_files_stein` | lockups PNG avec la ligne C. JÉSUTONDJI SAMUEL STEIN |
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
4. ~~Film **ÉDUCATION / ateliers**~~ ✅ `FILM-EDUCATION-9x16.mp4` (On nous a volé notre éducation / Nan yi a ga djin wê / Concentré sur le chemin / Je me relève toujours)
5. ~~Film **CATALOGUE par pochettes**~~ ✅ `FILM-CATALOGUE-34-9x16.mp4` (34 pochettes, lit = montage des 20 hooks)

**Série complète : 5 films de service + 2 pubs + 1 film citations = 8 vidéos.**
