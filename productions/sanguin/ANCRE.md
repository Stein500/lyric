# Sanguin — ancre et décisions

- Sources : `Sanguin.mp3` et `Sanguin.txt` à la racine du dépôt ; horodatages conservés.
- Affichage : paroles intégrées directement par le générateur, sur demande de l'artiste ; contrôle orthographique de chaque image indispensable.
- Les passages chantant la signature développée sont affichés sous la seule forme « WTBW » ; audio intact.
- Badge : DSKY ↔ WTBW ; ne pas développer WTBW dans les habillages.
- Style : anime seinen noir et blanc ; personnage et style approuvés par l'artiste.
- `fonds/scene-01-ancre.png` : ancre corrigée générée avec « WTBW » ; correction pas encore validée par l'artiste. Clip et contrôles finaux non réalisés.

## Suite — salve 1

- L'artiste a validé l'ancre corrigée et demandé de continuer.
- Salve 1 : 8 demandées, 8 générées, 0 échec technique (`scene-02.png` à `scene-09.png`).
- Statut : images générées, non validées pour le rendu. Le contrôle initial révèle des guillemets ajoutés sur plusieurs plans, un point ajouté sur scene-08, ainsi que des cadrages et des zones de texte à vérifier ou corriger. La fidélité visuelle et les zones sûres ne sont pas encore garanties ; ne pas considérer cette salve comme conforme.
- Les planches sont des supports de contrôle, pas un clip final. La durée décodée de l'audio et les contrôles vidéo restent à mesurer.

## Suite — salve 2

- Demande de l'artiste : chaque vers avec son image. Les reprises identiques pourront utiliser l'image du vers correspondant, sauf variante d'aube nécessaire ; ne pas regrouper plusieurs vers sur un même plan.
- Salve 2 : 8 demandées, 8 générées, 0 échec technique (`scene-10.png` à `scene-17.png`, vers de 00:45.43 à 01:06.18).
- Contrôle initial : ponctuation manquante sur les scènes 10 et 17, point supplémentaire sur la scène 13 ; certaines images ont un format 848×1264 au lieu de 768×1376. Images à corriger et à contrôler avant rendu, pas de validation finale revendiquée.
- Il reste les autres vers à illustrer, les contrôles 1:1, le montage, la couverture et les mesures finales.

## Format TikTok et salve 3

- Demande de l'artiste : toutes les images en portrait de résolution identique, adaptées à TikTok.
- Salve 3 : 8 demandées, 8 générées, 0 échec technique (`scene-18.png` à `scene-25.png`). Vérification initiale : `scene-19` répète « les » et doit être refaite ; les autres restent à contrôler en détail, notamment zones sûres et ponctuation.
- Les 25 images générées disposent maintenant d'une version de travail JPEG 1080×1920 dans `portrait-1080x1920/` ; dimensions vérifiées. Le script `outils/format_tiktok.py` conserve l'image entière et ajoute des marges noires si nécessaire plutôt que de couper les paroles. Les images de source plus larges présentent des bandes plus marquées ; ce ne sont pas des versions finales validées et la conformité des zones sûres reste à contrôler.

## Suite — salve 4

- Salve 4 : 8 demandées, 8 générées, 0 échec technique (`scene-26.png` à `scene-33-aube.png`) ; cinq vers supplémentaires et trois variantes d'aube du refrain final.
- 33 versions de travail au total dans `portrait-1080x1920/`, dimensions vérifiées. Sources de cette salve : 768×1376.
- Vérification initiale : la virgule de `scene-27` passe au début de la ligne suivante ; la progression lumineuse de `scene-30` après `scene-29` nécessite correction. Les images restent à contrôler pour la typographie exacte, le placement et la continuité avant rendu. Planche de contact et crops natifs enregistrés.
- Restent notamment le dernier vers du refrain final et la signature en variante d'aube, les corrections des salves, le calage, la couverture et le rendu complet.
