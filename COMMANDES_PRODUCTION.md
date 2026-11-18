# COMMANDES DE PRODUCTION — annexe du PROMPT UNIVERSEL GOSPEL v8.0

Toutes les commandes ci-dessous sont **celles qui ont réellement produit MESÍAS**, rendues paramétrables.
Elles s'exécutent depuis la racine d'une production (`productions/<nom>/`).

**Convention de lecture :** `<…>` = à remplacer. Aucune valeur n'est un exemple inventé : les valeurs
par défaut affichées sont les mesures réelles de MESÍAS.

---

## 0 — Installer l'environnement (une fois par session)

L'environnement peut être **remis à zéro entre deux tours** : relancer cette section avant tout.

```sh
python3 -m pip install --break-system-packages -q pillow imageio-ffmpeg numpy mutagen
python3 -c "import PIL, imageio_ffmpeg, numpy, mutagen; print('dépendances OK')"
```

Il n'y a **pas** de `ffmpeg` système dans cet environnement : on utilise celui embarqué.

```sh
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
echo $FF
$FF -version | head -1
```

Créer l'arborescence :

```sh
mkdir -p data assets/fonts scripts livrables work/base work/check
```

---

## 1 — Mesurer l'audio maître (avant toute promesse)

### 1.1 Durée **décodée** réelle — jamais la durée annoncée

```sh
$FF -hide_banner -i "<master.mp3>" 2>&1 | grep -E "Duration|Stream"
$FF -hide_banner -nostats -i "<master.mp3>" -f null - 2>&1 | tail -1
```

Sur MESÍAS : annoncé 12:23, **décodé 12:24,70** (744,705 s). C'est le second chiffre qui fait foi.

### 1.2 Sonie, crête vraie, plage dynamique

```sh
$FF -hide_banner -nostats -i "<master.mp3>" -filter_complex ebur128=peak=true -f null - 2>&1 | tail -14
```

Lecture : `I:` = LUFS intégré, `Peak:` = crête vraie (dBFS), `LRA:` = plage.

### 1.3 Silence final (pour placer la carte finale)

```sh
$FF -hide_banner -nostats -i "<master.mp3>" -af "silencedetect=n=-40dB:d=1.5" -f null - 2>&1 \
  | grep -E "silence_(start|end)"
```

Sur MESÍAS : silence de **739,349 s** à 744,709 s (durée 5,360 s).

### 1.4 Extraire la piste audio sans réencodage

```sh
$FF -y -hide_banner -loglevel error -i "<master.mp3>" -map 0:a -c:a copy "<data/master_audio.mp3>"
```

### 1.5 Lire les paroles embarquées (tag `USLT`) — pour information seulement

```sh
python3 - <<'EOF'
from mutagen.id3 import ID3
t = ID3("<master.mp3>")
print([(f.FrameID, len(str(f))) for f in t.values()])
uslt = [f for f in t.values() if f.FrameID == "USLT"]
if uslt:
    open("data/paroles_du_master.lrc.txt", "w", encoding="utf8").write(str(uslt[0].text))
    print("extrait -> data/paroles_du_master.lrc.txt")
EOF
```

⚠️ Ce tag n'est **pas** une référence fiable (v8.0 §3.2). L'extraire, l'archiver, l'écarter explicitement.
`ffmpeg -f ffmetadata` ne fonctionne pas pour cela sur tous les builds (`Encoder not found`).

---

## 2 — Normaliser le master (2 passes, résultat vérifié)

### 2.1 Première passe : mesure

```sh
$FF -hide_banner -nostats -i "<master.mp3>" \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json" -f null - 2>&1 | tail -14
```

Relever `input_i`, `input_tp`, `input_lra`, `input_thresh`, `target_offset`.

### 2.2 Seconde passe : normalisation

```sh
$FF -y -hide_banner -loglevel error -i "<master.mp3>" \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=-8.77:measured_TP=4.75:measured_LRA=11.10:measured_thresh=-19.12:offset=-0.28:linear=true:print_format=summary" \
  -ar 48000 -ac 2 -c:a libmp3lame -b:a 320k -map_metadata -1 \
  "<livrables/<artiste> - <titre> (master normalise -14LUFS).mp3>"
```

Remplacer les valeurs `measured_*` par celles du §2.1. **Ne jamais les recopier de ce document.**

### 2.3 Vérifier le résultat, et **écrire le mode réellement utilisé**

```sh
$FF -hide_banner -nostats -i "<livrables/…normalise….mp3>" \
  -filter_complex ebur128=peak=true -f null - 2>&1 | grep -A2 "Integrated"
```

Sur MESÍAS : **−14,1 LUFS, crête vraie −1,5 dBFS**, et le `loudnorm` a basculé en mode
**dynamique** (entrée écrêtée à +4,7 dBFS) — c'est à noter dans le README, pas à cacher.

### 2.4 Réécrire des tags propres

```sh
$FF -y -hide_banner -loglevel error -i "<normalise.mp3>" -map 0:a -c:a copy \
  -metadata title="<titre exact>" -metadata artist="<artiste>" \
  -metadata comment="normalise I=-14 LUFS TP=-1.5, 48 kHz stereo, MP3 CBR 320" \
  "<normalise_tags.mp3>"
python3 -c "
from mutagen.mp3 import MP3
a = MP3('<normalise_tags.mp3>')
print(dict(a.tags) if a.tags else 'AUCUN TAG')
print('durée', round(a.info.length, 3))"
```

Toujours **relire les tags après écriture**. Un `-vn` est nécessaire si le fichier porte une pochette.

---

## 3 — Contrat des vers et traduction

### 3.1 Vérifier la couverture de la traduction

```sh
python3 - <<'EOF'
import json, importlib.util
spec = importlib.util.spec_from_file_location("tr", "data/traduction_fr.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
FR = mod.FR
m = json.load(open("data/verses_map.json", encoding="utf8"))
manquants = [v["i"] for v in m["verses"] if v["debut_source"] not in FR and v["i"] not in FR]
print("vers :", len(m["verses"]), "| clés :", len(FR), "| manquants :", manquants[:20])
EOF
```

**Aucun rendu si `manquants` n'est pas vide.**

### 3.2 Recaler les débuts sur un fichier de paroles (optionnel, à lire avant)

```sh
python3 scripts/sync_master.py
```

⚠️ Sur MESÍAS cette approche a **échoué** (écarts de −6,7 s à +13,2 s). Le calage validé est un
**offset global** décidé à l'écoute (§8.2 du prompt). Ne pas utiliser ce script comme preuve.

### 3.3 Appliquer l'offset d'écoute

Modifier **un seul chiffre** dans `data/verses_map.json` :

```sh
python3 - <<'EOF'
import json
p = "data/verses_map.json"
m = json.load(open(p, encoding="utf8"))
m["calage"]["offset_affichage_s"] = -0.25      # <- le chiffre donné par l'artiste
m["calage"]["statut"] = "calé à l'écoute par l'artiste"
json.dump(m, open(p, "w", encoding="utf8"), ensure_ascii=False, indent=1)
print("offset :", m["calage"]["offset_affichage_s"])
EOF
```

Négatif = le texte arrive **après** la voix, il faut l'avancer. Positif = l'inverse.

---

## 4 — Images

### 4.1 Assigner le pool par règles sémantiques

```sh
python3 scripts/assign_pool.py
```

Affiche les images utilisées et le **nombre de vers par image**. Vérifier qu'aucun plan ne dépasse
~15 vers sur 190. Si c'est le cas, le compteur d'emplois ne joue pas (v8.0 §5.5).

### 4.2 Construire les bases 1080×1920

```sh
python3 - <<'EOF'
import sys, os, glob
sys.path.insert(0, "scripts")
import render as R
os.makedirs("work/base", exist_ok=True)
for f in glob.glob("assets/*.png"):
    name = os.path.basename(f)
    R.base_image(f).save(os.path.join("work/base", name), quality=95)
print("bases :", len(os.listdir("work/base")))
EOF
```

⚠️ **Toujours en PNG**, jamais en JPEG : le moteur relit `work/base/<nom>.png`.

### 4.3 Planche de contrôle d'une salve

```sh
python3 - <<'EOF'
from PIL import Image, ImageDraw
import glob, os
files = sorted(glob.glob("assets/<motif>*.png"))     # ex. "assets/pool_1*.png"
tw, th, cols = 270, 480, 5
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * tw, rows * th), (18, 18, 24))
d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f).convert("RGB"); im.thumbnail((tw, th))
    x, y = (i % cols) * tw, (i // cols) * th
    sheet.paste(im, (x + (tw - im.width) // 2, y + (th - im.height) // 2))
    d.text((x + 6, y + 6), os.path.basename(f)[:18], fill=(255, 220, 140))
sheet.save("work/check/salve.jpg", quality=90)
print("planche ->", "work/check/salve.jpg")
EOF
```

**Contrôler la planche avant d'intégrer.** Une image fautive se régénère, elle ne se rattrape pas.

### 4.4 Prévisualiser un vers avec son texte réel

```sh
python3 -c "
import sys; sys.path.insert(0,'scripts')
import render
render.preview('<image>.png', <index_vers>, '/tmp/pv.png')
print('-> /tmp/pv.png')"
```

---

## 5 — Rendu

### 5.1 Maquette courte (à faire écouter)

```sh
python3 scripts/render_video.py --from 1 --to 12 \
  --out work/maquette_1-12.mp4 --crf 24 \
  --audio "livrables/<artiste> - <titre> (master normalise -14LUFS).mp3"
```

C'est **ce fichier** qu'on envoie à l'artiste pour obtenir l'offset. Pas le clip complet.

### 5.2 Clip complet, par segments

La durée décodée et le silence final sont **passés en paramètres** — ne jamais les coder en dur
pour une nouvelle chanson.

```sh
DUR=$(python3 -c "print(744.705)")     # durée DÉCODÉE mesurée (§1.1)
SIL=$(python3 -c "print(739.349)")     # silence final mesuré (§1.3)

for i in $(seq 0 39); do
  python3 scripts/render_clip.py --seg $i 40 --crf 21 \
    --dur-audio $DUR --silence $SIL --tail 5.00 \
    --audio "livrables/<master normalise>.mp3" \
    --out work/clip_seg$i.mp4 || echo "ECHEC segment $i"
done
```

Compter **30 à 45 s par segment** (machine à 2 cœurs). 40 segments ≈ 25 minutes.

### 5.3 Assembler

```sh
python3 scripts/render_clip.py --assemble \
  --dur-audio $DUR --silence $SIL --tail 5.00 \
  --audio "livrables/<master normalise>.mp3"
```

Le script affiche la durée totale attendue **avant** de rendre. Vérifier le nombre de frames
(`(DUR + tail) × 30`). Sur MESÍAS : **22 491 frames / 749,705 s**.

### 5.4 Teaser 15 s (450 frames exactement)

```sh
python3 scripts/render_clip.py --teaser --teaser-start <début_en_secondes> --crf 21
```

`--teaser-start` doit être un instant **du morceau réel**, pas une estimation.

---

## 6 — Version publiable (sous 95 Mo)

### 6.1 Calibrer AVANT d'encoder les 12 minutes

```sh
# 120 s au réglage visé, puis extrapolation
$FF -y -hide_banner -loglevel error -ss 300 -t 120 -i "<clip_master.mp4>" \
  -c:v libx264 -preset slow -crf 31 -maxrate 1150k -bufsize 2300k -pix_fmt yuv420p -an /tmp/calib.mp4
python3 -c "
import os
s = os.path.getsize('/tmp/calib.mp4')
print('extrait 120 s :', s//1024, 'Ko -> estimation', round(s*<DUREE>/120/1048576), 'Mo sur', <DUREE>//60, 'min')"
```

Sur MESÍAS : CRF 29 → 124 Mo (trop) ; **CRF 31 + `maxrate` 1150k → 98,8 Mo** ✅.

### 6.2 Encoder la version publiable

```sh
$FF -y -hide_banner -loglevel error -i "<clip_master.mp4>" \
  -c:v libx264 -preset slow -crf 31 -maxrate 1150k -bufsize 2300k \
  -pix_fmt yuv420p -x264-params keyint=60:min-keyint=30 \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -c:a aac -b:a 128k -ar 48000 -movflags +faststart \
  "livrables/MESIAS_clip_1080x1920_leger.mp4"
```

### 6.3 Vérifier à l'œil (zoom 1:1 sur le texte)

```sh
$FF -y -hide_banner -loglevel error -ss 410 -i "<clip_master.mp4>" -frames:v 1 /tmp/orig.png
$FF -y -hide_banner -loglevel error -ss 10  -i "<leger.mp4>"       -frames:v 1 /tmp/leger.png
python3 -c "
from PIL import Image
a = Image.open('/tmp/orig.png').crop((300,1050,780,1250))
b = Image.open('/tmp/leger.png').crop((300,1050,780,1250))
s = Image.new('RGB', (960, 810)); s.paste(a,(0,0)); s.paste(b,(0,410))
s.save('work/check/q.jpg', quality=96); print('-> work/check/q.jpg')"
```

---

## 7 — Couvertures (1080×1920, JPEG)

```sh
python3 scripts/make_cover.py
```

Trois fichiers : principale, variante visage, variante paysage. **Aucun texte sur le visage**,
rien sous `y = 1574`.

---

## 8 — Contrôles chiffrés (sur le fichier **assemblé**, pas les segments)

```sh
python3 scripts/checks.py "livrables/<clip>.mp4" --expect <DUREE_TOTALE> --json work/check/checks.json
```

Sortie attendue :

| Contrôle | Attendu |
|---|---|
| `duree_s` | = durée cible à 0,01 s près |
| `black` | `[]` |
| `freeze` | `[]` (seuil serré 1,2 s) |
| `loudness.I` | ≈ −14,1 |
| `loudness.peak` | ≤ −1,0 |
| `faststart` | `True` |
| `ecart_duree_s` | ≈ 0 |

Commandes directes si le script n'est pas disponible :

```sh
$FF -hide_banner -nostats -i "<clip>.mp4" -vf "blackdetect=d=0.5:pix_th=0.10" -an -f null - 2>&1 | grep black_start
$FF -hide_banner -nostats -i "<clip>.mp4" -vf "freezedetect=n=0.001:d=1.2" -an -f null - 2>&1 | grep freeze_
$FF -hide_banner -nostats -i "<clip>.mp4" -filter_complex ebur128=peak=true -f null - 2>&1 | tail -12
python3 -c "
d=open('<clip>.mp4','rb').read(4*1024*1024)
print('faststart :', d.find(b'moov') < d.find(b'mdat'))"
```

---

## 9 — Empreintes et livraison

```sh
cd livrables
ls -1 | grep -v '^SHA256SUMS' > /tmp/l.txt
xargs -a /tmp/l.txt -d '\n' sha256sum > SHA256SUMS.txt
sha256sum -c SHA256SUMS.txt
```

**Ne jamais lister dans `SHA256SUMS.txt` un fichier absent du dépôt** : le contrôle échoue
et l'utilisateur croit à une corruption (panne réelle sur MESÍAS).

```sh
cd ../..
git add -A && git commit -m "<production>: <étape>" && git push origin <branche>
SHA=$(git rev-parse HEAD)
echo "liens à figer sur $SHA"
```

Vérifier la présence réelle des fichiers côté GitHub avant de donner les URL :

```sh
gh api "repos/<compte>/<dépôt>/contents/<chemin>?ref=$SHA" --jq '.[] | "\(.name)\t\(.size)"'
```

---

## 10 — Termux (à recopier dans la livraison)

```sh
pkg install -y curl coreutils termux-api
termux-setup-storage
BASE="https://raw.githubusercontent.com/<compte>/<dépôt>/<SHA>/<chemin>"

curl -L --retry 3 -C - -o "clip.mp4" "$BASE/clip.mp4"
curl -L --retry 3 -C - -o "teaser.mp4" "$BASE/teaser.mp4"
curl -L --retry 3 -C - -o "couverture.jpg" "$BASE/couverture.jpg"

termux-media-scan -v "clip.mp4" "teaser.mp4" "couverture.jpg"

sha256sum "clip.mp4" "teaser.mp4"
```

- `-C -` reprend un téléchargement interrompu.
- `termux-media-scan` est **obligatoire**, sinon TikTok ne voit pas les fichiers.
- URL **figées sur le SHA**, jamais sur un nom de branche.

---

## 11 — Diagnostic des pannes connues

| Symptôme | Cause | Commande de diagnostic | Correctif |
|---|---|---|---|
| durée trop courte de 5 s | `-shortest` | `python3 scripts/checks.py <f> --expect <duree>` | `apad=whole_dur=<T> -t <T>` |
| `freezedetect` signale un gel | trajectoire en sinus | `freezedetect=n=0.001:d=1.2` | rampes triangulaires |
| carte figée malgré un panoramique | fond déjà recadré, débattement nul | `python3 -c "from PIL import Image;print(Image.open('<base>.png').size)"` | garder la source surdimensionnée (1,30×) |
| arête horizontale dans le voile | rampe linéaire | capture d'un frame | `alpha = strength·t²(3−2t)` |
| `GH001 pre-receive hook declined` | fichier > 100 Mo | `du -h livrables/*` | version allégée, ou release |
| `uploads.github.com … EOF` | domaine bloqué dans le sandbox | `curl -sS -m 10 -o /dev/null -w "%{http_code}" https://uploads.github.com/` | publier depuis une machine connectée |
| `ModuleNotFoundError: PIL` | sandbox remis à zéro | `python3 -c "import PIL"` | §0 de ce document |
| `Encoder not found` sur `-f ffmetadata` | muxeur absent du build | — | passer par `mutagen` |
| `loudnorm` en mode dynamique | crête d'entrée au-dessus de 0 dBFS | lire `normalization_type` dans la sortie | **le déclarer**, ce n'est pas une erreur |

---

## 12 — Ordre d'exécution condensé

```sh
# 0. environnement
python3 -m pip install --break-system-packages -q pillow imageio-ffmpeg numpy mutagen

# 1. mesurer
$FF -hide_banner -nostats -i "<master>" -f null - 2>&1 | tail -1
$FF -hide_banner -nostats -i "<master>" -af "silencedetect=n=-40dB:d=1.5" -f null - 2>&1 | grep silence_start

# 2. normaliser (2 passes, valeurs relevées, PAS recopiées)
# 3. contrat + traduction (couverture 100 %)
# 4. images : ancre -> salves de 10 -> planches -> assign_pool.py -> bases
# 5. maquette 12 vers -> FAIRE ÉCOUTER -> offset
# 6. segments -> assemblage
# 7. checks.py --expect <durée totale>
# 8. version < 95 Mo (calibrer sur 120 s d'abord) -> contrôle à l'œil
# 9. teaser 15 s -> couvertures
# 10. sha256sum -> commit -> push -> URL figées sur le SHA -> Termux
```
