# PROMPT UNIVERSEL DE PRODUCTION LYRICS — v5.8 « TYPO PEINTE »

Mise à jour : **2026-10-10**. Ajouté à v5.7 « Mariage parfait », qu'il **complète sans le contredire**.
Expérimenté et validé sur la production `productions/mahu-ti-te-gbe/` (31 plans, 49 vers, 20 images).
Il **remplace** v5.7 §2 et §6 sur le seul point du texte : la typographie n'est plus incrustée en post-production,
elle est **peinte par le modèle dans l'image**. Les paramètres d'une chanson ne se reportent jamais sur une autre.

## 0 — Priorité (inchangée, rappel)

1. Demande explicite actuelle de l'artiste. 2. Configuration validée de la production (ancre, personnages, titre exact).
3. v5.8 (ce document) pour la typo et les icônes. 4. v5.7, puis v5.6, puis v5.5.
États « proposé / généré / validé par l'artiste / rendu / contrôlé » distincts. **Jamais** d'invention de validation,
de fichier final, de hash publié ou de mesure.

## 1 — Ce que change v5.8 (et pourquoi)

| Sujet | v5.7 | **v5.8** |
|---|---|---|
| Paroles à l'écran | calque PIL/Pillow centré, mot actif or, vague d'eau | **texte peint par le modèle dans la matière** (capitales d'or serif condensée, mot actif en or vif, suite crème). Le calque PIL devient un **plan B** uniquement si l'orthographe du modèle est faute |
| Icônes, stickers | interdits dans l'œuvre (zone UI propre) | **autorisés et voulus** : 1 à 3 par image, dorés, touchés par la lumière de la scène, collés au sens du mot (lanterne = lumière, colombe = souffle, main = porter) |
| Rythme des plans | 1 plan par bloc de 2-3 vers | **1 plan par vers** quand le budget le permet (49 vers = 49 plans, ou 19 blocs + 12 plans de vers isolés) ; les reprises réutilisent le plan du même vers |
| Zones sûres | règle pour le calque | **règle écrite dans le prompt de génération** (voir §3) |
| Cartes accueil/finale | inchangées | incrustation PIL autorisée (elles ne sont pas chantées) + **Montserrat obligatoire** (ExtraBold/SemiBold), jamais DejaVu |

## 2 — Orthographe : la règle qui évite le piège

Le modèle écrit juste mais **vérifier image par image** reste obligatoire :
- recopier le vers **exact** dans le prompt, entre guillemets, avec la consigne « écrit exactement et sans faute » ;
- exiger les diacritiques (`TÈ`, `GBÈ`, `WÊ`) et nommer la langue du vers si elle est mixte (fon + anglais) ;
- lire le résultat **sur une contact sheet à ≥ 480 px de large**, sinon les fautes passent inaperçues ;
- une image fautée = régénérée, **jamais corrigée au pinceau numerico** sur la bitmap ;
- si un plan échoue (réponse sans image) : le consigner comme échec, ne pas le compter comme livré.

## 3 — Zones sûres appliquées au prompt de génération (1080×1920)

- aucun texte dans les **140 premiers pixels** en haut (marge de sécurité sur la borne 144) ;
- aucun texte dans les **340 derniers pixels** en bas ;
- aucun texte à droite de `x ≥ 910` entre `y 960` et `1690` (zone bouton/pavé de TikTok) ;
- bloc de texte centré, largeur ≤ 740 px, dans la bande `y 620 → 1340` ;
- la typo ne doit **jamais couvrir un visage** : si elle touche la bouche, le plan est limité à ≤ 3 s au montage ou régénéré ;
- la **tête n'est jamais rognée** : pour passer de 768×1376 (sortie native) à 1080×1920, on ancre en **haut** et on
  rogne le bas, jamais l'inverse.

## 4 — Recettes de style validées (au choix, une par chanson)

- **ENCRE & FEUILLE D'OR** (validée sur « Mahu ti tè gbè ») : peinture numérique matière épaisse, clair-obscur
  Rembrandt à source unique, pluie/vapeur, grain 35 mm, filets d'or sur tout ce qui est divin, palette bleu nuit
  `#0B1B2A` / teal / ambre `#E8A33D` / or `#D9A441` / crème `#F3E7D3`. Convient aux textes de foi, d'endurance, de deuil.
- **AUBE CLOCHETTES** (v5.6, conservée) : fonds clairs, CTA premium, pour les punchlines motivées courtes.
- **STUDIO ANIME SEINEN** (validée sur « Gbètché vivi ») : cel-shading dur, contours épais, pour le storytelling rue/adrénaline.
Une seule recette par chanson, recopiée mot pour mot dans chaque prompt, avec le bloc personnage mot pour mot.

## 5 — Continuité entre plans (la demande « on dirait que ça bouge »)

- même lieu, même heure, même intensité de pluie : l'arc avance par paliers (nuit → crachin → brume → aube).
- le plan `n+1` reprend la **position** du personnage dans le plan `n` (même bord du cadre, même appui au sol).
- un motif récurrent traverse les plans (ici : le fil de lumière dorée, la colombe, la pastille `0326`).
- léger motion blur **uniquement** sur les plans d'action (chute, cri, tirage) ; jamais sur les gros plans de visage.

## 6 — Audio (rappel v5.7, avec les ajouts mesurés)

- durée **décodée** uniquement (`ffmpeg -map 0:a:0 -f null -`) ; la durée annoncée du fichier peut mentir de 0,4 s.
- mesurer la crête **avant** de promettre un master : ici `+0,06 dBTP` source = écrêtage, corrigé par `TP=-1.5` en
  loudnorm 2 passes ; vérifier après coup (`ebur128` = −14,0 LUFS, astats peak = −1,24 dB).
- `silencedetect` peut ne rien trouver sur un morceau continu : dans ce cas les fenêtres de clochettes se calculent
  sur les **chronomètres des paroles** (ici 9 fenêtres ≥ 5 s), pas sur le silence.
- master : chanson seule, 48 kHz, 320 kb/s, `-vn` obligatoire pour tuer la pochette héritée de l'outil de génération,
  puis ID3 `TIT2/TPE1/TALB/TPE2` + `APIC` 1080 + `USLT` propre (sans horodatages) + `TXXX` SIGNATURE/MASTER/IA.

## 7 — Git et livraison (inchangés)

Commit + push après chaque étape, **sur la branche de la session uniquement**, jamais de `reset --hard` automatique.
Livraison toujours = fichier 9:16 · Titre · Captions · Hashtags · déclaration IA · commandes Termux une ligne par
fichier séparées par `;`, sur le hash du commit **après** push.

## 8 — Ce qui est annulé explicitement

Les points 11, 12 et 13 de `Instructions A.txt` (personnage féminin nu/anatomie exhibée, caméra sur les parties du
corps, vérification de l'érection) sont **annulés** par v5.7 §2 et le restent dans v5.8 : tenues fermées et élégantes,
cadrages gros plan visage / plan moyen / plan large, tout passe par le visage et l'attitude. Aucune photo personnelle
envoyée au générateur sans autorisation écrite.

## 9 — Historique

- **v5.8** (2026-10-10) — « Typo peinte » : texte et icônes peints par le modèle, zones sûres écrites dans le prompt,
  1 plan par vers, `−vn` + ID3 complet, `silencedetect` en secours, contact sheet de contrôle orthographique.
- **v5.7** (2026-10-10) — « Mariage parfait » : fusion v5.5 + v5.6, badge sans drapeau, carte d'accueil et carte finale
  sans contacts, code de fin, clochettes premium, personnages habillés, livraison Titre + Captions + Hashtags.
- **v5.6** (2026-10-05) — clochettes CTA, style S6 Aube Sacrée, mot sacré en post-production.
- **v5.5** (2026-09-30) — hybride, commande, paroles centrées, safe zones, Termux une ligne.

**Signature :** « Wolof TechStein beat wê ! » ⚡
