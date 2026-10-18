# ANCRE — « On est réel » (Dsky) · production 2026-10-18

Règles appliquées : **PROMPT UNIVERSEL v5.9 « Ça bouge, sans voiler la parole »** (§0 → §15), combiné aux indications explicites de `Mini prompt On est réel.txt` (*héros Thomas Sankara, Roi Béhanzin, Roi Bio Guéra, nouveaux présidents de l'AES, familles relevées, accent sur ceux qui veulent abandonner mais doivent se souvenir que cela n'est pas une option*).

**État actuel (§1)** : **GÉNÉRÉ / CONTRÔLÉ — PROPOSÉ À LA VALIDATION DE L'ARTISTE** *(aucune validation de l'artiste n'est inventée)*.

---

## 1. Paramètres verrouillés de la production (§2)

```
TITRE        : On est réel
ARTISTE      : Dsky
LANGUES      : français (signature en fon/wolof : « Wolof TechStein beat wê ! »)
PAROLES      : On est Réel.md          (57 lignes = 57 vers, horodatages de l'artiste non retouchés)
AUDIO        : On est réels_1.mp3      (maître fourni par l'artiste, jamais généré)
RECETTE      : ENCRE & FEUILLE D'OR — « la nuit qui finit bien »
CODE DE FIN  : 0405 (4 chiffres, lié à la durée décodée mesurée : 4 min 05 s = 244,99 s)
SIGNATURE    : « Wolof TechStein beat wê ! »
MODE         : PEINT (confirmé par l'artiste : « Peint stp »)
DOSSIER      : productions/on-est-reel/ (fonds/ livrables/ fonts/ + verses_map.json + CARTE-VERS.md)
```

---

## 2. Source audio et mesures réelles (§11 — mesurées, jamais déclarées à peu près)

| Mesure | Valeur mesurée | Méthode |
|---|---|---|
| Fichier source | `On est réels_1.mp3` | PCM 16 bits (`pcm_s16le`) encapsulé sous extension `.mp3`, 48 000 Hz, stéréo, 1 536 kb/s |
| Durée décodée | **244,99 s** (`00:04:04.99`) | `ffmpeg -map 0:a:0 -f null -` → concorde avec `[length:04:05]` → code **`0405`** |
| Loudness source (pass 1) | **−13,39 LUFS**, LRA **7,30 LU** | `loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json` |
| Vraie crête source (pass 1) | **−1,11 dBTP** (seuil −23,76 LUFS) | `loudnorm` pass 1 (`input_tp`) |
| Silences ≥ 3,5 s à −42 dB | **aucun (`[]`)** | `silencedetect=n=-42dB:d=3.5` |
| Master `_master_noart.mp3` | **−14,0 LUFS**, LRA **7,5 LU**, TP **−1,7 dBFS**, crête **−1,75 dB** | `loudnorm` 2 passes linéaires (`offset=-0.24`), 48 kHz, MP3 320 kb/s (`-vn`), contrôlé par `ebur128` + `astats` |
| Paroles chronométrées | **57 vers**, `10,70 s → 244,99 s` | `On est Réel.md` → normalisé sans retouche d'horodatage dans `timings_source.lrc` |

**Fenêtres de clochette éligibles en MODE PEINT (§6 : `[fin d'affichage + 0,15 s → début du vers suivant]`, seuil ≥ 4,00 s)** :
1. Après v-02 : **`17,15 s → 24,48 s`** (7,33 s libres)
2. Après v-50 : **`187,35 s → 193,01 s`** (5,66 s libres)
3. Après v-56 : **`225,11 s → 232,32 s`** (7,21 s libres)
4. Après v-57 : **`234,67 s → 244,99 s`** (10,32 s libres avant la carte finale `244,99 → 249,99 s`)

*(L'intro `0,00 → 10,70 s` est réservée à la carte d'accueil en 2 temps : `0,00 → 4,90 s` et `4,90 → 10,70 s` — aucune clochette pendant les cartes ni pendant la lecture d'un vers).*

---

## 3. Direction artistique — Recette « ENCRE & FEUILLE D'OR — la nuit qui finit bien » (§8 & §9)

1. **Peinture numérique matière épaisse (gouache/impasto) + feuille d'or** : tous les contours héroïques, ancestraux et spirituels sont rehaussés de filets d'or (`#D9A441`).
2. **Clair-obscur Rembrandt à source unique** : lanterne de rue ambrée (`#E8A33D`), bougie ou forge dans la nuit profond bleu `#0B1B2A`, évoluant par paliers continus (nuit → crachin → brume → **aube dorée** à partir du pont et du refrain final, avec 5 variantes d'aube dédiées pour éviter tout retour à la nuit).
3. **Ancre du protagoniste (« celui qui veut abandonner mais se souvient que cela n'est pas une option »)** :
   - *Homme noir d'une trentaine d'ans, peau mate foncée, cheveux en courtes locks, chemise de lin crème fermée jusqu'au col, pantalon sombre*.
   - Dans l'ancre (`fonds/scene-01-ancre.png`), il a un genou posé dans la boue rouge sous la pluie mais se relève puissamment, poing fermé sur le cœur, regard levé vers la lanterne ambrée.
4. **Héros historiques, leaders de l'AES et familles relevées (`Mini prompt On est réel.txt` + §14)** :
   - **Thomas Sankara**, **le roi Béhanzin** (Danxomè) et **le roi Bio Guéra** (Borgou) : peints en silhouettes/fresques d'or veillant dans la matière murale ou les nuées d'orage (`scene-01-ancre.png`, `scene-06.png`, et scènes ancestrales de la salve 2).
   - **Les nouveaux présidents de l'AES** : peints en fresque dorée sobre et digne en tenues fermées (`scene-10.png` et scènes de souveraineté/justice en salve 2/3), **strictement sans aucun drapeau, sans bannière nationale, sans blason ni logo** conformément aux interdits permanents §3 et §14.
   - **Les familles relevées** : père soutenu par la main lumineuse de son fils (`scene-07.png`), mère en prière devant le rameau fruitier d'or (`scene-08.png`), frère et sœur brisant les barreaux vers la lumière (`scene-09.png`), famille unie sous l'arche d'or (`scene-04.png`).
5. **Tenues & pudeur (§3 & §14)** : tenues fermées et élégantes sur tous les plans, visages entièrement dans le cadre, aucune nudité (les points 11–13 de `Instructions A.txt` sont annulés).

---

## 4. Typographie peinte et zones sûres (§3, §4, §15)

- **Texte écrit dans l'image par le générateur** : capitales serif d'or `#D9A441` et crème `#F3E7D3`, accompagnées de 1 à 3 stickers dorés au trait collés au sens du vers et traversées par le fil de lumière dorée.
- **Zones sûres 1080×1920** :
  - rien dans `y 0 → 144` ;
  - rien à droite de `x ≥ 910` entre `y 960` et `y 1690` ;
  - rien sous `y = 1574` ;
  - bloc de texte centré, largeur ≤ 740 px, dans la bande `y 620 → 1340`, jamais sur un visage ;
  - ancrage en haut lors du passage 768×1376 → 1080×1920 (le crâne n'est jamais coupé).
