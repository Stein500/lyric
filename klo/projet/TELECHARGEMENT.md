# 📥 Téléchargement des 3 vidéos Klo (Termux / Android)

**Destination obligatoire :** `/storage/emulated/0/Web+/`
Les vidéos sont dans le commit **`54ddb050bbcdfd92b2e23fe0bf74972f937de30f`**.
Si la connexion coupe, relance la même commande : `curl -C -` reprend tout seul.

```bash
# 1) Aller dans le dossier de travail + nettoyer les fichiers cassés
cd /storage/emulated/0/Web+/
find . -name "*.mp4" -size -100k -delete

# 2) Télécharger les 3 vidéos (reprenable)
curl -fL --retry 5 --retry-delay 3 -C - -o "Klo_V1_FestifOr_9x16.mp4" \
  "https://raw.githubusercontent.com/Stein500/lyric/54ddb050bbcdfd92b2e23fe0bf74972f937de30f/klo/projet/livrables/Klo_Anniversaire_V1_FestifOr_9x16.mp4"

curl -fL --retry 5 --retry-delay 3 -C - -o "Klo_V2_NuitCyan_9x16.mp4" \
  "https://raw.githubusercontent.com/Stein500/lyric/54ddb050bbcdfd92b2e23fe0bf74972f937de30f/klo/projet/livrables/Klo_Anniversaire_V2_NuitCyan_9x16.mp4"

curl -fL --retry 5 --retry-delay 3 -C - -o "Klo_V3_PartyConfettis_9x16.mp4" \
  "https://raw.githubusercontent.com/Stein500/lyric/54ddb050bbcdfd92b2e23fe0bf74972f937de30f/klo/projet/livrables/Klo_Anniversaire_V3_PartyConfettis_9x16.mp4"

# 3) Vérifier les tailles (V1 ~36M, V2 ~38M, V3 ~46M)
ls -lh /storage/emulated/0/Web+/Klo_V*.mp4
```

**Les 3 vidéos (1:45, 1080×1920) :**
- **V1 Festif Or/Rose** : photos robe rose + bokeh doré, gâteau, feux d'artifice.
- **V2 Nuit Cyan « Ma lumière »** : photos cosy + ciel étoilé cyan, néon.
- **V3 Party Confettis** : les 9 photos mélangées + confettis/ballons.

Chaque vidéo : son de la chanson + paroles incrustées calées sur la musique, badge
**⚡ DAÏSKY PROD** statique, format statut WhatsApp / TikTok / Reels.
