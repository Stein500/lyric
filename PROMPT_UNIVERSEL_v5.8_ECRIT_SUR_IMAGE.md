# 🎬 PROMPT UNIVERSEL DE PRODUCTION LYRICS — v5.8 « ÉCRIT SUR L'IMAGE »

Mise à jour : **2026-10-10**. Ce document **hérite de v5.6** (`PROMPT_UNIVERSEL_v5.6_AUBE_CLOCHETTES.md`) et des règles
**v5.7 « Aube & clochettes appliquées »** transmises oralement pour « Gbètché vivi » ; il **les remplace** là où il y a
conflit. Les paramètres d'une chanson ne se reportent **jamais** automatiquement sur une autre chanson.

Priorité d'application : **demande explicite de l'artiste de la session** → configuration validée → règles v5.8 → v5.6 → v5.5 → archive v5.3.

---

## 0 — Nouveautés de la v5.8 (décisions et leçons de « Gbètché vivi », version 2)

1. **L'outil écrit DANS l'image** (§A) : le texte n'est plus seulement un calque posé au montage, il est **gravé dans la
   matière de la scène** (marker sur papier scotché, néon, craie au sol, peinture stencil) et généré **par le générateur
   d'images**, sur une image **déjà validée** en v1 (mode édition, pas re-création).
2. **Autocollants et icônes dessinés par le moteur** (§B) : scotch, étoiles découpées, souligne au feutre, cadre pointillé,
   flèche courbe, icônes vectorielles (cloche, partage, signet, play, œil, check, étincelle) — **jamais d'emoji système**.
3. **Zone dessinée bornée** (§C) : tout ce que le moteur dessine reste dans **y 1140 → 1574** et **x ≤ 910**, pour que le
   contrôle « aucune encre sur le visage » reste mesurable et **vert**.
4. **Contrôle d'orthographe du texte gravé = étape obligatoire** (§A.4) : planche de relecture à 100 %, sinon on livre des
   fautes brûlées dans l'image, donc invisibles au correcteur orthographique et incurables au montage.
5. **Le ratio 9:16 est exigé à chaque édition** (§A.2) : un `generate_image` en mode édition peut rendre 0,67 de ratio ;
   corriger par un nouveau prompt, **jamais** par un recadrage haut/bas.
6. **Chaîne audio** (§D) : un **limiteur posé avant** l'encodage MP3/AAC (l'encodeur dépasse toujours d'environ +0,5 dB), et
   `-hide_banner -nostats` (surtout **pas** `-v error`, qui avale le JSON de mesure de `loudnorm`).
7. **Tags** (§E) : **APIC par ffmpeg puis USLT par eyeD3**, dans cet ordre — dans l'autre sens les paroles sont perdues.
8. **Rendu** (§F) : `start_process`, jamais `nohup … &` depuis un appel bash (l'appel se fait avoir par le timeout et le
   suivi est perdu) ; smoke test de 10 frames avant les 5 995 ; pas de commit avant `moov` valide.
9. **`freezedetect` n'est pas un défaut** (§G.3) quand l'artiste interdit le recadrage/zoom : fonds fixes = images qui ne
   bougent pas. Le déclarer, ne pas le cacher, ne pas tricher avec un faux Ken Burns.

---

## A — Texte gravé dans l'image (la règle « écris sur l'image »)

### A.1 Ce qu'on demande au générateur
- Édition d'une image **déjà validée** (`images=[personnages/anim-NN.png]`) → la personne, la lumière et le cadrage sont
  conservés ; on n'ajoute **que** l'écriture et les matières.
- Formulation type, dans cet ordre : *« garde exactement le même homme, la même pose, le même studio, la même lumière, le
  même cadrage, rien de coupé en haut ni en bas »* → *« écris DANS la scène, en majuscules au marqueur noir, sur la feuille
  de papier blanc scotchée au mur à gauche »* → le mot exact, en clair, entre guillemets simples → *« une seule personne, pas
  de drapeau, pas de logo de marque, pas de filigrane, pas de bande noire »*.
- **Le mot doit être court** : 1 à 4 mots, ou 4 chiffres. Au-delà, l'orthographe dérive.
- Interdire explicitement l'écriture **sur la peau, les lunettes et les vêtements** (sinon le texte mange le visage).

### A.2 Où on l'écrit (zones autorisées)
| Zone | y (sur 1920) | Usage |
|---|---|---|
| Mur / glace / whiteboard, **à gauche ou à droite de la tête** | 260 → 1000 | titre, hook, adlib, mot du refrain |
| Sol (craie, peinture stencil) | 1580 → 1900 | un seul mot fort (« LIBRE »), sous la zone de texte |
| Objet tenu / scotché, à hauteur d'épaule | 980 → 1130 | carte de code, étiquette |
| **Interdit** | 0 → 144 et **au-dessus du visage** (front, yeux, bouche, menton) | — |
| **Interdit** | bande de paroles **y 1160 → 1330** sur ~740 px de large | rien d'important ne doit s'y trouver : le moteur la couvre d'un scrim et y écrit les paroles |

Si le mot généré tombe dans la bande de paroles, **on régénère** avec « garde le sol completely vide d'écriture » (leçon
A03 v2 : « VIVI » peint au sol se retrouvait sous les paroles → régénéré).

### A.3 Ratio
Exiger dans le prompt : « même ratio vertical très allongé, 9 de large pour 16 de haut, ne pas élargir l'image ». Mesurer
après génération : `largeur/hauteur = 0,5581 ± 0,002` sur les 30+ plans (le moteur redimensionne en 1080×1920, un ratio
différent = **étirement** du visage, donc rejet). Mesurer aussi **les colonnes de bord** (noir quasi total = lettrebox
parasite) : la règle « pas de bande noire » vaut pour les quatre bords.

### A.4 Contrôle orthographe (non négociable)
1. Construire une **planche** de tous les plans modifiés (`PLANCHE-v2-*.jpg`) et la **lire à l'écran**.
2. Vérifier lettre à lettre : les accents disparaissent souvent (« ME PLAÎT » → « ME PLAIT ») → **acceptable** sur un mur
   peint à la main, **à déclarer** dans la notice ; « Wanyiyi » passé derrière une tête → **inacceptable**, régénéré.
3. Budget : maximum **10 générations par tour**. Bon découpage observé : 6 plans d'abord, 3 corrections ensuite, 1 spare.
4. Un texte qu'on ne peut pas corriger proprement (marque, nomComplexe, citation longue) → le faire en **post-production**
   (PIL), pas dans l'image.

---

## B — Autocollants et icônes (primitives validées dans `stickers.py`)

| Primitive | Effet | Règle |
|---|---|---|
| `tape` | bande de masking tape aux bords déchirés, rotation ±13° | jitter issu d'un `default_rng` **grainé par la position** → stable d'une frame à l'autre |
| `star` / `burst` | étoile découpée à crans, rayons | alpha ≤ 235, jamais de contour blanc franc |
| `squiggle` | soulignement au feutre, épaisseur variable | sous la dernière ligne du vers, **jamais** au-dessus de y 1134 |
| `highlight` | coup de surligneur derrière **le mot actif** | flou 3,2 px, alpha ≈ 110, tracé **avant** le texte |
| `dashed` | cadre pointillé dessiné à la main | 13 px de tiret / 10 de blanc, alpha ≤ 165 |
| `arrow` | flèche courbe à tête en V | un seul point d'attention par frame |
| `icon` | cloche, partage, signet, play, œil, check, étincelle | **contours vectoriels**, jamais d'emoji |
| `tag` | étiquette inclinée (REFRAIN ×3, ADLIB, code) | libellé **déduit des données**, jamais inventé (§C.3) |
| `sparkles` | étincelles qui clignotent | phase liée à `t`, zone bornée |

Contraintes héritées (toujours vraies) : or **→ bronze** uniquement, halo doux, balancement de clochette **±12°** amorti,
période 1,2 s, pulsation 0,8 s, **aucun drapeau**, **aucun logo**, texte UI en police nette.

## C — Géométrie du bloc de paroles (avec ou sans stickers)

1. **Borne haute = bas de tête mesuré** sur les fonds, pas une intuition. Méthode : lire les crops, pas un détecteur
   (la détection de peau et les boîtes d'un détecteur générique **ment** sur ces images : mains, torse, néons, porte
   lumineuse accrochés → abandonnée). Pour « Gbètché vivi » : `FACE_LIMIT = 1134`.
2. Bloc calé **sous** cette borne, ici **y 1160 → 1330**, largeur ≤ 740 px, corps auto-ajusté (78 → 40) avec coupe en 2
   lignes au meilleur équilibre, `min(4, max(2, 0,07·car + 1,2))` borné au vers suivant − 0,05 s, fondu 0,35/0,18 s,
   mot actif or (scale 1,06 en attaque), passés crème, suivants DIM, vague de 4,5 px à 0,9 Hz.
3. Etiquettes de section : **dédrites du fichier de paroles** — ligne qui revient ≥ 3 fois = `REFRAIN ×n` ; réplique de
   signature/producteur = `ADLIB`. Sinon aucune étiquette. Ne jamais écrire « REFRAIN » par supposition.
4. Lisibilité : fond assombri (0,74 en v1, **0,80 en v2** pour laisser lire l'écriture gravée) + scrim sombre flouté
   derrière le bloc (bande 56 → W−56, rayon 58, flou 40).
5. **Audit automatique à chaque livraison** : `max|frame − fond| > 6` **au-dessus de y 1134**, hors bandeau de badge
   (y 140→216) = violation. L'audit ne teste pas les fenêtres CTA (la cloche est censée occuper le centre).

## D — Chaîne audio (deux passes réelles + plafond)

1. Passe 1 : `loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json` avec `-hide_banner -nostats` (avec `-v error`, le JSON est
   avalé et la passe 2 part en mode dynamique).
2. Passe 2 : `linear=true` + mesures `measured_I/TP/LRA/thresh` + `offset` reprises du JSON.
3. **Après** la normalisation, pos **un limiteur avant l'encodeur** : `alimiter=limit=0,79:level=false:attack=5:release=90`
   (≈ −2,05 dBFS) → le MP3/AAC rendu mesure ≈ −1,5 dBTP. Sans lui, l'encodeur ressort à −0,9/+0,1 dBFS.
   `level=false` est **obligatoire** : par défaut `alimiter` remonte le signal à pleine échelle (constaté : −14 → −12,5 LUFS).
4. Carte finale muette : `-af apad=whole_dur=<total>`, `-t <total>`, sinon l'image se fige sur une piste plus courte.
5. Encodage vidéo : `rawvideo rgb24` sur stdin → `libx264 -preset veryfast -crf 24 -pix_fmt yuv420p` +
   `-colorspace bt709 -color_primaries bt709 -color_trc bt709` + `-movflags +faststart`, AAC 256k / 48 kHz stéréo.

## E — Tags du master (ordre imposé)

1. `ffmpeg -map 0:a -map 1:v -c:a copy -c:v copy -id3v2_version 3 -metadata:s:v title="Album cover"
   -metadata:s:v comment="Cover (front)" -metadata title=… -metadata artist=… -metadata album=…` → **APIC**.
2. **puis** `eyeD3 --add-lyrics=PAROLES:Paroles:fre MASTER.mp3` → **USLT** (l'ancienne méthode « ffmpeg ne sait pas
   écrire USLT » reste vraie ; eyeD3 installé dans le venv de travail le fait ici, sinon la commande est à donner à
   l'artiste en Termux).
3. Vérifier avec `eyed3` (module **minuscule** : `import eyed3`, pas `eyeD3`) : `tag.images` et `tag.lyrics` non vides.
   Un champ `comment` peut ne pas s'afficher dans `tag.comments` alors qu'il est dans la frame : contrôler avec ffmpeg.
4. La pochette carrée ne rogne **jamais** la tête : buste recadré latéralement + fond **flouté étiré**, jamais de pad noir,
   jamais de crop haut/bas.
5. Noms de fichiers livrés : **sans accent ni espace** si possible (les chemins Termux/URLs mangent les accents ; sinon
   tout URL est passé en `%C3%A9`/`%20`).

## F — Rendu et reprise

1. **Smoke test de 10 frames** choisies à des moments qui font mal (0,1 s après un fondu d'intro, un vers de 2 lignes,
   une fenêtre CTA, un plan visage serré, la carte finale) avant de lancer 6 000 frames.
2. Lancer le rendu complet avec l'outil process en arrière-plan (`start_process`), pas `nohup &` dans un appel shell.
3. Progression à surveiller : taille du `.mp4` (le stdout d'un pipeline tamponné ne montre rien).
4. Ne jamais commiter avant d'avoir lu `rc=0` + `frames=N duree=…` et vérifié `moov` (le fichier tronqué lit « moov atom
   not found »).
5. Un fichier de rendu intermédiaire lourd (WAV 48 k, caches) reste **hors** git (`.gitignore`).

## G — Contrôles du fichier livré (commandes types)

```
FF=$(python -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
"$FF" -hide_banner -i CLIP.mp4 | grep -E "Duration|Stream"                    # 1080x1920 / 30 fps / yuv420p / aac
"$FF" -v info -i CLIP.mp4 -map 0:v:0 -f null - | grep "^frame="                # frames == durée × fps
"$FF" -v info -i CLIP.mp4 -vf blackdetect=d=0.10:pix_th=0.10 -f null -         # 0 passage noir hors fondus voulus
"$FF" -v info -i CLIP.mp4 -af ebur128=peak=true,astats -f null - | grep -E "I:|TPK|Peak level"
"$FF" -v info -i CLIP.mp4 -vf freezedetect=n=-60dB:d=4 -f null - | grep -c freeze
```
1. **Durée annoncée = durée décodée** : `frames/FPS` doit retomber sur le `Duration` affiché.
2. **Volume** : intégrées à −14 LUFS, crête ≤ −1,5 dBFS.
3. **Freeze** : les déclarer et dire **pourquoi** (fonds fixes = conséquence de l'interdiction du crop), jamais les cacher.
4. **Preuve visuelle par crop** de la limite paroles/visage (ligne rouge = haut de la bande de paroles sur les deux plans
   les plus serrés) à joindre aux contrôles : un ratio chiffré obtenu par un détecteur non fiable ne vaut rien.

## H — Paquet de livraison (à chaque chanson)

Clip 9:16 · master MP3 320k taggé (APIC + USLT) · covers carrées (1 principale + 3 de rechange) · `.lrc` des paroles ·
notice de production de la chanson (`ANCRE.md`) · **ce prompt à jour** · commandes Termux.

1. Titre d'upload + variante courte, **caption** avec l'accroche « regarde jusqu'à la fin », le **code de fin** et les
   trois verbes CTA (commente / partage / enregistre), **10 à 13 hashtags**, **déclaration IA** explicite (visuels + clip
   générés par IA, paroles et audio de l'artiste, origine du beat si elle est mentionnée dans les métadonnées sources).
2. **Termux, format anti-casse** : une seule ligne par fichier, séparateur `;`, jamais `&&` ni continuation multiligne,
   `curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/NOM <url>` ; URLs **URL-encodées** ; gabarit :
   `mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/NOM https://raw.githubusercontent.com/{OWNER}/{REPO}/{HASH}/CHEMIN; ls -lh /storage/emulated/0/Web+/NOM`
3. Le `{HASH}` est pris **après** le commit des livrables (`git rev-parse HEAD`) et **vérifié** fichier par fichier
   (`git cat-file -e {HASH}:{CHEMIN}`) avant d'être partagé. Le doc de livraison qui contient le hash est commité
   **après** les livrables (2ᵉ commit) — sinon il se référence lui-même.

## I — À faire valider par l'artiste (ne jamais considérer acquis)

- le **code de fin** (4 chiffres) — s'il est posé par défaut, l'écrire en toutes lettres : « non validé » ;
- le **choix de police** : une police d'affichage **unicase sans jambage** fait lire `p`, `g`, `y` comme des majuscules sur
  une ligne longue → à signaler, avec le coût du changement (re-rendu complet) ;
- le **calage mot à mot** : les horodatages de l'artiste sont la source, le surlignage reste provisoire ;
- la **densité d'écriture dans l'image** (v2) : trop de texte gravé concurrent les paroles → 6 plans sur 30, pas plus.

## J — Version 2 de « Gbètché vivi » (référence d'implémentation)

- Drapeau **`--v2`** de `productions/gbetche-vivi/render_lyric_video.py` : pose `V2=1` **avant** l'import de
  `render_intro_cta` (le fond d'intro est figé à l'import), bascule les 6 plans marqués sur `personnages/anim-v2-NN.png`
  (01, 03, 05, 12, 29, 30), remonte l'assombrissement du fond à 0,80, ajoute surligneur + souligné + `deco_v2` (scotch,
  cadre pointillé, étoile, étiquette de section, étincelles) et `intro_v2` (cadre sur les pilules, flèche vers la cloche),
  écrit `livrables/Gbetché vivi - 916 v2.mp4`.
- `make_cover_v2.py` : 4 carrés 1080² décorés (feuille scotchée + titre écrit au marqueur + souligné feutre + étiquette
  de code + cloche/partage/signet vectoriels + étoiles + étincelles), master v2 = **audio identique**, APIC v2 puis USLT.
- Écarts assumés v1 → v2 : écriture dans la matière, autocollants vectoriels, un peu moins de noir sur les images.
