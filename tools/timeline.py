# -*- coding: utf-8 -*-
"""
Timeline "Motivé" — Daïsky Prod / TechStein.

Toute la donnée de minutage (shots = images, subs = sous-titres) vit ICI,
dans un fichier commité, pour être reproductible et ne rien perdre même si
l'espace est réinitialisé.

Durée audio réelle : 158.90 s (2:38.90).
Section = ancrage sur les repères fournis par l'artiste ; les lignes
(vers/refrains) sont réparties proprement dans chaque section pour une
lisibilité parfaite (WrapStyle=1, pas de \n manuel).

Styles ASS : verse / hook / hook_final / bridge / wolof.
(Les paroles sont déjà en FRANÇAIS => pas de traduction FR sous chaque ligne.
  Seules les lignes WOLOF sont sans traduction, conformément à la charte.)
"""

# ---------------------------------------------------------------- SHOTS ----
# (start, end, image)  -> image depuis assets/raw/portrait/<image>.jpg
# La somme des durées doit être exactement 158.90.
SHOTS = [
    (0.000,  8.000, '01_ancrage_artiste_nuit'),
    (8.000, 15.000, '02_toit_ville_nuit'),
    (15.000, 22.000, '03_feu_veines_braises'),
    (22.000, 30.000, '04_marche_avant_rue'),
    (30.000, 38.000, '09_peuple_marche'),
    (38.000, 40.000, '04_marche_avant_rue'),
    (40.000, 45.000, '06_visages_derriere_verre'),
    (45.000, 49.000, '03_feu_veines_braises'),
    (49.000, 53.000, '05_escalier_montée'),
    (53.000, 56.000, '07_etoiles_yeux'),
    (56.000, 60.000, '08_construire_abri'),
    (60.000, 66.000, '03_feu_veines_braises'),
    (66.000, 74.000, '04_marche_avant_rue'),
    (74.000, 82.000, '09_peuple_marche'),
    (82.000, 83.900, '12_clash_plus_rapide'),
    (83.900, 86.000, '13_crier_dans_bruit'),
    (86.000, 88.000, '14_critiques_du_vent'),
    (88.000, 90.000, '15_regarde_nuit'),
    (90.000, 92.000, '16_etoiles_dans_les_yeux'),
    (92.000, 94.000, '17_course_neon'),
    (94.000, 97.000, '18_mon_peuple'),
    (97.000, 100.000, '16_etoiles_dans_les_yeux'),
    (100.000, 104.000, '18_mon_peuple'),
    (104.000, 110.000, '18_mon_peuple'),
    (110.000, 116.500, '16_etoiles_dans_les_yeux'),
    (116.500, 132.000, '19_refrain_final_explosif'),
    (132.000, 135.000, '10_triomphe_sommet'),
    (135.000, 150.000, '20_outro_aube'),
    (150.000, 158.900, '11_cover_hero_manga'),
]

# ---------------------------------------------------------------- SUBS ------
# (start, end, text, style)
SUBS = [
    # INTRO
    (1.000, 4.500, 'Wolof TechStein beat wê…', 'wolof'),
    (5.000, 10.000, 'Yeah… Motivé…', 'verse'),

    # REFRAIN 1
    (15.000, 19.000, 'Motivé, motivé, j\'suis pas fatigué', 'hook'),
    (19.000, 22.000, 'Le feu dans les veines, j\'suis toujours allumé', 'hook'),
    (22.000, 26.000, 'Motivé, motivé, j\'vais tout déchirer', 'hook'),
    (26.000, 30.000, 'T\'es pas dans ma ligue, tu peux toujours rêver', 'hook'),
    (30.000, 33.600, 'Wolof TechStein beat wê!', 'wolof'),

    # COUPLET 1
    (38.000, 39.600, 'J\'me lève tôt, j\'me couche tard', 'verse'),
    (39.600, 41.200, 'La vie m\'a donné des coups, j\'ai pris ma part', 'verse'),
    (41.200, 43.400, 'J\'ai vu des sourires se cacher derrière des dards', 'verse'),
    (43.400, 45.400, 'Des promesses en l\'air, des amis en retard', 'verse'),
    (45.400, 47.200, 'Mais j\'avance, j\'avance, j\'plie pas, j\'cède pas', 'verse'),
    (47.200, 49.000, 'J\'ai la tête haute, j\'crois en moi, j\'lâche pas', 'verse'),
    (49.000, 50.800, 'Les obstacles sont grands, mais mes rêves sont plus grands', 'verse'),
    (50.800, 53.000, 'Chaque pas que j\'fais, c\'est un pas vers les sommets', 'verse'),

    # PRÉ-REFRAIN 1
    (53.000, 54.000, 'Ils peuvent parler, ils peuvent douter', 'verse'),
    (54.000, 55.800, 'Pendant qu\'ils parlent, moi j\'avance, j\'vais les laisser', 'verse'),
    (55.800, 57.800, 'La route est longue, mais j\'ai le temps', 'verse'),
    (57.800, 60.000, 'J\'suis motivé, c\'est maintenant', 'verse'),

    # REFRAIN 2
    (60.000, 63.000, 'Motivé, motivé, j\'suis pas fatigué', 'hook'),
    (63.000, 66.000, 'Le feu dans les veines, j\'suis toujours allumé', 'hook'),
    (66.000, 71.000, 'Motivé, motivé, j\'vais tout déchirer', 'hook'),
    (71.000, 74.000, 'T\'es pas dans ma ligue, tu peux toujours rêver', 'hook'),
    (74.000, 77.600, 'Wolof TechStein beat wê!', 'wolof'),

    # COUPLET 2
    (82.000, 83.900, 'Tu m\'as pris pour un faible, t\'as cru que j\'allais plier', 'verse'),
    (83.900, 85.700, 'Mais j\'ai grandi dans le bruit, j\'ai appris à crier', 'verse'),
    (85.700, 87.500, 'Tes critiques, j\'m\'en balance, c\'est du vent, c\'est du bruit', 'verse'),
    (87.500, 89.300, 'Pendant que tu regardes en bas, moi j\'regarde la nuit', 'verse'),
    (89.300, 91.100, 'J\'ai des rêves plein la tête, des étoiles dans les yeux', 'verse'),
    (91.100, 93.300, 'Toi t\'es resté sur place, moi j\'vais toujours plus haut, c\'est mieux', 'verse'),
    (93.300, 95.100, 'J\'ai pas de temps pour les jaloux, les rageux, les aigris', 'verse'),
    (95.100, 97.000, 'J\'suis trop occupé à construire mon propre abri', 'verse'),

    # PRÉ-REFRAIN 2
    (97.000, 98.000, 'Ils peuvent parler, ils peuvent douter', 'verse'),
    (98.000, 100.000, 'Pendant qu\'ils parlent, moi j\'avance, j\'vais les laisser', 'verse'),
    (100.000, 102.000, 'La route est longue, mais j\'ai le temps', 'verse'),
    (102.000, 104.000, 'J\'suis motivé, c\'est maintenant', 'verse'),

    # PONT
    (104.000, 106.000, 'Le chemin est dur, mais j\'suis pas seul', 'bridge'),
    (106.000, 108.000, 'J\'ai ma foi, j\'ai mon cœur, j\'ai mon peuple', 'bridge'),
    (108.000, 110.000, 'Chaque pas que j\'fais, c\'est pour les miens', 'bridge'),
    (110.000, 116.500, 'Motivé, j\'irai jusqu\'au bout, c\'est certain', 'bridge'),

    # REFRAIN FINAL
    (116.500, 120.000, 'Motivé, motivé, j\'suis pas fatigué', 'hook_final'),
    (120.000, 123.900, 'Le feu dans les veines, j\'suis toujours allumé', 'hook_final'),
    (123.900, 128.000, 'Motivé, motivé, j\'vais tout déchirer', 'hook_final'),
    (128.000, 132.000, 'T\'es pas dans ma ligue, tu peux toujours rêver', 'hook_final'),
    (132.000, 135.500, 'Wolof TechStein beat wê!', 'wolof'),

    # OUTRO
    (135.500, 139.000, 'Wolof TechStein beat wê…', 'wolof'),
    (150.000, 152.000, '(Motivé…)', 'verse'),
    (152.500, 158.600, 'MOTIVÉ', 'hook_final'),
]

# ------------------------------------------------------------------ AUDIO ----
AUDIO = "Motivé- Daïsky 1.mp3"
DURATION = 158.90           # durée audio exacte (mesurée)
W = 1080
H = 1920
FPS = 24
