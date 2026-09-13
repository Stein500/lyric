# 🎬 PROMPT UNIVERSEL DE PRODUCTION LYRICS — v4.9 (« Je crache mes démons » : cold-open, DSKY✓, quotas, pièges audio, héros fidèle)

**Artiste :** Daïsky · **Production de référence :** *Je crache mes démons* (9:16, 3:41, hook 6 s + 210,02 s + apad 5 s)
**Utilisation :** Référence OBLIGATOIRE pour tous les clips lyrics Daïsky Prod / TechStein. Toute déviation doit être validée par l'artiste.
**Remplace :** v4.8.2 (les mises à jour « à intégrer » de la v4.8.2 sont INTÉGRÉES ici).

---

## 🚨 0. MISES À JOUR INTÉGRÉES (validées artiste sur *Je crache mes démons*)

1. **PLUS DE TEASER FINAL.** Le teasing est remplacé par un **COLD-OPEN en tête de vidéo** :
   - **4 à 6 s** (validé : **6 s**) qui jouent **la partie croustillante du morceau** (extrait audio du refrain explosif, ici 21.5→27.5 s = 2 lignes refrain) AVANT l'intro musicale.
   - Visuel cold-open : images des 2 lignes chantées (slots refrain) + **titre cursive en haut** + **icônes CTA** ; puis coupe propre vers l'intro (fond s00 + titre + Daïsky).
   - Structure temporelle : `TOTAL = HOOK + durée_chanson + apad(5 s)` ; toutes les fenêtres de vers sont décalées de `HOOK` (ici 6.0 s).
2. **Icônes like / s'abonner / commenter** visibles **les 2 premières secondes** (fondu entrée 0,3 s / sortie 0,4 s).
3. **Badge = `DSKY✓`** (carte opaque + liseré cyan + éclair polygonal, DejaVu Sans Bold) **AU MILIEU EN HAUT** (y = 36 px), discret et visible, posé en POST en dernier sur TOUTES les frames + covers. Remplace « ⚡ DAÏSKY PROD » haut-gauche (⚡ reste dans la signature endcard).
4. **Icône partage** « ultra cool » générée par l'IA (fond noir → composite screen/alpha luminance) affichée **au milieu de la vidéo** (`TOTAL/2 ± 2,5 s`, pulse 1,4 Hz, fondu 0,4 s).
5. **RÈGLE ANTI-MÉLANGE (validée artiste : « que les icônes et textes ne soient pas mal mélangés »)** : aucun élément UI ne chevauche un glyphe de paroles. Positions canoniques 9:16 : badge y=36 centré · titre hook/intro y≈210-300 · paroles base bas H−300 (sprite top H−300) · **CTA rangée centrée en bas y = H−30−h_cta (h_cta = 72 px)** → ≥ 13 px sous les descenders · icône partage y = 0,40×H. Vérif bbox obligatoire avant rendu.

##  0bis. DÉSYNCHRONISME — RÈGLES D'OR (inchangées, prouvées)

1. **SOLUTION A — FLUX CONTINU FRAME-ACCURATE** : un seul flux de `ceil(TOTAL × FPS)` frames, frame `i` ↔ `t = i/FPS` ; vers affectés **par temps** ; encodage image2pipe mjpeg → libx264 en une passe ; mux audio (`apad`, `afade`) + `vf fade` out final. Interdits : concat demuxer vidéo, clips séparés.
2. **RÈGLE DES 0,03 s** : vers affichés avec 0,03 s d'AVANCE (`d0 = t0 − 0,03`) ; fonds sur l'horloge musique.
3. **Aucune image statique** : Ken Burns (canvas 1,1× : 1188×2112) zoom 1,02→1,08 alterné par slot + pan sinusoïdal + **vague eau continue** sur les paroles (ampl. ~4,5 px, 0,9 Hz, phase par colonne) ; apparition staggered ~0,9 s (délai par colonne), disparition cascade inversée.
4. **Cursive = ligne connectée** (jamais lettre par lettre) — GreatVibes.

## 🧭 1. ORDRE DE PRODUCTION (séquence validée)

1. Analyse MP3 (durée décodée, LUFS/TP passe 1, structure) + **validation paroles** (§1bis).
2. Décisions artiste : charte, héros, formats, hook, CTA (questions structurées).
3. Ancres (1/charte) + maquettes badge/vers/CTA → **validation artistique**.
4. Salves de **10 images max** (§7bis) → planche contact → validation → salve suivante.
5. Pré-calcul fonds → rendu 9:16 → vérifs §12 → MP3 master + tags → covers 100 % IA.
6. **Commit + push après CHAQUE étape** (branche `arena/<id>-<slug>`).

### 1bis. VALIDATION PAROLES (méthode prouvée)
- Force d'onset = flux spectral − 1,15 × médiane locale (fenêtre 4 s) ; pic = onset ; tolérance **±0,35 s**.
- **Monotonie obligatoire** + **fenêtre mini 1,2 s** entre vers consécutifs (détecte les timestamps inversés/copiés).
- Correction : motif miroir d'un refrain répété (deltas identiques) + pics audio (piano/bridge) ; corrections journalisées (`work/timings_validated.json`) + **fichier `.lrc` corrigé committé**.
- Cas réel : refrain 1 l3 `36.5→27.0`, l8 `40.0→39.5` ; pont l3 `148.5→146.5`.

## 🖼 7. IMAGES — RÈGLES ABSOLUES (+ 7bis quotas)

- RÈGLE 1 : 1 image par ligne UNIQUE ; répétitions réutilisent (refrain ×3, pré-refrain ×2, tags) ; `N = uniques + 2` (intro + endcard) **par format** ; choix final = artiste.
- RÈGLE 2 : salves de 10 max, planche contact + validation entre salves ; salve refusée = seuls les slots concernés régénérés.
- **7bis QUOTA PLATEFORME : 10 générations d'images PAR TOUR** (= 1 salve/tour, cohérent avec RÈGLE 2). Si un slot est bloqué par la **modération** : reformuler (éviter retenue/prise physique → « poids de fumée », « soutenir un ami »), régénérer le slot seul au tour suivant.
- Nommage : `assets/raw/portrait/s{slot:02d}_<motclé>.png` ; s00 intro ; endcard = s{N+1}.
- **Post-contrôle** : ratio, aucun texte/llettre/chiffre (régénérer si enseigne néon avec idéogrammes !), héros conforme.

## 🧱 16bis. BLOC HÉROS DAÏSKY (fidèle aux photos Sam/Samu — validé artiste)

> `semi-realistic anime-seinen cinematic style, the same young Black man in his early twenties, slim non-muscular build, short dark hair faded at the sides, small chin goatee, no glasses, simple grey zip-up jacket with colorful wax-print sleeves, thin silver chain, faithful ordinary face, not idealized, not muscular`

- **ANTI-EMBELLISSEMENT (règle d'or artiste : « je ne suis pas musclé, ne m'embellis pas »)** : silhouette mince jamais musclée, visage ordinaire fidèle, pas de glorification corporelle.
- Suffixes canoniques : **B** nuit (`deep blue-black night, warm amber backlight, subtle electric cyan rim light, wet asphalt reflections, atmospheric haze, crushed blacks with cyan highlights, moody anime-seinen cinematic grading, 35mm film grain`) · **A** pont (`warm golden sunset backlight, … moody romantic cinematic grading`) ; hybride B+A validé.
- 7 blocs obligatoires par prompt (cadrage, sujet, bloc héros, plan, suffixe, zone texte, interdits + `no signage`).

## 🎞 9. MONTAGE (SOLUTION A) — structure cold-open

1. Fonds : cover-resize LANCZOS → canvas 1188×2112 → JPEG q92 (`work/fonds_portrait/f{slot:02d}.jpg`).
2. Frames : hook (slots refrain + titre haut + CTA 0-2 s) → intro (s00 + titre + Daïsky jusqu'à 1ʳᵉ voix) → vers (avance 0,03 s, vague eau) → icône partage au milieu → endcard (fondu final + apad 5 s) ; badge DSKY✓ dernier.
3. Mux : audio = **hook + chanson** masterisé (§11bis) ; `[1:a]apad=whole_dur=T,afade=out:T-3:3[a]` + `[0:v]fade=out:T-3:3[v]` ; **ré-encodage vidéo obligatoire si filtre fade** (`-c:v copy` + filtre = erreur).
4. Export `livrables/<Titre>_9x16_v<N>.mp4` crf19 veryfast aac 192k +faststart. Texte 9:16 : cursive 76 px, max 940 px, sinon 2 lignes (jamais troncature).

## 🎧 11bis. AUDIO — PIÈGES PROUVÉS

- **Mesure loudnorm : `-v info`** (le JSON passe 1 est émis au niveau info ; `-v error` → JSON absent → crash).
- **Concat hook+chanson : tout décoder en WAV 48 k d'abord** (`concat demuxer` pcm+mp3 = durée tronquée/gain faux) ; puis loudnorm 2 passes ; `offset=` (pas `target_offset=`) ; TP cible −1,8.
- MP3 livrable = **chanson seule** masterisée 320 k + tags §3 (USLT paroles nettoyées) ; mesuré final : −14,19 LUFS / −1,67 dBTP ✓.
- Vidéo = hook+chanson (même chaîne).

## ✅ 12. VÉRIFICATIONS (valeurs mesurées sur la production de référence)

1. Durée = `nb_frames/fps` ±0,05 (3:41.03 pour T=221.02) · streams 1080×1920 30 fps.
2. blackdetect : seul le fade final (black_start ≈ T−0,36).
3. freezedetect = 0.
4. Frontières de vers par diff pixel MP4 vs reconstruction : **1,8–2,6 px** (< 6) à 10.3/112/126/152 s.
5. Badge statique par construction (composé en dernier, sprite unique).
6. Endcard : titre cursive + contacts DejaVu Bold + @daiskypro + signature.
7. MP3 : LUFS/TP/durée/tags.
8. Covers lisibles + badge post.
9. **Audit bbox sprites : marges glyphs ≥ 6 px (mesuré 39 px)** + règle anti-mélange §0.5.

## 🖼 10. COVERS — 100 % IA (confirmé)

- Base générée **AVEC titre intégré** : grande cursive dorée lumineuse + `Daïsky` dessous ; zone sombre haut 9:16 / gauche 16:9 ; orthographe du titre = point de validation ; **badge DSKY✓ posé en post** ; sorties 1080×1920 + 1920×1080 + carré 1080×1080 (APIC).

## 🔤 14bis. POLICES (acquisition prouvée, CDN bloqués)

- GreatVibes : `npm pack @fontsource/great-vibes` → woff2 latin → **fontTools+brotli → .ttf** committé dans `assets/fonts/GreatVibes-Regular.ttf` (coverage complet, « œuvre » inclus) ; DejaVu Sans Bold dans `assets/fonts/`.
- Cursive = paroles + titres intro/endcard/covers UNIQUEMENT ; tout le reste (badge, endcard, contacts) = DejaVu Sans Bold.

## 📜 Historique
- **v4.9** — cold-open 6 s (partie croustillante) remplace le teaser · DSKY✓ milieu haut · CTA 2 s bas centré 72 px + règle anti-mélange · icône partage milieu · quotas 10 gén/tour + contournement modération · validation paroles (monotonie, fenêtre mini, miroir refrain, .lrc) · pièges audio (`-v info`, concat WAV, `-c:v copy`+filtre) · bloc héros DAÏSKY fidèle/anti-embellissement · acquisition polices npm/fontTools · valeurs de vérif de référence.
- v4.8.2 → v4.6 : voir archives `PROMPT_UNIVERSEL_v4.8.2.md`.

**Signature :** « Wolof TechStein beat wê ! » ⚡
