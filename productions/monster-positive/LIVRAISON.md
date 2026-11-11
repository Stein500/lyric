# LIVRAISON — MONSTER POSITIVE · Daïsky (WTBW)

## 1) Titre
**MONSTER POSITIVE — Daïsky** (clip lyrics 9:16, 3:58.7, « Wolof TechStein beat 웨 ! »)

## 2) Captions (TikTok/Shorts/Reels)
- FR : « Ils m'ont appelé monstre… alors j'ai rendu ça positif. 🔥 MONSTER POSITIVE — Daïsky. Lequel de tes "défauts" est devenu ta force ? 👇 »
- EN : « They called me a monster… so I made it positive. MONSTER POSITIVE — Daïsky ⚡ Which "flaw" became your superpower? 👇 »

## 3) Hashtags (13 max)
#MonsterPositive #Daïsky #WTBW #WolofTechStein #LyricsVideo #AfroAnime #TikTokMusic #NewMusic2026 #PositiveVibes #LyricShorts #Seinen #9x16 #FYP

## 4) Fichiers 9:16
- `livrables/MONSTER-POSITIVE-Daïsky-9x16.mp4` — 1080×1920@30, 238,70 s, H.264 bt709 +faststart, AAC 256k 48 kHz
- `livrables/COVER-tiktok-1080x1920.jpg` — couverture dédiée (JPEG q95, 4:4:4)
- `livrables/master_normalise.mp3` — master artiste loudnorm 2 passes (−14,0 LUFS, −1,88 dBTP, 320k CBR)

## 5) Déclaration IA
- **Visuels : OUI** (44 plans générés par IA, lettrage cuit par moteur PIL, habillage animé par script)
- **Audio : NON** — master 100 % artiste (`Monster _ Daïsky.m4a`, sha256 538e29b5…), aucune voix/musique générée, non retouché (seul un loudnorm de livraison + apad 6 s)

## 6) Contrôles (voir livrables/CONTROLES.txt)
- durée 238,70 s = 7161 frames/30 ✔ · blackdetect 0 ✔ · freezedetect −33dB/2,5s : 0 gel ✔ ·
  loudness −14,0 LUFS ✔ · crête ≤ −1,0 dB ✔ · faststart ftyp→moov→mdat ✔ · typo nette 1:1 (CONTROLE-paroles.jpg / CONTROLE-typo-zoom.jpg) ✔

## 7) Commandes Termux (une ligne par fichier, séparées par `;`)
```
pkg install -y curl && termux-setup-storage
```
```
curl -L --retry 3 -C - -o ~/storage/downloads/MONSTER-POSITIVE-DAISKY-9x16.mp4 "<URL_RAW_MP4@SHA>"; termux-media-scan -v ~/storage/downloads/MONSTER-POSITIVE-DAISKY-9x16.mp4;
curl -L --retry 3 -C - -o ~/storage/downloads/COVER-tiktok-1080x1920.jpg "<URL_RAW_COVER@SHA>"; termux-media-scan -v ~/storage/downloads/COVER-tiktok-1080x1920.jpg;
curl -L --retry 3 -C - -o ~/storage/downloads/MONSTER-POSITIVE-DAISKY-master.mp3 "<URL_RAW_MP3@SHA>"; termux-media-scan -v ~/storage/downloads/MONSTER-POSITIVE-DAISKY-master.mp3
```
(Liens raw figés sur le SHA du commit de livraison, branche `prod/monster-positive`.)

## Notes de prod
- Prompt universel : `PROMPT-UNIVERSEL-v6.4.md` (harmonie v6.0 × v6.3) · config : `PROD-CONFIG.md` · contrat : `verses_map.json` + `CARTE-VERS.md`
- 49 vers (LRC artiste inchangés) · 44 plans distincts + variante aube (v37) · MODE HYBRIDE : VO peinte + pilule FR défilante
- 6 fenêtres CTA clochettes · badge clignotant Daïsky↔WTBW · cartes SALUT·WTBW / MERCI·WTBW animées · aucun code, aucun lien, aucun logo
- Texte des vers recopié à l'identique (y compris « lumiere »/« frontiere » sans accent, tels quels dans le fichier artiste)
