#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""console.py — console de production live (aperçu du clip pendant que les plans arrivent).

Sert un tableau de bord : /            (HTML)
                        /api/state     (JSON : carte-vers, plans dispo, segments prêts)
                        /seg/<i>.mp4   (segment de 8 s, rendu à la demande puis en cache)
                        /img/<nom>     (planche de contrôle)

Le worker de fond pré-rend les segments dans l'ordre, un seul à la fois.
    python3 console.py [--port 8000] [--seg 8]
"""
import json, os, subprocess, sys, threading, time, http.server, socketserver, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
SEGDIR = os.path.join(HERE, "livrables", "seg")
FF = os.environ.get("FF") or subprocess.run([sys.executable, "-c",
      "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"],
      capture_output=True, text=True).stdout.strip()

DOC = json.load(open(os.path.join(HERE, "verses_map.json"), encoding="utf-8"))
TOTAL = DOC["clip_duree_s"]
SEG = 8.0
NS = int(TOTAL // SEG) + 1
LOCK = threading.Lock()
DONE = set()


def seg_path(i):
    return os.path.join(SEGDIR, f"seg-{i:02d}.mp4")


def render_seg(i):
    os.makedirs(SEGDIR, exist_ok=True)
    a = i * SEG
    dur = min(SEG, TOTAL - a)
    if dur <= 0.1:
        return
    t0 = time.time()
    subprocess.run([sys.executable, os.path.join(HERE, "render.py"), "--start", f"{a:.2f}",
                    "--dur", f"{dur:.2f}", "--out", f"livrables/seg/seg-{i:02d}.mp4"],
                   cwd=HERE, check=True, capture_output=True)
    DONE.add(i)
    print(f"  seg {i:02d} · {a:6.1f}s · rendu en {time.time()-t0:5.1f}s", flush=True)


def worker():
    while True:
        with LOCK:
            todo = [i for i in range(NS) if i not in DONE and not os.path.exists(seg_path(i))]
        if not todo:
            time.sleep(3)
            continue
        try:
            render_seg(todo[0])
        except Exception as e:                       # noqa: BLE001
            print("  échec segment", todo[0], e, flush=True)
            time.sleep(5)


def state():
    plans = sorted({v["image"] for v in DOC["vers"]})
    dispo = [p for p in plans if os.path.exists(os.path.join(HERE, p))]
    done = sorted(i for i in range(NS) if os.path.exists(seg_path(i)))
    return {
        "titre": DOC["titre"], "artiste": DOC["artiste"], "recette": DOC["recette"],
        "module": DOC["mode"], "duree": TOTAL, "vers": len(DOC["vers"]), "plans": len(plans),
        "plans_dispo": len(dispo), "segments": NS, "segments_prets": len(done),
        "seg_taille": SEG,
        "plan_courant": [{"t": v["t"], "fin": v["fin"], "texte": v["texte"], "image": v["image"],
                          "dispo": os.path.exists(os.path.join(HERE, v["image"]))}
                         for v in DOC["vers"]],
    }


HTML = """<!doctype html><html lang="fr"><head><meta charset="utf-8">
<title>WTBW · console — %(titre)s</title>
<style>
:root{--or:#F4C562;--nuit:#0b1016;--carte:#121a24;--txt:#eef3fb;--gris:#93a4bb}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(1200px 600px at 50%% -10%%,#16222e,#070b10 70%%);
color:var(--txt);font:15px/1.5 Montserrat,system-ui,sans-serif}
header{padding:18px 22px;border-bottom:1px solid #22303f;display:flex;gap:18px;align-items:baseline;flex-wrap:wrap}
h1{font-size:17px;margin:0;letter-spacing:.06em;text-transform:uppercase}
.tag{color:var(--or);font-size:12px;letter-spacing:.16em;text-transform:uppercase}
main{display:grid;grid-template-columns:minmax(300px,420px) 1fr;gap:22px;padding:22px}
video{width:100%%;aspect-ratio:9/16;background:#000;border-radius:16px;border:1px solid #22303f}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px;margin-bottom:16px}
.stat{background:var(--carte);border:1px solid #22303f;border-radius:14px;padding:12px}
.stat b{display:block;font-size:22px;color:var(--or)}
.stat span{font-size:11px;color:var(--gris);letter-spacing:.12em;text-transform:uppercase}
.bar{height:8px;background:#1b2632;border-radius:99px;overflow:hidden;margin:6px 0 18px}
.bar i{display:block;height:100%%;background:linear-gradient(90deg,#F4C562,#FFE07A);width:0}
table{width:100%%;border-collapse:collapse;font-size:13px}
td,th{padding:5px 8px;border-bottom:1px solid #1b2632;text-align:left;vertical-align:middle}
th{color:var(--gris);font-size:11px;letter-spacing:.1em;text-transform:uppercase}
.ok{color:#6ee7a8}.no{color:#ff8d8d}
tr.now{background:#1b2a1f}
.small{color:var(--gris);font-size:12px}
a{color:var(--or)}
</style></head><body>
<header><span class="tag">WTBW</span><h1>%(titre)s — %(artiste)s</h1>
<span class="tag">%(recette)s</span><span class="small">%(module)s</span></header>
<main>
 <section>
  <div class="stats">
   <div class="stat"><b id="s-plans">–</b><span>plans générés</span></div>
   <div class="stat"><b id="s-vers">–</b><span>vers calés</span></div>
   <div class="stat"><b id="s-seg">–</b><span>segments rendus</span></div>
   <div class="stat"><b id="s-dur">–</b><span>durée clip</span></div>
  </div>
  <div class="bar"><i id="bar"></i></div>
  <video id="v" controls autoplay muted playsinline loop></video>
  <p class="small">Lecture continue : les segments se rendent en file (8 s chacun, ~2,5× le temps réel).
  Le son est coupé par défaut — clique sur ▶︎ pour l'entendre.</p>
 </section>
 <section>
  <div class="small" id="cur">—</div>
  <table><thead><tr><th>#</th><th>t</th><th>vers</th><th>plan</th><th>état</th></tr></thead>
  <tbody id="rows"></tbody></table>
 </section>
</main>
<script>
let segIdx = 0, segTaille = 8, vers = [], nSeg = 1;
const v = document.getElementById('v');
function playSeg(i){
  if(i >= nSeg) { i = 0; }
  segIdx = i;
  v.src = '/seg/' + String(i).padStart(2,'0') + '.mp4?t=' + Date.now();
  v.play().catch(()=>{});
}
v.addEventListener('ended', ()=> playSeg(segIdx+1));
v.addEventListener('error', ()=> setTimeout(()=> playSeg(segIdx), 4000));
async function tick(){
  try{
    const s = await (await fetch('/api/state',{cache:'no-store'})).json();
    segTaille = s.seg_taille; nSeg = s.segments; vers = s.plan_courant;
    document.getElementById('s-plans').textContent = s.plans_dispo + '/' + s.plans;
    document.getElementById('s-vers').textContent = s.vers;
    document.getElementById('s-seg').textContent = s.segments_prets + '/' + s.segments;
    document.getElementById('s-dur').textContent = Math.round(s.duree) + ' s';
    document.getElementById('bar').style.width = (100*s.segments_prets/s.segments).toFixed(1)+'%%';
    const t = segIdx*segTaille + (v.currentTime||0);
    const rows = vers.map(x=>{
      const now = t>=x.t && t<x.fin;
      return `<tr class="${now?'now':''}"><td>${String(vers.indexOf(x)+1).padStart(2,'0')}</td>
      <td>${x.t.toFixed(1)}</td><td>${x.texte}</td><td class="small">${x.image.split('/').pop()}</td>
      <td class="${x.dispo?'ok':'no'}">${x.dispo?'plan prêt':'ancre'}</td></tr>`;
    }).join('');
    document.getElementById('rows').innerHTML = rows;
    const cur = vers.filter(x=> t>=x.t && t<x.fin).pop();
    document.getElementById('cur').textContent = cur ? `t=${t.toFixed(1)}s · ${cur.texte}` : `t=${t.toFixed(1)}s · carte`;
  }catch(e){}
}
setInterval(tick, 2000); tick();
setTimeout(()=>{ if(!v.src) playSeg(0); }, 1500);
</script></body></html>
"""


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=HERE, **k)

    def log_message(self, *a):
        pass

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        if u.path == "/":
            body = HTML % state()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(body.encode())
            return
        if u.path == "/api/state":
            body = json.dumps(state(), ensure_ascii=False).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        if u.path.startswith("/seg/"):
            i = int(u.path.split("/")[-1].split(".")[0])
            p = seg_path(i)
            if not os.path.exists(p):
                with LOCK:
                    todo = [k for k in range(NS) if k not in DONE and not os.path.exists(seg_path(k))]
                if todo and todo[0] == i:
                    try:
                        render_seg(i)
                    except Exception:                 # noqa: BLE001
                        pass
            if os.path.exists(p):
                data = open(p, "rb").read()
                self.send_response(200)
                self.send_header("Content-Type", "video/mp4")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            self.send_response(503)
            self.end_headers()
            return
        return super().do_GET()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    port = 8000
    if "--port" in sys.argv:
        port = int(sys.argv[sys.argv.index("--port") + 1])
    if "--seg" in sys.argv:
        SEG = float(sys.argv[sys.argv.index("--seg") + 1])
        NS = int(TOTAL // SEG) + 1
    threading.Thread(target=worker, daemon=True).start()
    print(f"console WTBW · http://0.0.0.0:{port} · {NS} segments de {SEG:.0f}s", flush=True)
    with Server(("0.0.0.0", port), H) as httpd:
        httpd.serve_forever()
