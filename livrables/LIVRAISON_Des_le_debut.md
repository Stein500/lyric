# LIVRAISON — « Dès le début » (Daïsky)

**Production lyrics complète** · style **S6 « Aube Sacrée »** · prompt appliqué : **v5.6 « Aube & Clochettes »**
(remplacera la v5.5 ; hérite de tout le référentiel v5.3/§G/§H).

---

## 1. Fichiers livrés (`livrables/`)

| Fichier | Contenu | Contrôles |
|---|---|---|
| `Des_le_debut_9x16.mp4` | clip vertical 1080×1920, 30 fps, H.264 BT.709, AAC 192 kb/s | durée = cold-open 6,85 s + chanson 199,99 s + 5 s de fin ; aucune frame noire hors fondu final ; aucun gel |
| `Des_le_debut_master_320k.mp3` | chanson seule, 199,99 s, 48 kHz, **320 kb/s** | ID3v2.4 : TIT2 / TPE1 / TALB / TDRC / TCON + **APIC 1080×1080** + **USLT** + contacts (email, WhatsApp) |
| `cover_des_le_debut_1080x1080.jpg` | cover carrée (APIC des plateformes) | titre exact, artiste, badge, drapeau, contacts |
| `cover_des_le_debut_9x16.jpg` | cover story / statut | idem |
| `cover_des_le_debut_16x9.jpg` | cover YouTube | idem, composition à gauche |
| `PROMPT_UNIVERSEL_v5.6_AUBE_CLOCHETTES.md` | référentiel à jour | règle CTA clochettes, style S6, leçons |
| `TERMUX_Des_le_debut.md` | commandes de téléchargement | une ligne par fichier, hash du commit de livraison |

## 2. Clochettes CTA — la règle que tu as demandée

Déclenchement automatique dans **chaque fenêtre de plus de 5 s sans parole affichée** :

| # | Fenêtre | Durée | Contexte |
|---|---|---|---|
| 1 | 0:00,0 → 0:05,7 | 5,7 s | intro instrumentale |
| 2 | 0:22,6 → 0:29,0 | 6,5 s | après « Jésus, Christ Sauveur, Roi des rois » |
| 3 | 1:45,9 → 1:56,5 | 10,7 s | après « Jésus… Christ… Sauveur… » |
| 4 | 2:10,7 → 2:31,8 | **21,1 s** | pont instrumental |
| 5 | 2:49,2 → 3:20,0 | **30,8 s** | queue finale + endcard |

Animation : cloche **vectorielle** (aucune emoji système) qui **oscille ±12°** avec halo pulsé, **2 anneaux d'onde**,
**3 étincelles**, flèche clignotante ; textes **UI** `ABONNE-TOI` et **`PARTAGE`** (pastille à contour cyan pulsé,
action prioritaire) + rappel « Clique sur la cloche — puis PARTAGE ».
Dans les fenêtres longues, la séquence **se répète toutes les 4 s** (jamais une icône figée pendant 21 s).
Entrée/sortie en **fondu 0,35 s**.

## 3. Paroles (mode mixte, validé)

- **Pendant les vers** : centrées H/2, police **Barlow Condensed Bold** (505 glyphes — tous les accents des paroles vérifiés),
  mot actif **or**, mots passés **crème**, **vague d'eau** continue (amplitude 4,5 px, 0,9 Hz), largeur sûre ≤ 720 px.
- **Pendant les clochettes** : le texte s'efface en 0,35 s et **revient exactement à la même position**.
- Badge **`Dsky` + drapeau Bénin vectoriel** en fondu 0,4 s **à chaque vers**, opacité ≤ 75 %, y = 150.
- **Safe zones respectées** : rien dans la bande haute (y 0–144), le rail droit (x ≥ 910 ∧ y 960–1690) ni la bande basse (y ≥ 1574).
- Bandeau Bénin **54 px** en pied de cadre (30 px en paysage), couleurs `#008751 / #FCD116 / #E8112D`.

## 4. Images

- **40 fonds** = 20 scènes × 2 formats, tous vérifiés : aucune lettre, aucun logo, aucun filigrane,
  aucun tatouage portant un mot (symboles uniquement), plein cadre (aucune bande noire),
  personnages entiers (visages, mains et pieds dans le cadre).
- Héros **inventés** (un homme et une femme, humbles, jamais embellis) ; **aucune photo personnelle** n'a été envoyée à l'IA.
- Mouvement : **Ken Burns 1,02→1,08 + panoramique sinusoïdal + respiration** (vague d'eau) → l'illusion du mouvement continu.
- **Arc lumineux** : aube `dim` → couplets `modérée` → refrains `full` → ponts `or` → outro `décroissant` → endcard `sombre épuré`.

## 5. Resynchronisation honnête

Les **51 départs de vers proviennent de ton fichier de paroles** ; l'audit automatique les a comparés aux pics d'énergie
de l'audio (`timings_audited.json`) : écart moyen ≈ 171 ms, **intervalle minimal 1,29 s** (règle ≥ 1,2 s respectée),
**44 vers conservés** tels quels. Aucun départ n'a été déplacé automatiquement : un pic spectral est un indice
musical, pas une preuve d'attaque vocale. **La synchronisation vocale fine reste à confirmer à l'écoute.**

## 6. Tags du master

```
TIT2 = Dès le début        TPE1 = Daïsky           TALB = Dès le début
TDRC = 2026                TCON = Gospel / Louange
APIC = cover 1080×1080     USLT = paroles complètes
TXXX email   = daiskyproduction@gmail.com
TXXX contact = WhatsApp +229 01 61 16 24 08 / +229 01 49 11 49 51
```

## 7. Reste à faire (sur ta demande)

- **Clip 16:9 (YouTube)** : pipeline prêt (`--format 16x9`), à lancer.
- **Mot « Jésus » en post-production** sur le tatouage (avant-bras droit + poitrine) — incrustation à valider.
- **Retouche des photos de `Samuel/`** (7 prompts : DSLR, lumière, color grading, peau, fond, cinéma, finition) — chantier séparé,
  jamais lancé sans ton accord (10 images max par salve).
