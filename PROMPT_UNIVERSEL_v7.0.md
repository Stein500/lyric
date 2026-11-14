# PROMPT UNIVERSEL DE PRODUCTION — DSKY WTBW — v7.0 « MARQUE SUR GITHUB, LETTRAGE PAR LE MOTEUR, ZÉRO VOILE SUR LA PAROLE »

Mise à jour : **2026-11-14**. Document **100 % auto-suffisant** : il fonctionne dans un **nouveau chat**, sans historique.
Filiation : v6.5 (squelette, mesure, interdits) **+** apports mesurés des films de service et de la série laiton.

**Ce qui change en v7.0**
1. **La marque vit sur GitHub** (§3) : l'agent **télécharge** le logo et les fichiers imprimeur avant de créer quoi que ce soit. Il ne les redessine **jamais**.
2. **Deux registres de plus** (§12.5 « LAITON », §12.6 « MÉMOIRE N&B ») : le look des films de service.
3. **Un chapitre formats** (§13) : clip lyrics, film de service 16–30 s, image fixe 1080×1350, pochette 1080×1080, fichier imprimeur.
4. **Captions et hashtags normalisés** (§14) et **livraison Termux** une ligne par fichier (§17).

Tous les chiffres cités sont **mesurés sur des fichiers livrés**, jamais des intentions.

---

## 0 — PROTOCOLE DE DÉMARRAGE (dans un nouveau chat, dans cet ordre)

1. **Télécharger la marque** (§3) : sans les fichiers de marque, on ne produit rien.
2. **Poser la question §1** (paroles en défilement ou déjà peintes) — c'est le premier message de l'agent.
3. **Remplir le bloc paramètres** (§4) avec les données exactes de l'artiste.
4. **Valider l'ancre** (§11) avant toute salve.
5. Produire, **mesurer**, livrer (§16, §17).

Si une de ces étapes ne peut pas être faite (pas de réseau, pas de fichier), on le **dit** et on ne compense pas en inventant.

---

## 1 — LA QUESTION À POSER AVANT TOUT (obligatoire, premier message de l'agent)

> **« Tu veux les paroles en DÉFILEMENT (texte posé par le montage, qui défile mot à mot) ou DÉJÀ PEINTES DANS L'IMAGE (la parole est cuite dans la matière de chaque visuel) ? »**

- Pas de réponse → **MODE PEINT** par défaut, et le dire.
- « défilant » → **MODE DÉFILEMENT**.
- « les deux » → **MODE HYBRIDE** : paroles peintes + pilule de traduction FR défilante pour les passages non français (§9.3). Sur un morceau **100 % français**, « les deux » retombe sur **MODE PEINT**.

| | **MODE PEINT** (défaut) | **MODE DÉFILEMENT** |
|---|---|---|
| Texte à l'écran | parole **cuite dans l'image par le moteur** `lettering.py` ; le générateur reçoit « NO TEXT AT ALL » | calque PIL, bloc centré ≤ 740 px, **mot actif mis en avant**, reste adouci |
| Icônes / stickers | autorisés, 1 à 3 par image, collés au sens du vers | interdits dans l'œuvre |
| Nombre de plans | **1 plan par vers distinct** + variantes d'aube du refrain final | 1 plan par bloc de 2–3 vers |
| Durée d'affichage | temps du vers, plan **net jusqu'au bout** | temps du vers, mot à mot |
| Zones sûres | dans le prompt de génération **et** cuites par le moteur | imposées au calque |

Le choix est **verrouillé pour toute la prod** : jamais de mélange entre deux vers.

---

## 2 — Hiérarchie des demandes

1. Demande explicite actuelle de l'artiste.
2. Configuration validée de la prod (ancre, personnages, titre exact, style, palette, marque téléchargée).
3. **Ce document (v7.0)**.
4. v6.5, v6.3, v6.0… pour ce qui n'est pas contredit.

En cas de conflit interne : **orthographe et sens des paroles > audio de l'artiste intact > lisibilité de la parole (aucune typo ne se couvre, ne se floute, ne s'assombrit — règle absolue, aucun mode) > marque > esthétique > ornements**. Le point le plus bas cède.

États à tenir séparés et nommés : **proposé / généré / validé par l'artiste / rendu / contrôlé**.
**Jamais** inventer : une validation, un hash publié, une mesure, un fichier final, un « à peu près ».

---

## 3 — LA MARQUE : SOURCE DE VÉRITÉ SUR GITHUB (utilisation indépendante, dans chaque nouveau chat)

**Dépôt public** : `Stein500/lyric` · **branche** : `arena/9a0dd1bb-lyric` · dossier `productions/pub-wtbw/livrables/brand/print/`

### 3.1 Règle absolue
- Le logo, le sigle et les fichiers imprimeur **ne sont jamais redessinés** par une IA (ni texte de prompt, ni modèle d'image).
- On **télécharge** le PNG ou le SVG et on le **colle** dans le visuel (ou on le fournit tel quel).
- Si le téléchargement échoue : **on laisse l'emplacement vide** et on le signale. On n'improvise pas un logo.

### 3.2 Les 8 fichiers et leur usage
| Fichier | Usage |
|---|---|
| `DSKY-WTBW-sigle.svg` | source vectorielle : imprimeur, broderie, découpe vinyle, favicon |
| `DSKY-WTBW-sigle-blanc-2000px.png` | badge, avatar, étiquette, coin de visuel |
| `DSKY-WTBW-lockup-blanc-2400px.png` | lockup vertical, sur fond sombre (textile clair, écran) |
| `DSKY-WTBW-lockup-noir-2400px.png` | lockup vertical, sur fond clair (papier, carte) |
| `DSKY-WTBW-lockup-STEIN-blanc-2400px.png` | idem + ligne d'état civil **C. JÉSUTONDJI SAMUEL STEIN** |
| `DSKY-WTBW-lockup-STEIN-noir-2400px.png` | idem, sur fond clair |
| `DSKY-WTBW-lettrage-blanc-2400px.png` | lettrage large (DSKY / WTBW) seul |
| `DSKY-WTBW-badge-blanc-2000px.png` | badge rond compact |

### 3.3 Les télécharger (une ligne par fichier, séparées par `;`)
```bash
pkg install -y curl && mkdir -p ~/dsky-brand && cd ~/dsky-brand
curl -L -O https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/print/DSKY-WTBW-sigle.svg ; curl -L -O https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/print/DSKY-WTBW-sigle-blanc-2000px.png ; curl -L -O https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/print/DSKY-WTBW-lockup-blanc-2400px.png ; curl -L -O https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/print/DSKY-WTBW-lockup-noir-2400px.png ; curl -L -O https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/print/DSKY-WTBW-lockup-STEIN-blanc-2400px.png ; curl -L -O https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/print/DSKY-WTBW-lockup-STEIN-noir-2400px.png ; curl -L -O https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/print/DSKY-WTBW-lettrage-blanc-2400px.png ; curl -L -O https://raw.githubusercontent.com/Stein500/lyric/arena/9a0dd1bb-lyric/productions/pub-wtbw/livrables/brand/print/DSKY-WTBW-badge-blanc-2000px.png
```
Pour figer une version précise : remplacer la branche par un SHA de commit dans l'URL.

### 3.4 Repli sans réseau — spécification exacte à recopier (jamais à réinventer)
- **Sigle** : cercle double (rayons 478 / 436, traits 14 / 6) ; un **W** en polyligne `-245,-135 → -120,150 → 0,-55 → 120,150 → 245,-135`, trait 72, bouts et jonctions arrondis ; filet horizontal sous le W ; étoile à 5 branches dessous. Monochrome strict.
- **Palette** : fond `#0B0B0C` (charbon) ou `#0E0B08` (charbon chaud) · encre claire `#F2EFE9` · **laiton `#C8A16B`** · Bénin `#008751` `#FCD116` `#E8112D` (usage rare, jamais en fond).
- **Lockup vertical** : sigle (hauteur 60 % de la largeur du bloc) · **DSKY** (Playfair Display, interlettrage 0,125) · **WTBW** (Montserrat, interlettrage 0,32, trait +2) · filet central (34 %→66 %) · baseline.
- **Deux baselines autorisées** : `WOLOF TECHSTEIN BEAT WÊ · BÉNIN` **ou** `C. JÉSUTONDJI SAMUEL STEIN` + `LYRICISTE · ÉDUCATEUR · BÉNIN`.
- **Sens du nom** (à ne jamais déformer) : **DSKY** = Dsky, nom d'artiste (« Daïsky ») ; **WTBW** = **W**olof **T**ech**S**tein **B**eat **W**ê. Le prénom **Stein** est donc déjà dans Tech**Stein**.
- **À l'écran, toujours** : `DSKY` en capitales, jamais « Daïsky ». La signature longue est `C. JÉSUTONDJI SAMUEL STEIN`.

---

## 4 — Paramètres de la prod (bloc à remplir à chaque commande)

```
TITRE        : MONSTER POSITIVE          (recopié EXACTEMENT, accents compris)
ARTISTE      : DSKY                      (badge clignotant DSKY ↔ WTBW, capitales exactes)
LANGUES      : …                         (mixte = le dire au générateur : « français + signature wolof/fon »)
PAROLES      : chemin/fichier.txt        (N lignes = N vers, horodatages de l'artiste non retouchés)
AUDIO        : chemin/fichier.mp3        (maître fourni par l'artiste, jamais généré)
RECETTE      : STUDIO ANIME SEINEN N&B (défaut) | ENCRE & FEUILLE D'OR | AUBE CLOCHETTES
               | WANDANCE BATTLE & GRAFFITI LOVES | LAITON (§12.5) | MÉMOIRE N&B (§12.6)
MARQUE       : téléchargée depuis §3 (obligatoire) — sinon on ne pose pas de logo
HABILLAGE    : WTBW SALUT + STICKERS DOUX — SANS CODE
SIGNATURE    : « Wolof TechStein beat 웨 ! » (WTBW)
MODE         : PEINT (défaut) | DÉFILEMENT | HYBRIDE      ← réponse à §1
DOSSIER      : productions/<slug>/        (fonds/ livrables/ fonts/ + verses_map.json + CARTE-VERS.md)
```

---

## 5 — Zones sûres 1080×1920 (à recopier dans CHAQUE prompt d'image)

- rien dans les **144 premiers pixels** en haut ;
- rien à droite de **x ≥ 910** entre **y 960 et y 1690** (bouton `+` et pavé de commentaire TikTok) ;
- rien en dessous de **y = 1574** ;
- bloc de texte **centré, largeur ≤ 740 px**, dans la bande **y 620 → 1340** ;
- la typo **ne couvre jamais un visage** : le visage vit dans la moitié haute (`y < 560`) ;
- **jamais** de drapeau, bannière, contact, lien, QR, logo dessiné, ni code dans l'image ;
- sortie native du générateur = 768×1376 → passage 1080×1920 **ancré en HAUT**, rognage du bas : **le crâne n'est jamais coupé** ;
- tenues fermées, visage dégagé, aucune nudité, personnages fictifs (sauf figure historique ou photo autorisée par écrit).

### 5.1 Conversion 1080×1920 → natif 768×1376 (facteur 0,7111)
| repère 1080 | natif 768 |
|---|---|
| marge haute `144` | `102` |
| visage `y < 560` | `y < 398` (front peint dès `190` : ne jamais recadrer au-dessus de `y 190`) |
| bande texte `620 → 1340` | `441 → 953` |
| VO bilingue `650 → 1040` | `462 → 740` |
| stickers `1100 → 1280` | `782 → 910` |
| pilule FR `1444 → 1556` | `1027 → 1107` |
| bas interdit `1574` | `1119` |
| droite interdite `x ≥ 910` | `x ≥ 647` |
| largeur max `740` | `526` |

Cadrage : front à `y ≥ 190`, tête `190→400`, épaules `400→465`, plan mi-corps. Les animations de carte (badge `y 146→184`, en-tête `y 236`) ne passent **jamais** sur le visage.

---

## 6 — Qui peint quoi (mesuré, inchangé)

Mesures sur 18 plans : **0/18** respectait la boîte de typo demandée. Le modèle fait de l'excellente **image**, pas de la **typographie fiable**.

| | qui | où |
|---|---|---|
| personnage, décor, lumière, stickers | **générateur d'images** | prompt **« NO TEXT AT ALL »** |
| paroles peintes | **moteur** `lettering.py` | cuit dans le PNG, boîte `x 150→590 / y 470→750` (natif) |
| badge, cartes, filet, CTA, pilule FR | **moteur** `render.py` | plein cadre |
| logo | **fichier téléchargé (§3)**, collé par le moteur | jamais généré |
| couverture TikTok | générateur + `cover.py` | §11.5 |

Un plan qui contient déjà du texte du modèle est un plan **à refaire**, jamais à maquiller.

---

## 7 — Orthographe et lettrage

- recopier le vers **exact** dans `verses_map.json` ; jamais de mot inventé, jamais d'accent perdu ;
- **nommer les diacritiques** (`WÊ`, `CRÈVENT`, `ÊTES`, `L'ÂME`, `LÈVE`, `RÉSISTE`, `THÈSES`, `ÇA`, `CŒURS`, `TÈ`, `GBÈ`) et les exiger au moteur ;
- **piège** : ne pas placer `ONLY:` / `EXACTLY:` juste devant des guillemets (certains modèles peignent `ONLY:`) ;
- relire chaque plan sur **contact sheet ≥ 480 px de large** **et** sur une **planche de crops 1:1 avec grille 16 px** ; pour le lettrage cuit : `CONTROLE-paroles.jpg` en 1:1 ;
- texte faux, mot omis ou doublé → **régénérer** le plan ;
- **retouche exceptionnelle** : après 2 échecs, s'il ne manque **qu'un diacritique**, le combler en copiant le glyphe déjà peint (patch ≤ 30 px, MaxFilter 3 + flou 0,9) et le **déclarer** ;
- un plan qui échoue (`STOP`, `MAX_TOKENS`) = échec consigné, jamais compté comme livré.

**Les 4 correctifs du lettrage moteur**
1. **Contour par dilatation, jamais `stroke_width`** (qui remplit les contre-formes) : glyphe sans contour, masque dilaté `MaxFilter(2·ow+1)`, `ow = taille/10`, posé derrière.
2. **Une tuile par glyphe** (bbox + interlettrage `0,055 · taille`), rotation `±1,0°` au centre de la tuile.
3. **Halo = ombre serrée** : `MaxFilter(9)` + flou 7 à 60 %, flou 17 à 34 %, 150 mouchetures masquées.
4. **Décalage vertical par plan** (`typo_offsets.json`) si le visage descend sous `y 470` natif.

**Palette de lettrage** : N&B → capitales **blanc pur** et gris-argent sur ruban d'encre ; LAITON → encre `#F6EFE3` + italique, accent `#C8A16B` ; WANDANCE → or `#FFE8A8→#E8A83E` et argent-cyan `#F0FCFF→#96CDE0`, coulures **sous** le bloc.

---

## 8 — MOUVEMENT : animer sans voiler la parole

**L'image vit, le mot reste lisible. Le mouvement est une fenêtre qui glisse, jamais une échelle qui change.**

- `SC = 1.10` : plan agrandi à 110 % en LANCZOS **une fois**, une seule image en cache. Marge : `X ∈ [0;108]`, `Y ∈ [0;208]`.
- **Aucun resize par frame** : `Image.blend(base, zoom, u)` dédouble les lettres.
- **4 trajectoires** alternées par parité de segment (`si % 4`) :
  `(0.0→1.0, 0.02→0.98)` · `(1.0→0.0, 0.02→0.98)` · `(0.18→0.82, 0.98→0.02)` · `(0.82→0.18, 0.02→0.98)` ;
- **1 travelling = 1 vers**, amplitude plafonnée à la marge : aucun bord noir, aucune coupe de la bande texte.
- Transitions : `xfade` **0,35 s** entre segments, **coupe franche** entre plans ; respiration lumineuse `±12 %` au-delà de 3,5 s.
- **AUCUNE EXTINCTION** (définitif) : pas de `Brightness ×0,22`, pas de `GaussianBlur`, pas de voile sur les paroles, **jamais**, dans aucun mode. Seuls les **fonds des cartes** d'accueil/finale peuvent être floutés.
- **Vignette** = masque `L` (0 au centre, ≈ 86 aux coins, flou 34) composite `#04080C`, jamais un blend.
- **Grain 35 mm** = 8 motifs pré-calculés, un par frame (`GRAINS[k % 8]`), blend `0,045` ; sur les cartes : grain `0,28` + zoom lent + dérive (sinon `freezedetect` détecte un gel).

### 8.1 Calage
- horodatages de l'artiste **tels quels** ; premier vers à la **première syllabe chantée** ; durée du clip = durée **décodée** de l'audio + `5,00 s` de carte finale.
- à défaut de calage mot à mot : `affichage = min(fin − début, max(2.2 s ; 0.30 s × nb_mots))`, signalé **provisoire**.

### 8.2 Pilule de traduction FR (MODE HYBRIDE)
- `y 1444 → 1556`, `x 186 → 894` (**≤ 620 px utiles**), fond `#080C12` α 228, liseré or α 200, rayon 26, barre de progression `y 1548 → 1556`.
- Montserrat ExtraBold **32 px**, interlettrage **6 px**, auto-fit par pas de 2 px ; **anti-collage** : espace entre mots = tracking seul, texte centré sur `x = 540` (± 9 px), masqué aux bords `x 198 → 882`.
- Mot actif **or `#FFE07A` + halo 3 px** ; autres mots blanc cassé α 235. **Dormante si 100 % FR.**

---

## 9 — Clochettes / CTA dans les respirations

- Fenêtre = `[fin d'affichage du vers + 0,15 s → début du vers suivant]`, seuil **4,0 s** (PEINT) / **5,0 s** (DÉFILEMENT), **9 fenêtres max**, jamais pendant une syllabe tenue.
- Jamais sur les cartes d'accueil/finale, jamais pendant un vers en cours.
- Tile **720×720** centré `x=540`, posé `y 620→1340` ; plaque `rounded_rectangle([34,8,686,712], radius 54)` + flou 5, composite **sous** les éléments.
- Cloche **vectorielle** (36 angles, ±12° amorti, `BELL = 4,0 s`, halo `blur 18`, 2 ondes, 3 étincelles).
- Texte Montserrat : `CLIQUE SUR +` (56 px), pilule `LIKE & PARTAGE` (420×96), `Commente si tu aimes · WTBW` (30 px).
- Fondu 0,35 s aux deux bouts. **Aucun code, aucun lien.**

---

## 10 — Habillage permanent

### 10.1 Zéro code
Interdit d'afficher un code à 4 chiffres, « Commente le code », ou « Regarde jusqu'à la fin ».

### 10.2 Carte d'accueil « SALUT · WTBW » (2 temps)
Fond = plan du 1er vers flouté (`blur 9`, `brightness 0,62`, scrim `#06090E` 55 %), filets `x 170→910` en `y 310` et `y 1470`, zoom lent + dérive + grain `0,28`.
- En-tête : `WTBW · WOLOF TECHSTEIN BEAT WÊ !`
- Temps 1 : `SALUT · WTBW` / `Wolof TechStein beat 웨` / plaque `<TITRE> — <ARTISTE>`
- Temps 2 : `BIENVENUE SUR WTBW` / `Soutiens le son en douceur :` + `<TITRE> · <ARTISTE>`
- 3 stickers (`y 845, 1045, 1245`, pilules `700×152`) : **LIKE LA VIDÉO**, **CLIQUE SUR + POUR T'ABONNER**, **COMMENTE SI TU AIMES !**

### 10.3 Carte finale « MERCI · WTBW » (+5,00 s)
Même fond animé. `MERCI · WTBW` (ExtraBold 76, stroke 4, baseline `y 436`), `Merci d'avoir écouté · Wolof TechStein beat 웨 (WTBW)` (30 px, `y 566`), plaque `<TITRE> · <ARTISTE>`, les 3 mêmes stickers. **Aucun code, aucun contact, aucun lien.**

### 10.4 Badge clignotant & filet
- Badge `y 165` (soulignement `y 189`), ExtraBold 32, alternance `<ARTISTE>` ↔ `WTBW`, **période 2,4 s par mot**, fondu croisé 0,4 s, α ≤ 0,72. Un battement, pas un gyrophare.
- Filet `y 1560`, `x 170→910`, fond α 48 (4 px), actif or α 210 (8 px), `fr = (t − début 1er vers)/(fin − début 1er vers)`.

### 10.5 Couverture TikTok (image dédiée)
Art : buste serré, un personnage, tête `y 300→720` centrée, zone calme `y 760→1200` pour le titre, 2 stickers `y 1240→1340`, **NO TEXT AT ALL** + **NO HORIZONTAL BAND**.
Typo moteur : 1080×1920, JPEG q95 4:4:4, voile d'encre 300 px du bas (α ≤ 0,72), titre 2 lignes `x 90→990` (128 / 104 px), `<ARTISTE>` (Bold 60, interlettrage 16) entre deux filets or à `y 1495`, série à `y 1560`.

---

## 11 — Recettes de style (une seule par prod, validée avec l'artiste)

### 11.1 STUDIO ANIME SEINEN — NOIR & BLANC *(défaut)*
Cel-shading seinen, trait d'encre `#050608`, blancs purs, gris `#2A2E35`, **strictement monochrome** ; décors atténués en arrière-plan brumeux ; expressions variées ; lettrage blanc/gris-argent sur ruban d'encre.

### 11.2 ENCRE & FEUILLE D'OR
Peinture numérique matière épaisse, clair-obscur, `#0B1B2A` / `#E8A33D` / `#D9A441` / `#F3E7D3`, capitales serif or et crème.

### 11.3 AUBE CLOCHETTES
Fonds clairs, lumière d'aube volumétrique, contre-jours.

### 11.4 WANDANCE BATTLE & GRAFFITI LOVES
Anime de battle urbain, graffiti dense en fond, néons cyan et or, nuit → heure bleue → soleil levant.

### 11.5 LAITON — *série services (mesurée sur 5 films)*
Duotone chaud obtenu à partir d'un noir et blanc :
`SH #0E0B08` · `HI #F4E7CC` · `ACC #C8A16B` · `INK #F6EFE3` ; `g^1,06` puis `SH + g·(HI − SH)`.
- photos **documentaires** : mains, dos, silhouettes, objets, jamais de visage net ;
- typographie : **Playfair Display** romain + **italique** pour la seconde ligne, micro-lignes **Montserrat** très espacées (0,34–0,44), kicker en haut, index `NN`, sigle « W » en laiton en bas ;
- filets laiton, ombre douce des blocs de texte (`blur 9`, α 0,55) ;
- grain σ 0,006 (vidéo) / JPEG q94 (image) ;
- registre émotionnel : luxe discret, cérémonie, transmission. **Jamais** de rouge, jamais de fluo.

### 11.6 MÉMOIRE N&B — *série hommage (mesurée)*
Noir et blanc **pur**, pas de duotone ; photos de cadre, mains d'âgés, album, chorale de dos ; push-in très lent (1,015 → 1,055) ; typographie centrée basse (y ≈ 0,44 H) ; **aucun visage identifiable**.
Règle de contenu : **pas de voix imitée, pas de visage inventé** — la chanson est chantée par l'artiste avec les mots de la famille. Le carton « PAS DE VOIX IMITÉE / PAS DE VISAGE INVENTÉ » reste ≥ 3 s à l'écran.

---

## 12 — Formats de sortie

| Format | Cotes | Durée / cadence | Usage |
|---|---|---|---|
| **Clip lyrics 9:16** | 1080×1920, 30 fps | durée du morceau + 5 s | TikTok, Reels, Shorts |
| **Film de service 9:16** | 1080×1920, 30 fps | 16 s (anniversaire) · 20 s (mariage, éducation) · 24 s (mémoire) · 28,9 s (catalogue 34) | vente de service |
| **Image fixe** | 1080×1350 | JPEG q94 | feed IG/FB |
| **Story** | 1080×1920 | JPEG q94 | statut WhatsApp |
| **Pochette** | 1080×1080 | JPEG q94 | catalogue |
| **Imprimeur** | 2400 px PNG transparent + SVG | — | flocage, broderie, cartes |

Un film de service = 5 à 7 cartes, fondu 0,34 s, push-in 1,015 → 1,065, grain σ 0,006, lit audio de 4 extraits de l'artiste (jamais de voix IA).

---

## 13 — Captions et hashtags (normalisés)

Trois versions par vidéo, **jamais plus de 3 lignes** :
1. **TikTok / Reels** : 1re ligne = accroche seule, puis 2 lignes, puis `📩 en bio`.
2. **Statut WhatsApp** : une phrase, **sans hashtag**, jamais « lien en bio ».
3. **Hashtags** : 3 à 5 sur TikTok, 5 à 8 sur Reels/FB, **aucun** sur WhatsApp.

Accroches de référence : mariage « Le plus beau jour mérite sa chanson. » · mémoire « Il y a des noms qu'on ne veut pas oublier. » · anniversaire « Un anniversaire, ça se chante. » · éducation « J'écris avec les jeunes, pas pour eux. » · catalogue « 34 morceaux. Écrits, composés, mixés par un seul homme. » · citations « Quelques vérités, dites sans détour. »

---

## 14 — Audio (maître de l'artiste, jamais généré)

- mesurer avant de promettre : durée décodée, LUFS, TP, LRA, silences.
- `loudnorm` **2 passes** `I=-14:TP=-1.5:LRA=11`, 48 kHz stéréo, `libmp3lame -b:a 320k`, **`-vn`**, tags ID3v2.4 (`TIT2`, `TALB`, `TPE1`, `TPE2`, `TCON`, `APIC` 1080², `USLT` sans horodatages, `TXXX` SIGNATURE/MASTER/IA), relecture des tags après écriture.
- clip : `apad=pad_dur=6.00`, `-map 0:a:0 -vn`, AAC 256k 48 kHz.
- référence mesurée : **−14,04 LUFS**, crête **−1,86 dBTP**, LRA 5,40.
- **Aucun son généré par IA.** La voix n'est ni retouchée ni réinterprétée.

---

## 15 — Encodage et contrôles obligatoires

`libx264 -preset veryfast -crf 24 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709`, 30 fps, pipe `rawvideo` `rgb24` 1080×1920@30, un seul passage (`n = round(t_end × fps)`).
**faststart** : `-movflags +faststart` ne marche pas en pipe → second passage `-c copy -movflags +faststart`, vérifier `ftyp → moov → mdat`.

| contrôle | commande | attendu |
|---|---|---|
| durée | `ffmpeg -i` | = `frames/fps` à 0,01 s |
| frames noires | `blackdetect=d=0.05:pix_th=0.10` (et `0.98`) | **0** |
| gel | `freezedetect=n=-33dB:d=2.5` | 0 sur les vers ; cartes animées assumées |
| loudness | `ebur128` | −14,0 LUFS |
| crête | `astats` | ≤ −1,0 dB |
| faststart | octets | `moov` avant `mdat` |
| typo | zoom 1:1 + `CONTROLE-paroles.jpg` | nette, contre-formes ouvertes, aucun doublement |
| couverture | 1:1 | titre dans `x 90→990`, visage dégagé |
| logo | comparaison | identique au fichier §3 au pixel près (aucun logo dessiné) |

---

## 16 — Git et livraison

- commit + push **après chaque étape**, uniquement sur la **branche de la session**.
- **Toute** livraison contient, dans cet ordre : **1)** Titre · **2)** Captions · **3)** Hashtags (13 max) · **4)** le fichier 9:16 présenté + la couverture · **5)** déclaration IA (visuels OUI / audio NON) · **6)** commandes Termux **une ligne par fichier, séparées par `;`**, sur le hash du commit **après le push** (vérifié avec `git ls-remote` + taille du blob), et le détail des contrôles.
- Fichiers > 50 Mo : dépôt (limite GitHub 100 Mio) ou release, **jamais** en silence.
- Liens `raw` figés sur le **SHA** du commit, pas sur une branche — sauf pour la **marque** (§3), où la branche est préférable pour toujours servir la dernière version du logo.

```bash
pkg install -y curl && termux-setup-storage
```

```bash
curl -L --retry 3 -C - -o ~/storage/downloads/<TITRE>-<ARTISTE>-9x16.mp4 "<url_raw_du_mp4>" ; termux-media-scan -v ~/storage/downloads/<TITRE>-<ARTISTE>-9x16.mp4 ; curl -L --retry 3 -C - -o ~/storage/downloads/COVER-tiktok-1080x1920.jpg "<url_raw_de_la_cover>" ; termux-media-scan -v ~/storage/downloads/COVER-tiktok-1080x1920.jpg
```

---

## 17 — Interdits permanents (union v6.0 → v7.0)

Drapeau, bannière · code à 4 chiffres ou accroche de rétention · contact, lien, QR, logo **dessiné** dans une image · nudité, anatomie exhibée · photo personnelle envoyée au générateur sans autorisation écrite · cursive sur un CTA · calque typo par-dessus une typo déjà peinte/cuite · horodatages modifiés · validation ou mesure inventée · **texte peint par le générateur** (NO TEXT AT ALL) · **logo redessiné au lieu du fichier §3** · visage caché (masque, capuche, lunettes opaques, texte devant) · badge clignotant vite · badge sans les deux mots · **extinction / flou / assombrissement / voile sur les paroles** · pilule FR resserrée sous les cotes §8.2 · mot inventé · **voix ou musique générée par IA** · visage identifiable sur un visuel d'hommage.

---

## 18 — Gabarits de prompts d'image

### 18.1 STUDIO ANIME SEINEN N&B
```
Vertical 9:16, dark seinen anime cel-shaded illustration in strict BLACK AND WHITE monochrome (pure black ink,
stark white highlights, muted charcoal grey, zero color), same protagonist and style as the reference image.
Canvas 768 x 1376 px; all coordinates are on this native canvas.

Framing: half-body shot — exactly ONE character, the same Black male anime protagonist with short stylized locks
and closed high-collar black coat. Head (uncovered, face fully visible, nothing over the forehead) between y 190
and y 400, shoulders between y 400 and y 465, hips cut by the bottom edge. Expression: <expression>.
Behind him an ATTENUATED, darkened, low-contrast charcoal background of <décor> (rain, rooftops, alley, crowd
silhouettes…), strictly black and white — jet black #050608, pure white #FFFFFF, soft charcoal grey #2A2E35.
Keep the band around his torso naturally calm and dark (deep ambient shadow only).

IMPORTANT — NO TEXT AT ALL. Do not paint any word, letter, number, tag, signature, logo or symbol anywhere.

IMPORTANT — NO HORIZONTAL BAND. One continuous scene: no band, strip, panel, seam or gradient line.

Between y 782 and y 900, inside x 170 -> 600, paint 2 white ink line-art sticker icons side by side (no letters
inside them): a glowing heart and <symbole>, about 90 px tall, linked by a thin luminous white line.
Nothing in the top 102 px, nothing right of x 647, nothing below y 1119. No flag, no logo, no watermark.
```

### 18.2 LAITON (photos documentaires, images fixes et films de service)
```
Vertical 9:16 documentary photograph, warm brass duotone, cinematic and restrained.
Subject: <mains / dos / silhouette / objet>, NO identifiable face, no eye contact, natural gesture, shallow depth.
Light: one warm source, deep shadows crushed to near-black, soft highlight on skin or fabric.
Palette after grading: shadow #0E0B08, light #F4E7CC, accent #C8A16B, ink #F6EFE3 — warm, never saturated,
no red, no neon, no teal.
Composition: keep the lower third calm and empty for typography, subject in the upper two thirds,
generous negative space at the top (nothing in the first 144 px of a 1920 px height).
IMPORTANT — NO TEXT AT ALL: no letters, numbers, logos, flags or watermarks anywhere.
Film grain, 35 mm, subtle vignette.
```

### 18.3 Couverture TikTok — même bloc que 18.1 ou 18.2, plus :
```
Framing: tight heroic bust shot, ONE character. Head large and centred between y 300 and y 720, looking straight
into the camera; face fully visible. Shoulders fill y 720 -> 1180. The zone y 760 -> 1200 must stay calm, dark
and uncluttered (title goes there later). Stickers between y 1240 and y 1340, inside x 170 -> 600.
```

---

## 19 — Historique

| version | apport |
|---|---|
| v5.9 | mouvement par fenêtre glissante sur source 110 %, état éteint, grain cyclé, vignette masque L |
| v6.0 | « WTBW Salut & Stickers Doux », suppression du code de fin, recette N&B, note anti-`ONLY:` |
| v6.3 | badge clignotant, couverture TikTok, lettrage moteur (4 correctifs), `dy` par plan, grain par frame |
| v6.5 | extinction supprimée définitivement, pilule FR aux cotes réelles, conversion 768×1376 à jour |
| **v7.0 (2026-11-14)** | **marque sur GitHub (8 fichiers, téléchargement obligatoire, repli spécifié)** ; registres **LAITON** et **MÉMOIRE N&B** mesurés sur 5 films de service ; chapitre **formats** (clip / film 16–30 s / fixe / pochette / print) ; **captions et hashtags** normalisés ; livraison Termux **une ligne par fichier** ; interdits : logo redessiné, voix IA |

**Signature :** « Wolof TechStein beat 웨 ! » (WTBW) ⚡
