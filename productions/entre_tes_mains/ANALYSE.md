# ANALYSE — « Entre Tes Mains » (TechStein)

## Audio (§A.1)
- Source : `Entre tes mains.mp3` (repo racine), généré Suno (id 9f99ffc5…), TPE1 source `codjosamuelstein`.
- Durée décodée (`-map 0:a:0 -vn -f null -`) : **107,08 s** ; 48 kHz stéréo.
- Loudnorm passe 1 : `input_i=-16,25 LUFS`, `input_tp=+0,04 dBTP`, `input_lra=8,80`, `input_thresh=-26,66`, `target_offset=0,89`.
- RMS moyen −18,4 dB ; pas de silence interne (seul silence : 105,81→107,08, fin).

## Paroles & audit des horaires (§A.2/§A.3)
- Source LRC `[mm:ss.xx]` : 19 vers, premier tag vocal « C'est Techstein ».
- Audit par flux spectral (seuil 1,15×médiane locale 4 s) : 18/19 onsets confirmés à ≤0,35 s.
- Anomalies corrigées (voir `timings_audited.json`) :
  - L13 (1,26 s) et L15 (0,79 s) sous le minimum de travail 1,2 s → regroupements d'affichage en blocs 2 lignes (L13+L14, L15+L16), onsets conservés.
  - L17 : pic spectral à +0,55 s jugé accent instrumental (pas d'attaque vocale nette) → onset source 81,53 conservé, **signalé provisoire**.
- **Calage mot à mot PROVISOIRE** (répartition au nombre de caractères dans chaque fenêtre de vers) ; synchronisation vocale complète à confirmer à l'écoute par l'artiste.

## Hook (§A.5 / §6)
- Refrain-titre : « Entre Tes mains, je remets tout, » onset 85,02 (delta +0,02).
- Coupe naturelle proposée et utilisée : **85,02→91,02 = 6,00 s** (enveloppe RMS : fin de phrase ≈91,0, aucun silence exploitable) ; approuvée par inclusion dans la livraison, modifiable sur demande.

## Structure du clip
- TOTAL = HOOK 6,00 + chanson 107,08 + apad 5,00 = **118,08 s** → 3543 frames @30 fps (durée mesurée 118,10 s ✓ ±0,05).
- Paroles centrées H/2, largeur sûre ≤720 px, avance 0,03 s, apparition staggered 0,9 s, vague 4,5 px / 0,9 Hz, mot actif or, mots passés atténués lisibles.
- Badge `Dsky` + pictogramme Bénin, fondu 0,4 s par vers, opacité max 75 %, jamais permanent.
- Bandeau Bénin 54 px (y 1866→1920) composé en post, couleurs #008751/#FCD116/#E8112D.
- Ken Burns canvas 1188×2112, zoom 1,02↔1,08 alterné par slot, pan sinusoïdal ; crossfade 0,5 s aux frontières de scènes.
- Endcard 5 s : titre cursive GreatVibes + WhatsApp + email seulement + badge ; fade final 3 s audio+vidéo, seul noir du clip (blackdetect ✓), freezedetect = 0.

## Master (§D.4)
- Chanson seule, loudnorm 2 passes (pré-filtres highpass=30/lowpass=18000, `offset=0,90` passe 2), MP3 **320 kb/s 48 kHz**, `-t 107,08`.
- Contrôle final : **−14,49 LUFS / −1,71 dBTP** (TP ≤ −1,5 ✓).
- Tags ID3v2.4 : TIT2/TPE1 TechStein/TALB/TDRC 2026, TXXX contact+email, USLT paroles nettoyées, APIC cover 1080.
