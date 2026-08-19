# « I'm not afraid » — Lyric video (Daïsky × TechStein)

Clip **lyrics** en **kinetic typography**, généré par code avec [Remotion](https://remotion.dev), calé sur `not afraid.mp3` (3:35). Reprend l'univers de *« I'm Not Dying »* : **phénix aux couleurs du Bénin** (vert / jaune-or / rouge), **flammes et braises**, **fond noir**, typographie **brush/graffiti** pour les moments choc.

> Ce repo contient le **moteur de rendu** (pas le MP4 final). Le MP4 est produit par la commande ci-dessous.

---

## Rendu

```bash
cd remotion
npm install

# 1) Préparer Chromium (le réseau ne laisse passer que npm)
./scripts/setup-browser.sh

# 2) Rendu 16:9 (YouTube) — 1920×1080, ~3:35
LD_LIBRARY_PATH=/tmp/chromium-libs/lib \
  npx remotion render src/index.tsx ImNotAfraidLyrics out/im-not-afraid.mp4 \
  --browser-executable=/tmp/chromium

# 3) Rendu 9:16 (TikTok / Reels / Shorts / Stories) — 1080×1920
LD_LIBRARY_PATH=/tmp/chromium-libs/lib \
  npx remotion render src/index.tsx ImNotAfraidVertical out/im-not-afraid-vertical.mp4 \
  --browser-executable=/tmp/chromium
```

**Studio / aperçu interactif** (navigateur) :

```bash
LD_LIBRARY_PATH=/tmp/chromium-libs/lib \
  npx remotion studio src/index.tsx --browser-executable=/tmp/chromium
```

---

## Contenu — les 12 scènes au minutage exact

| # | Scène | Temps | Effet |
|---|-------|-------|-------|
| 1 | Intro | 0:00–0:13 | Braise qui s'allume, 3 CTA (🔔 ❤️ 💬) + titre brush à liseré rouge |
| 2 | Ad-lib + mini-hook | 0:13–0:34 | Éclat de flamme, mots qui claquent (flash blanc), parenthèses « pensée » |
| 3 | Tag signature ×3 | 0:34–0:50 | Stamp animé, cycle rouge → or → vert |
| 4 | Couplet 1 « La chute » | 0:50–1:13 | Désaturé/froid, silhouette, flamme qui s'allume à « une flamme », citation en italique, fissure sur « forgé » |
| 5 | Pré-refrain 1 | 1:13–1:29 | Montée en saturation, plumes du phénix en filigrane |
| 6 | Refrain 1 | 1:29–1:48 | Phénix en grand, explosion de particules, scale-punch, stamp court |
| 7 | Couplet 2 « Le combat » | 1:48–2:04 | Chaleur orangée, clé dorée sur « clé », fracture lumineuse sur « cicatrice » |
| 8 | Pré-refrain 2 | 2:04–2:20 | Comme la scène 5, en plus intense |
| 9 | Pont « La libération » | 2:20–2:40 | Ralenti doré apaisé, texte qui flotte, phénix en vol calme |
| 10 | Refrain final | 2:40–2:57 | Apothéose, saturation maximale, flashs sur le beat |
| 11 | Tag final ×3 | 2:57–3:15 | Stamp plus grand/plus rapide, tremblement « drop » |
| 12 | Outro | 3:15–3:35 | Dernier écho, CTA de clôture, logo « Daïsky Pro × TechStein 🇧🇯 » + mention *I'm Not Dying* |

**Arc de couleur** (désaturé/froid → chaud → explosion → or → saturation max) : implémenté par interpolation de courbes dans [`src/theme.ts`](src/theme.ts) (`gradeAt`, `flameAt`, `phoenixAt`).

---

## Structure

```
src/
  index.tsx            # compositions (16:9 + 9:16)
  Root.tsx             # audio + LyricVideo
  LyricVideo.tsx       # assemblage fond + scènes + grain
  theme.ts             # polices, palette, arcs (couleur/flamme/phénix), easing
  data.ts              # les 12 scènes, paroles + traductions + minutage
  icons.tsx            # icônes SVG (bell/heart/comment/share/key/flag…)
  components/
    Background.tsx     # braises, fumée, phénix, flamme, teinte, vignette, grain
    text.tsx           # kinetic type : lignes, mots-clés or, stamps, CTA, titre
public/
  not afraid.mp3       # la chanson
  assets/phoenix_*.png # visuels phénix (Bénin / or) — image-to-video possibles
```

### Points clés d'implémentation

- **Synchronisation texte/voix** : chaque ligne est un `<Sequence>` démarrant à `start` secondes ; les mots « pop » un par un (scale + flash blanc) sur les refrains, et montent du bas (fade-up) sur les couplets.
- **Mots-clés émotionnels** en **or** (`emphasis`), icône **clé dorée** sur « clé », **fracture lumineuse** (SVG) sur « cicatrice ».
- **Polices** embarquées via npm (`@fontsource/*`) : *Permanent Marker* (brush/graffiti), *Anton* (display), *Archivo* (texte), *Inter* (UI) — aucune dépendance à Google Fonts.
- **Rendu déterministe** : PRNG seedé pour les braises (rendu stable entre deux exports).

---

## Ajuster

- **Timing / paroles** : tout est dans [`src/data.ts`](src/data.ts).
- **Taille / format** : `width`/`height` des compositions dans [`src/index.tsx`](src/index.tsx) (les tailles de texte s'adaptent automatiquement).
- **Images de référence pour Runway/Kling** : `public/assets/phoenix_main.png` (phénix Bénin) et `phoenix_gold.png` (phénix doré du pont) sont prêtes pour l'image-to-video.
