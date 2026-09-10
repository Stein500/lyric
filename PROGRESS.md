# 🎬 PROGRESS — « Guerrier » (Daïsky) · clip lyrics

**Charte de prod :** `PROMPT_UNIVERSEL_v4.9.3.md` (badge DSKY✓ haut-centre · stickers cœurs ❤️💞)
**Sources :** `Guerrier* Daïsky.mp3` + `guerrier.txt` (LRC horodaté)

## ✅ Étape 1 — Analyse MP3 + validation paroles (2026-09-10)
- [x] Environnement reconstruit (`work/setup_env.sh` : venv + imageio-ffmpeg + mutagen + numpy + pillow + matplotlib)
- [x] Durée décodée : **206,40 s (3:26.4)** · 48 kHz stéréo · MP3 192 kb/s (cover 360×360 embarquée)
- [x] Loudness source : **-13,66 LUFS / -1,64 dBTP / LRA 3,9** (déjà quasi conforme -14/-1,8 ; repasse mastering §11 tout de même)
- [x] Tempo : pulse **~160 BPM (feel half-time ~80)**
- [x] Structure : intro tag ×4 (0:02-0:24) → refrain 1 (0:35-0:55) → tag crié (1:08) → couplet 8 lignes (1:23-1:58) → refrain 2 = refrain 1 (1:59-2:19) → tag crié (2:26) → couplet/pont 5 lignes (2:35-3:11) → outro instrumentale ~15 s
- [x] **Paroles validées 28/28** : chaque timestamp correspond à un onset vocal réel (+0,00 à +0,38 s) → avec l'avance d'affichage 0,03 s, tout est conforme §0.2
- [x] **Aucun passage instrumental > 20 s** (max ~16 s) → pas d'images solo obligatoires ; outro ~15 s couverte par le fond endcard

## 🧮 Budget images présenté à l'artiste (RÈGLE 1 — §7)
28 lignes → **17 lignes uniques** (tag ×6 dédupliqué, refrain 2 = refrain 1, chaque ligne chorus dédupliquée) :
- option **strict** : 17 uniques + 2 (intro + endcard) = **19 images/format** (1 seule image pour les 6 « Wolof TechStein beat wê! »)
- option **recommandée** : +1 image tag « crié » milieu (1:08) +1 image tag final (2:26) = **21 images/format** (3 moments de tag distincts : intro ×4 / cri 1:08 / cri 2:26)
- ×2 formats (9:16 + 16:9) + 1 base cover → salves de 10 max.

## ✅ Étape 2 — Décisions artiste (2026-09-10)
- [x] **Charte : HYBRIDE B+A** — couplets/tags en Dark Trap B (nuit, éclairs cyan/ambre), refrains « On est africains » en coucher de soleil doré A (lumière max), pont/outro décrescendo ambre, endcard sombre épuré.
- [x] **Budget : 21 images/format** (17 uniques + intro + endcard + 2 images tag dédiées) → ×2 formats = 42 images + 1 base cover. Salves de 10 : P-1(10) P-2(10) P-3(1) / L-1(10) L-2(10) L-3(1).
- Plan des slots (verse → image) :
  - s00 intro_bg (0→2.71) · f01 tag_intro (×4 : 2.71/8.48/14.59/20.17) · f02 africains (35.51/41.78/119.75/125.98) · f03 blanc_de_coeur (47.80/131.58) · f04 on_avance (51.83/135.74) · f05 tag_cri_1 (68.01) · f06-f13 couplet 1 (83.90→114.07) · f14 tag_cri_2 (146.76) · f15-f19 couplet 2/pont (155.88→187.19) · f20 endcard_bg (fondu final ~202s → fin + apad 5 s)

## ⏳ À venir (ordre §1)
- [ ] Image d'ancrage + maquette badge/stickers → validation
- [ ] Salves images portrait 9:16 puis paysage 16:9
- [ ] Rendu 9:16 v2 + cursive → vérifs §12 → 16:9 → MP3 master + tags → covers
- [ ] Teaser autonome (§17)

## 🚨 Dérogation validée artiste (2026-09-10) — BLOC HÉROS GUERRIER
Le bloc héros universel (andogyne clair) est **remplacé pour « Guerrier »** par un héros **noir africain** (demande artiste : le personnage doit cadrer avec « On est africains ») :
`the same Black African hero, mid-thirties, proud strong features, deep brown skin, short natural black hair, mixed masculine and feminine grace, open dark silk shirt, thin silver chain`
→ régénération des ancres B/A puis des salves P1/P2 avec ce bloc. Les scènes de foule/reines/ancêtres montrent des visages africains.
