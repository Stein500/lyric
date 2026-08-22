# PROGRESS — Vidéo Lyrics « Héritage de mes parents » (Daïsky)

> Fichier de suivi anti-réinitialisation. Le reprendre en premier si la session redémarre.
> Dernière mise à jour : projet terminé, restauration post-reset effectuée.

## ⚠️ RÈGLE DE PERSISTANCE (apprise d'un reset réel)
Snapshot = le dossier de travail SAUF les dossiers nommés : `out/`, `build/`, `dist/`, `target/`, `.venv/`, `node_modules/`, `__pycache__/`, `.git/`…
→ **Le dossier des livrables s'appelle `livrables/` (JAMAIS `out/`).**
→ `~/.local` (pip --user) n'est pas restauré : réinstaller `pip3 install --user --break-system-packages pillow imageio-ffmpeg mutagen` après un reset.
→ Pousser sur GitHub dès que possible : seul le remote survit à tout.
→ Reconstruction complète possible via `src/` + `manifest.json` + `assets/images/` + `assets/raw/`.

## Incident 20/08 — reset d'espace
Commit initial perdu avec `.git` (re-cloné) + dossier `out/` non persisté.
Restauré : chemins renommés `out→livrables`, toolchain réinstallée, cover/pochette/MP3 régénérés, vidéo ré-encodée, commit+push refaits.

## Constat initial
- MP3 présent : `/home/user/lyric/Héritage de mes parents-Daïsky.mp3` (4,8 Mo)
- Artiste/branding (linktr.ee/daiskypro) : **Daïsky Pro (TechStein)** — « Wolof TechStein beat wê ! » — Bénin
  - YouTube/TikTok/Insta/X/Facebook : @daiskypro — Lien : https://linktr.ee/daiskypro
- Branche de travail : `arena/01a01f92-lyric` (ne JAMAIS pousser ailleurs)
- ffmpeg système absent → binaire via `imageio-ffmpeg` (python). Fonts : DejaVu dans /usr/share/fonts/truetype.
- Marque géographique/style : on garde l'esthétique cohérente avec les sorties précédentes de Daïsky (master : "i'm not dying").

## Charte graphique (TOUT doit suivre ceci — zéro décalage de style)
- Format : vertical 9:16, 1080x1920 (TikTok / YouTube Shorts / Reels)
- Palette : bleu nuit profond **#0B1026** → noir charbon **#05070F**, or ambré **#F2B33D**, reflets cuivre **#D97A2B**, texte ivoire **#F5EFDF**
- Style : silhouettes cinématiques contre-jour, lumière dorée volumétrique, grain de film léger, particules de poussière dorées, ambiance émotionnelle "sacrifice → lumière"
- **Aucun texte dans les images générées** (le texte est ajouté après, proprement, par incrustation)
- Ancre de style : `assets/images/01_intro.jpg` → toutes les autres la référencent
- Police sous-titres : DejaVu Sans Bold + contour doré

## Plan des 10 images (style strictement identique)
| # | Fichier | Passage | Timing vidéo | Scène |
|---|---------|---------|--------------|-------|
| 01 | 01_intro.jpg | INTRO (CTA) | 0:00–0:09 | Route vers soleil levant, famille 3 silhouettes → + badges LIKE / ABONNE-TOI / PARTAGE (incrustés) |
| 02 | 02_refrain.jpg | REFRAIN (x2) | 0:09–0:43 & 1:16.8–1:40 | Parents soulevant l'enfant vers disque solaire doré |
| 03 | 03_couplet1_pere.jpg | COUPLET1 A | 0:43–0:50.8 | Père rentrant 2h du matin, dos courbé, rue lampe froide |
| 04 | 04_couplet1_mere.jpg | COUPLET1 B | 0:50.8–1:04 | Mère, cuisine bougie, sourire, frigo vide |
| 05 | 05_prerefrain.jpg | PRÉ-REFRAIN (x2) | 1:04–1:16.8 & 2:01–2:14 | Escalier de lumière vers le ciel |
| 06 | 06_couplet2.jpg | COUPLET2 | 1:40–2:01 | Père valise aéroport aube + mère livre fermé (double exposition) |
| 07 | 07_pont.jpg | PONT | 2:14–2:35 | Étreinte adulte-parents, halo doré, piano seul |
| 08 | 08_refrain_final.jpg | REFRAIN FINAL | 2:35–3:05 | Sommet de montagne, explosion de particules d'or |
| 09 | 09_outro.jpg | OUTRO | 3:05–3:20 | Lanterne d'or montant dans nuit bleue (+ carte de fin) |
| 10 | 10_cover.jpg | COVER plateformes | (miniature) | Mains d'or libérant barque de lumière, espace titre |

## Étapes
- [x] 1. Audit dépôt + outillage (pip pillow/imageio-ffmpeg/mutagen) — MP3 = 201,72 s
- [x] 2. 10 images générées (ancre 01_intro validée, 9 déclinaisons verrouillées dessus) ✔ style synchronisé (planche `assets/contact_sheet.jpg`)
- [x] 3. Incrustations PIL : intro CTA (♥ LIKE / ✚ ABONNE-TOI / ↗ PARTAGE), carte de fin outro, cover titrée + pochette carrée (`src/prep_overlays.py`)
- [x] 4. `manifest.json` (11 segments, 47 lignes de paroles) + `lyrics.ass` (`src/gen_ass.py`, MarginV 430 = zone sûre TikTok)
- [x] 5. Montage v2 ✔ : `out/Heritage_DaiskyPro_Lyrics_9x16.mp4` — 1080×1920, 30 fps, 3:21.73 (= MP3), AAC 48 kHz 192k, loudnorm −14 LUFS, faststart, 37,9 Mo
- [x] 6. MP3 propre ✔ : `out/Héritage de mes parents - Daïsky (master propre).mp3` — 0 trace suno/c2pa (vérif binaire), tags propres + pochette 1400 embarquée, audio identique (copie de flux)
- [x] 7. `PROMPT_UNIVERSEL.md` réutilisable ✔
- [x] 8. QA finale ✔ : planche d'images cohérente, spot-checks t=5/12/47/58.5/118/136/172/190 OK, zones sûres respectées

## ✅ PROJET TERMINÉ — 20/08/2026 (9:16) · 🔁 EXTENSION YOUTUBE 16:9 — 21/08

### v2 — Version YouTube paysage (en cours)
- [x] 10 images paysage 16:9 (`assets/images/paysage/`, miroirs des 10 portraits) — **20 images au total** ✔
- [x] Badge « Daïsky Prod » haut-gauche (56,44 réf. 1920) **sur les 10 images paysage, même position** (`src/prep_paysage.py`)
- [x] Intro : titre + CTA + « Prod : Daïsky Prod • Studio : TechStein » ; Outro : carte de crédits complète (slogan, prod, studio, tél, emails, linktree)
- [x] `lyrics_yt.ass` : 6 STYLES DE POLICES variés (Refrain=Sans Bold, Couplet=Sans Mono Bold, PréRefrain=Serif Bold, Pont=Serif centré, Intro/Outro=Serif, Hook=or massif)
- [x] MP3 master propre REGÉNÉRÉ avec tags complets : TPE2/TPUB=Daïsky Prod, TENC=TechStein, COMM=slogan+prod+studio+contacts+linktree ✔ (+ APIC pochette) — toujours 0 trace suno/c2pa
- [x] Covers YT : `livrables/Cover_Heritage_YT_1920x1080.jpg` + `Cover_Heritage_YT_1280x720.jpg`
- [x] Encodage YT 16:9 ✔ → `livrables/Heritage_DaiskyPro_Lyrics_16x9_YT.mp4` (1920×1080, 30 fps, 3:21.73 = MP3, 38 Mo)
- [x] `PROMPT_UNIVERSEL.md` v2 (double format, badge fixe, polices variées, bloc identité/tags, règle livrables/)
- [x] QA YT ✔ (6 polices vérifiées, badge fixe partout, crédits OK) + commit + push

### v1 — faite le 20/08 (restaurée après reset, poussée en commit 2df6d73)
Livrables 9:16 : MP4 vertical, cover 1080×1920, pochette 1400.

### v4 — REEL 2 STICKERS (« Maman a arrêté ses études… ») — 22/08 (✅ terminé)
- [x] Prompt : ajout **§3bis RÈGLES PERMANENTES** (application auto à chaque création, plus rien à redemander) — demandé par l'utilisateur
- [x] Extrait n°2 : couplet2 → pré-refrain2 (**1:40–2:14 = 34,0 s**)
- [x] 10 images `assets/images/reel2/` (style B Sticker-Bomb, verrouillées sur l'ancre série r01) : études maman, papa aéroport, sablier jeunes/vieux, bulle de protection, toit victoire, pas→pages, photo de famille, trésor-héritage, porté sur le dos, saut entre toits
- [x] Badge fixe partout + CTA sur r201/r210 + @daiskypro (`src/prep_reel2.py` générique)
- [x] `reel2.ass` + `src/build_reel2.py` → sortie : `livrables/Reel2_Heritage_MamanPapa_9x16.mp4` (34,0 s, audio `-ss 100 -t 34`)
- [x] QA + commit + push

### v3 — REEL STICKERS VIRAL (« couplet 1 ») — 22/08 (✅ terminé)
- Demande : 10 images NOUVELLES, couleurs VIVES, personnes AFRICAINES, style sticker-bomb plein d'émojis → rafter likes/abos
- [x] Extrait choisi : couplet1 → pré-refrain (**0:43–1:16.8 = 33,8 s**, les punchlines les plus partageables)
- [x] 10 images `assets/images/reel/` (ancre r01_pere validée → 9 déclinaisons verrouillées) — palette vive : orange électrique / magenta / turquoise / jaune
- [x] Badge Daïsky Prod haut-gauche fixe sur les 10 (`src/prep_reel.py`) + CTA jaunes « ♥ LIKE / ✚ ABONNE-TOI / ↗ PARTAGE » sur r01 (début) ET r10 (fin) + @daiskypro
- [x] Raws dans `assets/raw/reel/`
- [x] Montage `src/build_reel.py` : coups secs à chaque punchline (durées = lignes), zoom punch 10 %, sous-titres `reel.ass` (blanc contour noir 72, chute « I'll touch the sky » en or 80)
- [x] Sortie : `livrables/Reel_Heritage_Viral_9x16.mp4` — **33,8 s pile**, 1080×1920, 30 fps, AAC 48 kHz, loudnorm −14, 18 Mo
- [x] QA frames t=1.5/11.5/26/32 ✔ | audio = extrait MP3 `-ss 43 -t 33.8`

## Sync lyrics (normalisée depuis les timings fournis)
Voir `manifest.json` (source de vérité).
