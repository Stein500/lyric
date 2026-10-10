# Analyse — « Ça monte, ça descend » (Dsky)

Date d'analyse : 2026-10-10 · Sources : `Ça monte_ ça descend.mp3`, `Ça monte, Ça descend.txt` (55 vers horodatés), tags ID3 du MP3.

## 1. Fiche technique (mesurée)

| Élément | Valeur | Remarque |
|---|---|---|
| Durée décodée | **197,60 s** (3 min 17 s) | mesurée par ffmpeg (`-f null`), pas seulement le tag `[length:03:17]` |
| Format source | MP3 190 kb/s, 48 kHz, stéréo | pochette 360×360 intégrée |
| Crête (flottant décodé) | **+3,02 dBFS** | le décodage dépasse 0 dBFS → à traiter au master (limiteur / loudnorm) |
| Loudnorm passe 1 (cible −14 LUFS / TP −1,5) | entrée **−14,31 LUFS**, TP **+0,72 dBTP**, LRA 4,9 | niveau déjà proche de la cible ; le TP est au-dessus de 0 |
| Tempo estimé | **≈143,6 BPM** (ou 71,8 BPM en demi-tempo) | ambiguïté demi/double tempo : le « ça monte / ça descend » sonne en demi-tempo |
| Métadonnées | titre « Ça Monte, Ça Descend », artiste `codjosamuelstein` | commentaire ID3 : **« made with suno »** → morceau généré par IA |

## 2. Dynamique (RMS par tranche de 10 s)

| Tranche | dBFS | Lecture |
|---|---|---|
| 0–10 s | −22,7 | intro 808 glissé, voix grave |
| 10–30 s | −18,8 → −16,2 | montée progressive |
| 30–40 s | −14,4 | entrée couplet 1 |
| 40–130 s | −11,2 → −13,4 | bloc énergique (couplets, pré-refrains, drops) |
| 130–150 s | −15,0 / −15,2 | creux (pont piano, respiration) |
| 150–190 s | −10,3 → −9,6 | outro / drop final, le plus fort du morceau |
| 190–198 s | −28,9 | queue silencieuse |

Le morceau monte en trois paliers puis retombe dans le pont. La dynamique est « ça monte, ça descend » **littéralement**, ce qui justifie le découpage visuel (fond club → rue → drop → pont calme).

## 3. Structure (balises USLT du MP3)

1. **Intro** (0–14 s) : « Wolof TechStein beat wê ! », « Yeah! Let's go! », « Ça monte! / Ça descend! »
2. **Refrain** (14–27 s) : « Ça monte, ça descend… »
3. **Couplet 1** (27–47 s, rap rapide) : « Trois heures du mat' … », « Wadjaya… », « Vivi oor… », « Djalé… »
4. **Pré-refrain** (46–53 s) : « Ça monte, ça monte… » — build-up
5. **Drop / refrain** (53–72 s) : « ÇA MONTE, ÇA DESCEND… », « J'SUIS DANS L'BÂTIMENT »
6. **Couplet 2** (≈80–100 s, voix féminine) : « J'suis dans l'game… », « Kissi noumi… », « Gbètché vivi… », « Nonvi konou… », « Dokpè… »
7. Pré-refrain + drop répétés (≈100–125 s)
8. **Pont** (≈132–152 s, piano, calme) : « Ça redescend… / Mais ça va remonter dans un instant »
9. **Drop final** (≈152–190 s, tutti, 808 massifs) puis tag « (On s'arrête jamais...) » à 192 s

Les tags de section (USLT) donnent la forme ; les horodatages `[mm:ss.xx]` ne couvrent que **55 lignes** (les refrains répétés ne sont pas horodatés).

## 4. Horodatages et fenêtres sans parole (base de la clochette)

Hypothèse de durée d'affichage (à valider à l'écoute) : `min(4 s, max(2 s, 0,07 s × nb_caractères + 1,2 s))`, bornée par le vers suivant.

Fenêtres **sans texte ≥ 5 s** (clochettes CTA), calculées par `render_lyric_video.py` :

| # | Fenêtre | Durée | Passages (répétés toutes les 4 s) |
|---|---|---|---|
| 1 | 72,69 → 78,32 s | 5,63 s | 2 |
| 2 | 125,71 → 131,88 s | 6,17 s | 2 |
| 3 | 142,75 → 152,25 s | 9,50 s | 3 |
| 4 | 186,37 → 192,13 s | 5,76 s | 2 |

- Intro 0 → 4,88 s : 4,88 s seulement → **pas de clochette** (sous le seuil), remplacée par la carte d'accueil.
- Queue après « On s'arrête jamais » : 2,7 s → pas de clochette, la carte finale prend le relais.

Données complètes : `timings_audited.json`.

## 5. Points de vigilance

1. **Crête +3 dBFS** au décodage : le master doit être limité (TP ≤ −1,5 dBTP) avant publication audio seule ; la vidéo livrée reprend l'audio source tel quel en AAC 256 kb/s.
2. **Calage des mots provisoire** : les mots sont répartis au nombre de caractères sur la durée du vers. Un calage vocal réel n'a pas été fait.
3. **Tag « made with suno »** : à déclarer si la plateforme demande une étiquette de contenu généré par IA (TikTok propose ce réglage).
4. **Langues** : français + mots fon/ewe/wolof (ex. « gbètché », « nonvi », « dokpè ») — sous-titres à vérifier avec l'artiste avant une traduction.
5. **Fonds IA** : quatre scènes sans texte, sans visage, sans logo. Aucune photo personnelle n'a été envoyée au générateur.

## 6. Décisions appliquées à ce clip (cf. prompt v5.7)

- Carte d'accueil 0 → 4,9 s : « Regarde jusqu'à la fin » puis « pour découvrir comment proposer un son ou des lyrics à réaliser pour toi ! ».
- Drapeau du Bénin **retiré** partout (badge « Dsky » seul).
- Fin : plus de contacts. « Merci d'avoir regardé » + code **1010** (« 1 = ça monte · 0 = ça descend »).
- Clochette : typographie premium (Montserrat ExtraBold/Black, dégradés, halo) au lieu du rendu archaïque.
