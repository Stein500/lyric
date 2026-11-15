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

## Suite — salve 5 et carte provisoire

- Salve 5 : 8 demandées, 8 générées, 0 échec technique : deux nouveaux plans d'aube et six propositions de correction (`-correction`). Les corrections ont été relues sur la planche de contact ; les contrôles 1:1 et zones sûres restent à faire.
- `verses_map.json` et `CARTE-VERS.md` attribuent provisoirement une image à chacun des 46 vers horodatés ; les répétitions réutilisent les mêmes plans, avec variantes d'aube au refrain final. Les horodatages de début sont conservés, les fins ne sont pas inventées. Toutes les images attribuées existent, mais cela ne signifie pas qu'elles sont conformes ou validées.
- Des anomalies des salves précédentes subsistent. Le montage et ses contrôles, la couverture et les mesures audio ne sont pas réalisés.

## Suite — salve 6 et mesure audio source

- Salve 6 : 8 corrections demandées, 8 générées, 0 échec technique (`scene-02`, `03`, `04`, `05`, `06`, `08`, `09`, `11`, suffixe `-correction`). La carte provisoire utilise ces propositions ; contrôle détaillé 1:1, zones sûres et continuité toujours nécessaires.
- Mesure du fichier source `Sanguin.mp3` avec FFmpeg 9.0.2, filtre `ebur128=peak=true` : durée décodée relevée 172,799979 s, niveau intégré −14,2 LUFS, LRA 10,3 LU, crête vraie −1,3 dBTP. `silencedetect=noise=-50dB:d=1` signale un silence final de 170,867771 à 172,799979 s. Ces chiffres concernent uniquement la source, pas un master final ni un clip.
- Aucun montage ni contrôle final du clip réalisé à ce stade.

## Prototypes animés d'habillage

- À la demande de l'artiste : prototypes muets d'introduction et de fin dans `livrables/APERCU-intro-muet.mp4` et `livrables/APERCU-outro-muet.mp4` ; ils ne sont pas le clip final.
- Cartes dessinées par `outils/cartes_animees.py` : dérive douce du fond flouté, salut en deux temps avec fondu, trois stickers flottants, cœur vectoriel dont le contour se dessine, et aucune expansion de WTBW. Intro 148 images à 30 i/s (4,933 s) ; outro 150 images (5,000 s) ; encodées en 1080×1920 à partir d'un prototype dessiné en 540×960. Aucun son dans ces aperçus.
- Prototypes non encore validés, grain et tous les contrôles du rendu final non réalisés. Les fichiers source de paroles continuent à nécessiter des contrôles. Le montage complet reste à faire.
