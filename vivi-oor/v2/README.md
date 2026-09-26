# Vivi OOR — V2, les dix retouches IA

Nouvelle demande : **afficher les dix images ici et les retravailler avec l’IA**.

## Voir les images

- **[`VIVI_OOR_10_images_directement_ici.html`](VIVI_OOR_10_images_directement_ici.html)** : affichage direct des dix retouches IA, avec les photos intégrées au fichier. **Aucune URL externe, aucun chemin d’image relatif, aucun serveur requis.** Faire défiler pour voir chaque portrait séparément. À privilégier dans le viewer.
- **[`VIVI_OOR_10_images_a_feuilleter.pdf`](VIVI_OOR_10_images_a_feuilleter.pdf)** : dix pages, une image 9:16 en grand par page ; consultation sans dépendance externe.
- [`index.html`](index.html) : galerie interactive à utiliser avec le serveur local, agrandissement au clic, navigation précédente/suivante et téléchargement individuel. Adaptée au téléphone.
- [`livrables/`](livrables/) : **10 PNG, 1080 × 1920, sans texte**.
- [`VIVI_OOR_V2_10_images_9x16.zip`](https://raw.githubusercontent.com/Stein500/lyric/eaec1480a8a5875f30681ee270d70dcb12e335cd/vivi-oor/v2/VIVI_OOR_V2_10_images_9x16.zip) : exactement les dix PNG, environ 20 Mo.
- [`VIVI_OOR_V2_apercu.jpg`](VIVI_OOR_V2_apercu.jpg) : vue d’ensemble secondaire ; la galerie permet de voir chaque portrait en grand.
- [`LIVRAISON_TERMUX.md`](LIVRAISON_TERMUX.md) : téléchargement reprenable du ZIP et du catalogue de prompts au commit immuable de livraison.

Les noms et numéros de la galerie sont placés **hors des images**. Aucun titre, badge ou contact n’est incrusté dans les dix PNG.

## Travail effectué

Dix appels d’édition IA, un par composition. Chacun reçoit :

1. **La même photo originale** `Samu/Snapchat-795169778.jpg`, comme référence principale des traits, de l’expression et de la tenue.
2. La composition V1 correspondante, pour conserver le décor et guider le cadrage.

Direction de retouche : raccords du portrait avec son environnement, lumière plus cohérente, réduction de la dominante magenta, rendu de peau moins bruité sans effet plastique, profondeur photographique plus naturelle. Pas de nouveau costume, d’accessoires ajoutés ou de personnage supplémentaire.

Les dix ambiances restent celles inspirées des paroles : invitation dorée, miel, étincelles, attente, lagune, cœur ouvert, trésor, dîner, danse et aube. Le catalogue [`PROMPTS_IMAGES_VIVI_OOR_V2.md`](PROMPTS_IMAGES_VIVI_OOR_V2.md) contient les instructions intégrales, rédigées avant génération.

**Important :** cette V2 est une **retouche IA de l’image entière**, pas une conservation pixel par pixel du portrait. Les traits sont guidés par l’original et les dix images ont été revues visuellement, mais les microdétails et le cadrage peuvent varier légèrement, notamment les épaules plus recentrées sur la 08. La source et la [V1 à portrait détouré](../README.md) restent intactes. Il ne faut pas attribuer les contrôles de fidélité pixel de la V1 aux nouvelles images.

## Contrôles

- Dix générations et dix PNG finaux distincts.
- Exports RGB 1080 × 1920 par redimensionnement proportionnel et léger recadrage, sans étirement.
- Sources IA de 768 × 1376, sauf la 02 en 768 × 1365 : l’export 1080 × 1920 n’est pas une capture native dans cette résolution.
- Revue des dix images : présence d’un seul personnage, tête entièrement visible, tenue globalement conservée, absence de texte incrusté et des cœurs Snapchat.
- Source originale non modifiée, empreinte SHA-256 vérifiée.
- ZIP ouvert et vérifié : dix entrées, aucun échec CRC.
- Galerie : liens locaux vers les dix aperçus et les dix PNG ; aucune dépendance à un service externe pour l’affichage.

Les empreintes, tailles et dimensions sont dans [`controle_qualite.json`](controle_qualite.json).

## Reproduire l’export, sans nouvelle génération

Depuis la racine du dépôt, avec Pillow installé :

```bash
python3 vivi-oor/v2/scripts/export.py
```

Pour afficher la galerie localement / en preview :

```bash
python3 -m http.server 3000 --bind 0.0.0.0 --directory vivi-oor/v2
```

L’export utilise les retouches IA déjà enregistrées dans `assets/edits/`. Les petits JPEG d’`apercus/` servent uniquement à l’affichage rapide : ce ne sont pas dix scènes supplémentaires et ils ne sont pas dans le ZIP.

Pour reconstruire la présentation autonome et le PDF, avec Pillow et pypdf installés :

```bash
python3 vivi-oor/v2/scripts/presentation.py
```

Ce script vérifie les empreintes des dix PNG, crée les dix pages et intègre les dix aperçus au HTML. Il ne retouche aucune image et ne lance aucune nouvelle génération IA. Ces nouveaux fichiers changent uniquement la présentation des dix retouches V2, pour éviter les problèmes d’affichage des liens externes et des chemins relatifs.
