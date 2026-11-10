# Kit de publication — Ghost u see · Daïsky

## Fichiers
- Clip vertical : `GHOST-U-SEE-DAISKY-9x16.mp4`
- Couverture : `COVER-GHOST-U-SEE-1080x1920.jpg`

## Titre
**Ghost u see — Daïsky | Lyric video vertical FR/EN/ES**

## Légende
Entre ce que les autres projettent et la personne que l’on choisit d’être. « Ghost u see » : un clip vertical illustré, avec les paroles intégrées aux images et une traduction française en karaoké pour les passages anglais et espagnols.

## Hashtags
#Daïsky #GhostUSee #WTBW #LyricVideo #Musique #AfroAnime #AnimeArt #Animation #Paroles #FrenchSubtitles #EnglishLyrics #SpanishLyrics #MusiqueUrbaine

*(13 hashtags.)*

## Déclaration IA
Les illustrations ont été générées avec l’aide de l’IA. Les paroles et leur synchronisation sont celles de l’œuvre; les traductions françaises sont affichées en pilule karaoké pour les passages anglais et espagnols. Le clip utilise le master audio original fourni par l’artiste; aucune voix ni musique n’a été générée par IA.

## Commandes Termux

### Téléchargement direct avec curl
Une URL HTTPS directe est nécessaire. Après avoir obtenu cette URL auprès d’un hébergeur :

```sh
pkg update -y
pkg install curl ffmpeg -y
termux-setup-storage
curl -fL "URL_HTTPS_DIRECTE_DU_MP4" -o ~/storage/downloads/GHOST-U-SEE-DAISKY-9x16.mp4
```

Le MP4 de ce livrable est actuellement fourni dans Arena et n’a pas d’URL publique `curl`. Sans le publier sur un hébergeur, télécharge-le depuis le lecteur Arena, puis copie-le depuis **Download/Téléchargements** :

```sh
pkg install ffmpeg -y
termux-setup-storage
mkdir -p ~/storage/shared/Movies ~/storage/shared/Pictures
cp ~/storage/downloads/GHOST-U-SEE-DAISKY-9x16.mp4 ~/storage/shared/Movies/
cp ~/storage/downloads/COVER-GHOST-U-SEE-1080x1920.jpg ~/storage/shared/Pictures/
ffprobe -v error \
  -show_entries stream=codec_name,width,height,r_frame_rate \
  -show_entries format=duration \
  -of default=noprint_wrappers=1 \
  ~/storage/shared/Movies/GHOST-U-SEE-DAISKY-9x16.mp4
```

Le MP4 est déjà encodé en H.264/AAC, 1080 × 1920, 30 i/s; il n’est pas nécessaire de le réencoder pour le publier.
