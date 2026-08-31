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

## Prochaines étapes (en attente réponses)
- [ ] Confirmer charte visuelle (reco B Dark/Lightning), source images, périmètre, écran de fin.
- [ ] Générer images (2 salves ≤10), pré-calcul fonds + badge haut-gauche.
- [ ] Pipeline SOLUTION A : flux continu 4500 frames @30 FPS + mux audio master pad + fade.
- [ ] Exports 9:16 + 16:9, cover, MP3 master -14 LUFS + tags ID3 complets.
- [ ] Vérifications obligatoires §7 puis commit/push.
