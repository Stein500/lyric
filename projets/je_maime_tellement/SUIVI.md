# Je m'aime tellement — suivi de production

## Décisions confirmées

- Priorité exclusive à **Je m'aime tellement** ; **Drague moi 1** attend.
- **Les paroles données par l'utilisateur font foi**, y compris « si belle,si dure,si lui ». Ne pas les remplacer par les paroles embarquées dans le MP3.
- **Aucune avance : 0,00 s.** Tous les timestamps fournis sont conservés. À 30 fps, première frame à ou après le timestamp (quantification < 1 frame, aucune anticipation).
- Artiste **Daïsky Pro**, album **Success**, label **Daïsky Prod / TechStein**.
- Charte **A**, héroïne fictive IA, amour de soi, lumière dorée et grain cinéma.
- Pack complet, 9:16 avant 16:9, MP3 master/tagué, covers et endcard v4.7.

## Sources et contrôle technique

Les quatre fichiers MP3/LRC des deux titres ont été récupérés depuis le commit utilisateur `45d4b52`, sans quitter `arena/01a072d8-lyric`. Aucun traitement de Drague moi n'a été effectué.

- Audio de Je m'aime tellement décodé **sans avertissement** : **193,159979 s**, 48 kHz, stéréo, 9 271 679 échantillons par canal.
- Source : **−13,34 LUFS**, **−0,86 dBTP**, LRA **5,20 LU**. Il ne s'agit pas encore d'un master.
- Tempo automatique estimé autour de **70 BPM**, ou **140** en double tempo ; ne sert pas à recaler les paroles.
- **49 entrées vocales** et une indication INTRO : **51 images par format**, intro et endcard comprises. Refrains/tags répétés : images distinctes, pas de réutilisation.
- Copie de production UTF-8 dans `paroles_utf8.lrc` ; les deux `cSur` du fichier reçu deviennent `cœur`, conformément au texte donné en conversation. Aucun autre mot ni timestamp modifié. Les deux fichiers source restent intacts (SHA-256 dans `analyse_audio.json`).
- Limite honnête : audit technique réalisé, pas de certification indépendante des onsets chantés à ±0,35 s. Le téléchargement du modèle de transcription n'était pas accessible ; aucune transcription n'a été substituée au texte de l'utilisateur.

## Ancrage validé — évolution demandée par l’utilisateur

- Source IA sans texte : `assets/ancrage/charte_A.png`.
- Maquette : `../../livrables/Je_maime_tellement_ancrage_A_9x16_v1.jpg`.
- Héroïne adulte fictive : peau brun foncé, cheveux afro naturels, blouse ivoire, jupe sombre, petites créoles dorées ; geste d'auto-étreinte, fragilité et apaisement.
- Validation reçue : « Oui continue... ajoute des images style animé..forme généreuse aussi ». Même identité et palette A, ajout d’images animé et silhouette plus généreuse.
- Vers de démonstration : celui de **00:30.47**, sans réécriture (espaces typographiques et retour à la ligne seulement).
- Badge ajouté en post à **(36,36)**, 332×94, contour cyan, éclair polygonal et @daiskypro ; sera posé en dernier et strictement identique sur les frames.
- Cette image est une **maquette fixe d'ancrage**, pas un clip. Le clip aura Ken Burns, vague continue et rendu frame-accurate.
- L’ancrage initial est validé ; ne pas redemander cette validation. La première salve ci-dessous intègre les changements demandés.

## Salve portrait 01 — validée

- **10 nouvelles sources IA distinctes**, slots **S00 à S09** : intro et neuf premières lignes vocales. Période : 00:00.00 → 00:48.01 (fin exclue).
- **5 cinéma + 5 animé**. Même héroïne adulte, tenue et palette dorée, avec une silhouette généreuse ; progression vers des métaphores de résistance, soleil intérieur et doutes nocturnes.
- Planche : `../../livrables/Je_maime_tellement_planche_01_9x16_v1.jpg`.
- Aperçu animé avec le vers de **00:32.54** : `../../livrables/Je_maime_tellement_apercu_anime_9x16_v1.jpg`. Aperçu fixe de composition, pas un clip animé.
- Manifeste : `salves/portrait_01.json` (vers exacts, timestamps, styles, chemins, références, SHA-256 et statut de validation).
- Sources sans typographie : `assets/raw/portrait/s00…s09_*.png`. Dix fichiers et dix empreintes distinctes vérifiés ; fichiers audio/LRC d’origine inchangés.
- S01 avait une marge supérieure rectangulaire produite par le modèle. Un **dérivé séparé** dans `assets/prepared/portrait/` la remplace par un prolongement de son propre ciel ; le personnage et tous les pixels à partir de la ligne 190 sont préservés. Le brut reste intact. Aucun nouvel appel IA pour cette préparation.
- Référence animé pour la suite : le dérivé préparé S01 ; référence cinéma : l’ancrage original. Corps, coiffure, peau, tenue et visage doivent rester cohérents.
- **10 générations dans la salve 01.** Règle des 10 maximum par session respectée.
- **Validée par l’utilisateur : « On continue ».** Les slots S00 à S09 sont approuvés ; aucune de leurs images sources n’a été modifiée.
- Suite engagée après validation : **salve 02, S10 à S19**.

## Salve portrait 02 — en attente de validation artistique

- Autorisation : **« On continue »**, après présentation de la planche 01.
- **10 nouvelles sources IA distinctes**, **S10 à S19**, de **00:48.01 à 01:11.29** (fin exclue).
- **5 cinéma + 5 animé**, avec la même héroïne adulte, silhouette généreuse, afro naturel, blouse ivoire, jupe sombre et palette dorée.
- Arc visuel : reflet douloureux → pensées qui tournent → quête d’approbation → matin neuf → pouvoir intérieur → cicatrices/victoires → larmes qui portent → mouvement → apprentissage → valeur de soi.
- Les cicatrices sont illustrées par les veines dorées d’un bol réparé, sans blessure corporelle.
- Planche : `../../livrables/Je_maime_tellement_planche_02_9x16_v1.jpg`.
- Aperçu animé avec le vers de **00:56.35** : `../../livrables/Je_maime_tellement_apercu_anime_salve_02_9x16_v1.jpg`. Maquette fixe, pas encore un clip.
- Manifeste : `salves/portrait_02.json`. Sources sans texte : `assets/raw/portrait/s10…s19_*.png`.
- Contrôles : **20 empreintes distinctes** sur les deux salves, dimensions des images, sources audio/LRC intactes, texte et timestamps identiques, première frame jamais anticipée, planche et aperçu inspectés. Aucun traitement du morceau Drague moi.
- **20 / 51 fonds portrait générés ; 31 restent à produire.** Le format paysage reste à faire séparément.
- **10 générations dans cette salve/session ; pas de deuxième salve dans le même tour.**
- **Attendre la validation de la planche 02.** Prochaine salve : **S20 à S29**. Ne reprendre que les slots refusés si l’artiste demande des retouches.

## Reproduire

```bash
bash scripts/setup_env.sh
.venv/bin/python scripts/analyse_je_maime.py
.venv/bin/python scripts/maquette_je_maime.py
.venv/bin/python scripts/planche_je_maime.py projets/je_maime_tellement/salves/portrait_01.json
.venv/bin/python scripts/planche_je_maime.py projets/je_maime_tellement/salves/portrait_02.json
```

Les scripts sont versionnés. `.venv/`, `work/`, `.cache/` et `bin/` restent hors Git ; `livrables/` reste versionné. Les onsets vocaux, le début précis de l'endcard et les vérifications du rendu final ne doivent pas être déclarés validés sans contrôle effectif.
