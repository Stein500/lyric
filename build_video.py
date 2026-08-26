#!/usr/bin/env python3
"""
⚡ Lightning Is My Name — Daïsky — build v4 FINALE
- Lyrics avec (start, end, text, style, fr) hardcodés — pas de calcul automatique
- Segments vidéo = liste (start, end, img_path) alignée sur les coupures précises
- Badge "Daïsky Prod" overlay bas-gauche, static
- 2 exports : 9:16 (natif portrait) et 16:9 (letterbox-contain)
- Vérification post-rendu : durée exacte 169.48s, 0 trou noir > 300ms
"""

import os, sys, subprocess, json, math, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

ROOT = Path("/home/user/lyric")
AUDIO = ROOT / "Lightning_is_my_name_Daïsky.m4a"
ASSETS_P = ROOT / "assets/raw/portrait"
LIVR = ROOT / "livrables"
WORK = ROOT / "work"
for d in (LIVR, WORK, WORK/"clips", WORK/"prep", WORK/"subs"):
    d.mkdir(parents=True, exist_ok=True)

# FFMPEG — découvert dynamiquement depuis imageio_ffmpeg (fonctionne en venv comme en système)
try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    # fallback : utiliser le ffmpeg de PATH
    FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
    print(f"⚠️ imageio_ffmpeg absent, fallback ffmpeg PATH : {FFMPEG}")
DURATION = 169.486

# ----------------------------------------------------------------------
# 1. LYRICS v4 — tous hardcodés (start, end) en secondes
# style: verse / hook / hook_final / verse_es / wolof / bridge
# ----------------------------------------------------------------------
LYRICS = [
    # Intro (0.0 - 3.5)
    (0.0,  3.5,  "",  "intro", ""),
    # HOOK 1 (3.5 - 35)
    (3.5,  7.5,  "Bottom of the map, silver spoon in the dark", "hook", "En bas d'la carte, cuillère d'argent dans l'noir"),
    (7.5, 11.5,  "Writing my name in the clouds before they hit the spark", "hook", "J'écris mon nom dans les nuages avant l'étincelle"),
    (11.5, 15.5, "You saw the flash, never heard the battle cry before", "hook", "T'as vu l'éclair, jamais entendu le cri d'guerre avant"),
    (15.5, 19.5, "I made the thunder wait 'til I walked through the door", "hook", "J'ai fait attendre le tonnerre avant d'passer la porte"),
    (19.5, 23.5, "They selling tickets to the come-up, I don't wait in line", "hook", "Ils vendent des billets pour l'ascension, j'fais pas la queue"),
    (23.5, 27.5, "Arena full and half of y'all was doubting I'd be fine", "hook", "L'arène est pleine et la moitié d'entre vous doutait que j'tienne"),
    (27.5, 31.5, "It's looking dark, but the dark's where the light gets to define", "hook", "Ça a l'air sombre, mais l'sombre c'est là où la lumière s'définit"),
    (31.5, 35.0, "Lightning is my name, I been electric my whole life", "hook", "Lightning est mon nom, j'suis électrique toute ma vie"),
    # VERSE 1 (35 - 71)
    (35.0, 39.0, "Midnight writing sessions, scars up on the page", "verse", "Sessions d'écriture à minuit, cicatrices sur la page"),
    (39.0, 43.0, "Grinding 'til the vision's sharper than the blade they tried to cage", "verse", "J'grinde jusqu'à c'qu'la vision soit plus nette que la lame qu'ils ont voulu encaisser"),
    (43.0, 47.0, "They gave me hand-me-downs, I made a legacy out of rage", "verse", "Ils m'ont filé des trucs d'occasion, j'en ai fait un héritage de rage"),
    (47.0, 51.0, "You set the clock, I kept the precision when they turned the page", "verse", "T'as réglé l'horloge, j'ai gardé la précision quand ils ont tourné la page"),
    (51.0, 55.0, "Pressure on the chest, I don't fold when the concrete cracks", "verse", "Pression sur la poitrine, j'plie pas quand le béton se fend"),
    (55.0, 59.0, "Every scar a blueprint for the way the building cracks", "verse", "Chaque cicatrice un plan sur la façon dont l'bâtiment se fend"),
    (59.0, 63.0, "They told me wait my turn, I was ready when the curtain called", "verse", "Ils m'ont dit attends ton tour, j'étais prêt quand l'rideau s'est levé"),
    (63.0, 67.0, "Legends don't ask permission when the storm's about to fall", "verse", "Les légendes n'demandent pas la permission quand l'tombe est sur le point d'tomber"),
    (67.0, 71.0, "If the sky's the limit then I'm aiming past the ceiling, yeah", "verse", "Si l'ciel est la limite alors j'vise au-delà du plafond, ouais"),
    # HOOK 2 / pont 71-83
    (71.0, 75.0, "Bottom of the map, silver spoon in the dark", "hook", "En bas d'la carte, cuillère d'argent dans l'noir"),
    (75.0, 79.0, "Writing my name in the clouds before they hit the spark", "hook", "J'écris mon nom dans les nuages avant l'étincelle"),
    (79.0, 83.0, "You saw the flash, never heard the battle cry before", "hook", "T'as vu l'éclair, jamais entendu le cri d'guerre avant"),
    # VERSE 2 ESPAGNOL (83 - 110)
    (83.0, 86.5,  "Silencio cuando entro, el hambre está tatuada", "verse_es", "Silence quand j'entre, la faim est tatouée"),
    (86.5, 90.0,  "Construí el imperio donde el miedo era morada", "verse_es", "J'ai construit l'empire là où la peur habitait"),
    (90.0, 93.5,  "La escuela fue la sombra, el dolor fue el combustible", "verse_es", "L'école était l'ombre, la douleur était l'carburant"),
    (93.5, 97.0,  "Cada golpe en el pecho me hizo menos vulnerable", "verse_es", "Chaque coup dans la poitrine m'a rendu moins vulnérable"),
    (97.0, 100.5, "No pido permiso si el micrófono me llama", "verse_es", "J'demande pas la permission si l'micro m'appelle"),
    (100.5,104.0, "Enciendo el cuarto cuando toco la tarima", "verse_es", "J'allume la pièce quand j'touche la scène"),
    (104.0,107.0, "Esto no es suerte, esto es código que escribo", "verse_es", "C'est pas d'la chance, c'est du code que j'écris"),
    (107.0,110.0, "En cada verso va un decreto de mi estirpe", "verse_es", "Dans chaque vers va un décret de ma lignée"),
    # BRIDGE (110 - 122)
    (110.0,114.0, "They said I'm standing on the edge and I should turn around", "bridge", "Ils ont dit j'suis au bord et que j'devrais faire demi-tour"),
    (114.0,118.0, "Crown so heavy, but I wear it like I'm heaven-bound", "bridge", "Couronne si lourde, mais j'la porte comme si j'allais au ciel"),
    (118.0,122.0, "Hold on through the dark, even when the night gets loud", "bridge", "Tiens bon dans l'sombre, même quand la nuit fait du bruit"),
    # Lien bridge 122-124 (violon)
    (122.0,124.0, "", "bridge", ""),
    # HOOK repris 124-132
    (124.0,128.0, "Lightning don't glow 'til the darkest night comes out", "hook", "L'éclair brille pas qu'à la nuit la plus sombre"),
    (128.0,132.0, "So when the lights go low, yeah, you know who's coming 'round", "hook", "Donc quand les lumières baissent, ouais, tu sais qui arrive"),
    # VERSE 3 RAPIDE (132 - 149)
    (132.0,135.5, "Pointing at the sky, every finger like a javelin", "verse", "J'pointe le ciel, chaque doigt comme un javelot"),
    (135.5,139.0, "Bets were on the floor, every hater said I'd cave in", "verse", "Les paris étaient par terre, chaque haineux disait qu'j'céderais"),
    (139.0,142.5, "Ruins to the castle, now the castle's where I'm standing in", "verse", "Des ruines au château, maintenant l'château c'est là où j'me tiens"),
    (142.5,145.5, "Betting on myself was the only win I needed in", "verse", "Parier sur moi-même c'était la seule victoire dont j'avais besoin"),
    (145.5,149.0, "Hardware for the bars, software for the soul within", "verse", "Hardware pour les barres, software pour l'âme dedans"),
    # HOOK FINAL (149 - 156)
    (149.0,152.0, "Lightning never lies, you can see it when the storm hits", "hook_final", "L'éclair ne ment jamais, tu peux l'voir quand l'tombe arrive"),
    (152.0,156.0, "Reescribiendo el código, forjado en la oscuridad", "hook_final_es", "Réécrivant le code, forgé dans l'obscurité"),
    # OUTRO (156 - fin)
    (156.0,162.0, "Wolof TechStein beat wê!", "wolof", ""),
    (162.0,169.48,"", "outro", ""),
]

# ----------------------------------------------------------------------
# 2. SEGMENTS — alignement précis image ↔ temps
# ----------------------------------------------------------------------
SEGMENTS = [
    (0.0,  3.5,  "01_anchor_cover_lightning.jpg"),                 # Intro cover
    (3.5,  7.5,  "02_bottom_dark_writing.jpg"),
    (7.5,  11.5, "03_arenas_doubts_old.jpg"),
    (11.5, 15.5, "04_midnight_grind_scars.jpg"),
    (15.5, 19.5, "05_hook_dark_but_electric.jpg"),
    (19.5, 23.5, "05_hook_dark_but_electric.jpg"),
    (23.5, 27.5, "03_arenas_doubts_old.jpg"),
    (27.5, 31.5, "05_hook_dark_but_electric.jpg"),
    (31.5, 35.0, "01_anchor_cover_lightning.jpg"),                 # hook close
    # Verse 1
    (35.0, 39.0, "04_midnight_grind_scars.jpg"),
    (39.0, 43.0, "04_midnight_grind_scars.jpg"),
    (43.0, 47.0, "27_throne_amps_cables.jpg"),
    (47.0, 51.0, "28_digital_rain_glyphs.jpg"),
    (51.0, 55.0, "24_eyes_lightning_reflection.jpg"),
    (55.0, 59.0, "13_v3_lab_hardware_neural_flash.jpg"),
    (59.0, 63.0, "29_hero_back_walk_storm.jpg"),
    (63.0, 67.0, "30_final_signature_shout.jpg"),
    (67.0, 71.0, "25_techstein_gauntlet_lightning.jpg"),
    # Hook 2 / reprise
    (71.0, 75.0, "05_hook_dark_but_electric.jpg"),
    (75.0, 79.0, "05_hook_dark_but_electric.jpg"),
    (79.0, 83.0, "22_fist_explosion_drop.jpg"),
    # Verse 2 ES
    (83.0, 86.5,  "06_verse2_silencio_hambre_imperio.jpg"),
    (86.5, 90.0,  "07_verse2_sombras_escuela_dolor.jpg"),
    (90.0, 93.5,  "07_verse2_sombras_escuela_dolor.jpg"),
    (93.5, 97.0,  "23_portonovo_street_rain.jpg"),
    (97.0, 100.5, "08_verse2_micro_enciendo_decreto.jpg"),
    (100.5,104.0, "08_verse2_micro_enciendo_decreto.jpg"),
    (104.0,107.0, "13_v3_lab_hardware_neural_flash.jpg"),
    (107.0,110.0, "25_techstein_gauntlet_lightning.jpg"),
    # Bridge
    (110.0,114.0, "09_bridge_edge_crown_violin.jpg"),
    (114.0,118.0, "19_cover_single_portrait.jpg"),
    (118.0,122.0, "10_bridge_hold_on_darkest_night.jpg"),
    (122.0,124.0, "09_bridge_edge_crown_violin.jpg"),             # violin link
    (124.0,128.0, "10_bridge_hold_on_darkest_night.jpg"),
    (128.0,132.0, "05_hook_dark_but_electric.jpg"),
    # Verse 3 rapid-fire
    (132.0,135.5, "11_anchor_animated_rapidfire.jpg"),
    (135.5,139.0, "12_v3_ruins_bets_legacy.jpg"),
    (139.0,142.5, "12_v3_ruins_bets_legacy.jpg"),
    (142.5,145.5, "29_hero_back_walk_storm.jpg"),
    (145.5,149.0, "13_v3_lab_hardware_neural_flash.jpg"),
    # Hook Final — moment clé "never lies"
    (149.0,152.0, "16_hookfinal_lightning_never_lies.jpg"),
    (152.0,156.0, "15_hookfinal_reescribiendo_codigo.jpg"),
    # Outro Wolof + fade
    (156.0,162.0, "21_wolof_sabar_percussions.jpg"),
    (162.0,169.48,"18_outro_violin_fade_wolof.jpg"),
]

# Vérification : segments doivent sommer à DURATION
total_seg = sum(e-s for s,e,_ in SEGMENTS)
assert abs(total_seg - DURATION) < 0.05, f"Segments total {total_seg} != {DURATION}"

# ----------------------------------------------------------------------
# 3. Badge Daïsky Prod
# ----------------------------------------------------------------------
def make_badge(w, h):
    """Badge PNG avec 'DAÏSKY PROD' fixe en bas-gauche, overlay."""
    scale = w / 1080.0  # référence 1080 largeur (portrait)
    badge = Image.new("RGBA", (w, h), (0,0,0,0))
    draw = ImageDraw.Draw(badge)
    pad = int(40*scale); bh = int(64*scale); font_sz = int(30*scale)
    # bande
    draw.rounded_rectangle(
        [pad, h-bh-pad, pad+int(340*scale), h-pad],
        radius=int(14*scale), fill=(0,0,0,150), outline=(77,210,255,220), width=max(2,int(3*scale))
    )
    # texte — essai de polices ; fallback défaut
    for fp in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
               "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
        if os.path.exists(fp):
            font = ImageFont.truetype(fp, font_sz); break
    else:
        font = ImageFont.load_default()
    draw.text((pad+int(20*scale), h-bh-pad+int(12*scale)),
              "⚡ DAÏSKY PROD", fill=(77,210,255,255), font=font)
    # petit éclair à droite
    draw.text((pad+int(270*scale), h-bh-pad+int(8*scale)), "⚡",
              fill=(232,163,61,255), font=font)
    return badge

# ----------------------------------------------------------------------
# 4. Préparation des frames : resize + badge + grain
# ----------------------------------------------------------------------
def prepare_frame(src_path, target_w, target_h, mode="cover"):
    """Retourne le chemin d'une frame préparée (JPG). mode=cover crop, contain=letterbox."""
    stem = Path(src_path).stem
    out = WORK/"prep"/f"{stem}_{target_w}x{target_h}_{mode}.jpg"
    if out.exists() and out.stat().st_size > 10_000:
        return out
    img = Image.open(src_path).convert("RGB")
    iw, ih = img.size
    if mode == "cover":
        # crop fill (utilisé pour le 9:16 natif)
        scale = max(target_w/iw, target_h/ih)
        nw, nh = int(iw*scale), int(ih*scale)
        img = img.resize((nw, nh), Image.LANCZOS)
        left = (nw - target_w)//2; top = (nh - target_h)//2
        img = img.crop((left, top, left+target_w, top+target_h))
    else:  # contain (letterbox)
        scale = min(target_w/iw, target_h/ih)
        nw, nh = int(iw*scale), int(ih*scale)
        bg = Image.new("RGB", (target_w, target_h), (5,6,10))  # fond noir profond
        img = img.resize((nw, nh), Image.LANCZOS)
        bg.paste(img, ((target_w-nw)//2, (target_h-nh)//2))
        img = bg
    # overlay badge
    badge = make_badge(target_w, target_h)
    img = img.convert("RGBA")
    img.alpha_composite(badge)
    img = img.convert("RGB")
    img.save(out, "JPEG", quality=92)
    return out

# ----------------------------------------------------------------------
# 5. Génération sous-titres ASS (WrapStyle=1, fade 80/120ms)
# ----------------------------------------------------------------------
def gen_ass(target_w, target_h, out_path):
    """Génère un fichier ASS avec les sous-titres EN+FR."""
    # Marges adaptées au format
    is_portrait = target_h > target_w
    if is_portrait:
        playres_x, playres_y = target_w, target_h
        fontsize_en = 54; fontsize_fr = 34
        margin_v = 340  # plus haut pour laisser place aux visuels
    else:
        playres_x, playres_y = target_w, target_h
        fontsize_en = 62; fontsize_fr = 38
        margin_v = 180
    # Polices — chercher une sans-serif
    font_name = "DejaVu Sans"
    for fp in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if not os.path.exists(fp): font_name = "Arial"

    lines = []
    lines.append("[Script Info]")
    lines.append("Title: Lightning Is My Name - Daïsky - Lyrics v4")
    lines.append("ScriptType: v4.00+")
    lines.append("WrapStyle: 1")
    lines.append(f"PlayResX: {playres_x}")
    lines.append(f"PlayResY: {playres_y}")
    lines.append("ScaledBorderAndShadow: yes")
    lines.append("")
    lines.append("[V4+ Styles]")
    lines.append("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding")
    # Style par type
    # Couleurs en BGR hex &AA BB GG RR
    CYAN  = "&H00FFD24D"   # #4DD2FF
    WHITE = "&H00FFFFFF"
    AMBER = "&H003DA3E8"   # #E8A33D
    BLACK_SHADOW = "&H80000000"
    OUTLINE = "&H00000000"

    def add_style(name, sz, color, bold=1, italic=0):
        lines.append(f"Style: {name},{font_name},{sz},{color},&H000000FF,{OUTLINE},{BLACK_SHADOW},{bold},{italic},0,0,100,100,0,0,1,3,2,2,60,60,{margin_v},1")

    add_style("hook",       fontsize_en, CYAN, bold=1)
    add_style("hook_final", int(fontsize_en*1.1), AMBER, bold=1)
    add_style("hook_final_es", int(fontsize_en*1.0), AMBER, bold=1, italic=1)
    add_style("verse",      fontsize_en, WHITE, bold=1)
    add_style("verse_es",   fontsize_en, WHITE, bold=1, italic=1)
    add_style("bridge",     fontsize_en-4, CYAN, bold=0, italic=1)
    add_style("wolof",      int(fontsize_en*1.1), AMBER, bold=1)
    # Sous-titres FR = plus petit, blanc, en dessous
    add_style("fr",         fontsize_fr, "&H00E0F0FF", bold=0, italic=1)

    lines.append("")
    lines.append("[Events]")
    lines.append("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")

    def t2s(ts):
        h = int(ts//3600); m = int((ts%3600)//60); s = ts%60
        return f"{h}:{m:02d}:{s:05.2f}"

    # Offset pour position FR sous la ligne EN
    # Pour chaque ligne non vide, on met EN + FR (décalée de margin_v+40)
    fr_margin_offset = int(margin_v - (fontsize_en + 10) - (fontsize_fr//2))
    for (s,e,text,style,fr) in LYRICS:
        if not text.strip():
            continue
        fade_in, fade_out = 8, 12  # en centièmes de seconde → 80ms / 120ms
        en_text = text.replace(",", " " if False else ",")
        # fades via \fad(fade_in_cs, fade_out_cs)
        fx = f"\\fad({fade_in*10},{fade_out*10})"
        lines.append(f"Dialogue: 0,{t2s(s)},{t2s(e)},{style},,0,0,{margin_v},,{{{fx}}}{en_text}")
        if fr and style != "wolof":
            lines.append(f"Dialogue: 1,{t2s(s)},{t2s(e)},fr,,0,0,{fr_margin_offset},,{{{fx}}}{fr}")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path

# ----------------------------------------------------------------------
# 6. Montage : concat demuxer + burn ass + audio
# ----------------------------------------------------------------------
def render(format_name, target_w, target_h):
    print(f"\n{'='*60}\n🎬 RENDU {format_name} {target_w}x{target_h}\n{'='*60}")
    mode = "cover" if target_h > target_w else "contain"
    # préparer toutes les frames
    seg_frames = []
    for s,e,img in SEGMENTS:
        p = prepare_frame(str(ASSETS_P/img), target_w, target_h, mode)
        seg_frames.append((s,e,str(p)))
    # clips silencieux image→vidéo
    clip_dir = WORK/"clips"
    clips = []
    for i,(s,e,fp) in enumerate(seg_frames):
        dur = e - s
        out_c = clip_dir/f"c4_{format_name}_{i:03d}.mp4"
        if not (out_c.exists() and out_c.stat().st_size > 5000):
            cmd = [FFMPEG, "-y", "-loglevel", "error",
                   "-loop", "1", "-i", fp,
                   "-f", "lavfi", "-t", f"{dur}", "-i", f"anullsrc=r=44100:cl=stereo",
                   "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                   "-t", f"{dur}", "-pix_fmt", "yuv420p",
                   "-vf", f"scale={target_w}:{target_h}:force_original_aspect_ratio=disable,setsar=1,fps=24",
                   "-c:a", "aac", "-b:a", "128k", "-shortest",
                   "-movflags", "+faststart",
                   str(out_c)]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0:
                print(f"ERREUR clip {i}:", r.stderr[-500:]); sys.exit(1)
        clips.append(out_c)
    # concat list
    listf = WORK/f"concat4_{format_name}.txt"
    listf.write_text("\n".join(f"file '{c}'" for c in clips), encoding="utf-8")
    concat_out = WORK/f"concat4_{format_name}.mp4"
    cmd = [FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
           "-i", str(listf), "-c", "copy", str(concat_out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("ERREUR concat:", r.stderr[-800:]); sys.exit(1)
    # ASS
    ass_p = gen_ass(target_w, target_h, WORK/"subs"/f"subs4_{format_name}.ass")
    final = LIVR/f"Daïsky - Lightning Is My Name (Lyrics {format_name.replace('16x9_YT','16x9').replace('9x16','9x16')}).mp4"
    # filtre subtitles avec chemin échappé
    ass_path_esc = str(ass_p).replace("\\","\\\\").replace(":","\\:").replace("'","\\'")
    vf = f"ass='{ass_path_esc}'"
    cmd = [FFMPEG, "-y", "-loglevel", "error",
           "-i", str(concat_out), "-i", str(AUDIO),
           "-map", "0:v:0", "-map", "1:a:0",
           "-c:v", "libx264", "-preset", "medium", "-crf", "22",
           "-pix_fmt", "yuv420p", "-r", "24",
           "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
           "-af", f"afade=t=in:st=0:d=0.3,afade=t=out:st={DURATION-3}:d=3",
           "-t", f"{DURATION}",
           "-vf", vf,
           "-movflags", "+faststart",
           "-shortest",
           str(final)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("ERREUR burn+audio:", r.stderr[-1500:]); sys.exit(1)
    print(f"✅ {final}  ({final.stat().st_size/1e6:.1f} MB)")
    return final

# ----------------------------------------------------------------------
# 7. Vérification post-rendu
# ----------------------------------------------------------------------
def verify(path):
    print(f"\n🔍 Vérification {path.name}")
    # durée
    r = subprocess.run([FFMPEG, "-i", str(path), "-f", "null", "-"],
                       capture_output=True, text=True, timeout=60)
    # ffmpeg écrit dans stderr
    m = None
    import re
    for line in r.stderr.splitlines():
        if "time=" in line:
            mm = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", line)
            if mm: m = (int(mm.group(1)), int(mm.group(2)), float(mm.group(3)))
    if m:
        t = m[0]*3600+m[1]*60+m[2]
        print(f"  durée: {t:.2f}s (attendu {DURATION:.2f}s) — écart {t-DURATION:+.2f}s")
        assert abs(t - DURATION) < 0.3, f"Durée incorrecte: {t} vs {DURATION}"
    # blackdetect
    cmd = [FFMPEG, "-i", str(path), "-vf", "blackdetect=d=0.3:pix_th=0.10",
           "-an", "-f", "null", "-"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    blacks = [l for l in r.stderr.splitlines() if "black_start" in l]
    print(f"  black gaps >300ms: {len(blacks)}")
    for b in blacks: print("   ", b.strip())
    assert len(blacks) == 0, f"{len(blacks)} trou(s) noir(s) détecté(s)"
    print("  ✅ OK")

def extract_frames(path, ts_list, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    for ts in ts_list:
        out = out_dir/f"t{int(ts)}.jpg"
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-ss", f"{ts}",
                        "-i", str(path), "-frames:v", "1", "-q:v", "2", str(out)],
                       check=True)
    print(f"  📸 {len(ts_list)} frames extraites dans {out_dir}")

# ----------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------
if __name__ == "__main__":
    out9 = render("9x16", 1080, 1920)
    out16 = render("16x9_YT", 1920, 1080)
    verify(out9); verify(out16)
    extract_frames(out9, [27, 66, 150, 165], WORK/"checks_v4")
    print("\n" + "="*60)
    print("🏁 RENDUS v4 TERMINÉS — tous vérifiés")
    print("="*60)
