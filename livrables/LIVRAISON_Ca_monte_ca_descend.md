# 🚀 LIVRAISON FINALE — « Ça monte, ça descend » (Daïsky)

> **Branche :** `arena/60458a92-lyric` · **HASH :** `258b4035cdf64d8ff0c83b99d674bed35c66b5f0`

## 📦 Livrables (commités sur la branche)
```
livrables/
  Ca_monte_ca_descend_16x9_v1.mp4            21 Mo   1920×1080 · H.264 · 30 fps · 3:28 · AAC 192 kb/s
  Ca_monte_ca_descend_master_320k.mp3         8 Mo   320 kb/s · 48 kHz · -14 LUFS / -1,8 dBTP · ID3v2.4 + APIC + USLT
  cover_Ca_monte_ca_descend_1080x1080.jpg   227 ko   cover carrée (APIC du master, Spotify/Apple)
  cover_Ca_monte_ca_descend_9x16.jpg        351 ko   cover verticale (TikTok / Reels / Shorts)
  cover_Ca_monte_ca_descend_16x9.jpg        451 ko   cover horizontale (YouTube)
```

## ✍️ Titre, Caption, Hashtags (à publier dès que la vidéo est prête)

**Titre :** `Ça monte, ça descend — Daïsky`
**Caption :**
```
🔼🔽 Wolof TechStein beat wê !
3h du mat' dans l'club, le beat qui tape, tout l'monde debout.
« Prépare-toi, ça va drop fort. »

🎧 Dispo maintenant (lien en bio)
Retiens bien le code : 9 - 7 - 6 - 1
#CaMonteCaDescend #Daïsky #WolofTechStein #AfroHouse #BeninMusic #ClubVibes
```

## 🎬 Le clip 16:9 — 6 frames avec action continue
1. **00:00–00:14** — Le héros sur le trottoir, main sur la poignée
2. **00:14–00:46** — Il pousse la porte, magenta/cyan, foule en arrière-plan
3. **00:46–01:18** — Il danse au milieu de la piste, sourire, bras mobiles
4. **01:18–01:46** — Il se penche vers le DJ booth, dialogue avec le DJ
5. **01:46–02:32** — Il s'arrête contre un pilier en béton, reprend son souffle
6. **02:32–03:17** — Il remonte sur scène, micro en main, drop final + confettis
7. **03:17–03:28** — Endcard : titre + « Merci d'avoir regardé » + **code 9-7-6-1**

Mouvement continu garanti par **Ken Burns 1,02→1,08 + pan sinusoïdal + fondu 0,4 s** entre chaque vers (règle v5.5 §11.2).

## ✅ Conformité aux Instructions A (points 1 à 10)
- ✅ Point 1 — Analyse complète du morceau (197,64 s · ~97 BPM · 23 fenêtres CTA).
- ✅ Point 2 — v5.6 (couches clochettes) + v5.5 (règles) lus.
- ✅ Point 3 — **Mariage parfait v5.6 × S3 Neon Afro-Futurism** appliqué.
- ✅ Point 4 — **Endcard sans contact/email/téléphone**, juste « Merci d'avoir regardé ».
- ✅ Point 5 — **Carton intro** : « Regarde jusqu'à la fin pour découvrir comment proposer un son ou un lyrics à réaliser pour toi ! ».
- ✅ Point 6 — **Code 9-7-6-1** facile à retenir (9-7 = BPM, 6-1 = la courbe).
- ✅ Point 7 — **Plus de drapeau du Bénin en bas des vidéos** — uniquement sur les 3 covers et en fin d'endcard si tu veux l'ajouter (ici on l'a mis sur les covers uniquement).
- ✅ Point 8 — **Titre, Caption, Hashtags** listés ci-dessus dès maintenant.
- ✅ Point 9 — **Clochette vectorielle** + textes UI en qualité premium (DejaVu Sans Bold, PARTAGE prioritaire, contour cyan pulsé).
- ✅ Point 10 — **Lisibilité totale 16:9** : paroles base H-170 (y=910), badge top-left, endcard centrée cx=0,38·W (x=729).

## ⛔ Points 11 à 14 — refusés (contenu sexuel explicite)
Voir historique de la conversation — refus maintenu sans dérogation.

## ▶️ Commandes Termux (une ligne par fichier, séparateur `;`)

```bash
pkg update -y; pkg install -y curl ca-certificates; termux-setup-storage
```

```bash
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/Ca_monte_ca_descend_16x9_v1.mp4 https://raw.githubusercontent.com/Stein500/lyric/258b4035cdf64d8ff0c83b99d674bed35c66b5f0/livrables/Ca_monte_ca_descend_16x9_v1.mp4
```

```bash
curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/Ca_monte_ca_descend_master_320k.mp3 https://raw.githubusercontent.com/Stein500/lyric/258b4035cdf64d8ff0c83b99d674bed35c66b5f0/livrables/Ca_monte_ca_descend_master_320k.mp3
```

```bash
curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/cover_Ca_monte_ca_descend_1080x1080.jpg https://raw.githubusercontent.com/Stein500/lyric/258b4035cdf64d8ff0c83b99d674bed35c66b5f0/livrables/cover_Ca_monte_ca_descend_1080x1080.jpg
```

```bash
curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/cover_Ca_monte_ca_descend_9x16.jpg https://raw.githubusercontent.com/Stein500/lyric/258b4035cdf64d8ff0c83b99d674bed35c66b5f0/livrables/cover_Ca_monte_ca_descend_9x16.jpg
```

```bash
curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/cover_Ca_monte_ca_descend_16x9.jpg https://raw.githubusercontent.com/Stein500/lyric/258b4035cdf64d8ff0c83b99d674bed35c66b5f0/livrables/cover_Ca_monte_ca_descend_16x9.jpg
```

## 🔁 Pour rejouer le pipeline (régénération)
```bash
bash scripts/setup_env.sh       # crée /tmp/lyric-venv
# Génère les 6 fonds paysage avec generate_image, prompts dans productions/ca_monte_ca_descend/PROMPT_ANCRES_ET_SALVE.md
# Place-les dans assets/raw/landscape/s01_*.png ... s06_*.png
bash scripts/pipeline_complet.sh
```
