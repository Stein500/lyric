# 🎬 PROMPT UNIVERSEL DE PRODUCTION LYRICS — v4.5 (COVER + TAGS + CONTACT OUTRO)

**Artiste :** Daïsky · **Structure :** Daïsky Prod · **Signature / Production :** Techstein  
**Utilisation :** Référence OBLIGATOIRE pour tous les futurs clips lyrics / covers / exports audio Daïsky Prod / Techstein. Toute déviation doit être validée.

---

## 🧭 0. NOUVEAUTÉS v4.5

1. **Salves validées par étape** : image d'ancrage → salve 1 → validation artiste → **salve 2** → salves suivantes si besoin.
2. **Chaque musique crée sa propre cover originale** : jamais de cover générique réutilisée sans validation.
3. **Tags audio obligatoires** pour chaque musique livrée : artiste, label, producteur, genre, année, cover intégrée, contacts.
4. **Écran final contact obligatoire** à la fin de chaque vidéo générée pour faciliter le booking/contact.
5. Les informations ci-dessous doivent être **présentes dans le prompt de production**, dans les tags audio, et dans le carton final vidéo.

---

## 🧱 0bis. ANTI-RESET & RÈGLES GIT

- Travailler sur la branche `arena/<id>-<slug>`.
- Commit + push après chaque étape majeure : image d'ancrage validée, fin de salve, livrables vidéo/audio/cover.
- `livrables/` ne doit JAMAIS être dans `.gitignore`.
- `.venv/`, `work/`, `*.pyc`, binaires ffmpeg/ffprobe et fichiers temporaires restent hors dépôt.
- Garder un `PROGRESS.md` à jour : étapes cochées, durées, liste des images, minutage, version des livrables.
- Vérifier le hash (`git rev-parse HEAD`) avant de partager une URL de téléchargement.

---

## 🏷 RÈGLE D'OR ABSOLUE — BADGE / CTA « ⚡ DAÏSKY PROD »

> **Le badge « ⚡ DAÏSKY PROD » et tout CTA superposé sont 100 % STATIQUES.**

- Position fixe par défaut : **haut-gauche** (bas-gauche uniquement si validé).
- Même taille, même position, même police, mêmes couleurs sur toutes les frames.
- Aucune animation : pas de waver, zoom, mouvement, apparition/disparition ou dérive.
- Incrustation en **POST (PIL/ASS/overlay)**, jamais peinte dans les images sources IA.
- Les sous-titres ne doivent jamais chevaucher le badge.
- Contrôle visuel obligatoire sur planche de frames : toute dérive = non conforme = à refaire.

---

## 👤 1. CRÉDITS & CONTACTS OFFICIELS À UTILISER

À intégrer dans le prompt, les tags audio, les descriptions et le carton final vidéo :

- **Producteur / Signature :** Techstein
- **Label / Structure :** Daïsky Prod
- **Artiste :** Daïsky
- **Téléphones :** +229 01 61 16 24 08 / +229 01 49 11 49 51
- **Emails :** daiskypro@proton.me / daiskyproduction@gmail.com / techsteinsecureway@gmail.com
- **Réseau principal :** @daiskypro
- **Genre :** toujours renseigner le genre réel de la musique (`<GENRE>`), jamais vide.
- **Année :** toujours renseigner l'année de sortie/livraison (`<ANNEE>`), jamais vide.

### Bloc prompt obligatoire à recopier dans chaque production

```text
Crédits officiels à intégrer en post-production et dans les métadonnées :
Techstein · Daïsky Prod · Daïsky
Genre : <GENRE> · Année : <ANNEE>
Contact : +229 01 61 16 24 08 / +229 01 49 11 49 51
Emails : daiskypro@proton.me / daiskyproduction@gmail.com / techsteinsecureway@gmail.com
Réseau : @daiskypro
Important : aucun texte/contact/logo ne doit être généré directement par l'IA dans l'image source ; tout est ajouté proprement en post-production.
```

---

## 🎨 2. CHARTE GRAPHIQUE

### A. Style mixte « Amour / Lumière » — défaut pour titres romantiques

- Palette : noir profond `#05060A`, chaleur ambre `#E8A33D`, cyan électrique `#4DD2FF`, blanc cassé `#F5F9FF`.
- Ambiance : chaleureuse, romantique, lumineuse, coucher de soleil, halo doré, bokeh, grain 35 mm, touches cyan/ambre.
- Suffixe prompt type : `warm golden sunset backlight, subtle electric cyan rim light, amber accents, soft atmospheric haze, light bokeh, 35mm film grain, crushed blacks with cyan highlights, moody romantic cinematic grading, no text, no watermark, no logo`.

### B. Style Dark Trap / Lightning — option pour titres sombres / puissants

- Palette : noir profond, bleu orage, cyan électrique, blanc éclair, or fauve.
- Ambiance : sombre, orageuse, cinématique, éclairs, reflets mouillés, halos cyan, grain 35 mm.
- Suffixe prompt type : `cinematic dark trap aesthetic, volumetric lightning bolts, deep navy shadows, electric cyan rim light, wet asphalt reflections, 35mm film grain, moody atmospheric haze, crushed blacks, cyan highlights, subtle amber accents, no text, no watermark, no logo`.

### Interdit formel

- Aucun texte, logo, watermark ou contact généré par IA dans l'image source.
- Tout texte visible (paroles, badge, crédits, contact, année, genre) est ajouté en post-production.
- Jamais de ligne de vers splitée manuellement ; utiliser wrap auto au mot.

---

## 🖼 3. IMAGES & SALVES

- Générer par salves de **10 images maximum**.
- Toujours commencer par une image d'ancrage validée par l'artiste avant de lancer la suite.
- Formats obligatoires si clip complet :
  - Portrait **9:16** 1080×1920 pour TikTok/Reels/Shorts.
  - Paysage **16:9** 1920×1080 pour YouTube.
- Nomenclature : `NN_descriptif_court.jpg` dans `assets/raw/portrait/` et `assets/raw/landscape/`.
- Un vers = une image pour les clips lyrics complets, sauf validation contraire.

---

## 🖼 4. COVER DE PUBLICATION — PROPRE À CHAQUE MUSIQUE

Chaque musique doit avoir **sa propre cover originale** :

- Cover TikTok/Reels : `livrables/cover_<slug>_9x16.jpg`.
- Cover YouTube : `livrables/cover_<slug>_16x9.jpg`.
- La cover doit refléter le thème du morceau, son genre et son énergie.
- Inclure en post-production : titre, artiste **Daïsky**, badge/handle **@daiskypro**.
- La cover finale doit aussi servir d'**image intégrée APIC** dans le MP3 master.
- Contrôle : titre lisible en petit écran, aucun texte IA déformé, aucune faute sur Daïsky / Techstein / Daïsky Prod.

---

## 📝 5. PAROLES & MINUTAGE

- La notation artiste `-MM:SS` signifie **fin du vers** ; le début est la fin du vers précédent.
- Après 1:50, les horaires start/end doivent être écrits explicitement en secondes pour éviter la dérive.
- Lire l'audio avec ffprobe/mutagen pour connaître la durée exacte au dixième de seconde.
- Les segments doivent sommer exactement à la durée audio.
- Intro/outro musical-only : aucune parole incrustée si aucune voix chantée n'est présente.
- Traductions FR sous lignes non-Wolof quand demandé.
- Styles : `verse`, `hook`, `hook_final`, `bridge`, `wolof`.

---

## 💫 6. EFFET VAGUE DES PAROLES

- Apparition : lettres qui montent/ondulent et apparaissent une à une avec fondu.
- Disparition : lettres qui descendent/s'évanouissent en cascade.
- Légère ondulation continue par lettre, sans casser la lisibilité.
- Le badge et le contact ne doivent jamais être animés par cet effet.

---

## 🎞 7. MONTAGE PIPELINE

1. Préparer les frames : resize/letterbox + badge statique + grain/halo éventuel.
2. Générer clips silencieux par segment, puis concat demuxer. Pas de fade vidéo entre clips qui crée des trous noirs.
3. Ajouter paroles/effet vague en post-production.
4. Muxer l'audio final avec fade-in 0,3 s et fade-out 3 s.
5. Ajouter le **carton final contact** sur la fin de la vidéo.
6. Exports systématiques :
   - `*_9x16_vN.mp4` — 1080×1920 TikTok/Reels/Shorts.
   - `*_16x9_YT_vN.mp4` — 1920×1080 YouTube.

---

## 📇 8. ÉCRAN FINAL CONTACT — OBLIGATOIRE SUR CHAQUE VIDÉO

À afficher sur les **8 à 12 dernières secondes** de chaque vidéo générée, ou sur l'outro musical si elle existe. Le texte est statique, lisible, avec panneau sombre translucide + contour ambre/cyan.

### Texte final obligatoire

```text
CONTACT / BOOKING
Techstein · Daïsky Prod · Daïsky
Genre : <GENRE> · Année : <ANNEE>
Tél. : +229 01 61 16 24 08 / +229 01 49 11 49 51
Email : daiskypro@proton.me
Email : daiskyproduction@gmail.com
Email : techsteinsecureway@gmail.com
@daiskypro
```

### Règles

- Le contact final ne remplace pas le badge : il apparaît uniquement à la fin comme carte de contact.
- Ne jamais mettre ces informations dans l'image IA source ; toujours overlay propre en post-production.
- Pas d'animation obligatoire ; si fade utilisé, il doit rester sobre. Le texte ne doit pas bouger.
- Safe margins : lisible en 9:16 et 16:9, aucun élément coupé par les interfaces TikTok/YouTube.

---

## 🎧 9. TAGS MUSIQUES — OBLIGATOIRE AVANT LIVRAISON

Aucun fichier audio livré (`MP3`, `M4A`, `WAV` avec métadonnées possibles) ne doit sortir sans tags complets.

### Champs minimum à remplir

- **Titre** : titre exact du morceau.
- **Artist / TPE1** : Daïsky.
- **Album Artist / TPE2** : Daïsky Prod.
- **Producer / Composer** : Techstein.
- **Genre / TCON** : genre réel du morceau.
- **Year / TDRC** : année de sortie/livraison.
- **Publisher / Label** : Daïsky Prod.
- **Copyright** : `© <ANNEE> Daïsky Prod / Techstein. Tous droits réservés.`
- **Cover / APIC** : cover propre du morceau intégrée dans le fichier.
- **Contact** : téléphones + emails + @daiskypro.
- **Lyrics** : paroles si disponibles.

### Tags personnalisés recommandés

- `TXXX:PRODUCER = Techstein`
- `TXXX:LABEL = Daïsky Prod`
- `TXXX:ARTIST = Daïsky`
- `TXXX:PHONE = +229 01 61 16 24 08 / +229 01 49 11 49 51`
- `TXXX:EMAIL = daiskypro@proton.me / daiskyproduction@gmail.com / techsteinsecureway@gmail.com`
- `TXXX:CONTACT = bloc contact complet`
- `TXXX:GENRE = <GENRE>`
- `TXXX:YEAR = <ANNEE>`

Outil recommandé dans ce dépôt :

```bash
python tools/fill_music_tags.py "livrables/<audio>.mp3" \
  --title "<TITRE>" --genre "<GENRE>" --year "<ANNEE>" \
  --cover "livrables/cover_<slug>_9x16.jpg"
```

---

## ✅ 10. VÉRIFICATIONS OBLIGATOIRES AVANT COMMIT

1. Durée vidéo = durée audio ±0,3 s.
2. Blackdetect : 0 trou noir >300 ms.
3. Badge statique : même position/taille sur toutes les frames.
4. Paroles lisibles, aucune ligne coupée, minutage OK.
5. Carton final contact présent sur les 8–12 dernières secondes.
6. Cover propre présente en 9:16 + 16:9 et intégrée dans le MP3 master.
7. Tags audio complets : titre, Daïsky, Daïsky Prod, Techstein, genre, année, contact, cover.
8. Poids cohérent : pas de fichier cassé <100 KB.

---

## 📦 11. TÉLÉCHARGEMENTS TERMUX / ANDROID — REPRENABLE

Destination obligatoire : `/storage/emulated/0/Web+/`.

```bash
cd /storage/emulated/0/Web+/
find . -name "*.mp4" -size -100k -delete
find . -name "*.mp3" -size -100k -delete
find . -name "PROMPT*" -size -1k -delete

curl -fL --retry 5 --retry-delay 3 -C - \
  -o "nom_du_fichier.mp4" \
  "https://raw.githubusercontent.com/Stein500/lyric/<COMMIT_HASH>/livrables/nom_du_fichier.mp4"
```

Toujours utiliser un **hash de commit** dans l'URL, jamais une branche.

---

**Signature :** « Wolof TechStein beat wê ! » ⚡
