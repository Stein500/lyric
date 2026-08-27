# PROGRESS — Clip lyrics “Trop Belle” — Daïsky / TechStein

Date session : 2026-08-27
Branche Arena : `arena/01a043f0-lyric`

## Décisions validées par l’artiste

- Livrables : **TikTok/Reels/Shorts 9:16 d’abord**, puis déclinaisons autres formats.
- Durée : **respecter la durée complète du MP3**. Analyse Xing MP3 : environ **202.992 s = 3:23.0**.
- Écart noté : les paroles fournies finissent vers **3:13** ; les ~10 dernières secondes seront traitées comme outro/fade visuel-audio, sauf correction ultérieure.
- Style visuel mis à jour : **animation conte familial + BD africaine originale**, avec personnages noirs / afro-descendants, en gardant l’énergie dark trap cyan/ambre.
- Sous-titres : **ASS + traduction FR sous les lignes anglaises**, Wolof sans traduction, lignes françaises seules.

## Prompt de référence lu

Source : `PROMPT_UNIVERSEL_MAJ.md` — v4.2 finale rigoureuse.

Règles critiques retenues :

- Pas de texte/logo/watermark généré dans les images IA.
- Badge `⚡ DAÏSKY PROD` ajouté uniquement en post-production.
- Timings `-MM:SS` fournis par l’artiste = fin de vers.
- À partir de 1:50, tous les timings start/end seront explicitement hardcodés.
- Sous-titres ASS : WrapStyle 1, fade 80/120 ms, outline noir, ombre.
- Pipeline vidéo : frames préparées → clips silencieux → concat demuxer → burn ASS + mux audio.
- Vérifications finales : durée, blackdetect, contrôle visuel du dernier tiers.

## État chantier

- [x] MP3 `Trop Belle.mp3` repéré.
- [x] Prompt universel v4.2 lu.
- [x] Dossiers de travail créés.
- [x] `.gitignore` configuré sans ignorer `livrables/`.
- [x] Direction visuelle changée selon retour artiste : style animation + BD africaine.
- [x] Salve portrait 01–10 générée en style afro-BD animé.
- [ ] Validation artiste de la salve 01–10.
- [ ] Minutage lyrics complet en tableau.
- [ ] ASS portrait 9:16.
- [ ] Montage TikTok 9:16.
- [ ] Vérifications automatiques et visuelles.
- [ ] Déclinaison 16:9 YouTube.
- [ ] Commit/push de livrables validés.

## Notes minutage importantes

- Audio complet estimé depuis l’en-tête Xing : 8458 frames MP3 × 1152 / 48000 = **202.992 s**.
- Outro fourni : 3:03–3:13 ; extension prévue jusqu’à 3:23 si on garde le MP3 entier.


## Salve portrait 01–10 — style afro-BD animé

Fichiers générés dans `assets/raw/portrait/` :

1. `01_intro_wolof_signature_afro_bd.jpg`
2. `02_elle_est_trop_belle_afro_bd.jpg`
3. `03_refrain_scared_of_you_afro_bd.jpg`
4. `04_honte_hommes_virils_afro_bd.jpg`
5. `05_couplet_ame_transe_afro_bd.jpg`
6. `06_maladroit_sideral_afro_bd.jpg`
7. `07_trouille_peur_ventre_afro_bd.jpg`
8. `08_creature_etrange_oiseau_afro_bd.jpg`
9. `09_pre_refrain_roc_fissure_afro_bd.jpg`
10. `10_guerrier_sans_armure_afro_bd.jpg`

Contact sheet locale : `work/contact_sheet_portrait_01_10_afro_bd.jpg` (non commit, dossier work ignoré).
