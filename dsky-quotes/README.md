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
│   ├── photos-originales/         ← photos sources (photos studio + dossiers Samu / Samuel)
│   └── fonts/                     ← Playfair Display + Montserrat (OFL)
├── salve-01 … salve-04/
│   ├── post/                      ← 1080×1350 (4:5) — feed IG / FB
│   └── story/                     ← 1080×1920 (9:16) — story / statut WhatsApp
├── salve-05/                      ← citation 41 (la finale) + couverture cover-post/cover-story
├── salve-0N.json                  ← métadonnées (texte, style, base) de chaque salve
├── compose.py                     ← moteur de composition (texte, badge, signature, drapeau 🇧🇯)
├── cover.py                       ← générateur de couverture
├── push.sh                        ← push main + branche légère en 1 commande
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
# 1. Générer les bases IA (une par citation, visage préservé) → assets/bases/base-XX.jpg
# 2. Renseigner salve-0N.json (num, style, base, text)
# 3. Composer :
python3 compose.py 01     # → salve-01/post/*.jpg + salve-01/story/*.jpg
```

## 🗺️ Planning des salves

- [x] **Salve 01** — citations 1 → 10
- [x] **Salve 02** — citations 11 → 20 *(photos réelles de l'auteur, grading cinéma par citation)*
- [x] **Salve 03** — citations 21 → 30 *(fonds studio/cinéma régénérés, texte hors visage)*
- [x] **Salve 04** — citations 31 → 40 *(les 3 photos studio d'origine, 10 fonds uniques)*
- [x] **Salve 05** — citation 41, la finale *(+ couverture « PENSÉES d'un Lyriciste béninois »)*

---

© 2026 C. Jésutondji Samuel Stein — Visuels générés par IA d'après les photos de l'auteur.
Polices : SIL Open Font License.


---

# 🎤 SAISON 2 — « Le voyage du parolier » (45 → 54)

- **Format** : Story 1080×1920 uniquement
- **Images** : 100 % IA (scènes anonymes — silhouettes, objets, foules) — aucune photo de l'auteur
- **Citations** : écrites par l'IA pour l'auteur, dans sa voix de lyriciste
- **Nouveauté** : barre CTA intégrée — *Like · Commente · Partage · Abonne-toi*
- **Moteur** : `compose_s2.py` + `saison-02.json` → `saison-02/story/`

---

# 🖤 Les Vraies (55 → 64)

- **Format** : Story 1080×1920 uniquement — `saison-02/story/`
- **Citations** : thèmes imposés par l'auteur, écrits dans sa voix (*l'argent, le cœur, la rue…*)
- **Visuels** : 100 % IA anonymes, une ambiance par citation

---

# 🎨 Série ART (65 → 90)

Série ART I→IV (65 → 100). La citation est **typographiée par l'IA à l'intérieur de l'œuvre elle-même**
(effet chic, vocabulaire simple). Le code n'ajoute plus que le branding : badge `DSKY 🇧🇯`,
N°, signature, drapeau et barre CTA dans la bande basse — moteur `compose_art.py`.

*Lisibilité d'abord : lettres grandes, horizontales, fort contraste.*

| # | Thème | Style de l'œuvre |
|---|---|---|
| 65 | Le travail | constructivisme russe |
| 66 | La passion | anime flamboyant |
| 67 | La musique | BD africaine |
| 68 | La famille | Disney/Pixar |
| 69 | Les faux amis | ligne claire (ombre au poignard) |
| 70 | Le temps | Art Déco |
| 71 | Le silence | estampe ukiyo-e |
| 72 | Pardonner | vitrail gothique |
| 73 | Temps & argent | Bauhaus / style suisse |
| 74 | La jalousie | timbre gravé |
| 75 | L'amour vrai | Ghibli aquarelle |
| 76 | L'échec | affiche de film |
| 77 | La discipline | comics américain |
| 78 | La vérité | papercut renard & loup |
| 79 | La mère | mosaïque kente |
| 80 | Le rêve | fresque urbaine |
| 81 | La trahison | néo-noir cinématographique |
| 82 | L'ami & ta place | huile, bar feutré |
| 83 | Le boulot | affiche suisse |
| 84 | Le sourire qui sauve | supérette africaine la nuit |
| 85 | Tomber amoureux | gouache, taxi au crépuscule |
| 86 | Les petits bonheurs | illustration conte |
| 87 | La déception | comic book noir & rouge |
| 88 | Les rêves reportés | anime nostalgique |
| 89 | Les masques | nature morte baroque |
| 90 | Le vrai amour | cuisine à 1 h du matin |
| 91 | Le capital confié | huile Caravaggio (ailes noires) |
| 92 | Les secrets | surréalisme Magritte |
| 93 | La réussite | escalier de marbre dans la brume |
| 94 | Le serpent | miniature persane |
| 95 | L'aube de la ville | marché de l'aube |
| 96 | La pluie | aquarelle nocturne, tôle |
| 97 | L'honnêteté | linogravure taximan |
| 98 | Le je t'aime des nôtres | photo familiale |
| 99 | Le message relu | photo nocturne |
| 100 | Le masque de l'argent | portrait baroque doré |
| 101 | Les deux rires | pop art (Warhol) |
| 102 | Le conseiller | théâtre d'ombres wayang |
| 103 | L'argent & la rue | crépuscule, deux mondes |
| 104 | L'acteur | expressionnisme muet |
| 105 | Le but du quartier | affiche foot rétro |
| 106 | L'appel de loin | nocturne, téléphone ancien |
| 107 | Vingt ans | mains au marché |
| 108 | La paix signée | jazz Harlem |
| 109 | Le nom | sceau de cire |
| 110 | L'heure juste | Catrina au sablier |
| 111 | La confiance fêlée | kintsugi à l'or |
| 112 | La main sous la nappe | noces N&B |
| 113 | Le SMS de paie | risographie |
| 114 | Le vieux père | cyanotype |
| 115 | Le visage du matin | Art Nouveau (Mucha) |
| 116 | Le bonjour banal | quai de gare années 50 |
| 117 | Le projet murmuré | sumi-e |
| 118 | La dignité | studio Sidibé 1960 |
| 119 | La clé de la confiance | mosaïque byzantine |
| 120 | Le miroir du matin | marbre antique |
| 121 | Ton prime c'est maintenant | affiche boxe rétro |
| 122 | Le défi grandit | chevalier & dragon |
| 123 | Ton prime (intégrale) | athlétisme années 70 |
| 124 | Devenir prêt | pub années 50 |
| 125 | La collection de peurs | Tim Burton |
| 126 | Le premier pas | Bauhaus |
| 127 | Le signal | torche & montagne |
| 128 | Le défi (intégrale) | roman graphique 2 cases |
| 129 | L'obstacle pousse | gravure botanique |
| 130 | Le monstre de demain | ombre de dragon |
| 131 | L'habitant du recul | cirque, funambule |
| 132 | Terrasse aujourd'hui | silhouettes Reiniger |

Textes intégraux : `citations/citations_corrigees.md` (sections Série ART, ART II, ART III).

---

© 2026 C. Jésutondji Samuel Stein — Visuels 100 % IA. Polices : SIL Open Font License.

### 📱 Version TIKTOK (`saison-02/tiktok/` — moteur `compose_art_tt.py`)
Mêmes œuvres, mais branding remonté en **zone sûre TikTok** : signature + CTA terminent à ~1630 px,
**290 px libres en bas** pour le pseudo / la légende / le titre musical de TikTok — rien n'est masqué.
