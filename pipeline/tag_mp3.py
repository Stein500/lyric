from mutagen.id3 import ID3, TIT2, TPE1, TALB, TPE2, TPUB, TCOM, TCON, TDRC, TXXX, USLT
from mutagen.mp3 import MP3
import re, sys
p = sys.argv[1] if len(sys.argv) > 1 else "work/master_guerrier.mp3"
tags = ID3()
tags.add(TIT2(encoding=3, text="Guerrier"))
tags.add(TPE1(encoding=3, text="Daïsky"))
tags.add(TALB(encoding=3, text="TechStein Prod"))
tags.add(TPE2(encoding=3, text="Daïsky Prod"))
tags.add(TPUB(encoding=3, text="TechStein / Daïsky Prod"))
tags.add(TCOM(encoding=3, text="TechStein · Daïsky"))
tags.add(TCON(encoding=3, text="Afro-Rock / World"))
tags.add(TDRC(encoding=3, text="2026"))
tags.add(TXXX(encoding=3, desc="contact", text="Tel: 2290161162408 / 2290149114951"))
tags.add(TXXX(encoding=3, desc="email", text="daiskypro@proton.me / daiskyproduction@gmail.com / techsteinsecureway@gmail.com"))
tags.add(TXXX(encoding=3, desc="producer", text="TechStein"))
tags.add(TXXX(encoding=3, desc="label", text="Daïsky Prod"))
lyrics = []
for ln in open("guerrier.txt", encoding="utf-8"):
    m = re.match(r"\[[\d:.]+\](.*)", ln.strip())
    if m:
        t = m.group(1).replace("(fort)","").replace("(cri de guerre)","").replace("(crié)","").strip()
        lyrics.append(t)
tags.add(USLT(encoding=3, lang="fra", desc="Guerrier", text="\n".join(lyrics)))
tags.save(p, v2_version=4)
print("tags OK:", [k for k in MP3(p).tags.keys()])
