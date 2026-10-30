# Salve 02 — correction + scènes 12 à 19

## Bilan réel

- **Demandées** : 10 images (scènes 06, 10, 12–19)
- **Générées** : 10 images
- **QC visuel/typo accepté par l’agent** : 7 images — scènes 06, 12, 14, 15, 17, 18 et 19
- **Échecs consignés** : 3 images — scènes 10, 13 et 16
- **Taille des images** : 768 × 1376 px
- **Contact sheet** : `CONTROLE-salve02.jpg`, 2 colonnes × 5 rangées; chaque tuile fait 500 × 896 px
- **Contrôle typo 1:1** : `CONTROLE-salve02-typo.jpg`, grille de 16 px
- **Retouche de lettres** : aucune
- **Validation par l’artiste** : en attente pour cette salve; seule l’ancre est validée par l’artiste.

## Contrôle par scène

| Scène | Vers source | État QC | Note |
|---:|---|---|---|
| 06 | `Wolof TechStein beat wê!` | QC accepté — correction de la salve 01 | Cette version ne contient que la signature demandée; l’ancienne version avec paragraphe anglais reste rejetée. |
| 10 | `J'ai vu des promesses s'envoler comme des abeilles` | **Échec — à régénérer** | La lumière bleue nocturne est cohérente, mais le modèle a ajouté un point après `abeilles`; le vers source n’a pas ce point. Version écartée dans `fonds/rejected/scene-10-v2-extra-period.png`. |
| 12 | `J'ai gardé le feu qui brûle dans mon âme` | QC accepté | `âme` et le texte relus. |
| 13 | `On m'a dit "t'es trop petit, t'es trop lent, t'es trop différent"` | **Échec — à régénérer** | Le vers était explicitement fourni dans le prompt, mais le modèle a ajouté une paire de guillemets autour de la ligne entière en plus des guillemets intérieurs présents dans la source. Version écartée dans `fonds/rejected/scene-13-v1-extra-quote-marks.png`. |
| 14 | `Mais j'ai transformé leurs insultes en sang, en talent` | QC accepté | Métaphore stylisée sans gore; texte relu. |
| 15 | `Maintenant je suis debout, j'ai des cicatrices sur le cœur` | QC accepté | Apostrophes, accents et `cœur` relus. |
| 16 | `Chaque larme versée est devenue une œuvre` | **Échec — à régénérer** | Texte relu, mais l’image introduit un lever de soleil trop tôt (50,70 s, avant le pont). Version écartée dans `fonds/rejected/scene-16-v1-premature-dawn.png`. |
| 17 | `Ils ont voulu ma fin, ils ont voulu ma chute` | QC accepté | Texte relu; pluie et vent symboliques, sans attaquants. |
| 18 | `Mais je suis un roc, je résiste, je lutte` | QC accepté | Texte relu; palette nocturne. |
| 19 | `Je tombe, je me relève` | QC accepté | Texte relu; pose de relèvement. |

## Règle d’affichage appliquée

Chaque mot destiné à apparaître dans une image est écrit explicitement dans le prompt de cette image. Aucun texte inventé par le générateur n’est accepté : le paragraphe anglais de la scène 06 v1, le point ajouté à la scène 10 v2 et les guillemets supplémentaires de la scène 13 sont consignés comme échecs, pas comme contenu livré.

## Corrections suivies dans la salve 03

- Scène 10 : **QC accepté** après suppression du point final parasite.
- Scène 13 : **QC accepté**; une seule paire de guillemets entoure maintenant la parole citée.
- Scène 16 : toujours **rejetée**; le modèle a rendu une barre d’interface sociale malgré l’interdiction.

Les autres résultats du lot initial restent inchangés.
