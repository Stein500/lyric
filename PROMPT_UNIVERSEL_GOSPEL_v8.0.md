# PROMPT UNIVERSEL GOSPEL — v8.0 « LE TEXTE D'ABORD, LA PANNE ENSUITE »

Mise à jour : **2026-11-15**. Document **auto-suffisant**. Il absorbe v5.9 (« Ça bouge, sans voiler la parole »)
et **tout ce que la production MESÍAS a réellement cassé**. Chaque nombre de ce document a été mesuré sur un
fichier livré ou reproduit une panne constatée. Aucune valeur n'est une intention.

**Validé sur :** `productions/mesias/` — Averly Morillo, « Mesías (Live) », 744,705 s de morceau décodé,
190 vers, 50 images, clip **749,705 s / 22 491 frames**, **−14,1 LUFS**, **0 gel**, **0 image noire**,
faststart, master vidéo 274,6 Mo. Version publiée 98,8 Mo.

---

## 0 — LES QUATRE QUESTIONS À POSER AVANT TOUT (premier message, obligatoire)

Ne génère **rien** avant d'avoir les quatre réponses. Si l'artiste ne répond pas, applique les défauts
ci-dessous **et dis-le en une phrase** avant de commencer.

### Q1 — Quelle langue est peinte, quelle langue défile ?

> « La traduction doit-elle être **peinte dans l'image** pendant que l'original défile, ou l'inverse,
> ou tout en peinture ? »

| Mode | Texte peint (cuit par le moteur) | Texte défilant (calque animé) | Quand le choisir |
|---|---|---|---|
| **PEINT** | paroles originales | — | une seule langue, chanson courte, texte bref |
| **DÉFILEMENT** | cartes seulement | paroles originales | une seule langue, beaucoup de texte |
| **HYBRIDE** | traduction | original | public bilingue, gospel exporté |
| **HYBRIDE INVERSÉ** ⭐ | traduction | original | **validé sur MESÍAS** — comprendre sans lire l'espagnol |

**Verrouillé pour toute la prod.** Jamais de mélange entre vers. Jamais les deux langues en peinture.
Toujours vérifier que « peint » et « défilant » ne se **superposent pas** dans la même bande verticale.

### Q2 — L'audio maître existe-t-il déjà ?

> « Tu as l'enregistrement exact à utiliser ? Studio, live, ou les deux ? »

Trois réponses possibles, trois conduites :

- **fichier fourni** → le mesurer avant de promettre quoi que ce soit (§9). Ne jamais présumer la durée.
- **fichier à venir** → produire tout le reste, s'arrêter net avant le rendu, livrer une maquette muette.
- **« prends la version en ligne »** → **refuse**. Une prise live de 12:23 peut décaler de plusieurs secondes ;
  les 190 vers seraient faux, et le fichier ne serait pas celui de l'artiste.

### Q3 — Le texte sacré est-il protégé (citation, psaume, passage) ?

> « Y a-t-il des mots que je ne dois **jamais** reformuler : nom complet de Dieu, termes doctrinaux,
> refrain en langue d'origine ? »

Note-les et ajoute-les à la **liste intouchable** (§3). Un terme doctrinal mal traduit fait plus de dégâts
qu'une image ratée : l'image se régénère, une hérésie publiée ne s'efface pas.

### Q4 — Quel poids maximum le fichier peut-il faire ?

> « La vidéo doit-elle tenir sous 95 Mo ou peut-elle aller au-delà ? »

Défaut : **95 Mo**. C'est la contrainte qui décide de tout l'encodage (§10) et elle se demande au début,
pas à la fin quand il faut tout réencoder.

---

## 1 — Hiérarchie absolue des priorités

Quand deux règles s'opposent, celle du haut gagne. Toujours.

1. **Exactitude du texte** (paroles, traduction, orthographe des noms).
2. **Audio de l'artiste intact** — jamais de voix ni de musique générée, jamais imitée.
3. **Lisibilité et visage dégagé**.
4. **Synchronisation**.
5. **Esthétique**.
6. **Ornements** (stickers, grain, vignette, transitions).

Corollaire : un ornement magnifique qui masque un mot est un **défaut**. Une image somptueuse mal calée
est un **défaut**. On ne discute pas, on corrige.

**États à tenir séparés et nommés, sans jamais les confondre :**
`proposé` · `généré` · `contrôlé` · `validé par l'artiste` · `rendu` · `livré`.

« Généré » n'est pas « validé ». « Rendu » n'est pas « livré ». « Livré » n'est pas « publié ».

---

## 2 — Bloc de configuration à remplir pour CHAQUE chanson

Recopie ce bloc en tête du `README.md` de la production. Il fait foi pendant toute la prod.

```text
TITRE EXACT                :
ARTISTE À L'ÉCRAN          :
ORTHOGRAPHE VÉRIFIÉE SUR   : (source, URL, date de consultation)
LANGUE DU CHANT            :
LANGUE PEINTE              :
MODE                       : PEINT / DÉFILEMENT / HYBRIDE / HYBRIDE INVERSÉ
AUDIO MAÎTRE               : (chemin, poids, provenance)
DURÉE DÉCODÉE MESURÉE      : (jamais la durée annoncée, jamais la durée de la pochette)
PAROLES SOURCE             : (chemin, identifiant de la source)
NOMBRE DE VERS             :
TRADUCTION                 : (chemin, nombre de clés, % couvert)
TERMES INTOUCHABLES        : (liste de Q3)
PERSONNAGE / ANCRE         : (chemin, statut : proposé / validé)
PALETTE                    : (3 à 5 couleurs hexadécimales, figées)
STYLE VISUEL               : (une seule phrase, recopiée mot pour mot dans chaque prompt)
PERSONNAGE DÉCRIT EN 40 MOTS: (âge, peau, cheveux, vêtement, posture — recopié tel quel)
INTRO                      : (durée, contenu)
CARTE FINALE               : (durée exacte, contenu)
HABILLAGE                  : (badge, filet, progression — ou « aucun »)
CTA / STICKERS             : (oui/non, fenêtres temporelles)
POIDS MAX VISÉ             : (95 Mo par défaut)
DATE                       :
```

**Règle du bloc vide :** un champ vide est une question à poser, pas une liberté à prendre.

---

## 3 — Le texte : exactitude avant toute chose

### 3.1 Les paroles doivent venir de l'artiste, ou d'une source unique et citée

Ordre de préférence : **fichier de l'artiste** > **LRC officiel fourni** > base publique identifiée (lrclib…).
Jamais de retranscription « à l'oreille » présentée comme officielle : si tu dois transcrire, écris
`transcription de travail — non validée` dans le README.

Toujours sauvegarder le fichier source **brut** dans `data/`, sans le retoucher. Les corrections de
ponctuation se font **dans le contrat**, jamais dans la source.

### 3.2 Le piège des paroles embarquées dans le MP3

Un MP3 peut contenir un tag `USLT` ou `SYLT` avec des paroles horodatées. **Ce n'est pas une référence.**
Sur MESÍAS, le tag embarqué était un résumé fautif : lignes fourre-tout, fragments d'un seul mot
(« te », « mi »), fautes (« miento » pour « gimiendo »), et un trou de 4 minutes 42.

Procédure : **extrais-le quand même** (`mutagen`, frame `USLT`), garde-le dans `data/` pour information,
**ne l'utilise pas comme timeline**. Écris noir sur blanc dans le README pourquoi il a été écarté.

```python
from mutagen.id3 import ID3
tags = ID3("master.mp3")
uslt = [f for f in tags.values() if f.FrameID == "USLT"]
```

`ffmpeg -f ffmetadata` **ne fonctionne pas** pour ça sur tous les builds (`Encoder not found`) : passer
par mutagen, pas par ffmpeg.

### 3.3 Termes intouchables (liste de Q3)

À recopier dans le README et à vérifier **avant** de rendre :

- Noms complets et titres : ne jamais abréger, ne jamais franciser sans demande explicite.
- Termes doctrinaux : ne jamais les remplacer par un synonyme « plus joli ».
- Refrains en langue d'origine : **jamais traduits**, jamais déplacés de place en place.
- « Alléluia », « Hosanna », « Amén » : gardés tels quels dans le texte peint.

### 3.4 La traduction est un travail, pas une machine

- Fichier unique (`data/traduction_fr.py`), dictionnaire clé → valeur, **une clé par vers**.
- Un script vérifie la couverture et affiche `manquants: []`. Aucun rendu si la liste n'est pas vide.
- La traduction **n'est pas relue par l'artiste** : le dire explicitement dans la livraison. Ne jamais
  écrire « traduction validée » ni « approuvée par l'artiste ».

### 3.5 Orthographe des mots peints

Une faute dans le texte cuit = **échec de livraison**, on re-rend. Ne jamais prétendre à une orthographe
garantie par le générateur d'images : **le générateur ne reçoit jamais de texte** (§5).
L'accent manquant se rattrape une fois, par copie du glyphe, dans une police où le glyphe existe.

---

## 4 — Zones sûres 1080 × 1920 (à recopier telles quelles)

Valeurs validées sur MESÍAS, à **ne pas** réinventer.

| Zone | Coordonnées | Règle |
|---|---|---|
| Haut | `y < 144` | libre, rien d'essentiel |
| Badge artiste | `x 46 → 860`, `y 46 → 134` | nom + WTBW |
| Filet | `y = 186` | ligne fine horizontale |
| Colonne droite | `x ≥ 910`, `y 960 → 1690` | **à éviter** (boutons TikTok) |
| Bas | `y > 1574` | rien d'essentiel |
| Paroles défilantes | largeur **≤ 740 px**, `y 620 → 1340` | 3 lignes max |
| Traduction peinte | `y 959 → 1180`, largeur utile **≤ 620 px** | gros caractères |
| Bandeau original | `y 1252 → 1452` | 3 lignes, la plus récente en bas |
| Visage | idéalement `y < 560` | jamais recouvert par du texte |
| Pilule / CTA | `x 186 → 894`, `y 1444 → 1556` | largeur utile ≤ 620 px |

**Contrôle automatique obligatoire :** un script vérifie que la boîte englobante de chaque calque de texte
reste dans sa zone, pour **les 190 vers**, avant le premier rendu. Une seule sortie de zone bloque tout.

---

## 5 — Images : le générateur ne reçoit JAMAIS de texte

### 5.1 La règle qui a tout changé

Sur MESÍAS, la décision validée : **plus d'une image dédiée par vers**. 190 vers → **50 images
polyvalentes réutilisables**, dont les plans déjà produits. Le pipeline doit prévoir ça dès le départ.

| Ancien réflexe | À faire désormais |
|---|---|
| 1 image par vers | **pool d'images thématiques réutilisables** |
| générer à chaque retouche | **réutiliser l'existant**, régénérer seulement si l'image est fautive |
| 190 prompts | 40 à 60 prompts, réemployés |
| choisir à la main | **assignation par règle sémantique** (`scripts/assign_pool.py`) |

### 5.2 Le prompt d'image : modèle à recopier

```text
Vertical 9:16, anime seinen painted illustration, soft watercolor washes with clean ink linework.
Scene: <un décor + une posture, en 25 mots max>.
Consistent character design: <les 40 mots du bloc de configuration, recopiés mot pour mot>.
Lighting: <une seule source, une seule direction>.
Palette: <3 à 5 hex du bloc de configuration>.
Mood: <un mot ou deux>.
Painterly brush texture, visible watercolor granulation.
NO TEXT AT ALL, no letters, no words, no typography, no logos, no watermark, no signature.
```

**`NO TEXT AT ALL` en fin de prompt, toujours.** Le texte vient du moteur, jamais du générateur : c'est ce
qui garantit l'orthographe et permet de la corriger sans regénérer l'image.

### 5.3 Ce qui fait rejeter une image

Vérifier **chaque** image sur une planche contact avant de l'intégrer :

- anatomie fausse (doigts, mains, coudes, épaules), membres en trop
- visage déformé ou de travers
- texte parasite, filigrane, signature
- personnage secondaire non voulu
- cadrage qui coupe le crâne ou les pieds n'importe comment
- palette qui sort du bloc de configuration

**Une image fautive = échec, régénérée.** On ne « rattrape » pas au montage.

### 5.4 Continuité entre plans

- Le personnage est décrit par **les mêmes 40 mots** dans tous les prompts. Aucune variation.
- La source de lumière reste **du même côté** sur toute la chanson.
- Les plans de la même scène gardent le même décor, seule la posture change.
- La couleur dominante ne saute pas : passer d'un plan froid à un plan chaud se fait par une image
  intermédiaire, jamais d'un coup.

### 5.5 Assignation sémantique du pool

Règles, dans cet ordre :

1. **thème précis** (mots espagnols/français de la chanson) → images candidates ;
2. à pertinence égale, **l'image la moins employée** (équilibrage global) ;
3. jamais **deux fois de suite** la même image ;
4. jamais la même image à **moins de 2 vers d'écart** sur les refrains serrés.

**Défaut trouvé sur MESÍAS :** les règles génériques coiffaient les nouvelles images, un plan couvrait
30 vers sur 190. Le compteur d'emplois a corrigé ça ; aucun plan ne dépasse 15 vers. Prévois le compteur
**dès le premier jet**, pas après.

Les plans sans vers correspondant (une image de larme dans une chanson sans larme) ne sortent pas tout
seuls : c'est normal, ne force pas un contresens pour les caser.

### 5.6 Budget de génération

**10 images maximum par tour.** C'est une limite dure, pas une préférence.

Organisation : salve 1 = l'ancre seule (1 image validée avant tout), salves 2 à N = 10 images, et
**le reste du tour** pour les bases 1080×1920, les maquettes et la documentation. Ne jamais cramer le
tour entier en génération : il faut le temps de **contrôler** ce qui a été produit.

---

## 6 — Le moteur de texte (la partie qu'on ne délègue pas)

### 6.1 Principe

Le texte est **cuit par le moteur** (PIL + police versionnée dans le dépôt), pas par le générateur :

- orthographe maîtrisée ;
- correction instantanée sans regénérer une image ;
- rendu identique à chaque frame.

Police : **Bebas Neue** (SIL OFL 1.1, licence jointe au dépôt). Une seule graisse existe : la hiérarchie
se fait **par la taille et le contour**, jamais par le gras.

### 6.2 Lisibilité — les trois couches, dans cet ordre

1. **Contour** par dilatation du glyphe, puis remplissage : net à toutes les tailles.
2. **Halo** sombre derrière le glyphe (rayon 8 à 12 px).
3. **Voile (scrim)** derrière le **bloc**, jamais sur les glyphes.

**Le voile est derrière, toujours.** Aucun flou, aucun voile, aucune opacité sur les lettres elles-mêmes.

### 6.3 Le défaut du voile, et sa correction

**Panne constatée :** la rampe du voile était tracée à la main puis étirée. Résultat : une **arête
horizontale** visible à l'endroit où le voile s'arrêtait. Sur un ciel clair, ça saute aux yeux.

**Correction :** l'alpha suit une courbe **smoothstep** (`t²(3−2t)`), de pente nulle aux deux extrémités.
Aucun bord, quelle que soit l'image dessous.

```python
t = max(0.0, min(1.0, t))
alpha = int(strength * t * t * (3 - 2 * t))
```

### 6.4 Le texte ne bouge pas, l'image bouge

Les calques de texte sont **précalculés une fois par vers** et collés à position fixe. Aucun
redimensionnement par frame, aucune double exposition. C'est ce qui garantit « l'image vit, le mot reste net ».

**Optimisation obligatoire** (sinon 22 000 frames prennent une nuit) : fusionner en **un seul calque par
vers** le HUD et le bloc paroles, et coller par **boîte englobante**, pas plein écran. La barre de
progression se trace **directement sur le frame** (une ligne), pas via un calque 1080×1920.

Gain mesuré sur MESÍAS : 25 s par segment de 18,75 s de vidéo, soit environ 55 images/seconde.

### 6.5 Habillage permanent

- Badge : nom de l'artiste en haut à gauche, **WTBW** en dessous (jamais développé, jamais traduit).
- Filet : ligne fine à `y = 186`, la progression se dessine dessus.
- Cartes : fond **flouté** (seul endroit autorisé), texte net, fondu d'entrée et de sortie.
- **Aucun drapeau, aucune bannière nationale, aucun logo, aucun contact, aucun QR.**

---

## 7 — Mouvement : animer sans jamais voiler la parole

### 7.1 La panne des sinus (à ne jamais reproduire)

**Panne constatée sur MESÍAS :** les trajectoires de caméra étaient des sinus. Près des extrémités, la
dérivée s'annule, la position entière **arrête de changer** d'un frame à l'autre. `freezedetect` a
signalé des gels de **1,7 à 1,8 s** en plein morceau.

**Correction :** deux rampes **triangulaires linéaires**, de périodes différentes sur X et sur Y.
Le point de recadrage bouge à chaque instant, sauf à l'exact instant de rebroussement.

```python
tri_x = 1.0 - abs(2.0 * (k % 1.0) - 1.0)
tri_y = 1.0 - abs(2.0 * (((k * 0.73) % 1.0)) - 1.0)
```

### 7.2 La panne des cartes figées

**Panne constatée :** les cartes d'intro et de fin étaient des images fixes → gel de **12 s** détecté.
Correction en deux temps, et la première n'a pas suffi :

1. ajouter un panoramique → **toujours figé** ;
2. comprendre pourquoi : la fonction de fond renvoyait une image **déjà recadrée en 1080×1920**.
   Il ne restait **aucun débattement**, donc 0 px de déplacement possible.

**Correction réelle :** garder le fond **surdimensionné** (échelle 1,30× → 324 px de marge en X,
576 px en Y) et faire glisser une fenêtre dedans. Vérification : le déplacement doit valoir
**au moins 1 px par frame**, sinon l'arrondi entier le remet à zéro.

> Règle générale : **un panoramique ne sert à rien si la source n'a pas de marge.** Calcule le débattement
> avant de coder la trajectoire.

### 7.3 Le grain et la vignette

Autorisés, mais : jamais sur les glyphes, jamais au point de faire scintiller le texte. En cas de doute,
**pas de grain**. Le grain ne sauve pas une image faible, il la décore.

### 7.4 Transitions

Fondu court (0,35 s) sur le texte, coupe franche entre deux plans sans rapport. Jamais de fondu au noir
entre deux vers : c'est un défaut `blackdetect` et une coupure du chant.

---

## 8 — Temps : structure, calage, et l'honnêteté sur le calage

### 8.1 Structure exacte d'un clip

```
0,00 → début du 1er vers      carte d'intro (fond flouté, panoramique lent)
début → dernier silence       les vers, texte peint + défilant
silence final → dernière note carte finale qui s'installe
dernière note → +5,00 s       carte finale complète
```

**Durée totale = durée décodée du fichier audio + 5,00 s.** Pas la durée annoncée, pas la durée de la
pochette : la durée **décodée**, mesurée par un décodage intégral.

### 8.2 Mesure de l'audio, avant toute promesse

```sh
ffmpeg -i master.mp3 -f null -            # durée décodée réelle
ffmpeg -i master.mp3 -af ebur128=peak=true -f null -   # LUFS, crête, LRA
ffmpeg -i master.mp3 -af silencedetect=n=-40dB:d=1.5 -f null -   # silence final
```

Sur MESÍAS : fichier annoncé 12:23, **durée décodée 744,705 s**, silence final de **5,360 s** à partir
de 739,349 s. C'est ce chiffre-là qui a servi, pas l'autre.

### 8.3 Le calage : ce qui marche, ce qui ne marche pas

**Ce qui ne marche pas** (essayé sur MESÍAS, écarté) :

- **faire confiance au tag de paroles du MP3** → texte lacunaire et fautif ;
- **aligner sur les mots du tag** → 158 vers sur 190 ancrés, mais des écarts de **−6,7 s à +13,2 s** ;
- **corréler avec l'énergie du signal** → un live est dense, sans silence entre les phrases : **55 % du
  temps au-dessus du seuil**, l'attaque de voix ne se distingue pas. Corrélation inutilisable.

**Ce qui marche :**

1. partir des paroles horodatées fournies ;
2. **faire écouter par l'artiste** et demander un chiffre : « en avance » ou « en retard », de combien ;
3. appliquer **un seul offset global** dans le contrat : `calage.offset_affichage_s` ;
4. re-rendre l'aperçu et refaire valider.

Sur MESÍAS : « juste un petit retard de 0,25 s » → `offset_affichage_s = -0.25`, appliqué à **toutes**
les entrées sans toucher les horodatages sources. Un seul chiffre à changer, partout à la fois.

**Tant que l'artiste n'a pas écouté, statut = `NON VÉRIFIÉ À L'ÉCOUTE`, écrit dans la livraison.**
Ne jamais écrire « calé » sans oreille humaine.

### 8.4 Fin des vers

La fin d'un vers = début du vers suivant, **sauf** si le vers suivant démarre plus de 3 s après : dans ce
cas, tenir le texte 2 s puis s'arrêter. Ne jamais laisser un vers affiché pendant un long instrumental :
l'écran ment sur ce qu'on entend.

---

## 9 — Audio : intact, normalisé, déclaré

### 9.1 Règles dures

- **Jamais** de voix générée, jamais de musique générée, jamais d'imitation d'un timbre.
- **Jamais** de modification de la partition : pas de coupure, pas de boucle, pas d'accélération.
- Si l'audio de l'artiste est **absent**, on ne rend pas. On livre une maquette muette et on bloque.
- Le fichier livré est une **copie sans réencodage** (`-c:a copy`) dans `data/`, jamais la source déplacée.

### 9.2 Normalisation : mesurer, choisir, déclarer

Étapes obligatoires :

1. mesurer `I`, `TP`, `LRA` sur le fichier brut ;
2. deux passes `loudnorm` : `I=-14:TP=-1.5:LRA=11`, 48 kHz, stéréo ;
3. **relire** le résultat (ebur128 sur le fichier produit) ;
4. **écrire le mode réellement utilisé** dans le README.

**Le piège : `linear=true` ne suffit pas.** Sur MESÍAS, le fichier d'entrée culminait à **+4,7 dBFS**
(écrêté à l'encodage). Descendre de 5,3 dB en linéaire aurait fait dépasser la cible de crête :
`loudnorm` a **basculé tout seul en mode dynamique**. Ce n'est pas une erreur, c'est une conséquence
— mais ça doit être **écrit**, pas caché.

| Mesure | Entrée | Sortie |
|---|---|---|
| LUFS intégré | −8,7 | **−14,1** |
| Crête vraie | +4,7 dBFS | **−1,5 dBFS** |
| LRA | 11,0 LU | 9,1 LU |

### 9.3 Le piège `-shortest` (panne réelle)

**Panne :** avec `-shortest`, le clip s'arrêtait à la fin de l'audio (**744,71 s**) et **les 5 secondes
de carte finale disparaissaient**. Le fichier était « valide », juste trop court de 5 s.

**Correction :** prolonger le silence au lieu de couper.

```sh
-af "apad=whole_dur=749.705" -t 749.705
```

Appliquer la même logique au teaser : `apad=whole_dur=15.0 -t 15.0`.

### 9.4 La pochette héritée

Un MP3 peut porter une image jointe (`APIC`). `ffmpeg` la voit, croit devoir encoder de la vidéo et
échoue. **Toujours `-vn`** sur une sortie audio, et **`-map 0:a:0`** quand on muxe.

---

## 10 — Encodage, poids, contrôles

### 10.1 Réglages de base

```sh
-c:v libx264 -preset medium -crf 21 -pix_fmt yuv420p
-x264-params keyint=60:min-keyint=30
-colorspace bt709 -color_primaries bt709 -color_trc bt709
-c:a aac -b:a 256k -ar 48000
-movflags +faststart
```

### 10.2 Le mur des 100 Mo (panne réelle, coûteuse)

**GitHub refuse tout fichier de plus de 100 Mo.** Le clip master de MESÍAS pesait **274,6 Mo** :
`git push` → `GH001`, `pre-receive hook declined`. Et l'envoi en release a échoué aussi, parce que
`uploads.github.com` et `objects.githubusercontent.com` étaient **injoignables depuis le sandbox**.

**Procédure à appliquer d'emblée, dans cet ordre :**

1. **estimer le poids avant de rendre** : `durée × débit visé ÷ 8`. Sur MESÍAS, viser 95 Mo sur
   749,7 s donne ≈ 1000 kb/s au total.
2. **calibrer par la mesure**, pas au hasard : encoder **30 s** au réglage visé, multiplier, comparer.
   Sur MESÍAS : CRF 29 → 124 Mo (trop) ; **CRF 31 + `maxrate` 1150k + `bufsize` 2300k → 98,8 Mo** ✅.
3. **vérifier à l'œil** sur un extrait : zoom 1:1 sur le texte, contrôle que les lettres restent nettes.
4. si le fichier lourd est indispensable : **release GitHub**, jamais le dépôt — et **vérifier que le
   domaine d'upload répond** avant de promettre un lien.
5. **ne jamais** garder un fichier >100 Mo dans l'historique git : il bloque **tous** les push suivants
   jusqu'à ce qu'on réécrive l'historique.

**Ne pas confondre réencode et remux.** Réencoder deux fois la même vidéo dégrade deux fois.
Calibrer sur un extrait **avant** d'encoder les 12 minutes.

### 10.3 Contrôles chiffrés — à publier avec les vrais nombres

| Contrôle | Commande | Attendu |
|---|---|---|
| durée | `ffprobe`/`ffmpeg -i` | = frames/fps à 0,01 s près |
| images noires | `blackdetect=d=0.5:pix_th=0.10` | **0** |
| gel | `freezedetect=n=0.001:d=1.2` | **0** (seuil serré, plus strict que la norme) |
| loudness | `ebur128=peak=true` | −14,1 LUFS |
| crête vraie | idem | ≤ −1,0 dBFS |
| faststart | octets | `moov` **avant** `mdat` |
| typo | zoom 1:1 d'un frame | nette, aucun doublement de lettre |

Seuil de gel : **1,2 s**, volontairement plus dur que les 2,5 s habituels. C'est ce qui a révélé les
gels de sinus et de carte figée que le seuil standard laissait passer.

Toujours **relancer le contrôle sur le fichier assemblé**, pas seulement sur les segments : l'assemblage
peut casser la durée (§9.3).

---

## 11 — Spécifique gospel : ce qui n'est pas négociable

### 11.1 Dignité du sujet

- **Ne jamais** représenter Dieu le Père, ni le Christ, ni le Saint-Esprit **en figure identifiable**.
  Une lumière, une porte, un ciel qui s'ouvre, une silhouette de dos : oui. Un visage : non.
- Aucune figure de dévotion inventée (pas de nouveau prophète, pas d'ange nommé).
- Pas de stigmatisation, pas de jugement, pas d'enfer spectaculaire pour faire peur.
- Pas de croix **portée** comme un accessoire de mode ; une croix en décor d'autel est acceptable.
- Pas de miracle **inventé** : on illustre le texte, on ne fabrique pas une scène absente du chant.

### 11.2 Ce qui est interdit dans une image

Drapeau, bannière nationale, symbole de parti · logo d'église ou de ministère · contact, lien, QR ·
nudité, anatomie exhibée, caméra sur une partie du corps · photo personnelle envoyée au générateur sans
autorisation écrite · signe occulte ou ésotérique détourné.

### 11.3 Vocabulaire

- Les termes intouchables de Q3 sont **invisibles aux corrections automatiques**.
- Les langues d'origine (espagnol, yoruba, wolof, créole…) gardent leur orthographe **exacte** dans le
  texte peint, accents compris. C'est la première chose à vérifier sur un frame.
- « WTBW » s'écrit **WTBW**. Jamais développé, jamais traduit, jamais expliqué à l'écran.

### 11.4 Ton

Le gospel n'a pas besoin d'être sombre pour être profond. Éviter le misérabilisme visuel qui contredit
un texte d'espérance : si le refrain dit « victoire », la palette doit s'ouvrir à ce moment-là.

---

## 12 — Livraison : format jamais négociable

Toute réponse de livraison contient, **dans cet ordre** :

1. **Titre exact** de l'œuvre.
2. **Caption** prête à coller (2 à 4 phrases, sans hashtag dedans).
3. **Hashtags** : **13 maximum**, comptés.
4. **Le fichier 9:16** présenté à l'utilisateur (pas seulement nommé).
5. **Déclaration IA** : visuels **OUI**, audio **NON**, en une phrase claire.
6. **Commandes Termux**, une ligne par fichier, `curl -L --retry 3 -C - -o`, puis `termux-media-scan -v`,
   avec les URL **figées sur le SHA du commit poussé**.
7. **Les contrôles chiffrés** du §10.3, avec les valeurs réelles.

### 12.1 Termux — la partie que les utilisateurs ratent

```sh
pkg install -y curl coreutils termux-api
termux-setup-storage
BASE="https://raw.githubusercontent.com/<compte>/<dépôt>/<SHA>/<chemin>"
curl -L --retry 3 -C - -o "fichier.mp4" "$BASE/fichier.mp4"
termux-media-scan -v "fichier.mp4"
```

- `termux-media-scan` n'est **pas facultatif** : sans lui, TikTok ne voit pas le fichier.
- `-C -` permet de **reprendre** un téléchargement interrompu, pas de recommencer.
- Les URL pointent sur le **SHA**, jamais sur un nom de branche.
- Fournir un **`SHA256SUMS.txt`** et les valeurs attendues, pour que l'utilisateur puisse vérifier.
- **Ne jamais** mettre dans `SHA256SUMS.txt` un fichier qui n'est pas dans le dépôt : le contrôle
  échouera et l'utilisateur croira à une corruption. (Panne réelle sur MESÍAS.)

### 12.2 Ce qui doit être dit dans la livraison, même si personne ne le demande

- ce qui n'a **pas** été validé par l'artiste (traduction, calage) ;
- ce qui a été **modifié** techniquement (normalisation audio, mode dynamique) ;
- ce qui **n'a pas été livré** et pourquoi (fichier trop lourd, upload bloqué) ;
- ce qui **n'a pas fonctionné** dans les tentatives (alignement automatique, release GitHub).

Un défaut annoncé vaut mieux qu'un défaut découvert par l'artiste après publication.

---

## 13 — Git et survie du sandbox

- commit + push **après chaque étape**, uniquement sur la **branche de la session**.
- **Jamais** de `git reset --hard` automatique.
- **L'environnement peut être remis à zéro entre deux tours** : le clone local peut revenir à un commit
  ancien, `productions/` peut disparaître, `PIL` et `imageio-ffmpeg` peuvent manquer.
  **Vérifier avant de répondre :** `git log --oneline -1`, `ls productions/`, `python3 -c "import PIL"`.
  Si le local est en retard mais que le distant est bon : `git fetch` puis `git checkout -B <branche> <sha>`.
- `work/` (bases, maquettes, segments) va dans `.gitignore`. Les **livrables** restent versionnés,
  **sauf** ce qui dépasse 100 Mo.
- Polices **versionnées** dans le dépôt avec leur licence.
- Ne jamais conclure qu'un lien est mort depuis le sandbox : `raw.githubusercontent.com` y est souvent
  bloqué. Vérifier **la taille du blob par l'API** à la place.
- Après un `git push` refusé, lire l'erreur **avant** de réessayer : `GH001` = fichier trop lourd,
  ce n'est pas un problème d'authentification.

---

## 14 — Interdits permanents

1. Générer, imiter ou remplacer la **voix** de l'artiste.
2. Générer la **musique** ou modifier la partition.
3. Utiliser un audio qui n'est **pas** celui de l'artiste.
4. Écrire « calé », « validé », « approuvé » **sans oreille humaine** ou sans réponse de l'artiste.
5. Publier une **mesure inventée**, un **hash non poussé**, un **fichier annoncé mais absent**.
6. Mettre du texte sur le **visage**.
7. Mettre un **voile ou un flou sur les glyphes**.
8. **Superposer** traduction peinte et original défilant dans la même bande.
9. Mettre un fichier **>100 Mo** dans l'historique git.
10. Développer ou traduire **WTBW**.
11. Dire « clip officiel » quand c'est un clip lyrics produit par WTBW.
12. Se contenter de « à peu près » — sur un mot, sur une mesure, sur une date.

---

## 15 — Ordre d'exécution d'une production complète

```
 1. Poser les 4 questions (§0).                     → bloc de configuration rempli
 2. Mesurer l'audio (§8.2).                          → durée, LUFS, crête, silence
 3. Écrire/valider les paroles + la traduction.      → couverture 100 %, « manquants: [] »
 4. Écrire le contrat des vers (JSON).               → débuts, fins, images, zones
 5. Générer l'ancre (1 image), la faire contrôler.   → style verrouillé
 6. Générer les salves d'images (10/tour).           → 40 à 60 plans
 7. Contrôler les planches contact.                  → aucune image fautive
 8. Assigner le pool par règles sémantiques.         → compteur d'emplois équilibré
 9. Construire les bases 1080×1920.                  → 1 fichier par plan
10. Maquette courte (12 vers) avec audio.            → FAIRE ÉCOUTER, demander l'offset
11. Appliquer l'offset, re-rendre la maquette.       → validation d'écoute obtenue
12. Rendu par segments (20 à 40), assemblage.        → contrôle de durée
13. Contrôles chiffrés (§10.3) sur le fichier final. → 0 noir, 0 gel, faststart
14. Version publiable (<95 Mo), calibrée par mesure. → contrôle à l'œil
15. Teaser 15 s (450 frames exactement).             → contrôle
16. Couvertures (1 principale + 2 variantes).        → zones sûres, aucun texte sur le visage
17. Empreintes SHA256 des fichiers réellement livrés.
18. Push, puis URL figées sur le SHA.
19. Livraison au format §12, avec ce qui n'est pas validé.
```

**Chaque étape se termine par un contrôle, pas par une impression.** Si un contrôle échoue, on corrige
**avant** de passer à la suivante — jamais « on verra à la fin ».

---

## 16 — Historique

- **v8.0** (2026-11-15) — « Le texte d'abord, la panne ensuite ». Quatre questions obligatoires (dont la
  langue peinte/défilante et le poids cible). Mode **HYBRIDE INVERSÉ** ajouté. Images **polyvalentes**
  réutilisables au lieu d'un plan par vers, avec assignation sémantique et compteur d'emplois.
  Chapitre **pannes réelles** : sinus gelés → rampes triangulaires, cartes figées → fond surdimensionné,
  `-shortest` → `apad`, scrim en arête → smoothstep, tag `USLT` trompeur, mur des 100 Mo.
  Contrôles au seuil **1,2 s**, normalisation **déclarée** (mode dynamique imposé), `SHA256SUMS` honnête.
  Chapitre gospel : dignité du sujet, interdits propres au genre, vocabulaire intouchable.
  Validé sur MESÍAS : 749,705 s, 22 491 frames, 190 vers, 50 images, −14,1 LUFS, 0 gel, 0 noir, faststart.
- **v5.9** (2026-10-14) — question §0 (défilant / peint), chapitre mouvement, contrôles chiffrés.
- **v5.8** — typo peinte par le modèle, 1 plan par vers.
- **v5.7** — badge sans drapeau, cartes sans contact, clochettes.
- **v5.6** — clochettes CTA. **v5.5** — hybride, Termux une ligne par fichier.

**Signature : « WTBW » — et rien d'autre.**
