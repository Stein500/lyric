# PROGRESS — Noukiko tché wê

Mise à jour : 2026-09-22

## État du chantier

- [x] Prompt universel v5.2 mis à jour : drapeau béninois à côté du badge mobile, badge juste au-dessus des paroles, motifs béninois discrets.
- [x] Héroïne validée : jeune fille noire béninoise de 13–14 ans, bien joufflue, sourire naturel.
- [x] Banque d'images 9:16 : ancrage + salves `s01` à `s69`.
- [x] Variété renforcée : plans assis, marche, profil, trois-quarts, danse, accroupie, fenêtre, banc, balançoire, bord de l'eau, gros plans.
- [x] Banderole béninoise chic et discrète ajoutée en bas des images.
- [x] Affectation paroles/images préparée dans `PLAN_9x16_Noukiko.md` : 50 occurrences minutées, 34 vers uniques, répétitions réutilisées.
- [ ] Validation audio exacte des fenêtres de paroles.
- [ ] Préparation du lock-up post-production : drapeau vectorisé à gauche + badge `DSKY✓`, juste au-dessus du `lyric_bbox`.
- [ ] Rendu vidéo continu 9:16 1080×1920.
- [ ] Contrôles durée, blackdetect, dernières 30 secondes, lisibilité et safe zones.

## Blocage technique actuel

L'encodeur `ffmpeg/ffprobe` n'est pas installé dans le sandbox et l'accès réseau du gestionnaire de paquets est indisponible. Le plan, les images et l'affectation sont prêts ; l'export MP4 commencera dès que l'encodeur sera disponible.

## Livrable prévu

`livrables/Noukiko_tche_we_9x16_v1.mp4`
