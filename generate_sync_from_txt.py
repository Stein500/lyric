import json

synced_lyrics = [
    # Intro
    {"text": "[INTRO - Spoken, piano sombre, violon]", "time": 0.0, "isSection": True},
    {"text": "Wolof TechStein beat wê...", "time": 0.0, "isSection": False},
    {"text": "Yeah... They thought I was done...", "time": 10.0, "isSection": False},
    
    # Chorus 1
    {"text": "[REFRAIN - Punchy, batterie lourde, cordes]", "time": 15.0, "isSection": True},
    {"text": "I'm not dying, I'm not fading", "time": 15.0, "isSection": False},
    {"text": "I'm rising from the ashes, I'm creating", "time": 18.0, "isSection": False},
    {"text": "I'm not dying, I'm not breaking", "time": 24.0, "isSection": False},
    {"text": "Every scar is proof of my awakening", "time": 28.0, "isSection": False},
    {"text": "Wolof TechStein beat wê!", "time": 32.0, "isSection": False},
    
    # Verse 1
    {"text": "[COUPLET1 - Flow rapide, agressif]", "time": 35.0, "isSection": True},
    {"text": "Ils m'ont vu au fond, ils ont cru que c'était fini", "time": 35.0, "isSection": False},
    {"text": "Que j'allais me taire, que j'allais plier, que j'allais perdre la vie", "time": 38.0, "isSection": False},
    {"text": "Mais dans le noir, j'ai trouvé une lumière", "time": 42.0, "isSection": False},
    {"text": "Chaque coup m'a rendu plus fort, plus fier", "time": 43.0, "isSection": False},
    {"text": "J'ai pleuré, j'ai crié, j'ai frappé les murs", "time": 46.0, "isSection": False},
    {"text": "Mais j'ai gardé l'espoir, même dans l'ordure", "time": 48.0, "isSection": False},
    {"text": "Ils voulaient ma fin, ils voulaient mon abandon", "time": 51.0, "isSection": False},
    {"text": "Mais je suis un phénix, je renais de mes cendres, c'est ma saison", "time": 53.0, "isSection": False},
    
    # Pre-Chorus 1
    {"text": "[PRÉ-REFRAIN - Montée en puissance, violon]", "time": 57.0, "isSection": True},
    {"text": "You thought I'd break, you thought I'd fall", "time": 57.0, "isSection": False},
    {"text": "But I'm standing taller, I'm standing tall", "time": 60.0, "isSection": False},
    {"text": "The fire inside will never die", "time": 65.0, "isSection": False},
    {"text": "Watch me rise, watch me fly", "time": 69.0, "isSection": False},
    
    # Chorus 2
    {"text": "[REFRAIN - Punchy, batterie lourde]", "time": 72.0, "isSection": True},
    {"text": "I'm not dying, I'm not fading", "time": 72.0, "isSection": False},
    {"text": "I'm rising from the ashes, I'm creating", "time": 75.0, "isSection": False},
    {"text": "I'm not dying, I'm not breaking", "time": 81.0, "isSection": False},
    {"text": "Every scar is proof of my awakening", "time": 85.0, "isSection": False},
    {"text": "Wolof TechStein beat wê!", "time": 89.0, "isSection": False},
    
    # Verse 2
    {"text": "[COUPLET2 - Flow posé, plus mélodique]", "time": 92.0, "isSection": True},
    {"text": "Chaque nuit a été une guerre, chaque jour une bataille", "time": 92.0, "isSection": False},
    {"text": "Mais j'ai tenu, j'ai serré les dents, j'ai fait mentir les failles", "time": 96.0, "isSection": False},
    {"text": "On m'a dit \"laisse tomber, tu n'y arriveras jamais\"", "time": 99.0, "isSection": False},
    {"text": "Mais j'ai transformé leurs doutes en carburant, en paix", "time": 102.0, "isSection": False},
    {"text": "Je suis pas mort, je suis pas fini", "time": 106.0, "isSection": False},
    {"text": "Je suis juste en train de renaître, de de de de de de... de de... de devenir infini", "time": 110.0, "isSection": False},
    {"text": "La douleur m'a forgé, les larmes m'ont lavé", "time": 113.0, "isSection": False},
    {"text": "Maintenant je marche sur l'eau, je suis libéré", "time": 117.0, "isSection": False},
    
    # Pre-Chorus 2
    {"text": "[PRÉ-REFRAIN - Montée en puissance, cordes]", "time": 121.0, "isSection": True},
    {"text": "You thought I'd break, you thought I'd fall", "time": 121.0, "isSection": False},
    {"text": "But I'm standing taller, I'm standing tall", "time": 125.0, "isSection": False},
    {"text": "The fire inside will never die", "time": 130.0, "isSection": False},
    {"text": "Watch me rise, watch me fly", "time": 134.0, "isSection": False},
    
    # Bridge
    {"text": "[PONT - Calme, piano seul, violon, voix posée]", "time": 137.0, "isSection": True},
    {"text": "I'm not dying, I'm just beginning", "time": 137.0, "isSection": False},
    {"text": "The end is not my story, I keep winning", "time": 140.0, "isSection": False},
    {"text": "My heart is beating, I'm still breathing", "time": 145.0, "isSection": False},
    {"text": "This life is mine, I'm not leaving", "time": 150.0, "isSection": False},
    
    # Chorus 3 (Final)
    {"text": "[REFRAIN FINAL - Explosif, batterie lourde, tutti]", "time": 152.0, "isSection": True},
    {"text": "I'm not dying, I'm not fading", "time": 152.0, "isSection": False},
    {"text": "I'm rising from the ashes, I'm creating", "time": 155.0, "isSection": False},
    {"text": "I'm not dying, I'm not breaking", "time": 161.0, "isSection": False},
    {"text": "Every scar is proof of my awakening", "time": 165.0, "isSection": False},
    {"text": "Wolof TechStein beat wê!", "time": 169.0, "isSection": False},
    
    # Outro
    {"text": "[OUTRO - Fade, piano, violon, voix soufflée]", "time": 185.0, "isSection": True},
    {"text": "Wolof TechStein beat wê...", "time": 185.0, "isSection": False},
    {"text": "(I'm not dying...)", "time": 189.0, "isSection": False}
]

# Write to synced_lyrics.json
with open("synced_lyrics.json", 'w', encoding='utf-8') as f:
    json.dump(synced_lyrics, f, indent=4, ensure_ascii=False)
print("Saved synced_lyrics.json!")

# Write to LRC format
with open("i'm not dying 1.lrc", 'w', encoding='utf-8') as f:
    f.write("[ti:I'm not dying]\n")
    f.write("[ar:Daïsky]\n")
    f.write("[al:Succeed]\n")
    f.write("[by:Daïsky]\n\n")
    for item in synced_lyrics:
        if item['isSection']:
            f.write(f"\n# {item['text']}\n")
        else:
            t = item['time']
            m = int(t // 60)
            s = int(t % 60)
            ms = int((t % 1) * 100)
            f.write(f"[{m:02d}:{s:02d}.{ms:02d}]{item['text']}\n")
print("Saved i'm not dying 1.lrc!")
