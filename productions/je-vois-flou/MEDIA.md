# Téléchargement des médias — Je vois flou · WTBW

## Principe

Le dépôt `Stein500/lyric` pèse déjà ~11,6 Go. Les 129 Mo de vidéo et les images
ne vont **pas** dans l'historique Git : ils sont publiés en **GitHub Release**
(assets téléchargeables par URL directe, sans token, puisque le dépôt est public).

Tag de release prévu : **`je-vois-flou-v1`**

## URL directe des assets

Une fois la release publiée, chaque asset suit le schéma :

```
https://github.com/Stein500/lyric/releases/download/je-vois-flou-v1/<NOM_FICHIER>
```

| Asset | Nom exact |
|---|---|
| Clip final | `Je-vois-flou-WTBW-1080x1920-FINAL.mp4` |
| Teaser 1 | `Teaser-T1-WTBW-15s.mp4` |
| Teaser 2 | `Teaser-T2-WTBW-15s.mp4` |
| MP3 + pochette | `Je-vois-flou-WTBW-final-avec-pochette.mp3` |
| MP3 nu | `Je-vois-flou-WTBW-master-320.mp3` |
| Teaser 1 audio | `teaser-T1-15s.mp3` |
| Teaser 2 audio | `teaser-T2-15s.mp3` |
| Cover 1 | `Cover-1-WTBW-1080x1920.jpg` |
| Cover 2 | `Cover-2-WTBW-1080x1920.jpg` |
| Cover 3 | `Cover-3-WTBW-1080x1920.jpg` |
| Cover carrée | `Cover-carree-WTBW-1080x1080.jpg` |

## Commandes Termux

```bash
# 0. préparation
pkg update -y && pkg install -y curl
mkdir -p ~/storage/shared/Je-vois-flou && cd ~/storage/shared/Je-vois-flou
BASE="https://github.com/Stein500/lyric/releases/download/je-vois-flou-v1"

# 1. tout télécharger d'un coup (reprise possible avec -C -)
for f in \
  "Je-vois-flou-WTBW-1080x1920-FINAL.mp4" \
  "Teaser-T1-WTBW-15s.mp4" \
  "Teaser-T2-WTBW-15s.mp4" \
  "Je-vois-flou-WTBW-final-avec-pochette.mp3" \
  "Je-vois-flou-WTBW-master-320.mp3" \
  "teaser-T1-15s.mp3" \
  "teaser-T2-15s.mp3" \
  "Cover-1-WTBW-1080x1920.jpg" \
  "Cover-2-WTBW-1080x1920.jpg" \
  "Cover-3-WTBW-1080x1920.jpg" \
  "Cover-carree-WTBW-1080x1080.jpg" ; do
    curl -L -C - --retry 5 --retry-delay 3 -o "$f" "$BASE/$f"
done

# 2. vérifier que rien n'est vide ou tronqué
ls -lh
for f in *.mp4; do
  echo "== $f"; ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null || echo "ffmpeg absent"
done
```

### Une seule vidéo

```bash
BASE="https://github.com/Stein500/lyric/releases/download/je-vois-flou-v1"
curl -L -C - -o clip.mp4 "$BASE/Je-vois-flou-WTBW-1080x1920-FINAL.mp4"
```

### Sans `curl` (si Termux le refuse)

```bash
pkg install -y wget
wget -c "$BASE/Je-vois-flou-WTBW-1080x1920-FINAL.mp4"
```

## Notes de fiabilité

- `-C -` = reprise après coupure réseau. À garder : la vidéo fait 110 Mo.
- Ne pas utiliser `curl` sans `-L` : GitHub répond par une redirection 302 vers
  un CDN, et vous récupéreriez une page HTML de quelques centaines d'octets.
- Un fichier de ~600 octets = échec. Un MP4 valide fait plusieurs Mo.
- Vérification de durée attendue : clip **00:03:06**, teasers **00:00:15**.
