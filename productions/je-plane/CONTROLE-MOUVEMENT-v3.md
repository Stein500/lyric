# Je plane — vérification et correction du mouvement

## Diagnostic

Le contrôle initial `freezedetect=n=-33dB:d=2.5` signalait **26 débuts de gel**. Ce filtre détecte des périodes dont l'image varie peu ; il ne démontre pas à lui seul que toutes les images de ces périodes sont strictement identiques.

Huit fenêtres de deux secondes ont été analysées avec OpenCV dans une zone du décor située au-dessus des sous-titres, convertie en niveaux de gris puis réduite à 400×350 pixels. Sur les fenêtres échantillonnées de l'ancienne version, aucune des 60 paires successives de chaque fenêtre n'était pixel-identique dans cette zone ; la différence contenait aussi du grain et de la compression. La corrélation de phase, qui estime la translation du décor sur une seconde, indique notamment environ **(+0,23 ; +6,36) pixels** à 7 s et **(+1,90 ; +1,23) pixels** à 130 s. Ce sont des estimations sur les zones échantillonnées, pas une preuve que chaque image de toute la vidéo bouge.

## Correction

- Le travelling du décor a été renforcé et reste continu, avec une oscillation horizontale et verticale dans la marge du zoom ; la taille et la position des paroles ne bougent pas avec le décor.
- Les vagues, transitions, badge, filet et clochette finale sont conservés. Le niveau du grain n'a pas été augmenté pour contourner la détection.
- Le plan du vers 14 a été recadré sans déformation sur un fond étendu afin de ne pas couper la coiffure lors du travelling.
- Les deux teasers ont été régénérés depuis le nouveau clip.

## Mesures du fichier final

- **Clip complet : 0 intervalle de gel détecté** avec exactement `freezedetect=n=-33dB:d=2.5` (contre 26 auparavant). Ce résultat est limité à ce filtre et à ce seuil.
- Les deux teasers : **0 intervalle de gel détecté** au même seuil ; chacun comporte **450 images à 30 i/s**, soit 15,00 s.
- Les huit fenêtres ont été analysées de nouveau : par exemple à 7 s, translation estimée sur une seconde **(+41,77 ; +34,49) pixels** dans la zone du décor ; aucune des 60 paires successives de chaque fenêtre échantillonnée n'était strictement identique dans cette zone. Voir `analyser_mouvement.py` pour la méthode et les limites de la mesure.
- `blackdetect=d=0.05:pix_th=0.10` ne signale aucun intervalle sur le clip ; le seuil sévère `pix_th=0.98` signale 0–178,4 s en raison de la scène sombre et ne signifie pas que toute l'image est noire. Les deux teasers ne signalent aucun intervalle au seuil 0.10.
- Le clip comporte **5 353 images à 30 i/s**, 1080×1920 ; `moov` est avant `mdat` dans les trois MP4. Le décodage intégral des flux audio et vidéo des trois fichiers s'est terminé sans erreur. L'empreinte SHA-256 du flux AAC est identique à celle de la version précédente (`b18d97c5178440227eb41fec242d33779bc094f44d3b15377af92d42a37ca20a`). Le MP3 master et les couvertures ne sont pas modifiés.
- Des images extraites de chacun des 48 vers ont été examinées pour le cadrage, avec un contrôle spécifique du vers 14 corrigé ; cela ne remplace pas le visionnage intégral de chaque image à 1:1.

Le calage mot à mot et les bornes des teasers restent estimés et non vérifiés à l'écoute. La correction du mouvement ne permet pas de garantir leur synchronisation.

## Reproduction

Dans l'environnement Python : `pip install -r productions/je-plane/requirements.txt`. Puis `.venv/bin/python productions/je-plane/produire.py prepare`, `render` et `teasers`. Mesurer avec `.venv/bin/python productions/je-plane/analyser_mouvement.py <fichier.mp4>` et ffmpeg `freezedetect` ; ne pas remplacer une mesure de mouvement par une simple hausse du grain.
