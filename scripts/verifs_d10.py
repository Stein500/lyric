"""§D.10 — Vérifications du clip 9:16 'Nan yi a ga djin wê'."""
import json, subprocess, re, sys
FF = "work/ffmpeg"
MP4 = "livrables/Nan yi a ga djin wê - clip 9x16.mp4"

def run(*a):
    return subprocess.run([FF] + list(a), capture_output=True, text=True).stderr

# durée + streams
info = run("-i", MP4)
dur = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", info)
d = int(dur.group(1)) * 3600 + int(dur.group(2)) * 60 + float(dur.group(3))
print(f"durée: {d:.2f} s (attendu ~173.84)")
print("streams:", "video" if "Video: h264" in info else "??", "|", re.findall(r"Audio: [^\n,]+", info))
print("1080x1920" if "1080x1920" in info else "RESOLUTION ??")

# blackdetect : seul le fade final
bd = run("-i", MP4, "-vf", "blackdetect=d=0.5:pix_th=0.10", "-an", "-f", "null", "-")
blacks = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", bd)
print("blackdetect:", blacks, "→ OK si uniquement fin (>170 s)")

# freezedetect
fd = run("-i", MP4, "-vf", "freezedetect=n=0.003:d=2", "-an", "-f", "null", "-")
frz = re.findall(r"freeze_start", fd)
print("freezedetect:", len(frz), "freeze(s) (0 attendu)")

# loudness du mux final
lz = run("-i", MP4, "-af", "loudnorm=print_format=json", "-f", "null", "-")
m = re.search(r'"input_i" : "(-?[\d.]+)".*"input_tp" : "(-?[\d.]+)"', lz, re.S)
print("LUFS/TP mux:", m.groups() if m else "?")
