#!/usr/bin/env python3
"""
🎵 Daïsky — « I'm Not Afraid » — MP3 Tagger v3
- Removes ALL Suno provenance tags (WOAS, TXXX:comment, GEOB C2PA).
- Adds a TechStein producer credit tag.
- Embeds lyrics (USLT), cover art (APIC), and standard metadata.
"""

import os, sys
from mutagen.mp3 import MP3
from mutagen.id3 import (
    ID3, TIT2, TPE1, TALB, TCON, TDRC, COMM, USLT, APIC, TXXX,
)

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MP3_PATH = os.path.join(BASE, "not afraid.mp3")
COVER_PATH = os.path.join(BASE, "production", "images", "cover", "cover_youtube.jpg")

LYRICS = """🔥 NOUVEAU SON 🔥
Daïsky
I'M NOT AFRAID
[Prod. TechStein]
👆 ABONNE-TOI — LIKE — COMMENTE 👆
Yeah...
Je n'ai plus peur...
(I'm not afraid anymore)
To stand up → Se lever
To break the chains → Briser les chaînes
I'm not afraid
(Je n'ai pas peur)
I'm not afraid
To rise again through the pain
(Me relever malgré la douleur)
WOLOF TECHSTEIN BEAT WÊ! 🔥
WOLOF TECHSTEIN
BEAT WÊ! 🔥
WOLOF ❖ TECHSTEIN ❖ BEAT ❖ WÊ! ⚡
J'ai touché le fond
J'ai vu le vide en face
Les doutes m'ont bouffé
J'ai perdu ma trace
Mais dans le noir
j'ai trouvé une ✦ flamme
Petite mais brûlante
elle a ravivé mon âme
On m'a dit "t'y arriveras pas"
(They said you won't make it)
Mais j'ai transformé leurs mots
en carburant, en vérité
Chaque chute m'a forgé
(Fall forged me)
Chaque larme m'a lavé
(Tears cleansed me)
Je marche sur l'eau
(Now I walk on water)
J'ai plus peur de me noyer
(Not afraid to drown)
I've been down, I've been low
(J'ai été au fond)
But I'm ready, I'm ready to go
(Mais je suis prêt)
I've been broken, I've been scarred
(J'ai été brisé)
But I'm rising, I'm reaching the stars
(Mais je m'élève)
I'm not afraid of the fall
(Je n'ai pas peur de tomber)
I'm not afraid of it all
(Je n'ai peur de rien)
I've survived the worst of me
(J'ai survécu au pire de moi-même)
Now I'm finally free
(Maintenant, je suis enfin libre)
I'M NOT AFRAID !!!
(Je n'ai pas peur)
I'M NOT AFRAID !!!
To rise again through the pain
Renaître à travers la douleur
WOLOF ❖ TECHSTEIN ❖ BEAT ❖ WÊ!
🔥 ⚡ 🔥 ⚡ 🔥
WOLOF TECHSTEIN BEAT WÊ!
I'm not afraid...
(Je n'ai plus peur)
✧ ✧ ✧
Daïsky — I'm Not Afraid
[Prod. TechStein]
🔔 ABONNE-TOI  ❤️ LIKE  💬 COMMENTE
#ImaNotAfraid #Daïsky #TechStein #MboaZick"""


def tag_mp3():
    if not os.path.exists(MP3_PATH):
        print(f"❌ MP3 introuvable: {MP3_PATH}")
        sys.exit(1)
    if not os.path.exists(COVER_PATH):
        print(f"❌ Cover introuvable: {COVER_PATH}")
        sys.exit(1)

    print(f"🎵 Tagging: {MP3_PATH}")
    audio = MP3(MP3_PATH)

    # Wipe ALL existing ID3 tags (clean slate, NO Suno preservation)
    audio.tags = ID3()

    # Standard metadata
    audio.tags.add(TIT2(encoding=3, text="I'm Not Afraid"))
    audio.tags.add(TPE1(encoding=3, text="Daïsky"))
    audio.tags.add(TALB(encoding=3, text="Single"))
    audio.tags.add(TCON(encoding=3, text="Rap / Hip-Hop"))
    audio.tags.add(TDRC(encoding=3, text="2026"))
    audio.tags.add(COMM(encoding=3, lang="eng", desc="", text="Prod. TechStein — Wolof TechStein beat wê !"))

    # TechStein producer credit (replaces Suno tags)
    audio.tags.add(TXXX(encoding=3, desc="Producer", text="TechStein"))
    audio.tags.add(TXXX(encoding=3, desc="Producer Tag", text="Wolof TechStein beat wê !"))
    audio.tags.add(TXXX(encoding=3, desc="Producer Contact", text="@TechStein"))
    audio.tags.add(TXXX(encoding=3, desc="Production", text="TechStein Production — Wolof TechStein beat"))

    # Lyrics (USLT)
    audio.tags.add(USLT(encoding=3, lang="eng", desc="", text=LYRICS))

    # Cover (only ONE APIC)
    with open(COVER_PATH, "rb") as f:
        cover_data = f.read()
    audio.tags.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover — Daïsky Production", data=cover_data))

    audio.save()
    print()
    print(f"✅ MP3 tagged successfully!")
    print(f"   Title          : I'm Not Afraid")
    print(f"   Artist         : Daïsky")
    print(f"   Album          : Single")
    print(f"   Genre          : Rap / Hip-Hop")
    print(f"   Year           : 2026")
    print(f"   Comment        : Prod. TechStein — Wolof TechStein beat wê !")
    print(f"   Producer TXXXs : TechStein (Producer + Tag + Contact + Production)")
    print(f"   Cover          : {os.path.basename(COVER_PATH)} ({len(cover_data)} bytes)")
    print(f"   Lyrics         : {len(LYRICS)} characters")
    print(f"   ❌ NO Suno tags preserved")


if __name__ == "__main__":
    tag_mp3()
