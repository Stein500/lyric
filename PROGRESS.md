# PROGRESS — branche arena/01a0594e-lyric

## 2026-08-31 — Étape 1 : Analyse « Le Survivant »
- [x] Environnement : python venv `/home/user/.venv` (imageio-ffmpeg ⇒ ffmpeg 7.0.2 binaire, mutagen, numpy, matplotlib). ffprobe indisponible (bloqué réseau) → probing via ffmpeg -i + mutagen + décodage PCM (durée exacte à l'échantillon).
- [x] Analyse MP3 `Le Survivant.mp3` : durée 149,960 s, 48 kHz stéréo, ID3v2.4, cover 360×360, Suno.
- [x] Loudness : I=-13,8 LUFS · TP=-0,7 dBTP (⚠️ > -1,5) · LRA 6,1 → masterisation requise.
- [x] Structure musicale détectée (13 blocs, STFT bandes + onsets) — voir `livrables/ANALYSE_Le_Survivant.md`.
- [x] Validation `le survivant... timing.txt` : 47 vers, 46/47 calés à ±0,35 s ; 1 écart mineur (2:24, voix chuchotée). **Timing FIABLE jusqu'à la fin** ; dérive vidéo = défaut montage segments (§0 v4.6), pas des paroles.
- [x] Pièges de parsing identifiés : tiret-séparateur `-1:02`, plage `0:06-0:07`, `Yeah...-2:18`.
- [x] Livrables : `livrables/ANALYSE_Le_Survivant.md` + `livrables/analyse/le_survivant_structure.png`.
- [x] .gitignore conforme (work/, .venv/, *.pyc ; livrables/ jamais ignoré).

## 2026-08-31 — Étape 2 : décisions + ancrage (en cours de validation)
- [x] Décisions : charte HYBRIDE (B dark/lightning + A chaleureux pont) · images 100 % IA · salves de 10 · 9:16 d'abord · endcard 2:24 + apad 5 s (total 2:35) · « un vers = une image » → **49 images 9:16 + 49 en 16:9 + 1 cover = 99 au total** (voir `livrables/PLAN_Le_Survivant.md`).
- [x] Ancres générées : `assets/raw/portrait/ancrage_B_dark.png` + `ancrage_A_pont.png` ; maquettes badge+vers : `livrables/analyse/ancrage_{B,A}_avec_badge_vers.png`.
- [x] Validation utilisateur du style d'ancrage → ✅ validé (B + A + style texte).
- [x] **SALVE 1/5 générée** : `assets/raw/portrait/s00_intro.png` → `s09_beatwe2.png` (slots 0-9, charte B) + planche contact `livrables/analyse/salve1_contact_sheet.png`.

- [x] **SALVE 5/5 générée (FINALE)** : s40→s48 — TOTAL **49/49 images 9:16** (768×1376 chacune, charte B + pont A).
- [x] Planches contact : `livrables/analyse/salve{1..5}_contact_sheet.png`.

## Prochaines étapes
- [ ] Validation salve 5 → pré-calcul des 49 fonds (upscale 1080×1920, letterbox, badge haut-gauche, JPEG q92).
- [ ] Rendu SOLUTION A : flux continu ceil(155×30)=4650 frames @30 FPS, vague + Ken Burns, mux audio master pad 5 s + afade/vf fade → `livrables/Le_Survivant_9x16_v1.mp4`.
- [ ] Vérifs §7 → 16:9 (salves paysages + rendu) → MP3 master -14 LUFS + tags → covers.


## 2026-08-31 — Étape 3 : RENDU 9:16 (SOLUTION A frame-accurate) ✅
- [x] Pré-calcul 49 fonds 1188×2112 JPEG q92 (marge Ken Burns) ; badge posé en post, pixel-identique.
- [x] `work/render9x16.py` : flux unique 4650 frames @30 FPS (chaque frame = t=i/30), vague par lettre (entrée staggered / ondulation continue / cascade inversée), Ken Burns, intro musical-only + titre, endcard crédits+contacts dès 2:29.5, apad 5 s → 2:35.00.
- [x] Vérifs §7 : durée 155.000 s = audio ±0.00 s ; 4650 frames ; blackdetect = 0 sauf 0,3 s finales du fade-out charte ; freezedetect = 0 ; frontières vers validées par diff pixel (MP4 vs logique, 8 temps dont zone 2:00+) ; badge statique (0,81 px).
- [x] ⚠️ INCIDENT anti-reset : sandbox restauré à d53dac9 en cours de session → récupéré via `git fetch origin + reset --hard FETCH_HEAD` (tout était pushé). Le push après CHAQUE étape a sauvé le travail.
- Livrable : `livrables/Le_Survivant_9x16_v1.mp4` (78,7 Mo, h264 crf19 + aac 192k).
- [ ] Suite : 16:9 (salves paysage + rendu) → MP3 master -14 LUFS + tags ID3 → covers.

## 2026-08-31 — Étape 4 : v2 (avance 0,03 s) + salve YT 1/5
- [x] NOUVELLE RÈGLE : vers affichés avec **0,03 s d'avance** sur timing.txt (`ADVANCE=0.03` dans work/common.py, `apply_advance()` ; fonds restent sur l'horloge musique).
- [x] `livrables/Le_Survivant_9x16_v2.mp4` — re-rendu complet 4650 frames. Vérifs : 2:35.00, 0 figé, noir = fade final seul, avance confirmée (S05 visible entre 24,97 et 25,00), zone 2:00+ OK (S43 @121,47), endcard OK.
- [x] SALVE YT 1/5 : 10 images 16:9 (`assets/raw/landscape/s00→s09`) + planche contact `livrables/analyse/salveYT1_contact_sheet.png`.
- [x] Cover : script `work/cover.py` prêt (GreatVibes auto-détecté si work/fonts/GreatVibes-Regular.ttf ajouté — tous les CDN fonts bloqués réseau, fallback serif incliné). Génération de la base reportée (limite 10 images/tour).

## 2026-08-31 — Étape 5 : COVERS de publication
- [x] Bases IA générées : `assets/raw/cover_base_9x16.png` + `cover_base_16x9.png` (héros + éclair doré + cœur lumineux, zones sombres réservées au texte).
- [x] `livrables/cover_survivant_9x16.jpg` (1080×1920) + `livrables/cover_survivant_16x9.jpg` (1920×1080) : titre glow ambre (GreatVibes auto si fourni), sous-titre Daïsky + label/genre/année, filement décoratif, badge haut-gauche identique au clip.
- [ ] En attente validation user → puis SALVE YT 2/5 (slots 10-19).
- [x] SALVE YT 2/5 : 10 images 16:9 (slots 10-19) + planche `salveYT2_contact_sheet.png`. (covers validées user)
- [x] SALVE YT 3/5 : 10 images 16:9 (slots 20-29) + planche `salveYT3_contact_sheet.png`.
- [x] SALVE YT 4/5 : 10 images 16:9 (slots 30-39 : fin couplet 2 + pré-ref B, pont A doré, 1er vers ref finale) + planche `salveYT4_contact_sheet.png`.
