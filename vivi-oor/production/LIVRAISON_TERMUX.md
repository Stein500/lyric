# Vivi OOR — livraison MP4, MP3, covers et paroles

**Commit immuable des livrables : `210e9117622d82bbb22c92b9fb3bc94604ea46ab`.** Fichiers poussés, présence, tailles et identifiants de blobs vérifiés via l’API GitHub. Le téléchargement Termux lui-même reste à exécuter sur le téléphone.

Le clip et le MP3 sont aussi accessibles directement dans le viewer et dans la page de livraison en preview, sans passer par GitHub.

## Préparer Termux (si nécessaire)

Une seule ligne à copier ; accepter ensuite la permission de stockage Android.

```bash
pkg update -y; pkg install -y curl ca-certificates; termux-setup-storage
```

Destination : **/storage/emulated/0/Web+/VIVI_OOR_FINAL**. Chaque commande ci-dessous est une seule ligne. Après une coupure, relancer exactement la même commande pour reprendre le téléchargement.

## MP4 — clip complet

[Téléchargement direct](https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/VIVI_OOR_lyrics_9x16.mp4) · 44 482 163 octets

```bash
mkdir -p /storage/emulated/0/Web+/VIVI_OOR_FINAL; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/VIVI_OOR_FINAL/VIVI_OOR_lyrics_9x16.mp4 https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/VIVI_OOR_lyrics_9x16.mp4; ls -lh /storage/emulated/0/Web+/VIVI_OOR_FINAL/VIVI_OOR_lyrics_9x16.mp4
```

## MP3 — morceau seul

[Téléchargement direct](https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/VIVI_OOR_master_320k.mp3) · 8 529 249 octets

```bash
mkdir -p /storage/emulated/0/Web+/VIVI_OOR_FINAL; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/VIVI_OOR_FINAL/VIVI_OOR_master_320k.mp3 https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/VIVI_OOR_master_320k.mp3; ls -lh /storage/emulated/0/Web+/VIVI_OOR_FINAL/VIVI_OOR_master_320k.mp3
```

## Cover universelle 3000

[Téléchargement direct](https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/cover_vivi_oor_universelle_3000.jpg) · 1 299 234 octets

```bash
mkdir -p /storage/emulated/0/Web+/VIVI_OOR_FINAL; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/VIVI_OOR_FINAL/cover_vivi_oor_universelle_3000.jpg https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/cover_vivi_oor_universelle_3000.jpg; ls -lh /storage/emulated/0/Web+/VIVI_OOR_FINAL/cover_vivi_oor_universelle_3000.jpg
```

## Cover carrée / APIC

[Téléchargement direct](https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/cover_vivi_oor_1080x1080.jpg) · 300 879 octets

```bash
mkdir -p /storage/emulated/0/Web+/VIVI_OOR_FINAL; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/VIVI_OOR_FINAL/cover_vivi_oor_1080x1080.jpg https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/cover_vivi_oor_1080x1080.jpg; ls -lh /storage/emulated/0/Web+/VIVI_OOR_FINAL/cover_vivi_oor_1080x1080.jpg
```

## Cover verticale

[Téléchargement direct](https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/cover_vivi_oor_9x16.jpg) · 533 418 octets

```bash
mkdir -p /storage/emulated/0/Web+/VIVI_OOR_FINAL; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/VIVI_OOR_FINAL/cover_vivi_oor_9x16.jpg https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/cover_vivi_oor_9x16.jpg; ls -lh /storage/emulated/0/Web+/VIVI_OOR_FINAL/cover_vivi_oor_9x16.jpg
```

## Cover horizontale

[Téléchargement direct](https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/cover_vivi_oor_16x9.jpg) · 324 232 octets

```bash
mkdir -p /storage/emulated/0/Web+/VIVI_OOR_FINAL; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/VIVI_OOR_FINAL/cover_vivi_oor_16x9.jpg https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/cover_vivi_oor_16x9.jpg; ls -lh /storage/emulated/0/Web+/VIVI_OOR_FINAL/cover_vivi_oor_16x9.jpg
```

## Cover portrait alternatif

[Téléchargement direct](https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/cover_vivi_oor_portrait_alternative_1080.jpg) · 343 721 octets

```bash
mkdir -p /storage/emulated/0/Web+/VIVI_OOR_FINAL; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/VIVI_OOR_FINAL/cover_vivi_oor_portrait_alternative_1080.jpg https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/cover_vivi_oor_portrait_alternative_1080.jpg; ls -lh /storage/emulated/0/Web+/VIVI_OOR_FINAL/cover_vivi_oor_portrait_alternative_1080.jpg
```

## Paroles LRC

[Téléchargement direct](https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/Vivi_OOR.lrc) · 2 323 octets

```bash
mkdir -p /storage/emulated/0/Web+/VIVI_OOR_FINAL; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/VIVI_OOR_FINAL/Vivi_OOR.lrc https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/Vivi_OOR.lrc; ls -lh /storage/emulated/0/Web+/VIVI_OOR_FINAL/Vivi_OOR.lrc
```

## Sous-titres du clip

[Téléchargement direct](https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/Vivi_OOR_clip.srt) · 3 413 octets

```bash
mkdir -p /storage/emulated/0/Web+/VIVI_OOR_FINAL; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/VIVI_OOR_FINAL/Vivi_OOR_clip.srt https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/Vivi_OOR_clip.srt; ls -lh /storage/emulated/0/Web+/VIVI_OOR_FINAL/Vivi_OOR_clip.srt
```

## Sous-titres de la chanson

[Téléchargement direct](https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/Vivi_OOR_chanson.srt) · 3 324 octets

```bash
mkdir -p /storage/emulated/0/Web+/VIVI_OOR_FINAL; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/VIVI_OOR_FINAL/Vivi_OOR_chanson.srt https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/Vivi_OOR_chanson.srt; ls -lh /storage/emulated/0/Web+/VIVI_OOR_FINAL/Vivi_OOR_chanson.srt
```

## Paroles texte

[Téléchargement direct](https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/Vivi_OOR_paroles.txt) · 1 838 octets

```bash
mkdir -p /storage/emulated/0/Web+/VIVI_OOR_FINAL; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/VIVI_OOR_FINAL/Vivi_OOR_paroles.txt https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/Vivi_OOR_paroles.txt; ls -lh /storage/emulated/0/Web+/VIVI_OOR_FINAL/Vivi_OOR_paroles.txt
```

## Animation des paroles

[Téléchargement direct](https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/VIVI_OOR_lyrics_mot_a_mot.ass) · 195 115 octets

```bash
mkdir -p /storage/emulated/0/Web+/VIVI_OOR_FINAL; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/VIVI_OOR_FINAL/VIVI_OOR_lyrics_mot_a_mot.ass https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/VIVI_OOR_lyrics_mot_a_mot.ass; ls -lh /storage/emulated/0/Web+/VIVI_OOR_FINAL/VIVI_OOR_lyrics_mot_a_mot.ass
```

## Prompt à jour

[Téléchargement direct](https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/PROMPT_UNIVERSEL_v5.3.2.md) · 28 486 octets

```bash
mkdir -p /storage/emulated/0/Web+/VIVI_OOR_FINAL; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/VIVI_OOR_FINAL/PROMPT_UNIVERSEL_v5.3.2.md https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/PROMPT_UNIVERSEL_v5.3.2.md; ls -lh /storage/emulated/0/Web+/VIVI_OOR_FINAL/PROMPT_UNIVERSEL_v5.3.2.md
```

## Caption et hashtags

[Téléchargement direct](https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/CAPTION_VIVI_OOR.txt) · 181 octets

```bash
mkdir -p /storage/emulated/0/Web+/VIVI_OOR_FINAL; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/VIVI_OOR_FINAL/CAPTION_VIVI_OOR.txt https://raw.githubusercontent.com/Stein500/lyric/210e9117622d82bbb22c92b9fb3bc94604ea46ab/vivi-oor/production/livrables/CAPTION_VIVI_OOR.txt; ls -lh /storage/emulated/0/Web+/VIVI_OOR_FINAL/CAPTION_VIVI_OOR.txt
```

## Contrôle facultatif

Comparer le résultat à ces empreintes :

- `VIVI_OOR_lyrics_9x16.mp4` : `8e396d626911979cd3f6343e3739aece1065015d083a3a71a4d3fe1fa0f87afb`
- `VIVI_OOR_master_320k.mp3` : `2fe6814ed527a86ae43d3f8f5c8f3a88a5aa27f49dece057f06aabf94561486f`

```bash
sha256sum /storage/emulated/0/Web+/VIVI_OOR_FINAL/VIVI_OOR_lyrics_9x16.mp4; sha256sum /storage/emulated/0/Web+/VIVI_OOR_FINAL/VIVI_OOR_master_320k.mp3
```

Les fichiers texte/LRC/SRT/ASS sont normalement petits. En revanche, un MP4 ou MP3 de quelques kilo-octets n’est pas une livraison complète. Ne pas effacer les vrais fichiers après une simple coupure : `-C -` reprend les téléchargements partiels.

Le MP4 comprend une ouverture de 6 s et une fin de 5 s ; le MP3 contient seulement la chanson complète. Les positions des mots sont estimées à l’intérieur des timecodes de vers fournis.
