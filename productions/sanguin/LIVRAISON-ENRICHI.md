# Sanguin · DSKY — version enrichie et teaser

## Livrables

- `livrables/SANGUIN-DSKY-COMPLET-ENRICHI.mp4` : version complète fondée sur la V1 préférée par l'artiste, avec bandeau de messages défilants, progression, cœurs tracés et étincelles autour du badge. Intro et outro conservées.
- `livrables/SANGUIN-DSKY-TEASER-15s.mp4` : extrait indépendant de 15 s à partir de 00:24.166667 de la version complète ; audio extrait du morceau existant et réencodé, aucune musique ou voix générée.
- `livrables/COVER-SANGUIN-1080x1920.jpg` : couverture existante.

Le filet est à y=195 plutôt qu'à y=1560 : lors d'un contrôle d'échantillons, la position basse traversait certaines paroles déjà peintes. Le bandeau est en haut et les paroles restent celles des images. La synchronisation des fins de vers reste provisoire et les contrôles exhaustifs de tous les vers et zones sûres n'ont pas été réalisés. Aucun élément n'affirme une validation finale de l'artiste.

## Contrôles mesurés

| Contrôle | Complet | Teaser |
|---|---:|---:|
| Dimensions / cadence | 1080×1920, 30 i/s | 1080×1920, 30 i/s |
| Images / durée | 5 334 / 177,80 s | 450 / 15,00 s |
| `blackdetect=d=0.05:pix_th=0.10` | 0 intervalle | 0 intervalle |
| `blackdetect=d=0.05:pix_th=0.98` | 13 intervalles | 2 intervalles |
| `freezedetect=n=-33dB:d=2.5` | 12 débuts détectés | 0 début détecté |
| Niveau intégré | −14,3 LUFS | −13,1 LUFS |
| LRA | 10,2 LU | 3,3 LU |
| Crête vraie | −1,6 dBTP | −2,8 dBTP |
| Faststart | moov avant mdat | moov avant mdat |

Le test noir à seuil 0,98 est très sévère sur les images monochromes sombres : ces intervalles ne sont pas assimilés automatiquement à des écrans intégralement noirs. Les détections de gel du clip complet restent une limite connue ; les animations en haut de l'image ne suffisent pas à faire passer ce test, malgré leur mouvement visible. Aucun contrôle de typo exhaustif, master MP3 séparé ni normalisation −14 LUFS du teaser n'est revendiqué.

Visuels générés avec IA ; lettrages des vers générés dans les images selon la demande de l'artiste, habillage ajouté au montage ; audio fourni par l'artiste. Aucun son généré par IA.
