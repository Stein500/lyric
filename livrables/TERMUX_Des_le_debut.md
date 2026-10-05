# 📲 Termux — récupérer la livraison « Dès le début »

**Hash du commit de livraison :** `3e8e5009b5316d9b04ae512f210e6ae56f59a48b`
Copie **une ligne à la fois** (séparateur `;`, jamais `&&`). Si le shell affiche `>` : Ctrl+C, puis recolle la ligne entière.

## 0. Préparation (une seule fois)
```
pkg update -y; pkg install -y curl ca-certificates; termux-setup-storage
```

## 1. Clip vertical 9:16 (63 Mo — le fichier lourd, à lancer en premier)
```
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o "/storage/emulated/0/Web+/Des_le_debut_9x16.mp4" "https://raw.githubusercontent.com/Stein500/lyric/3e8e5009b5316d9b04ae512f210e6ae56f59a48b/livrables/Des_le_debut_9x16.mp4"; ls -lh "/storage/emulated/0/Web+/Des_le_debut_9x16.mp4"
```

## 2. Master MP3 320 kb/s (8,3 Mo)
```
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o "/storage/emulated/0/Web+/Des_le_debut_master_320k.mp3" "https://raw.githubusercontent.com/Stein500/lyric/3e8e5009b5316d9b04ae512f210e6ae56f59a48b/livrables/Des_le_debut_master_320k.mp3"; ls -lh "/storage/emulated/0/Web+/Des_le_debut_master_320k.mp3"
```

## 3. Cover carrée 1080×1080
```
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o "/storage/emulated/0/Web+/cover_des_le_debut_1080x1080.jpg" "https://raw.githubusercontent.com/Stein500/lyric/3e8e5009b5316d9b04ae512f210e6ae56f59a48b/livrables/cover_des_le_debut_1080x1080.jpg"; ls -lh "/storage/emulated/0/Web+/cover_des_le_debut_1080x1080.jpg"
```

## 4. Cover story 9:16
```
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o "/storage/emulated/0/Web+/cover_des_le_debut_9x16.jpg" "https://raw.githubusercontent.com/Stein500/lyric/3e8e5009b5316d9b04ae512f210e6ae56f59a48b/livrables/cover_des_le_debut_9x16.jpg"; ls -lh "/storage/emulated/0/Web+/cover_des_le_debut_9x16.jpg"
```

## 5. Cover YouTube 16:9
```
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o "/storage/emulated/0/Web+/cover_des_le_debut_16x9.jpg" "https://raw.githubusercontent.com/Stein500/lyric/3e8e5009b5316d9b04ae512f210e6ae56f59a48b/livrables/cover_des_le_debut_16x9.jpg"; ls -lh "/storage/emulated/0/Web+/cover_des_le_debut_16x9.jpg"
```

## 6. Prompt universel à jour (v5.6) + rapport de livraison
```
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o "/storage/emulated/0/Web+/PROMPT_UNIVERSEL_v5.6_AUBE_CLOCHETTES.md" "https://raw.githubusercontent.com/Stein500/lyric/3e8e5009b5316d9b04ae512f210e6ae56f59a48b/PROMPT_UNIVERSEL_v5.6_AUBE_CLOCHETTES.md"; ls -lh "/storage/emulated/0/Web+/PROMPT_UNIVERSEL_v5.6_AUBE_CLOCHETTES.md"
```
```
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o "/storage/emulated/0/Web+/LIVRAISON_Des_le_debut.md" "https://raw.githubusercontent.com/Stein500/lyric/3e8e5009b5316d9b04ae512f210e6ae56f59a48b/livrables/LIVRAISON_Des_le_debut.md"; ls -lh "/storage/emulated/0/Web+/LIVRAISON_Des_le_debut.md"
```

## 7. Tout vérifier d'un coup
```
ls -lh /storage/emulated/0/Web+/Des_le_debut* /storage/emulated/0/Web+/cover_des_le_debut* /storage/emulated/0/Web+/PROMPT_UNIVERSEL_v5.6_AUBE_CLOCHETTES.md /storage/emulated/0/Web+/LIVRAISON_Des_le_debut.md
```

> **Reprise après coupure réseau** : relance la même ligne, `-C -` reprend où le téléchargement s'était arrêté.
> Si un fichier fait moins de 100 ko après coupure, supprime-le puis relance.
