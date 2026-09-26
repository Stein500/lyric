# VIVI OOR — 10 images, une seule photo

> **Clip, MP3 et covers prêts : [livraison musique complète](production/README.md).** Le montage utilise les dix portraits V2 validés et le nouveau mode d’apparition des paroles.

> **Nouvelle livraison : [V2 — les dix retouches IA](v2/README.md)**, avec une [galerie autonome, images directement intégrées](v2/VIVI_OOR_10_images_directement_ici.html), un [PDF de dix images en grand](v2/VIVI_OOR_10_images_a_feuilleter.pdf) et un [nouveau ZIP](https://raw.githubusercontent.com/Stein500/lyric/eaec1480a8a5875f30681ee270d70dcb12e335cd/vivi-oor/v2/VIVI_OOR_V2_10_images_9x16.zip). La documentation ci-dessous décrit la **V1**, conservée sans modification. Ses tests de conservation pixel ne s’appliquent pas à la V2.

**Choix validés par l’artiste le 26 septembre 2026 :** photo proposée acceptée · carte blanche pour les décors · vertical 9:16 · aucun texte.

## Livraison

- **10 PNG RGB en 1080 × 1920**, dans [`livrables/`](livrables/).
- [`VIVI_OOR_10_images_9x16.zip`](https://raw.githubusercontent.com/Stein500/lyric/d086aed69b3ea636f36768b65feb5d2accb6abe6/vivi-oor/VIVI_OOR_10_images_9x16.zip) : uniquement les dix PNG, environ 20 Mo.
- [`VIVI_OOR_apercu_10_images.jpg`](VIVI_OOR_apercu_10_images.jpg) : planche des dix résultats. Ses légendes sont à l’extérieur des vignettes ; **les images individuelles n’ont aucun texte, badge ou logo**.
- [`PROMPTS_IMAGES_VIVI_OOR.md`](PROMPTS_IMAGES_VIVI_OOR.md) : les dix prompts complets et leurs liens avec les paroles.
- [`controle_qualite.json`](controle_qualite.json) : dimensions, empreintes et contrôle de conservation du portrait.
- [`LIVRAISON_TERMUX.md`](LIVRAISON_TERMUX.md) : téléchargement reprenable au commit immuable de livraison.

**Périmètre : images seulement.** Aucun clip, cover supplémentaire ou nouveau master audio n’a été généré. Le MP3 et les paroles d’origine restent intacts. Il y a exactement dix générations de décors, pas de génération d’ancre supplémentaire. Les images peuvent servir ultérieurement au clip.

## Photo choisie

[`Samu/Snapchat-795169778.jpg`](../Samu/Snapchat-795169778.jpg) : portrait au léger sourire, regard vers l’objectif, sans lunettes, gilet gris-violet sur une tenue à manches imprimées.

Ce regard adressé au spectateur et cette expression conviennent à la proximité amoureuse de « Vivi OOR ». Le visage est dégagé ; on ne cherche ni un personnage inventé ni une apparence plus spectaculaire que celle de l’artiste.

### Protection du portrait

L’IA a généré **les décors seuls**, chaque fois avec **le même original passé en référence**. Le véritable portrait a ensuite été détouré et recomposé par programme :

- aucun visage, corps, vêtement ou changement de pose généré ;
- aucune correction esthétique, modification de corpulence, de teinte ou d’expression ;
- aucun débruitage, lissage de peau ou « super-résolution » générative ;
- même cadrage et mêmes proportions dans les dix compositions ;
- retrait du mur et des trois cœurs Snapchat, qui appartenaient au fond ;
- un seul agrandissement uniforme **720 × 1280 → 1080 × 1920** (Lanczos) ;
- léger fondu de contour de détourage ; l’intérieur opaque du portrait est **identique pixel par pixel** à l’original ainsi redimensionné, vérifié sur les dix PNG.

La douceur, le grain et la dominante chaude déjà présents sur la photo source sont volontairement conservés : il ne s’agit pas d’inventer des détails de visage absents de la photo. L’agrandissement ne transforme pas la source en une prise de vue native haute résolution.

## Lecture du morceau

Sources consultées : [`Vivi O O R.txt`](../Vivi%20O%20O%20R.txt), [`VIVI OOR.mp3`](../VIVI%20OOR.mp3), prompts v5.1.1, v5.2 et v5.3 **avec priorité à l’addendum v5.3.1**. La consigne actuelle « 10 images seulement » remplace la règle ancienne « une image par vers ». Pour une éventuelle vidéo ultérieure, les paroles devront rester hors visage conformément à l’addendum.

Le texte associe trois mouvements :

1. **Douceur et désir amoureux**, avec le miel, les baisers et les étincelles. Traduction : ambre, verre doré, petites lumières et textures douces, sans illustration littérale excessive.
2. **Attachement et vulnérabilité**, avec « reste avec moi », « je t’attends », « je t’ouvre mon cœur ». Traduction : véranda calme, portes ouvertes, jardin accueillant.
3. **Joie de vivre partagée**, avec les instants savourés, le trésor, le festin et la danse jusqu’au matin. Traduction : lagune, lumière précieuse, dîner, terrasse de danse puis aube.

La direction S2 « Golden Sunset » évolue vers une nuit ambre/indigo et revient à une aube crème/lavande. Il ne s’agit pas d’un univers guerrier ou sombre. Les décors sont des créations, pas des photographies de lieux réellement visités par l’artiste.

### Repères des dix images

| N° | Image | Référence aux paroles | Décor |
|---|---|---|---|
| 01 | Invitation dorée | 00:21.13 — « aime-moi » | Terrasse, arche et couchant |
| 02 | Le goût du miel | 00:52.71 — « ta bouche a le goût du miel » | Verrière ambrée et jasmin |
| 03 | Les étincelles | 00:56.07 — « chaque baiser est une étincelle » | Jardin et guirlandes lumineuses |
| 04 | Reste avec moi | 00:47.10 — « reste avec moi » | Véranda et rideaux de lin |
| 05 | Chaque instant | 00:35.59 — « je savoure chaque instant avec toi » | Lagune calme |
| 06 | Le cœur ouvert | 01:39.85 — « je t’ouvre mon cœur » | Portes ouvertes sur un jardin |
| 07 | Notre trésor | 02:10.71 — « notre amour est un trésor » | Alcôve prune et lanterne dorée |
| 08 | Le festin | 01:53.38 — « la vie est un festin » | Dîner sous des suspensions chaudes |
| 09 | Jusqu’au matin | 02:13.89 — « dansons jusqu’au matin » | Terrasse nocturne, lune et lumières |
| 10 | L’aube douce | 02:32.68 — « je savoure chaque instant avec toi » | Terrasse sur l’eau au petit matin |

Les numéros suivent un parcours visuel, **pas un montage chronologique validé**. Les repères sont ceux des paroles fournies, non des timestamps réalignés à la voix.

### Vérification audio préliminaire (source non modifiée)

- Décodage mesuré : **204,96 s** (3 min 24,96 s), source 48 kHz stéréo.
- Paroles : **44 entrées horodatées, 30 textes uniques** ; temps croissants.
- Analyse loudnorm initiale : −14,71 LUFS intégrés, crête vraie +0,51 dBTP, LRA 5,50 LU. Ce sont des mesures, **pas un master normalisé livré**.
- Le tempo automatique présentait plusieurs candidats ; aucun BPM définitif ni alignement mot-à-mot n’est revendiqué ici.

## Reproduction technique

Les décors originaux, le masque et le catalogue des prompts sont versionnés. Les modèles, environnements Python et essais de détourage ne sont pas publiés.

Depuis la racine du dépôt :

```bash
python3 -m venv .venv
.venv/bin/pip install -r vivi-oor/requirements.txt
.venv/bin/python vivi-oor/scripts/compose.py
```

Le script recompose les dix PNG, exécute les assertions de fidélité, crée la planche et vérifie que le ZIP contient exactement dix fichiers.

- `scripts/prepare_manifest.py` : brief, manifeste et prompts complets rédigés avant génération.
- `scripts/build_matte.py` : détourage par trimap manuelle + GrabCut, **sans génération RGB**. Reconstruction facultative du masque ; nécessite `opencv-python-headless==5.0.0.93`. Le masque final est déjà fourni.
- `scripts/compose.py` : aucun appel IA ; recomposition reproductible avec Pillow/NumPy. Le léger flou de profondeur de champ s’applique **au décor seulement**.

Le fichier universel v5.3 reste inchangé à la racine ; cette fiche constitue le brief spécifique à cette livraison de dix images.
