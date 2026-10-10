# Gbètché vivi — Production lyrics · dossier de fabrication

Cadre appliqué : `PROMPT_UNIVERSEL_v5.7` (2026-10-10, fusion v5.5 + v5.6). Source audio : `Gbètché vivi.mp3` · paroles + horodatages : `Gbètché vivi - Bandit positif.txt` (47 vers). Mise à jour : 2026-10-10, tour 4 — **salve 2 livrée, 16/30 fonds générés et contrôlés**.

## 0 — Décisions de l'artiste (dans l'ordre où elles sont tombées)

1. **Les images portrait ne doivent pas être coupées en haut ni en bas dans la vidéo** → images **natives 9:16**, aucune reprise paysage recadrée. (§2)
2. **30 images** pour ce morceau, avec un ancrage proposé. (§3)
3. **Pivot tour 2** : « je préfère une seule personne… un homme qui me ressemble, prendre mes photos dans `Sam` et générer… personne animée dans un studio ». → **un seul héros**, inspiré du visage de l'artiste, en **rendu 3D « long-métrage d'animation »**, dans un **studio**. La salve photo « couple » est **archivée, non montée**.
4. **Tour 4** : « salve 2 et travail » → poursuite sans nouvelle question d'ancre.
5. Autorisation d'usage du visage : **donnée par la personne concernée elle-même** (§2 v5.7 respecté). Références faciales extraites des deux mp4 de `Sam/` via `ffmpeg`, stockées dans `_refs/`, **hors Git** (`_refs/.gitignore`) ; elles ne sont plus renvoyées au générateur depuis l'ancre validée.

## 1 — Ancrage retenu : « STUDIO POSITIF »

| Élément | Décision |
|---|---|
| Personnages | **1 seul**, l'avatar animé de l'artiste, dans tous les plans — aucune 2ᵉ personne, même en fond, même en reflet |
| Style | rendu 3D cinématique de long-métrage d'animation, proportions réalistes, peau subsurface, tissu mat ; pas de caricature, pas de plastique luisant |
| Lieu | studio : cyclorama gris chaud, béton ciré, néons teal, spot doré, brume légère |
| Palette | or / ambre + teal-indigo |
| Tenue (bloc héros, à recopier mot pour mot) | chemise col mandarin tie-dye indigo et bleu-gris à manches noires, **fermée jusqu'en haut** ; pantalon noir droit ; baskets blanches ; montre sombre au poignet gauche ; lunettes rectangulaires monture fine sombre ; cheveux très courts |
| Visage | jeune homme noir, visage rond-ovale, peau brune chaude, barbe naissante, expression calme, digne, souriante |
| Énergie | tête haute, épaules relâchées, mains ouvertes ; gestes de gratitude, de fraternité et de fête sobre ; aucune arme, aucun argent étalé |
| Interdits | nudité, cadrage sur le corps, membre coupé, texte/lettre/logo/drapeau/filigrane/emoji, bande noire, bordure ou trait clair dessiné près des bords |

Ancre validée par l'artiste (choix 2 sur 2) : `personnages/ancre-anim-01.png` — **toute génération repart de ce fichier via `images=`**.

## 2 — Règle « portrait jamais coupé » (demande n°1)

1. Images générées **en 9:16 vertical natif**, jamais de conversion paysage → portrait.
2. Chaque prompt impose : tête entièrement visible avec **≥ 10 % d'air au-dessus**, corps complet jusqu'aux chaussures, mains non coupées, rien d'important dans les 8 % supérieurs (zone badge) ni les 18 % inférieurs (zone CTA/crédits).
3. Rendu : **`scale=1080:1920:flags=lanczos` seul** — jamais `force_original_aspect_ratio=increase` + `crop`, jamais de `pad`. Sortie mesurée 768×1376 (ratio 0,5581 pour 0,5625 visé) → **étirement vertical de 0,8 %** préféré à une coupe de 8 px : imperceptible, aucune information perdue.
4. Contrôle de sortie : `qa_fonds.py` (bandes noires, air du crâne, zones sûres) + `cropdetect` au montage.

## 3 — Plan des 30 fonds studio (segments calés sur les débuts de vers)

Durée **décodée mesurée : 194,83 s** (start offset 0,023 s) — le `[length:03:14]` du fichier texte est un arrondi. Découpe en 30 segments par programmation dynamique : moyenne **6,30 s**, **aucune coupe d'image en milieu de vers**, minimum 2,57 s, maximum 15,07 s. Table de travail : `plan_fonds.tsv`.

| # | t0 → t1 | s | Scène studio — homme seul, personnage animé, 9:16 natif non rogné | État |
|---|---|---|---|---|
| A01 | 5,87 → 11,94 | 6,07 | Présentation : debout au micro, main sur la poitrine | généré |
| A02 | 11,94 → 17,49 | 5,55 | Gratitude : assis sur le tabouret haut, mains jointes | généré |
| A03 | 17,49 → 24,19 | 6,70 | Bénédiction : bras ouverts, paumes vers le haut, halo doré | généré |
| A04 | 24,19 → 27,36 | 3,17 | Paix : mains jointes devant la bouche, yeux fermés | généré |
| A05 | 27,36 → 41,60 | 14,24 | Marche sans chaîne : couloir de studio, chaîne rouillée au sol (fenêtre clochettes) | généré |
| A06 | 41,60 → 45,45 | 3,85 | La cabine : casque devant la vitre, salle de mixage **vide** (2ᵉ personne retirée salve 2) | généré |
| A07 | 45,45 → 52,32 | 6,87 | Rire : tête renversée, micro détendu | généré |
| A08 | 52,32 → 55,97 | 3,65 | Bandit positif : index à la tempe (tête abaissée à 11,3 %, cadre parasite retiré, salve 2) | généré |
| A09 | 55,97 → 59,36 | 3,39 | Spot unique : assis en tailleur dans le cercle de lumière, micro au sol | généré |
| A10 | 59,36 → 64,70 | 5,34 | Confiance : remonte ses lunettes, fond teal profond | généré |
| A11 | 64,70 → 70,93 | 6,23 | Menton haut : paume posée sur un caisson de monitoring | généré |
| A12 | 70,93 → 75,00 | 4,07 | Visage : rasant doré, yeux brillants, reflet du néon dans les verres | généré |
| A13 | 75,00 → 81,82 | 6,82 | Écrire : carnet sur les genoux, banc de mixage éteint et vide | généré |
| A14 | 81,82 → 88,26 | 6,44 | Parole tenue : poing serré tendu vers la caméra | généré |
| A15 | 88,26 → 91,50 | 3,24 | Verre d'eau : geste simple, carafe sur le tabouret | généré |
| A16 | 91,50 → 106,57 | 15,07 | La porte s'ouvre : bras levés dans le couloir, lumière blanche au fond (fenêtre clochettes) | généré |
| A17 | 106,57 → 112,45 | 5,88 | Marche latérale devant le cyclorama, plan large | généré |
| A18 | 112,45 → 118,07 | 5,62 | Deux mains posées sur la vitre de la cabine, salle vide derrière | généré |
| A19 | 118,07 → 124,51 | 6,44 | Adossé au mur acoustique, bras croisés, regard ferme | généré |
| A20 | 124,51 → 128,58 | 4,07 | Contre-jour total, silhouette dorée, visage encore lisible | généré |
| A21 | 128,58 → 135,62 | 7,04 | Danse douce sur place, épaules, sourire | généré |
| A22 | 135,62 → 139,12 | 3,50 | Cri de ralliement : poings levés dans la brume | généré |
| A23 | 139,12 → 146,00 | 6,88 | Dagbé : il règle un casque posé sur la console éteinte, manches retroussées | généré |
| A24 | 146,00 → 149,52 | 3,52 | Il s'avance dans le couloir, portes ouvertes qui inondent le sol de lumière | généré |
| A25 | 149,52 → 156,01 | 6,49 | Libération : fumée épaisse, néons, bras ouverts vers le haut | généré |
| A26 | 156,01 → 162,75 | 6,74 | Béni, en paix : assis au bord du cyclorama, lumière d'aube, micro entre les genoux | généré |
| A27 | 162,75 → 170,09 | 7,34 | Vue de dessus : minuscule au centre du studio vide, cercle de lumière (fenêtre clochettes) | à planifier |
| A28 | 170,09 → 181,17 | 11,08 | Mains sur ses propres épaules — apaisement, un seul visage au cadre | à planifier |
| A29 | 181,17 → 183,74 | 2,57 | Front calme : lunettes qui renvoient le néon, léger sourire | à planifier |
| A30 | 183,74 → 194,83 | 11,09 | Face caméra, main sur le cœur, lumière d'or → fond de la carte finale | à planifier |

**Fenêtres sans texte ≥ 5 s** (clochettes, durée d'affichage v5.7, à confirmer à l'écoute) : 30,24 → 41,60 · 94,38 → 106,57 · 173,11 → 181,17. La fenêtre 186,27 → 194,83 est tenue par **la carte finale**, pas par les clochettes.

## 4 — Carte d'accueil, carte finale, code

- **Accueil ~5 s** sur A01 : « Regarde jusqu'à la fin » puis « pour découvrir comment proposer un son ou des lyrics à réaliser pour toi ! » (≈ 4 mots/s, fondu 0,35 s, pas de coupe au milieu d'un vers).
- **Finale 5 s** après la chanson, sur A30 : « Merci d'avoir regardé » · « Tu veux un son ou des lyrics à réaliser pour toi ? » · « Commente le code » · code en grand, légende courte. Aucun contact, aucun lien, aucun logo.
- **Code proposé : `0314`** (durée du morceau 03:14). Alternatives `1414`, `3030` (trois mots-clés — Wanyiyi, Nonvi, Dagbé — une seule victoire). **En attente du choix de l'artiste.**
- Badge **« Dsky » seul, sans drapeau**, y = 160, opacité ≤ 75 %, fondu 0,4 s par vers. Paroles centrées sur H/2, largeur sûre ≤ 740 px, mot actif or / passés crème, vague 4,5 px à 0,9 Hz, effacement fondu 0,35 s pendant les clochettes.

## 5 — Audio et master (mesuré, pas supposé)

- Source : **194,83 s décodées**, 48 kHz stéréo, 182 kb/s.
- **−14,8 LUFS intégrés**, crête **−0,0 dBFS** → master en loudnorm **deux passes** (−14 LUFS / −1,5 dBTP) obligatoire, sinon la crête est hors marge.
- MP3 320 kb/s / 48 kHz, ID3v2.4 avec APIC (cover) + USLT (paroles nettoyées du caractère U+200E présent dans le fichier texte).
- Le calage mot-à-mot au nombre de caractères reste **provisoire** : à signaler dans la livraison ; tempo non encore attaqué.

## 6 — Livrables dus (§7 v5.7)

9:16 1080×1920 · titre · captions (légende courte + code) · 10 à 13 hashtags · **déclaration IA** (visuels 3D et avatar générés) · commandes Termux une ligne par fichier, `;` en séparateur, sur le hash du commit **après** push. Titre proposé : « Gbètché vivi — Dsky ».

## 7 — Contrôles salve 1 (A01→A08, avant correction)

| Fichier | Ratio | Bandes noires h/b | Air au-dessus du crâne | Verdict |
|---|---|---|---|---|
| `ancre-anim-01` | 0,5581 | 0 / 0 px | 11,0 % | OK (guide d'identité, hors montage) |
| `anim-01` → `anim-04` | 0,5581 | 0 / 0 | 11,0 → 11,6 % | OK |
| `anim-05` | 0,5581 | 0 / 0 | 0,0 % → **faux positif** | crâne réel vers 38 %, le crible accroche les néons du plafond. OK |
| `anim-06` | 0,5581 | 0 / 0 | 10,8 % | défaut n°1 : 2ᵉ personne (l'engineer) au fond → **corrigé salve 2** |
| `anim-07` | 0,5581 | 0 / 0 | 11,8 % | OK |
| `anim-08` | 0,5581 | 0 / 0 | 2,5 % | défaut n°2 : tête dans la zone badge + trait clair à ~4 % du bord → **corrigé salve 2** |

## 8 — Contrôles salve 2 (A06 et A08 corrigés + A09→A16)

`qa_fonds.py 'anim-*'` sur les 16 fonds : **768×1376, ratio 0,5581, 0 ligne noire en tête et en queue sur les 16 fichiers** → `scale` pur au montage = **aucune coupe haut/bas**, ce que l'artiste avait demandé.

| Point contrôlé | Mesure | Verdict |
|---|---|---|
| `anim-06` régénéré | air 10,8 % | salle de mixage **vide** derrière la vitre : plus de 2ᵉ personne |
| `anim-08` régénéré | air **2,5 % → 11,3 %** | tête hors de la zone badge, trait de bord disparu |
| `anim-09` → `anim-15` | air 10,9 → 18,2 % | OK, homme seul sur les 7 plans |
| `anim-16` | 0,0 % mesuré | **faux positif** : c'est le néon du plafond ; mains levées vers 18 %, vérifié à la planche. OK |
| Consistance personnage | 16 images | mêmes lunettes, même chemise tie-dye indigo/manches noires, pantalon noir, baskets blanches : aucune dérive sur `PLANCHE-anim-salve2.jpg` |
| Rendu test | `scale=1080:1920` sur un fond | sortie **1080×1920 exacte**, rien de rogné |

- Le crible « liseré clair » du script reste **informatif** : sur ce décor lumineux, seuil 140 → tout déclenche, seuil 150 + 45 % de couverture → rien. Les vrais traits de cadre sont relevés à la planche puis confirmés par `cropdetect` au montage.
- **Point de montage à trancher** : 10 des 16 fonds ont un tube néon clair dans la bande y 0→144, là où se pose le badge (y = 160, opacité ≤ 75 %). Proposition retenue par défaut : **scrim sombre 40 % derrière le badge** (300 × 74 px, rayon 16) plutôt que de retoucher les images ; sinon je descends le badge à y = 200.

## 9 — Archive : salve photo « MIDI POSITIF » (couple, 10 images)

Générée avant le pivot, **non montée**. Contrôle d'époque : `ancre-01.png` présentait **109 px de noir en haut (8,5 %)** → réparé (bande retirée, puis 61 px rognés sur chaque côté ; densité de contours des lisères 4,4 contre 6,9 au centre : du fond uniquement, aucun personnage touché), original conservé en `ancre-01-brut.png`. Les 10 scènes sont propres (aucune bande noire, 768×1376). **Aucun report automatique sur un autre morceau.**

## 10 — Prochain tour (ordre)

1. **A17 → A26** (10 = plafond de générations par tour), chacune repartant de `ancre-anim-01.png`.
2. **A27 → A30** + retouches éventuelles, planche des 30, validation de l'artiste.
3. Montage 9:16 (`scale` pur, jamais de `crop`), cartes d'accueil et finale, clochettes premium sur les 3 fenêtres, contrôles `blackdetect` / `freezedetect` / `cropdetect`, master −14 LUFS / −1,5 dBTP, covers, livrables (titre, captions, hashtags, déclaration IA, code **0314** à valider).
4. Commit + push après chaque étape, sur `arena/f0df3f2f-lyric` uniquement. `ffmpeg` utile est fourni par `imageio-ffmpeg` (pas d'installation système possible dans ce sandbox).

## 11 — Intro « libre + clochette » (demande du tour 5)

Demande : **début libre de toute parole**, qui donne l'envie de regarder jusqu'à la fin, **avec la clochette et les CTA dès l'ouverture** (commenter, partager, enregistrer, s'abonner).

Moteur : `render_intro_cta.py` (PIL + ffmpeg `imageio-ffmpeg`, piloté en rawvideo, aucun fichier intermédiaire). Sortie : `livrables/intro-clochette-916.mp4`.

| Paramètre | Valeur appliquée |
|---|---|
| Fenêtre | 0,000 → 5,867 s (176 images / 30 fps = 5,867 s) — le 1ᵉ vers tombe à 5,87 s, aucune parole pendant l'intro |
| Fond | `anim-01.png` en `scale=1080:1920` **sans crop** + scrim doux (132/126 alpha floutés derrière les blocs de texte pour ne pas manger le visage) |
| Carte 1 | « REGARDE JUSQU'À LA FIN », y = 268, souli gné cyan, fondu 0,35 s, 0,30 → 2,05 s |
| Carte 2 | « pour découvrir comment / proposer un son ou des lyrics / à réaliser pour toi ! », 3 lignes, y 404/464/524, 1,95 → 5,62 s ≈ 15 mots en 3,7 s = **4,0 mots/s** (plafond §3) |
| Cloche | vecteur supersamplé **×3**, dégradé or → bronze, anse, battant, reflet ; balancement ±12° amorti (exp(−0,85·t), période 1,2 s), halo cyan pulsé 0,8 s, **2 ondes concentriques** (0,9 s), **3 étincelles**, **flèche clignotante** (2,5 Hz) vers la cloche ; bande y 612 → 1012 |
| CTA | `ABONNE-TOI` blanc → bleu pâle, espacement 7 px, halo cyan (y 1002) · pillules `PARTAGE` `COMMENTE` `ENREGISTRE` : fond sombre translucide, contour dégradé cyan → magenta, texte dégradé, halo pulsé 0,8 s (y 1044 → 1122, bord droit mesuré ≤ x 905) · rappel « Clique sur la cloche, puis PARTAGE » (600, crème, y 1168) · « commente · partage · enregistre » (y 1236) |
| Badge | « Dsky » seul, **sans drapeau**, y 152 → 204, opacité 75 %, fondu 0,4 s |
| Zones sures | rien dans y 0 → 144 (le badge commence à 152), rien sous y 1574 (dernier texte 1236), rien à droite de x 910 entre y 960 et 1690 ✓ |
| Encodage | H.264 high, CRF 20, yuv420p, **bt709**, `+faststart`, son AAC 192k / 48 kHz pris sur `Gbètché vivi.mp3` (0 → 5,867 s) |
| Poids | 1,1 Mo pour 5,87 s |

**Contrôles mesurés sur le fichier** : `Duration 00:00:05.87`, **176 frames** = durée/FPS ✓ ; `blackdetect d=0.10` → **0 frame noire** ; `freezedetect n=0.05:d=1.2` → 1 segment signalé à t=0, attendu ici : le fond est une image fixe **volontairement** (carte d'intro), la seule zone animée est la séquence clochette. Aucun zoom/pan n'est appliqué : un Ken Burns recadrerait, ce que l'artiste a interdit.

## 12 — Contrôles salve 3 (A17 → A26)

10 nouveaux fonds : **768×1376, ratio 0,5581, 0 ligne noire en tête/queue sur les 10**, aucun membre coupé, **un seul personnage** sur chaque plan. Le crible « air au-dessus du crâne » signale A18, A20, A22, A23 (0 → 5,4 %) : **faux positifs**, dus aux néons verticaux, à la porte lumineuse et à la lampe d'atelier — vérifiés à la planche `PLANCHE-anim-salve3.jpg`, crânes réels entre 12 et 27 %.

**Un point à trancher — A17** : le marcheur projette **deux ombres portées** sur le mur (deux sources lumineuses). Ce sont bien SES ombres, mais à vitesse de lecture elles peuvent se lire comme deux silhouettes, alors que tu veux un homme seul. Réponse possible : soit on garde (ça fait « studio, deux projecteurs »), soit je régénère A17 avec une seule lumière.

**Reste à produire : A27 → A30** (4 images) + la régénration éventuelle de A17.
