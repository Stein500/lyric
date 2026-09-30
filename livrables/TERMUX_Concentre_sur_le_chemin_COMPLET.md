# Télécharger le pack — Concentré sur le chemin

**Daïsky · deux clips complets, master MP3, trois pochettes, dix fonds et prompts.**

Les exports v1 sont contrôlés techniquement. Les fonds sont approuvés ; le calage mot à mot reste estimé depuis ton LRC, pas encore validé à l’écoute.

Commit immuable des médias et du prompt : `7321792a9d81bff773c695287e58a76b602b0a5e`. Chaque fichier a été vérifié par l’API GitHub puis son contenu brut réellement téléchargé et comparé en SHA-256. L’accès TLS direct à raw.githubusercontent.com échoue dans ce sandbox ; les octets ont été vérifiés via l’API GitHub (format raw), sans désactiver TLS. Les liens publics ci-dessous restent au même hash vérifié. Ce document de commandes est enregistré dans le commit suivant.

## 1. Préparer Termux une fois

Copier cette ligne et accepter l’autorisation Android :

```sh
pkg update -y; pkg install -y curl ca-certificates coreutils; termux-setup-storage
```

## 2. Télécharger — une ligne entière par fichier

Destination : `/storage/emulated/0/Web+/`. Relancer la même ligne après une coupure : `-C -` reprend le fichier partiel. Les fichiers sont livrés séparément pour éviter une seconde grosse archive des mêmes vidéos.

### Clip vertical · TikTok / Reels / Shorts

[`Concentre_sur_le_chemin_9x16_v1.mp4`](https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/Concentre_sur_le_chemin_9x16_v1.mp4) — **30,147,295 octets**.

```sh
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/Concentre_sur_le_chemin_9x16_v1.mp4 https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/Concentre_sur_le_chemin_9x16_v1.mp4; ls -lh /storage/emulated/0/Web+/Concentre_sur_le_chemin_9x16_v1.mp4
```

### Clip horizontal · YouTube

[`Concentre_sur_le_chemin_16x9_YT_v1.mp4`](https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/Concentre_sur_le_chemin_16x9_YT_v1.mp4) — **29,379,843 octets**.

```sh
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/Concentre_sur_le_chemin_16x9_YT_v1.mp4 https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/Concentre_sur_le_chemin_16x9_YT_v1.mp4; ls -lh /storage/emulated/0/Web+/Concentre_sur_le_chemin_16x9_YT_v1.mp4
```

### Master MP3 · chanson seule, 320 kb/s

[`Concentre_sur_le_chemin_master_320k.mp3`](https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/Concentre_sur_le_chemin_master_320k.mp3) — **9,071,735 octets**.

```sh
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/Concentre_sur_le_chemin_master_320k.mp3 https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/Concentre_sur_le_chemin_master_320k.mp3; ls -lh /storage/emulated/0/Web+/Concentre_sur_le_chemin_master_320k.mp3
```

### Pochette carrée · 1080 × 1080

[`cover_concentre_sur_le_chemin_1080x1080.jpg`](https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/cover_concentre_sur_le_chemin_1080x1080.jpg) — **530,290 octets**.

```sh
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/cover_concentre_sur_le_chemin_1080x1080.jpg https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/cover_concentre_sur_le_chemin_1080x1080.jpg; ls -lh /storage/emulated/0/Web+/cover_concentre_sur_le_chemin_1080x1080.jpg
```

### Pochette portrait · 1080 × 1920

[`cover_concentre_sur_le_chemin_9x16.jpg`](https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/cover_concentre_sur_le_chemin_9x16.jpg) — **799,580 octets**.

```sh
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/cover_concentre_sur_le_chemin_9x16.jpg https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/cover_concentre_sur_le_chemin_9x16.jpg; ls -lh /storage/emulated/0/Web+/cover_concentre_sur_le_chemin_9x16.jpg
```

### Pochette YouTube · 1920 × 1080

[`cover_concentre_sur_le_chemin_16x9.jpg`](https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/cover_concentre_sur_le_chemin_16x9.jpg) — **686,184 octets**.

```sh
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/cover_concentre_sur_le_chemin_16x9.jpg https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/cover_concentre_sur_le_chemin_16x9.jpg; ls -lh /storage/emulated/0/Web+/cover_concentre_sur_le_chemin_16x9.jpg
```

### Les dix fonds approuvés · ZIP

[`Concentre_sur_le_chemin_10_images_v2.zip`](https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/Concentre_sur_le_chemin_10_images_v2.zip) — **6,412,030 octets**.

```sh
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/Concentre_sur_le_chemin_10_images_v2.zip https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/Concentre_sur_le_chemin_10_images_v2.zip; ls -lh /storage/emulated/0/Web+/Concentre_sur_le_chemin_10_images_v2.zip
```

### Planche des cinq paires de fonds

[`Concentre_sur_le_chemin_planche_10_fonds_v2.jpg`](https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/Concentre_sur_le_chemin_planche_10_fonds_v2.jpg) — **1,667,153 octets**.

```sh
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/Concentre_sur_le_chemin_planche_10_fonds_v2.jpg https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/Concentre_sur_le_chemin_planche_10_fonds_v2.jpg; ls -lh /storage/emulated/0/Web+/Concentre_sur_le_chemin_planche_10_fonds_v2.jpg
```

### Paroles LRC · horaires de la chanson source

[`Concentre_sur_le_chemin.lrc`](https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/Concentr%C3%A9%20sur%20le%20chemin.lrc) — **3,155 octets**.

```sh
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/Concentre_sur_le_chemin.lrc https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/Concentr%C3%A9%20sur%20le%20chemin.lrc; ls -lh /storage/emulated/0/Web+/Concentre_sur_le_chemin.lrc
```

### Prompt universel complet à jour

[`PROMPT_UNIVERSEL_v5.5_HYBRIDE_COMMANDE.md`](https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/PROMPT_UNIVERSEL_v5.5_HYBRIDE_COMMANDE.md) — **38,906 octets**.

```sh
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/PROMPT_UNIVERSEL_v5.5_HYBRIDE_COMMANDE.md https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/PROMPT_UNIVERSEL_v5.5_HYBRIDE_COMMANDE.md; ls -lh /storage/emulated/0/Web+/PROMPT_UNIVERSEL_v5.5_HYBRIDE_COMMANDE.md
```

### Catalogue des prompts d’images

[`PROMPTS_IMAGES_Concentre_sur_le_chemin.md`](https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/PROMPTS_IMAGES_Concentre_sur_le_chemin.md) — **71,559 octets**.

```sh
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/PROMPTS_IMAGES_Concentre_sur_le_chemin.md https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/PROMPTS_IMAGES_Concentre_sur_le_chemin.md; ls -lh /storage/emulated/0/Web+/PROMPTS_IMAGES_Concentre_sur_le_chemin.md
```

### Index de la livraison et repères d’écoute

[`LIVRAISON_Concentre_sur_le_chemin.md`](https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/LIVRAISON_Concentre_sur_le_chemin.md) — **4,783 octets**.

```sh
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/LIVRAISON_Concentre_sur_le_chemin.md https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/LIVRAISON_Concentre_sur_le_chemin.md; ls -lh /storage/emulated/0/Web+/LIVRAISON_Concentre_sur_le_chemin.md
```

### Empreintes SHA-256 des fichiers

[`Concentre_sur_le_chemin_SHA256.txt`](https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/Concentre_sur_le_chemin_SHA256.txt) — **1,267 octets**.

```sh
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/Concentre_sur_le_chemin_SHA256.txt https://raw.githubusercontent.com/Stein500/lyric/7321792a9d81bff773c695287e58a76b602b0a5e/livrables/Concentre_sur_le_chemin_SHA256.txt; ls -lh /storage/emulated/0/Web+/Concentre_sur_le_chemin_SHA256.txt
```

## 3. Vérifier les téléchargements

Après téléchargement du fichier des empreintes :

```sh
cd /storage/emulated/0/Web+; sha256sum -c Concentre_sur_le_chemin_SHA256.txt
```

Chaque fichier téléchargé doit afficher `OK`. Un fichier non encore téléchargé sera signalé comme manquant ; il suffit de lancer sa ligne.

## Si Termux signale une erreur

- Si le shell affiche seulement `>` : Ctrl+C, puis recoller une ligne complète.
- Une erreur HTTP n’est pas un média : `-fL` évite d’enregistrer la page d’erreur.
- Comparer la taille exacte indiquée ci-dessus. Un MP4/JPG/MP3 de quelques octets est un fichier raté : supprimer uniquement ce fichier puis relancer.
- Les documents Markdown/LRC peuvent légitimement faire moins de 100 ko ; ne pas les supprimer pour cette seule raison.
- Si `curl` refuse une reprise parce qu’un fichier local est déjà complet, vérifier son SHA-256 avant de le supprimer ou de le retélécharger.

## Repères d’écoute du clip

Le hook dure 6,90 s ; ensuite la chanson commence depuis son début. Écouter notamment **00:32,20**, **01:32,54** et **02:39,74** dans les clips. Les tests audio n’ont mesuré aucune dérive du montage sur ces trois passages ; cela ne prouve pas l’alignement phonétique de chaque mot.
