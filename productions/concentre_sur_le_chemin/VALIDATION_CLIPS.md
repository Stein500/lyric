# Concentré sur le chemin — contrôles des exports complets

**Contrôles exécutés le 2026-09-30.** Images approuvées par l’artiste (« Oui je valide !! ») ; exports v1 contrôlés techniquement. **Aucune approbation vocale/phonétique inventée.**

## Vidéos effectivement produites

| | Portrait | YouTube |
|---|---|---|
| Fichier | `livrables/Concentre_sur_le_chemin_9x16_v1.mp4` | `livrables/Concentre_sur_le_chemin_16x9_YT_v1.mp4` |
| Dimensions | 1080×1920 | 1920×1080 |
| Frames / FPS | 6 752 / 30 | 6 752 / 30 |
| Durée décodée vidéo | 225,066667 s | 225,066667 s |
| Taille exacte | 30 147 295 octets | 29 379 843 octets |
| Codec / couleur | H.264 High, yuv420p, BT.709 | H.264 High, yuv420p, BT.709 |
| Audio | AAC LC, 192 kb/s, 48 kHz stéréo | AAC LC, 192 kb/s, 48 kHz stéréo |
| Gel ≥1 s (`noise=-70dB`) | Aucun détecté | Aucun détecté |
| Noir détecté | Début 224,933333 s : fin du fondu uniquement | Début 224,933333 s : fin du fondu uniquement |
| Frames reconstruites contrôlées | 25 | 25 |
| Erreur RGB moyenne maximale | 3,2747 / 255 | 3,6525 / 255 |
| Fondus inter-scènes | 0,4 s, calculés dans le flux unique | 0,4 s, calculés dans le flux unique |
| Nouvelles générations IA | 0 | 0 |

Rapports complets avec SHA-256, échantillons couleur et résultats par frame : `qa_portrait.json` / `qa_landscape.json`. Les planches `livrables/controle_clip_{9x16,16x9_YT}_v1.jpg` utilisent des frames **réellement extraites des MP4**, pas uniquement des images avant encodage.

Calcul : 6,90 s d’ouverture + 213,160 s de chanson + 5 s de fin = **225,060 s** théoriques. `ceil(225,06×30)=6752`, soit 225,066667 s après arrondi à la frame. Le PCM vidéo a 10 803 200 échantillons par canal à 48 kHz, exactement 1 600 par frame. Un flux de frames, **pas de concat demuxer vidéo**. Hook et chanson sont assemblés après décodage audio.

## Paroles, badge et cadrage

- Les **58 occurrences / 38 textes distincts / 389 mots** sont conservés depuis les sources. Aucun changement de tournure (« concentrée » notamment), accent, casse ou mot local.
- Barlow Condensed Bold : **104–112 px** en portrait, **128 px** en paysage. Maximum quatre lignes portrait / deux lignes paysage.
- Bloc final composé et centré avant animation, largeur 720 px portrait (x=180→900) / 1640 px paysage (x=140→1780). Toutes les lignes restent fixes pendant l’apparition des mots.
- Portrait : bloc central incluant le padding transparent dans y=708→1212 ; l’encre visible reste au-dessus de la zone basse interdite et avant le rail droit x≥910. Paysage : bloc y=394→686, loin des contrôles bas y≥960.
- Mot actif crème/or, mots précédents atténués, vague continue d’amplitude 4,5 px à 0,9 Hz. Marges des vrais glyphes vérifiées après vague et contour.
- Badge `Dsky` + pictogramme vectoriel Bénin, position fixe, plafond 75 %, fondu entrée et sortie **0,4 s pour chaque vers**. Pas de doublon intégré au fond. Introduction et endcard ont leur propre fenêtre.
- Le bandeau Bénin est recomposé **après** le mouvement : 54 px portrait / 30 px paysage. PNG exacts ; échantillons des MP4 contrôlés avec une tolérance de 9 niveaux par canal.
- Mouvement paysage s03 conservateur pour préserver la chaussure proche du bord ; mouvement portrait s04 limité et cadrage adapté au badge. Aucun étirement non proportionnel du visage/corps.
- Le dernier ad-lib n’est pas prolongé sur les vingt dernières secondes instrumentales. L’endcard titre / WhatsApp / email commence sur les trois dernières secondes de la chanson et continue pendant les cinq secondes de fin.

## Vérification audio réelle — sans faux statut vocal

Corrélation à 12 kHz mono sur trois fenêtres de 5 s, source et audio décodé de chacun des MP4 :

| Source | Clip (ouverture comprise) | Déphasage portrait | Déphasage paysage |
|---|---|---|---|
| 00:25,30 | 00:32,20 | 0,000 s | 0,000 s |
| 01:25,64 | 01:32,54 | 0,000 s | 0,000 s |
| 02:32,84 | 02:39,74 | 0,000 s | 0,000 s |

Cela vérifie **l’absence de dérive ou d’erreur de montage audio**, pas les attaques vocales de chaque mot.

Les départs de vers sont ceux du LRC fourni ; avance d’affichage 0,03 s. Les mots sont répartis selon une estimation syllabique avec des ajustements faibles sur les pics proches. Les fins d’ad-libs éloignés sont plafonnées explicitement pour laisser respirer les instrumentaux. **Pas de forced alignment phonétique disponible ; pas de validation humaine à l’écoute enregistrée.** `approvals.vocal_sync=false` et `human_vocal_validation=false` sont volontairement conservés.

L’ouverture reprend 01:53,28→02:00,18 de la chanson (deux vers du refrain-titre, 6,90 s). L’option ouverture est demandée ; sa coupe n’a pas reçu d’approbation séparée. Demander un retour avec l’heure du clip et le mot concerné si un ajustement est nécessaire.

## Master et pochettes

- Chanson seule, **213,160 s décodées**, sans hook ni silence d’endcard.
- MP3 320 kb/s, 48 kHz stéréo, audio mappé explicitement avant ajout de la pochette.
- Loudnorm deux passes, mêmes pré-filtres highpass 30 Hz / lowpass 18 kHz, offset −0,53 à la passe 2, cible −14 LUFS / −1,8 dBTP.
- MP3 après encodage : **−14,02 LUFS / −1,64 dBTP**, sous le plafond −1,5 dBTP. Pas de gain correctif supplémentaire nécessaire.
- Durée gardée exacte malgré la queue du filtre loudnorm (padding/trim de 40 ms).
- ID3v2.4 : titre exact, Daïsky, contacts, provenance source ; paroles USLT sans timestamps, APIC carré 1080 identique au JPG livré. Aucun producteur/compositeur/genre inventé.
- Trois pochettes aux tailles 1080×1080, 1080×1920 et 1920×1080 ; fonds déjà approuvés réutilisés, Great Vibes pour le titre en post, DejaVu pour l’artiste/badge. Boîtes titre/artiste sans chevauchement, marges sûres vérifiées. Elles n’ont pas reçu d’approbation artistique séparée.
- Master récupéré de la sauvegarde : PCM reconstitué pour le paysage, audio MP3 comparé échantillon par échantillon au master publié ; **fichier master publié conservé à l’identique**, sans republier une variation de tags/padding.

Détails : `audio_master_report.json`, `covers_report.json` ; le SHA-256 du master publié est `2bae6f88839a7060433d2fe37e174ec8c5c9f2bd1b994af632530e606bb657ec`.

## Tests et livraison distante

- Suite : `python -m unittest discover -s tests -v` dans `/tmp/lyric-venv`.
- Résultat du passage final, après vérification distante : `test_run_report.json`.
- Manifeste des vrais fichiers : `delivery_manifest.json`.
- Preuves du hash GitHub, tailles, blobs, **contenu brut réellement téléchargé** et SHA-256 : `delivery_remote_checks.json`, écrit seulement après publication des médias.
- Index utilisateur : `livrables/LIVRAISON_Concentre_sur_le_chemin.md` ; empreintes `livrables/Concentre_sur_le_chemin_SHA256.txt`.
- Commandes Termux : `livrables/TERMUX_Concentre_sur_le_chemin_COMPLET.md`, une ligne par fichier, séparateurs `;`, `curl -fL --retry 5 --retry-delay 3 -C -`, dossier `/storage/emulated/0/Web+/`.
- Les commandes référencent le **commit immuable des médias/prompt**, contrôlé après push ; le document de commandes est naturellement committé ensuite. Pas de lien à une branche mutable, pas de faux hash.
- Pas de seconde archive contenant des copies des deux gros MP4 ; les fichiers se téléchargent séparément. Le ZIP existant reste limité aux dix fonds approuvés.

### Accès réseau pendant le contrôle distant

Le TLS direct vers `raw.githubusercontent.com` échoue dans cette sandbox (`curl` code 35), tandis que GitHub/API reste accessible. Le contrôle télécharge donc les **octets bruts via l’API GitHub** (`Accept: application/vnd.github.raw+json`) au même hash, puis compare taille et SHA-256. Le rapport distingue `raw_download_verified=false` et `api_raw_download_verified=true` : aucun faux statut de téléchargement direct. Certificats TLS toujours vérifiés. Les commandes Android restent les URL publiques raw canoniques, adaptées à la reprise ; l’API ne garantit pas `Range` et ne remplace donc pas silencieusement le lien de téléchargement Termux.
