# LIVRAISON — MONSTER POSITIVE · DSKY (WTBW)

## 1) Titre
**MONSTER POSITIVE — DSKY** (clip lyrics 9:16, 3:58.7, « Wolof TechStein beat 웨 ! »)

## 2) Captions (TikTok/Shorts/Reels)
- FR : « Ils m'ont appelé monstre… alors j'ai rendu ça positif. 🔥 MONSTER POSITIVE — DSKY. Lequel de tes "défauts" est devenu ta force ? 👇 »
- EN : « They called me a monster… so I made it positive. MONSTER POSITIVE — DSKY ⚡ Which "flaw" became your superpower? 👇 »

## 3) Hashtags (13 max)
#MonsterPositive #DSKY #WTBW #WolofTechStein #LyricsVideo #AfroAnime #TikTokMusic #NewMusic2026 #PositiveVibes #LyricShorts #Seinen #9x16 #FYP

## 4) Fichiers 9:16
- `livrables/MONSTER-POSITIVE-DSKY-9x16.mp4` — 1080×1920@30, 238,70 s, H.264 bt709 +faststart, AAC 256k 48 kHz
- `livrables/COVER-tiktok-1080x1920.jpg` — couverture dédiée (JPEG q95, 4:4:4)
- `livrables/master_normalise.mp3` — master artiste loudnorm 2 passes (−14,0 LUFS, −1,88 dBTP, 320k CBR)

## 5) Déclaration IA
- **Visuels : OUI** (44 plans générés par IA, lettrage cuit par moteur PIL, habillage animé par script)
- **Audio : NON** — master 100 % artiste (`Monster _ DSKY.m4a`, sha256 538e29b5…), aucune voix/musique générée, non retouché (seul un loudnorm de livraison + apad 6 s)

## 6) Contrôles (voir livrables/CONTROLES.txt)
- durée 238,70 s = 7161 frames/30 ✔ · blackdetect 0 ✔ · freezedetect −33dB/2,5s : 0 gel ✔ ·
  loudness −14,0 LUFS ✔ · crête −2,13 dBTP ✔ · faststart ftyp→moov→mdat ✔ · typo nette 1:1 ✔ · pilule FR lisible 1:1 (CONTROLE-pill-t24/t66.jpg) ✔ · badge DSKY/WTBW ✔ · aucune extinction/flou sur les paroles peintes ✔

## 7) Commandes Termux (une ligne par fichier, séparées par `;`)
```
pkg install -y curl && termux-setup-storage
```
```
curl -L --retry 3 -C - -o ~/storage/downloads/MONSTER-POSITIVE-DSKY-9x16.mp4 "https://raw.githubusercontent.com/Stein500/lyric/5da23237ee8232dfa9f01dfbf6344b9aeeac082d/productions/monster-positive/livrables/MONSTER-POSITIVE-DSKY-9x16.mp4"; termux-media-scan -v ~/storage/downloads/MONSTER-POSITIVE-DSKY-9x16.mp4;
curl -L --retry 3 -C - -o ~/storage/downloads/COVER-tiktok-1080x1920.jpg "https://raw.githubusercontent.com/Stein500/lyric/5da23237ee8232dfa9f01dfbf6344b9aeeac082d/productions/monster-positive/livrables/COVER-tiktok-1080x1920.jpg"; termux-media-scan -v ~/storage/downloads/COVER-tiktok-1080x1920.jpg;
curl -L --retry 3 -C - -o ~/storage/downloads/MONSTER-POSITIVE-DSKY-master.mp3 "https://raw.githubusercontent.com/Stein500/lyric/5da23237ee8232dfa9f01dfbf6344b9aeeac082d/productions/monster-positive/livrables/master_normalise.mp3"; termux-media-scan -v ~/storage/downloads/MONSTER-POSITIVE-DSKY-master.mp3
```
Liens raw **figés sur le SHA `5da23237ee8232dfa9f01dfbf6344b9aeeac082d`** (branche `prod/monster-positive`, vérifié `git ls-remote` + tailles blobs API : mp4 29 071 212 o, cover 381 696 o, mp3 9 350 791 o — tous < 50 Mo, en commit ordinaire).

## Notes de prod
- Prompt universel : `PROMPT-UNIVERSEL-v6.5.md` (v6.4 nettoyée le 2026-11-13 : badge « DSKY WTBW », pilule FR cotes §5.7 anti-collage, §5.4 extinction supprimée définitivement) · config : `PROD-CONFIG.md` (v6.5) · contrat : `verses_map.json` + `CARTE-VERS.md`
- 49 vers (LRC artiste inchangés) · 44 plans distincts + variante aube (v37) · MODE HYBRIDE : VO peinte + pilule FR défilante
- 6 fenêtres CTA clochettes · badge clignotant DSKY↔WTBW · cartes SALUT·WTBW / MERCI·WTBW animées · aucun code, aucun lien, aucun logo
- Texte des vers recopié à l'identique (y compris « lumiere »/« frontiere » sans accent, tels quels dans le fichier artiste)
