# Timeline Yafoy — (texte, t0, t1, slot, doré?)  · horloge musique ; ADVANCE appliqué au rendu
ADVANCE = 0.03
DUR = 244.99
ENDCARD_T = 240.0        # début endcard (fade final ~240)
TOTAL = DUR + 5.0        # apad 5 s -> 249.99
R = True  # refrain -> doré
LINES = [
 ("Wolof TechStein beat wê !",        4.0,  6.5, 's01', R),
 ("Yeah... Yafoy t'es encore...",     6.5, 12.0, 's02', False),
 ("Yafoy t'es encore une légende",   12.0, 15.5, 's03', R),
 ("Yafoy t'es encore un combat",     15.5, 19.0, 's04', R),
 ("Yafoy t'es encore la flamme",     19.0, 23.0, 's05', R),
 ("Yafoy t'es encore là, comme ça",  23.0, 25.5, 's06', R),
 ("Wolof TechStein beat wê !",       25.5, 28.0, 's01', R),
 ("Tu as traversé des tempêtes, tu as vu des nuits noires", 34.0, 38.0, 's07', False),
 ("Tu as serré les poings, tu as refusé de croire",         38.0, 41.5, 's08', False),
 ("Les mensonges, les trahisons, les coups bas",            41.5, 44.5, 's09', False),
 ("Mais tu es encore debout, tu es encore là",              44.5, 48.5, 's10', False),
 ("On t'a dit « t'es fini, t'es trop vieux, t'es trop lent »",48.5, 51.0,'s11', False),
 ("Mais tu as ri, tu as dansé, tu es resté vivant",         51.0, 55.0, 's12', False),
 ("Tu es le rock qui ne meurt jamais",                      55.0, 57.5, 's13', False),
 ("La guitare qui hurle, le son qui t'emballe",             57.5, 62.0, 's14', False),
 ("T'es encore le feu, la passion",                         62.0, 65.5, 's15', False),
 ("T'es encore la révolution",                              65.5, 69.5, 's16', False),
 ("T'es encore la voix qui résonne",                        69.5, 72.5, 's17', False),
 ("T'es encore la couronne",                                72.5, 75.5, 's18', False),
 ("Yafoy t'es encore une légende",   77.0, 81.0, 's03', R),
 ("Yafoy t'es encore un combat",     81.0, 84.0, 's04', R),
 ("Yafoy t'es encore la flamme",     84.0, 88.0, 's05', R),
 ("Yafoy t'es encore là, comme ça",  88.0, 91.0, 's06', R),
 ("Wolof TechStein beat wê !",       91.0, 93.5, 's01', R),
 ("Les années passent, les modes changent, les gens s'en vont", 96.0,100.0,'s19', False),
 ("Mais toi tu restes, tu tiens, tu es le son",            100.0,103.0,'s20', False),
 ("Tu as vu des rois tomber, des stars s'éteindre",        103.0,106.5,'s21', False),
 ("Mais toi tu es la lumière qui ne cesse de peindre",     106.5,110.0,'s22', False),
 ("On t'a oublié, on t'a rangé, on t'a enterré",           110.0,114.0,'s23', False),
 ("Mais tu es revenu, tu as dansé, tu as frappé",          114.0,117.0,'s24', False),
 ("Tu es le violon qui pleure et qui crie",                117.0,120.0,'s25', False),
 ("Tu es la batterie qui fait vibrer la vie",              120.0,123.0,'s26', False),
 ("T'es encore le feu, la passion",                        127.0,130.0,'s15', False),
 ("T'es encore la révolution",                             130.0,134.0,'s16', False),
 ("T'es encore la voix qui résonne",                       134.0,137.0,'s17', False),
 ("T'es encore la couronne",                               137.0,140.0,'s18', False),
 ("Yafoy, t'es encore là, malgré tout",                    144.0,147.5,'s27', False),
 ("Malgré les doutes, les blessures, les dégoûts",         147.5,154.0,'s28', False),
 ("T'es encore debout, t'es encore fier",                  154.0,162.0,'s29', False),
 ("T'es encore le roi, le guerrier, la lumière",           162.0,168.5,'s30', False),
 # solo guitare 168.5 -> 210 : 3 images dédiées, pas de texte
 ("Yafoy t'es encore une légende",  210.0,213.5,'s03', R),
 ("Yafoy t'es encore un combat",    213.5,216.0,'s04', R),
 ("Yafoy t'es encore la flamme",    216.0,219.0,'s05', R),
 ("Yafoy t'es encore là, comme ça", 219.0,223.0,'s06', R),
 ("Wolof TechStein beat wê !",      223.0,226.0,'s01', R),
 ("Wolof TechStein beat wê...",     226.0,235.0,'s01', False),
 ("(Yafoy... t'es encore...)",      235.0,240.0,'s02', False),
]
# fonds par fenêtre (slot visible même sans texte)
BACKS = []
prev_end = 0.0
for txt,t0,t1,slot,gold in LINES:
    if t0 > prev_end:
        BACKS.append((prev_end, t0, None))   # géré ci-dessous
    BACKS.append((t0,t1,slot)); prev_end = t1
# instrumental : intro 0-4 (s00), inter-couplets -> garder slot précédent, solo 168.5-210 -> s31/s32/s33
def background_at(t):
    if t < 4.0: return 's00'
    if 168.5 <= t < 182.5: return 's31'
    if 182.5 <= t < 196.5: return 's32'
    if 196.5 <= t < 210.0: return 's33'
    if t >= ENDCARD_T: return 's34'
    last = 's00'
    for txt,t0,t1,slot,g in LINES:
        if t >= t0: last = slot
        if t < t0: break
    return last
