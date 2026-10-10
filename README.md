# DSKY QUOTES 🇧🇯

> **Citations — C. Jésutondji Samuel Stein « Dsky »** · Lyriciste · Bénin
> Série de quotes 100 % IA : portrait fidèle (aucune modification du visage), fonds réinventés,
> typographie professionnelle incrustée par programme (Playfair Display & Montserrat).

---

## 📁 Structure

```
DSKY-QUOTES/
├── citations/
│   └── citations_corrigees.md     ← les 41 citations corrigées & affinées (féminins marqués)
├── assets/
│   ├── bases/                     ← visuels IA générés à partir des photos originales
│   ├── photos-originales/         ← photos sources (photos studio + dossiers Samu / Samuel)
│   └── fonts/                     ← Playfair Display + Montserrat (OFL)
├── salve-01 … salve-04/
│   ├── post/                      ← 1080×1350 (4:5) — feed IG / FB
│   └── story/                     ← 1080×1920 (9:16) — story / statut WhatsApp
├── salve-05/                      ← citation 41 (la finale) + couverture cover-post/cover-story
├── salve-0N.json                  ← métadonnées (texte, style, base) de chaque salve
├── compose.py                     ← moteur de composition (texte, badge, signature, drapeau 🇧🇯)
├── cover.py                       ← générateur de couverture
├── push.sh                        ← push main + branche légère en 1 commande
└── README.md
```

## 🎨 Direction artistique (style « mix »)

| Style | Ambiance | Usage |
|---|---|---|
| `LUXE` | noir & or, chiaroscuro | citations fortes, dignité, argent |
| `MINIMAL` | dégradés doux, épuré | réflexions, relations |
| `AFRO` | couleurs du Bénin, énergie urbaine | punchlines, fierté, humour |

**Charte** : badge pilule `DSKY 🇧🇯` (drapeau béninois vectorisé) en haut à gauche ·
numéro de la citation à droite · citation centrée dans le tiers supérieur ·
signature `C. JÉSUTONDJI SAMUEL STEIN — LYRICISTE · BÉNIN` en bas.

## 🔁 Reproduire / étendre

```bash
# 1. Générer les bases IA (une par citation, visage préservé) → assets/bases/base-XX.jpg
# 2. Renseigner salve-0N.json (num, style, base, text)
# 3. Composer :
python3 compose.py 01     # → salve-01/post/*.jpg + salve-01/story/*.jpg
```

## 🗺️ Planning des salves

- [x] **Salve 01** — citations 1 → 10
- [x] **Salve 02** — citations 11 → 20 *(photos réelles de l'auteur, grading cinéma par citation)*
- [x] **Salve 03** — citations 21 → 30 *(fonds studio/cinéma régénérés, texte hors visage)*
- [x] **Salve 04** — citations 31 → 40 *(les 3 photos studio d'origine, 10 fonds uniques)*
- [x] **Salve 05** — citation 41, la finale *(+ couverture « PENSÉES d'un Lyriciste béninois »)*

---

© 2026 C. Jésutondji Samuel Stein — Visuels générés par IA d'après les photos de l'auteur.
Polices : SIL Open Font License.


---

# 🎤 SAISON 2 — « Le voyage du parolier » (45 → 54)

- **Format** : Story 1080×1920 uniquement
- **Images** : 100 % IA (scènes anonymes — silhouettes, objets, foules) — aucune photo de l'auteur
- **Citations** : écrites par l'IA pour l'auteur, dans sa voix de lyriciste
- **Nouveauté** : barre CTA intégrée — *Like · Commente · Partage · Abonne-toi*
- **Moteur** : `compose_s2.py` + `saison-02.json` → `saison-02/story/`

---

# 🖤 Les Vraies (55 → 64)

- **Format** : Story 1080×1920 uniquement — `saison-02/story/`
- **Citations** : thèmes imposés par l'auteur, écrits dans sa voix (*l'argent, le cœur, la rue…*)
- **Visuels** : 100 % IA anonymes, une ambiance par citation

---

# 🎨 Série ART (65 → 90)

Série ART I→IV (65 → 100). La citation est **typographiée par l'IA à l'intérieur de l'œuvre elle-même**
(effet chic, vocabulaire simple). Le code n'ajoute plus que le branding : badge `DSKY 🇧🇯`,
N°, signature, drapeau et barre CTA dans la bande basse — moteur `compose_art.py`.

*Lisibilité d'abord : lettres grandes, horizontales, fort contraste.*

| # | Thème | Style de l'œuvre |
|---|---|---|
| 65 | Le travail | constructivisme russe |
| 66 | La passion | anime flamboyant |
| 67 | La musique | BD africaine |
| 68 | La famille | Disney/Pixar |
| 69 | Les faux amis | ligne claire (ombre au poignard) |
| 70 | Le temps | Art Déco |
| 71 | Le silence | estampe ukiyo-e |
| 72 | Pardonner | vitrail gothique |
| 73 | Temps & argent | Bauhaus / style suisse |
| 74 | La jalousie | timbre gravé |
| 75 | L'amour vrai | Ghibli aquarelle |
| 76 | L'échec | affiche de film |
| 77 | La discipline | comics américain |
| 78 | La vérité | papercut renard & loup |
| 79 | La mère | mosaïque kente |
| 80 | Le rêve | fresque urbaine |
| 81 | La trahison | néo-noir cinématographique |
| 82 | L'ami & ta place | huile, bar feutré |
| 83 | Le boulot | affiche suisse |
| 84 | Le sourire qui sauve | supérette africaine la nuit |
| 85 | Tomber amoureux | gouache, taxi au crépuscule |
| 86 | Les petits bonheurs | illustration conte |
| 87 | La déception | comic book noir & rouge |
| 88 | Les rêves reportés | anime nostalgique |
| 89 | Les masques | nature morte baroque |
| 90 | Le vrai amour | cuisine à 1 h du matin |
| 91 | Le capital confié | huile Caravaggio (ailes noires) |
| 92 | Les secrets | surréalisme Magritte |
| 93 | La réussite | escalier de marbre dans la brume |
| 94 | Le serpent | miniature persane |
| 95 | L'aube de la ville | marché de l'aube |
| 96 | La pluie | aquarelle nocturne, tôle |
| 97 | L'honnêteté | linogravure taximan |
| 98 | Le je t'aime des nôtres | photo familiale |
| 99 | Le message relu | photo nocturne |
| 100 | Le masque de l'argent | portrait baroque doré |
| 101 | Les deux rires | pop art (Warhol) |
| 102 | Le conseiller | théâtre d'ombres wayang |
| 103 | L'argent & la rue | crépuscule, deux mondes |
| 104 | L'acteur | expressionnisme muet |
| 105 | Le but du quartier | affiche foot rétro |
| 106 | L'appel de loin | nocturne, téléphone ancien |
| 107 | Vingt ans | mains au marché |
| 108 | La paix signée | jazz Harlem |
| 109 | Le nom | sceau de cire |
| 110 | L'heure juste | Catrina au sablier |
| 111 | La confiance fêlée | kintsugi à l'or |
| 112 | La main sous la nappe | noces N&B |
| 113 | Le SMS de paie | risographie |
| 114 | Le vieux père | cyanotype |
| 115 | Le visage du matin | Art Nouveau (Mucha) |
| 116 | Le bonjour banal | quai de gare années 50 |
| 117 | Le projet murmuré | sumi-e |
| 118 | La dignité | studio Sidibé 1960 |
| 119 | La clé de la confiance | mosaïque byzantine |
| 120 | Le miroir du matin | marbre antique |
| 121 | Ton prime c'est maintenant | affiche boxe rétro |
| 122 | Le défi grandit | chevalier & dragon |
| 123 | Le bon moment | constructivisme |
| 124 | La peur grossit | pulp comic |
| 125 | Champion du report | affiche satirique |
| 126 | Rétréci | théâtre |
| 127 | Vite fait, fait | forge |
| 128 | Un toi debout | affiche WPA |
| 129 | L'abonnement au doute | pop art |
| 130 | Changer de propriétaire | Art Déco |
| 131 | Le distributeur vide | film noir surréaliste |
| 132 | La porte entrouverte | photo N&B |
| 133 | Le soleil gratuit | affiche voyage 50s |
| 134 | Le havre | marine au phare |
| 135 | La petite faim | nature morte baroque |
| 136 | Les 20 % | photo domestique |
| 137 | Meuble / pensée | photo conceptuelle |
| 138 | La larme | film noir |
| 139 | Le non propre | rose refusée |
| 140 | La plante du voisin | gouache narrative |
| 141 | Le bateau de papier | macro billet-bateau |
| 142 | La montre fondue | montre Dalí |
| 143 | Les masques à prix | photo conceptuelle |
| 144 | Le forage de joie | mère & fils, heure dorée |
| 145 | La porte intérieure | clé-billet & miroir |
| 146 | L'invité sans argent | gravure ancienne |
| 147 | Partir pour toi | escalade à l'aube |
| 148 | Les ficelles | constructivisme |
| 149 | Le portefeuille du père | tirelire-lion |
| 150 | La couronne qui coule | couronne dans le sable |
| 151 | Qui lit sur toi | manguier & marché |
| 152 | Le diplôme au tiroir | nature morte |
| 153 | La correction | tableau-fenêtre |
| 154 | Les langues du marché | gamin & costards |
| 155 | Le passeport | néo-noir néon |
| 156 | Qui ne pas prêter | linogravure |
| 157 | Mère / prof / rue | double exposition |
| 158 | Le premier salaire | mains calleuses |
| 159 | Les refus notés | couloir de portes |
| 160 | Quand tu as faim | forge |
| 161 | L'homme pressé | portail des nuages |
| 162 | Celui qui crie | oni & moine |
| 163 | Le feu de paille | braises |
| 164 | L'eau calme | dragon du fleuve |
| 165 | Le vent et le soleil | esprit & déité |
| 166 | Celui qui écoute | taverne de guilde |
| 167 | La maison au feu | esprit-flamme |
| 168 | Le tambour | taiko géant |
| 169 | Les trois saisons | sanctuaire |
| 170 | Les jambes de la vérité | renard à neuf queues |
| 171 | La poignée de main | corridor & corbeaux |
| 172 | Réunion | salle en deux moitiés |
| 173 | Le vrai et le faux | rose vs serpents |
| 174 | Les deux masques | bal masqué |
| 175 | La disparition | coffret & fumée |
| 176 | Le coin de la taverne | brinde & murmure |
| 177 | La lumière de la chance | bannière royale |
| 178 | Le conseil de la nuit | lanterne & roue |
| 179 | La marmite vide | bol fumant sous la pluie |
| 180 | Dix ombres | feu de camp |
| 181 | En phase ? | festival flou |
| 182 | Le miroir retourné | terrasse à l'aube |
| 183 | Tes gestes le crient ⭐ | miroir & lumières |
| 184 | Droite | reine au fil d'or |
| 185 | Le cœur embellit | marchande rapiécée |
| 186 | Le parfum | roses fanées |
| 187 | Le vrai maquillage | rire doré |
| 188 | Sans savoir pourquoi | la jarre portée |
| 189 | Laide, vraiment ? | garde vs noble glacé |
| 190 | La jalousie | masque fendu |
| 191 | Le chien | voleur acculé |
| 192 | Le pain du travail | ouvrier vs voleur |
| 193 | L'argent à jambes | pièces ailées |
| 194 | Le nom vide | monument effrité |
| 195 | Les mains de fumée | butin emporté |
| 196 | À la porte | gardes masqués |
| 197 | La nuit ou le matin | route en deux |
| 198 | La main qui vole | balance & braises |
| 199 | Les portes verrouillées | grille sous la pluie |
| 200 | Le tambour muet | village en cercle |
| 201 | Chaque pierre | route aux gargouilles |
| 202 | En secret | jardinier & arbre-vision |
| 203 | Les mouches | graine sous cloche |
| 204 | Sans discours | forêt-cathédrale |
| 205 | Le fleuve et la flaque | vallée miroir |
| 206 | L'arme qui ne s'émousse pas | samouraï |
| 207 | Ton travail parle | forgeron |
| 208 | Avant de semer | crieur de moisson |
| 209 | Ton calme | porte & curieux |
| 210 | Sans microphone | moisson & anneaux |
| 211 | La flèche en cendres | archer maudit |
| 212 | Le champ vide | compteur de récoltes |
| 213 | Le trousseau de clés | œil à la serrure |
| 214 | Le premier fan | l'ombre qui suit |
| 215 | Leur miroir | bal des reflets |
| 216 | Vrais vs masques | deux couloirs |
| 217 | Son propre grenier | soufflet de nuit |
| 218 | L'arme | souffle en lames |
| 219 | Bon courage | allée des masques |
| 220 | Le bonheur silencieux | fumée au petit matin |

Textes intégraux : `citations/citations_corrigees.md` (sections Série ART, ART II, ART III).

---

© 2026 C. Jésutondji Samuel Stein — Visuels 100 % IA. Polices : SIL Open Font License.

### 📱 Version TIKTOK (`saison-02/tiktok/` — moteur `compose_art_tt.py`)
Mêmes œuvres, mais branding remonté en **zone sûre TikTok** : signature + CTA terminent à ~1630 px,
**290 px libres en bas** pour le pseudo / la légende / le titre musical de TikTok — rien n'est masqué.
