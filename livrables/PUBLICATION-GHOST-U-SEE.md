# Kit de publication — Ghost u see · Daïsky

## Livrables
- Clip vertical : `GHOST-U-SEE-DAISKY-9x16.mp4`
- Audio seul : `GHOST-U-SEE-DAISKY-MASTER.mp3` — 320 kb/s, stéréo, avec la pochette intégrée
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

## Téléchargement dans Termux
```sh
pkg update -y
pkg install curl ffmpeg -y
termux-setup-storage
mkdir -p ~/storage/downloads ~/storage/shared/Movies ~/storage/shared/Music ~/storage/shared/Pictures
curl -fL "https://raw.githubusercontent.com/Stein500/lyric/arena/5fe20db4-lyric/livrables/GHOST-U-SEE-DAISKY-9x16.mp4" -o ~/storage/downloads/GHOST-U-SEE-DAISKY-9x16.mp4
curl -fL "https://raw.githubusercontent.com/Stein500/lyric/arena/5fe20db4-lyric/livrables/GHOST-U-SEE-DAISKY-MASTER.mp3" -o ~/storage/downloads/GHOST-U-SEE-DAISKY-MASTER.mp3
curl -fL "https://raw.githubusercontent.com/Stein500/lyric/arena/5fe20db4-lyric/livrables/COVER-GHOST-U-SEE-1080x1920.jpg" -o ~/storage/downloads/COVER-GHOST-U-SEE-1080x1920.jpg
cp ~/storage/downloads/GHOST-U-SEE-DAISKY-9x16.mp4 ~/storage/shared/Movies/
cp ~/storage/downloads/GHOST-U-SEE-DAISKY-MASTER.mp3 ~/storage/shared/Music/
cp ~/storage/downloads/COVER-GHOST-U-SEE-1080x1920.jpg ~/storage/shared/Pictures/
ffprobe -v error -show_entries stream=codec_name,sample_rate,channels,bit_rate -show_entries format=duration -of default=noprint_wrappers=1 ~/storage/shared/Music/GHOST-U-SEE-DAISKY-MASTER.mp3
```

Le MP4 est en H.264/AAC, 1080 × 1920, 30 i/s. Le MP3 est un export audio seul en 320 kb/s, avec la couverture intégrée; il provient du fichier audio original fourni.
