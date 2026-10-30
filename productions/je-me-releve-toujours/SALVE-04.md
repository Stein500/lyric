# Salve 04 — corrections + scènes 27 à 34

## Bilan réel

- **Demandées** : 10 images (corrections des scènes 16 et 25; scènes 27 à 34)
- **Générées** : 10 images
- **QC visuel/typo accepté par l’agent** : 9 images — scènes 16, 25, 27, 28, 29, 30, 32, 33 et 34
- **Échec consigné** : 1 image — scène 31
- **Taille** : 768 × 1376 px par image
- **Contact sheet** : `CONTROLE-salve04.jpg`, 2 colonnes × 5 rangées; chaque tuile fait 500 × 896 px
- **Contrôle typo 1:1** : `CONTROLE-salve04-typo.jpg`, grille de 16 px
- **Retouche de lettres** : aucune
- **Validation par l’artiste** : en attente pour cette salve; l’ancre seule est validée par l’artiste.

## Contrôle par scène

| Scène | Vers source | État QC | Note |
|---:|---|---|---|
| 16 | `Chaque larme versée est devenue une œuvre` | QC accepté — correction | Aucun élément d’interface parasite; accents et ligature `œ` relus. |
| 25 | `Mais j'ai gardé la tête haute, j'ai gardé l'envie` | QC accepté — correction | Plus de point après `envie`; ponctuation source respectée. |
| 27 | `Ils m'ont frappé, ils m'ont volé, ils m'ont trahi` | QC accepté | Vers relu; sans violence graphique. |
| 28 | `Mais j'ai serré les dents, j'ai crié, j'ai rugi` | QC accepté | Apostrophes et accents relus. |
| 29 | `La vie m'a donné des coups, je lui ai donné des coups` | QC accepté | Ponctuation relue. |
| 30 | `Je suis le roi du ring, je suis debout, je suis fou` | QC accepté | Vers relu; ring symbolique, sans adversaire. |
| 31 | `Arigato, gracias, merci, monwê` | **Échec — à régénérer** | Le prompt contenait `Arigato` avec A majuscule, mais l’image commence par `arigato` minuscule. Image écartée dans `fonds/rejected/scene-31-v1-lowercase-arigato.png`. Original peint; traduction FR défilante réservée au montage. |
| 32 | `Je remercie la vie, je remercie la peine` | QC accepté | Vers relu. |
| 33 | `Elle m'a forgé, elle m'a soudé` | QC accepté | Apostrophes et accents relus. |
| 34 | `Maintenant je suis une armée, je suis l'éclat` | QC accepté | Apostrophe et accent de `éclat` relus. |

## Contrat texte

Chaque parole demandée figurait explicitement dans le prompt de son image. La casse incorrecte de `Arigato` vient du modèle; elle est consignée comme échec et n’est pas comptée comme image disponible.

## Correction suivie dans la salve 05

- Scène 31 : **QC accepté** après rétablissement du A majuscule de `Arigato`; le style de lettrage précédent est conservé.

La prochaine étape visuelle est la salve d’aube du refrain final.
