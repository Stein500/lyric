# Contrôles — Salve 1 (`scene-01-ancre` → `scene-08`)

## Journal des appels de génération du tour (§10.2 — limite plateforme 10 générations / tour)

- **Demandées** : 12 appels `generate_image` (dont 2 retouches de prompt court sur `scene-01-ancre.png` pour supprimer le mot parasite `ONLY` devant la 2e ligne, conformément au §4).
- **Réussies** : **10 générations** (`scene-01-ancre.png` validée après 2 régénérations courtes + `scene-02.png` à `scene-08.png` du premier coup).
- **Échouées (limite plateforme atteinte à 10/10)** : `scene-09.png` et `scene-10.png` (consignées comme non générées à ce tour, planifiées en tête de la Salve 2).

---

## Grille de contrôle visuel et orthographique (contact sheet `CONTROLE-salve1.jpg`, tuiles 540×968 ≥ 480 px)

| Plan | Fichier | Vers couverts (`t` s) | Texte peint vérifié à l'œil | Diacritiques | Zones sûres (`y 620→1340`) | Visage & crâne | Icônes dorées | Verdict |
|---|---|---|---|---|---|---|---|---|
| 01 | `scene-01-ancre.png` | v13 (35,87), v15 (47,16), v30 (91,41), v32 (101,74) | `JE SUIS LA GLACE` / `GLACE, GLACE` | — | OK | Entier, dégagé | Flocon d'or + cœur dans glaçon d'or | **Validé (Ancre)** |
| 02 | `scene-02.png` | v01 (6,03), v02 (10,09), v12 (32,37), v29 (87,60) | `WOLOF TECHSTEIN` / `ÇA BRÛLE !` | `Ç`, `Û` présents | OK | Entier, dégagé | Flamme fondant un glaçon-cœur + ondes | **Validé** |
| 03 | `scene-03.png` | v03 (14,17) | `ÉCOUTE...` | `É` présent | OK | Entier, dégagé | Oreille au trait d'or + onde acoustique | **Validé** |
| 04 | `scene-04.png` | v04 (15,12) | `ON T'A RACONTÉ MA VIE` / `ILS ONT PAS MENTI` | `T'A`, `É` présents | OK | Entier (plan moyen marche) | Livre ouvert d'or + œil doré | **Validé** |
| 05 | `scene-05.png` | v05 (16,79) | `J'SUIS PAS UN ANGE` / `J'SUIS PAS UN SAINT NON PLUS` | `J'SUIS` ×2 | OK | Entier, dégagé | Auréole brisée d'or + aile dorée | **Validé** |
| 06 | `scene-06.png` | v06 (18,61) | `SI TU VEUX TOUCHER` / `MON CŒUR, MA FILLE` | Ligature `Œ` nette | OK | Entier, main gantée sur le torse | Main ouverte d'or + cœur givré | **Validé** |
| 07 | `scene-07.png` | v07 (20,78) | `Y'A UN SOUCI` / `J'VAIS ÊTRE CRU` | `Y'A`, `J'VAIS`, `Ê` présents | OK | Profil entier, dégagé | Triangle d'alerte `!` + éclair d'or | **Validé** |
| 08 | `scene-08.png` | v08 (22,47) | `J'AI VU DES FRÈRES` / `SE TRANSFORMER EN OMBRES` | `J'AI`, `È` présents | OK | 3/4 dos regard caméra, entier | 3 silhouettes d'or + croissant d'ombre | **Validé** |

---

## Contrôle Audio Master (`livrables/_master_noart.mp3`)

- Passe 1 (`loudnorm`) sur `Glace - Daïsky.mp3` : `input_i = -13.46 LUFS`, `input_tp = -1.90 dBTP`, `input_lra = 7.00 LU`, `input_thresh = -23.58 LUFS`, `target_offset = -0.85 LU`.
- Passe 2 (`loudnorm` linéaire, `48 kHz`, `320 kb/s`, `-vn`) :
  - **Integrated Loudness** : **−14,0 LUFS**
  - **True Peak** : **−2,5 dBTP**
  - **Sample Peak (`astats`)** : **−2,48 dB** (attendu ≤ −1,0 dB)
  - **LRA** : **6,7 LU**
  - **Durée décodée** : **180,00 s** (8 639 999 échantillons à 48 000 Hz)
