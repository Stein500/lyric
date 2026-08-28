# 🎂 Chantier — Joyeux Anniversaire KLO (3 vidéos 9:16)

**Son :** `klo/Joyeux anniversaire Klo.mp3` — durée exacte **105.024 s** (1:45), 48 kHz stereo.
**Format livré :** 1080×1920 (9:16) → statut WhatsApp + TikTok/Reels/Shorts.
**Date de Klo :** 30 août. Surnoms : **Klo / Confiance / JésuKlo**.
**Charte :** TechStein (badge « ⚡ DAÏSKY PROD » statique incrusté en post, paroles en ASS, zéro trou noir, fade audio in/out).

## 3 vidéos (visuels / ambiance différents, même son + paroles)
1. **V1 — Festif Or/Rose** : photos robe rose + tresses perles, bokeh doré, gâteau, feux d'artifice.
2. **V2 — Nuit Cyan « Ma Lumière »** : photos cosy Stitch, ciel étoilé cyan, néon, feux d'artifice.
3. **V3 — Party Confettis** : les 9 photos mélangées, confettis/ballons, néon, feux d'artifice.

## Ressources
- 9 photos d'origine : `assets/raw/portrait/IMG-20260827-WA00{02..10}.jpg` (960×1280, 3:4).
- 7 fonds générés (sans visage/texte) : `assets/gen/` gold_bokeh, gold_roses, cake, fireworks, cyan_stars, cyan_party, confetti.

## Minutage (son 105.024 s) — paroles calées sur les horaires de l'artiste
| De–À (s) | Texte | Voix/Style |
|---|---|---|
| 1.0–12.2 | Titre : KLO / Confiance / 30 août | carte titre |
| 8.8–11.8 | Wolof TechStein beat wê… | signature |
| 12.3–17.0 | Joyeux anniversaire, Klo | refrain |
| 17.0–22.0 | Joyeux anniversaire, ma lumière | refrain |
| 22.0–27.0 | 30 août, c'est ton jour | refrain |
| 27.0–33.2 | Le monde est plus beau quand tu es là | refrain |
| 33.2–35.2 | Tu es la joie, tu es la paix | couplet M |
| 35.2–38.0 | Chaque jour avec toi est un rêve | couplet M |
| 38.0–40.2 | Je te souhaite tout le bonheur | couplet M |
| 40.2–44.2 | Ma Confiance, mon cœur | couplet M |
| 44.2–46.2 | Tu es la joie, tu es la paix | couplet F |
| 46.2–49.0 | Chaque jour avec toi est un rêve | couplet F |
| 49.0–51.2 | Je te souhaite tout le bonheur | couplet F |
| 51.2–54.5 | Ma Confiance, mon cœur | couplet F |
| 54.5–57.2 | Que cette année soit belle | pont |
| 57.2–59.5 | Que tes rêves deviennent réels | pont |
| 59.5–62.3 | Klo, tu es unique | pont |
| 62.3–65.2 | Confiance, tu es magnifique | pont |
| 65.2–71.2 | Joyeux anniversaire, JésuKlo… | outro |
| 71.2–78.8 | Joyeux anniversaire, Confiance… | outro |
| 79.0–82.5 | Wolof TechStein beat wê… | signature |
| 91.0–94.5 | Wolof TechStein beat wê… | signature |
| 95.0–103.5 | Carte de clôture : Joyeux Anniversaire Klo / Confiance | carte |

## Pipeline
1. PIL : frames 1080×1920 (photo = carte arrondie sur fond flouté + halo couleur ; bg = cover + voile bas).
2. ffmpeg zoompan (Ken Burns doux, alterné) → clips → xfade (fondu 0.6 s, zéro trou noir).
3. Overlay badge PNG statique + burn ASS paroles + mux audio (afade in 0.3 s / out 3 s).
4. QA : durée = 105 s ±0.3, blackdetect = 0, inspection de frames.

## Livrables
- `livrables/Klo_Anniversaire_V1_FestifOr_9x16.mp4`
- `livrables/Klo_Anniversaire_V2_NuitCyan_9x16.mp4`
- `livrables/Klo_Anniversaire_V3_PartyConfettis_9x16.mp4`

**Signature :** Wolof TechStein beat wê ! ⚡
