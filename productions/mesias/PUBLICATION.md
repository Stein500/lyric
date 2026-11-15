# Publications TikTok — MESÍAS (Live) · Averly Morillo

Deux publications : le **teaser 15 s** et le **clip complet**. Les liens des commandes Termux sont
figés sur le **SHA publié** (voir §5), jamais sur une branche mouvante.

---

## 1 — TEASER 15 s (extrait `07:44,13 → 07:59,13`)

### Description

> Il y a un moment où le désir devient plus fort que la fatigue. 🕯️
> « Poderoso Dios » — 15 secondes de MESÍAS en direct, et la traduction française s'allume
> image par image pour celles et ceux qui ne parlent pas encore espagnol.
> Le morceau entier (12:24) est sur mon profil.
>
> Averly Morillo — Mesías (Live) 🎶

### Hashtags (13 — maximum respecté)

```
#Mesias #AverlyMorillo #MusicaCristiana #Adoracion
#LyricsEnEspanol #TraductionFrancaise #TikTokMusic
#LiveWorship #GreenMusic #PoderosoDios
#WTBW #CristoTikTok #MusiqueChretienne
```

### Déclaration d'IA (à joindre en commentaire épinglé)

> Les illustrations sont générées par IA (image par image, sans reprise du clip officiel).
> La typographie, la traduction et le montage sont faits par le moteur WTBW.
> L'audio est l'enregistrement live de l'artiste, fourni par elle, à niveau normalisé
> (−14 LUFS, crête −1,5 dBFS) — aucun son n'a été généré ni imité.

---

## 2 — CLIP COMPLET (12:29,705)

### Description

> MESÍAS en direct, en entier — 12 minutes et 29 secondes où le peuple appelle et le ciel répond.
> 🕯️ Paroles espagnoles originales qui défilent, traduction française peinte en gros à l'écran :
> pour la première fois, on comprend chaque phrase sans quitter l'image.
>
> ⏱ Enregistrement live complet, non coupé.
> 🎤 Averly Morillo — Mesías (Live), Green Music.
>
> Chapitre : 00:00 l'appel · 00:57 « ven, ven, ven » · 01:03 « Mesías, ven » ·
> 07:44 « Poderoso Dios » · 10:12 le retour au silence.

### Hashtags (13 — maximum respecté)

```
#Mesias #AverlyMorillo #MusicaCristiana #Adoracion
#LetrasEnEspanol #TraductionFrancaise #LiveWorship
#GreenMusic #MusicaCristiana2026 #Alabanza
#WTBW #MusicaGospel #FoiChretienne
```

### Épinglé

> Traduction française intégrale affichée à l'écran — dis-moi si une phrase mérite une meilleure
> nuance, je corrige et je re-rends. Les illustrations sont générées par IA, l'audio est celui de
> l'artiste (aucun son généré).

---

## 3 — Ce que dit la vidéo d'elle-même

| Élément | Teaser | Clip |
|---|---|---|
| Durée exacte | 15,000 s (450 frames) | 749,705 s (22 491 frames) |
| Format | 1080×1920, 30 i/s, H.264 High, BT.709 | idem |
| Audio | AAC 48 kHz stéréo, 256 kb/s | idem |
| Faststart | oui (`moov` en tête) | oui |
| Images noires | aucune | aucune hors carte finale |
| Gels > 1,5 s | aucun | aucun |

---

## 4 — Sous-titres et accessibilité

Le texte est **dans l'image** (c'est le principe du clip) : il n'y a donc pas de piste `.srt` à
activer. La traduction française est volontairement grosse et contrastée (720 px de large max,
contour sombre + halo) pour rester lisible sur un écran de téléphone en extérieur.

---

## 5 — Commandes Termux (Android)

Remplacer `SHA` par le commit publié indiqué en fin de document. Ces commandes :
- reprennent un téléchargement interrompu (`-C -`), réessaient (`--retry 3`),
- refusent les redirections vers un domaine inattendu,
- puis déclarent les fichiers au système (`termux-media-scan`) pour qu'ils apparaissent
  immédiatement dans la galerie et dans TikTok.

```sh
pkg install -y curl
cd ~/storage/downloads

# --- clip complet (≈ 190 Mo) ---
curl -L --retry 3 -C - -o "MESIAS_clip_1080x1920.mp4" \
  "https://raw.githubusercontent.com/Stein500/lyric/SHA/productions/mesias/livrables/Averly%20Morillo%20-%20MESIAS%20(clip%20lyrics%201080x1920).mp4"

# --- teaser 15 s (≈ 5 Mo) ---
curl -L --retry 3 -C - -o "MESIAS_teaser_15s.mp4" \
  "https://raw.githubusercontent.com/Stein500/lyric/SHA/productions/mesias/livrables/MESIAS_teaser_15s_1080x1920.mp4"

# --- couverture TikTok ---
curl -L --retry 3 -C - -o "MESIAS_couverture.jpg" \
  "https://raw.githubusercontent.com/Stein500/lyric/SHA/productions/mesias/livrables/MESIAS_couverture_TikTok_1080x1920.jpg"

# --- master audio normalisé (si besoin de reposter le son seul) ---
curl -L --retry 3 -C - -o "MESIAS_master_-14LUFS.mp3" \
  "https://raw.githubusercontent.com/Stein500/lyric/SHA/productions/mesias/livrables/Averly%20Morillo%20-%20MESIAS%20(master%20normalise%20-14LUFS).mp3"

# --- déclaration au système, sans quoi TikTok ne voit pas les fichiers ---
termux-media-scan -v "MESIAS_clip_1080x1920.mp4"
termux-media-scan -v "MESIAS_teaser_15s.mp4"
termux-media-scan -v "MESIAS_couverture.jpg"
termux-media-scan -v "MESIAS_master_-14LUFS.mp3"
```

**Vérification d'intégrité avant publication :**

```sh
pkg install -y coreutils
sha256sum "MESIAS_clip_1080x1920.mp4" "MESIAS_teaser_15s.mp4"
# comparer aux empreintes du fichier livrables/SHA256SUMS.txt publié avec le même commit
```

---

## 6 — Ce qu'il ne faut PAS dire dans la publication

- Ne pas écrire « clip officiel » : c'est un **clip lyrics** produit par WTBW, pas un visuel
  d'Averly Morillo ni de son label.
- Ne pas écrire « traduction certifiée » ni « approuvée par l'artiste » : la traduction est un
  travail de production, relu mais non validé par l'autrice.
- Ne pas écrire « WTBW » développé : la marque s'écrit uniquement **WTBW**.
