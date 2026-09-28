# Ancre et maquette — contrôle du 2026-09-28

**État : attente de validation de l’artiste. Ce n’est pas le clip final.**

## Fichiers

- `livrables/Concentre_sur_le_chemin_maquette_9x16_v1.mp4` — 4,553,267 octets, 1080×1920, **435 frames / 30 fps / 14,500 s**, H.264 yuv420p progressif, audio AAC stéréo 48 kHz (≈195 kb/s mesuré).
- `livrables/Concentre_sur_le_chemin_ancre_9x16_v1.jpg` — image d’approbation avec un vrai vers complet, badge et bandeau ; PNG de contrôle sans perte également livré.
- `assets/raw/concentre_sur_le_chemin/portrait/s01_tete_lourde.png` — **seule génération IA de cette étape**, 768×1376, sans lettrage ni badge/drapeau généré. Références originales autorisées du dossier Samu jointes à l’appel.
- `assets/composed/concentre_sur_le_chemin/portrait/s01_tete_lourde.png` — 1080×1920, fond recadré avec bandeau, sans badge permanent. Le rendu vidéo utilise volontairement le brut et ajoute les overlays après le mouvement pour éviter les doublons.

## Réalisé et vérifié

- Caractères gras Barlow Condensed Bold, 104–112 px suivant le vers, retour à la ligne avant réduction ; tous les 58 textes testés sans suppression de mots. Bloc centré à (540, 960), chaque ligne centrée, largeur maximale 720 px, bord droit 900 < rail 910, aucun texte sous y=1574.
- Lecture effective de la maquette réduite à **360×640** : badge « Dsky » lisible, pictogramme drapeau distinct, vrais vers complets visibles ; texte hors du visage.
- Apparition mot à mot et vague simultanées, avec les positions du vers complet précalculées. Mot actif crème/or, passé atténué. La vague n’anime pas le badge.
- Badge unique, séparé du fond : fondus de **0,4 s**, plafond **75 %** ; quasi nul aux frontières de chaque vers selon l’échantillonnage à 30 fps. Absence de badge au tout début et après la dernière fenêtre de cette maquette.
- Bandeau de **54 px** (y=1866→1920) : vert x<360, jaune et rouge sur les 720 px droits. PNG : pixels exacts (0,135,81), (252,209,22), (232,17,45). MP4, sur les 14 frames contrôlées : (0,134,79), (252,208,21), (229,15,44), écarts de compression ≤3 par canal.
- Aucun intervalle noir détecté au seuil 98 % de pixels sombres / seuil pixel 0,04 / durée minimale 0,1 s. Aucun gel ≥1 s détecté au seuil −60 dB. Mouvement continu du fond et des glyphes présents.
- **14 frames MP4** comparées à leur reconstruction aux mêmes indices, dont les frontières de vers : erreur absolue moyenne RGB de **1.8836 à 2.2246 niveaux/255**. C’est une mesure d’écart colorimétrique moyen, pas une revendication de décalage spatial en pixels.
- **20 tests automatisés réussis** : parsing, encodage, texte inchangé, timings structurels, retours à la ligne, centrage, safe zones, présence des glyphes, vague, fondus de badge, géométrie/pixels du drapeau.

Le cadrage de l’ancre a été relevé de 120 px en retirant du plafond vide ; prolongement non génératif des huit dernières lignes du sol vide en bas. Aucun étirement du visage/corps, aucune seconde génération. Pieds et mains restent cadrés.

## Encore à approuver / non réalisé

- **Ressemblance et choix des lunettes**, pose, rendu des habits, style et taille des paroles : validation artiste obligatoire. Les références montrent très peu de pilosité ; vérifier notamment que le traitement ombré du menton de l’ancre convient, sans le déclarer identique aux photos.
- Audio source de **01:53.00 à 02:07.50** ; simple gain −1,6 dB pour la maquette. Ce n’est pas le master normalisé deux passes de la chanson entière.
- Départs de vers issus de la source avec avance de 0,03 s. **Temps de mots provisoires**, répartis selon leur longueur, pas d’alignement vocal forcé validé. La fin du cinquième vers est provisoire ; les trois passages de validation de la chanson entière restent à contrôler.
- Seulement **1 fond généré sur les 10 prévus**. Les 4 autres portraits, les 5 paysages, les clips complets, le master et les covers n’existent pas encore ; attendre l’accord sur l’ancre.

## Reproduire

```sh
bash scripts/setup_env.sh
/tmp/lyric-venv/bin/python scripts/analyse_chanson.py --audio 'Concentré sur le chemin.mp3' --lyrics 'concentré sur le chemin.txt' --title 'Concentré sur le chemin' --output work/concentre_sur_le_chemin
/tmp/lyric-venv/bin/python scripts/render_ancre.py
/tmp/lyric-venv/bin/python scripts/check_maquette.py
/tmp/lyric-venv/bin/python -m unittest discover -s tests -v
```

Les détails frame par frame et logs FFmpeg se régénèrent sous `work/concentre_sur_le_chemin/`.
