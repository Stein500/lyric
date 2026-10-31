# PROMPT UNIVERSEL DE PRODUCTION LYRICS — v6.1

## « La parole exacte, un personnage cohérent, une provenance honnête »

**Mise à jour : 31 octobre 2026.** Document autonome consolidant les règles utiles de v5.9 et les corrections demandées pendant la production de « Je me relève toujours ». Il ne remplace ni les sources de l’artiste ni les instructions plus récentes de l’artiste. Conserver les versions antérieures et les journaux de production.

---

## 0 — Priorité et vérité de l’état

1. Demande actuelle explicite de l’artiste; 2. paramètres et références qu’il a approuvés; 3. ce prompt; 4. versions antérieures seulement si elles ne contredisent pas les points précédents.
2. Distinguer **proposé**, **généré**, **QC agent accepté/rejeté**, **validé par l’artiste**, **rendu**, **contrôlé** et **livré**. L’existence d’un fichier ou l’acceptation par l’agent n’est pas une validation artistique.
3. Ne jamais inventer une approbation, une traduction, une mesure, un hash poussé, une écoute ou un livrable. Si un contrôle n’a pas été fait, le dire. Corriger les journaux si un contrôle ultérieur invalide un résultat précédent.
4. Pour une nouvelle chanson, avant de générer quoi que ce soit, demander : **« Tu veux les paroles en DÉFILEMENT ou DÉJÀ PEINTES DANS L’IMAGE ? »** Si l’artiste ne répond pas, proposer PEINT par défaut et le signaler. S’il choisit les deux, utiliser PEINT pour les vers et réserver les incrustations aux traductions, cartes et habillage explicitement prévus. Verrouiller le choix pour toute la chanson.
5. **Aucun code à quatre chiffres**, aucune demande d’en choisir un, aucun code inventé sur les cartes. Ce point remplace toutes les anciennes règles sur les codes de durée.

---

## 1 — Bloc de configuration à remplir par chanson

```text
TITRE EXACT       : …
ARTISTE           : …                      (nom ID3, casse normale)
BADGE VIDÉO       : … / …                  (valeurs exactes et rythme d’alternance)
PAROLES           : …                      (fichier et convention de ses horodatages)
AUDIO MAÎTRE      : …                      (ne jamais le modifier)
LANGUES / GLOSSES : …                      (sens incertain = à confirmer)
MODE              : PEINT | DÉFILEMENT     (choix verrouillé)
STYLE / ANCRE     : …                      (référence approuvée par l’artiste)
FORMATS DEMANDÉS  : …                      (par défaut portrait 9:16 si c’est la demande)
DOSSIER           : productions/<slug>/
CARTES / CTA      : chaînes exactes listées avant composition, sans code
PROVENANCE IA     : image … ; audio …       (fondée sur les sources, pas sur une hypothèse)
```

**Exemple validé pour « Je me relève toujours »** : mode PEINT; artiste ID3 **Dsky**; badges vidéo alternés **WTBW / DSKY**; tomate rouge ronde et expressive, grands yeux, sourcils/calyx feuillus, petits bras et pieds, illustration 3D cinématique. L’ancre est approuvée; l’approbation des autres images et du montage doit être recueillie séparément. Pour une autre chanson, ne pas imposer automatiquement cette tomate si l’artiste choisit une autre direction.

---

## 2 — Paroles, langues et traduction

- Copier les paroles **verbatim**, y compris casse, apostrophes, accents, virgules, points, guillemets et ponctuation finale. Ne pas réécrire pour faire tenir une ligne. Les retours à la ligne de composition ne modifient pas le vers.
- Analyser la convention réelle des horodatages du fichier : début ou fin selon ce qu’il indique. Ne jamais les déplacer pour faciliter le montage. Conserver les timestamps originaux dans la carte; convertir en secondes sans décalage cumulé.
- En PEINT, un plan par vers distinct; les reprises identiques peuvent réutiliser un visuel cohérent. Créer des variantes dédiées quand l’arc du récit l’exige, par exemple l’aube du refrain final.
- Pour chaque passage non français : **original peint dans l’image, seule la traduction française dans la bande basse**. La traduction doit correspondre au sens confirmé, sans superposer une transcription à la parole peinte. Ne pas traduire un mot dont le sens est incertain : demander son gloss à l’artiste et indiquer l’incertitude. Une signature assimilée à un nom propre peut rester non traduite, mais tout sens linguistique incertain et toute éventuelle exemption restent à signaler à l’artiste.
- Pour ce morceau : `Yeah... I'm still standing...` → `Ouais... je suis toujours debout...`; `Arigato, gracias, merci, monwê` → `Merci, merci, merci — c'est confirmé.` L’artiste a confirmé `monwê` = « c’est ça / c’est confirmé ». **Ne pas modifier `monwê` dans l’original.** Ne pas prétendre que le sens isolé de `wê` dans la signature a été confirmé s’il ne l’a pas été.
- La bande basse de traduction doit rester lisible et séparée du texte original, sans couvrir un visage ni un sticker de l’image. Un discret fond de sous-titre est une interface, pas une bannière ou un panneau dans la scène.

---

## 3 — Ancre et continuité visuelle

1. Générer une ancre 9:16 et la soumettre à l’artiste. La figer après sa validation, avec chemin, dimensions, prompt et état dans `ANCRE.md`.
2. Utiliser l’ancre et, lors d’une reprise, **l’image correspondant au vers** comme références de génération. Garder les mêmes caractéristiques du personnage, son visage visible et son identité d’une image à l’autre.
3. Faire progresser décor, météo et lumière par étapes cohérentes. Ne pas retourner à une nuit déjà dépassée après l’aube; préparer des variantes d’aube si une reprise en a besoin.
4. Aucune photo personnelle envoyée au générateur sans autorisation écrite. Pas de nudité, de drapeau, de bannière, de panneau, de contact, de lien, de QR, de logo parasite ni de visage caché.
5. Les objets symboliques ou stickers doivent être **demandés explicitement** et ne doivent pas se transformer en ponctuation ou en décoration typographique non sollicitée.

---

## 4 — Contrat de texte du prompt d’image PEINT

Tout ce qui doit être écrit dans une image doit figurer **explicitement dans le prompt correspondant**. Lister exactement toutes les chaînes autorisées; demander **aucun autre mot, chiffre, signe, ponctuation, marque ou ornement typographique**. Ne pas se contenter de « texte approprié » ou « affiche le vers ».

### Gabarit adaptable

```text
Une image verticale 9:16, illustration 3D cinématique, même personnage et même style
que les images de référence. Scène : <lieu, heure, posture, lumière, objets voulus>.

Le SEUL texte visible dans cette image est exactement, avec casse, accents et ponctuation :
<recopier ici le vers source complet, exactement>

Écrire ces mots DANS l’image dans le style <sérif / script / cursif> de la référence
précise de ce vers; haute lisibilité, contraste naturel et texte sous le personnage,
jamais sur son visage. N’écrire absolument aucun autre caractère ou mot; aucun signe,
ornement typographique ou ponctuation supplémentaire. Objets expressément autorisés :
<liste exhaustive, ou aucun>. Laisser la bande basse libre pour <traduction FR si utile>.

Pas de drapeau, panneau, bannière, filigrane, logo, contact, lien, QR, règle, grille,
mesure, repère ou diagramme. Personnage entier et visage dégagé. Composer dans les
zones sûres du portrait final; ne pas dessiner ces zones dans l’image.
```

- **Style lettre par lettre :** si l’image de référence de ce vers utilise du script, conserver le script; si elle utilise une cursive, conserver la cursive; si elle utilise du sérif, conserver ce sérif. Ne jamais uniformiser automatiquement tous les plans ni remplacer une écriture peinte par une police.
- Pour une régénération, joindre l’image de référence appropriée et demander explicitement de conserver son style de lettrage. Chaque tentative garde son prompt et son état.
- Les chaînes compositées au montage — badge, traduction, cartes et CTA — sont elles aussi définies explicitement dans le script ou le cahier de production. Elles ne doivent jamais être improvisées par le générateur.

---

## 5 — Zones sûres portrait et contrôle visuel

Pour un rendu **1080 × 1920** : garder une marge en haut d’environ **144 px**; badge éventuel vers y=160; ne pas placer le texte principal dans la colonne droite x≥910 entre y=960 et y=1690; éviter tout texte sous y≈1574. Garder le bloc principal centré et viser **740 px maximum de largeur**. Ne pas couper la tête, les lettres ou les accents. La traduction peut occuper une bande basse distincte au-dessus de la limite inférieure. Adapter le cadrage à la vraie image, puis vérifier une frame du MP4 : une zone sûre décrite dans un prompt n’est pas une preuve.

- Écrire les zones sûres en prose dans le prompt; **ne jamais produire de règle, grille, nombres de mesure ou diagramme dans l’image finale**.
- Vérifier visage dégagé, contraste sur téléphone, lisibilité, texte exact, absence de signes et d’ornements non demandés, cohérence du personnage, continuité de la lumière et marges à chaque image.
- Travailler en **salves de 10 générations maximum**; consigner demandées, obtenues, échecs, reprises et dimensions. Contact sheet à tuiles de largeur ≥480 px, puis lecture à pleine résolution / crop 1:1 en cas de doute. Les grilles sont uniquement des outils de contrôle, jamais des images livrables.
- Tout ajout non sollicité, faute, diacritique manquant, ponctuation fausse, lettrage changé, mauvais contraste ou visage caché = **rejet**, archivage et régénération. Ne pas corriger en recomposant une lettre à la police. N’effectuer aucune retouche de lettre non autorisée par l’artiste; déclarer explicitement toute retouche qu’il autoriserait.
- Après rendu, relire les frames réellement encodées, pas seulement les PNG. Si un frame révèle un problème passé inaperçu, corriger le journal précédent et rerendre; ne pas conserver à tort un verdict de QC positif.

---

## 6 — Carte de vers et minutage

Créer `verses_map.json` et `CARTE-VERS.md` à partir des paroles sources : index, timestamp source, début, fin déduite ou fournie, texte exact, langue, traduction et état, image, existence réelle, reprise/variante et durée d’affichage. Compter les fichiers distincts séparément des occurrences. `disponible` dépend de l’existence effective du chemin, pas d’une valeur saisie à la main.

- Durée audio : **compter les échantillons décodés** et diviser par la fréquence; ne pas confondre la durée des en-têtes MP3 avec la durée décodée. Finir la vidéo sur un nombre entier de frames. À 30 fps, un changement au premier frame non antérieur au timestamp présente un écart inférieur à 1/30 s; publier l’écart observé.
- La formule de lecture `min(fin_vers, début + max(2,2 s, 0,30 s × nombre de mots))` est une **heuristique provisoire**, pas une preuve de la fin chantée. Sans calage mot à mot, garder de préférence chaque vers lisible jusqu’au début source du suivant; ne pas l’éteindre au milieu d’un chant uniquement parce que l’heuristique est courte.
- Une longue pause instrumentale, l’extinction d’un vers et une fenêtre de CTA doivent être **vérifiées à l’écoute**. Si la fin chantée n’est pas confirmée, marquer la décision provisoire et demander validation; ne pas dire « sans voix » sur simple différence de timestamps.
- Conserver les reprises et les variantes, ainsi que les positions des cartes et CTA, dans le rapport de rendu. Toute synchronisation non vérifiée à l’écoute reste à valider.

---

## 7 — Cartes, badge, traduction et clochette

- **Accueil** dans la plage instrumentale précédant le premier vers, sans retarder l’audio ni manger une parole : sticker **WTBW** et texte explicite du type « Regarde jusqu'à la fin pour découvrir comment proposer un son ou des lyrics à réaliser pour toi ! ». Titre et lignes ajustés aux zones sûres. Utiliser une portion du décor réellement exempte de paroles, pas un crop qui laisse apparaître des fragments de lettres.
- **Finale** : après la fin décodée de la chanson, carte de 5 s environ, sticker **WTBW** et message chaleureux `Merci d'avoir regardé`. Aucun code, contact, lien, QR, drapeau ou logo parasite.
- **Badge vidéo** : alterner les chaînes exactes demandées, ici `WTBW` puis `DSKY`, d’un vers au suivant. Le nom ID3 reste `Dsky`. Police Montserrat ExtraBold ou autre police approuvée pour l’habillage, position haute sûre, contour lisible, fade discret. Ne pas recouvrir un visage ou les paroles; pas de badge parasite sur les cartes ou CTA si cela fait doublon.
- **Traduction** : originale peinte et unique ligne FR dans la bande basse, sans paraphrase inventée, au bon segment et avec fond discret si nécessaire. Conserver l’orthographe et la ponctuation approuvées.
- **Clochette / CTA** : uniquement dans une fenêtre confirmée sans parole en cours; prévoir au moins 4 s en PEINT. Ne jamais la placer sur une carte d’accueil, un visage ou une parole encore en lecture. Si aucune fenêtre n’est confirmée, ne pas l’inventer. Textes autorisés si choisis : `ABONNE-TOI` et `PARTAGE`, Montserrat, lisibles, sans texte ou signe supplémentaire; l’icône cloche est dessinée et doucement animée. Pas de plaque couvrant le personnage ni de bannière.

---

## 8 — Mouvement sans dédoublement de lettres

- Agrandir chaque source **une seule fois**, puis faire glisser une fenêtre fixe de 1080 × 1920 à l’intérieur de l’image préparée. 4 trajectoires douces alternées; limites de recadrage vérifiées. Jamais de zoom brutal, rotation, shake ou interpolation entre deux échelles qui dédouble les caractères peints.
- Une trajectoire accompagne le vers; les cartes peuvent rester fixes. Lors d’une vraie respiration instrumentale, une portion sans texte du même décor peut former un plan complémentaire, sans annoncer la parole suivante à l’avance.
- Entre plans, un fondu n’est permis que s’il ne superpose pas deux paroles et ne décale pas leur apparition. **Préférer une coupe nette** si un fondu crée deux lignes lisibles simultanément. Un léger fondu vers une image sans texte est possible après la fin confirmée de la lecture.
- Après un vers réellement terminé, le plan peut être assombri/flouté progressivement sur la même échelle. Ne pas recourir à ce traitement avant la fin chantée sur la foi d’une simple estimation.
- Aucun grain intermittent ou vignettage qui rend le texte illisible. Contrôler la netteté sur une frame encodée à 1:1 et éviter tout ghosting.

---

## 9 — Audio et métadonnées : maître protégé, provenance conservée

1. Mesurer la durée décodée, le LUFS, la plage et la crête vraie du maître; calculer son **SHA-256 avant et après**. Ne jamais le modifier.
2. Produire une **copie dérivée** si une normalisation ou un changement ID3 est demandé. Pour une normalisation streaming, viser environ −14 LUFS avec `loudnorm` en deux passes; prévoir suffisamment de marge de crête pour l’encodage MP3/AAC, puis **remesurer le fichier encodé**. Exemple : cible pré-encodage −2,0 dBTP pour respecter le seuil mesuré ≤−1,0 dBTP après compression.
3. Dans le dérivé : `TIT2`, `TALB`, `TPE1`, `TPE2`, `TCON`; pochette carrée 1080² `APIC` avec seulement les chaînes prévues; `USLT` propre à partir du fichier de paroles, sans timestamps; champs `TXXX` de signature, source, SHA et provenance IA. Relire toutes les balises et vérifier la pochette après écriture. Pour ffmpeg, mapper explicitement `0:a:0` et utiliser `-vn` à l’encodage audio pour ne pas traiter la pochette comme une vidéo.
4. **Ne jamais effacer la provenance pour présenter une œuvre IA comme non-IA.** Si le maître indique `made with suno`, conserver cette information et le lien d’origine dans les métadonnées de provenance et déclarer **audio IA : OUI**. Un lien de provenance dans les tags n’est pas un lien affiché à l’écran. Une conversion ne doit pas recopier comme valide un manifeste C2PA devenu périmé; conserver le maître intact et tracer son hash et sa provenance dans le dérivé. Si la provenance est contestée, demander un autre maître vérifiable.
5. Pour la vidéo : AAC 48 kHz, sans décaler la chanson; ajouter le silence nécessaire à la carte finale. Signaler les fondus audio appliqués. Différencier les mesures du maître, du MP3 dérivé et du MP4.

---

## 10 — Encodage et QC de livraison

- Portrait 1080 × 1920, 30 fps si demandé, `libx264`, `yuv420p`, BT.709, AAC, `+faststart`. Le nombre de frames est arrondi sur la durée audio décodée plus la carte finale; vérifier le résultat réel.
- Contrôles réels et chiffrés : durée et nombre de frames; dimensions/fps; `blackdetect` (indiquer les intervalles trouvés); `freezedetect` (lister les plages signalées et expliquer cartes fixes ou mouvements trop lents sans les masquer); LUFS et crête vraie encodés; `moov` avant `mdat`; contrôle typo à 1:1; contact sheets de frames et lecture des cartes, traduction, CTA, reprise et 30 dernières secondes.
- Comparer les timestamps des frames de changement avec les timestamps source; cette comparaison technique ne remplace pas une écoute de synchronisation. Signaler distinctement ce qui reste à valider artistiquement ou à l’oreille.
- Ne pas annoncer zéro défaut, une durée, un taux de compression ou une validation avant mesure. Rejeter et rerendre si la parole, la sécurité ou la lisibilité échoue.

---

## 11 — Git, livrables et réponse

- Ne travailler que sur la branche de session. Conserver le maître et les sources; exclure les environnements locaux et le travail temporaire, pas les livrables demandés. Ne pas committer les binaires ffmpeg ou les dépendances installées. Versionner les polices nécessaires avec leurs licences.
- Vérifier `git status` et `git diff --check`; committer puis pousser uniquement la branche de session. Vérifier le hash local avec `git rev-parse HEAD` et le hash distant avec `git ls-remote`. Vérifier la présence et la taille des livrables via l’API GitHub avant de publier une commande de téléchargement à hash figé.
- Une livraison comprend : **1. Titre; 2. caption; 3. hashtags (13 maximum); 4. vidéo 9:16; 5. déclaration IA séparée visuels/audio; 6. si demandé, commandes Termux reprenables, une ligne par fichier, épinglées au commit poussé et vérifié; 7. résumé des contrôles et limites.** Présenter le fichier principal dans le visualiseur.
- Si une validation artistique ou une écoute reste à faire, livrer le fichier comme **proposition** et demander cette validation. Ne pas le qualifier de final approuvé.

---

## 12 — Résultat de référence de la production « Je me relève toujours »

- 58 occurrences source, 43 textes distincts, 47 chemins d’image avec variantes d’aube. L’ancre seule a été approuvée par l’artiste au moment de la rédaction.
- La première version de scène 31 a connu des rejets de casse puis d’ornement non demandé; la nouvelle conserve `Arigato, gracias, merci, monwê`. La scène 06-aube a été reprise pour remplacer des points de suspension incorrects par `!`.
- Le premier rendu a révélé un contraste insuffisant sur scène 04-aube malgré une acceptation précédente : v1 rejetée et conservée, v2 générée avec le même sérif et un fond naturel plus sombre. Les journaux conservent la correction.
- Le maître porte une provenance Suno. Toute livraison doit la déclarer fidèlement; l’artiste demandé est **Dsky**. Les mesures et l’état du montage sont publiés dans le rapport de production, jamais extrapolés depuis ce prompt.
