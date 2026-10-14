# PROMPT UNIVERSEL DE PRODUCTION LYRICS — v5.9 « ÇA BOUGE, SANS VOILER LA PAROLE »

Mise à jour : **2026-10-14**. Document **auto-suffisant** : il absorbe v5.7 « Mariage parfait » (jamais commité, donc
non téléchargeable), v5.8 « Typo peinte » et le moteur réel de `productions/mahu-ti-te-gbe/`. Tous les chiffres
ci-dessous sont **mesurés sur des fichiers livrés**, pas des intentions.

---

## 0 — LA QUESTION À POSER AVANT TOUT (obligatoire, premier message du agent)

Avant de générer quoi que ce soit, demander à l'artiste, en une phrase :

> **« Tu veux les paroles en DÉFILEMENT (texte posé par le montage, qui défile mot à mot) ou DÉJÀ PEINTES DANS
> L'IMAGE (le modèle écrit la parole dans la matière de chaque visuel) ? »**

- L'artiste ne répond pas → **MODE PEINT** par défaut (c'est le mode validé sur « Mahu ti tè gbè »), et le dire dans la réponse.
- Il répond « défilant » → **MODE DÉFILEMENT**.
- Il répond « les deux » → **MODE PEINT** pour les visuels, et incrustation réservée aux cartes + mots-clés.

| | **MODE PEINT** (validé) | **MODE DÉFILEMENT** |
|---|---|---|
| Texte à l'écran | écrit **dans l'image** par le générateur ; le montage n'incruste **aucune** typo hors cartes | calque PIL, bloc centré ≤ 740 px, **mot actif en or**, crème pour le reste |
| Icônes / stickers | **autorisés et voulus**, 1 à 3 par image, dorés, touchés par la lumière de la scène | **interdits dans l'œuvre** : zone basse réservée au sous-titre |
| Nombre de plans | **1 plan par vers** (49 vers → 49 plans, ou N blocs + variantes dédiées) | 1 plan par bloc de 2–3 vers |
| Accentuation | aucune sur-typo ; le gras est déjà dans la peinture | halo or 3 px + `spaced()` lettrage espacé |
| Durée d'affichage | temps du vers, **puis le plan s'éteint** (§5.4) | temps du vers, mot à mot |
| Zones sûres | écrites **dans le prompt de génération** (§3) | imposées au calque (§3) |

Le choix est **verrouillé pour toute la prod** : pas de mélange entre vers, jamais.

---

## 1 — Hiérarchie des demandes (rappel permanent)

1. Demande explicite actuelle de l'artiste. 2. Configuration validée de la prod (ancre, personnages, titre exact, code).
3. v5.9 (ce document). 4. v5.8, puis v5.7, v5.6, v5.5 pour ce qui n'est pas contredit.
États à tenir séparés et nommés : **proposé / généré / validé par l'artiste / rendu / contrôlé**.
**Jamais** inventer : validation de l'artiste, hash publié, mesure, fichier final, « à peu près ».

---

## 2 — Paramètres de la prod (bloc à remplir à chaque chanson)

```
TITRE        : …                      (recopié EXACTEMENT, accents compris)
ARTISTE      : …                      (signature d'écran, ex. « Dsky »)
LANGUES      : …                      (mixte = le dire au générateur : « fon + anglais »)
PAROLES      : chemin/fichier.txt     (49 lignes = 49 vers, horodatages de l'artiste non retouchés)
AUDIO        : chemin/fichier.mp3     (maître fourni par l'artiste, jamais généré)
RECETTE      : ENCRE & FEUILLE D'OR | AUBE CLOCHETTES | STUDIO ANIME SEINEN | <nouvelle>
CODE DE FIN  : … (4 chiffres, lié à la durée : 3 min 26 s → 0326)
SIGNATURE    : « Wolof TechStein beat wê ! »
MODE         : PEINT (défaut) | DÉFILEMENT      ← réponse à la question §0
DOSSIER      : productions/<slug>/               (fonds/ livrables/ fonts/ + verses_map.json + CARTE-VERS.md)
```

---

## 3 — Zones sûres 1080×1920 (à recopier dans CHAQUE prompt d'image)

- rien dans les **144 premiers pixels** en haut (marge de sécurité : la règle d'or dit 140) ;
- rien à droite de **x ≥ 910** entre **y 960 et y 1690** (zone bouton + pavé de commentaire TikTok) ;
- rien en dessous de **y = 1574** ;
- bloc de texte **centré, largeur ≤ 740 px**, dans la bande **y 620 → 1340** ;
- la typo **ne couvre jamais un visage** : si elle touche la bouche, le plan est soit limité à ≤ 3 s au montage, soit régénéré ;
- **jamais de drapeau, jamais de bannière, jamais de contact/lien/logo** dans l'image ;
- sortie native du générateur = 768×1376 → passage à 1080×1920 **ancré en HAUT**, rognage du bas : **le crâne n'est
  jamais coupé** ;
- tenues fermées et élégantes, visage dégagé, aucune nudité, personnages fictifs uniquement.

---

## 4 — Orthographe : règle + droit de retouche exceptionnel

- recopier le vers **exact** dans le prompt, entre guillemets, avec « écris exactement, sans faute, avec les accents » ;
- **nommer les diacritiques** si la langue en porte (`TÈ`, `GBÈ`, `WÊ`, `Ñ`, `Ŋ`) et les exiger 2 fois (une fois dans
  la consigne, une fois en listing lettre à lettre si le plan les rate) ;
- relire chaque plan sur une **contact sheet ≥ 480 px de large** (sinon les fautes passent) ; un doute = **crop pleine
  résolution avec grille de 16 px** et lecture du crop, jamais du thumbnail ;
- texte faux sur une lettre → **régénérer une fois avec un prompt court** (le modèle échoue plus sur les prompts longs) ;
- **retouche exceptionnelle** (validée sur `v-152-10` de la prod « Mahu ti tè gbè ») : si, après 2 échecs de
  génération, il ne manque **qu'un diacritique**, il est permis de le combler en **copiant le glyphe déjà peint par le
  modèle dans la même image** (patch ≤ 30 px, masque = pixels de la couleur du glyphe uniquement, MaxFilter 3 + flou
  0,9), jamais en recomposant un caractère à la police. Cette retouche doit être **déclarée** dans la livraison.
- un plan qui échoue à la génération (réponse sans image, `STOP`, `MAX_TOKENS`) = **échec consigné**, jamais compté comme livré.

---

## 5 — MOUVEMENT : animer sans voiler la parole (le cœur de v5.9)

**Principe : l'image vit, le mot reste lisible. Le mouvement est une fenêtre qui glisse, jamais une échelle qui change.**

### 5.1 Préparation (une fois par plan)
- `SC = 1.10` : le plan 768×1376 est agrandi à **110 %** (≈ 1188×2132) en LANCZOS, puis on garde **deux** images en cache :
  la nette et la « éteinte » (§5.4). Marge disponible : **108 px en x, 212 px en y**.
- **Aucun resize par frame** : c'est ce qui tuait la version 1 du rendu — `Image.blend(base, zoom, u)` entre deux
  échelles **double les lettres** de la typo peinte (ghosting visible au zoom 1:1, invisible en miniature).

### 5.2 Le travelling
- la frame = `big.cropfenêtre 1080×1920 dont l'origine glisse` de `(ax0,ay0)` à `(ax1,ay1)` selon l'avancement `u` du vers ;
- **4 trajectoires**, alternées par parité de segment (parité de l'indice du segment sur la liste complète, cartes comprises),
  pour que l'œil ne devine jamais le rythme :
  `(0.0→1.0, 0.02→0.98)` · `(1.0→0.0, 0.02→0.98)` · `(0.18→0.82, 0.98→0.02)` · `(0.82→0.18, 0.02→0.98)` ;
- **1 travelling = 1 vers**, jamais plus vite que la lecture : durée du travelling = durée du vers ;
- amplitude **plafonnée à la marge** (§5.1) : on ne découvre jamais de bord noir, on ne recadre pas la bande de texte
  peinte y 620→1340 ;
- **les cartes ne bougent pas** (flou + scrim fixes) : ce sont des plaques de titre, leur immobilité est voulue ;
- pas de rotation, pas de parallaxe multi-couches, pas de shake, pas de zoom-in brutal : tout ce qui fait *trembler*
  une lettre peinte est interdit.

### 5.3 Transitions
- `xfade` (fondu enchaîné) de **0,35 s** uniquement **entre deux plans** ;
- aucun effet à l'intérieur d'un plan pendant les **1,2 premières s** (temps d'attaque de la lecture) ;
- la transition ne doit jamais durer sur deux vers chantés en même temps.

### 5.4 État « éteint » d'un vers déjà lu
- quand le vers a fini de s'afficher (`disp`) mais que son plan court encore (respiration instrumentale), le plan
  passe à **`Brightness 0.40` + `GaussianBlur 2`** en **fondu de 0,35 s**, sur **la même fenêtre** que l'image nette :
  `Image.blend(nette, eteinte, g)` avec `g = (t − disp)/0.35`. Comme l'échelle est identique, il n'y a pas de ghosting.
- le plan revient à fond (nette, luminosité 1.0) dès le vers suivant.

### 5.5 Grain et vignette (les deux pièges à connaître)
- **vignette** = masque `L` centré (0 au centre, ≈ 86 aux coins, flou 34) composite d'une couleur `#040A12` :
  `Image.composite(noir, cur, masque)`. **Jamais** `Image.blend(cur, image_sombre, k)` → ça noie l'image (défaut réel
  du premier rendu de la prod).
- **grain 35 mm** = **4 variantes pré-calculées, cyclées** (`grains[k % 4]`, seed fixe) en composite sur
  `Brightness 1.09`. **Jamais** `if k % 3 == 0` : ça produit un stroboscope alterné vide/plein.

### 5.6 Calage
- si l'artiste fournit des horodatages (`.lrc` / txt chronométré) : les **garder tels quels**, ne jamais recalculer sa
  voix ; durée du clip = durée **décodée** de l'audio (`ffmpeg -map 0:a:0 -f null -`), pas celle annoncée par le fichier.
- formule d'affichage par vers, en l'absence de calage mot à mot :
  `affichage = min(fin_vers, début_vers + max(2.2 s, 0.30 s × nombre_de_mots))`, plafonnée à la fin du vers.
  La signaler comme **provisoire** dans la livraison.

---

## 6 — Clochettes / CTA (fenêtres, géométrie, interdits)

- **Fenêtre = temps sans parole en cours de lecture**, donc `[fin d'affichage du vers + 0,15 s → début du vers
  suivant]`, et seuil **4,0 s** en MODE PEINT (5,0 s en MODE DÉFILEMENT : la typo incrustée, elle, s'efface vraiment).
  Les fenêtres « brutes » calculées seulement sur les temps de vers sont **fausses** : elles tombent sur un vers en
  cours d'affichage et empâtent la typo peinte (défaut réel, corrigé en production).
- **jamais** de CTA sur les cartes d'accueil, ni pendant un vers lu.
- Tile **720×720 centré sur x=540, posé en y 620→1340** → n'empiète donc sur aucune zone sûre.
- **Plaque** : `rounded_rectangle([34,8,686,712], radius 54, fill (7,13,21,158), outline or α 70)` + flou 5,
  composite **sous** les éléments : c'est elle qui neutralise la parole peinte pendant le CTA.
- Cloche **dessinée** (pas de photo, pas d'emoji) : silhouette en dégradé or→bronze, **36 angles** de balancement
  supersamplés ×3, pendule `±12°` amortie sur une période `BELL = 4,0 s`, halo `GaussianBlur 18` α 46, 2 ondes
  concentriques (période 0,9 s), 3 étincelles, flèche clignotante vers la cloche.
- Texte : **Montserrat obligatoire**, jamais de cursive pour un CTA → `ABONNE-TOI` 62 px blanc→bleu pâle espacé de
  7 px, pilule `PARTAGE` 360×96 dégradé cyan→magenta, rappel « Clique sur la cloche, puis PARTAGE » 34 px crème.
  Compter les pixels du `PARTAGE` final : c'est lui qui doit rester sous 910 px de large.
- Entrée/sortie en **fondu 0,35 s** aux deux bouts de la fenêtre.

---

## 7 — Habillage permanent (cartes, badge, progression)

- **Carte d'accueil ≈ 5 s + 5 s** (2 temps) : « Regarde jusqu'à la fin » + `(durée, c'est le code)` puis
  « pour découvrir comment proposer un son ou des lyrics à réaliser pour toi ! ».
- **Carte finale 5,00 s après la fin de la chanson** : « Merci d'avoir regardé » + « Tu veux un son ou des lyrics à
  réaliser pour toi ? » + « Commente le code » + **code 210 px** en or. **Aucun contact, aucun lien, aucun logo.**
- Fabrication des cartes : fond = plan du 1er vers (accueil) / du dernier (finale), `GaussianBlur 9`,
  `Brightness 0.74`, `Color 1.06`, scrim `#0B1B2A` α **118**, filet or (170→910) au-dessus et au-dessous du bloc,
  `head` 40 px or, tailles de lignes 88 / 54 / 96 / 46 / 40 / 210, et **auto-réduction de la police tant que la ligne
  dépasse 740 px** (`fit()`), halo or 3 px sur les très gros titres.
- **Badge artiste** : « Dsky » (ou l'artiste) **en y = 160**, Montserrat ExtraBold 44, **un seul fondu de 0,4 s par
  vers**, α max **0,72** (≤ 75 %), soulignement or 3 px, **liseré sombre** 5 offset (6,12,20 α 0,72·α) pour rester
  lisible sur un ciel clair. **Jamais permanent**, jamais pendant les cartes, jamais pendant un CTA.
- **Filet de progression** : y = **1560**, x **170→910**, fond crème α 46 de 4 px, partie or α 205 de 8 px,
  `fr = (t − début_du_1er_vers) / (fin_chanson − début_1er_vers)`.

---

## 8 — Recettes de style (une seule par chanson, recopiée mot pour mot)

- **ENCRE & FEUILLE D'OR — « la nuit qui finit bien »** *(validée 34 plans / 49 vers, sans un seul texte faux non déclaré)* :
  peinture numérique matière épaisse, clair-obscur Rembrandt à source unique, pluie/vapeur, grain 35 mm, filets d'or
  sur tout ce qui est divin, palette bleu nuit `#0B1B2A` / teal / ambre `#E8A33D` / or `#D9A441` / crème `#F3E7D3` ;
  capitales d'or serif condensée pour le vers, mot actif en or vif, reste crème ; stickers dorés collés au sens du mot
  (lanterne = lumière, colombe = souffle, main = porter, vague = miséricorde, cœur = tenir).
- **AUBE CLOCHETTES** *(v5.6)* : fonds clairs, CTA premium, punchlines motivées courtes.
- **STUDIO ANIME SEINEN** *(validée sur « Gbètché vivi »)* : cel-shading dur, contours épais, storytelling rue/adrénaline.

## 9 — Continuité entre plans

- même lieu, même heure, même intensité de pluie : l'arc avance par paliers (nuit → crachin → brume → **aube**) ;
- le plan `n+1` reprend la **position** du personnage dans le plan `n` (même bord de cadre, même appui au sol) ;
- un motif traverse les plans (fil de lumière dorée, colombe, pastille du code) ;
- motion blur **uniquement** sur les plans d'action (chute, cri, tirage), jamais sur un gros plan de visage ;
- **pas de retour en arrière de la lumière** : une reprise arrivée après l'aube garde une **variante aube dédiée**
  (3 variantes `v-160-26`, `v-163-62`, `v-166-97` créées pour ça, plutôt qu'un retour à la scène de nuit).

---

## 10 — Méthode de fabrication (salves, ancre, contrôle)

1. **Ancre d'abord** : générer 1 image, la valider à l'œil avec l'artiste, la figer (`fonds/scene-01-ancre.png` +
   `ANCRE.md`). Elle sert de `images=[…]` de référence de style à **toutes** les salves.
2. **Salves ≤ 10 images par tour** (limite plateforme) ; consigner chaque tour : demandées / réussies / échouées.
3. `verses_map.json` = contrat unique entre les paroles et les visuels, un objet par vers :
   `{i, t, fin, affichage_s, texte, image, disponible, reprise}` + `plans_distinctes`, `plans_disponibles`,
   `plans_manquantes`, `fenetres_clochettes`, `regle_clochettes`, `code`, `duree_decodee_s`.
   `disponible` est **recalculé avec `os.path.exists`**, jamais saisi à la main.
4. `CARTE-VERS.md` générée depuis le JSON (jamais écrite à la main : elle dérive).
5. QC visuel : contact sheet de la salve, **puis** contact sheet des frames du rendu, **puis** zoom 1:1 sur la typo
   d'un frame de rendu (c'est lui qui révèle le ghosting).

---

## 11 — Audio (maître de l'artiste, jamais généré)

- mesurer **avant** de promettre : crête, LUFS, silence. Écrêtage source (+0,06 dBTP constaté) → `loudnorm` **2 passes**
  `I=-14:TP=-1.5:LRA=11`, résample 48 kHz, `libmp3lame -q:0`, puis **`-vn` obligatoire** (tuer la pochette héritée),
  ID3 `TIT2/TALB/TPE1/TPE2/TCON` + `APIC` 1080² + `USLT` propre (sans horodatages) + `TXXX` SIGNATURE/MASTER/IA ;
  relire les tags après écriture.
- pour le clip : `apad=pad_dur=<carte finale>` sur le maître, AAC 256k 48 kHz. **Ajouter `-map 0:a:0`** sinon ffmpeg
  voit l'APIC jointe au MP3, croit devoir encoder du h264 dans le `.m4a` et échoue.

## 12 — Encodage et contrôles obligatoires du rendu

- `libx264 -preset veryfast -crf 24 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709
  -movflags +faststart` (archive max : `--crf 18 --preset slow`, ~2,5× tout).
- pipe `rawvideo` `rgb24` 1080×1920@30 → un seul passage ; la frame count `n = round(t_end × fps)`.
- **Contrôles à publier avec les chiffres réels** :
  | contrôle | commande | attendu |
  |---|---|---|
  | durée | `ffmpeg -i` | = `frames/fps` à 0,01 s près |
  | frames noires | `blackdetect=d=0.05:pix_th=0.10` | **0** |
  | gel | `freezedetect=n=-33dB:d=2.5` | 0 sur les vers ; les cartes et les CTA sur image fixe sont signalés **et assumés** |
  | loudness | `ebur128` | −14,0 LUFS |
  | crête | `astats` | ≤ −1,0 dB |
  | faststart | octets | `moov` avant `mdat` |
  | typo | zoom 1:1 d'un frame | nette, **aucun doublement de lettre** |

---

## 13 — Git et livraison (format jamais négociable)

- commit + push **après chaque étape**, uniquement sur la **branche de la session** ; jamais de `git reset --hard`
  automatique ; après un wipe du sandbox : `git fetch` + `git reset --mixed` + **`git checkout-index -a -f`** ;
  dépendances recréées via venv (`imageio-ffmpeg mutagen pillow numpy`), polices **versionnées** dans le dépôt.
- **toute** réponse de livraison contient, dans cet ordre :
  **1)** Titre · **2)** Captions · **3)** Hashtags (13 max) · **4)** le fichier 9:16 (présenté à l'utilisateur) ·
  **5)** Déclaration IA (visuels OUI / audio NON) · **6)** commandes Termux, **une ligne par fichier, séparées par
  `;`**, sur le hash du commit **après le push** (vérifié avec `git ls-remote` + taille du blob via API), et le détail
  des contrôles.
- `raw/<hash>/` renvoie un 302 vers `media.githubusercontent.com` (bloqué dans le sandbox) : **ne jamais** conclure à
  un lien mort depuis le sandbox, vérifier la taille du blob par l'API à la place.

## 14 — Interdits permanents

Drapeau, bannière nationale · contact, lien, QR, logo dans une image · nudité, anatomie exhibée, caméra sur les
parties du corps (**annulent les points 11–13 de `Instructions A.txt`**) · photo personnelle envoyée au générateur
sans autorisation écrite · cursive sur un CTA · calque typo par-dessus la typo peinte · horodatages de l'artiste
modifiés · « à peu près », validation inventée, hash non poussé présenté comme livré.

---

## 15 — Gabarit de prompt d'image (MODE PEINT) — à recopier pour chaque vers

> Vertical 9:16, cinematic painted illustration, same style as the reference image.
> Scene: <lieu, heure, météo, posture et position du personnage identiques au plan précédent>.
> Palette: deep night blue #0B1B2A, teal shadows, amber #E8A33D key light, gold #D9A441, cream #F3E7D3.
> Hand-painted serif gold capitals in the middle band read EXACTLY: "<VERS>" — copy the letters exactly, including
> every accent mark (<lister les caractères accentués, ex. È deux fois>). Below it a smaller cream line: "<suite>".
> 1 to 3 gold sticker icons glued to the meaning: <icônes>. A <motif récurrent> crosses the frame.
> Text must sit between y 620 and y 1340, centred, max 740 px wide, never over the face, nothing in the top 144 px,
> nothing right of x 910 between y 960 and 1690, nothing below y 1574. No flag, no banner, no watermark, no logo,
> no contact, no other letters anywhere, closed elegant clothing, face visible. Head fully inside the frame.

## 16 — Historique

- **v5.9** (2026-10-14) — « Ça bouge, sans voiler la parole » : question §0 obligatoire (défilant / peint), chapitre
  mouvement complet (source à 110 %, fenêtre glissante, 4 trajectoires, état éteint, pièges vignette et grain), seuil
  de clochette recalculé sur le temps **libre** 4,0 s, auto-réduction de police sur les cartes, liseré du badge,
  droit de retouche d'un seul diacritique par copie du glyphe peint, contrôles de rendu chiffrés, `-map 0:a:0` à l'audio,
  3 variantes aube pour la continuité lumière, note sur v5.7 jamais commité. Validé sur : `productions/mahu-ti-te-gbe/`
  (34 plans, 49 vers, clip 6 342 frames / 211,40 s, −14,0 LUFS, blackdetect 0, faststart).
- **v5.8** (2026-10-10) — typo peinte par le modèle, 1 plan par vers, zones sûres dans le prompt, `-vn` + ID3.
- **v5.7** (2026-10-10) — Mariage parfait : badge sans drapeau, cartes sans contact, code de fin, clochettes premium
  *(jamais commitée : ses règles sont intégrées ici)*.
- **v5.6** (2026-10-05) — clochettes CTA, Aube Sacrée. **v5.5** (2026-09-30) — hybride, Termux une ligne par fichier.

**Signature :** « Wolof TechStein beat wê ! » ⚡
