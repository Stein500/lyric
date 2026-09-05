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

## Ancrage proposé — validation artistique attendue

- Source IA sans texte : `assets/ancrage/charte_A.png`.
- Maquette : `../../livrables/Je_maime_tellement_ancrage_A_9x16_v1.jpg`.
- Héroïne adulte fictive : peau brun foncé, cheveux afro naturels, blouse ivoire, jupe sombre, petites créoles dorées ; geste d'auto-étreinte, fragilité et apaisement.
- Vers de démonstration : celui de **00:30.47**, sans réécriture (espaces typographiques et retour à la ligne seulement).
- Badge ajouté en post à **(36,36)**, 332×94, contour cyan, éclair polygonal et @daiskypro ; sera posé en dernier et strictement identique sur les frames.
- Cette image est une **maquette fixe d'ancrage**, pas un clip. Le clip aura Ken Burns, vague continue et rendu frame-accurate.
- **Une image d'ancrage générée, aucune salve lancée.** Après validation : première salve portrait de 10 maximum, planche contact, validation avant la suivante.

## Reproduire

```bash
bash scripts/setup_env.sh
.venv/bin/python scripts/analyse_je_maime.py
.venv/bin/python scripts/maquette_je_maime.py
```

Les scripts sont versionnés. `.venv/`, `work/`, `.cache/` et `bin/` restent hors Git ; `livrables/` reste versionné. Les onsets vocaux, le début précis de l'endcard et les vérifications du rendu final ne doivent pas être déclarés validés sans contrôle effectif.
