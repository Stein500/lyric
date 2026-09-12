# Toko Longa — production progress

**Projet :** lyric visual vertical 9:16 + teaser + trois covers
**Titre :** *Toko Longa*
**Artiste :** Nass'M Rodyboy
**Réalisation lyric visual :** Techstein / DSKY Prod
**Branche :** `arena/01a09162-lyric`
**Référence :** prompt universel v4.8.2, règle stricte « une image par ligne unique »
**Direction :** documentaire cinématique, mariage visuel Bénin × Congo, terre rouge, palmiers, travail collectif, cyan discret et ambre solaire.

## Correction demandée — nouvelle passe stricte

La première vidéo `Toko_Longa_lyrics_9x16_v1.mp4` est conservée comme brouillon technique, mais elle n'est **pas** la version conforme au prompt : elle utilise des plaques narratives réutilisées.

Le LRC contient **73 entrées horodatées**, soit **63 lignes uniques** après déduplication. Le rendu conforme demande donc :

- 63 images portrait distinctes, une par ligne unique ;
- les refrains/ad-libs répétés réutilisent l'image de leur première occurrence ;
- 1 image d'intro + 1 image d'endcard ;
- total cible : **65 images portrait 9:16** ;
- les cinq images du teaser restent un budget séparé de cinq images.

## Salves portrait 9:16

- [x] Salve 01 générée : slots `s01` à `s10`.
- [x] Salve 01 validée pour continuer.
- [x] Salve 02 générée : slots `s11` à `s20`.
- [x] Salve 02 validée avec demande de refaire l'image `s12`.
- [x] Correction de `s12` avec un casting féminin différent.
- [x] Salve 03 générée : correction `s12` + slots `s21` à `s29` (10 générations).
- [x] Salve 03 validée pour continuer avec un casting plus varié.
- [x] Correction de `s02` avec un casting féminin différent.
- [x] Salve 04 générée : correction `s02` + slots `s30` à `s38` (10 générations).
- [x] Salve 04 validée avec la correction de `s02` et le casting varié.
- [x] Salve 05 générée : slots `s39` à `s48` (10 générations).
- [x] Salve 05 validée pour continuer.
- [x] Salve 06 générée : slots `s49` à `s58` (10 générations).
- [x] Salve 06 validée pour continuer.
- [x] Salve 07 générée : slots `s59` à `s63` + intro + endcard (7 générations).
- [x] Les 63 images de vers uniques + intro + endcard sont maintenant disponibles.
- [x] Planches contact produites pour chaque salve.
- [ ] Validation artistique finale des 65 images.
- [ ] Montage du lyric visual strictement par vers.

Le suivi exact des textes, timestamps et fichiers est dans `assets/raw/portrait/verse_index.json`.

## Package déjà produit (brouillon v1)

- [x] Source audio et paroles identifiées.
- [x] Audio mesuré : `179.328 s` (2:59.328), 48 kHz, stéréo.
- [x] Teaser 9:16 de `27.95 s` avec 5 images.
- [x] Trois covers verticales 1080×1920.
- [x] MP3 master tagué 320 kb/s avec cover intégrée.
- [x] Badge `DSKY✓` centré en haut, fixe et posé en post.
- [x] CTA like / abonnement / commentaire pendant les 2 premières secondes.
- [x] Icône de partage au milieu.
- [x] Contrôles techniques du brouillon : résolution, durée, blackdetect et freezedetect conformes.
- [ ] Remplacer le lyric visual par la version strictement par vers après les 65 images.
- [ ] Refaire le contrôle technique et visuel de la version finale.
- [ ] Commit/push de chaque salve et du rendu final.

## Nommage

- Portraits : `assets/raw/portrait/s{slot:02d}_<mot-clé>.png`.
- Source LRC nettoyée : `assets/lyrics/Toko_Longa_clean.lrc`.
- Brouillon actuel : `livrables/Toko_Longa_lyrics_9x16_v1.mp4`.
- Futur rendu conforme : `livrables/Toko_Longa_lyrics_9x16_v2.mp4`.
