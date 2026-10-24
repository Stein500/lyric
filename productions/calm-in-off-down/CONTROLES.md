# RAPPORT DE CONTRÔLE QUALITÉ GLOBAL — « Calm in off down » (Daïsky)

## 1. Bilan des 4 salves d'images (`39/39` plans distincts = `42/42` vers, `100 %`)

| Salve | Plans générés & contrôlés à 1:1 | Planches de contrôle 1:1 inspectées via `read_file` | Fautes d'orthographe | Visages voilés | Statut |
|---|---|---|---|---|---|
| **Salve 1** | `10/10` (`scene-01-ancre.png`, `scene-02.png` .. `scene-10.png`) | `CONTROLE-salve1.jpg`, `CONTROLE-salve1-typo.jpg`, `CONTROLE-apercu-bilingue.jpg` | `0` | `0` | **Validé par l'artiste** |
| **Salve 2** | `9/10` (`scene-11.png` .. `scene-13.png`, `scene-15.png` .. `scene-20.png`) | `CONTROLE-salve2.jpg`, `CONTROLE-salve2-typo.jpg`, `CONTROLE-defilement-fr.jpg` | `0` | `0` | **Validé par l'artiste** |
| **Salve 3** | `10/10` (`scene-14.png`, `scene-21.png`, `scene-22.png`, `scene-24.png`, `scene-25.png`, `scene-27.png` .. `scene-31.png`) | `CONTROLE-salve3.jpg`, `CONTROLE-salve3-typo.jpg` | `0` | `0` | **Validé par l'artiste** |
| **Salve 4** | `10/10` (`scene-32.png` .. `scene-37-final.png`, `v-140-13-aube.png`, `v-146-60-aube.png`, `v-149-86-aube.png`, `v-164-33-aube.png`) | `CONTROLE-salve4.jpg`, `CONTROLE-salve4-typo.jpg` | `0` | `0` | **Contrôlé 1:1 OK** |
| **TOTAL** | **`39/39` plans distincts (`42/42` vers)** | **10 planches de contrôle inspectées via `read_file`** | **`0`** | **`0`** | **100 % CONFORME** |

---

## 2. Contrôles techniques §12 sur le MP4 final (`livrables/calm-in-off-down-916.mp4`)

- **Fichier** : `productions/calm-in-off-down/livrables/calm-in-off-down-916.mp4`
- **Taille** : `51 901 661` octets (`49,50 Mo`)
- **Flux vidéo** : `H.264 (High) (avc1)`, `yuv420p (tv, bt709, progressive)`, `1080 × 1920`, `30 fps`, `1936 kb/s`, `5658 frames`
- **Flux audio** : `AAC (LC) (mp4a)`, `48 000 Hz`, stéréo, `256 kb/s`, `9 053 184 samples`
- **Durée mesurée vs `frames / fps`** :
  - `5658 frames / 30 fps = 188,600 s` (`00:03:08.60`)
  - Durée conteneur : `188,600 s` (écart `0,000 s ≤ 0,05 s`)
- **Ordre des atomes MP4 (`+faststart`)** :
  - `ftyp` @ offset `0` (`32` octets)
  - `moov` @ offset `32` (`199 816` octets)
  - `free` @ offset `199 848` (`8` octets)
  - `mdat` @ offset `199 856` (`51 701 805` octets)
  - Validation : **`moov` (`32`) < `mdat` (`199 856`) — `+faststart` actif**.
- **Détection d'images noires (`blackdetect=d=0.05:pix_th=0.10`)** :
  - Résultat : **`0` image noire détectée**.
- **Détection de gel d'image (`freezedetect=n=-33dB:d=2.5`)** :
  - Résultat : **`0` segment gelé ≥ 2,5 s** sur toute la durée (`0,00 s → 188,60 s`, y compris cartes d'accueil WTBW, 3 ponts instrumentaux avec clochettes CTA et carte finale).
- **Audio du MP4 (`ebur128=peak=true` + `astats=metadata=1:reset=0`)** :
  - `Integrated loudness I = -14.0 LUFS`
  - `Loudness Range LRA = 4.4 LU`
  - `True Peak = -1.1 dBFS`
  - `astats Peak level = -1.237254 dB`, `RMS level = -14.868247 dB` (`0` saturation, `0` clic).

---

## 3. Contrôles visuels §12 sur le MP4 final (`CONTROLE-mp4-final.jpg` & `CONTROLE-typo-zoom.jpg`)

Inspectés via `read_file` :
1. **`productions/calm-in-off-down/CONTROLE-mp4-final.jpg`** (`2000 × 2776 px`, 12 vignettes `480 × 854 px` extraites du MP4 final aux instants `2.00s`, `7.00s`, `25.80s`, `18.00s`, `36.20s`, `57.50s`, `82.00s`, `110.50s`, `123.50s`, `141.50s`, `165.30s`, `185.60s`) :
   - **Visages** : 100 % dégagés sur les 42 vers ; le badge `"Daïsky"` (`32 pt` à `y = 146..184`) est positionné dans le haut de la chevelure, bien au-dessus du front (`y ≥ 210`).
   - **Zones sûres** : rien dans les `144 px` du haut, rien dans le rail droit (`x ≥ 910, y 960 → 1690`), rien sous `y = 1574`.
   - **Mode Hybride Bilingue** : paroles VO (anglais/espagnol/WTBW) peintes en graffiti dans `y = 650 → 1040`, stickers `"love"` dans `y = 1100 → 1280`, et pilule de traduction française défilant mot à mot dans `y = 1452 → 1545` au-dessus du filet de progression `y = 1560`.
   - **Cartes WTBW & Clochettes CTA** : accueil en 2 temps (`SALUT · WTBW` puis `BIENVENUE SUR WTBW`), finale (`MERCI D'AVOIR ÉCOUTÉ !`) avec les 3 stickers vectoriels doux (`LIKE LA VIDÉO`, `CLIQUE SUR + POUR T'ABONNER`, `COMMENTE SI TU AIMES !`), sans aucun code ; 3 séquences clochettes CTA nettes pendant les pauses instrumentales.
2. **`productions/calm-in-off-down/CONTROLE-typo-zoom.jpg`** (`1688 × 2200 px`, 8 découpes **1:1** `820 × 480 px` avec grille `16 px`) :
   - Confirmation à l'échelle `1:1` de la netteté du lettrage graffiti peint et du défilement mot à mot de la traduction française (mot actif en or chaud `#FFE07A` + halo sombre `3 px` + curseur karaoké).

---

## 4. Contrôles §11 sur le Master MP3 (`livrables/Calm in off down - master 320k.mp3`)

- **Fichier** : `productions/calm-in-off-down/livrables/Calm in off down - master 320k.mp3`
- **Taille** : `7 664 555` octets (`7,31 Mo`)
- **Format** : MP3 CBR `320 kbps`, `48 000 Hz`, stéréo, `183,61 s` (`8 813 448` échantillons)
- **Mesures audio (normalisation linéaire 2 passes)** :
  - `Integrated loudness I = -14.0 LUFS`
  - `Loudness Range LRA = 4.4 LU`
  - `True Peak = -1.4 dBFS` (`astats Peak level = -1.415535 dB`)
- **Tags ID3v2.4 vérifiés (`mutagen`)** :
  - `TIT2 = Calm in off down`
  - `TPE1 = Daïsky`
  - `TPE2 = Daïsky`
  - `TALB = Calm in off down - Single`
  - `TCON = Hip-Hop / Afro-Urbain`
  - `TDRC = 2026`
  - `TXXX:SIGNATURE = Wolof TechStein beat wê !`
  - `TXXX:IA = Généré avec assistance IA`
  - `TXXX:MASTER = -14.0 LUFS / -1.5 dBTP / CBR 320k 48kHz`
  - `USLT:Lyrics:mul = 2001 caractères` (paroles propres sans timestamps)
  - `APIC:Cover = image/jpeg, type=3 (COVER_FRONT), 1080×1080 px (306 900 octets)`
