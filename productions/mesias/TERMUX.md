# TERMUX — récupérer les fichiers MESÍAS sur Android

Copie-colle, ligne par ligne. Tout est figé sur le commit **`cb0ecaf`** : les liens ne
changeront pas et ne renverront pas 404.

**Ce qui existe réellement dans ce commit** (tailles vérifiées sur GitHub) :

| Fichier | Poids |
|---|---|
| `MESIAS_clip_1080x1920_leger.mp4` | 94,2 Mo — le clip complet 12:29,71 |
| `MESIAS_teaser_15s_1080x1920.mp4` | 5,1 Mo — le teaser 15,00 s |
| `MESIAS_couverture_TikTok_1080x1920.jpg` | 324 Ko — couverture principale |
| `MESIAS_couverture_variante_visage_1080x1920.jpg` | 537 Ko |
| `MESIAS_couverture_paysage_1080x1920.jpg` | 519 Ko |
| `Averly Morillo - MESIAS (master normalise -14LUFS).mp3` | 28,4 Mo |
| `SHA256SUMS.txt` | 761 o |

> Le **master 274,6 Mo n'est pas ici** : GitHub refuse les fichiers de plus de 100 Mo.
> La version `leger` est le même montage, encodé à débit réduit pour tenir sous la limite.

---

## 1 — Installation (une seule fois)

```sh
pkg update
pkg install -y curl coreutils termux-api
```

`termux-api` est indispensable pour `termux-media-scan` : sans lui, TikTok ne voit pas les
fichiers téléchargés. Il faut aussi l'application **Termux:API** installée depuis F-Droid.

## 2 — Autoriser l'accès au stockage (une seule fois)

```sh
termux-setup-storage
```

Accepte la demande qui s'affiche. Le dossier `~/storage/downloads` pointe alors vers
`/sdcard/Download`.

## 3 — Télécharger

```sh
cd ~/storage/downloads
BASE="https://raw.githubusercontent.com/Stein500/lyric/cb0ecaf/productions/mesias/livrables"
```

### Le clip complet (94,2 Mo)

```sh
curl -L --retry 3 -C - -o "MESIAS_clip_leger.mp4" \
  "$BASE/MESIAS_clip_1080x1920_leger.mp4"
```

### Le teaser 15 s (5,1 Mo)

```sh
curl -L --retry 3 -C - -o "MESIAS_teaser_15s.mp4" \
  "$BASE/MESIAS_teaser_15s_1080x1920.mp4"
```

### Les trois couvertures

```sh
curl -L --retry 3 -C - -o "MESIAS_couverture.jpg" \
  "$BASE/MESIAS_couverture_TikTok_1080x1920.jpg"

curl -L --retry 3 -C - -o "MESIAS_couv_visage.jpg" \
  "$BASE/MESIAS_couverture_variante_visage_1080x1920.jpg"

curl -L --retry 3 -C - -o "MESIAS_couv_paysage.jpg" \
  "$BASE/MESIAS_couverture_paysage_1080x1920.jpg"
```

### Le master audio normalisé (28,4 Mo)

Attention : l'espace et les parenthèses sont dans le nom du fichier, il faut les encoder.

```sh
curl -L --retry 3 -C - -o "MESIAS_master.mp3" \
  "$BASE/Averly%20Morillo%20-%20MESIAS%20(master%20normalise%20-14LUFS).mp3"
```

### Les empreintes

```sh
curl -L --retry 3 -C - -o "SHA256SUMS.txt" "$BASE/SHA256SUMS.txt"
```

---

## 4 — Vérifier que le téléchargement n'est pas corrompu

```sh
cd ~/storage/downloads
sha256sum "MESIAS_clip_leger.mp4" "MESIAS_teaser_15s.mp4" "MESIAS_couverture.jpg"
```

Tu dois obtenir exactement :

```
ae74866b0933d6727b41ce7693b5e088a513bb9e01cb7f0511434ede56a1275d  MESIAS_clip_leger.mp4
d54193651beb32021cb992c01a37ee4e52edf5a98edcfc8022a28beb784c3a2a  MESIAS_teaser_15s_1080x1920.mp4
679861edfd5194da9718136db4f5c03fe1acc827410746e9f18de34d3893bad2  MESIAS_couverture.jpg
```

**Une empreinte différente = fichier corrompu ou incomplet.** Ne publie pas : relance la même
commande `curl` avec `-C -`, elle reprend là où elle s'est arrêtée.

---

## 5 — Déclarer les fichiers au système (sinon TikTok ne les voit pas)

```sh
cd ~/storage/downloads
termux-media-scan -v "MESIAS_clip_leger.mp4"
termux-media-scan -v "MESIAS_teaser_15s.mp4"
termux-media-scan -v "MESIAS_couverture.jpg"
termux-media-scan -v "MESIAS_couv_visage.jpg"
termux-media-scan -v "MESIAS_couv_paysage.jpg"
termux-media-scan -v "MESIAS_master.mp3"
```

Après ça, les fichiers apparaissent dans la galerie et dans l'écran d'import de TikTok.

---

## 6 — En cas de problème

| Symptôme | Cause | Ce qu'il faut faire |
|---|---|---|
| `curl: (6) Could not resolve host` | pas de réseau ou DNS | vérifie la connexion, relance |
| `curl: (23) Failed writing body` | stockage plein | `df -h ~/storage/downloads`, libère de la place |
| Le téléchargement s'arrête au milieu | coupure réseau | relance **la même commande**, `-C -` reprend sans recommencer |
| `termux-media-scan: command not found` | paquet `termux-api` absent | `pkg install -y termux-api` + app Termux:API |
| Le fichier est dans la galerie mais TikTok ne le propose pas | index pas rafraîchi | relance `termux-media-scan -v fichier.mp4`, puis redémarre TikTok |
| `404 Not Found` | URL mal recopiée | utilise exactement le bloc de la section 3 |

---

## 7 — Une seule commande pour tout

Si tu ne veux pas copier quinze lignes, colle ce bloc entier dans Termux :

```sh
cd ~/storage/downloads && \
BASE="https://raw.githubusercontent.com/Stein500/lyric/cb0ecaf/productions/mesias/livrables" && \
for f in "MESIAS_clip_1080x1920_leger.mp4:MESIAS_clip_leger.mp4" \
         "MESIAS_teaser_15s_1080x1920.mp4:MESIAS_teaser_15s.mp4" \
         "MESIAS_couverture_TikTok_1080x1920.jpg:MESIAS_couverture.jpg" \
         "MESIAS_couverture_variante_visage_1080x1920.jpg:MESIAS_couv_visage.jpg" \
         "MESIAS_couverture_paysage_1080x1920.jpg:MESIAS_couv_paysage.jpg"; do
  src="${f%%:*}"; dst="${f##*:}"
  echo "→ $dst"
  curl -L --retry 3 -C - -o "$dst" "$BASE/$src"
done && \
curl -L --retry 3 -C - -o "MESIAS_master.mp3" \
  "$BASE/Averly%20Morillo%20-%20MESIAS%20(master%20normalise%20-14LUFS).mp3" && \
curl -L --retry 3 -C - -o "SHA256SUMS.txt" "$BASE/SHA256SUMS.txt" && \
termux-media-scan -v MESIAS_clip_leger.mp4 MESIAS_teaser_15s.mp4 MESIAS_couverture.jpg && \
echo "TERMINÉ"
```
