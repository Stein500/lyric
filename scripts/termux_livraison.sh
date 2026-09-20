# 📱 LIVRAISON TERMUX — 'Nan yi a ga djin wê' v3 FINAL (commit b38ec25a, livrables inclus)
# FORMAT ANTI-CASSE §E.6 : UNE SEULE LIGNE, séparateur ';' (jamais && ni \), curl -fL -C - reprenable.
# Repo PUBLIC ✔ → raw.githubusercontent sans token.
#
# ── Checklist Termux fraîchement installé (une ligne) :
# pkg update -y; pkg install -y curl ca-certificates; termux-setup-storage; mkdir -p /storage/emulated/0/Web+
#   (accepter le popup stockage)
#
# ── TOUT TÉLÉCHARGER dans Web+ (une seule ligne, copier-coller tel quel) :
mkdir -p /storage/emulated/0/Web+; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/NanYiAGa_clip_9x16_v3.mp4 https://raw.githubusercontent.com/Stein500/lyric/b38ec25a81b66ef02ea1b1dc0a8202bd85181ab5/livrables/Nan%20yi%20a%20ga%20djin%20w%C3%AA%20-%20clip%209x16.mp4; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/NanYiAGa_master.mp3 https://raw.githubusercontent.com/Stein500/lyric/b38ec25a81b66ef02ea1b1dc0a8202bd85181ab5/livrables/Nan%20yi%20a%20ga%20djin%20w%C3%AA%20-%20master.mp3; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/NanYiAGa_cover_1920.jpg https://raw.githubusercontent.com/Stein500/lyric/b38ec25a81b66ef02ea1b1dc0a8202bd85181ab5/livrables/Nan%20yi%20a%20ga%20djin%20w%C3%AA%20-%20cover%201080x1920.jpg; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/NanYiAGa_cover_1080.jpg https://raw.githubusercontent.com/Stein500/lyric/b38ec25a81b66ef02ea1b1dc0a8202bd85181ab5/livrables/Nan%20yi%20a%20ga%20djin%20w%C3%AA%20-%20cover%201080x1080.jpg; curl -fL --retry 5 --retry-delay 3 -C - -o /storage/emulated/0/Web+/PROMPT_UNIVERSEL_v5.2_FINAL.md https://raw.githubusercontent.com/Stein500/lyric/b38ec25a81b66ef02ea1b1dc0a8202bd85181ab5/PROMPT_UNIVERSEL_v5.2_FINAL.md; ls -la /storage/emulated/0/Web+/
#
# ── Vérification post-téléchargement (md5 attendus) :
#   162e81c07f6ebee777586518a9e710ed  NanYiAGa_clip_9x16_v3.mp4  (40,1 Mo)
#   19a97fdea94de745b37f609d07bfc4af  NanYiAGa_master.mp3        (6,9 Mo)
#   f0fc14974b71394c148ce3f49cb187dc  NanYiAGa_cover_1920.jpg
#   36950750b4f14299ec716460952dcb46  NanYiAGa_cover_1080.jpg
#   bd887438a55ea7d81fd0862c056ba8cd  PROMPT_UNIVERSEL_v5.2_FINAL.md
# md5sum /storage/emulated/0/Web+/NanYiAGa_* /storage/emulated/0/Web+/PROMPT_*
#
# ── Si le shell reste bloqué sur '>' : Ctrl+C avant de coller.
