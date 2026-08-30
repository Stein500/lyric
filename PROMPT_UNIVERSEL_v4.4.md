# 🎬 PROMPT UNIVERSEL DE PRODUCTION LYRICS — v4.4 (FINALE RIGOUREUSE)

**Artiste :** Daïsky · **Projet de référence :** *L'amour est la réponse* (FR/Wolof)
**Utilisation :** Référence OBLIGATOIRE pour tous les futurs clips lyrics Daïsky Prod / TechStein. Toute déviation doit être validée.

---

## 🧭 0. NOUVEAUTÉS v4.4 (résumé des ajouts)

1. **Charte « Amour / Lumière »** (option par défaut pour les titres romantiques) : remplace la Dark Trap quand le titre l'exige. Le style mixte (chaleur + touches cyan/ambre) est validé.
2. **Badge / CTA = EN HAUT-GAUCHE** (position fixe désormais) — voir RÈGLE D'OR ABSOLUE.
3. **Format PAYSAGE 16:9 (YouTube)** en plus du 9:16 (TikTok/Reels). Images paysage dans `assets/raw/landscape/`.
4. **Effet « VAGUE »** sur l'apparition/disparition des vers (lettres qui ondulent, montent/descendent, fondu lettre par lettre).
5. **Musical-only** : l'intro « Wolof TechStein beat wê ! » et l'outro sont purement musicales (aucune parole incrustée).
6. **Cover de publication** (TikTok + YouTube) : titre en cursive + @daiskypro + éclair doré + couple, style Disney/anime inspiré des photos de l'artiste.
7. **Masterisation MP3** : objet → `livrables/*_MASTER.mp3`, **-14 LUFS** (ebur128) + nettoyage (highpass 30 Hz, lowpass 18 kHz), durée conservée.

---

## 🧱 0bis. ANTI-RESET & RÈGLES GIT

- Travailler sur la branche `arena/<id>-<slug>`.
- Commit + push après chaque étape majeure (image d'ancrage validée, fin de salve, livrables).
- `livrables/` ne JAMAIS dans `.gitignore`. `.venv/`, `work/`, `*.pyc` dans `.gitignore`.
- Garder un `PROGRESS.md` à jour.
- Ne jamais committer de binaires ffmpeg/ffprobe ou de venv.
- Vérifier le hash (`git rev-parse HEAD`) avant de partager une URL de téléchargement.

---

## 🏷 RÈGLE D'OR ABSOLUE — BADGE / CTA « ⚡ DAÏSKY PROD »

> **Le badge « ⚡ DAÏSKY PROD » (et tout CTA : @daiskypro, « abonne-toi », crédits) est 100 % STATIQUE.**
> - **Position fixe : EN HAUT-GAUCHE** (à défaut, bas-gauche si validé) — **même taille, même position, même police, mêmes couleurs** sur TOUTES les frames, du premier au dernier instant.
> - **AUCUN** waver / animation / zoom / apparition-disparition / mouvement.
> - Incrusté en **POST (PIL/ASS)**, jamais peint dans l'image source (`assets/raw/`).
> - Placé **au-dessus** de la vidéo ; les sous-titres ne doivent jamais le chevaucher.
> - **Contrôle visuel obligatoire** : sur toute planche de frames, le badge doit être rigoureusement à la même place sur chaque image. Toute dérive = NON CONFORME = à refaire.

---

## 🎨 1. CHARTE GRAPHIQUE

### A. Style mixte (défaut pour titres amour) — validé
- **Palette** : Noir profond `#05060A` / chaleur ambre `#E8A33D` (or fauve) / cyan électrique `#4DD2FF` / blanc cassé `#F5F9FF`.
- **Ambiance** : amoureuse, chaleureuse, légère (coucher de soleil, halo doré, bokeh, grain 35 mm, touches cyan/ambre subtiles, formes soulignées de façon classe).
- Prompt suffixe type : `warm golden sunset backlight, subtle electric cyan rim light, amber accents, soft atmospheric haze, light bokeh, 35mm film grain, crushed blacks with cyan highlights, moody romantic cinematic grading, no text, no watermark, no logo`.

### B. Style Dark Trap / Lightning (option pour titres sombres)
- Palette cyan/ambre, éclairs, reflets mouillés, grain 35 mm. Sceau esthétique : salve 1 hyperréaliste, salve 2 noir animé seinen, salve 3 bonus.

### ⚠️ Interdit formel
- **AUCUN texte / eau / logo généré par IA** — texte, badge, crédits, @handle incrustés ensuite en PIL/ASS.
- Jamais de ligne de vers splitée à la main (WrapStyle=1, ou wrap auto au mot).

---

## 🖼 2. IMAGES

- 20 portraits **9:16** (1080×1920) TikTok/Reels/Shorts.
- + paysages **16:9** (1920×1080) YouTube, dans `assets/raw/landscape/`.
- **10 images max par salve**, avec image d'ancrage validée par l'artiste avant de continuer.
- Nomenclature `NN_descriptif_courte.jpg`.
- Un **vers = une image** pour les clips lyrics complets (30 images pour la chanson type).

---

## 💫 3. EFFET VAGUE (apparition/disparition des vers)

- Apparition : lettres qui **montent/ondulent** et apparaissent **une à une** (staggered) avec fondu.
- Disparition : lettres qui **descendent/s'évanouissent** en cascade (staggered reverse).
- Légère ondulation continue (sinusoïde par lettre) pour la sensation de vague.
- Transition ~0,9 s ; rendu image par image (PIL) ou ASS/SRT animé. Ne jamais casser la lisibilité (contour/ombre).

---

## 📝 4. PAROLES & MINUTAGE

- Notation `-MM:SS` = **fin** du vers (début = fin du vers précédent). Après 1:50 : tout en dur (secondes explicites).
- Durée EXACTE via ffprobe/mutagen ; les segments somment exactement à la durée audio.
- **Musical-only** : segments intro/outro = image + musique, **sans** texte.
- Traductions FR sous chaque ligne non-Wolof quand requis.
- Cursive : **GreatVibes** (lisible avec contour noir + ombre). Badge : **Pacifico**.

---

## 🎞 5. MONTAGE PIPELINE

1. Frames (PIL) : resize/letterbox + badge **haut-gauche** + texte cursive animé (vague) → JPEG q92.
2. Clips silencieux : `-loop 1 -i frame.jpg -t dur -f lavfi -i anullsrc=... -c:v libx264 -preset veryfast -crf 23 -pix_fmt yuv420p -r 24 -c:a aac -b:a 128k`.
3. Concat demuxer `concat.txt` → `-f concat -safe 0 -c copy`. **Zéro trou noir.**
4. Burn + mux : `-vf ass=subs.ass` (si sous-titres) + `-af afade=t=in:st=0:d=0.3,afade=t=out:st=DUR-3:d=3` + `-vf fade=t=out...` et mux audio.
- Deux exports : **9:16** 1080×1920 (`*_9x16_vN.mp4`) et **16:9** 1920×1080 (`*_16x9_YT_vN.mp4`).

---

## 🎧 6. MASTERISATION MP3 (livrable)

- Sortie `livrables/*_MASTER.mp3`.
- Objectif **-14 LUFS** (vérifié ebur128), true peak ≤ -1,5 dBTP, LRA ~11.
- Nettoyage : `highpass=f=30, lowpass=f=18000`.
- 2 passes loudnorm `linear=true` avec mesures exactes (sinon 1 passe dynamique).
- Durée conservée (pas de coupe).

---

## 🖼 7. COVER DE PUBLICATION (TikTok + YouTube)

- Visuel : couple (style **Disney/anime** inspiré des photos de l'artiste) + **éclair doré** + **cœur lumineux** + dégradé cyan/ambre.
- Titre en **grande cursive GreatVibes** + sous-titre (nom de l'artiste).
- **@daiskypro** en **haut-gauche** avec petit éclair doré (badge).
- Deux formats : `cover_daïsky_9x16.jpg` (1080×1920) et `cover_daïsky_16x9.jpg` (1920×1080), dans `livrables/`.

---

## ✅ 8. VÉRIFICATIONS OBLIGATOIRES AVANT COMMIT

1. Durée exacte (audio ±0,3 s).
2. Blackdetect → **0 trou noir > 300 ms**.
3. Frame-by-frame des 30 dernières secondes + sections clés : minutage OK, badge identique (haut-gauche, zéro dérive), vers intacts, musical-only respecté.
4. Aucune ligne coupée (wrap auto).
5. Poids cohérent.
6. Cover : titre lisible, @daiskypro présent, both formats.
7. MP3 master : -14 LUFS, durée complète.

---

## 📦 9. TÉLÉCHARGEMENTS (Termux / Android) — REPRENABLE

- Destination : `/storage/emulated/0/Web+/`.
- Nettoyage fichiers cassés (`find . -name "*.mp4" -size -100k -delete`).
- `curl -fL --retry 5 --retry-delay 3 -C - -o "nom.mp4" "https://raw.githubusercontent.com/Stein500/lyric/<COMMIT_HASH>/livrables/..."`.
- Toujours donner le **hash** du commit.

---

**Signature :** « Wolof TechStein beat wê ! » ⚡
