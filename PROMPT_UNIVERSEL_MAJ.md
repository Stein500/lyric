# 🎬 PROMPT UNIVERSEL DE PRODUCTION LYRICS — v4.3 (FINALE RIGOUREUSE)

**Artiste de référence :** Daïsky  
**Projet de référence :** *Lightning Is My Name* (EN/ES/Wolof)  
**Utilisation :** Ce prompt est la référence OBLIGATOIRE pour TOUS les futurs clips lyrics de Daïsky Prod / TechStein. Toute déviation doit être validée.

---

> ⚡ **RÈGLE D'OR ABSOLUE — BADGE / CTA « DAÏSKY PROD » : NE DOIT JAMAIS BOUGER.**
> **Le badge « ⚡ DAÏSKY PROD » (et tout CTA superposé : "abonne-toi", "dispo", crédits, etc.) est 100 % STATIQUE.**
> - Même **taille**, même **position**, même **police**, mêmes **couleurs** sur **TOUTES** les frames de la vidéo — du premier au dernier instant.
> - **AUCUN** waver, **AUCUNE** animation, **AUCUN** mouvement, **AUCUN** zoom, **AUCUN** effet d'apparition/disparition, **AUCUN** changement pendant les changements de plan.
> - Le badge/CTA est incrusté en **POST (PIL/ASS)** après la génération des images : il n'est **JAMAIS** peint dans l'image source (`assets/raw/`).
> - Le badge/CTA est **au-dessus** de la vidéo, il ne peut jamais être recouvert ni décalé par un sous-titre ; les sous-titres ne doivent jamais chevaucher le badge.
> - **Contrôle visuel obligatoire** (règle v4.2) : sur TOUTE planche de frames, vérifier que le badge est **rigoureusement à la même place** sur chaque image. Toute dérive = non conforme = à refaire.

---

## 🧱 0. ANTI-RESET & RÈGLES GIT

- Toujours travailler sur une branche dédiée `arena/<id>-<slug>`.
- **Commit + push après chaque étape majeure** (image d'ancrage validée, fin de salve, livrables).
- Le dossier `livrables/` ne doit JAMAIS être dans `.gitignore`.
- Les outils (venv, work/, __pycache__, *.pyc) vont dans `.gitignore` pour ne pas polluer GitHub avec des binaires 70+ MB.
- Maintenir un `PROGRESS.md` à la racine reprenant l'état exact du chantier (étapes cochées, durées, liste des images, minutage).
- Avant de partager une URL de téléchargement, vérifier par `git rev-parse HEAD` que le hash du commit est bien celui qui contient le fichier.
- **DESTINATION TÉLÉCHARGEMENT = TOUJOURS `/storage/emulated/0/Web+/`** (Android/Termux). Les commandes curl de la section 6 doivent systématiquement `cd /storage/emulated/0/Web+/` avant le téléchargement.
- **BADGE / CTA « DAÏSKY PROD » = STATIQUE, NE BOUGE JAMAIS** : même taille, même position, même style sur TOUTES les frames (aucun waver/animation/zoom). Incrusté en POST (PIL/ASS), jamais dans l'image source. Voir « RÈGLE D'OR ABSOLUE » en tête de ce document.
- **JAMAIS de binaire ffmpeg/ffprobe ou de venv dans le dépôt** (GitHub bloque >100 MB et warning >50 MB).

---

## 🎨 1. CHARTE GRAPHIQUE — DARK TRAP / LIGHTNING / CYAN / AMBER

### Palette
| Nom | Hex | Usage |
|---|---|---|
| Noir profond | `#05060A` | Fond |
| Bleu orage | `#0B1024` | Ombres |
| Cyan électrique | `#4DD2FF` | Rim light, accents, hook |
| Blanc éclair | `#F5F9FF` | Versets |
| Or fauve | `#E8A33D` | Lignes hook final / pont / Wolof |

### Ambiance
Sombre, orageuse, cinématique, contrastes violents, éclairs comme source de lumière principale, grain 35mm, halos cyan, reflets mouillés.
**Sceau esthétique :** première salve (images 01-10) = cinématique hyperréaliste ; salve 2 (11-20) = noir animé / seinen manga / cel-shaded (c'est la salve pour les rapides, hook final, outro, cover officielle) ; salve 3 (21-30) = bonus scènes dans le même style animé.

### Prompt suffixe à ajouter systématiquement
`cinematic dark trap aesthetic, hyperreal (or: black-and-cyan seinen manga cel-shaded), volumetric lightning bolts, deep navy shadows, electric cyan rim light, wet asphalt reflections, 35mm film grain, moody atmospheric haze, color grading: crushed blacks, cyan highlights, subtle amber accents, no text, no watermark, no logo`

### ⚠️ INTERDIT FORMEL
- **AUCUN texte, eau, logo généré par IA** — tout le texte (paroles, badge, crédits) est incrusté ensuite en PIL/ASS.
- Jamais de ligne de vers splitée à la main ; laisser WrapStyle=1 faire le wrap au mot.

---

## 🖼 2. IMAGES — 30 IMAGES 9:16 MINIMUM

- **10 images maximum par salve** de génération, avec une image d'ancrage validée visuellement par l'artiste avant de continuer.
- 20 portraits 9:16 (1080×1920) : la base pour TikTok/Reels/Shorts.
- 20 paysages 16:9 : pour youtube 
- Nomenclature : `NN_descriptif_courte.jpg` dans `assets/raw/portrait/` (ou `landscape/`).
- Après génération, on superpose en POST (PIL) un badge **"⚡ DAÏSKY PROD"** statique en bas-gauche, **même taille, même position, même style sur TOUTES les frames, sans aucun mouvement** (aucun waver/animation/zoom). Le badge n'est JAMAIS peint dans l'image source (`assets/raw/`). Toute dérive du badge entre deux frames = NON CONFORME.

---

## 📝 3. PAROLES & MINUTAGE — RÈGLE D'OR v4.2

> ⚠️ **MID/END VIGILANCE — RÈGLE CRITIQUE** : l'offset s'accumule dans le dernier tiers de la chanson. À partir de 1:50, TOUS les horaires (start ET end) sont **hardcodés explicitement** en secondes (`149.0, 152.0, ...`), jamais calculés à partir d'un `-MM:SS` relatif au vers précédent.

- Notation `-MM:SS` dans les paroles de l'artiste = **fin du vers** (pas début). Le début est la fin du vers précédent, SAUF pour les vers après qui doivent être écrits en plages explicites `m:ss-m:ss`.
- Lire l'audio avec mutagen/ffprobe pour avoir la durée EXACTE au dixième de seconde ; les coupures de segments doivent sommer exactement à cette durée.
- Le sample fourni par l'artiste (Wolof signature, drop, explosion) a sa propre plage verrouillée en dur.
- Traduction FR sous **chaque ligne non-Wolof** (une ligne, plus petit, italique, blanc-cassé, juste sous la ligne EN/ES).
- Styles : `verse`, `hook` (cyan, bold), `hook_final` (ambre, bold, +10% taille), `bridge` (cyan clair, italic, plus petit), `wolof` (ambre, bold, +10% taille, sans FR).

### Sous-titres ASS
- `WrapStyle: 1` (wrap au mot, pas de `\n` forcé dans le texte).
- Fades courts : **fade-in 80 ms, fade-out 120 ms** (`\fad(80,120)`).
- Outline 3 px noir + ombre 2 px pour la lisibilité sur les éclairs.
- Marges : ~340 px du bas en portrait, ~180 px en paysage.
- La ligne FR est décalée sous la ligne EN (même durée de vie, même fade).

---

## 🎞 4. MONTAGE — PIPELINE VIDÉO

### Ordre du pipeline
1. **Préparation des frames** (PIL) : resize/letterbox + badge overlay + grain/halo éventuel → JPEG quality 92 dans `work/prep/`.
2. **Clips silencieux** par segment : `ffmpeg -loop 1 -i frame.jpg -t dur -f lavfi -t dur -i anullsrc=... -c:v libx264 -preset veryfast -crf 23 -pix_fmt yuv420p -vf scale=W:H,fps=24 -c:a aac -b:a 128k -shortest -movflags +faststart clip.mp4`.
3. **Concat demuxer** : fichier `concat.txt` avec `file 'clip_XXX.mp4'` → `ffmpeg -f concat -safe 0 -i concat.txt -c copy concat.mp4`. **PAS de filtre `fade=t=in/out`** sur les clips individuels : ça crée des trous noirs au concat.
4. **Burn ASS + mux audio final** : `ffmpeg -i concat.mp4 -i audio.m4a -map 0:v:0 -map 1:a:0 -c:v libx264 -preset medium -crf 22 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 44100 -ac 2 -af "afade=t=in:st=0:d=0.3,afade=t=out:st=DURATION-3:d=3" -t DURATION -vf "ass=subs.ass" -movflags +faststart -shortest final.mp4`.

### Règles d'or du montage
- **Zéro trou noir** entre segments (utiliser le concat demuxer, pas le filtre `fade` sur les pistes vidéo).
- **BADGE / CTA STATIQUE ABSOLU** : le badge « ⚡ DAÏSKY PROD » (et tout CTA) reste **fixe en bas-gauche**, même taille/position/style sur 100 % des frames. **PAS de waver, PAS d'animation, PAS de zoom, PAS d'apparition/disparition.** Incrusté en POST (PIL/ASS), au-dessus de la vidéo, jamais recouvert par les sous-titres.
- Audio : fade-in 0,3 s, fade-out 3 s avant la fin.
- Deux exports systématiques :
  - **9:16** 1080×1920 → TikTok/Reels/Shorts (`*_9x16_vN.mp4`)
  - **16:9** 1920×1080 → YouTube (`*_16x9_YT_vN.mp4`)
- Livrables dans `livrables/` (jamais dans `out/`, `build/`, `dist/`).

---

## ✅ 5. VÉRIFICATIONS OBLIGATOIRES AVANT CHAQUE COMMIT

1. **Durée exacte** : ffprobe ou ffmpeg null mux → doit correspondre à la durée de l'audio à ±0.3 s.
2. **Blackdetect** : `ffmpeg -vf blackdetect=d=0.3:pix_th=0.10 -an -f null -` → **0 trou noir >300 ms**.
3. **Frame-by-frame des 30 DERNIÈRES SECONDES** (règle v4.2) : extraire une frame toutes les 2–3 s dans la fin de vidéo (de `DURATION-30` à la fin) + 1 frame de contrôle par section clé (début V1, milieu V2, hook final "never lies", outro Wolof, tout dernier frame du fade). Vérifier visuellement :
   - pas de dérive de minutage (les sous-titres correspondent à l'audio)
   - le Wolof est bien présent sur son segment
   - l'outro ne coupe pas brutalement (fade-out 3 s propre)
   - **badge « ⚡ DAÏSKY PROD » présent ET RIGOUREUSEMENT À LA MÊME PLACE / TAILLE sur chaque frame** (zéro dérive, zéro animation) ; vers intacts, FR présents
4. **Vérification de 0 ligne coupée** (wrap auto OK, aucun `\n` manuel dans les paroles courtes).
5. **Poids cohérent** : 9:16 ~20–30 MB, 16:9 ~12–20 MB pour 2:50 ; si le fichier est <100 KB c'est qu'il y a eu une erreur.

---

## 📦 6. TÉLÉCHARGEMENTS — COMMANDES REPRENABLES OBLIGATOIRES (v4.2)

> ⚠️ **DESTINATION OBLIGATOIRE (TOUJOURS)** : tous les fichiers récupérés sur Android/Termux DOIVENT être téléchargés dans
> **`/storage/emulated/0/Web+/`** (le dossier de travail de l'artiste). C'est le répertoire par défaut, figé, pour TOUS les
> livrables (`*.mp4`, `*.zip`, images, ...). Ne jamais télécharger ailleurs.

Toutes les URLs partagées avec l'artiste (Termux / Android) DOIVENT :

1. **Aller dans le dossier de destination et faire un nettoyage** des fichiers cassés (fichiers partiels / erreurs 404 qui font des 14 octets) :
   ```bash
   cd /storage/emulated/0/Web+/
   find . -name "*.mp4" -size -100k -delete
   find . -name "PROMPT*" -size -1k -delete
   ```
2. **Utiliser curl en mode REPRENABLE** vers `/storage/emulated/0/Web+/` :
   ```bash
   cd /storage/emulated/0/Web+/
   curl -fL --retry 5 --retry-delay 3 -C - \
     -o "nom_du_fichier.mp4" \
     "https://raw.githubusercontent.com/Stein500/lyric/<COMMIT_HASH>/livrables/..."
   ```
   - `-fL` : fail on error + suivre redirects
   - `--retry 5 --retry-delay 3` : retries automatiques sur coupure réseau
   - **`-C -` : REPRISE AUTOMATIQUE** — si la connexion coupe, relancer la même commande et ça repart d'où c'était arrêté
3. **Toujours donner le hash du commit** dans l'URL (pas de branche), pour garantir le contenu exact.
4. Vérification post-téléchargement : `ls -lh /storage/emulated/0/Web+/` (les tailles doivent correspondre à celles annoncées).

---

## 🚀 7. CHECKLIST RÉSUMÉE PAR ÉTAPE

- [ ] Cadre, dossiers, PROGRESS.md, .gitignore (livrables/ PAS exclu)
- [ ] Génération 30 portraits 9:16 par salves de ≤10 avec image d'ancrage validée
- [ ] Minutage : lecture audio + tableau de (start, end, text, style, fr) ; **après 1:50 tout en dur**
- [ ] Badge PIL overlay statique bas-gauche sur toutes les frames (NE BOUGE JAMAIS : même taille/position/style, pas d'animation)
- [ ] Montage pipeline : prép → clips → concat → burn ASS + mux audio → 2 exports
- [ ] Vérifications auto (durée + blackdetect) + frame-by-frame des 30 dernières secondes
- [ ] Commit avec message descriptif, push, vérification du hash
- [ ] Partager uniquement des commandes curl `-C -` reprenables avec hash de commit, téléchargées dans `/storage/emulated/0/Web+/`

---

**Signature :** "Wolof TechStein beat wê !" ⚡
