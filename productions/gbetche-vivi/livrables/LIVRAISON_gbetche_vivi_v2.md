# 📦 LIVRAISON v2 — « Gbètché vivi » (Bandit Positif) · l'outil écrit dans l'image

Version 2 demandée : **« je veux que l'outil IA écrive les choses directement sur l'image, avec des icônes et stickers »**.
Mon parti pris (je me suis écrit mon propre prompt, §A de la v5.8) : **le texte est gravé dans la matière** (marker sur
papier scotché, néon script, craie au sol, peinture stencil, étiquette bagage) **et** les autocollants/icônes sont **dessinés
par le moteur** (scotch, étoiles découpées, cadre pointillé, surligneur, souligné feutre, flèche, cloche/partage/signet/play,
étincelles). La règle v5.7 « aucune écriture sur les images » est donc **levée par toi** pour cette version ; restent
interdits : logos, drapeaux, filigranes, bandes noires.

**Commit de livraison :**  (branche , dépôt ) — les 9 fichiers ci‑dessous ont été
vérifiés présents **dans ce commit** via  (tailles identiques à celles du tableau).

## 1 · Fichiers

| Fichier | Poids | Ce que c'est |
|---|---|---|
|  | 16.28 Mo | **clip 9:16 v2** — écriture gravée dans les images (marker, néon, craie, papier scotché) + autocollants et icônes dessinés par le moteur · 1080×1920 · 30 fps · 5 995 images · 199,83 s · H.264 CRF 24 bt709 + AAC 256k/48 kHz ·  |
|  | 7.67 Mo | **master v2** — audio **identique** au master v1 · −14,0 LUFS, crête vraie −1,6 dBFS · 320 kb/s · 48 kHz · tags ID3v2.3 : TIT2, TPE1, TALB, TCON, COMM, **TYER 2026**, **APIC 1080² (v2)**, **USLT « Paroles » / fre · 2 384 car.** |
|  | 0.23 Mo | **pochette carrée 1080×1080 v2** — titre écrit au marqueur sur feuille scotchée, souligné feutre, cloche/partage/signet vectoriels, étiquette « 0314 », étoiles |
|  | 0.21 Mo | pochette v2 de rechange (plan néon « Wanyiyi ») |
|  | 0.22 Mo | pochette v2 de rechange (plan « LIBRE » à la craie) |
|  | 0.22 Mo | pochette v2 de rechange (plan accueil « REGARDE JUSQU'A LA FIN ») |
|  | 0.00 Mo | paroles horodatées (tes horodatages, jamais décalés) — la même source que l'USLT du master |
|  | 0.01 Mo | **le prompt universel à jour (v5.8)** : la règle « l'outil écrit dans l'image », zones autorisées/interdites, contrôle d'orthographe, chaîne audio, ordre APIC→USLT, contrôles fichier, format Termux |
|  | 0.03 Mo | notice de production de la chanson — §13 contrôles v1, **§15 version 2** |

## 2 · Ce que la v2 change à l'écran

- **0,0 → 5,9 s — accueil** : le whiteboard du fond porte « REGARDE JUSQU'A LA FIN » écrit au marqueur, une carte « 0314 » et
  une cloche dessinée ; le moteur ajoute un **cadre pointillé doré** autour des trois pilules et une **flèche orange** courte
  qui monte vers la rangée, plus des étincelles.
- **Vers chantés** : le mot en cours reçoit un **coup de surligneur** or, la ligne est **soulignée au feutre**, le bloc est
  **scotché** (deux bandes de masking tape) et **encadré en pointillés** ; une étiquette en bas à gauche annonce la section,
  **déduite de tes paroles** :  sur les quatre lignes qui reviennent trois fois,  sur
  « Wolof TechStein beat wê ! » (5 apparitions). Aucune étiquette ailleurs.
- **Texte gravé plan par plan** : A01 accueil (whiteboard + cartes) · A03 « MA VIE ME PLAIT » sur feuille scotchée + smiley +
  étoile · A05 « LIBRE » à la craie contre la chaîne cassée, poster à flèche rouge, néon « WOLOF » · A12 néon script
  « Wanyiyi » · A29 « NONVI » peint au mur + flèche + deux étoiles découpées · A30 « MERCI » + étiquette bagage « 0314 » +
  bandeau cloche (ce plan sert aussi de fond à la carte finale).
- **194,8 → 199,8 s — carte finale** : « 0314 » dans un **cadre pointillé scotché**, étoiles, étincelles sur les côtés.
- Fond assombri à **0,80** (0,74 en v1) et scrim plus doux : l'écriture gravée devait rester lisible sous les paroles.

## 3 · Titre


Variante courte : 

## 4 · Caption + code

> ✍️ Cette fois, **c'est écrit sur les murs** : « regarde jusqu'à la fin », « libre », « merci », et le code — **0314**.
>
> Gbètché vivi, ma vie me plaît ✊🏿 Version 2 du clip : 30 plans, les paroles surlignées au feutre, le refrain étiqueté, les
> icônes dessinées à la main. Tu sens le passage ? **Commente le code **, partage, enregistre, et mets la cloche 🔔
> avant le prochain son.
>
> Wolof TechStein beat wê ! — Bandit Positif.

## 5 · Hashtags (13)



## 6 · Déclaration IA

> **Visuels, écritures dans l'image et clip générés avec l'IA**, sous direction artistique de l'artiste (30 images portrait
> natives 1080×1920, texte gravé dans la matière, autocollants et icônes vectoriels dessinés par le moteur, montage,
> animation). **Paroles : l'artiste.** Audio : master issu du fichier fourni par l'artiste (métadonnées d'origine : beat
> généré avec Suno) — retravaillé uniquement en normalisation de volume (−14 LUFS), limitation de crête et encapsulage.
> Aucun drapeau, aucun logo de marque, aucun filigrane.

## 7 · Commandes Termux

Termux neuf d'abord :  (accepter la popup), puis
**une ligne par fichier**, collées une par une (jamais , jamais de continuation) :



Contrôle :  — clip ≈ 16,3 Mo, master ≈ 7,7 Mo. Réseau coupé ? **relancer la même ligne**
( reprend là où ça s'arrête). Shell bloqué sur  : Ctrl+C puis recoller la ligne entière.

## 8 · Contrôles chiffrés du fichier livré

- **Durée annoncée = durée décodée** : , **5 995 frames** ÷ 30 fps = 199,833 s.
- **Audit « parois du visage » rejoué sur la v2** : 30 frames testées, **0 pixel d'encre au‑dessus de y 1134** hors bandeau
  de badge ; encre de parole la plus haute = **y 1139**. L'audit a servi : la première passe v2 faisait déborder surligneur
  et scotch de ~25 px au‑dessus de la limite → tracé borné puis **re‑rendu complet**.
- **** : **aucun** passage noir.
- **Volume du clip** : **−14,1 LUFS** intégrés, **crête vraie −1,5 dBTP** (pic échantillon −1,49 dBFS) — limiteur à
  −2,05 dBFS posé **avant** l'AAC, sinon l'encodeur ressortait à +0,1 dBFS.
- **** : 2 segments ≥ 4 s (6 en v1) — les étincelles et stickers animés cassent la détection ; les fonds
  restent fixes **parce que tu as interdit le recadrage/zoom**, c'est voulu, pas un défaut.
- **Géométrie** : ratio 0,5581 sur les 36 plans (768×1376) et **aucune barre noire latérale** (mesure des colonnes de bord).
- **Orthographe gravée relue à la planche à 100 %** : « REGARDE JUSQU'A LA FIN », « MA VIE ME PLAIT », « LIBRE », « WOLOF »,
  « Wanyiyi », « NONVI », « MERCI », « 0314 ». Les accents ont sauté sous la main du générateur (« PLAÎT » → « PLAIT ») —
  accepté pour un mur peint à la main ; les paroles à l'écran, elles, gardent l'orthographe exacte de ton fichier.
- **Trois régénérations** ont été nécessaires après lecture : « VIVI » peint au sol se trouvait sous la bande de paroles
  (A03), un plan est ressorti en ratio 0,67 (A05, corrigé en 9:16 natif), le néon « Wanyiyi » passait derrière la tête
  (A12, repositionné à gauche de la silhouette).
- Preuves jointes au dépôt : , ,
  , , .

## 9 · Trois points à trancher

1. **** reste un code **posé par défaut, jamais validé par toi**. Il est écrit à trois endroits (carte d'accueil
   gravée, fond de la carte finale, cadre dessiné par le moteur) → le changer = 1 plan régénéré + 1 re‑rendu (~10 min ici).
2. **Densité d'écriture** : 6 plans sur 30 portent du texte gravé (plafond de 10 générations par tour, et l'écriture
   concurrence les paroles si on en met partout). Tu veux les 30 plans marqués ? je les traite en 3 tours.
3. **Police unicase sans jambage** (, ,  se lisent comme des majuscules sur une ligne longue) : gardée parce que
   l'accueil validé en v1 l'utilise déjà. Dis‑le moi et je bascule sur une police à jambages (re‑rendu complet).

## 10 · Le prompt à jour

 (15,6 ko) est dans ce commit : règle « l'outil écrit dans l'image » (§A), zones
autorisées/interdites, contrôle d'orthographe obligatoire sur planche, ratio imposé à chaque édition, chaîne audio (limiteur
**avant** l'encodeur, ), ordre **APIC puis USLT**, contrôles du fichier livré avec les commandes
exactes, format des commandes Termux, et la leçon de performance des calques (dessiner en sous‑boîte, cacher le statique :
200 ms → 28 ms par frame). Notice de la chanson :  (§13 v1, §15 v2).
