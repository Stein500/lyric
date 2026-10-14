# ANCRE — « Glace » (Dsky) · production 2026-10-14

Règles appliquées : **PROMPT UNIVERSEL v5.9 « Ça bouge, sans voiler la parole »** (§0 → §16), avec **MODE PEINT** validé par l'artiste en réponse à la question obligatoire du §0 (*« Déjà peint »*).

---

## 1. Source et mesures réelles (vérifiées sur les fichiers du dépôt)

| Mesure | Valeur | Méthode |
|---|---|---|
| Fichier audio | `Glace - Daïsky.mp3` | commit `8ab4a05` |
| Durée décodée | **180,00 s** (8 639 999 échantillons à 48 kHz) | `ffmpeg -map 0:a:0 -f null -` (`[length:03:00]` dans `Glace.txt`) |
| Échantillonnage | 48 000 Hz, stéréo, MP3 ~188 kb/s | sonde `ffmpeg` |
| Loudness source | **−13,46 LUFS** (`ebur128` : −13,4 LUFS), LRA **7,00 LU** | `loudnorm` pass 1 & `ebur128` |
| Vraie crête source | **−1,90 dBTP** (sample peak −1,94 dB) | `loudnorm` pass 1 (`input_tp`) & `astats` |
| Master normalisé (`_master_noart.mp3`) | **−14,0 LUFS**, TP **−2,5 dBTP**, crête **−2,48 dB**, LRA **6,7 LU**, 48 kHz 320 kb/s, `-vn` | `loudnorm` 2 passes linéaire + vérification `ebur128` / `astats` |
| Pochette embarquée source | 360×360 mjpeg (`Stream #0:1`) | supprimée sur le master par `-vn`, sera remplacée par `cover-1080.jpg` |
| Paroles | **45 vers** chronométrés de `00:06.03` à `02:45.25` | `Glace.txt` → `timings_source.lrc` (horodatages gardés tels quels) |
| Code de fin | **`0300`** | lié à la durée décodée : 3 min 00 s → `0300` |

### Fenêtres de clochettes CTA (§6 — MODE PEINT, seuil ≥ 4,00 s de temps libre après `[fin_affichage + 0,15 s]`)

- `42,50 → 47,16 s` (**4,66 s** libres après v14 `Je suis la glace, glace, glace (big boss !)`)
- `145,56 → 150,14 s` (**4,58 s** libres après v42 `Je suis la glace, glace, glace (tech !)`)
- `152,49 → 157,79 s` (**5,30 s** libres après v43 `Wolof TechStein ça brûle !... (glace)`)
- `160,14 → 165,25 s` (**5,11 s** libres après v44 `Wolof TechStein ça brûle... (big boss)`)
- `167,60 → 180,00 s` (**12,40 s** libres après v45 `Wolof... TechStein... ça brûle... (Tech...)`)
- Carte d'accueil : `0,00 → 6,03 s` (pas de clochette) · Carte finale : `180,00 → 185,00 s` (code `0300`).

---

## 2. Direction artistique — Recette « ENCRE & FEUILLE D'OR — le cœur sous la glace » (§8)

1. **Peinture numérique matière épaisse + feuille d'or** : gouache et couteau, givre et contours sacrés tracés à la feuille d'or `#D9A441`.
2. **Clair-obscur Rembrandt à source unique** : réverbère ambré `#E8A33D` dans la ruelle nocturne givrée, puis phares / brume urbaine, puis **aube dorée** à partir du refrain final (`124,63 s`) sans retour en arrière de la lumière (§9).
3. **Pluie, cristaux de givre, vapeur froide, grain 35 mm** : continuité de lieu, de météo et de posture d'un plan au suivant.
4. **Typographie peinte dans la matière** : capitales d'or serif condensée pour l'accroche du vers, ligne secondaire en crème `#F3E7D3`, centrée dans la bande `y 620 → 1340`, largeur ≤ 740 px.
5. **Icônes & stickers dorés intégrés (1 à 3 par plan)** : flocon/cristal d'or, cœur pris dans un glaçon d'or, flamme qui fond la glace, oreille + onde sonore, livre ouvert + œil, auréole brisée + aile, main + cœur givré, triangle d'alerte + éclair, silhouettes d'ombres + lune.
6. **Palette fermée** : bleu nuit `#0B1B2A`, ombres teal, ambre `#E8A33D`, or `#D9A441`, crème `#F3E7D3`. Aucun drapeau, aucun logo, aucun contact.

---

## 3. Ancre personnage (figée sur `fonds/scene-01-ancre.png`)

- **Le protagoniste** (recopié mot pour mot dans chaque prompt) : *homme noir fictif d'une fin de vingtaine d'années, peau mate foncée, courtes locks soignées, mâchoire calme et déterminée, portant un col roulé crème fermé sous un manteau de laine bleu nuit à col montant fermé bordé d'un fin filet d'or et de givre, fine chaîne de laiton au col, debout dans une ruelle urbaine mouillée et givrée la nuit sous un réverbère ambré*.
- **Le motif récurrent (§9)** : un **fil de lumière dorée** qui traverse le cadre et relie les icônes dorées.
- **Éthique & zones sûres (§3 & §14)** : tenues fermées et élégantes, visage dégagé, tête entière dans le tiers supérieur (`y > 144`), aucune nudité (points 11–13 de `Instructions A.txt` annulés).
