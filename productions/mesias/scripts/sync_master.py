# -*- coding: utf-8 -*-
"""Recale les 190 vers du contrat sur le MP3 maître fourni par l'artiste.

Le MP3 porte un USLT : 175 lignes horodatées, souvent découpées en fragments de
1 à 3 mots et parfois fautives (« miento » pour « gimiendo »). On ne s'en sert donc
pas comme d'une transcription : on s'en sert comme d'un jeu d'ANCRES.

  1. flux de mots horodatés du master (739 mots) ;
  2. pour chaque vers du contrat, toutes les positions candidates (2 mots exacts) ;
  3. chaîne croissante optimale (programmation dynamique) : on maximise le nombre
     de vers ancrés en respectant l'ordre du master ;
  4. les vers restants sont interpolés sur la table de correspondance
     contrat(s) -> master(s) construite par les ancres, par morceaux ;
  5. les fins se déduisent du début master du vers suivant.

Sorties : data/verses_map.json (debut_master, fin_master, statut_calage),
          data/calage_rapport.md
"""
import json, os, re, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER_LRC = os.path.join(ROOT, "data", "paroles_du_master.lrc.txt")


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z ñ]+", " ", s)
    return [w for w in s.split() if w]


def master_words():
    rows = []
    for line in open(MASTER_LRC, encoding="utf8"):
        m = re.match(r"\[(\d+):(\d+\.\d+)\]\s*(.*)", line.strip())
        if not m:
            continue
        t = int(m.group(1)) * 60 + float(m.group(2))
        text = m.group(3).strip()
        if text.startswith("["):
            continue
        ws = norm(text)
        for k, w in enumerate(ws):
            rows.append((w, t + 0.24 * k))
    return rows


def main():
    path = os.path.join(ROOT, "data", "verses_map.json")
    m = json.load(open(path, encoding="utf8"))
    mw = master_words()
    words = [w for w, _ in mw]
    times = [t for _, t in mw]
    print("mots horodatés dans le master :", len(mw))

    # 1. candidats par vers
    cands = []
    for v in m["verses"]:
        ws = norm(v["texte_source"])
        if not ws:
            cands.append([])
            continue
        # clé : les 2 premiers mots, mais un fragment de 2 mots identiques
        # (« ven amado ») doit correspondre aux 2 mêmes mots du master et pas
        # à un chevauchement glissant sur « ven ven ven ».
        K = 2 if len(ws) >= 2 else 1
        key = ws[:K]
        pos = [i for i in range(len(words) - K + 1) if words[i:i + K] == key]
        if not pos and K == 2:                  # repli : le premier mot seulement
            pos = [i for i in range(len(words)) if words[i] == ws[0]]
        cands.append(pos)

    vers_prec = m["verses"]
    # 2. chaîne croissante optimale
    ncand = [len(c) for c in cands]
    NEG = -10 ** 9
    best = [[NEG] * max(1, ncand[i]) for i in range(len(cands))]
    back = [[None] * max(1, ncand[i]) for i in range(len(cands))]
    if cands[0]:
        for j in range(ncand[0]):
            best[0][j] = 1
    for i in range(1, len(cands)):
        if not cands[i]:
            continue
        for j, p in enumerate(cands[i]):
            for i2 in range(i - 1, -1, -1):
                if not cands[i2]:
                    continue
                gain = None
                for j2, p2 in enumerate(cands[i2]):
                    # bornes : le candidat doit commencer après la fin du vers précédent
                    end_prev = p2 + (2 if len(norm(vers_prec[i2]["texte_source"])) >= 2 else 1)
                    if end_prev <= p and best[i2][j2] > NEG and (gain is None or best[i2][j2] > gain[0]):
                        gain = (best[i2][j2], j2, i2)
                if gain and gain[0] + 1 > best[i][j]:
                    best[i][j] = gain[0] + 1
                    back[i][j] = (gain[2], gain[1])
    # meilleure fin de chaîne
    bi, bj, bv = -1, -1, NEG
    for i in range(len(cands)):
        for j in range(ncand[i]):
            if best[i][j] > bv:
                bi, bj, bv = i, j, best[i][j]
    print("debug: premier vers avec candidat :", next((i for i, c in enumerate(cands) if c), None),
          "| nb candidats vers 2 :", len(cands[1]) if len(cands) > 1 else 0)
    anchors = {}
    if bv <= NEG // 2:
        bi = bj = None
    while bi is not None and bi >= 0 and bj is not None and bj >= 0:
        if not cands[bi]:
            break
        anchors[bi] = cands[bi][bj]
        nxt = back[bi][bj]
        if nxt is None:
            break
        bi, bj = nxt

    print(f"vers ancrés exactement : {len(anchors)} / {len(m['verses'])}")

    # 3. table de correspondance + interpolation par morceaux
    pts = sorted((m["verses"][i]["debut_source"], times[p]) for i, p in anchors.items())
    vers = m["verses"]

    def to_master(t):
        if not pts:
            return t
        if t <= pts[0][0]:
            return t + (pts[0][1] - pts[0][0])
        if t >= pts[-1][0]:
            return t + (pts[-1][1] - pts[-1][0])
        for (s0, m0), (s1, m1) in zip(pts, pts[1:]):
            if s0 <= t <= s1:
                r = (t - s0) / (s1 - s0) if s1 > s0 else 0
                return m0 + r * (m1 - m0)
        return t

    for i, v in enumerate(vers):
        if i in anchors:
            v["debut_master"] = round(times[anchors[i]], 3)
            v["ecart_ms"] = round((v["debut_master"] - v["debut_source"]) * 1000)
            v["statut_calage"] = "ancre_master"
        else:
            v["debut_master"] = round(to_master(v["debut_source"]), 3)
            v["ecart_ms"] = round((v["debut_master"] - v["debut_source"]) * 1000)
            v["statut_calage"] = "interpole"
    for k, v in enumerate(vers):
        v["fin_master"] = vers[k + 1]["debut_master"] if k + 1 < len(vers) else None

    ec = sorted(v["ecart_ms"] for v in vers if v["statut_calage"] == "ancre_master")
    med = ec[len(ec) // 2] if ec else 0
    m["calage"] = {
        "source": "ancres du MP3 maître (USLT intégré, 175 lignes)",
        "vers_ancres": len(anchors),
        "vers_interpoles": len(vers) - len(anchors),
        "ecart_median_ancre_ms": med,
        "ecart_min_ancre_ms": ec[0] if ec else None,
        "ecart_max_ancre_ms": ec[-1] if ec else None,
        "duree_audio_decodee_s": 744.705,
        "statut": "calé sur le master, fins non écoutées",
    }
    json.dump(m, open(path, "w", encoding="utf8"), ensure_ascii=False, indent=1)

    out = ["# RAPPORT DE CALAGE — MESÍAS (Live) sur le master fourni", "",
           f"- Vers ancrés exactement sur les ancres du master : **{len(anchors)} / {len(vers)}**",
           f"- Vers interpolés entre ancres : {len(vers) - len(anchors)}",
           f"- Écart médian (contrat lrclib → master) sur les ancres : **{med:+d} ms**",
           f"- Écarts ancres : min {ec[0]:+d} ms · max {ec[-1]:+d} ms" if ec else "",
           "", "| # | début contrat | début master | écart | statut |", "|---|---|---|---|---|"]
    for v in vers[:20]:
        out.append(f"| {v['i']} | {v['debut_source']:.2f} | {v['debut_master']} | "
                   f"{v['ecart_ms']:+d} ms | {v['statut_calage']} |")
    out.append("| … | … | … | … | … |")
    for v in vers[-8:]:
        out.append(f"| {v['i']} | {v['debut_source']:.2f} | {v['debut_master']} | "
                   f"{v['ecart_ms']:+d} ms | {v['statut_calage']} |")
    open(os.path.join(ROOT, "data", "calage_rapport.md"), "w", encoding="utf8").write("\n".join(out) + "\n")
    print(f"médiane ancres {med:+d} ms · min {ec[0]:+d} · max {ec[-1]:+d}")


if __name__ == "__main__":
    main()
