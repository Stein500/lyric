# Salve 08 — cover TikTok « DSKY WTBW »

## Demande et état

L’artiste demande une **cover TikTok obligatoire** dont le **seul texte visible est `DSKY WTBW`**, en majuscules : pas de `Dsky`, pas de titre ni d’autre texte sur la cover. La consigne est intégrée au prompt complet `../../PROMPT_UNIVERSEL_v6.2_COMPLET.md`. Elle concerne la cover; les métadonnées audio et le badge vidéo précédemment choisis ne sont pas modifiés implicitement.

- Une comparaison précédente a été montrée mais **aucune image n’a été sélectionnée**; elle n’est pas livrée.
- Après la précision de l’artiste : **3 générations**, dans une salve de moins de 10; **2 rejets** puis **1 cover retenue au QC agent**.
- Validation artistique de la cover : **en attente**.

| Version | Résultat | Contrôle |
|---|---|---|
| v1 | rejet | Texte exact, mais couture horizontale visible dans le ciel et texte trop large pour les marges ciblées. |
| v2 | rejet | Reprise avec référence au lettrage sérif; la couture et la largeur excessive persistent. |
| v3 | QC agent accepté | `DSKY WTBW` exact, aucune autre écriture ni signe ajouté, fond continu, personnage fidèle à l’ancre, visage dégagé; texte centré et lisible. |

La comparaison des trois essais est consignée dans `CONTROLE-cover-tiktok.jpg`. Les essais v1/v2 sont des brouillons de travail, non livrés; la planche conserve leur aspect pour le contrôle. La grille ou les légendes de contrôle ne sont pas présentes dans la cover.

## Cover livrée

- `livrables/cover-tiktok-DSKY-WTBW.jpg` — **1080 × 1920 px**, JPEG, **465 285 octets**.
- SHA-256 : `93a28092972ed92e9febe53fc01b784f5016d687eed297acf0fa58ea39ae0675`.
- Source v3 générée en **768 × 1376 px**; agrandissement LANCZOS et recadrage du bas vers 9:16. Aucune lettre n’a été retouchée ou recomposée.
- QC à pleine résolution et crop typo 1:1 : `DSKY WTBW` correctement écrit et contrasté; crop central 3:4 (1080 × 1440) également vérifié. Le cadrage effectivement utilisé par TikTok peut varier selon l’interface.
- La couverture carrée précédemment incorporée au MP3 est un autre fichier et n’a pas été modifiée; demander explicitement si l’artiste veut aussi la remplacer.

## Prompt exact de la v3

Référence jointe : `fonds/scene-01-ancre.png`, tomate approuvée par l’artiste.

```text
New portrait 9:16 TikTok cover, clean cinematic 3D illustration. Recreate the approved round red tomato character from the reference, with expressive brown eyes, little green limbs and a leafy calyx, standing in an uncluttered garden at sunrise. Keep her face fully clear. One continuous seamless background; no horizontal seams, bands, borders or patches. The ONLY text anywhere reads exactly:
DSKY WTBW
Use elegant cream serif capitals, one line, centered below the tomato. Make this text moderately sized, no more than 60% of the width, and keep it and the face within the central safe area for a 3:4 crop. D S K Y followed by one space and W T B W; each letter exact and uppercase. No title, no other spelling, no other text, letters, numbers, punctuation, typographic ornament, symbol, watermark, sign, banner, flag, logo, QR, link, ruler or grid. Do not reproduce the text shown in the reference.
```
