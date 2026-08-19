# « I'm not afraid » — Lyric video (Daïsky × TechStein)

Clip **lyrics** en **kinetic typography**, calé sur `not afraid.mp3` (3:35). Reprend l'univers de *« I'm Not Dying »* : **phénix aux couleurs du Bénin** (vert / jaune-or / rouge), **flammes et braises**, **fond noir**, typographie **brush/graffiti** pour les moments choc.

> ⚡ **Méthode de rendu RAPIDE (ffmpeg)** — arrière-plans générés par IA qui **reviennent selon les paroles**, animés en Ken Burns + fondus, texte superposé synchronisé. Rendu complet en **~4 minutes** (au lieu de ~40 min avec un rendu navigateur image-par-image).

---

## Rendu rapide (recommandé)

```bash
cd remotion
npm install

# 1) Arrière-plans IA (déjà générés dans public/bg/ — 7 humeurs récurrentes)
# 2) Overlays texte (PNG transparents, une fois par ligne) — nécessite Chromium
./scripts/setup-browser.sh
LD_LIBRARY_PATH=/tmp/chromium-libs/lib node --experimental-strip-types scripts/render-text-overlays.mjs

# 3) Assemblage + encodage (~4 min) — ffmpeg statique complet embarqué via npm
node --experimental-strip-types scripts/build-video.mjs
# → out/im-not-afraid.mp4 (1920×1080, h264 + AAC)
```

Pour un **test rapide** des 16 premières secondes :

```bash
node --experimental-strip-types scripts/build-video.mjs 16
# → out/test-fast.mp4
```

---

## Les 7 arrière-plans IA (récurrents selon les paroles)

| Image | Humeur | Sections |
|---|---|---|
| `bg-intro.png` | Braise unique sur noir | Intro (0–34) |
| `bg-verse2.png` | Silhouette face aux flammes (combat) | Tag ×3 (34–50) + Couplet 2 (108.8–124.8) |
| `bg-verse1.png` | Silhouette voûtée, froid désaturé (la chute) | Couplet 1 (50–73) |
| `bg-prerefrain.png` | Feu montant + plumes qui apparaissent | Pré-refrains ×2 (73–89.9, 124.8–140) |
| `bg-chorus.png` | Phénix Bénin + explosion d'étincelles | Refrain 1 (89.9–108.8) |
| `bg-bridge.png` | Phénix doré apaisé (libération) | Pont (140–160) + Outro (195–215.2) |
| `bg-final.png` | Apothéose, phénix plein cadre | Refrain final + Tag final (160–195) |

Le mapping sections → image est dans `scripts/build-video.mjs` (tableau `SEGMENTS`).

---

## Contenu — les 12 scènes au minutage exact

| # | Scène | Temps | Effet texte |
|---|-------|-------|-------------|
| 1 | Intro | 0:00–0:13 | 3 CTA (🔔 ❤️ 💬) + titre brush à liseré rouge |
| 2 | Ad-lib + mini-hook | 0:13–0:34 | Mots qui claquent, parenthèses « pensée » |
| 3 | Tag signature ×3 | 0:34–0:50 | Stamp animé, cycle rouge → or → vert |
| 4 | Couplet 1 « La chute » | 0:50–1:13 | Blanc gras, citation en italique, flamme sur « flamme » |
| 5 | Pré-refrain 1 | 1:13–1:29 | Mots-clés en or |
| 6 | Refrain 1 | 1:29–1:48 | Scale-punch visuel, stamp court |
| 7 | Couplet 2 « Le combat » | 1:48–2:04 | Clé dorée sur « clé », fracture sur « cicatrice » |
| 8 | Pré-refrain 2 | 2:04–2:20 | Comme scène 5, plus intense |
| 9 | Pont « La libération » | 2:20–2:40 | Texte qui flotte, halo doré |
| 10 | Refrain final | 2:40–2:57 | Apothéose |
| 11 | Tag final ×3 | 2:57–3:15 | Stamp plus grand/rapide |
| 12 | Outro | 3:15–3:35 | Dernier écho, CTA, logo « Daïsky Pro × TechStein 🇧🇯 » + mention *I'm Not Dying* |

---

## Structure

```
scripts/
  render-text-overlays.mjs  # rend les 56 lignes en PNG transparents (Chromium + polices npm)
  build-video.mjs           # assemble : Ken Burns + fondus + texte + audio (ffmpeg)
  setup-browser.sh          # prépare Chromium (réseau limité à npm)
src/                        # source Remotion (12 scènes, arcs couleur/flamme/phénix)
public/
  bg/                       # 7 arrière-plans IA (16:9)
  assets/                   # phénix + visuels Stories (image-to-video possibles)
  not afraid.mp3            # la chanson
out/
  text/                     # overlays texte générés (gitignoré)
  im-not-afraid.mp4         # rendu final (gitignoré)
```

### Points clés d'implémentation

- **Synchronisation texte/voix** : chaque ligne est calée sur `start`/`end` (dans `src/data.ts`) ; `build-video.mjs` décale chaque PNG via `setpts` et le fond en fondu (`fade … :alpha=1`).
- **Typographie** : *Permanent Marker* (brush), *Anton* (display), *Archivo* (texte), *Inter* (UI) — polices embarquées via npm (`@fontsource/*`), mots-clés émotionnels en **or**.
- **Arrière-plans vivants** : `zoompan` (Ken Burns lent) + fondus entre sections + `vignette` + `noise` (grain cinématique).
- **Rendu déterministe** : tout est piloté par les mêmes données de timing.

---

## Ajuster

- **Timing / paroles / mots-clés** : `src/data.ts` (puis re-générer les overlays + re-render).
- **Mapping image → section** : tableau `SEGMENTS` dans `scripts/build-video.mjs`.
- **Durée de fondu / grain / saturation** : `FAD`, `noise`, `eq` dans `build-video.mjs`.
- **Images de référence pour Runway/Kling** : `public/assets/phoenix_main.png` (Bénin) et `phoenix_gold.png` (doré).
