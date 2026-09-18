# Suivi de Production — Nan yi a ga djin wê (v5.1.1)

**Artiste :** Daïsky  
**Titre :** Nan yi a ga djin wê  
**Cadre :** PROMPT_UNIVERSEL_v5.1.1.md  
**Date :** 2026-09-18  
**Branche :** arena/01a0b5a3-lyric  

---

## 📊 État d'avancement

- [x] **§A. ANALYSE AUTOMATIQUE COMPLÈTE**
  - [x] A.1 Audio : Durée 162.80 s (2:42.80), SR 48000 Hz stéréo, BPM ~74 (double ~148 BPM Trap/Drill), Loudnorm mesuré (`input_i: -14.24`, `input_tp: -0.50`, `input_lra: 9.10`, `target_offset: -0.41`).
  - [x] A.2 Paroles : 48 vers horodatés analysés, structure identifiée (Intro, Refrain, Couplet 1, Pré-refrain, Refrain, Couplet 2, Pont EN, Refrain final, Outro).
  - [x] A.3 Validation vers par vers : Onsets spectraux alignés, monotonie et fenêtres vérifiées -> `work/timings_validated.json` et `Nan yi a ga djin wê.lrc` générés.
  - [x] A.4 Budget images : 36 vers uniques + 2 (intro s00 + endcard s37) = **38 images par format** (salves de 10 max).
  - [x] A.5 Cold-open : Refrain 1 (00:19.22 -> 00:25.22, 6.0 s) sélectionné.
  - [x] A.6 Identité visuelle : Bloc héros fidèle défini à partir des photos de Daïsky (`Snapchat-1818173374.jpg`, etc.) avec règle anti-embellissement absolue.
  - [x] Polices : `assets/fonts/GreatVibes-Regular.ttf` (couverture 100% vérifiée) et `assets/fonts/DejaVuSans-Bold.ttf`.
- [ ] **§B. QUESTIONNAIRE DE DÉMARRAGE** (en cours)
- [ ] **§C. PRODUCTION**
  - [ ] Salve 1 (s00-s09) : Ancre + 9 images
  - [ ] Salve 2 (s10-s19) : 10 images
  - [ ] Salve 3 (s20-s29) : 10 images
  - [ ] Salve 4 (s30-s37) : 8 images + Covers
  - [ ] Pré-calcul des fonds Ken Burns & masques
  - [ ] Rendu vidéo 9:16 (safe zones v5.1.1, texte au milieu, badge pilule dynamique)
  - [ ] Master audio 320k normalisé + tags ID3v2.4
  - [ ] Contrôles qualité D.10 (blackdetect, diff pixels, synchronisation)
  - [ ] Commandes de téléchargement Termux anti-casse
