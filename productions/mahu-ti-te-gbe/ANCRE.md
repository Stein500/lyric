# ANCRE — « Mahu ti tè gbè » (Dsky) · production 2026-10-10

Règles appliquées : **PROMPT UNIVERSEL v5.7 « Mariage parfait »** (§0 → §7), plus la demande explicite du jour :
*l'IA écrit les mots directement dans l'image, avec icônes et stickers* (donc **pas** de sous-titrage incrusté après coup).

---

## 1. Source et mesures réelles (vérifiées, pas déclarées)

| Mesure | Valeur | Comment |
|---|---|---|
| Fichier | `Mahu ti tebe Eng.mp3` | déposé le 2026-09-? / commit `b08f97b0` (2026-10-09 17:14:53 UTC) |
| Durée décodée | **206,40 s** (0:03:26.42) | `ffmpeg -map 0:a:0 -f null -` → concorde avec `[length:03:26]` du fichier texte |
| Échantillonnage | 48 000 Hz, stéréo, MP3 ~185 kb/s (VBR) | sonde ffmpeg |
| Vraie crête | **+0,06 dBTP** → dépasse 0, **écrêtage numérique présent** | `loudnorm` pass 1 (`input_tp`) |
| Loudness | **−13,58 LUFS**, LRA 9,3 | `loudnorm` pass 1 (`input_i`, `input_lra`) |
| Pochette embarquée | 360×360 mjpeg → trop petite | à remplacer par une cover 1080 |
| Silences ≥ 3,5 s à −42 dB | **aucun** | morceau continu → les fenêtres libres viennent des chronomètres des paroles, pas du silence |
| Paroles | **49 vers** chronométrés, 9,33 s → 196,07 s | `Mahu ti tè gbè.txt` → normalisé en `timings_source.lrc` |

Maillage d'affichage §6 : 154,7 s couvertes sur 206,4 s (75 %) — aucune correction de copier-coller nécessaire,
les horodatages de l'artiste sont gardés tels quels.

**Fenêtres sans texte ≥ 5 s** (calculées, §4 : clochettes premium) :
`9,33→17,24` (7,91 s) · `17,24→26,06` (8,82 s) · `38,50→44,25` (5,75 s) · `97,52→103,10` (5,58 s) ·
`166,97→172,39` (5,42 s) · `172,39→182,73` (10,34 s) · `182,73→189,46` (6,73 s) · `189,46→196,07` (6,61 s) · `196,07→206,40` (10,33 s → carte finale).
Intro `0→9,33` : carte d'accueil (§3), pas de clochette.

## 2. Direction artistique — les 6 techniques que je choisis

Nom du look : **« ENCRE & FEUILLE D'OR — la nuit qui finit bien »**.

1. **Peinture numérique + feuille d'or** : matière peinte (gouache épaisse, couteau), tous les contours divins tracés en or (filet, halo, icônes).
2. **Clair-obscur Rembrandt** : une seule source chaude par image (lanterne, lampe de rue, bougie, phare, aube), le reste en bleu nuit `#0B1B2A`.
3. **Pluie, vapeur, grain 35 mm** + léger motion blur directionnel → les 20 images se suivent comme des *frames* réelles (continuité de pose, de pas, de regard).
4. **Lettrage peint dans l'œuvre** (pas d'incrustation) : capitales dorées, serif condensée à empattements fins, mot actif en or vif, reste crème `#F3E7D3`.
5. **Icônes & stickers dorés intégrés à la matière** : colombe au trait, lanterne, bougie, mains ouvertes, ancre de marine, clé, enveloppe, flèche, pastille gommée, étoile filante — jamais en surimpression propre, toujours touchés par la lumière de la scène.
6. **Palette fermée** : bleu nuit, teal, ambre `#E8A33D`, or `#D9A441`, crème. Aucun drapeau, aucun logo, aucune marque.

## 3. Ancre personnages (à valider avant la salve 2)

- **L'homme** — même description recopiée mot pour mot dans chaque prompt : *homme noir d'une trentaine d'ans, peau mate foncée, cheveux en courtes locks, **chemise de lin crème fermée jusqu'au col**, fine chaîne de laiton avec petite croix, pantalon sombre, pieds nus dans une flaque ou bottes de toile selon la scène*. Visage : mâchoire serrée, yeux levés vers la source de lumière, émotion contenue.
- **La présence** — jamais un dieu barbu ni un ange littéral : un **filet de lumière dorée** qui traverse l'image, parfois une **colombe** au trait d'or, jamais un deuxième corps qui touche l'homme.
- Tenues fermées et élégantes, accent sur le visage et l'attitude. Nu : **aucune pose de nu, aucune anatomie suggérée** — les points 11 à 13 de `Instructions A.txt` sont **annulés** par §2 de v5.7, et cette production les applique tels quels ne les applique pas.

## 4. Typographie dans l'image (règle propre à cette chanson)

| Élément | Règle |
|---|---|
| Accroche | `MAHU TI TÈ GBÈ` en capitales d'or, écrite **par le générateur** dans la matière |
| Mot actif du vers | or vif `#D9A441`, légèrement plus grand |
| Suite du vers | crème `#F3E7D3`, serif condensée |
| Icônes | 1 à 3 maximum par image, dorées, collées au sens du mot (lanterne = « light », colombe = « spirit », mains = « carries me ») |
| Stickers | pastilles, flèches, petits traits d'accent, cercles gommés, compteur `0326` |
| Zones interdites | rien sur `y 0→144` ; rien à droite de `x ≥ 910` entre `y 960→1690` ; rien sous `y 1574` |
| Largeur de texte | ≤ 740 px sur 1080, centrée, dans la bande `y 620→1340` |
| Orthographe | exactement `MAHU TI TÈ GBÈ` (graves sur les deux E) ; aucune lettre parasite |

## 5. Livrables attendus à la fin

1. 19 fonds 9:16 typographiés (`fonds/scene-01..19.png`) + 1 pochette carrée 1080.
2. Master MP3 320 kb/s / 48 kHz, loudnorm 2 passes (−14 LUFS, −1,5 dBTP), ID3 `TIT2`/`TPE1`/`TALB` + `APIC` 1080 + `USLT` propres (l'écrêtage +0,06 dBTP de la source est corrigé par le true-peak limit).
3. `LIVRAISON_mahu_ti_te_gbe.md` : Titre · Captions · Hashtags · déclaration IA · commandes Termux sur le hash d'après push.
4. Prompt universel à jour (v5.8) intégrant la typo peinte + les icônes.

- **Titre exact** : `Mahu ti tè gbè` · artiste : **Dsky** · signature : *Wolof TechStein beat wê !*
- **Code de fin** : `0326` — la chanson dure 3 min 26 s (« commente 0326 »). Drapeau : **aucun**.
