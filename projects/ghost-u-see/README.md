# Ghost u see — clip vertical 9:16

Refonte du clip de Daïsky à partir du master audio fourni. La direction artistique associe une animation expressive de long métrage et une lumière inspirée de l’anime, avec des personnages noirs dans des environnements urbains modernes et une progression émotionnelle allant de la blessure à la liberté retrouvée.

## Mode paroles

- Chaque ligne chantée possède son illustration générée individuellement, avec le texte original intégré à l’image.
- Les traductions françaises des lignes anglaises et espagnoles apparaissent en pilule karaoké; les lignes françaises restent sans traduction.
- Le renderer n’imprime pas une seconde fois les paroles originales au-dessus des illustrations.

## Livrables

- `../../livrables/GHOST-U-SEE-DAISKY-9x16.mp4` — 1080 × 1920, 30 i/s, environ 4 min 10, master audio original normalisé pour diffusion, transitions courtes et carte de fin.
- `../../livrables/COVER-GHOST-U-SEE-1080x1920.jpg` — couverture verticale.
- `../../livrables/PUBLICATION-GHOST-U-SEE.md` — titre, légende, 13 hashtags, déclaration IA et commandes Termux.
- `verses_map.json` — 47 repères temporels, textes, traductions et chemin d’image par ligne chantée.
- `assets/generated-lyrics/` — 44 illustrations de paroles en 9:16; le mapping suit les identifiants des cues, certains noms historiques `verseNN` ne correspondant pas directement au numéro du cue.
- `assets/` — images d’ambiance utilisées pour les sections instrumentales, police gothique et licence.

## Reconstruction

Dépendances Python : `Pillow`, `mutagen`, `imageio-ffmpeg`. La roue `imageio-ffmpeg` fournit FFmpeg avec H.264, libass et loudnorm.

```sh
python3 -m venv .venv
.venv/bin/pip install pillow mutagen imageio-ffmpeg
.venv/bin/python projects/ghost-u-see/build_map.py
.venv/bin/python projects/ghost-u-see/render.py
```

Le renderer construit une plaque mobile avec fond adouci afin de préserver les paroles intégrées près des bords, anime 44 images de vers et conserve le master audio fourni (normalisation deux passes à −14 LUFS / −1,5 dBTP cible). Il ne génère ni ne remplace la voix ou la musique.

La police UnifrakturCook est distribuée sous SIL Open Font License; voir `assets/OFL.txt`.
