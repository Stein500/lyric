# Vivi OOR — MP4 lyrics, MP3 et covers

Livraison à la demande de l’artiste : clip **MP4**, master **MP3**, covers et paroles, avec une apparition améliorée selon le dernier prompt.

## Fichiers prêts

| Livrable | Fichier | Format |
|---|---|---|
| **Clip lyrics** | [VIVI_OOR_lyrics_9x16.mp4](livrables/VIVI_OOR_lyrics_9x16.mp4) | 1080 × 1920, 30 fps, H.264 / AAC, environ 44,5 Mo |
| **MP3 final** | [VIVI_OOR_master_320k.mp3](livrables/VIVI_OOR_master_320k.mp3) | 320 kb/s, 48 kHz stéréo, environ 8,5 Mo |
| Cover universelle | [cover_vivi_oor_universelle_3000.jpg](livrables/cover_vivi_oor_universelle_3000.jpg) | 3000 × 3000 |
| Cover audio / APIC | [cover_vivi_oor_1080x1080.jpg](livrables/cover_vivi_oor_1080x1080.jpg) | 1080 × 1080, également intégrée au MP3 |
| Cover verticale | [cover_vivi_oor_9x16.jpg](livrables/cover_vivi_oor_9x16.jpg) | 1080 × 1920 |
| Cover horizontale | [cover_vivi_oor_16x9.jpg](livrables/cover_vivi_oor_16x9.jpg) | 1920 × 1080 |
| Portrait alternatif | [cover_vivi_oor_portrait_alternative_1080.jpg](livrables/cover_vivi_oor_portrait_alternative_1080.jpg) | 1080 × 1080, portrait V2 déjà validé |
| Paroles synchronisées chanson | [Vivi_OOR.lrc](livrables/Vivi_OOR.lrc) · [SRT chanson](livrables/Vivi_OOR_chanson.srt) | Timecodes du fichier fourni |
| Sous-titres vidéo | [Vivi_OOR_clip.srt](livrables/Vivi_OOR_clip.srt) | Hook et décalage vidéo inclus |
| Animation modifiable | [VIVI_OOR_lyrics_mot_a_mot.ass](livrables/VIVI_OOR_lyrics_mot_a_mot.ass) | Texte, positions, tailles, fondus et transitions |
| Paroles propres | [Vivi_OOR_paroles.txt](livrables/Vivi_OOR_paroles.txt) | UTF-8, accents conservés |
| Prompt à jour | [PROMPT_UNIVERSEL_v5.3.2.md](livrables/PROMPT_UNIVERSEL_v5.3.2.md) | Hérite v5.3 et v5.3.1 |
| Caption | [CAPTION_VIVI_OOR.txt](livrables/CAPTION_VIVI_OOR.txt) | Légende + quatre hashtags |

Les commandes de téléchargement au commit immuable de livraison figurent dans **[LIVRAISON_TERMUX.md](LIVRAISON_TERMUX.md)**.

## Affichage des paroles

Mode retenu après la demande « en améliorant l’apparition des paroles du dernier prompt » : **mot grand puis petit**.

- Le mot actif apparaît progressivement, avec un agrandissement modéré ×1,45 → ×1,20, en crème/or et halo discret.
- Il rejoint ensuite sa place dans une traînée de mots plus petits. Les positions du vers complet sont calculées avant apparition : les anciens mots ne sautent pas horizontalement.
- Deux lignes maximum dans la traînée, longueurs contrôlées, accents et mots complets conservés.
- Paroles sur le gilet : mot actif autour de y1228, traînée autour de y1400/y1460, hors visage et au-dessus de la caption TikTok. La limite droite reste avant le rail des boutons.
- Scrim dégradé bas uniquement quand un vers est affiché. Badge DSKY✓ compact, opacité environ 69 %, fondus de 0,4 s avec chaque vers, pas de badge permanent.
- Zooms et déplacements légers sur les dix images V2, fondus entre décors. Aucun nouveau visage ni nouvelle image générée pour le clip.
- Fin simple : titre, WhatsApp, email et badge, sans longue liste de crédits.

**Précision de synchronisation :** les 44 débuts de vers reprennent les timecodes fournis par l’artiste. L’animation par mot est **estimée** à partir des syllabes, des phrases répétées et de points d’attaque musicaux, avec ajustement borné. Ce n’est pas un alignement vocal forcé ni une validation à l’écoute mot par mot. Un modèle ASR n’était pas accessible sur le réseau ; aucune précision vocale non mesurée n’est revendiquée. Les fichiers LRC/SRT/ASS restent livrés pour permettre des corrections fines.

## Durées

- Chanson et MP3 : **204,96 s**, soit **3 min 24,96 s**, sans hook ni silence ajouté.
- Clip : **6479 images / 30 fps = 215,9667 s**, soit environ **3 min 36 s**.
- Différence volontaire : hook de **6 s**, pris à **02:32.43 → 02:38.43** du morceau, puis chanson entière et **5 s** de fin. Une seule horloge vidéo ; pas de concaténation de clips.

## Audio et provenance

- Traitement doux selon le prompt : passe-haut 30 Hz, passe-bas 18 kHz, normalisation loudnorm en deux passes, ajustement de gain constant.
- **MP3 mesuré : −14,00 LUFS, crête vraie −1,72 dBTP.** Durée décodée exacte 204,96 s ; 320 kb/s, 48 kHz, deux canaux.
- Clip : AAC 192 kb/s, 48 kHz stéréo. Une marge supplémentaire a été appliquée après contrôle des crêtes du codec : **−15,23 LUFS et −2,02 dBTP** sur la livraison. Le MP3 reste à −14 LUFS.
- Pochette APIC, paroles USLT et paroles synchronisées par vers SYLT dans le MP3 ; artiste, titre, album, contacts et année renseignés.
- L’original `VIVI OOR.mp3` n’a pas été modifié. Son indication de provenance Suno, son URL et son manifeste source sont conservés comme provenance ; le manifeste source n’est **pas présenté comme une signature valide de l’export réencodé**.
- Pas de compositeur non confirmé inventé. Le genre « Afro-pop » est un choix de classement éditorial. Un export 320 kb/s n’invente pas des détails absents du MP3 source d’environ 184 kb/s.

## Covers

Les covers officielles utilisent un décor S2 déjà généré, avec **Vivi OOR**, **Daïsky**, DSKY✓ et bande Bénin ajoutés proprement en postproduction. Aucun visage supplémentaire n’a été généré. L’alternative portrait réutilise la V2 n°03. Le format 3000 × 3000 est une composition typographique dans cette taille, avec un décor source redimensionné, pas une promesse de photographie native 3000 pixels.

## Vérifications livrées

- [`metadata/video_quality.json`](metadata/video_quality.json) : 6479 images décodées, résolution/fréquence conformes, conteneur faststart, taille, hash et contrôles vidéo.
- Aucun arrêt détecté sur une durée ≥1,5 s avec seuil −80 dB. Noir seulement de 215,27 s à 215,93 s, dans le fondu final prévu.
- [`metadata/controle_visuel_clip.jpg`](metadata/controle_visuel_clip.jpg) : douze captures du fichier final, notamment hook, mots, reprises, outro et contacts.
- [`metadata/mp3_quality.json`](metadata/mp3_quality.json) : tags, pochette, durée audio décodée, niveau et crêtes après encodage.
- Corrélation de la forme d’onde avant/après traitement à 5, 45, 95, 154 et 176 s : décalage mesuré nul à 16 kHz.
- Le contrôle des positions du texte est géométrique ; il ne constitue pas une reconnaissance de la voix.

## Reproduction

Depuis la racine du dépôt, Python 3.11 :

```bash
python3 -m venv .venv
.venv/bin/pip install -r vivi-oor/production/requirements.txt
.venv/bin/python vivi-oor/production/scripts/prepare_audio.py
.venv/bin/python vivi-oor/production/scripts/covers.py
.venv/bin/python vivi-oor/production/scripts/master_mp3.py
.venv/bin/python vivi-oor/production/scripts/timeline.py
.venv/bin/python vivi-oor/production/scripts/render.py
.venv/bin/python vivi-oor/production/scripts/verify_video.py
```

Les polices sont versionnées avec leurs licences. FFmpeg vient de la wheel `imageio-ffmpeg`, sans binaire ajouté au dépôt. Les WAV et rendus de contrôle temporaires se reconstruisent dans `work/`, ignoré par Git. Le moteur OpenCV accélère les mouvements des fonds ; le texte ASS est rendu dans le flux vidéo unique.

Les anciens ZIP des images dupliquaient les PNG. Pour laisser la place au clip complet, **ces ZIP restent disponibles à leurs commits immuables vérifiés**, tandis que les PNG, photos et présentations sont conservés dans l’arbre courant : voir [ARCHIVES_IMAGES.md](../ARCHIVES_IMAGES.md).
