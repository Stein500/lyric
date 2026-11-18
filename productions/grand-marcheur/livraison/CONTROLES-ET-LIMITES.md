# Contrôles et limites — Grand Marcheur

Rendus effectués avec ffmpeg n9.0.2, à partir du maître MP3 fourni. Audio réencodé en AAC ; cinq secondes de silence ajoutées pour l’outro du clip. Aucun remplacement de voix ni de musique.

| Contrôle | Clip complet | Teaser provisoire |
|---|---:|---:|
| Durée | 225,07 s (conteneur) | 15,00 s |
| Images décodées | 6 752 | 450 |
| Vidéo | H.264, 1080 × 1920, SAR 1:1, 30 i/s | H.264, 1080 × 1920, SAR 1:1, 30 i/s |
| Audio | AAC stéréo 48 kHz, cible 256 kbit/s | AAC stéréo 48 kHz, cible 256 kbit/s |
| Loudness intégré / LRA | −14,5 LUFS / 6,8 LU | −15,3 LUFS / 4,9 LU |
| Crête vraie | −0,8 dBFS | −2,1 dBFS |
| Moov avant mdat | oui | oui |

Logs complets : `../controles/grand-marcheur-complet-ffmpeg.log` et `../controles/grand-marcheur-teaser-PROVISOIRE-ffmpeg.log`.

- `blackdetect=d=0.05:pix_th=0.10` : aucun intervalle signalé. Le test à `pix_th=0.98` signale 0–133,43 s et 136,53–225,03 s pour le clip, et 0–14,97 s pour le teaser : ce seuil extrême classe aussi des images normales comme noires ; il ne signifie pas que ces séquences sont des écrans noirs. Des captures représentatives ont été examinées (`../controles/ecrans-video-extraits.jpg`), mais pas toutes les images.
- `freezedetect=n=-33dB:d=2.5` signale cinq intervalles sur le clip : 3,13–6,10 ; 8,43–12,73 ; 102,07–105,23 ; 177,67–181,90 ; 195,37–201,97 s. Le mouvement volontaire est discret et peut être considéré comme une image fixe par ce détecteur. Aucun intervalle signalé sur le teaser. Ces alertes ne sont pas une validation visuelle exhaustive.
- Le clip a été construit sur les débuts du fichier de paroles ; les fins sont estimées. **Synchronisation et découpe du teaser non vérifiées à l’écoute humaine.** L’extrait 155,96–170,96 s a été choisi par analyse de signal, non validé ; une syllabe pourrait être coupée. Vérifier avant publication et corriger si nécessaire.
- Les captures représentatives ont été examinées, pas une planche de chaque plan extraite du MP4, ni tous les textes à 1:1 sur les vidéos finales. Le contrôle orthographique et des zones sûres reste donc partiel.
- L’habillage utilise un filet avec repère mobile, un message et deux badges alternés en fondu ; ce n’est pas un remplissage continu du filet ni un fondu croisé simultané des badges. La signalisation couleur remontée au décodage indique bt709 pour la matrice, mais les primaires et le transfert sont non spécifiés. Les variantes d’aube sont des retraitements, et une reprise reste plus sombre.
- Visuels générés par IA ; lettrage ajouté par moteur. Titre « Grand Marcheur » repris de la métadonnée du fichier source ; à confirmer par l’artiste. Affichage « WTBW » conforme à la consigne de l’utilisateur, tandis que l’audio conserve les paroles prononcées.
