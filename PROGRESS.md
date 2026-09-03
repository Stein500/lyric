# 🚧 PROGRESS.md — Clip lyrics « Je suis pauvre mais je kiffe »

**Artiste :** Daïsky · **Label :** Daïsky Prod / TechStein
**Spéc suivie :** `PROMPT_UNIVERSEL_v4.7.md` (la plus récente du dépôt — v4.7 > v4.3 > v4.2)
**Branche :** `arena/01a06299-lyric`
**Dernière mise à jour :** 2026-09-02

---

## 📊 Chiffres mesurés (pas estimés)

| Donnée | Valeur | Comment |
|---|---|---|
| Audio source | `Jsuis pauvre mais je kiffe 2.mp3` | MP3 VBR 186 kb/s, 48 kHz, stéréo |
| **Durée exacte** | **261,04 s (4:21.04)** | 12 529 919 échantillons PCM décodés / 48 000 |
| Loudness entrée | **−13,51 LUFS / −0,12 dBTP / LRA 7,20** | loudnorm passe 1 (`print_format=json`) |
| offset passe 2 | **−0,77** | `target_offset` du JSON → option `offset=` |
| **BPM** | **≈ 106–107** | autocorrélation enveloppe d'énergie |
| Fondu final audio | **253,9 s → 259,6 s** | profil dBFS 1 s + détection de seuil |
| **Nombre de vers** | **62** | parse de `Je suis Pauvre et riche.txt` |
| Fin du dernier vers | **245,00 s (4:05)** | plage explicite artiste `4:01-4:05` |
| Musique sans vers à la fin | **245 s → 253,9 s (≈ 9 s)** | ⚠️ à trancher avec l'artiste |

**Budget images (v4.7 §7, règle « 1 vers = 1 image ») : 62 + 2 = 64 par format.**
→ 64 portraits 9:16 (**7 salves** : 10+10+10+10+10+10+4) + 64 paysages 16:9 (**7 salves**) + 1 base cover ×2.
Slots : `s00` = fond intro musicale (0 → 9 s) · `s01…s62` = vers 1→62 · `s63` = fond endcard.

---

## ✅ Étapes

### 0. Cadre & analyse
- [x] Lecture de la spec la plus récente (`PROMPT_UNIVERSEL_v4.7.md`, 148 lignes)
- [x] Environnement reconstruit : `.venv/` (imageio-ffmpeg 7.0.2, mutagen 1.48.1, numpy 2.4.6, pillow 12.3.0) — `.venv/` et `work/` dans `.gitignore`
- [x] Durée exacte décodée + LUFS/TP/LRA + BPM + structure → `ANALYSE_AUDIO.md`
- [x] Parse des paroles → `work/timing.csv` (62 vers, `work/parse_lyrics.py`, 0 ligne non parsée)
- [x] Contrôle paroles ↔ audio (écarts < 2 s, voir `ANALYSE_AUDIO.md` §4)
- [x] `.gitignore` (livrables/ **pas** exclu)
- [x] PROGRESS.md
- [x] Police **Great Vibes** récupérée via l'API GitHub et commitée dans `fonts/` (457 588 octets, test Pillow OK)

### 1. Décisions artistiques — ✅ VALIDÉES PAR L'ARTISTE (2026-09-02)
- [x] **Charte = HYBRIDE** : B (dark trap / éclairs cyan-ambre) sur couplets + refrains,
      **A (mixte amour / sunset doré)** sur le PONT 178–201 s (**slots 47–54**, vérifié dans `work/timing.csv`) → v4.7 §6
- [x] **Périmètre session = 9:16 d'abord** : 64 images portrait + rendu + vérifs. Le 16:9 en session suivante.
- [x] **Fin (245 → 253,9 s, musique sans vers)** : texte « **Merci** » + `@daiskypro` / Daïsky Prod en ambre.
- [x] **Titre = « Je suis pauvre mais je kiffe » · Année = 2026** (TPE1 `Daïsky`, TALB `TechStein Prod`)

### 2. Image d'ancrage
- [x] Ancrage charte **B** : `assets/raw/portrait/s00_ANCRAGE_darktrap_lightning.png` (768×1376, ratio 0,558 ≈ 9:16, upscale LANCZOS → 1080×1920)
- [x] Ancrage charte **A** : `assets/raw/portrait/s00_ANCRAGE_mixte_amour_golden.png`
- [x] Maquette badge + vers : `assets/maquettes/maquette_badge_verse.jpg` (1080×1920) — script `work/maquette.py`
      · badge pastille semi-transparente + contour cyan + éclair polygonal (pas d'emoji), **fixe en (36, 36)**
      · vers : DejaVu Sans Bold 58, wrap au mot ≤ 920 px, centré, base à H−300, contour noir + ombre
- [ ] **Validation artistique des 2 ancres + de la maquette** (bloquant avant la salve 1)

### 3. Salves d'images — portraits 9:16 (7 salves)
**Style validé par l'artiste :** seinen animé cel-shadé noir/cyan (charte B), héros = le visage des photos `Samu/`
(mince, PAS musclé, gilet gris argenté + wax, lunettes ou non selon la scène). Référence identité :
`Samu/Snapchat-1835992965.jpg` + `1029267384.jpg` (avec lunettes) · `959878741.jpg` + `2142573272.jpg` (sans).

- [x] **Salve 1 portrait (s01–s10)** générée + planche contact `assets/maquettes/planche_salve1_s01-s10.jpg`
      · avec lunettes : s01, s04, s06, s07, s09 · sans lunettes : s02, s03, s05, s08, s10
- [x] Validation artiste salve 1 (« on continue »)
- [x] **Salve 2 portrait (s11–s20)** générée + planche `assets/maquettes/planche_salve2_s11-s20.jpg`
      · avec lunettes : s11, s13, s16, s18, s20 · sans lunettes : s12, s14, s15, s17, s19
- [x] Validation artiste salve 2 (« valide on continue »)
- [x] **Salve 3 portrait (s21–s30)** générée + planche `assets/maquettes/planche_salve3_s21-s30.jpg`
      · avec lunettes : s22, s23, s26, s28, s29 · sans lunettes : s21, s24, s25, s27, s30
- [x] Validation artiste salve 3 (« on continue »)
- [x] **RÈGLE v4.8 (artiste)** : refrains/chorus = mêmes images réutilisées → ajoutée dans `PROMPT_UNIVERSEL_v4.7.md` (ADDENDUM v4.8) + `work/slot_map.csv` (64 slots)
      · réutilisations : 43-46→s21-s24 · 55-60→s03-s08 · 61→s01
- [x] **Salve 4 portrait (s31–s40)** générée + planche `assets/maquettes/planche_salve4_s31-s40.jpg`
      · avec lunettes : s32, s34, s36, s38, s40 · sans lunettes : s31, s33, s35, s37, s39
- [ ] Salve 5 (s41–s42 + pont s47–s54) · [ ] Salve 6 (fonds s00/s63 + s62)
      ⚠️ après salve 6 : supprimer `work/fonds_portrait/f00.jpg f62.jpg f63.jpg` (fallbacks smoke) et relancer make_fonds

### 4bis. Moteur de rendu — ✅ ÉCRIT ET SMOKE-TESTÉ (2026-09-03)
- `work/render.py` : SOLUTION A (flux continu 30 fps, ADV 0,03 s), Ken Burns 1,02→1,08 + pan,
  vague 6 px/0,9 Hz + staggered letters, FR sous les lignes EN, badge statique posé en dernier,
  intro titre Great Vibes (0→9 s), « Merci » 245→253,9, endcard 254→266 (contacts §2),
  fonds pré-calculés `work/fonds_portrait/` (52/64 ok, fallback f01 pour s00/s62/s63 en attendant salve 6).
- Smoke frames vérifiés visuellement : `work/smoke/f_0020` (hook centré ≤920 px, vague ok),
  `f_0002` (intro), `f_0246.5` (Merci), `f_0264` (endcard complet). 0 overflow après fix getbbox. · [ ] Salve 4 (s31–s40)
- [ ] Salve 5 (s41–s50) · [ ] Salve 6 (s51–s60) · [ ] Salve 7 (s00, s61–s63)
- [ ] idem 7 salves paysage 16:9 (session suivante)
- [ ] Base cover

### ⚠️ Reset sandbox survenu le 2026-09-03 (règle anti-reset v4.7 §4 appliquée)
- `.venv/` et `work/` effacés (gitignorés, non snapshotés) → recréés : venv (imageio-ffmpeg, mutagen, numpy, pillow),
  `work/parse_lyrics.py`, `work/planche.py`, `work/ffmpeg`, `work/timing.csv` régénéré (62 vers OK).
- HEAD local retombé à `95db70c` → `git fetch origin arena/01a06299-lyric` + `git reset FETCH_HEAD`
  (remote était à `8885d2a`, tout récupéré à 100 %).

### 4. Rendu (v4.7 §9, SOLUTION A — flux continu frame-accurate)
- [ ] Script `work/render.py` (30 fps, ADVANCE = 0,03 s, vague + Ken Burns, badge posé en dernier)
- [ ] Export 9:16 `livrables/Je_suis_pauvre_mais_je_kiffe_9x16_v1.mp4`
- [ ] Export 16:9 `livrables/Je_suis_pauvre_mais_je_kiffe_16x9_YT_v1.mp4`

### 5. Master MP3 + covers
- [ ] Master 2 passes loudnorm → −14 LUFS / −1,8 dBTP, 320 k, tags ID3 v4.7 §3
- [ ] `livrables/cover_..._9x16.jpg` + `_16x9.jpg`

### 6. Vérifications (v4.7 §12) & livraison
- [ ] Durée ±0,05 s · blackdetect 0 · freezedetect 0 · diff pixel aux frontières · badge statique · endcard
- [ ] Commit + push, `git rev-parse HEAD`, commandes curl `-C -` vers `/storage/emulated/0/Web+/`

---

## ⚠️ Contraintes détectées dans ce sandbox

1. **Réseau partiel** : `github.com` (git) et `api.github.com` ✅ · `raw.githubusercontent.com` ❌ (`SSL_ERROR_SYSCALL`).
   → la police cursive a quand même pu être récupérée **via l'API GitHub** et commitée dans `fonts/GreatVibes-Regular.ttf`
   (457 588 octets, sha256 `8d5098…2d15`, chargée par Pillow : `('Great Vibes', 'Regular')`). Détail dans `ANALYSE_AUDIO.md` §7.
2. **2 CPU / 3,9 Go RAM / 20 Go libres** → rendu 7 980 frames (9:16) en PIL pur : compter plusieurs dizaines
   de minutes par format. Faisable, mais à lancer en processus de fond.
3. ffmpeg n'est **pas** installé système : on utilise le binaire embarqué `imageio-ffmpeg` (lien `work/ffmpeg`),
   jamais commité (v4.7 §4).

**Signature :** « Wolof TechStein beat wê ! » ⚡
