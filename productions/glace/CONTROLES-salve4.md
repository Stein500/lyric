# Contrôles — Salve 4 (`scene-19` + `v-121-25` → `v-165-25`) & Rendu final `glace-916.mp4`

## 1. Journal des appels de génération du tour (§4 & §10.2)

- **Demandées** : 10 appels `generate_image` (les 9 derniers plans `scene-19.png` + `v-121-25.png` à `v-165-25.png`, dont 1 relance sur `scene-19.png` après blocage lexical sur le mot « négros » remplacé par le sous-texte exact « VEULENT MA PLACE / ILS SONT TROP SUR LE PAL' »).
- **Réussies** : **9 / 9 plans distincts validés** → **36 / 36 plans distincts disponibles** dans `productions/glace/fonds/` (`0 manquant` dans `verses_map.json`).

---

## 2. Grille de contrôle visuel et orthographique — Salve 4 (`CONTROLE-salve4.jpg`, tuiles 540×968 ≥ 480 px)

| Plan | Fichier | Vers (`t` s) | Mise en scène (mood · tenues · décor · arc aube) | Texte peint contrôlé | Diacritiques | Zones sûres | Icônes dorées | Verdict |
|---|---|---|---|---|---|---|---|---|
| 19 | `scene-19.png` | v22 (64,26) | **Trône nocturne** · Costume 3 pièces bleu de Prusse & cape-manteau sur fauteuil de cuir et laiton en haut d'un grand escalier de marbre | `VEULENT MA PLACE` / `ILS SONT TROP SUR LE PAL'` | `PAL'` | OK | Trône d'or + Roi d'échecs doré | **Validé** |
| 37 | `v-121-25.png` | v37 (121,25) | **Duo cour pré-aube** · Manteau croisé noir à col d'or au premier plan ; femme en manteau long s'éloignant sous l'arche ambrée au loin | `J'EN AI MARRE D'ÊTRE TRAHI` / `À FORCE DE POIGNARDS J'SUIS AIGRI` | `J'EN`, `D'ÊTRE`, `À`, `J'SUIS` | OK | Bouclier entaillé d'or + dague brisée | **Validé** |
| 38 | `v-124-63.png` | v38 (124,63) | **Variante Aube dédiée (§9)** · Manteau ivoire & bleu nuit sur belvédère au lever du soleil doré | `WOLOF TECHSTEIN` / `ÇA BRÛLE !` | `Ç`, `Û` | OK | Soleil levant sur glace + flamme d'or | **Validé** |
| 39 | `v-127-95.png` | v39 (127,95), v41 (139,19) | **Variante Aube dédiée (§9)** · Caban marine & crème sur toits haussmanniens givrés baignés par l'aube dorée | `JE SUIS LA GLACE` / `GLACE, GLACE` | — | OK | Flocon d'or solaire + cœur dans glaçon | **Validé** |
| 40 | `v-131-54.png` | v40 (131,54) | **Aube cour d'honneur (duo)** · Pardessus cachemire bleu nuit & revers brodés d'or ; femme en robe longue sur le perron au soleil levant | `JE SUIS LA GLACE, GLACE, GLACE` / `BIG BOSS DANS LA PLACE !` | — | OK | Couronne d'or + diamant de glace | **Validé** |
| 42 | `v-143-01.png` | v42 (143,01) | **Variante Aube dédiée (§9)** · Veste architecturale bleu nuit & or devant verrière givrée traversée par l'aube | `JE SUIS LA GLACE` / `TECH !` | — | OK | Éclair circuit d'or + flocon solaire | **Validé** |
| 43 | `v-150-14.png` | v43 (150,14) | **Outro Aube 1** · Manteau long bleu nuit & écharpe de soie crème sur pont monumental au soleil levant | `WOLOF TECHSTEIN ÇA BRÛLE !` / `GLACE` | `Ç`, `Û` | OK | Glaçon-flamme d'or + ondes sonores | **Validé** |
| 44 | `v-157-79.png` | v44 (157,79) | **Outro Aube 2** · Costume croisé & long manteau bleu nuit à liseré d'or sur grand boulevard mouillé reflétant l'aube | `WOLOF TECHSTEIN ÇA BRÛLE...` / `BIG BOSS` | `Ç`, `Û` | OK | Couronne d'or + flamme dans anneau | **Validé** |
| 45 | `v-165-25.png` | v45 (165,25) | **Outro Aube Finale** · Manteau cérémoniel bleu nuit & feuille d'or face au plein soleil levant, colombe d'or en envol | `WOLOF... TECHSTEIN...` / `ÇA BRÛLE... TECH...` | `Ç`, `Û` | OK | Colombe d'or + badge `0300` | **Validé** |

---

## 3. Contrôles obligatoires du rendu `livrables/glace-916.mp4` (§12)

| Contrôle | Commande exécutée | Attendu (§12) | Mesure réelle | Verdict |
|---|---|---|---|---|
| **Durée** | `ffmpeg -i livrables/glace-916.mp4` | `= frames/fps` à 0,01 s près (`5550 / 30 = 185,00 s`) | `Duration: 00:03:05.00` (**185,00 s**, 5 550 frames @ 30 fps) | **OK** |
| **Flux vidéo/audio** | `ffmpeg -i livrables/glace-916.mp4` | H.264 `yuv420p` `bt709` 1080×1920@30 + AAC 256k 48 kHz | `h264 (High) yuv420p(tv, bt709) 1080x1920 1968 kb/s 30 fps` + `aac (LC) 48000 Hz stereo 256 kb/s` (51 650 704 o / 49,3 Mo) | **OK** |
| **Frames noires** | `blackdetect=d=0.05:pix_th=0.10` | **0** | **0** détection | **OK** |
| **Gel (`freezedetect`)** | `freezedetect=n=-33dB:d=2.5` | **0 sur les vers** ; cartes & CTA sur image fixe signalés et assumés | **0 sur les 45 vers en cours de lecture** ; uniquement `0→6,07 s` (carte d'accueil fixe), `167,8→180,0 s` (longue fenêtre CTA clochette finale sur plan éteint) et `180,97→185,0 s` (carte finale fixe) | **OK** |
| **Loudness clip** | `ebur128=peak=true` | **−14,0 LUFS** | **−14,0 LUFS** (LRA = 6,9 LU, True Peak = −2,4 dBFS) | **OK** |
| **Crête clip** | `astats=metadata=1:reset=0` | **≤ −1,0 dB** | **−2,47 dB** (`-2.467866 dB`) | **OK** |
| **Faststart** | inspection octets d'en-tête | `moov` avant `mdat` | `moov` à l'octet **36**, `mdat` à l'octet **197 556** (`moov < mdat`) | **OK** |
| **Typo peinte (zoom 1:1)** | `CONTROLE-typo-zoom.jpg` (crop 1:1 1080×400 à `t=37,00 s`) | nette, **aucun doublement de lettre** | **0 ghosting / 0 dédoublement** (travelling par fenêtre glissante sur source à 110 %, aucun resize par frame) | **OK** |
