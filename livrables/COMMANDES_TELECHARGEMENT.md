# 📥 COMMANDES DE TÉLÉCHARGEMENT REPRENABLES (TERMUX / ANDROID)

> ⚡ **DESTINATION :** `/storage/emulated/0/Web+/`  
> **Branche GitHub :** `arena/01a0497b-lyric`

---

## 🚀 MÉTHODE 1 (RECOMMANDÉE) : TÉLÉCHARGEMENT DIRECT VIA GIT (100% INFAILLIBLE)

Copiez-collez ce bloc unique dans Termux : il récupère directement tous les livrables dans votre dossier sans aucun risque d'erreur 404 :

```bash
cd /storage/emulated/0/Web+/
git clone --depth 1 -b arena/01a0497b-lyric https://github.com/Stein500/lyric.git __tmp_klo
cp -r __tmp_klo/livrables/* .
rm -rf __tmp_klo
ls -lh
```

---

## 🌐 MÉTHODE 2 : TÉLÉCHARGEMENT FICHIER PAR FICHIER AVEC CURL

```bash
cd /storage/emulated/0/Web+/

# 1. Vidéos MP4 Full HD
curl -fL --retry 5 --retry-delay 3 -C - \
  -o "Klo_HDB_9x16_TikTok_Lyrics.mp4" \
  "https://github.com/Stein500/lyric/raw/arena/01a0497b-lyric/livrables/Klo_HDB_9x16_TikTok_Lyrics.mp4"

curl -fL --retry 5 --retry-delay 3 -C - \
  -o "Klo_HDB_16x9_YouTube_Cinema.mp4" \
  "https://github.com/Stein500/lyric/raw/arena/01a0497b-lyric/livrables/Klo_HDB_16x9_YouTube_Cinema.mp4"

curl -fL --retry 5 --retry-delay 3 -C - \
  -o "Klo_HDB_9x16_WhatsApp_Prestige_VIP.mp4" \
  "https://github.com/Stein500/lyric/raw/arena/01a0497b-lyric/livrables/Klo_HDB_9x16_WhatsApp_Prestige_VIP.mp4"

# 2. GIFs Animés & Portraits HD
curl -fL --retry 5 --retry-delay 3 -C - \
  -o "Klo_HDB_Carte_Scintillante.gif" \
  "https://github.com/Stein500/lyric/raw/arena/01a0497b-lyric/livrables/Klo_HDB_Carte_Scintillante.gif"

curl -fL --retry 5 --retry-delay 3 -C - \
  -o "Klo_HDB_Queen_Klo_Sticker.gif" \
  "https://github.com/Stein500/lyric/raw/arena/01a0497b-lyric/livrables/Klo_HDB_Queen_Klo_Sticker.gif"

curl -fL --retry 5 --retry-delay 3 -C - \
  -o "Klo_Royal_Gold_Portrait.png" \
  "https://github.com/Stein500/lyric/raw/arena/01a0497b-lyric/livrables/Klo_Royal_Gold_Portrait.png"

curl -fL --retry 5 --retry-delay 3 -C - \
  -o "Klo_Anime_Cyber_Portrait.png" \
  "https://github.com/Stein500/lyric/raw/arena/01a0497b-lyric/livrables/Klo_Anime_Cyber_Portrait.png"

# 3. Vérification
ls -lh
```
