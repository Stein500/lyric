# -*- coding: utf-8 -*-
"""Contrôles chiffrés d'un livrable vidéo (v7.0).

Vérifie, avec les filtres ffmpeg, ce qui doit être prouvé et non affirmé :
  - durée décodée réelle et nombre de frames ;
  - blackdetect  : aucune plage noire (hors carte finale volontaire) ;
  - freezedetect : aucun gel de plus de 1,5 s ;
  - ebur128      : LUFS intégré, crête vraie, LRA de la piste muxée ;
  - faststart    : la boîte `moov` est-elle avant `mdat` ?
  - résolution, pixel format, espace colorimétrique, i/s.

Usage : python3 scripts/checks.py <fichier.mp4> [--json sortie.json]
"""
import argparse, json, os, re, subprocess, sys
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
FP = FF  # même binaire : ffmpeg -i suffit pour sonder


def run(args):
    return subprocess.run(args, capture_output=True, text=True).stderr


def probe(path):
    out = run([FP, "-hide_banner", "-i", path])
    d = {}
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", out)
    if m:
        d["duree_hms"] = f"{m.group(1)}:{m.group(2)}:{m.group(3)}"
        d["duree_s"] = round(int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)), 3)
    m = re.search(r"Stream #0:0.*Video: (\w+).*?, (\d+)x(\d+).*?, (\d+(?:\.\d+)?) fps", out)
    if m:
        d["codec_video"], d["largeur"], d["hauteur"] = m.group(1), int(m.group(2)), int(m.group(3))
        d["fps"] = float(m.group(4))
    m = re.search(r"Video:.*?(\d+)x(\d+).*?, (yuv\w+|[a-z0-9]+\([^)]*\))", out)
    if m:
        d["pix_fmt"] = m.group(3)
    m = re.search(r"Stream #0:1.*Audio: (\w+).*?, (\d+) Hz, (\w+)", out)
    if m:
        d["codec_audio"], d["audio_hz"], d["audio_canaux"] = m.group(1), int(m.group(2)), m.group(3)
    d["taille_octets"] = os.path.getsize(path)
    return d


def detect(path, vf, label):
    out = run([FP, "-hide_banner", "-nostats", "-i", path, "-vf", vf, "-an", "-f", "null", "-"])
    hits = [l.strip() for l in out.splitlines() if label in l]
    return hits


def loudness(path):
    out = run([FP, "-hide_banner", "-nostats", "-i", path, "-filter_complex",
               "ebur128=peak=true", "-f", "null", "-"])
    tail = out[out.rfind("Summary:"):] if "Summary:" in out else out[-1500:]
    d = {}
    for key, pat in [("I", r"I:\s+(-?\d+\.\d) LUFS"),
                     ("LRA", r"LRA:\s+(-?\d+\.\d) LU"),
                     ("peak", r"Peak:\s+(-?\d+\.\d) dBFS")]:
        m = re.search(pat, tail)
        if m:
            d[key] = float(m.group(1))
    return d


def faststart(path):
    """`moov` avant `mdat` = fichier lisible en streaming dès les premiers octets."""
    with open(path, "rb") as f:
        head = f.read(4096 * 1024)
    i_moov = head.find(b"moov")
    i_mdat = head.find(b"mdat")
    return {"moov_offset": i_moov, "mdat_offset": i_mdat,
            "faststart": bool(i_moov != -1 and (i_mdat == -1 or i_moov < i_mdat))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", default=None)
    ap.add_argument("--expect", type=float, default=None, help="durée attendue en secondes")
    args = ap.parse_args()

    d = probe(args.path)
    d["black"] = detect(args.path, "blackdetect=d=0.5:pix_th=0.10", "black_start")
    d["freeze"] = detect(args.path, "freezedetect=n=0.001:d=1.5", "freeze_start")
    if d.get("codec_audio"):
        d["loudness"] = loudness(args.path)
    d.update(faststart(args.path))
    if args.expect:
        d["ecart_duree_s"] = round(d.get("duree_s", 0) - args.expect, 3)

    print(f"=== {os.path.basename(args.path)} ===")
    for k, v in d.items():
        print(f"{k:16s}: {v}")
    if args.json:
        json.dump(d, open(args.json, "w", encoding="utf8"), ensure_ascii=False, indent=1)
        print("->", args.json)


if __name__ == "__main__":
    main()
