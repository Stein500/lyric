# LIVRAISON FINALE — « Calm in off down » (Daïsky)

- **Branche Git / GitHub** : `arena/c0e60266-lyric`
- **Dossier de production** : `productions/calm-in-off-down/`
- **Mode de production** : **Hybride Bilingue v6.0** (`PEINT_VO_GRAFFITI` dans l'image + `DEFILEMENT_TRADUCTION_FR` mot à mot dans la bande basse `y = 1452 → 1545`)
- **Recette visuelle** : `WANDANCE BATTLE & GRAFFITI LOVES — ORDONNÉ & VISAGE DÉGAGÉ`
- **Habillage v6.0** : `WTBW Salut & Stickers Doux` (`LIKE LA VIDÉO`, `CLIQUE SUR + POUR T'ABONNER`, `COMMENTE SI TU AIMES !`) — **sans système de code** (`systeme_code: false`, `drapeau: false`)

---

## 1. Tableau des livrables disponibles sur la branche `arena/c0e60266-lyric`

| Livrable | Chemin dans le dépôt | Dimensions / Format | Taille | Statut |
|---|---|---|---|---|
| **Clip Lyric Vidéo 9:16** | `productions/calm-in-off-down/livrables/calm-in-off-down-916.mp4` | `1080 × 1920` · `30 fps` · `H.264 High bt709 +faststart` + `AAC 256k 48 kHz` · `188,60 s` (`5658 frames`) | `51 901 661` octets (`49,50 Mo`) | **Rendu & contrôlé (§12 OK)** |
| **Master Audio 320 kbps** | `productions/calm-in-off-down/livrables/Calm in off down - master 320k.mp3` | `CBR 320 kbps` · `48 kHz` stéréo · `-14,0 LUFS` / `-1,4 dBTP` · ID3v2.4 complet (`APIC` 1080², `USLT`, `TXXX`) | `7 664 555` octets (`7,31 Mo`) | **Rendu & contrôlé (§11 OK)** |
| **Pochette 9:16** | `productions/calm-in-off-down/livrables/cover-916.jpg` | `1080 × 1920 px` JPEG | `472 235` octets | **Disponible** |
| **Pochette 1:1 (PNG)** | `productions/calm-in-off-down/livrables/cover-1080.png` | `1080 × 1080 px` PNG | `1 321 408` octets | **Disponible** |
| **Pochette 1:1 (JPEG / APIC)** | `productions/calm-in-off-down/livrables/cover-1080.jpg` | `1080 × 1080 px` JPEG | `306 900` octets | **Disponible** |
| **Carte d'accueil WTBW** | `productions/calm-in-off-down/livrables/carte-accueil.jpg` | `1080 × 1920 px` JPEG | `238 396` octets | **Disponible** |
| **Carte finale WTBW** | `productions/calm-in-off-down/livrables/carte-finale.jpg` | `1080 × 1920 px` JPEG | `243 126` octets | **Disponible** |
| **Paroles propres (USLT)** | `productions/calm-in-off-down/livrables/paroles_clean.txt` | Texte UTF-8 sans timestamps (42 vers) | `2 001` octets | **Disponible** |
| **39 fonds illustrés 9:16** | `productions/calm-in-off-down/fonds/*.png` | `39/39` plans `768 × 1376 px` (couvrant `42/42` vers + 4 variantes d'aube §9) | `39 fichiers PNG` | **100 % contrôlés 1:1** |
| **Contrôles MP4 finaux** | `productions/calm-in-off-down/CONTROLE-mp4-final.jpg` & `CONTROLE-typo-zoom.jpg` | Planche 12 vignettes + Zoom 1:1 (`16 px`) | `2 fichiers JPEG` | **Inspectés via `read_file`** |

---

## 2. Commandes Termux (Android) — Récupération en un bloc

Copie-colle ce bloc unique dans **Termux** pour récupérer automatiquement la branche `arena/c0e60266-lyric` et copier tous les livrables finaux dans ton dossier Android `/sdcard/Download/Calm-in-off-down/` :

```bash
pkg update -y && pkg install -y git && \
termux-setup-storage && \
cd ~ && rm -rf lyric-dl && \
git clone --depth 1 --branch arena/c0e60266-lyric https://github.com/Stein500/lyric.git lyric-dl && \
mkdir -p /sdcard/Download/Calm-in-off-down && \
cp -v ~/lyric-dl/productions/calm-in-off-down/livrables/"calm-in-off-down-916.mp4" /sdcard/Download/Calm-in-off-down/ && \
cp -v ~/lyric-dl/productions/calm-in-off-down/livrables/"Calm in off down - master 320k.mp3" /sdcard/Download/Calm-in-off-down/ && \
cp -v ~/lyric-dl/productions/calm-in-off-down/livrables/cover-916.jpg /sdcard/Download/Calm-in-off-down/ && \
cp -v ~/lyric-dl/productions/calm-in-off-down/livrables/cover-1080.png /sdcard/Download/Calm-in-off-down/ && \
cp -v ~/lyric-dl/productions/calm-in-off-down/livrables/cover-1080.jpg /sdcard/Download/Calm-in-off-down/ && \
cp -v ~/lyric-dl/productions/calm-in-off-down/livrables/carte-accueil.jpg /sdcard/Download/Calm-in-off-down/ && \
cp -v ~/lyric-dl/productions/calm-in-off-down/livrables/carte-finale.jpg /sdcard/Download/Calm-in-off-down/ && \
cp -v ~/lyric-dl/productions/calm-in-off-down/CONTROLE-mp4-final.jpg /sdcard/Download/Calm-in-off-down/ && \
cp -v ~/lyric-dl/productions/calm-in-off-down/CONTROLE-typo-zoom.jpg /sdcard/Download/Calm-in-off-down/ && \
ls -lh /sdcard/Download/Calm-in-off-down/
```
