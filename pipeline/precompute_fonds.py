import sys, os
from PIL import Image
fmt = sys.argv[1]  # portrait|landscape
W, H = (1080, 1920) if fmt == "portrait" else (1920, 1080)
CW, CH = int(W*1.1), int(H*1.1)
os.makedirs(f"work/fonds_{fmt}", exist_ok=True)
slots = ["s00_intro","s01_tag_intro","s02_africains","s03_blanc_coeur","s04_on_avance","s05_tag_cri1",
 "s06_epoque","s07_envahisseurs","s08_pleure","s09_renaitre","s10_oublions","s11_debout","s12_reines",
 "s13_ancetres","s14_tag_cri2","s15_arretons","s16_racines","s17_bamako","s18_accepte_toi","s19_traverse","s20_endcard"]
for i, s in enumerate(slots):
    im = Image.open(f"assets/raw/{fmt}/{s}.png").convert("RGB")
    aw, ah = im.size
    sc = max(CW/aw, CH/ah)
    im = im.resize((int(aw*sc), int(ah*sc)), Image.LANCZOS)
    aw, ah = im.size
    im = im.crop(((aw-CW)//2, (ah-CH)//2, (aw-CW)//2+CW, (ah-CH)//2+CH))
    im.save(f"work/fonds_{fmt}/f{i:02d}.jpg", quality=92)
print("fonds", fmt, "OK")
