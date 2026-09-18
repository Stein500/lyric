# 📸 RAPPORT DE PRODUCTION — SALVE 1 (DOSSIER SAMUEL)

**Date :** 2026-09-18  
**Projet :** Retouche photographique professionnelle DSLR & relooking haut de gamme  
**Dossier source :** `Samuel/` (8 photos originales)  
**Dossier sortie :** `Samuel/salve1/` et `livrables/Samuel/`  
**Archive ZIP :** `livrables/salve1_samuel.zip` et `Samuel/salve1/salve1_samuel.zip`  

---

## 🎯 Conformité aux 7 indications de l'artiste (`Indications.txt`) & directives

Chaque image a été générée en utilisant l'image originale correspondante comme ancrage strict (`images: ['Samuel/...']`) pour garantir la fidélité absolue à l'identité réelle de Samuel.

1. **Amélioration look DSLR :**  
   Rendu optique professionnel digne d'un reflex plein format avec objectifs à grande ouverture (85mm f/1.4 et 50mm f/1.4). Profondeur de champ naturelle, flou bokeh doux et progressif, séparation nette du sujet, dynamique étendue.
2. **Éclairage professionnel :**  
   Correction des ombres dures, des reflets et des zones surexposées d'origine. Éclairage doux de studio (key light diffuse, rim light dorée de contour) qui sculpte les volumes du visage de façon naturelle.
3. **Étalonnage couleur premium :**  
   Équilibre tonal soigné, tons de peau africains chauds, riches et authentiques, sans dérive chromatique, sans filtre criard ni saturation excessive.
4. **Retouche de peau naturelle :**  
   Respect scrupuleux de la carnation, préservation absolue du grain de peau et des micro-pores visibles. Aucun lissage plastique artificiel (« peau de cire IA »), zéro déformation du visage, respect de l'âge réel.
5. **Nettoyage et changement complet de l'arrière-plan :**  
   Suppression intégrale de tous les éléments perturbateurs d'origine (tôles ondulées, poutres en bois brut, tableau noir avec craie, fanions de fête verts, linge suspendu, sols encombrés). Remplacement par des décors architecturaux luxueux, modernes et contemporains (lounges d'hôtels, rooftop urbain au crépuscule, verrière géométrique, galeries d'art, studio ambré).
6. **Look cinématographique subtil :**  
   Atmosphère élégante et soignée, contraste naturel, rendu immersif haut de gamme.
7. **Retouche professionnelle finale & relooking :**  
   - **Changement complet des vêtements :** Remplacement des tuniques traditionnelles rayées et vêtements décontractés par des tenues modernes et sophistiquées adaptées à chaque pose.
   - **Suppression intégrale des cœurs et artéfacts :** Éradication complète et propre de tous les émojis cœurs (❤️💚💙) et stickers Snapchat.
   - **Fidélité des accessoires :** Port ou absence de lunettes strictement conforme à chaque photo originale.

---

## 📋 Tableau récapitulatif des 8 images de la Salve 1

| N° | Fichier original | Fichier DSLR généré | Relooking tenue | Nouveau décor | Détails clés & fidélité |
|---|---|---|---|---|---|
| 1 | `Snapchat-1058718015.jpg` | `Snapchat-1058718015_DSLR.jpg` | Blazer bleu nuit sur mesure + t-shirt noir épuré | Lounge architectural d'hôtel contemporain | Sans lunettes (conforme original), regard face, lumière douce |
| 2 | `Snapchat-1240900071.jpg` | `Snapchat-1240900071_DSLR.jpg` | Bomber texturé gris anthracite + t-shirt blanc | Intérieur design minimaliste, parquet foncé | Vue plongeante vers le bas, lunettes, zéro cœur |
| 3 | `Snapchat-1725744679.jpg` | `Snapchat-1725744679_DSLR.jpg` | Col roulé noir en maille fine + blazer charbon | Studio photo texturé bronze avec rim light dorée | Profil 3/4 gauche, lunettes, zéro tôle ondulée |
| 4 | `Snapchat-2000062992.jpg` | `Snapchat-2000062992_DSLR.jpg` | Chemise blanche col ouvert + gilet de costume | Atrium moderne sous une verrière géométrique | Contre-plongée vers le haut, lunettes, lumière zénithale |
| 5 | `Snapchat-2138729779.jpg` | `Snapchat-2138729779_DSLR.jpg` | Pardessus en laine noire + pull col rond texturé | Rooftop terrasse au crépuscule, bokeh urbain | Vue frontale légère contre-plongée, lunettes, regard sérieux |
| 6 | `Snapchat-354156549.jpg` | `Snapchat-354156549_DSLR.jpg` | Veste en suède camel + t-shirt blanc épuré | Salon d'art contemporain aux tons chauds et sculptures | Tête inclinée, lunettes, zéro cœur, zéro linge suspendu |
| 7 | `Snapchat-374649989.jpg` | `Snapchat-374649989_DSLR.jpg` | Pull en maille côtelée bleu nuit ajusté | Façade architecturale à persiennes en bois et soleil doré | Regard vers le haut en 3/4 droit, lunettes, lumière rasante |
| 8 | `Snapchat-948631217.jpg` | `Snapchat-948631217_DSLR.jpg` | Veste de smoking en velours vert émeraude + chemise noire | Galerie intimiste de musée avec toiles classiques | Profil droit strict, sans lunettes (conforme), zéro tableau noir |

---

## 📲 Commandes Termux (Téléchargement direct dans `/storage/emulated/0/Web+/`)

### 1. Commande globale (Pack ZIP complet avec les 8 photos)
```bash
mkdir -p /storage/emulated/0/Web+; cd /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -O https://raw.githubusercontent.com/Stein500/lyric/arena/01a0b07b-lyric/livrables/salve1_samuel.zip && unzip -o salve1_samuel.zip; ls -lh /storage/emulated/0/Web+/
```

### 2. Commande combinée (Télécharge les 8 images individuelles en direct)
```bash
mkdir -p /storage/emulated/0/Web+; cd /storage/emulated/0/Web+; for img in Snapchat-1058718015_DSLR.jpg Snapchat-1240900071_DSLR.jpg Snapchat-1725744679_DSLR.jpg Snapchat-2000062992_DSLR.jpg Snapchat-2138729779_DSLR.jpg Snapchat-354156549_DSLR.jpg Snapchat-374649989_DSLR.jpg Snapchat-948631217_DSLR.jpg; do curl -fL --retry 5 --retry-delay 3 -C - -O https://raw.githubusercontent.com/Stein500/lyric/arena/01a0b07b-lyric/livrables/Samuel/$img; done; ls -lh /storage/emulated/0/Web+/
```

### 3. Commandes unitaires image par image (au choix)
- **Image 1 (`Snapchat-1058718015_DSLR.jpg`) :**
```bash
mkdir -p /storage/emulated/0/Web+; cd /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -O https://raw.githubusercontent.com/Stein500/lyric/arena/01a0b07b-lyric/livrables/Samuel/Snapchat-1058718015_DSLR.jpg
```
- **Image 2 (`Snapchat-1240900071_DSLR.jpg`) :**
```bash
mkdir -p /storage/emulated/0/Web+; cd /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -O https://raw.githubusercontent.com/Stein500/lyric/arena/01a0b07b-lyric/livrables/Samuel/Snapchat-1240900071_DSLR.jpg
```
- **Image 3 (`Snapchat-1725744679_DSLR.jpg`) :**
```bash
mkdir -p /storage/emulated/0/Web+; cd /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -O https://raw.githubusercontent.com/Stein500/lyric/arena/01a0b07b-lyric/livrables/Samuel/Snapchat-1725744679_DSLR.jpg
```
- **Image 4 (`Snapchat-2000062992_DSLR.jpg`) :**
```bash
mkdir -p /storage/emulated/0/Web+; cd /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -O https://raw.githubusercontent.com/Stein500/lyric/arena/01a0b07b-lyric/livrables/Samuel/Snapchat-2000062992_DSLR.jpg
```
- **Image 5 (`Snapchat-2138729779_DSLR.jpg`) :**
```bash
mkdir -p /storage/emulated/0/Web+; cd /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -O https://raw.githubusercontent.com/Stein500/lyric/arena/01a0b07b-lyric/livrables/Samuel/Snapchat-2138729779_DSLR.jpg
```
- **Image 6 (`Snapchat-354156549_DSLR.jpg`) :**
```bash
mkdir -p /storage/emulated/0/Web+; cd /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -O https://raw.githubusercontent.com/Stein500/lyric/arena/01a0b07b-lyric/livrables/Samuel/Snapchat-354156549_DSLR.jpg
```
- **Image 7 (`Snapchat-374649989_DSLR.jpg`) :**
```bash
mkdir -p /storage/emulated/0/Web+; cd /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -O https://raw.githubusercontent.com/Stein500/lyric/arena/01a0b07b-lyric/livrables/Samuel/Snapchat-374649989_DSLR.jpg
```
- **Image 8 (`Snapchat-948631217_DSLR.jpg`) :**
```bash
mkdir -p /storage/emulated/0/Web+; cd /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -O https://raw.githubusercontent.com/Stein500/lyric/arena/01a0b07b-lyric/livrables/Samuel/Snapchat-948631217_DSLR.jpg
```
