# PROMPT UNIVERSEL DE PRODUCTION LYRICS — v6.0 « WTBW SALUT & STICKERS DOUX — ÇA BOUGE, SANS VOILER LA PAROLE »

Mise à jour : **2026-10-21**. Document **100 % auto-suffisant** : il intègre l'intégralité du moteur v5.9 (« Ça bouge, sans voiler la parole ») et le remplace par les **nouvelles directives officielles v6.0** validées sur `productions/goinfres/` :
1. **Suppression définitive du système de code de fin** (retrait de l'accroche *« Regarde jusqu'à la fin / durée c'est le code »* et retrait du code à 4 chiffres sur la carte finale).
2. **Nouvel accueil et finale en mode « Salut · Wolof TechStein beat wê (WTBW) »** avec **animations fluides et douces de 3 stickers vectoriels** :
   - **Like** (`LIKE LA VIDÉO` — cœur vectoriel pulsant en douceur),
   - **S'abonner sur `+`** (`CLIQUE SUR + POUR T'ABONNER` — bouton `+` vectoriel),
   - **Commenter** (`COMMENTE SI TU AIMES !` — bulle de commentaire vectorielle).
3. **Recette « STUDIO ANIME SEINEN — NOIR & BLANC, DÉCORS ATTÉNUÉS & EXPRESSIONS MULTIPLES »** validée à 36 plans / 47 vers (0 faute d'orthographe).

Tous les chiffres ci-dessous sont **mesurés sur des fichiers livrés**, jamais des intentions.

---

## 0 — LA QUESTION À POSER AVANT TOUT (obligatoire, premier message de l'agent)

Avant de générer quoi que ce soit, demander à l'artiste, en une phrase :

> **« Tu veux les paroles en DÉFILEMENT (texte posé par le montage, qui défile mot à mot) ou DÉJÀ PEINTES DANS
> L'IMAGE (le modèle écrit la parole dans la matière de chaque visuel) ? »**

- L'artiste ne répond pas → **MODE PEINT** par défaut, et le dire dans la réponse.
- Il répond « défilant » → **MODE DÉFILEMENT**.
- Il répond « les deux » → **MODE PEINT** pour les visuels, et incrustation réservée aux cartes + mots-clés.

| | **MODE PEINT** (validé) | **MODE DÉFILEMENT** |
|---|---|---|
| Texte à l'écran | écrit **dans l'image** par le générateur ; le montage n'incruste **aucune** typo hors cartes | calque PIL, bloc centré ≤ 740 px, **mot actif mis en avant**, reste adouci |
| Icônes / stickers | **autorisés et voulus**, 1 à 3 par image, collés au sens du vers | **interdits dans l'œuvre** : zone basse réservée au sous-titre |
| Nombre de plans | **1 plan par vers distinct** + variantes d'aube dédiées pour le refrain final (§9) | 1 plan par bloc de 2–3 vers |
| Accentuation | aucune sur-typo ; le gras est déjà dans la peinture | halo 3 px + `spaced()` lettrage espacé |
| Durée d'affichage | temps du vers, **puis le plan s'éteint** (§5.4) | temps du vers, mot à mot |
| Zones sûres | écrites **dans le prompt de génération** (§3) | imposées au calque (§3) |

Le choix est **verrouillé pour toute la prod** : pas de mélange entre vers, jamais.

---

## 1 — Hiérarchie des demandes (rappel permanent)

1. Demande explicite actuelle de l'artiste.
2. Configuration validée de la prod (ancre, personnages, titre exact, style, palette).
3. **v6.0 (ce document)**.
4. v5.9, v5.8, v5.7, v5.6, v5.5 pour ce qui n'est pas contredit.

États à tenir séparés et nommés : **proposé / généré / validé par l'artiste / rendu / contrôlé**.
**Jamais** inventer : validation de l'artiste, hash publié, mesure, fichier final, « à peu près ».

---

## 2 — Paramètres de la prod (bloc à remplir à chaque chanson)

```
TITRE        : …                      (recopié EXACTEMENT, accents compris)
ARTISTE      : …                      (signature d'écran, ex. « Dsky »)
LANGUES      : …                      (mixte = le dire au générateur : « français + signature wolof/fon »)
PAROLES      : chemin/fichier.txt     (N lignes = N vers, horodatages de l'artiste non retouchés)
AUDIO        : chemin/fichier.mp3     (maître fourni par l'artiste, jamais généré)
RECETTE      : STUDIO ANIME SEINEN N&B DÉCORS ATTÉNUÉS | ENCRE & FEUILLE D'OR | AUBE CLOCHETTES | <nouvelle>
HABILLAGE    : WTBW SALUT + STICKERS DOUX (Like · Clique sur + pour t'abonner · Commente si tu aimes) — SANS CODE
SIGNATURE    : « Wolof TechStein beat wê ! » (WTBW)
MODE         : PEINT (défaut) | DÉFILEMENT      ← réponse à la question §0
DOSSIER      : productions/<slug>/               (fonds/ livrables/ fonts/ + verses_map.json + CARTE-VERS.md)
```

---

## 3 — Zones sûres 1080×1920 (à recopier dans CHAQUE prompt d'image)

- rien dans les **144 premiers pixels** en haut (marge de sécurité : la règle d'or dit 140) ;
- rien à droite de **x ≥ 910** entre **y 960 et y 1690** (zone bouton `+` + pavé de commentaire TikTok) ;
- rien en dessous de **y = 1574** ;
- bloc de texte **centré, largeur ≤ 740 px**, dans la bande **y 620 → 1340** (les sous-lignes doivent rester **au-dessus** des icônes, jamais poussées sous `y = 1574`) ;
- la typo **ne couvre jamais un visage** : le visage du protagoniste vit dans la moitié haute (`y < 560`) ;
- **jamais de drapeau, jamais de bannière, jamais de contact/lien/logo, jamais de code** dans l'image ;
- sortie native du générateur = 768×1376 → passage à 1080×1920 **ancré en HAUT**, rognage du bas : **le crâne n'est jamais coupé** ;
- tenues fermées et élégantes, visage dégagé, aucune nudité, personnages fictifs uniquement (sauf figures historiques ou photos expressément autorisées par l'artiste).

---

## 4 — Orthographe : règle + pièges de prompt + droit de retouche exceptionnel

- recopier le vers **exact** dans le prompt, entre guillemets, sur 2 ou 3 lignes équilibrées ;
- **nommer les diacritiques** si la langue en porte (`WÊ`, `CRÈVENT`, `ÊTES`, `L'ÂME`, `LÈVE`, `RÉSISTE`, `THÈSES`, `ÇA`, `CŒURS`, `TÈ`, `GBÈ`) et les exiger explicitement ;
- **piège à éviter dans les prompts** : éviter de placer le mot anglais `ONLY:` ou `EXACTLY:` juste devant les guillemets d'une ligne courte, car certains modèles peignent littéralement `ONLY:` en haut du bloc (observé sur `scene-15` et `scene-29` v1 de *Goinfres*, corrigé immédiatement en v2) ;
- relire chaque plan sur une **contact sheet ≥ 480 px de large** (`500×896 px` par tuile) **ET** sur une **planche de crops pleine résolution 1:1 avec grille de 16 px** (`CONTROLE-salveN-typo.jpg`), jamais sur une miniature ;
- texte faux, mot omis ou mot doublé → **régénérer avec un prompt court et explicite** ;
- **retouche exceptionnelle** : si, après 2 échecs de génération, il ne manque **qu'un diacritique**, il est permis de le combler en **copiant le glyphe déjà peint par le modèle dans la même image** (patch ≤ 30 px, masque = pixels du glyphe uniquement, MaxFilter 3 + flou 0,9), jamais en recomposant un caractère à la police. Cette retouche doit être **déclarée** dans la livraison ;
- un plan qui échoue à la génération (`STOP`, `MAX_TOKENS`) = **échec consigné**, jamais compté comme livré.

---

## 5 — MOUVEMENT : animer sans voiler la parole

**Principe : l'image vit, le mot reste lisible. Le mouvement est une fenêtre qui glisse, jamais une échelle qui change.**

### 5.1 Préparation (une fois par plan)
- `SC = 1.10` : le plan 768×1376 est agrandi à **110 %** (≈ 1188×2132) en LANCZOS une seule fois par plan, puis on garde **deux** images en cache : la nette et l'« éteinte » (§5.4). Marge disponible : **108 px en x, 212 px en y**.
- **Aucun resize par frame** : `Image.blend(base, zoom, u)` entre deux échelles dédouble les lettres de la typo peinte (ghosting visible au zoom 1:1).

### 5.2 Le travelling
- la frame = `big.crop` d'une fenêtre 1080×1920 dont l'origine glisse de `(ax0,ay0)` à `(ax1,ay1)` selon l'avancement `u` du vers ;
- **4 trajectoires**, alternées par parité de l'indice du segment (`si % 4`) :
  `(0.0→1.0, 0.02→0.98)` · `(1.0→0.0, 0.02→0.98)` · `(0.18→0.82, 0.98→0.02)` · `(0.82→0.18, 0.02→0.98)` ;
- **1 travelling = 1 vers**, durée du travelling = durée du vers ;
- amplitude plafonnée à la marge (§5.1) : aucun bord noir découvert, aucune coupe de la bande de texte `y 620→1340` ;
- pas de rotation, pas de shake, pas de zoom-in brutal.

### 5.3 Transitions
- `xfade` (fondu enchaîné) de **0,35 s** uniquement **entre deux segments**.

### 5.4 État « éteint » d'un vers déjà lu
- quand le vers a fini de s'afficher (`disp`) mais que son plan court encore (respiration instrumentale `> 1,0 s`), le plan passe à **`Brightness 0.40` + `GaussianBlur 2`** en **fondu de 0,35 s** sur **la même fenêtre** que l'image nette :
  `Image.blend(nette, eteinte, g)` avec `g = min(1.0, (t − disp)/0.35)` → zéro ghosting.

### 5.5 Grain et vignette
- **vignette** = masque `L` centré (0 au centre, ≈ 86 aux coins, flou 34) composite d'une couleur sombre `#04080C` : `Image.composite(noir, cur, masque)`. Jamais `Image.blend(cur, image_sombre, k)`.
- **grain 35 mm** = **4 variantes pré-calculées, cyclées** (`grains[(k // 2) % 4]`, seed fixe) en composite sur `Brightness 1.09`.

### 5.6 Calage
- horodatages fournis par l'artiste gardés **tels quels** ; durée du clip = durée **décodée** de l'audio (`ffmpeg -map 0:a:0 -f null -`) + `5,00 s` de carte finale.
- formule d'affichage par vers en l'absence de calage mot à mot :
  `affichage = min(fin_vers - debut_vers, max(2.2 s, 0.30 s × nombre_de_mots))`, signalée comme **provisoire** dans la livraison.

---

## 6 — Clochettes / CTA pendant les respirations instrumentales

- **Fenêtre = temps sans parole en cours de lecture**, donc `[fin d'affichage du vers + 0,15 s → début du vers suivant]`, seuil **4,0 s** en MODE PEINT (5,0 s en MODE DÉFILEMENT).
- **Jamais** de clochette sur les cartes d'accueil/finale, ni pendant un vers en cours de lecture.
- Tile **720×720 centré sur x=540, posé en y 620→1340** (strictement dans les zones sûres).
- **Plaque** : `rounded_rectangle([34,8,686,712], radius 54)` + flou 5, composite **sous** les éléments pour neutraliser la parole peinte éteinte pendant le CTA.
- Cloche **dessinée en vectoriel** (pas d'emoji) : **36 angles** de balancement supersamplés ×3, pendule `±12°` amortie sur une période `BELL = 4,0 s`, halo `GaussianBlur 18`, 2 ondes concentriques (période 0,9 s), 3 étincelles, flèche clignotante vers la cloche.
- Texte en **Montserrat** (jamais de cursive) aligné sur l'univers **WTBW** :
  - `CLIQUE SUR +` (56 px ExtraBold espacé de 5 px),
  - pilule `LIKE & PARTAGE` (420×96 px),
  - rappel `Commente si tu aimes · WTBW` (30 px SemiBold).
- Entrée/sortie en **fondu 0,35 s** aux deux bouts de la fenêtre.

---

## 7 — Habillage permanent v6.0 : Accueil « SALUT · WTBW + STICKERS DOUX », Finale sans code, Badge, Progression

### 7.1 Suppression totale du système de code (nouvelle règle obligatoire v6.0)
- **Interdit** d'afficher « Regarde jusqu'à la fin / la durée c'est le code » à l'accueil.
- **Interdit** d'afficher un code à 4 chiffres ou « Commente le code » sur la carte finale.

### 7.2 Carte d'accueil « SALUT · WTBW » en 2 temps (`0,00 s → début du 1er vers`) avec animations fluides et douces de stickers
Fond = plan du 1er vers flouté (`GaussianBlur 9`, `Brightness 0.62`, scrim sombre), filets horizontaux (`x = 170 → 910`) en haut (`y = 310`) et en bas (`y = 1470`).
- **En-tête permanent** : `WTBW · WOLOF TECHSTEIN BEAT WÊ !` (Montserrat ExtraBold, centré ≤ 720 px).
- **Temps 1 (`0,00 → t0 / 2`)** :
  - Grand titre salutation avec léger flottement vertical doux (`±6 px`) : **`SALUT · WTBW`**
  - Sous-titre : **`Wolof TechStein beat wê`**
  - Plaque centrale encadrée : **`<TITRE> — <ARTISTE>`** (ex. `GOINFRES — DSKY`)
- **Temps 2 (`t0 / 2 → t0`)** :
  - Titre : **`BIENVENUE SUR WTBW`**
  - Sous-titre : **`Soutiens le son en douceur :`** + **`<TITRE> · <ARTISTE>`**
- **Les 3 Stickers vectoriels animés en douceur (`y = 845, 1045, 1245`, pilules `700×152 px` centrées)** présents sur les cartes :
  Chaque sticker flotte avec une trajectoire sinusoïdale fluide et douce déphasée (`dy = ±8 px`, `dx = ±5 px`, période `2,2 s`–`2,8 s`) et son icône vectorielle supersamplée ×3 respire doucement (`±4,5 %`, période `1,6 s`) :
  1. **Sticker LIKE** (icône **Cœur vectoriel**) : **`LIKE LA VIDÉO`** · *« Laisse un cœur si tu valides »*
  2. **Sticker + S'ABONNER** (icône **Bouton `+` vectoriel**) : **`CLIQUE SUR + POUR T'ABONNER`** · *« Rejoins Wolof TechStein beat wê »*
  3. **Sticker COMMENTER** (icône **Bulle de dialogue vectorielle**) : **`COMMENTE SI TU AIMES !`** · *« Dis-nous ton vers préféré »*

### 7.3 Carte finale « MERCI · WTBW » (`fin_chanson → fin_chanson + 5,00 s`) — sans code
Fond = plan du dernier vers flouté (`GaussianBlur 9`, `Brightness 0.62`, scrim sombre) :
- En-tête : **`WTBW · WOLOF TECHSTEIN BEAT WÊ !`**
- Titre : **`MERCI D'AVOIR ÉCOUTÉ !`**
- Sous-titre : **`Wolof TechStein beat wê (WTBW)`** · **`<TITRE> · <ARTISTE>`**
- Les **3 mêmes stickers vectoriels animés en douceur** (`LIKE LA VIDÉO`, `CLIQUE SUR + POUR T'ABONNER`, `COMMENTE SI TU AIMES !`). **Aucun code, aucun contact, aucun lien, aucun logo.**

### 7.4 Badge artiste & Filet de progression
- **Badge artiste** : « Dsky » (ou l'artiste) **en y = 160**, Montserrat ExtraBold 44, **un seul fondu de 0,4 s par vers**, α max **0,72** (≤ 75 %), soulignement 3 px, liseré sombre pour rester lisible sur un ciel clair/aube. **Jamais permanent**, jamais pendant les cartes, jamais pendant un CTA.
- **Filet de progression** : y = **1560**, x **170→910**, fond α 48 de 4 px, partie active α 210 de 8 px, `fr = (t − début_du_1er_vers) / (fin_chanson − début_1er_vers)`.

---

## 8 — Recettes de style (une seule par chanson, validée avec l'artiste)

- **STUDIO ANIME SEINEN — NOIR & BLANC, DÉCORS ATTÉNUÉS & EXPRESSIONS MULTIPLES** *(validée 36 plans / 47 vers sur « Goinfres », 0 faute)* :
  cel-shading seinen au trait d'encre noir franc (`#050608`), rehauts blancs purs (`#FFFFFF`), gris d'encre (`#2A2E35`), **strictement monochrome noir & blanc** ; **décors variés mais toujours atténués/assombris en arrière-plan brumeux** pour que le protagoniste et la typo blanche peinte dominent ; **expressions faciales variées** d'un plan à l'autre selon la dramaturgie du vers ; capitales serif blanches et gris-argent sur ruban d'encre noire dans `y 620→1340` + 2 stickers au trait d'encre blanche collés au sens du vers + fil lumineux blanc.
- **ENCRE & FEUILLE D'OR — « la nuit qui finit bien »** *(validée sur « Mahu ti tè gbè » et « On est réel »)* :
  peinture numérique matière épaisse, clair-obscur Rembrandt, palette bleu nuit `#0B1B2A` / ambre `#E8A33D` / or `#D9A441` / crème `#F3E7D3`, capitales serif d'or et crème, stickers dorés.
- **AUBE CLOCHETTES** *(v5.6)* : fonds clairs, lumière d'aube volumétrique.

---

## 9 — Continuité entre plans et progression vers l'aube

- l'arc lumineux avance par paliers continus (nuit / ombre → premières lueurs au pont → **aube lumineuse / plein soleil levant** sur le refrain final et l'outro) ;
- **pas de retour en arrière de la lumière** : toute reprise du refrain ou de la signature arrivant après le pont d'aube reçoit sa **variante aube dédiée** (ex. `v-167-69-aube.png`, `v-170-71-aube.png`, `v-174-05-aube.png`, `v-176-45-aube.png`, `v-181-90-aube.png` sur *Goinfres*).

---

## 10 — Méthode de fabrication (salves, ancre, contrôle)

1. **Ancre d'abord** : générer `fonds/scene-01-ancre.png`, la contrôler et la valider avec l'artiste (`ANCRE.md`). Elle sert de `images=[…]` de référence à **toutes** les salves.
2. **Salves ≤ 10 images par tour** ; consigner chaque tour : demandées / réussies / échouées.
3. `verses_map.json` = contrat unique généré par `build_map.py` : `{i, t, fin, affichage_s, texte, image, disponible, reprise}` où `disponible` est **recalculé avec `os.path.exists`**.
4. `CARTE-VERS.md` générée automatiquement depuis `verses_map.json`.
5. QC visuel obligatoire : planche contact `CONTROLE-salveN.jpg` (tuiles ≥ 480 px de large) + planche de crops 1:1 `CONTROLE-salveN-typo.jpg` (grille 16 px) + planche du MP4 final `CONTROLE-mp4-final.jpg` + zoom 1:1 `CONTROLE-typo-zoom.jpg`.

---

## 11 — Audio (maître de l'artiste, jamais généré)

- mesurer avant de promettre : durée décodée (`ffmpeg -map 0:a:0 -f null -`), LUFS, TP, LRA, silences.
- `loudnorm` **2 passes linéaires** `I=-14:TP=-1.5:LRA=11`, 48 kHz, stéréo, `libmp3lame -b:a 320k` (CBR 320 kbps), **`-vn` obligatoire**, puis tags ID3v2.4 (`TIT2`, `TALB`, `TPE1`, `TPE2`, `TCON`, `APIC` 1080², `USLT` propre sans horodatages, `TXXX` SIGNATURE/MASTER/IA) et relecture des tags après écriture.
- pour le clip : `apad=pad_dur=6.00` sur le maître avec **`-map 0:a:0 -vn`**, AAC 256k 48 kHz.

---

## 12 — Encodage et contrôles obligatoires du rendu

- `libx264 -preset veryfast -crf 24 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +faststart`.
- pipe `rawvideo` `rgb24` 1080×1920@30 → un seul passage (`n = round(t_end × fps)`).
- **Contrôles à publier avec les chiffres réels** :
  | contrôle | commande | attendu |
  |---|---|---|
  | durée | `ffmpeg -i` | = `frames/fps` à 0,01 s près |
  | frames noires | `blackdetect=d=0.05:pix_th=0.10` | **0** |
  | gel | `freezedetect=n=-33dB:d=2.5` | 0 sur les vers ; cartes et CTA signalés et assumés |
  | loudness | `ebur128` | −14,0 LUFS |
  | crête | `astats` | ≤ −1,0 dB |
  | faststart | octets | `moov` avant `mdat` |
  | typo | zoom 1:1 d'un frame rendu | nette, **aucun doublement de lettre** |

---

## 13 — Git et livraison

- commit + push **après chaque étape**, uniquement sur la **branche de la session**.
- **toute** réponse de livraison finale contient, dans cet ordre :
  **1)** Titre · **2)** Captions · **3)** Hashtags (13 max) · **4)** le fichier 9:16 (présenté à l'utilisateur) ·
  **5)** Déclaration IA (visuels OUI / audio NON) · **6)** commandes Termux, **une ligne par fichier, séparées par `;`**, sur le hash du commit **après le push** (vérifié avec `git ls-remote` + taille du blob via API), et le détail des contrôles + le prompt universel mis à jour.

---

## 14 — Interdits permanents

Drapeau, bannière nationale · système de code à 4 chiffres ou accroche « reste jusqu'à la fin pour le code » · contact, lien, QR, logo dans une image · nudité, anatomie exhibée · photo personnelle envoyée au générateur sans autorisation écrite · cursive sur un CTA · calque typo par-dessus la typo peinte · horodatages de l'artiste modifiés · validation ou mesure inventée.

---

## 15 — Gabarit de prompt d'image (MODE PEINT — STUDIO ANIME SEINEN N&B DÉCORS ATTÉNUÉS)

> Vertical 9:16, dark seinen anime cel-shaded illustration in strict BLACK AND WHITE monochrome (pure black ink, stark white highlights, muted charcoal grey tones, zero color), same anime protagonist and style as the reference image, with an attenuated muted background.
> Scene: In the upper frame (above y 560, head fully inside the frame), the same Black male anime protagonist with short stylized locks and closed high-collar black coat has a <expression faciale précise>. Behind him, an ATTENUATED, darkened, low-contrast charcoal background of <décor adapté au vers>.
> Palette: strictly black and white — deep jet black #050608, stark pure white #FFFFFF, soft attenuated charcoal grey #2A2E35 in the background.
> In the middle band over a deep black ink brushstroke, paint two lines of white serif capital letters:
> First line in large white capitals: "<LIGNE 1>"
> Second line below it in smaller silver-white capitals: "<LIGNE 2>" (include every accent mark: <lister les diacritiques>).
> Below the text (around y 1200, above y 1500), 2 white ink line-art sticker icons: <icône 1> and <icône 2>. A thin luminous white ink thread crosses the frame.
> Text between y 620 and y 1340, centred, max 740 px wide, never over the face, nothing in top 144 px, nothing below y 1574. No flag, no logo, no other text.

---

## 16 — Historique

- **v6.0** (2026-10-21) — « WTBW Salut & Stickers Doux » : suppression définitive du système de code de fin et de l'accroche « Regarde jusqu'à la fin pour voir le code » ; nouvel accueil en 2 temps « Salut · Wolof TechStein beat wê (WTBW) » et nouvelle carte finale WTBW animés avec 3 stickers vectoriels fluides et doux (`LIKE LA VIDÉO`, `CLIQUE SUR + POUR T'ABONNER`, `COMMENTE SI TU AIMES !`) ; clochettes CTA mises à jour en mode WTBW (`CLIQUE SUR +` / `LIKE & PARTAGE` / `Commente si tu aimes · WTBW`) ; recette « STUDIO ANIME SEINEN — Noir & Blanc, décors atténués & expressions multiples » ; note anti-`ONLY:` dans les prompts courts. Validé sur : `productions/goinfres/` (36 plans, 47 vers, clip 6 838 frames / 227,933 s, −14,0 LUFS, blackdetect 0, faststart OK).
- **v5.9** (2026-10-14) — « Ça bouge, sans voiler la parole » : question §0 obligatoire, mouvement par fenêtre glissante sur source 110 %, état éteint, grain 4 variantes cyclées, vignette masque L. Validé sur : `productions/mahu-ti-te-gbe/` et `productions/on-est-reel/`.

**Signature :** « Wolof TechStein beat wê ! » (WTBW) ⚡
