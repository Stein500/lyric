# 🚀 LIVRAISON — « Ça monte, ça descend » (Daïsky)

> **Branche :** `arena/60458a92-lyric`
> **HASH à utiliser pour Termux :** `__HASH__` *(à régénérer après commit/push final)*

## 📦 Livrables
Une fois `pipeline_complet.sh` terminé :

```
livrables/
  Ca_monte_ca_descend_9x16_v1.mp4          ← clip 9:16 (1080×1920, 30 fps, 208,64 s)
  Ca_monte_ca_descend_16x9_v1.mp4          ← clip 16:9 (1920×1080, 30 fps, 208,64 s)
  Ca_monte_ca_descend_master_320k.mp3      ← master audio 320 kb/s, ID3v2.4 + APIC + USLT
  cover_Ca_monte_ca_descend_1080x1080.jpg  ← cover carrée (APIC + Spotify/Apple)
  cover_Ca_monte_ca_descend_9x16.jpg       ← cover 9:16 (TikTok / Reels / Shorts)
  cover_Ca_monte_ca_descend_16x9.jpg       ← cover 16:9 (YouTube)
```

## ✍️ Titre, Caption, Hashtags (à publier dès le 9:16 livré — Instructions A point 8)

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

## ▶️ Commandes Termux (une ligne par fichier, séparateur `;`)

> Remplace `__HASH__` par le vrai hash après `git push` (la commande `git rev-parse HEAD` le donne).

```bash
pkg update -y; pkg install -y curl ca-certificates; termux-setup-storage
```

```bash
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/Ca_monte_ca_descend_9x16_v1.mp4 https://raw.githubusercontent.com/Stein500/lyric/__HASH__/livrables/Ca_monte_ca_descend_9x16_v1.mp4
```

```bash
curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/Ca_monte_ca_descend_16x9_v1.mp4 https://raw.githubusercontent.com/Stein500/lyric/__HASH__/livrables/Ca_monte_ca_descend_16x9_v1.mp4
```

```bash
curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/Ca_monte_ca_descend_master_320k.mp3 https://raw.githubusercontent.com/Stein500/lyric/__HASH__/livrables/Ca_monte_ca_descend_master_320k.mp3
```

```bash
curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/cover_Ca_monte_ca_descend_1080x1080.jpg https://raw.githubusercontent.com/Stein500/lyric/__HASH__/livrables/cover_Ca_monte_ca_descend_1080x1080.jpg
```

```bash
curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/cover_Ca_monte_ca_descend_9x16.jpg https://raw.githubusercontent.com/Stein500/lyric/__HASH__/livrables/cover_Ca_monte_ca_descend_9x16.jpg
```

```bash
curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/cover_Ca_monte_ca_descend_16x9.jpg https://raw.githubusercontent.com/Stein500/lyric/__HASH__/livrables/cover_Ca_monte_ca_descend_16x9.jpg
```

```bash
curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/PROMPT_UNIVERSEL_v5.6_AUBE_CLOCHETTES.md https://raw.githubusercontent.com/Stein500/lyric/__HASH__/PROMPT_UNIVERSEL_v5.6_AUBE_CLOCHETTES.md
```

## 🔁 Pipeline de production (rappel)

```bash
bash scripts/setup_env.sh       # crée /tmp/lyric-venv
# 1) Génère les 5 fonds portrait + 5 paysage via ton provider IA
#    (voir productions/ca_monte_ca_descend/PROMPT_ANCRES_ET_SALVE.md)
# 2) Pose-les dans assets/raw/portrait/ et assets/raw/landscape/
bash scripts/pipeline_complet.sh
```

## 📜 Notes de production
- **Héros inventé** (aucune photo perso, règle v5.5 §2) — bloc recopié à l'identique dans les 10 prompts.
- **Style S3 Neon Afro-Futurism** (mariage parfait v5.6 × S3 pour club/fête).
- **Cold-open 6 s** sur le refrain-titre (53,32 → 59,20 s).
- **Clochettes v5.6** dans les 23 fenêtres ≥ 5 s, avec **PARTAGE prioritaire** et textes UI en qualité premium.
- **Plus de drapeau en bas des vidéos** — uniquement sur covers et bandeau bas d'endcard.
- **Plus de contact/email** à l'endcard — « Merci d'avoir regardé » + **code 9-7-6-1** facile à retenir.
- **Carton intro** : « Regarde jusqu'à la fin pour découvrir comment proposer un son ou un lyrics à réaliser pour toi ! ».
- **Safe zones 9:16 strictes** : badge y=150, paroles H/2 dans la fenêtre 720 px, rail droit et bande basse libres.
- **Endcard sans contacts** : titre cursive + merci + code + sous-titre « la courbe qui monte, qui descend ».
