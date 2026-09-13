# 🎬 PROGRESS — « Je crache mes démons » (Daïsky Prod / TechStein)

Branche : `arena/01a09a22-lyric` · Référence : `PROMPT_UNIVERSEL_v4.8.2.md`
Dernière mise à jour : étape 1 (analyse + questions de décision)

---

## 1. ANALYSE (étape 1 — FAIT)

### Audio
| Item | Valeur |
|---|---|
| Fichier | `Je crache mes démons.mp3` |
| Durée décodée | **210,02 s (3:30.02)** |
| Bitrate / SR | 184 kbps (VBR) · 48 000 Hz |
| Loudness intégrée | **−13,9 LUFS** (cible −14) |
| True Peak | **−1,3 dBFS** (cible ≤ −1,5 après décodage) |
| LRA | 5,9 LU |
| Dernier son utile | **207,82 s (3:27.8)** → silence/fondu final jusqu'à 210,0 s |

→ Masterisation : quasi conforme. Repasse 2 `loudnorm` à prévoir en fin de chaîne
(cible I=−14 / TP=−1,8) pour sécuriser ≤ −1,5 dBTP après décodage MP3.

### Paroles (`Je crache les démons.txt`)
| Item | Valeur |
|---|---|
| Sections | INTRO · REFRAIN (×3) · COUPLET 1 · PRÉ-REFRAIN (×2) · COUPLET 2 · PONT · OUTRO |
| Lignes totales | **65** |
| Lignes **uniques** | **39** |
| Déduplication | refrain ×6 (4 lignes) · « Wolof TechStein beat wê ! » ×3 · pré-refrain ×2 (4 lignes) |

**Budget images (règle §7.1)**
- 9:16 → `39 uniques + 2 (fond intro musical + endcard)` = **41 images**
- 16:9 → **41 images**
- **Total = 82 images** (+ bases cover ×2) → **9 salves de 10 par format** (10+10+10+10+1)

### Photos de référence (héros)
- `Sam/` → 2 vidéos (Snapchat-174169237.mp4, Snapchat-2050730153.mp4) → frames extraites dans `work/refs/`
- `Samu/` → 13 photos (Snapchat-*.jpg)
- ⚠️ Session sans vision : l'IA **ne peut pas décrire** les photos elle-même.
  Elles sont utilisées comme **images de référence** passées au générateur, et
  l'artiste valide le **bloc héros écrit** (question 4).
- Consigne artiste : **peau foncée, pas musclé, aucune embellissement** (corps
  réel, mince/normal, pas de définition musculaire, pas de « beauté » idéalisée).

---

## 2. DÉCISIONS (étape 2 — EN ATTENTE DE VALIDATION)

- [ ] Titre exact pour cover / intro / endcard
- [ ] Charte graphique (A / B / hybride)
- [ ] Budget images final (41 ou réduit)
- [ ] Bloc héros + usage des photos Sam/Samu
- [ ] Paroles : texte conservé tel quel ou retravaillé
- [ ] Timing endcard (proposition : 3:25.0 → total ≈ 3:35 avec apad 5 s)

---

## 3. PIPELINE À VENIR (§1 ordre de production)

1. ✅ Analyse audio + paroles
2. ⏳ Décisions artiste
3. ⏳ Image d'ancrage (1 par charte) + maquette badge/vers → validation
4. ⏳ Salves de 10 max/session (planche contact → validation → salve suivante)
5. ⏳ Pré-calcul fonds → rendu 9:16 → vérifs §12 → 16:9 → MP3 master + tags → covers
6. ⏳ Teaser 2 images + CTA (v4.8.2) · commit + push après chaque étape

**Signature :** « Wolof TechStein beat wê ! » ⚡
