# COMMANDES TERMUX — « Entre Tes Mains » (TechStein)

Hash vérifié (les fichiers existent à ce commit, push confirmé) : `88de2d3da0dc7248569cbc1e25ee1ac093c4fcbf` (v2)

Sur Termux fraîchement installé :
```
pkg update -y; pkg install -y curl ca-certificates; termux-setup-storage
```
(accepter le popup, destination `/storage/emulated/0/Web+/`)

Une ligne par fichier — copier-coller la ligne entière ; si le shell affiche `>` : Ctrl+C puis recoller. `-C -` reprend un téléchargement coupé (relancer la même ligne).

```
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/Entre_Tes_Mains_clip_9x16.mp4 https://raw.githubusercontent.com/Stein500/lyric/88de2d3da0dc7248569cbc1e25ee1ac093c4fcbf/productions/entre_tes_mains/livrables/Entre_Tes_Mains_clip_9x16.mp4; ls -lh /storage/emulated/0/Web+/Entre_Tes_Mains_clip_9x16.mp4
```

```
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/Entre_Tes_Mains_master.mp3 https://raw.githubusercontent.com/Stein500/lyric/88de2d3da0dc7248569cbc1e25ee1ac093c4fcbf/productions/entre_tes_mains/livrables/Entre_Tes_Mains_master.mp3; ls -lh /storage/emulated/0/Web+/Entre_Tes_Mains_master.mp3
```

```
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/cover_Entre_Tes_Mains_1080.png https://raw.githubusercontent.com/Stein500/lyric/88de2d3da0dc7248569cbc1e25ee1ac093c4fcbf/productions/entre_tes_mains/livrables/cover_Entre_Tes_Mains_1080.png; ls -lh /storage/emulated/0/Web+/cover_Entre_Tes_Mains_1080.png
```

```
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/cover_Entre_Tes_Mains_1080x1920.png https://raw.githubusercontent.com/Stein500/lyric/88de2d3da0dc7248569cbc1e25ee1ac093c4fcbf/productions/entre_tes_mains/livrables/cover_Entre_Tes_Mains_1080x1920.png; ls -lh /storage/emulated/0/Web+/cover_Entre_Tes_Mains_1080x1920.png
```

```
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/cover_Entre_Tes_Mains_1920x1080.png https://raw.githubusercontent.com/Stein500/lyric/88de2d3da0dc7248569cbc1e25ee1ac093c4fcbf/productions/entre_tes_mains/livrables/cover_Entre_Tes_Mains_1920x1080.png; ls -lh /storage/emulated/0/Web+/cover_Entre_Tes_Mains_1920x1080.png
```

Tailles attendues : clip ≈ 31,4 Mo · master ≈ 5,3 Mo · covers ≈ 1,0 / 2,0 / 1,4 Mo. Si un fichier téléchargé fait moins de 100 ko : le supprimer puis relancer la même ligne.
