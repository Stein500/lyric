# 🎬 Drague moi — Daïsky Prod / TechStein · État d'avancement

**Morceau :** Drague moi · **Durée :** 03:00.0 · 48 kHz source
**Charte :** Hybride — B (anime sombre/éclairs cyan-ambre) couplets+refrains · A (coucher de soleil chaud) pont (seg 36–43)
**Héro :** femme anime (cel-shaded), box-braids, courbes généreuses, tenues très variées (robes, traditionnelles ankara, maillots/bikini, lingerie/bralette, slip…), poses variées (debout, assise, à genoux, allongée…)

## ✅ Étape 1 — Images & covers (terminée)
- 2 images d'ancrage (charte B + A) validées par l'artiste.
- **50 images 9:16** (s01–s50) générées par salves validées (1 à 5), décors + tenues variés, collées au sens des vers.
- Covers : `cover_Drague_moi_9x16.jpg` (1080×1920) + `cover_Drague_moi_carre.jpg` (1080×1080 pour le MP3), titre incrusté PIL (serif fallback, pas de texte IA).
- Source images converties en JPEG (work/raw_png_backup = PNG de travail, non versionné).

## ✅ Étape 2 — MP3 master (terminé)
- Mastering : highpass 30 / lowpass 18000 / loudnorm **I=-14,1 LUFS · TP≈-1,2 dB** (mesuré).
- Export libmp3lame **320 k, 48 kHz, stéréo, 03:00** → `livrables/Drague_moi_DAISKY.mp3`.
- Tags ID3v2.4 complets (titre, artiste, label, contacts, emails, paroles USLT, **cover carrée APIC**).

## ✅ Étape 2 — Vidéo 9:16 (terminée) — SOLUTION A v4.7
- Minutage artiste révisé : premier vers 00:05.46, dernier 02:46.33, outro → 03:00.
- **SOLUTION A (v4.7 §0/§9) : flux continu frame-accurate** — UN SEUL flux de 5400 frames (180 s × 30 fps), t=i/30 exact, vers affectés par temps (pas de concat/clips séparés → 0 dérive).
- Rendu Python (image2pipe mjpeg → libx264) : Ken Burns continu (zoom in/out + pan sinusoïdal, zéro image figée), sous-titres **féminins non-cursifs** dessinés par trame (fade in 0,12 s / out 0,18 s), **sans badge, sans effet vague**, avance 0,03 s.
- Muxage audio master + fondu final 3 s (pas de fade-in vidéo).
- **Vérifs auto : durée 180,00 s ✓ · blackdetect 0 (hors fondu final) ✓ · freezedetect 0 ✓ · timing texte vérifié (apparition à 5,46 s) ✓**
- Livrable : `livrables/Drague_moi_9x16_final.mp4` (1080×1920, ~62 Mo).

## 📋 Reste à faire / options
- [ ] 16:9 YouTube si demandé
- [ ] Endcard/contacts écran de fin si demandé
- [ ] Version allégée du 9:16 (< 50 Mo) pour partage facile si besoin
- [ ] Push + commandes curl `-C -` avec hash de commit

**Signature :** « Wolof TechStein beat wê ! » ⚡
