# DSKY QUOTES 🇧🇯

> **Citations — C. Jésutondji Samuel Stein « Dsky »** · Lyriciste · Bénin
> Série de quotes 100 % IA : portrait fidèle (aucune modification du visage), fonds réinventés,
> typographie professionnelle incrustée par programme (Playfair Display & Montserrat).

---

## 📁 Structure

```
DSKY-QUOTES/
├── citations/
│   └── citations_corrigees.md     ← les 41 citations corrigées & affinées (féminins marqués)
├── assets/
│   ├── bases/                     ← visuels IA générés à partir des photos originales
│   └── fonts/                     ← Playfair Display + Montserrat (OFL)
├── salve-01/
│   ├── post/                      ← 1080×1350 (4:5) — feed IG / FB
│   └── story/                     ← 1080×1920 (9:16) — story / statut WhatsApp
├── salve-01.json                  ← métadonnées (texte, style, base) de la salve 01
├── compose.py                     ← moteur de composition (texte, badge, signature)
└── README.md
```

## 🎨 Direction artistique (style « mix »)

| Style | Ambiance | Usage |
|---|---|---|
| `LUXE` | noir & or, chiaroscuro | citations fortes, dignité, argent |
| `MINIMAL` | dégradés doux, épuré | réflexions, relations |
| `AFRO` | couleurs du Bénin, énergie urbaine | punchlines, fierté, humour |

**Charte** : badge pilule `DSKY 🇧🇯` (drapeau béninois vectorisé) en haut à gauche ·
numéro de la citation à droite · citation centrée dans le tiers supérieur ·
signature `C. JÉSUTONDJI SAMUEL STEIN — LYRICISTE · BÉNIN` en bas.

## 🔁 Reproduire / étendre

```bash
# 1. Générer les bases IA (une par citation, visage préservé) → assets/bases/base-XX.png
# 2. Renseigner salve-0N.json (num, style, base, text)
# 3. Composer :
python3 compose.py 01     # → salve-01/post/*.png + salve-01/story/*.png
```

## 🗺️ Planning des salves

- [x] **Salve 01** — citations 1 → 10
- [x] **Salve 02** — citations 11 → 20 *(photos réelles de l'auteur, grading cinéma par citation)*
- [x] **Salve 03** — citations 21 → 30 *(fonds studio/cinéma régénérés, texte hors visage)*
- [x] **Salve 04** — citations 31 → 40 *(les 3 photos studio d'origine, 10 fonds uniques)*
- [ ] **Salve 03** — citations 21 → 30
- [ ] **Salve 04** — citations 31 → 40
- [ ] **Salve 05** — citation 41 (clôture)

---

© 2026 C. Jésutondji Samuel Stein — Visuels générés par IA d'après les photos de l'auteur.
Polices : SIL Open Font License.
