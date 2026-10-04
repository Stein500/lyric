# LIVRAISON — « ENTRE TES MAINS... » prière de début de semaine (TechStein)

Prompt appliqué : **PROMPT_UNIVERSEL_v5.5_HYBRIDE_COMMANDE.md** · branche `arena/01a10780-lyric` · commit livrables `1aa2c772e306021d130b3da36c0d2bba7e009a1e`.

## Configuration validée par l'artiste (§B)
- Fonds : **5 images** (`MODE_IMAGES=5`, portrait 9:16 seul) — exactement 5 générations.
- Style : **hybride S2 Golden Sunset + S4 Ink & Fire** (pont).
- Héros : **silhouette anonyme / mains en prière** (aucune photo personnelle).
- Badge : **Dsky + drapeau Bénin** (fondu 0,4 s par vers, ≤75 %, bandeau 54 px).

## Livrables (dossier `livrables/`)
| Fichier | Contenu | Contrôle |
|---|---|---|
| `Entre_Tes_Mains_clip_9x16.mp4` | clip lyrics complet 1080×1920, H.264 BT.709, 30 fps, 3543 frames, 118,10 s (hook 6 s + chanson 107,08 s + fin 5 s), AAC 192k | blackdetect = fade final seul ; freezedetect = 0 ; 23,1 Mo (<95 Mo) |
| `Entre_Tes_Mains_master.mp3` | chanson seule, 320 kb/s 48 kHz, loudnorm 2 passes | −14,49 LUFS / −1,71 dBTP ; ID3v2.4 : TIT2/TPE1 TechStein/TDRC 2026/TXXX contact+email/USLT/APIC |
| `cover_Entre_Tes_Mains_1080.png` | cover carrée 1080 (APIC) | titre cursive + Dsky + picto + bande Bénin, texte post-production |
| `cover_Entre_Tes_Mains_1080x1920.png` | variante story | idem + bandeau 54 px |
| `cover_Entre_Tes_Mains_1920x1080.png` | variante 16:9 | titre tiers gauche |
| `TERMUX_Entre_tes_mains.md` | commandes de récupération une-ligne | hash vérifié contenant tous les fichiers |

## Documents de production
- `../timings_audited.json` — structure audité (18/19 onsets confirmés par flux spectral ; regroupements L13+L14 / L15+L16 ; hook 85,02→91,02).
- `../ANALYSE.md` — mesures audio, hook, structure, master.
- `../PROMPTS_IMAGES_Entre_tes_mains.md` — les 5 prompts complets.
- `../PLANCHE_CONTACT.png` — planche de contrôle des scènes.
- `../backgrounds/` — les 5 originaux IA.
- `../scripts/` — pipeline rendu + covers/tags (versionnés).

## À confirmer par l'artiste à l'écoute
- Le calage mot à mot est **provisoire** (fenêtres de vers auditées, mots répartis au nombre de caractères).
- La coupe du hook (6,00 s naturelle) et le timing du vers « Une semaine de victoires et de vie » (81,53 s) sont signalés provisoires.
- Maquette intermédiaire de 15 s rendue et contrôlée avant le clip final (nommée MAQUETTE dans `work/`, non livrée).
