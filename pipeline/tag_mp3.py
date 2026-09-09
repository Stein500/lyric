import re
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TPE2, TPUB, TCOM, TCON, TDRC, TXXX, USLT, ID3NoHeaderError
MP3 = "livrables/Yafoy t'es encore là - Daïsky (Master).mp3"
# paroles nettoyées des timestamps
raw = open('yafoy.txt', encoding='utf-8').read()
lines = []
for l in raw.splitlines():
    if re.match(r'^\[.*\]$', l.strip()):
        lines.append(l.strip()); continue
    l2 = re.sub(r'\s*-?\d+:\d+(?:\.\d+)?(?:\s*-\s*\d+:\d+(?:\.\d+)?)?\s*$', '', l).rstrip()
    lines.append(l2)
# retirer le bloc de prod à la fin (après la dernière ligne outro)
txt = '\n'.join(lines)
txt = txt.split("Rock'n'Roll / Hard Rock. Tempo")[0].rstrip()
try: tags = ID3(MP3)
except ID3NoHeaderError: tags = ID3()
tags.delall('APIC')
tags.add(TIT2(encoding=3, text="Yafoy t'es encore là"))
tags.add(TPE1(encoding=3, text="Daïsky"))
tags.add(TALB(encoding=3, text="TechStein Prod"))
tags.add(TPE2(encoding=3, text="Daïsky Prod"))
tags.add(TPUB(encoding=3, text="TechStein / Daïsky Prod"))
tags.add(TCOM(encoding=3, text="TechStein · Daïsky"))
tags.add(TCON(encoding=3, text="Rock / Hard Rock / Afro-Rock"))
tags.add(TDRC(encoding=3, text="2026"))
tags.add(TXXX(encoding=3, desc="contact", text="Tel: 2290161162408 / 2290149114951"))
tags.add(TXXX(encoding=3, desc="email", text="daiskypro@proton.me · daiskyproduction@gmail.com · techsteinsecureway@gmail.com"))
tags.add(TXXX(encoding=3, desc="producer", text="TechStein"))
tags.add(TXXX(encoding=3, desc="label", text="Daïsky Prod"))
tags.add(USLT(encoding=3, lang='fra', desc='', text=txt))
tags.save(MP3, v2_version=4)
print('tags OK —', len(tags.keys()), 'frames. APIC: en attente de la cover (prochain tour).')
