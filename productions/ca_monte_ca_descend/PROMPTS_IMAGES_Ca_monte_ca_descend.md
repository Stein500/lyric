# 🎨 PROMPTS IMAGES — « Ça monte, ça descend » (Daïsky)

**Style retenu :** S3 NEON AFRO-FUTURISM (mariage parfait v5.6 × S3 pour énergie club).
**Héros :** inventé cohérent (aucune photo personnelle transmise · règle v5.5 §2).
**Budget :** `MODE_IMAGES=cinq_scenes`, `N_SCENES=5`, `FORMATS=[9:16, 16:9]` → **10 fonds** (5 scènes × 2 formats).
**Arc lumineux S3 :** `dim` intro → `modérée` couplets → `full neon` refrains → `cyan` pont → `magenta/or` refrain 3 → `chaud décroissant` outro.

## BLOC HÉROS (à recopier à l'identique dans chaque prompt)
> A young Wolof man, 26, lean and athletic but not muscular, medium-dark skin with warm undertones, short fade haircut with subtle blonde tips, light stubble beard, sharp jawline, calm confident eyes. He wears a loose midnight-blue wax-print shirt with subtle geometric patterns, sleeves pushed to the elbows, and dark indigo trousers. He carries himself with the relaxed pride of someone who owns the night.

## SUFFIXE S3 (à recopier à l'identique)
```
vivid magenta and electric cyan neon glow, afro-futurist holographic patterns floating in the air, rain-slick street reflecting neon signs (signs blank, no letters), deep indigo night, chromatic aberration edges, glossy futuristic cinematic grading, 35mm film grain
```

## LES 5 SCÈNES (10 fonds = 5 scènes × 2 cadrages)

### s01 — « Entrée dans le club » (couplets 1, 2, intro, outro)
- 9:16 : `vertical 9:16 portrait composition, tall framing` — sujet au tiers gauche, façade de club à droite avec néons cyan/magenta.
- 16:9 : `horizontal 16:9 landscape composition, wide framing` — rue de Cotonou sous la pluie, devant l'entrée lumineuse.
- SUJET-VERS : *« Trois heures du mat', j'suis dans l'club, j'suis dans l'zone »* → silhouette pushant la porte, lumière magenta lui scie le visage, néons cyan au-dessus, reflets sur l'asphalte mouillé, intensité **modérée**.
- PLAN : medium (tête + torse, personnage de dos 3/4).

### s02 — « La foule debout » (refrains 1, 2, 3)
- 9:16 : `vertical 9:16 portrait composition, tall framing` — héros bras levés, foule autour en silhouettes lumineuses, plafond stroboscopique cyan.
- 16:9 : `horizontal 16:9 landscape composition, wide framing` — la même scène en plan large, ligne d'horizon basse, foule à mi-hauteur.
- SUJET-VERS : *« Tout l'monde est debout, personne s'assoit, c'est l'temps »* → mer de mains levées, faisceau magenta qui balaie, intensité **full neon**.
- PLAN : wide (refrains/show).

### s03 — « La basse dans le corps » (couplet 1 bas, refrain 1 bas)
- 9:16 : `vertical 9:16 portrait composition, tall framing` — close-up poitrine + main contre le haut-parleur, vibration visuelle autour des doigts.
- 16:9 : `horizontal 16:9 landscape composition, wide framing` — plan moyen sur l'ampli mural, lignes concentriques magenta.
- SUJET-VERS : *« J'sens la basse qui tape dans mon corps »* → ondes sonores visibles, peau qui vibre, halo cyan autour des phalanges, intensité **modérée→full**.
- PLAN : close-up (émotion/transition).

### s04 — « Ça redescend » (pont + queue entre refrains 2 et 3)
- 9:16 : `vertical 9:16 portrait composition, tall framing` — héros adossé au mur du club, tête renversée, souffle visible, lumière cyan seule.
- 16:9 : `horizontal 16:9 landscape composition, wide framing` — extérieur, coin de rue sous la pluie,enseigne de bar floue en arrière-plan, reflets bleus.
- SUJET-VERS : *« J'reprends mon souffle, j'regarde le temps / ça va remonter dans un instant »* → moment de pause, goutte d'eau sur le front, intensité **modérée basse** (cyan dominant).
- PLAN : medium/intime.

### s05 — « Le drop final » (refrain 3 + outro)
- 9:16 : `vertical 9:16 portrait composition, tall framing` — héros face caméra, micro à la main, explosion de magenta derrière lui, kick visuel.
- 16:9 : `horizontal 16:9 landscape composition, wide framing` — vue de scène, confettis et lumière braquée sur le public.
- SUJET-VERS : *« J'suis dans l'bâtiment, j'fais trembler l'ciment / on s'arrête jamais »* → climax, faisceau blanc qui claque, intensité **full magenta/or**.
- PLAN : wide (show) + close-up visage intercalé via Ken Burns.

## GABARIT PROMPT FINAL (à générer 10 fois — 1 par cadrage)

```
{cadrage} · {sujet-vers selon scène} · {bloc héros} · {plan} · {suffixe S3} · {zone:
  vers → darker, less busy lower third with soft bokeh for lyric text readability
 | intro/covers 9:16 → large dark negative space across the top quarter
 | covers 16:9 → left third} · no text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, no signage · full figure, head and hands completely in frame, no cropped face, no out-of-frame elements, all fingers visible
```

## Post-production
- Texte des vers : `Barlow Condensed Bold` (npm `@fontsource/barlow-condensed` → woff2 → brotli → ttf dans `assets/fonts/`).
- Badge `Dsky` + pictogramme Bénin vectoriel, **discret, fondu 0,4 s PAR VERS** (v5.5 §0.2 et §4), jamais permanent.
- Bandeau Bénin 54 px plein bas (v5.5 §5) — **UNIQUEMENT en cover 9:16** et sur le **bandeau bas de l'endcard**. PAS dans les scènes vidéo (les Instructions A interdisent le drapeau du Bénin en bas des vidéos).
- Endcard sombre épuré, **sans contact ni email ni téléphone** (Instructions A point 4). Titre cursive + « Merci d'avoir regardé » + code chiffres à retenir (voir BRIEF.md).
