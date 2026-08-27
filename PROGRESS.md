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
- [x] Salve portrait 11–20 générée : couleurs vives rose/blanc/vert, afro-BD animé, plus de personnages noirs.
- [ ] Validation artiste de la salve 11–20.
- [ ] Minutage lyrics complet en tableau.
- [x] ASS portrait 9:16 généré.
- [x] Montage TikTok 9:16 v1 généré.
- [x] Vérifications automatiques et planche QC visuelle générées.
- [ ] Validation artiste du MP4 9:16 v1.
- [ ] Déclinaison 16:9 YouTube.
- [x] Salve paysage YouTube 16:9 01–10 générée.
- [ ] Validation artiste salve paysage 01–10.
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


## Salve portrait 11–20 — afro-BD animé couleurs vives

Consigne artiste : continuer avec couleurs vives — rose, blanc, vert, etc. — et plus de personnages noirs / afro-descendants, moins d’ambiance sombre.

Fichiers générés dans `assets/raw/portrait/` :

11. `11_refrain_lumineux_rose_vert_afro_bd.jpg`
12. `12_tempetes_lions_couleurs_vives_afro_bd.jpg`
13. `13_colosse_argile_afro_bd_color.jpg`
14. `14_brouillard_rose_vert_afro_bd.jpg`
15. `15_enigme_paradoxe_afro_bd.jpg`
16. `16_pre_refrain_violin_white_green_afro_bd.jpg`
17. `17_pont_piano_calme_afro_bd_couleur.jpg`
18. `18_genoux_amour_afro_bd_vif.jpg`
19. `19_poete_douleur_rose_blanc_vert.jpg`
20. `20_hook_final_tutti_afro_bd_bright.jpg`

Contact sheet locale : `work/contact_sheet_portrait_11_20_bright_afro_bd.jpg` (non commit, dossier work ignoré).


## Vidéo portrait 9:16 v1 — générée et contrôlée

Livrable : `livrables/trop_belle_9x16_v1.mp4`
Rapport QC : `livrables/trop_belle_9x16_v1_QC.md`
Script reproductible : `scripts/build_trop_belle_9x16_v1.py`
Sous-titres : `data/trop_belle_9x16_v1.ass`
Timeline : `data/trop_belle_timeline_v1.json`
Segments vidéo : `data/trop_belle_video_segments_9x16_v1.json`

Contrôles :

- Durée audio : 202.992 s
- Durée vidéo : 202.983 s
- Écart : 0.009 s — OK ±0.30 s
- Blackdetect >300 ms : 0 — OK
- Taille MP4 : 43.1 MB
- QC visuelle : planche extraite à 0.5, 20.5, 49.0, 74.0, 103.0, 129.0, 159.0, 176.0, 185.5, 193.5, 200.0, 202.5 s et enregistrée dans `livrables/trop_belle_9x16_v1_QC_sheet.jpg`.

Notes : première version portrait produite avec les 20 images existantes uniquement, en réutilisant certaines images sur hooks/outro. À valider par l’artiste avant déclinaison finale/autres formats.


## Règle téléchargement Android ajoutée

À partir de maintenant, toutes les commandes de téléchargement partagées avec l’artiste doivent écrire dans :

`/storage/emulated/0/Web+/`

Le prompt universel `PROMPT_UNIVERSEL_MAJ.md` a été mis à jour pour imposer ce dossier, avec `mkdir -p`, nettoyage ciblé et `curl -C -` reprenable.


## Salve paysage 16:9 01–10 — YouTube

Consigne artiste : générer les 10 premières images YouTube, rester dans le même style que la vidéo TikTok validée.

Direction : animation conte familial originale + BD africaine, personnages noirs / afro-descendants, couleurs vives rose/blanc/vert/cyan/or, ambiance propre et lumineuse, sans texte/logo généré.

Fichiers générés dans `assets/raw/landscape/` :

1. `01_intro_wolof_signature_afro_bd_16x9.jpg`
2. `02_elle_est_trop_belle_afro_bd_16x9.jpg`
3. `03_refrain_scared_of_you_afro_bd_16x9.jpg`
4. `04_honte_hommes_virils_afro_bd_16x9.jpg`
5. `05_couplet_ame_transe_afro_bd_16x9.jpg`
6. `06_maladroit_sideral_afro_bd_16x9.jpg`
7. `07_trouille_peur_ventre_afro_bd_16x9.jpg`
8. `08_creature_etrange_oiseau_afro_bd_16x9.jpg`
9. `09_pre_refrain_roc_fissure_afro_bd_16x9.jpg`
10. `10_guerrier_sans_armure_afro_bd_16x9.jpg`

Contact sheet locale : `work/contact_sheet_landscape_01_10_afro_bd.jpg` (non commit, dossier work ignoré).
