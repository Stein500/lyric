# 🎨 ANCRES & SALVE — « Ça monte, ça descend » (Daïsky)

> **Mode d'emploi.** Aucune API d'images n'est disponible dans la sandbox actuelle (accès sortant limité à GitHub/npm/PyPI). Les 10 prompts ci-dessous sont **prêts à coller** dans ton provider habituel (Midjourney / DALL·E / SDXL / Flux / etc.) pour générer les 10 fonds.
>
> **Format de prompt** : identique au gabarit v5.5 §E.1 (7 blocs dans l'ordre : cadrage · sujet-vers · héros · plan · suffixe S3 · zone · interdits).

---

## 🟣 ÉTAPE 1 — Ancre s01 9:16 (à valider AVANT la salve)

**Cette image est la référence.** Si tu la valides, je génère les 4 autres scènes 9:16 puis les 5 paysages 16:9 dans la foulée. Toute l'identité du héros (vêtements, teint, coupe) sera recopiée à l'identique dans les 9 autres prompts.

### Prompt ancre s01 9:16
```
vertical 9:16 portrait composition, tall framing · A young Wolof man, 26, lean and athletic but not muscular, medium-dark skin with warm undertones, short fade haircut with subtle blonde tips, light stubble beard, sharp jawline, calm confident eyes, pushing open the heavy door of a Cotonou nightclub at 3 a.m., magenta neon light slicing across his face, cyan neon sign glowing above the door, rain-slick street reflecting the lights, his silhouette is half inside half outside, the air feels electric and welcoming · He wears a loose midnight-blue wax-print shirt with subtle geometric patterns, sleeves pushed to the elbows, and dark indigo trousers. He carries himself with the relaxed pride of someone who owns the night. · medium (head and torso, three-quarter back view) · vivid magenta and electric cyan neon glow, afro-futurist holographic patterns floating in the air, rain-slick street reflecting neon signs (signs blank, no letters), deep indigo night, chromatic aberration edges, glossy futuristic cinematic grading, 35mm film grain · darker, less busy lower third with soft bokeh for lyric text readability · no text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, no signage · full figure, head and hands completely in frame, no cropped face, no out-of-frame elements, all fingers visible
```

**Taille à demander :** 768 × 1376 (format portrait, recadré ensuite en 1080 × 1920 au compositing).
**Sortie attendue :** `assets/raw/portrait/s01_entree_club.png`.

### ✅ Critères de validation
- [ ] Héros **fidèle au bloc** (teint, coupe, barbe, vêtements wax-print bleu nuit).
- [ ] **Ambiance S3** : magenta + cyan + reflets asphalte mouillé + nuit indigo.
- [ ] **Aucun texte** nulle part (les IA en collent parfois : régénère si oui).
- [ ] **Visage complet, mains entières**, pas de coupe.
- [ ] Cadrage 9:16 utilisable en bas de frame pour les paroles (zone y 1100–1570 peu chargée).

---

## 🟢 ÉTAPE 2 — Salve 9:16 (4 images, après validation de l'ancre)

> Une fois l'ancre validée, je génère les 4 autres scènes portrait avec exactement le **même bloc héros** recopié à l'identique.

### s02 9:16 — « La foule debout » (refrains)
```
vertical 9:16 portrait composition, tall framing · Wolof TechStein hero at the center of a Cotonou dancefloor, arms raised triumphantly, the crowd as glowing silhouettes around him, magenta and cyan strobes sweeping across the ceiling, hands and phones lifted in the air · He wears a loose midnight-blue wax-print shirt with subtle geometric patterns, sleeves pushed to the elbows, and dark indigo trousers. He carries himself with the relaxed pride of someone who owns the night. · wide (refrains/show) · vivid magenta and electric cyan neon glow, afro-futurist holographic patterns floating in the air, rain-slick street reflecting neon signs (signs blank, no letters), deep indigo night, chromatic aberration edges, glossy futuristic cinematic grading, 35mm film grain · darker, less busy lower third with soft bokeh for lyric text readability · no text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, no signage · full figure, head and hands completely in frame, no cropped face, no out-of-frame elements, all fingers visible
```

### s03 9:16 — « La basse dans le corps » (close-up)
```
vertical 9:16 portrait composition, tall framing · Close-up of the hero's chest and hand pressed against a huge club speaker, sound waves visible as concentric magenta rings radiating from his fingers, cyan halo around his knuckles, his shirt vibrating with the bass · He wears a loose midnight-blue wax-print shirt with subtle geometric patterns, sleeves pushed to the elbows, and dark indigo trousers. He carries himself with the relaxed pride of someone who owns the night. · close-up (emotion/transition) · vivid magenta and electric cyan neon glow, afro-futurist holographic patterns floating in the air, rain-slick street reflecting neon signs (signs blank, no letters), deep indigo night, chromatic aberration edges, glossy futuristic cinematic grading, 35mm film grain · darker, less busy lower third with soft bokeh for lyric text readability · no text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, no signage · full figure, head and hands completely in frame, no cropped face, no out-of-frame elements, all fingers visible
```

### s04 9:16 — « Ça redescend » (pont cyan)
```
vertical 9:16 portrait composition, tall framing · Wolof TechStein hero leaning against the outside wall of the club, head tilted back, catching his breath after a track, a single drop of sweat on his forehead lit by a lone cyan streetlight, the club door glowing magenta behind him, the rain has just stopped · He wears a loose midnight-blue wax-print shirt with subtle geometric patterns, sleeves pushed to the elbows, and dark indigo trousers. He carries himself with the relaxed pride of someone who owns the night. · medium/intimate · vivid magenta and electric cyan neon glow, afro-futurist holographic patterns floating in the air, rain-slick street reflecting neon signs (signs blank, no letters), deep indigo night, chromatic aberration edges, glossy futuristic cinematic grading, 35mm film grain · darker, less busy lower third with soft bokeh for lyric text readability · no text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, no signage · full figure, head and hands completely in frame, no cropped face, no out-of-frame elements, all fingers visible
```

### s05 9:16 — « Le drop final » (refrain 3 + outro)
```
vertical 9:16 portrait composition, tall framing · Wolof TechStein hero facing the camera with a wireless mic in his right hand, an explosion of magenta and gold confetti behind him, a white beam cutting across the dancefloor, the climax of the night · He wears a loose midnight-blue wax-print shirt with subtle geometric patterns, sleeves pushed to the elbows, and dark indigo trousers. He carries himself with the relaxed pride of someone who owns the night. · wide (show) · vivid magenta and electric cyan neon glow, afro-futurist holographic patterns floating in the air, rain-slick street reflecting neon signs (signs blank, no letters), deep indigo night, chromatic aberration edges, glossy futuristic cinematic grading, 35mm film grain · darker, less busy lower third with soft bokeh for lyric text readability · no text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, no signage · full figure, head and hands completely in frame, no cropped face, no out-of-frame elements, all fingers visible
```

---

## 🟡 ÉTAPE 3 — Salve 16:9 (5 images, même bloc héros)

> Recadrage 1376 × 768 puis composition 1920 × 1080. **Ne change pas le bloc héros** — c'est ce qui garantit la cohérence entre les deux formats.

### s01 16:9 — « Entrée dans le club »
```
horizontal 16:9 landscape composition, wide framing · A Cotonou street at 3 a.m. seen from across the road, the hero pushing open the heavy door of a nightclub on the right, magenta neon light spilling onto the wet asphalt, cyan neon sign above the door, reflections stretching across the road · He wears a loose midnight-blue wax-print shirt with subtle geometric patterns, sleeves pushed to the elbows, and dark indigo trousers. He carries himself with the relaxed pride of someone who owns the night. · wide · vivid magenta and electric cyan neon glow, afro-futurist holographic patterns floating in the air, rain-slick street reflecting neon signs (signs blank, no letters), deep indigo night, chromatic aberration edges, glossy futuristic cinematic grading, 35mm film grain · left third · no text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, no signage · full figure, head and hands completely in frame, no cropped face, no out-of-frame elements, all fingers visible
```

### s02 16:9 — « La foule debout »
```
horizontal 16:9 landscape composition, wide framing · Wide shot of a Cotonou dancefloor, sea of raised hands glowing under magenta and cyan strobes, hero on the small stage at center, low horizon line, crowd fills the midground · He wears a loose midnight-blue wax-print shirt with subtle geometric patterns, sleeves pushed to the elbows, and dark indigo trousers. He carries himself with the relaxed pride of someone who owns the night. · wide · vivid magenta and electric cyan neon glow, afro-futurist holographic patterns floating in the air, rain-slick street reflecting neon signs (signs blank, no letters), deep indigo night, chromatic aberration edges, glossy futuristic cinematic grading, 35mm film grain · left third · no text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, no signage · full figure, head and hands completely in frame, no cropped face, no out-of-frame elements, all fingers visible
```

### s03 16:9 — « La basse dans le corps »
```
horizontal 16:9 landscape composition, wide framing · Mid-shot of a huge wall-mounted club speaker vibrating with bass, hero's hand pressed flat against the cone, concentric magenta rings radiating from his palm, cyan halo around his wrist, his wax-print shirt caught mid-flutter · He wears a loose midnight-blue wax-print shirt with subtle geometric patterns, sleeves pushed to the elbows, and dark indigo trousers. He carries himself with the relaxed pride of someone who owns the night. · medium (close-up) · vivid magenta and electric cyan neon glow, afro-futurist holographic patterns floating in the air, rain-slick street reflecting neon signs (signs blank, no letters), deep indigo night, chromatic aberration edges, glossy futuristic cinematic grading, 35mm film grain · left third · no text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, no signage · full figure, head and hands completely in frame, no cropped face, no out-of-frame elements, all fingers visible
```

### s04 16:9 — « Ça redescend »
```
horizontal 16:9 landscape composition, wide framing · A quiet corner of a Cotonou street after the rain, hero leaning against a concrete pillar, head tilted back, catching his breath, lone cyan streetlight, blurred magenta glow from the club door behind him · He wears a loose midnight-blue wax-print shirt with subtle geometric patterns, sleeves pushed to the elbows, and dark indigo trousers. He carries himself with the relaxed pride of someone who owns the night. · medium · vivid magenta and electric cyan neon glow, afro-futurist holographic patterns floating in the air, rain-slick street reflecting neon signs (signs blank, no letters), deep indigo night, chromatic aberration edges, glossy futuristic cinematic grading, 35mm film grain · left third · no text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, no signage · full figure, head and hands completely in frame, no cropped face, no out-of-frame elements, all fingers visible
```

### s05 16:9 — « Le drop final »
```
horizontal 16:9 landscape composition, wide framing · Stage view from the crowd, hero in the center with a wireless mic, explosion of magenta and gold confetti behind him, white beam cutting across the dancefloor, the climax of the night · He wears a loose midnight-blue wax-print shirt with subtle geometric patterns, sleeves pushed to the elbows, and dark indigo trousers. He carries himself with the relaxed pride of someone who owns the night. · wide · vivid magenta and electric cyan neon glow, afro-futurist holographic patterns floating in the air, rain-slick street reflecting neon signs (signs blank, no letters), deep indigo night, chromatic aberration edges, glossy futuristic cinematic grading, 35mm film grain · left third · no text, no letters, no numbers, no logos, no watermark, no subtitles, no borders, no signage · full figure, head and hands completely in frame, no cropped face, no out-of-frame elements, all fingers visible
```

---

## 📁 Nommage (à respecter, v5.3 §F)

| Format | Chemin |
|---|---|
| Portrait | `assets/raw/portrait/s{01..05}_{motclé}.png` |
| Paysage | `assets/raw/landscape/s{01..05}_{motclé}.png` |

Tailles cibles : 768 × 1376 (portrait) et 1376 × 768 (paysage) ; recadrés en 1080 × 1920 / 1920 × 1080 au compositing.
