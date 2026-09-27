# Nonvi Konou — analyse préalable et direction de production

État : **ancre validée, salve 01 achevée, planche-contact en attente de validation**. Pas de clip livré à ce stade. Choix : style « Réalit » = photographie réaliste cinématographique chaleureuse ; héros inventé (aucun selfie utilisé) ; 9:16 seul ; cold-open 6 s à 135,56 s ; cover titrée en post ; livraison standard.

## Sources et mesures (27 septembre 2026)

- Audio : `Nonvi Konou.mp3`, 48 kHz, stéréo, **193,480 s décodées** (durée conteneur annoncée 193,51 s), avec une pochette vidéo attachée à ignorer lors de l'export audio (`-map 0:a:0 -vn`).
- Paroles : `Nonvi konou.txt` contient **50 vers horodatés, 35 textes distincts**. `Nonvi Konou.lrc` est la version LRC nettoyée des caractères de direction invisibles, avec horodatages source préservés. Les 15 reprises réutilisent les visuels de leur texte exact.
- Budget initial 9:16 : **35 illustrations de vers + intro instrumentale + endcard = 37 fonds distincts**, soit 4 salves maximum (10 + 10 + 10 + 7), **après validation d'une ancre**. Si 16:9 est choisi : budget identique en plus. Un vers répété exactement utilise la même image ; différence de ponctuation = autre image.
- Espacement min entre vers : au moins 1,2 s ; contrôle de pics du flux spectral dans ±0,35 s calculé sans remplacer automatiquement les entrées de voix par des attaques de batterie. Détails et intervalles dans `work/timings_validated.json` (cache reconstruit via `scripts/analyse_nonvi.py`). **Écoute / validation de synchronisation réelle encore nécessaire** avant rendu final.
- Tempo estimé par autocorrélation du flux spectral : **≈140,6 BPM** (ou demi-temps **70,3 BPM** ; ambiguïté typique). Repères énergétiques par RMS : premier refrain vers 15,61 s ≈ −17,4 dBFS ; refrain vers 59,30 s ≈ −14,1 ; reprise vers 135,56 s ≈ −12,6.
- Loudnorm passe 1 (`-v info`, cible −14 LUFS / TP −1,8) : **input_i −15,29 LUFS, input_tp +0,13 dBTP, input_lra 5,90, input_thresh −25,39, target_offset −0,91**. L'export final devra réellement faire une seconde passe et vérifier les mesures.
- Cold-open suggéré : **135,56 s**, « Nonvi konou, mon frère sourit » + « Gbè manfo do ohin min, la vie ne finit pas dans la misère », ~6 s ; section contenant le titre la plus énergétique. Si l'artiste préfère le premier refrain, commencer à 15,61 s.

## Direction confirmée par la demande

- **Une image IA narrative par vers distinct** ; recyclage seulement lorsque le texte est strictement identique.
- **Texte hybride simultané** : animation de vague d'eau et suivi **mot à mot**, vers centré horizontalement et verticalement, scrim central ; garder la largeur du vers stable durant le suivi. Adapter les vers longs en plusieurs lignes sans troncature.
- **Toutes les images** : bandeau long et propre en pied de page aux couleurs et à la géométrie correctes du **drapeau du Bénin** (vert vertical à gauche, jaune au-dessus du rouge à droite), et **« Dsky 🇧🇯 » lisible en haut**. Pour garantir l'orthographe, le drapeau et le badge seront dessinés en post-production sur chaque illustration, pas confiés au générateur d'images. Le badge étant déjà sur *chaque image*, ne pas le dupliquer à l'animation ; cette demande prime sur la consigne antérieure de badge uniquement intermittent. Position du bandeau en zone basse décorative, sans paroles sur les contrôles de plateformes.
- **Héros inventé confirmé**, sans lien avec les photos du dépôt : homme béninois fictif d'environ 27 ans, corpulence naturellement moyenne, peau brun foncé, visage ovale-arrondi, cheveux noirs crépus courts, barbe courte, sans lunettes, chemise de coton indigo à manches courtes avec col, pantalon sable. Garder ces caractéristiques à l'identique dans chaque prompt ; aucun embellissement du corps.

## Prochaine étape

Le questionnaire unique a été renseigné et **l'ancre a été validée par l'artiste**. Salve 01 : **10/37 images** (ancre + 9 nouvelles), soit encore **27 fonds à créer** en trois salves maximum (10 + 10 + 7). Voir `assets/nonvi_konou/plan_images.json` pour la correspondance des 50 occurrences avec les 35 vers distincts. Le modèle a parfois ajouté à tort des médaillons et des drapeaux approximatifs malgré les interdits ; ils ont été occultés sur les images habillées avant ajout du vrai bandeau géométrique. Éviter même la mention du mot « drapeau » dans les futurs prompts d'image ; ne parler que d'espace négatif réservé aux incrustations. Les brutes des 9 nouveaux visuels restent uniquement dans le cache ignoré `work/nonvi_salve_01/` pour limiter le poids Git, les images habillées et prompts étant versionnés.

**Ancre 01 créée** : `assets/nonvi_konou/ancre_01_brute.png` (génération IA sans texte), `assets/nonvi_konou/ancre_01_habillee.png` (badge + drapeau corrects) et `assets/nonvi_konou/ancre_01_maquette.png` (simulation du suivi mot à mot + vague au centre) ; prompt intégral `assets/nonvi_konou/ancre_01_prompt.md`. Cette maquette est une **image fixe de direction artistique**, et non une animation déjà rendue. **Attendre la validation de `assets/nonvi_konou/planche_salve_01.jpg` avant la salve 02**, puis continuer par lots de 10 au maximum. Le master MP3, les covers et les commandes Termux au hash immuable ne seront produits qu'après validation des visuels et réalisation du clip.

Reconstruction : installer les dépendances temporaires `imageio-ffmpeg numpy scipy` hors dépôt, puis exécuter `python scripts/analyse_nonvi.py`.
