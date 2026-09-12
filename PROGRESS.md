# Toko Longa — production progress

**Projet :** lyric visual vertical 9:16 + teaser + trois covers
**Titre :** *Toko Longa*
**Artiste :** Nass'M Rodyboy
**Réalisation lyric visual :** Techstein / DSKY Prod
**Branche :** `arena/01a09162-lyric`
**Référence de travail :** prompt universel v4.8.2, adapté au projet Toko Longa
**Direction validée pour cette passe :** documentaire cinématique, mariage visuel Bénin × Congo, terre rouge, palmiers, travail collectif, cyan discret et ambre solaire.

## Décisions de cette passe

- [x] Source audio et paroles identifiées dans le dépôt.
- [x] Audio mesuré : `179.328 s` (2:59.328), 48 kHz, stéréo, MP3 source 128 kb/s.
- [x] Cinq images teaser générées à partir des références `Sam/` et `Samu/`.
- [x] Trois bases de covers générées en 9:16.
- [x] Badge de marque choisi : `DSKY✓`, centré en haut, discret, fixe et posé en post.
- [x] CTA des deux premières secondes : trois icônes vectorielles fixes (like, abonnement, commentaire), sans texte long.
- [x] Icône de partage prévue au milieu du teaser et du lyric visual.
- [ ] Validation artistique finale des cinq images teaser et des trois covers.
- [x] Rendu du teaser 9:16 avec extrait `01:52.73 → 02:20.68` (`27.95 s`).
- [x] Rendu du lyric visual 9:16, paroles LRC nettoyées et synchronisées sur un flux continu à 30 fps.
- [x] Export MP3 master/tagué avec cover (`320 kb/s`, 48 kHz, `179.328 s`).
- [x] Finalisation des trois covers JPG (`1080×1920`, titre et crédits composés en post pour garantir l'orthographe).
- [x] Contrôle automatique : résolutions conformes, durée lyric `179.29 s` (écart `0.04 s`), aucun intervalle `blackdetect > 300 ms`, aucun intervalle `freezedetect ≥ 0.5 s` sur les exports finaux.
- [ ] Commit et push des livrables validés.

## Images teaser — 5 images demandées

| Slot | Fichier | Paroles / intention |
|---|---|---|
| 01 | `assets/raw/teaser/01_pas_de_pluie.png` | « Pas de pluie, pas de choix, faut y aller » / terre sèche et marche commune |
| 02 | `assets/raw/teaser/02_creuse_la_nuit.png` | « On creuse la nuit pour trouver de l'or » |
| 03 | `assets/raw/teaser/03_goutte_lingot.png` | « La gorge sèche… chaque goutte d'eau vaut un lingot » |
| 04 | `assets/raw/teaser/04_clan_soude.png` | « Le village attend, le clan est soudé » |
| 05 | `assets/raw/teaser/05_triomphe.png` | « La terre est dure mais on va réussir » / triomphe |

Les quatre images complémentaires déjà présentes sous `assets/raw/teaser/` servent uniquement à enrichir le lyric visual complet sans changer le budget teaser de cinq images.

## Extrait teaser

- Départ audio : `112.73 s` (`01:52.73`)
- Fin audio : `140.68 s` (`02:20.68`)
- Durée : `27.95 s`
- Pourquoi : bloc continu de paroles sur la dalle, le travail, les diamants, le clan, la faim et la réussite — pas de collage audio discontinu.

## Arborescence de production

- `assets/raw/teaser/` : sources IA verticales, sans texte ni badge.
- `assets/raw/covers/` : bases IA verticales, sans texte ni badge.
- `scripts/render_toko_longa.py` : rendu reproductible PIL + flux vidéo continu + mux audio.
- `livrables/` : exports finaux, volontairement versionnés.
- `work/` : environnement et caches locaux, ignorés par Git.
