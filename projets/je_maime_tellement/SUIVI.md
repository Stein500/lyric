# Je m'aime tellement — 9:16 + MP3 livrés, validation utilisateur attendue

## Instruction actuelle de l’utilisateur

Après la troisième salve, **arrêter à 30 fonds**, autoriser les réutilisations et **enchaîner directement sur le 9:16 complet et le MP3 propre**. L’utilisateur télécharge, vérifie puis valide. Ne pas lancer le 16:9, une autre salve ou le morceau Drague moi avant une nouvelle demande.

## Livrables

- `../../livrables/Je_maime_tellement_9x16_v1.mp4` — 1080×1920, 30 fps, H.264, AAC 192 kb/s, **198,166667 s**, environ 69,8 Mo.
- `../../livrables/Je_maime_tellement_master_v1.mp3` — 320 kb/s, 48 kHz stéréo, **193,159979 s**, environ 8,0 Mo.
- `../../livrables/cover_Je_maime_tellement_1080.jpg` — cover intégrée au MP3, dérivée d’un fond existant, aucune génération supplémentaire.
- `../../livrables/Je_maime_tellement_v1_infos.md` — informations et contrôles lisibles.
- `livraison_v1.json` — tailles, durées, empreintes et statut de la livraison.

## Décisions qui font foi

- Référence : `PROMPT_UNIVERSEL_v4.7.md`, avec les dérogations **propres à ce morceau** consignées dans `cadrage.json`.
- **Paroles fournies par l’utilisateur**, y compris « si belle,si dure,si lui » ; ne jamais leur substituer l’ancien USLT embarqué dans le MP3 source.
- **Aucune avance : 0,00 s.** À 30 fps, la première frame d’un vers est le plafond du timestamp × 30 ; jamais d’anticipation, quantification < 1 frame.
- Artiste **Daïsky Pro**, album **Success**, label **Daïsky Prod / TechStein**. Genre Rap et année 2026 repris de la source.
- Charte **A** dorée, cinéma et animé, même héroïne adulte noire, afro naturel, créoles dorées, blouse ivoire et jupe longue sombre, silhouette généreuse.
- Salves 01 et 02 validées ; salve 03 sélectionnée puis rendue **sans nouvelle pause artistique**, comme demandé.
- **30 fonds de scène** : 15 cinéma et 15 animé. Aucun nouvel appel de génération après S29. Les 20 vers restants et l’endcard réutilisent les fonds selon `montage_v1.json`.
- Le 16:9 et les autres publications sont différés jusqu’au contrôle utilisateur.

## Sources préservées

Les deux MP3/LRC de Je m’aime tellement et Drague moi ont été récupérés depuis le commit utilisateur `45d4b52`, sans changer de branche. Aucun traitement de Drague moi n’a été effectué.

- Source musicale : `Je m'aime tellement - Daïsky.mp3` ; décodage 48 kHz stéréo, **9 271 679 échantillons par canal**.
- Source LRC conservée intacte. `paroles_utf8.lrc` rétablit l’UTF-8 et les deux `cSur` → `cœur` conformément au texte de la conversation ; aucun autre mot ni timestamp modifié.
- 49 lignes vocales et une indication INTRO. Les annotations de jeu vocal ne sont pas affichées comme paroles.
- Empreintes et analyse initiale : `analyse_audio.json`.

## Rendu continu et contrôles

- **5 945 frames** sur un flux MJPEG continu vers libx264 ; aucune concaténation de clips. Chaque frame i correspond à t=i/30.
- Fonds LANCZOS sur canvas 1188×2112 puis Ken Burns affine fractionnel OpenCV, zoom 1,02–1,08, pan lent.
- Lettres : apparition décalée, vague sinusoïdale continue 6 px / 0,9 Hz, disparition en cascade inversée. Entrées et sorties adaptées aux fenêtres brèves, sans les déplacer.
- Badge exact de la maquette, **(36,36)**, 332×94, posé en dernier et jamais déplacé.
- Endcard à **189,50 s**, sur le fondu audio détecté ; contacts complets, environ 5 s de padding, fondu final de 3 s. Pas de fondu d’entrée vidéo.
- Vidéo : crf19, veryfast, yuv420p, plafond VBV 3500k / tampon 7000k, AAC 192k, faststart.
- **Contrôles passés**, consignés dans `controle_video_v1.json` : streams/durée/frames, faststart, blackdetect limité au fondu final, aucun freezedetect au seuil −70 dB / 1 s, 16 comparaisons de frames (dont après 2:00), badge et mouvement, corrélation source/master.
- `controle_master_v1.json` : MP3 **−13,93 LUFS / −1,70 dBTP**, durée identique à l’échantillon près, tags complets, cover carrée, paroles utilisateur. La provenance/commentaires et numéros de piste de l’original ont été conservés.
- Loudnorm a utilisé son **mode dynamique réel** en passe 2 pour respecter le plafond TP de cette source ; ne pas présenter ce master comme une normalisation exclusivement linéaire.
- Audio AAC du MP4 : **−14,00 LUFS / −1,04 dBTP**, sans clipping.

**Limite honnête :** les contrôles établissent le respect de la timeline fournie et l’absence de décalage introduit par le mastering. Ils ne remplacent pas l’écoute ni la validation artistique de l’utilisateur. Le modèle de transcription n’a pas pu être téléchargé ; aucune transcription automatique n’a été substituée au texte.

## Archivage sans perte des fonds

Pour que le patch courant conserve surtout les livrables complets sans dépasser son budget de persistance, les **30 bruts PNG (67,7 Mo) sont archivés intégralement dans le commit distant `70c07ac60a79d56915357371d897bbe34f3b78e0`** et retirés de l’arbre courant. Ils ne sont pas perdus ni remplacés par des vignettes.

- Index, tailles et SHA-256 : `archive_visuels.json`.
- La sauvegarde distante a été vérifiée **avant** de retirer les fichiers ; restauration et empreinte des 30 bruts testées ensuite.
- `resolve_asset()` restaure automatiquement les sources nécessaires dans `work/out/je_maime_tellement/restored_assets/`. En cas d’historique partiel, il fetch uniquement la branche de session, sans checkout ni reset.
- Pour obtenir tous les chemins physiques des bruts : `.venv/bin/python scripts/archive_je_maime_assets.py --restore`.
- Les chemins `source_image` et `generation_references` des manifestes restent leurs chemins **logiques** ; les outils d’images doivent utiliser les chemins de cache restaurés si ces bruts sont requis.
- Ancrage, référence animé préparée, polices, planches contact et livrables restent directement dans l’arbre courant.
- Le seul dérivé de préparation est S01 : prolongement de son propre ciel sur une marge supérieure ; tous les pixels à partir de la ligne 190, dont le personnage, sont conservés. Le brut d’origine est dans l’archive.

## Reproduire

```bash
bash scripts/setup_env.sh
.venv/bin/python scripts/archive_je_maime_assets.py --restore  # facultatif : restauration à la demande sinon
.venv/bin/python scripts/master_je_maime.py
.venv/bin/python scripts/prepare_montage_je_maime.py
.venv/bin/python scripts/render_je_maime.py
.venv/bin/python scripts/verify_je_maime.py
```

Les trois planches se reconstruisent avec `scripts/planche_je_maime.py` et le manifeste `salves/portrait_0N.json`. Le dossier `work/out/` est temporaire ; ne pas y compter sur des livrables persistants. `.venv/`, `work/`, `.cache/`, `bin/` et les caches Python sont hors Git ; **`livrables/` reste versionné**. Ne jamais committer ffmpeg ou l’environnement Python.
