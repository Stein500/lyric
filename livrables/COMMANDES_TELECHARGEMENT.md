# 📥 COMMANDES DE TÉLÉCHARGEMENT REPRENABLES (TERMUX / ANDROID)

> ⚡ **DESTINATION FIXE OBLIGATOIRE :** `/storage/emulated/0/Web+/`  
> **Commit Hash :** `64dd5cd419c36f16e62d38db839bf06a79f43984`

Copiez-collez ces blocs de commandes dans votre terminal Termux pour récupérer directement tous les livrables dans votre dossier de travail.

```bash
# 1. Accéder au dossier de destination et nettoyer les fichiers temporaires
mkdir -p /storage/emulated/0/Web+/
cd /storage/emulated/0/Web+/
find . -name "*.mp4" -size -100k -delete
find . -name "*.gif" -size -100k -delete

# 2. Téléchargement des 3 Vidéos MP4 Full HD (1080p)
curl -fL --retry 5 --retry-delay 3 -C - \
  -o "Klo_HDB_9x16_TikTok_Lyrics.mp4" \
  "https://raw.githubusercontent.com/Stein500/lyric/64dd5cd419c36f16e62d38db839bf06a79f43984/livrables/Klo_HDB_9x16_TikTok_Lyrics.mp4"

curl -fL --retry 5 --retry-delay 3 -C - \
  -o "Klo_HDB_16x9_YouTube_Cinema.mp4" \
  "https://raw.githubusercontent.com/Stein500/lyric/64dd5cd419c36f16e62d38db839bf06a79f43984/livrables/Klo_HDB_16x9_YouTube_Cinema.mp4"

curl -fL --retry 5 --retry-delay 3 -C - \
  -o "Klo_HDB_9x16_WhatsApp_Prestige_VIP.mp4" \
  "https://raw.githubusercontent.com/Stein500/lyric/64dd5cd419c36f16e62d38db839bf06a79f43984/livrables/Klo_HDB_9x16_WhatsApp_Prestige_VIP.mp4"

# 3. Téléchargement des GIFs Animés et Portraits HD
curl -fL --retry 5 --retry-delay 3 -C - \
  -o "Klo_HDB_Carte_Scintillante.gif" \
  "https://raw.githubusercontent.com/Stein500/lyric/64dd5cd419c36f16e62d38db839bf06a79f43984/livrables/Klo_HDB_Carte_Scintillante.gif"

curl -fL --retry 5 --retry-delay 3 -C - \
  -o "Klo_HDB_Queen_Klo_Sticker.gif" \
  "https://raw.githubusercontent.com/Stein500/lyric/64dd5cd419c36f16e62d38db839bf06a79f43984/livrables/Klo_HDB_Queen_Klo_Sticker.gif"

curl -fL --retry 5 --retry-delay 3 -C - \
  -o "Klo_Royal_Gold_Portrait.png" \
  "https://raw.githubusercontent.com/Stein500/lyric/64dd5cd419c36f16e62d38db839bf06a79f43984/livrables/Klo_Royal_Gold_Portrait.png"

curl -fL --retry 5 --retry-delay 3 -C - \
  -o "Klo_Anime_Cyber_Portrait.png" \
  "https://raw.githubusercontent.com/Stein500/lyric/64dd5cd419c36f16e62d38db839bf06a79f43984/livrables/Klo_Anime_Cyber_Portrait.png"

# 4. Vérification post-téléchargement
ls -lh /storage/emulated/0/Web+/
```
