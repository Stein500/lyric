# IMELDA · 13 NOVEMBRE — WTBW

**Trois films, dix affiches, trois couvertures.** Photos réelles de Imelda, aucun visage généré.
Signature unique et discrète : **WTBW**. Pas de drapeau, pas de contact, pas de code, pas de lien.

---

## 1. Les trois films (9:16 · 1080 × 1920 · 30 ips · H.264 + AAC 256 k)

| # | Film | Refrain utilisé | Durée | Poids | Loudness | Crête |
|---|------|-----------------|-------|-------|----------|-------|
| 1 | `IMELDA-01-NOUKIKO-TCHE-WE-WTBW-9x16.mp4` | *Noukiko tché wê* (16,19 → 58,80) | 42,60 s | 18 Mo | −13,9 LUFS | −1,1 dBFS |
| 2 | `IMELDA-02-AYON-DEKPE-WTBW-9x16.mp4` | *Ayon dèkpè* (40,23 → 80,60) | 40,37 s | 22 Mo | −14,0 LUFS | −2,1 dBFS |
| 3 | `IMELDA-03-TU-ES-TROP-BELLE-WTBW-9x16.mp4` | *Tu es trop belle* (86,49 → 125,00) | 38,50 s | 13 Mo | −13,8 LUFS | −3,6 dBFS |

Photos distinctes d'un film à l'autre :

- **Film 1 — le sourire :** 0031 · 0041 · 0036 · 0039 · 0048
- **Film 2 — la lumière :** 0043 · 0030 · 0046 · 0033 · 0037
- **Film 3 — la déclaration :** 0049 (enfant) · 0067 · 0066 · 0042

Écriture à l'écran (mature, dans l'esprit WTBW) :

1. « c'est mon sourire à moi » → *Personne ne te l'enlèvera.* → *Il y a des sourires qui réparent une journée.* → *Le tien répare des années.* → *Alors aujourd'hui, on le célèbre.*
2. *Tu ne marches pas : tu fais danser la lumière.* → *tu es trop jolie.* → *Le monde s'arrête quand tu passes.* → *Et moi, je reste à regarder.* → *Merci d'être toi.*
3. *Il y avait déjà ce sourire.* → *j'ai la trouille, c'est fou.* → *Je n'ai jamais eu peur du monde.* → *Seulement de ton regard.*

Carte finale commune : **JOYEUX ANNIVERSAIRE / Imelda / vœu / MERCI D'EXISTER / WTBW**.

---

## 2. Titres, captions, hashtags

**Film 1 — « NOUKIKO TCHÉ WÊ »**
> 13.11 · Le sourire qui répare mes journées. Joyeux anniversaire, Imelda. 🖤 « Noukiko tché wê » — WTBW

**Film 2 — « AYON DÈKPÈ »**
> 13.11 · Elle ne marche pas, elle fait danser la lumière. Joyeux anniversaire, Imelda. « Ayon dèkpè » — WTBW

**Film 3 — « TU ES TROP BELLE »**
> 13.11 · Je n'ai jamais eu peur du monde. Seulement de ton regard. Joyeux anniversaire, Imelda. « Tu es trop belle » — WTBW

**Hashtags (13 max, identiques aux trois)**
`#WTBW #WolofTechStein #JoyeuxAnniversaire #Imelda #13Novembre #NoukikoTcheWe #AyonDekpe #TuEsTropBelle #Cotonou #Benin #Afrobeats #Lyrics #Dsky`

---

## 3. Les dix affiches (1080 × 1350)

`livrables/affiches/AFFICHE-01…10-IMELDA-WTBW.jpg`

Dix décors N&B générés par IA (cadres végétaux, Art déco, sumi-e, marbre, papier déchiré, roses,
pinstripes, studio, halo) — **la personne n'est jamais générée ni retouchée** : sa photo réelle est
posée dans le décor, seule la mise en page (lettrage, filets, grain) est du studio.

Textes : « Joyeux anniversaire, Imelda. » · « Ce sourire-là, personne ne te l'enlèvera. » ·
« Tu ne marches pas : tu fais danser la lumière. » · « Et moi, je reste à regarder. » ·
« Il y a des sourires qui réparent une journée. » · « Le tien répare des années. » ·
« Tu es trop jolie. » · « J'ai la trouille, c'est fou. » · « Seulement de ton regard. » ·
« Joyeux anniversaire, Imelda. »

---

## 4. Couvertures TikTok (1080 × 1920)

`COVER-01-NOUKIKO-1080x1920.jpg` · `COVER-02-AYON-DEKPE-1080x1920.jpg` · `COVER-03-TROP-BELLE-1080x1920.jpg`

---

## 5. Déclaration IA

- **Visuels :** photos réelles de Imelda, étalonnées N&B par le moteur du studio. **Aucun visage généré,
  aucune retouche du corps, aucune image de synthèse de la personne.** Les dix décors d'affiche sont
  générés par IA (ornements, textures, cadres) sans personnage.
- **Audio :** maîtres de l'artiste (*Noukiko tché wê*, *Ayon dèkpè*, *Tu es trop belle*), **aucune voix ni
  musique générée**. Seuls les refrains ont été montés (coupe sur onset, fondu 0,02 s entrée / 1,0 s sortie)
  puis normalisés à −14 LUFS.

---

## 6. Contrôles mesurés

| contrôle | film 1 | film 2 | film 3 |
|---|---|---|---|
| durée | 42,60 s | 40,37 s | 38,50 s |
| frames | 1278 | 1211 | 1155 |
| blackdetect (0,05 s / 0,10) | fondus seuls (0–0,27 s, fin) | idem | idem |
| freezedetect (−33 dB / 2,5 s) | 2 passages lents | 2 | 6 |
| loudness | −13,9 LUFS | −14,0 LUFS | −13,8 LUFS |
| crête | −1,1 dBFS | −2,1 dBFS | −3,6 dBFS |
| faststart | `moov` avant `mdat` | idem | idem |
| audio | AAC 256 k · 48 kHz · stéréo | idem | idem |
| vidéo | H.264 High · CRF 22 · yuv420p · bt709 | idem | idem |

Les passages relevés par `freezedetect` sont les respirations lentes (zoom 1,02 → 1,12 sur 6 s) :
aucune image fixe, chaque frame porte grain animé, vague douce et poussières. Les cartes titre/finale
sont animées (révélations lettre à lettre, reflet qui balaie, dérive continue).

---

## 7. Ce qui n'a pas été fait, volontairement

- **Pas de code de fin, pas de CTA, pas de contact, pas de drapeau** : le studio reste neutre, seule WTBW apparaît.
- **Pas de son téléchargé sur le net** : les trois refrains de l'artiste sont utilisés (droits propres, voix intacte).
- **Pas de vidéos de Imelda** : aucune n'était fournie ; le mouvement vient du montage (zoom, vague, parallaxe).
- **Pas de 4e montage livré** : un médley 58 s des trois refrains existe en interne (`build_audio.py`), il n'est pas poussé.

---

## 8. Reproductibilité

```bash
python3 build_audio_songs.py      # 3 refrains -> cache/v{1,2,3}.m4a
python3 films.py v1               # film 1 (idem v2, v3)
python3 build_covers.py           # 3 couvertures
python3 build_posters.py          # 10 affiches (décors dans assets/decors/)
```

Dépendances : `pillow`, `numpy`, `scipy`, `imageio-ffmpeg`, `librosa` (analyse des onsets uniquement).
