# 🎬 PROMPT UNIVERSEL DE PRODUCTION LYRICS — v5.6 « AUBE & CLOCHETTES »

Mise à jour : **2026-10-05**. Ce document **hérite de v5.5** (`PROMPT_UNIVERSEL_v5.5_HYBRIDE_COMMANDE.md`) et
**le remplace** là où il y a conflit. Les paramètres d'une chanson ne se reportent **jamais** automatiquement sur une autre.

## 0 — Nouveautés de la v5.6 (décisions et leçons de « Dès le début »)

1. **Règle CTA « clochettes » (nouvelle, prioritaire)** — §9.
2. **Style S6 « Aube Sacrée »** ajouté aux styles canoniques (§G de la v5.5) — §10.
3. **Paroles en mode mixte** : centrées pendant les vers, **effacées pendant les clochettes** — §9.4.
4. **Tatouage texte = post-production** : un mot (ex. « Jésus ») n'est **jamais** demandé au générateur — §10.4.
5. **Fenêtre CTA calculée sur le temps réellement sans texte** (durée d'affichage des vers), pas sur l'écart entre départs — §9.2.
6. **Rendu segmenté et reprenable** : un rendu long ne se commite **jamais** avant `moov atom` valide — §11.5.

Priorité d'application : demande explicite de l'artiste → configuration validée → règles universelles v5.6 → v5.5 → archive v5.3.

---

## 9 — CLOCHETTES CTA : s'abonner et surtout PARTAGER

**Paramètres :** `CTA_MODE`, `CTA_SEUIL_S` (défaut **5,0**), `CTA_SEQUENCE_S` (défaut **3,0**), `CTA_REPETITION_S` (défaut **4,0**).

### 9.1 Déclenchement
- Toute **fenêtre sans parole affichée ≥ CTA_SEUIL_S** reçoit l'animation clochettes.
- « Sans parole » = **aucun glyphe de vers à l'écran**, donc : fin du dernier vers (départ + durée d'affichage)
  jusqu'au départ du vers suivant. Ne pas confondre avec un silence audio : un beat peut tourner sans voix.

### 9.2 Fenêtres : calcul honnête
- Calculer par programme : `fenêtre = [fin_affichage(vers i) ; départ(vers i+1)]`, garder `≥ 5 s`.
- La **queue instrumentale finale** (après la fin d'affichage du dernier vers) est une fenêtre CTA à part entière.
- L'**intro** avant le premier vers en est une aussi.
- Conserver la liste des fenêtres dans `timings_audited.json` (`fenetres_cta_5s`) — ce sont des données mesurées.

### 9.3 Animation (vectorielle, jamais une emoji système)
- Cloche **dessinée en vectoriel** (Pillow/SVG) : corps bombé, anse, battant, liseré clair, **halo lumineux**.
- **Balancement** ±12° avec amortissement exponentiel, période **1,2 s** ; **pulsation** douce **0,8 s**.
- **2 anneaux d'onde** concentriques (0,9 s), **3 étincelles** scintillantes, **flèche clignotante** vers la cloche.
- Textes **UI nette** (DejaVu Sans Bold / équivalent), jamais en cursive :
  `ABONNE-TOI` + **`PARTAGE` mis en avant** (pastille à contour cyan pulsé) + rappel « Clique sur la cloche — puis PARTAGE ».
- **Entrée/sortie en fondu 0,35 s** (cloche comprise), **pas d'icône figée**.
- Dans une fenêtre longue, **répéter la séquence toutes les 4 s** (fenêtre 25 s ≈ 6 passages), jamais une image statique.

### 9.4 Paroles en mode mixte (défaut v5.6)
- Pendant un **vers** : texte **centré H/2**, mot actif or/crème, mots passés atténués, vague d'eau continue.
- Pendant une **clochettes** : le bandeau de paroles s'efface (fondu 0,35 s) → la cloche occupe le centre.
- Au retour des paroles : **exactement la même position** qu'avant (aucun saut perçu).
- Le mot final reste visible **1,2 s** après la fin de la fenêtre de vers.

### 9.5 Safe zones (inchangées, obligatoires en 9:16 1080×1920)
- Bande haute **y 0→144** interdite · rail droit **x ≥ 910 ∧ y 960→1690** interdit · bande basse **y ≥ 1574** interdite.
- La cloche et les textes CTA vivent au **centre** (y 620–1300) : ni sous la barre de recherche, ni sous la caption.

---

## 10 — STYLE S6 « AUBE SACRÉE » (6ᵉ style canonique)

Pour la **louange, la foi, l'humilité, l'espérance** — là où S1 (nuit) ne convient pas.

**Suffixe à recopier à l'identique :**
```
warm volumetric god-rays through dusty air, terracotta and ochre earth tones,
deep indigo shadows, wax-print woven textile textures catching the light,
floating dust motes, soft bloom around skin, sacred reverent atmosphere,
crushed indigo blacks with golden highlights, 35mm film grain,
moody spiritual cinematic grading
```

| | S1 Dark Lightning | **S6 Aube Sacrée** |
|---|---|---|
| Moment | nuit | **aube → matin → heure dorée** |
| Lumière | contre-jour ambre + cyan | **rayons volumétriques + poussière en suspension** |
| Palette | bleu-noir / ambre / cyan | **terre cuite, ocre, indigo, or** |
| Usage | combat, titres sombres | **louange, foi, prière, espérance** |

**Arc lumineux S6 :** `dim` (intro) → `modérée` (couplets) → `full` (refrains) → `or` (ponts/bras levés) → `décroissant` (outro) → `sombre épuré` (endcard).

### 10.4 Règle « mot sacré » (leçon importante)
- **Aucun mot, aucune lettre n'est demandé à l'IA** : les modèles produisent des glyphes déformés ou inventés.
- Les **tatouages** religieux sont générés **en symboles uniquement** (croix fine, mains jointes, cœur sacré, couronne d'épines).
- Le **mot** (ex. « Jésus ») est **incrusté en post-production** : police propre, léger suivi de la peau, fondu 0,3 s,
  contrôle à taille téléphone. Idem pour tout texte sur la peau, les murs ou les objets.

---

## 11 — Leçons de production (v5.6)

1. **Héros inventés = cohérence entre images**, pas ressemblance : recopier le **bloc héros mot pour mot** dans chaque prompt,
   préciser la tenue exacte (couleur + matière) sinon elle dérive d'une image à l'autre, et faire porter la continuité
   par l'**étalonnage** et le **Ken Burns** plutôt que par la régénération.
2. **Mouvement = illusion** : 20 images ne bougent que si (a) elles racontent **une action continue**
   (entrer → poser → s'agenouiller → se relever → bras levés), (b) la **lumière progresse** dans le même sens,
   (c) chaque fond reçoit **Ken Burns 1,02→1,08 + pan sinusoïdal + respiration** (vague d'eau) et un fondu de 0,4 s.
3. **Gros plans nécessaires** : sur 200 s, 20 plans larges ne suffisent pas → intercaler mains, visages, objets
   (mains jointes, croix au sol, reflet dans l'eau) pour porter l'émotion et couvrir les transitions.
4. **Refus des bandes noires** : certains générateurs livrent des images avec **letterbox intégré** — vérifier et régénérer
   (`full-bleed, no black bars, no borders`).
5. **Anti-corruption des livrables** : ne **jamais** committer un média encore en cours d'écriture.
   Vérifier `ffmpeg -i fichier` (présence de la durée et des flux) avant tout commit ;
   un MP4 sans `moov atom` est un **fichier mort** — le régénérer, jamais le publier.
6. **Rendu long = segments** : découper en segments reprenables, concaténer sans ré-encodage, marier l'audio à la fin.
7. **Vérifications obligatoires avant livraison** : durée = `nb_frames/FPS` ±0,05 s · aucune frame noire hors fondu final ·
   aucun gel (`freezedetect`) · texte complet, centré, hors UI · badge unique et fondu **par vers** ·
   clochettes présentes dans **toutes** les fenêtres ≥ 5 s · glyphes et visages non coupés · audio/tags/covers conformes.

---

## 12 — Couche validée : « Dès le début » (Daïsky)

Cette section est **locale à cette commande**, ce n'est pas un défaut pour les suivantes.

- **Titre exact :** `Dès le début` · **artiste :** Daïsky · `daiskyproduction@gmail.com` ·
  WhatsApp `+229 01 61 16 24 08` / `+229 01 49 11 49 51`.
- **Sources :** `Dès le début.mp3` (200,0 s décodées, 48 kHz, stéréo, pochette 360×360 intégrée),
  `Dès le début- Jésus-Christ sauveur.txt` (51 vers, 32 textes distincts, sections voix masculine/féminine dans l'USLT).
- **Style S6**, héros **inventés** (un homme et une femme, humbles, jamais embellis), **aucune photo personnelle envoyée**.
- **40 fonds** = 20 scènes × 2 formats (portrait 768×1376, paysage 1376×768, recadrés en 1080×1920 / 1920×1080).
- **Clochettes :** 5 fenêtres mesurées — `0–5,68` (intro) · `22,56–29,03` · `105,85–116,54` ·
  `130,73–151,82` (21,1 s) · queue finale ; répétition 4 s, PARTAGE prioritaire.
- **Cold-open :** coupe naturelle du refrain-titre **52,11 → 58,96 s** (6,85 s), pas de coupe au milieu d'un vers.
- **Paroles :** mode mixte, Barlow Condensed Bold (récupérée par npm `@fontsource/barlow-condensed` → woff2 → ttf,
  505 glyphes, accents couverts), mot actif or, mots passés crème, vague 4,5 px / 0,9 Hz, largeur sûre ≤ 720 px.
- **Badge :** `Dsky` + pictogramme Bénin vectoriel, fondu 0,4 s **par vers**, opacité ≤ 75 %, y=150.
- **Bandeau Bénin :** 54 px (portrait) / 30 px (paysage), `#008751 / #FCD116 / #E8112D`.
- **Master :** chanson seule, 48 kHz, MP3 320 kb/s, loudnorm 2 passes (−14 LUFS / −1,8 dBTP), ID3v2.4 + APIC + USLT.
- **Livrables :** clubs 9:16 et 16:9, master, 3 covers, prompt à jour, commandes Termux (HASH après push).

**Signature :** « Wolof TechStein beat wê ! » ⚡
