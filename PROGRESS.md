# 🎬 PROGRESS — « Je crache les démons » (Daïsky Prod / TechStein)

Branche : `arena/01a09a22-lyric` · Référence : `PROMPT_UNIVERSEL_v4.8.2.md`
Dernière mise à jour : étape 2 — décisions validées + images d'ancrage générées

---

## 1. ANALYSE (étape 1 — FAIT ✅)

### Audio
| Item | Valeur |
|---|---|
| Fichier | `Je crache mes démons.mp3` |
| Durée décodée | **210,02 s (3:30.02)** |
| Bitrate / SR | 184 kbps (VBR) · 48 000 Hz |
| Loudness intégrée | **−13,9 LUFS** (cible −14) |
| True Peak | **−1,3 dBFS** |
| LRA | 5,9 LU |
| Dernier son utile | **207,82 s (3:27.8)** |

### Paroles (`Je crache les démons.txt`) → `Je crache les démons - timing.txt`
- 9 sections : INTRO · REFRAIN (×3) · COUPLET 1 · PRÉ-REFRAIN (×2) · COUPLET 2 · PONT · OUTRO
- **65 lignes** → **39 lignes uniques** (refrain ×6, pré-refrain ×2, tag ×3 dédupliqués)
- ⚠️ **CORRECTION v1** : ligne 05 « Je me relève… » marquée `−0:36.5` dans le .txt → hors chronologie. Corrigée en **−0:27.0** (calée sur le refrain 2 : 1:25.0). À confirmer à l'oreille.

### Budget images (§7.1)
- **9:16 = 39 uniques + 2 (fond intro musical `s00` + endcard `s40`) = 41 images** → **5 salves de 10**
- 16:9 = 41 images — **reporté après validation du 9:16** (décision artiste)

---

## 2. DÉCISIONS ARTISTE (étape 2 — VALIDÉES ✅)

| # | Décision | Choix |
|---|---|---|
| 1 | **Titre** (cover / intro / endcard) | **Je crache les démons** |
| 2 | **Charte** | ❌ ni A ni B → **INNOVER : faire l'inverse** des chartes habituelles |
| 3 | **Budget** | **9:16 d'abord** (41 images, 5 salves), 16:9 ensuite |
| 4 | **Héros** | **Héros réaliste inspiré des photos Sam/Samu** — peau foncée, mince/normal, **zéro muscle, aucune embellissement** |
| 5 | **Paroles** | **Texte du .txt conservé tel quel** |
| 6 | **Endcard** | **3:30.0 → 3:35.0** (fin exacte du MP3 + apad 5 s, fade out 3 s) |

---

## 3. CHARTE C / D — « L'INVERSE » (étape 3 — ANCRAGES GÉNÉRÉS, À VALIDER)

> Consigne artiste : innover, faire **exactement le contraire** de A (coucher de soleil doré) et B (nuit éclairs cyan).
> → On quitte la nuit ET le doré romantique : **plein jour, lumière crue, aucune complaisance** (cohérent avec « ne m'embellis pas »).

### Proposition C — « PLEIN JOUR / HIGH-KEY »
Blanc écrasé, soleil au zénith, ombres dures et sèches au sol, béton poussiéreux blanchi, ciel laiteux brûlé,
grain 35 mm, **cyan pâle gardé en filet (identité Daïsky) mais à contre-emploi sur fond clair**.
Symbole : les démons sont crachés **en plein jour**, à visage découvert — rien ne se cache dans le noir.
Arc lumineux **inversé** : intro = lumière plate blanche (vide, exposition totale) → couplets = ombres dures marquées
→ refrains = surexposition solaire → pont = ombre portée douce → outro = retour au blanc vide → endcard = blanc sale.

### Proposition D — « MIDI OUEST-AFRICAIN »
Soleil de midi écrasant, latérite rouge, poussière, bleu ciel dur, palette saturée terracotta/cobalt,
chaleur sèche, grain 35 mm. Symbole : avancer sous le soleil réel, cracher par terre et continuer.

### Suffixe technique C (canonique, à recopier tel quel)
`bleached high-key daylight, harsh overhead sun, hard clean shadows on the ground, pale dusty concrete, milky burnt-white sky, faint pale cyan rim accent, cool hard-edged shadow gradient across the lower third for lyric text readability, 35mm film grain, bleached low-contrast cinematic grading, natural documentary realism, no text, no letters, no numbers, no logos, no watermark, no subtitles, no borders`

### Suffixe technique D
`saturated West African midday light, red laterite earth, hard deep blue sky, vivid terracotta and cobalt palette, dry heat haze, dust particles in the air, faint pale cyan rim accent, hard-edged shadow across the lower third for lyric text readability, 35mm film grain, high-contrast sunlit cinematic grading, natural documentary realism, no text, no letters, no numbers, no logos, no watermark, no subtitles, no borders`

### Bloc héros (à recopier à l'identique dans CHAQUE prompt — ⚠️ À CORRIGER PAR L'ARTISTE)
`the same real young West African man, deep dark brown skin, slim lean natural build, no muscular definition, ordinary un-idealized everyday body, natural short hair, no heroic or glamorous embellishment, plain light cotton shirt and simple trousers`
> Session sans vision : l'IA ne peut pas décrire les photos. Les photos `Samu/` et les frames `Sam/` sont
> passées en **référence** au générateur. **L'artiste doit valider/corriger ce texte** (âge, cheveux, barbe, tenue).

### Fichiers
- `assets/raw/portrait/ANC_C_highkey.png`
- `assets/raw/portrait/ANC_D_midi.png`
- `work/refs/planche_ancrage.jpg` ← planche contact des 2 propositions

---

## 4. SUITE DU PIPELINE (§1 ordre de production)

- [x] 1. Analyse audio + paroles
- [x] 2. Décisions artiste
- [ ] 3. **Validation de l'ancrage (C ou D) + validation du bloc héros** ← EN COURS
- [ ] 4. Salves de 10 max/session (5 salves 9:16) : planche contact → validation → salve suivante
- [ ] 5. Pré-calcul fonds → rendu 9:16 → vérifs §12 → MP3 master + tags → covers
- [ ] 6. Teaser 2 images + CTA like/abonne/commente 2 premières secondes (v4.8.2) · badge **DSKY✓** centre-haut
- [ ] 7. 16:9 YouTube (après validation du 9:16)
- Commit + push après CHAQUE étape · `work/setup_env.sh` reconstruit l'environnement

**Signature :** « Wolof TechStein beat wê ! » ⚡
