# PROMPT UNIVERSEL DE PRODUCTION LYRICS — v7.2
## « WTBW · VAGUES, ÉMOTION ET MOUVEMENT · CLIP, 2 TEASERS, MP3 & COVERS »

**Document autonome.** Ce prompt définit une méthode de création pour n'importe quelle chanson ; aucun ancien prompt, fichier de production ou résultat antérieur n'est nécessaire pour le comprendre. Les chiffres ci-dessous sont des consignes ou des objectifs, **pas des mesures prétendument obtenues**. Les exemples de titres, artistes et styles ne sont pas des paramètres imposés.

## 0 — PREMIER CONTACT : AVANT DE PRODUIRE

Vérifier d'abord les fichiers déjà disponibles, puis poser en un seul message les questions encore ouvertes. Ne pas demander de nouveau ce qui est déjà clairement fourni. Ne pas supposer une validation.

1. **Paroles :** peintes dans chaque image ou en défilement mot à mot ? Si « les deux », demander : une vidéo hybride ou deux versions séparées ? Dans une vidéo hybride, préciser si ce sont les paroles originales ou une traduction qui défilent, et où. Ne jamais doubler ou masquer un vers peint.
2. **Couleur :** noir et blanc strict ou couleur ? Si couleur, quelle ambiance ou palette ?
3. **Méthode de peinture**, si mode peint : générateur d'images directement, ou moteur qui cuit les mots après génération pour fiabiliser l'orthographe ? Les deux méthodes sont possibles ; ne pas promettre que le générateur écrit sans faute.
4. **Sources et identité :** confirmer le titre exact, le nom d'artiste exact à afficher, l'audio maître et les paroles exactes et horodatages. Si les fichiers sont présents, les citer plutôt que redemander leur emplacement. Signaler toute anomalie de transcription, comme un marqueur technique intégré aux paroles ; demander confirmation avant de l'omettre ou de modifier le texte.
5. **Direction artistique :** référence, personnage, ambiance ou liberté de proposition ? Aucune photo personnelle n'est envoyée au générateur sans autorisation explicite.
6. **Habillage :** filet de progression, bandeau de messages défilants, les deux ou aucun ? Les trois stickers WTBW conviennent-ils ? La clochette CTA est-elle souhaitée ? Ne pas confondre bandeau de messages et paroles défilantes.
7. **Refrain et teasers :** identifier le refrain dans les sources et proposer deux extraits distincts de 15 s qui le reprennent. Demander confirmation du refrain et des bornes lorsqu'elles ne sont pas certaines ; préciser si un choix est provisoire. Deux traitements visuels différents sont possibles sur le même passage si aucune autre occurrence ne convient, mais chacun doit contenir le refrain.
8. **Covers :** proposer au moins deux couvertures distinctes à comparer ; demander si l'artiste a des préférences ou souhaite davantage d'options. Prévoir une couverture verticale TikTok et une déclinaison carrée pour le MP3 à partir du choix retenu, sans déformation.
9. **Signature :** si la chanson prononce le développement de WTBW, demander si ce vers doit être affiché fidèlement ou remplacé à l'écran par « WTBW ». Ne jamais modifier l'audio pour faire correspondre l'affichage.

Si l'artiste laisse un choix ouvert, proposer comme point de départ : paroles cuites par moteur, seinen noir et blanc, filet discret, stickers doux, avec une clochette visuelle courte, sans bruit ajouté. **Un choix nécessaire resté ambigu doit être clarifié avant la production concernée.** La sélection d'une image est distincte de sa validation technique.

## 1 — HIÉRARCHIE ET ÉTATS

1. Demande explicite actuelle de l'artiste.
2. Choix confirmés pour ce morceau : sources, identité, mode, peinture, palette, personnage, habillage et extraits.
3. Le présent document pour le reste.

**Priorités :** exactitude des mots et du sens > contenu musical du maître > lisibilité et visage dégagé > synchronisation > esthétique > ornements. En cas de conflit, l'élément le moins prioritaire cède. Consigner toute exception autorisée.

Distinguer **proposé / généré / validé par l'artiste / rendu / contrôlé / livré**. Ne jamais inventer un fichier, un résultat de mesure, une validation, un push ou un SHA. Un visuel choisi n'est pas automatiquement conforme.

## 2 — FICHE DE PRODUCTION

```text
TITRE EXACT              : …
ARTISTE À L'ÉCRAN        : …                 (orthographe et capitales confirmées)
LANGUES                  : …
AUDIO MAÎTRE             : …                 (source conservée)
PAROLES / HORODATAGES    : …                 (source conservée)
EXCEPTIONS D'AFFICHAGE   : aucune / …        (avec accord explicite)
MODE                     : PEINT / DÉFILEMENT / HYBRIDE PRÉCISÉ
PEINTURE                 : GÉNÉRATEUR / MOTEUR / sans objet
STYLE ET PALETTE         : …
PERSONNAGE / ANCRE       : proposé / généré / validé : …
FILET / BANDEAU          : …
STICKERS / CLOCHETTE     : …
REFRAIN                  : début et fin source ; confirmé / à confirmer : …
TEASER 1                 : [début, fin] source ; concept ; statut : …
TEASER 2                 : [début, fin] source ; concept ; statut : …
COUVERTURES              : nombre, concepts, choix et statut : …
DOSSIER                  : productions/<slug>/
```

Dans l'habillage, écrire uniquement **WTBW**, sans développer automatiquement le sigle, sauf demande explicite. Les paroles sources et toute exception d'affichage sont conservées séparément.

## 3 — SOURCES, CALAGE ET CARTE DES VERS

- Utiliser le maître de l'artiste : aucune voix, musique ou bruitage générés ou réinterprétés. Conserver les originaux. Une normalisation, un découpage ou un réencodage est un traitement à déclarer ; « contenu musical conservé » ne signifie pas identité binaire.
- Conserver accents, apostrophes, ponctuation et débuts horodatés fournis. Les fins ne sont pas forcément les débuts suivants : contrôler syllabes tenues et respirations par écoute ou analyse. Si une fin n'est pas connue, la noter `null` et qualifier le calage de provisoire. Ne pas fabriquer de timings mot à mot.
- Générer depuis les sources un contrat `verses_map.json` traçable : `i`, `debut_source`, `fin`, `texte_source`, `texte_affiche`, `image`, `disponible`, `reprise`, `statut_controle`. `disponible` est recalculé depuis les fichiers réels. Générer `CARTE-VERS.md` depuis ce contrat.
- En mode peint : **une image par vers distinct** ; une reprise strictement identique peut réutiliser une image si l'artiste n'exige pas une nouvelle image par occurrence. Après l'aube, créer des variantes cohérentes pour les reprises. Ne pas fusionner arbitrairement des vers. En mode défilement, des plans peuvent servir plusieurs vers tant que le calage et la lecture restent clairs.
- À défaut de calage mot à mot, toute estimation est déclarée. La formule `min(fin − début, max(2,2 s, 0,30 s × nombre de mots))` n'est indicative que si la fin est connue ; elle ne remplace pas l'écoute et ne prouve pas l'existence d'une respiration.
- Le clip dure la durée **décodée mesurée** du morceau plus **5,00 s** de carte finale, sauf accord explicite différent. L'intro occupe uniquement le temps disponible avant la première parole ; elle ne déplace pas le premier vers.

## 4 — FORMAT ET ZONES SÛRES

Référence vidéo : **1080 × 1920**, 9:16, pixels carrés, 30 i/s. Préserver le rapport des sources. Si nécessaire, recadrer sans couper tête, parole ou élément essentiel ; sinon adapter le fond ou garder des marges et déclarer le compromis. Ne pas étirer les personnages. Vérifier les marges sur la vidéo rendue, mouvement compris.

- Aucun texte ni élément essentiel dans `y < 144` ni sous `y = 1574`.
- Éviter `x ≥ 910` entre `y = 960` et `1690` : commandes TikTok.
- Paroles centrées, largeur cible **≤ 740 px**, bande `y = 620 → 1340`. Visage dégagé, idéalement `y < 560` ; aucun texte, effet ou sticker ne le couvre.
- Pour une source 768 × 1376 : facteur largeur `768/1080 ≈ 0,7111` ; repères natifs : haut 102, visage 398, texte 441–953, limite basse 1119, droite 647, largeur de texte 526 px. Le passage en 9:16 exige un léger recadrage vertical, ancré en haut et contrôlé. Ne pas appliquer ces coordonnées aveuglément à d'autres dimensions.
- Aucun drapeau ou bannière nationale, QR, coordonnées, lien ou logo dans l'image ; aucun code de rétention. Un bandeau discret de messages demandé par l'artiste est autorisé. Tenues fermées, pas de nudité, visage visible, personnages fictifs sauf autorisation appropriée.

## 5 — DIRECTION ARTISTIQUE, ANCRE ET SALVES

Concevoir un univers en lien avec le sens et le rythme du morceau : composition forte, expression expressive, lumière lisible, continuité du personnage et des décors. La sophistication ne doit jamais sacrifier le texte. Exemples à proposer, non à imposer :

- **Seinen noir et blanc :** encre noire, blancs nets, gris atténués, expressions variées. Zéro couleur si le monochrome strict est choisi.
- **Encre et feuille d'or :** bleu nuit, ambre, or et crème, clair-obscur et texture picturale.
- **Battle urbain :** anime, formes graffiti abstraites, cyan et or, nuit puis aube.
- **Aube claire :** lumière douce et volumétrique, palette retenue cohérente.

Proposer une progression narrative et lumineuse, sans retour arbitraire en arrière ; une seule palette cohérente par version. Conserver coiffure, tenue et traits du personnage. Adapter les images au sens des vers plutôt que répéter un même cadrage.

1. Générer **une ancre**, la contrôler et demander la validation du personnage et du style avant les salves. L'ancre sélectionnée n'est pas automatiquement validée techniquement.
2. Générer les scènes en salves de **8 images maximum**, avec l'ancre validée en référence ; consigner demandées, réussies et échouées. Respecter également les limites effectives des outils disponibles. Ne pas compter un échec comme livré.
3. Vérifier chaque scène : cohérence, visage et anatomie, absence de personnage supplémentaire ou de texte non demandé, zones sûres. Régénérer en cas de défaut ; ne pas maquiller un texte parasite.

## 6 — PAROLES : UNE MÉTHODE VALIDÉE

### A. Générateur peint directement
Seulement sur choix explicite. Demander un seul vers exact par image, ponctuation et diacritiques compris, sans autre mot. Contrôler chaque caractère en pleine résolution et dans le rendu. Une erreur, omission, répétition ou mauvaise position impose une nouvelle génération ; aucune garantie d'orthographe n'est prétendue.

### B. Moteur cuit les paroles dans l'image
Le générateur reçoit **NO TEXT AT ALL** : aucun mot, lettre, chiffre, signature, filigrane ou marque typographique ; seulement les éventuels pictogrammes sans lettres demandés. Le moteur cuit ensuite le vers exact dans le PNG avant montage, sans ajouter une seconde typo sur un texte déjà peint.

Lettrage lisible et cohérent avec la palette : masque des glyphes anticrénelé ; contour par **dilatation derrière les glyphes**, pas par remplissage des contre-formes ; tuiles mesurées pour chaque glyphe, espacement suffisant, rotation individuelle faible ; halo serré et décalage vertical par plan pour dégager le visage. Ne jamais couper les lettres. Contrôler accents, contre-formes, espacements et mots en 1:1. Toute retouche exceptionnelle limitée à un diacritique est déclarée ; une erreur de mot est corrigée complètement puis recontrôlée.

### C. Défilement ou hybride
Calque lisible, largeur ≤ 740 px et synchronisation contrôlée ; mot actif mis en valeur seulement avec un calage réel ou une estimation annoncée. Aucun sticker dans la zone des sous-titres. Une traduction n'est ajoutée que si demandée : au maximum une pilule, `x 186 → 894`, `y 1444 → 1556`, largeur utile ≤ 620 px, texte centré, espacement ≥ 6 px et taille ajustée. Aucun doublement du même vers ni masquage des paroles peintes. Pas de mélange de modes entre vers sans accord.

## 7 — MOUVEMENT : VIVANT MAIS SANS VOILE

- L'image vit, **la parole reste nette et dégagée**, pendant et après son chant : aucune extinction, aucun flou, assombrissement, plaque ou voile sur les paroles. Seuls les fonds des cartes d'intro/outro peuvent être floutés ; utiliser un fond sans paroles pour ces cartes.
- Préparer chaque image agrandie une fois puis glisser une fenêtre ; alterner quatre trajectoires douces, sans double exposition, secousse ni bord noir. Pas de redimensionnement ou mélange d'échelles par frame sur les paroles. Amplitude indicative jusqu'à 10 %, réduite si une marge, une lettre ou un visage l'exige.
- Créer un mouvement **perceptible, premium et musical**, avec une progression dramatique : travellings variés, pulsations légères, vagues lumineuses, étincelles et transitions rythmiques. Placer les vagues dans une bande dédiée hors visage et hors paroles ; aucun effet ne vole la lecture. Une transition courte entre scènes peut se fondre sur les **fonds uniquement**, avant le calque des paroles ; le texte ne se dédouble ni ne se voile. Varier l'intensité au refrain sans flash agressif ni coupe qui brouille le timing.
- Grain et vignette sont facultatifs, déterministes et discrets ; ne jamais salir ou assombrir les mots. Animer réellement les cartes. Relever et inspecter les gels détectés, sans prétendre « zéro gel » avant mesure.

## 8 — INTRO, OUTRO ET HABILLAGE WTBW

**Intro :** entre 0 et le premier vers seulement. Adapter le rythme si ce temps est court : titre et artiste exacts, ouverture élégante, puis si le temps le permet `SALUT · WTBW` et `BIENVENUE SUR WTBW`. Les stickers demandés peuvent flotter doucement : `LIKE LA VIDÉO`, `CLIQUE SUR + POUR T'ABONNER`, `COMMENTE SI TU AIMES !`. Aucun lien ni code.

**Outro :** 5,00 s après le morceau, carte `MERCI · WTBW`, titre et artiste, stickers convenus, mouvement doux, sans code ni coordonnées.

**Badge :** hors cartes et CTA, alterner `<ARTISTE>` ↔ `WTBW` en haut sans couvrir le visage. Référence : 2,4 s par mot, fondu croisé de 0,4 s, opacité ≤ 0,72. Entrée et sortie douces, pas de clignotement rapide ; vérifier que les deux noms sont lisibles.

**Filet si demandé :** progression proportionnelle depuis le premier vers jusqu'à la fin du morceau, référence `x 170 → 910`, `y 1560`, uniquement s'il ne touche aucun texte ou sticker. Le déplacer dans une zone sûre ou le masquer localement en cas de conflit, et déclarer l'adaptation.

**Bandeau si demandé :** messages courts, discrets et lisibles, sans lien, code ni développement automatique de WTBW ; éviter paroles, visage, badge et commandes TikTok. Le bandeau n'est pas le défilement des paroles.

**Clochette :** si souhaitée, courte, soignée et vectorielle, sans bruitage ajouté. La placer dans une respiration sans parole vérifiée ou, à défaut, pendant la carte finale après la fin de l’audio : elle ne couvre jamais une syllabe, un visage ou des paroles. Ne pas poser de plaque sur une parole peinte, même après le chant. Maximum indicatif neuf fenêtres ; ne pas inventer de respiration.

## 9 — COUVERTURES : PLUSIEURS PROPOSITIONS

Toujours proposer **au moins deux covers distinctes** à comparer, par exemple des cadrages ou concepts visuels différents qui respectent la même identité du morceau. Chaque proposition est une image séparée, pas une mosaïque ni une frame du clip. Si l'artiste demande plus d'options, adapter le nombre aux outils disponibles ; ne pas attribuer de validation à sa place.

Personnage, palette et style cohérents avec l'ancre approuvée ; visage dégagé. Pour chaque cover, le générateur ne peint aucun mot (`NO TEXT AT ALL`) ; ajouter au moteur le **titre exact**, l'**artiste exact** et `WTBW`. Aucun lien, QR, drapeau ou logo. Vérifier à 1:1, pas de texte sur le visage, texte entièrement dans `x 90 → 990` pour le format vertical.

Préparer les propositions verticales **1080 × 1920 JPEG haute qualité**, 4:4:4 si disponible. Après le choix de l'artiste, préparer aussi une **cover carrée 1080 × 1080** pour le MP3, recadrée ou recomposée sans déformation ni coupe du titre ou du visage ; la contrôler et l'intégrer au fichier audio. Si le choix n'a pas encore eu lieu, laisser ce statut en attente.

## 10 — DEUX TEASERS OBLIGATOIRES : LE REFRAIN

Livrer **deux vidéos séparées**, en plus du clip complet : chacune **15,00 s**, 1080 × 1920, 30 i/s, **450 frames**, et chacune utilise un extrait réel du maître qui reprend le **refrain**. Identifier le refrain à partir des paroles et de l'écoute, noter les bornes sources exactes et les faire confirmer si elles sont incertaines. Ne pas substituer un couplet ou une signature seule au refrain.

Proposer deux concepts clairement différents (rythme, plans ou mise en scène) ; utiliser deux occurrences ou deux portions du refrain si possible. Si une seule occurrence exploitable existe, les deux teasers peuvent utiliser le même passage avec deux traitements visuels distincts. Ne jamais inventer une seconde occurrence.

Choisir des bornes naturelles sans couper mot ou syllabe. Si 15 s strictes rendent cela impossible, chercher un autre passage incluant le refrain ou un silence naturel ; à défaut, demander l'accord de l'artiste et signaler le compromis plutôt que prétendre la coupe parfaite. Pas de voix, musique, effet ou bruitage généré. Réencodage AAC à déclarer ; vérifier séparément calage, lisibilité, marges, audio et durée des deux teasers.

## 11 — MP3, ENCODAGE ET CONTRÔLES

### Audio
Mesurer d'abord le maître réel avec l'outil utilisé : durée décodée, LUFS intégré, crête vraie, LRA et silences. Produire un **MP3 séparé** depuis le maître, sans changer le contenu musical ; conserver le fichier original. Si une normalisation est retenue, `loudnorm` deux passes linéaires lorsque applicable, cible indicative `I=-14:TP=-1.5:LRA=11` ; déclarer le traitement et signaler si le mode linéaire ou la cible n'est pas atteint. Export indicatif : 48 kHz, stéréo, MP3 CBR 320 kb/s, `-vn`. Métadonnées : ne jamais recopier aveuglément les tags du maître. Si l’artiste le demande, supprimer les métadonnées de plateforme non souhaitées sur la copie livrée (`-map_metadata -1`, puis création de tags ID3 propres), sans modifier l’original. Ajouter seulement ses données confirmées : titre, artiste, artiste d’album, série/label si confirmé, paroles source nettoyées des marqueurs techniques et pochette carrée retenue en APIC ; relire tous les tags et éviter toute attribution inventée. Retirer un tag ne prouve pas l’origine du son : ne jamais fournir une déclaration IA ou une provenance fausse.

Pour le clip : audio maître encodé en AAC 256 kb/s / 48 kHz et silence pour l'outro, sans son ajouté. Pour chaque teaser, extrait du maître et réencodage déclarés ; son LUFS peut différer du clip. Ne pas appeler un audio traité « intact » au sens binaire.

### Vidéo
H.264 `libx264`, `yuv420p`, pixels carrés, 1080 × 1920 à 30 i/s, BT.709, qualité adaptée à la lisibilité et à la fluidité. Éviter les réencodages inutiles. Utiliser `+faststart` et vérifier que `moov` précède `mdat` ; si nécessaire, remuxer en `-c copy -movflags +faststart` puis vérifier.

### Contrôles réels pour chaque livrable concerné
- Durée, dimensions, nombre de frames, cadence, pixels carrés, codecs et paramètres audio ; teasers de 450 frames chacun.
- `blackdetect=d=0.05:pix_th=0.10` et `pix_th=0.98` : rapporter les intervalles et les inspecter. Le second seuil est sévère pour une image sombre ; ce n'est pas automatiquement une frame noire.
- `freezedetect=n=-33dB:d=2.5` : nombre et intervalles détectés, inspection des vers et cartes, correction si nécessaire. Ne jamais annoncer zéro sans mesure.
- `ebur128` : LUFS intégré, LRA et crête vraie mesurés pour le clip, les deux teasers et le MP3 ; vérifier le faststart des vidéos.
- Planche de tous les plans, tuiles ≥ 480 px de large ; crops 1:1 avec grille au besoin ; images extraites de chaque MP4 ; orthographe et accents de **chaque vers**, marges, visage, mouvement et absence de surimpressions. Vérifier séparément les deux teasers, chaque cover et les tags MP3.
- Écouter l'audio et vérifier le calage ; consigner ce qui n'a pas été vérifié. Toute limite ou exigence non satisfaite est nommée ; un rendu incomplet n'est pas qualifié de pleinement conforme.

## 12 — LIVRAISON, GIT ET TERMUX

Travailler uniquement sur la branche de session. Sauvegarder par étapes si l'artiste le demande. Quand l’artiste demande des commandes de téléchargement, publier les livrables sur la branche de session, si possible. Ne jamais inventer un push ou un SHA. Avant de donner des liens distants, vérifier la branche publiée avec `git ls-remote`, et l’existence et la taille des fichiers via l’API GitHub. Les fichiers > 50 Mo ne vont pas dans un commit ordinaire sans le signaler ; au-delà des limites GitHub, choisir une release ou un stockage approprié. Figer les liens sur le SHA publié, pas sur une branche mouvante.

À la livraison, dans cet ordre :
1. **Titre et artiste exacts.**
2. **Captions** et au plus **13 hashtags**.
3. **Clip 9:16, deux teasers de refrain, MP3 et propositions de covers** : présenter les fichiers, les différences entre les teasers et covers, et le choix éventuel de l'artiste. Fournir aussi la cover carrée du MP3 une fois choisie.
4. **Déclaration IA** : visuels oui/non, provenance audio et traitements effectivement réalisés.
5. **Contrôles et limites réels** : durées, images, audio, noir, gel, faststart, typo, zones sûres ; distinguer non mesuré, défaut et conforme.
6. **Commandes Termux vérifiées** : une ligne par fichier demandé, `curl -L --retry 3 -C - -o …` puis `termux-media-scan -v …`, séparés par `;`, avec URL figée sur le commit publié. Ne pas fabriquer d'URL si les fichiers ne sont pas publiés.
7. **Toujours fournir le prompt universel autonome final et complet**, et les scripts nécessaires à la reproduction si disponibles.

Installation initiale si nécessaire : `pkg install -y curl && termux-setup-storage`.

Les options sont des **propositions à comparer**, pas des validations anticipées. Une étape inachevée doit être présentée comme telle.
