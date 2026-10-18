# Contrôles Qualité — Salve 6 & Rendu Final MP4/MP3 (v5.9 — MODE PEINT)

## 1. Salve 6 — 10 plans (5 scènes héros panafricains & béninois variés + 5 variantes aube)
Références photographiques utilisées via `images=[...]` :
- `image-search/ref_behanzin_bioguera_sankara.jpg` : **Roi Béhanzin** (portrait historique assis en toge royale drapée tenant sa longue pipe royale), **Thomas Sankara** (béret rouge), **Roi Bio Guéra** (statue équestre cabrée à Parakou, turban et lance).
- `image-search/ref_pan_african_heroes.jpg` : **Patrice Lumumba** (lunettes, costume), **Cheikh Anta Diop**, **Nelson Mandela**, **Kemi Seba** (figure panafricaine contemporaine béninoise).
- `image-search/ref_aes_3_presidents.jpg` : **Assimi Goïta** (kufi blanc), **Ibrahim Traoré** (béret rouge), **Abdourahamane Tiani** (béret militaire à deux étoiles).

| # | Fichier | Vers couvert(s) | Texte peint vérifié (zoom 1:1) | Héros & personnages représentés | Zones sûres & contraintes | Statut |
|---|---|---|---|---|---|---|
| 1 | `fonds/scene-14.png` | V14 | `LE FEU DE MES ANCÊTRES` / `LE FEU DE MES DIEUX` (`Ê` ok) | Roi Béhanzin (longue pipe royale), Thomas Sankara, Roi Bio Guéra à cheval | OK (0 drapeau, têtes entières) | **VALIDÉ** |
| 2 | `fonds/scene-15.png` | V15 | `ON PORTE LA DOULEUR` / `MAIS ON PORTE AUSSI LA TERRE` | Famille béninoise debout unie (père, mère, enfant) + terre rouge | OK | **VALIDÉ** |
| 3 | `fonds/scene-18.png` | V18 | `UN COMBATTANT, UN SURVIVANT` / `PLUS FORT QUE TOI` | Thomas Sankara & Ibrahim Traoré en médaillons dorés | OK | **VALIDÉ** |
| 4 | `fonds/scene-31.png` | V31 | `MES MOTS SONT DES MISSILES` / `MES RIMES SONT DES BOUCLIERS` | Patrice Lumumba, Cheikh Anta Diop, Nelson Mandela, Kemi Seba | OK (0 drapeau, têtes entières) | **VALIDÉ** |
| 5 | `fonds/scene-38.png` | V38 | `POUR LES HÉROS D'HIER` / `POUR LES LIONS D'AUJOURD'HUI` (`É`, `'` ok) | Roi Béhanzin, Thomas Sankara, Patrice Lumumba, Nelson Mandela, Kemi Seba | OK | **VALIDÉ** |
| 6 | `fonds/v-193-01-aube.png` | V47 (aube) | `AUJOURD'HUI JE SUIS DEBOUT` / `JE SUIS NÉ POUR CHANTER` (`'`, `É` ok) | Famille relevée dans l'aube dorée `#E8A33D` | OK | **VALIDÉ** |
| 7 | `fonds/v-198-28-aube.png` | V48 (aube) | `ON A PLEURÉ DANS L'OMBRE` / `MAIS ON A FINI PAR BRILLER` (`É`, `'` ok) | Roi Béhanzin (pipe), Thomas Sankara, Patrice Lumumba, Nelson Mandela (aube) | OK | **VALIDÉ** |
| 8 | `fonds/v-205-01-aube.png` | V49 (aube) | `ON A SERRÉ LES POINGS` / `ON A CRIÉ SOUS LE CIEL` (`É`×2 ok) | Roi Béhanzin (pipe), Assimi Goïta, Ibrahim Traoré, Abdourahamane Tiani, Bio Guéra (aube) | OK | **VALIDÉ** |
| 9 | `fonds/v-210-37-aube.png` | V50 (aube) | `POUR CEUX QUI N'ONT PAS DE VOIX` / `POUR CEUX QUI N'ONT PLUS RIEN` (`'`×2 ok) | Famille unie dans l'aube dorée | OK | **VALIDÉ** |
| 10 | `fonds/v-216-73-aube.png` | V51 (aube) | `ON EST RÉELS...` / `ON EST VIVANTS...` (`É` ok) | Patrice Lumumba, Cheikh Anta Diop, Nelson Mandela, Kemi Seba (aube) | OK | **VALIDÉ** |

## 2. Contrôles obligatoires sur le rendu livré (§12)
- **Plans distincts disponibles** : **46 / 46** (`0` manquant, couvrant **57 / 57** vers).
- **Durée décodée (`ffmpeg -i`)** : **`250,00 s`** (`00:04:10.00` = `7 500 frames / 30 fps` à `0,00 s` près).
- **Frames noires (`blackdetect=d=0.05:pix_th=0.10`)** : **`0`**.
- **Freeze (`freezedetect=n=-33dB:d=2.5`)** : **`0` sur les 57 vers** (uniquement sur les cartons d'accueil `0,00 → 10,77 s` et le carton final `245,33 → 250,00 s`, signalé et assumé).
- **Loudness (`ebur128`)** : **`-14,0 LUFS`** intégré (`LRA = 7,4 LU`, `True Peak = -1,8 dBFS`) sur le MP4 ; **`-14,0 LUFS`** (`LRA = 7,5 LU`, `True Peak = -1,7 dBFS`) sur le MP3 master 320 kb/s.
- **Crête (`astats`)** : **`-1,81 dB`** sur le MP4 ; **`-1,75 dB`** sur le MP3 master (`≤ -1,0 dB`).
- **Faststart** : `moov` à l'octet **`36`** avant `mdat` à l'octet **`262 588`** (`faststart = True`).
- **Typo pendant le travelling (`CONTROLE-typo-zoom.jpg`)** : zoom 1:1 d'un frame rendu — nette, aucun doublement de lettre.
- **Carton final** : **`5,00 s`** (`244,99 → 249,99 s`) avec code **`0405`** en `210 px` or `#D9A441`.
- **Drapeau dans l'image** : **aucun** (`0 / 46` plans).
