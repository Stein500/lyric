#!/usr/bin/env python3
"""Export the ten AI edits, an individual-image gallery and a ten-file ZIP."""
from pathlib import Path
import hashlib
import html
import json
import zipfile
from PIL import Image, ImageDraw, ImageFont, ImageOps, PngImagePlugin

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
SIZE = (1080, 1920)
LANCZOS = Image.Resampling.LANCZOS


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size, serif=False):
    name = 'PlayfairDisplay.ttf' if serif else 'Montserrat.ttf'
    f = ImageFont.truetype(str(ROOT/'dsky-quotes/assets/fonts'/name),size)
    f.set_variation_by_axes([400 if serif else 500])
    return f


def make_sheet(scenes):
    w, h, gap, margin = 288, 512, 18, 32
    header, labels, rowgap, footer = 132, 38, 20, 56
    canvas = Image.new('RGB',(2*margin+5*w+4*gap, header+2*(h+labels)+rowgap+footer),'#251e23')
    d=ImageDraw.Draw(canvas)
    d.text((margin,20),'VIVI OOR',font=font(52,True),fill='#f4e8db')
    d.text((margin,88),'10 portraits · Finition IA · 9:16 · Sans texte',font=font(18),fill='#d4beb0')
    names=['Invitation dorée','Le goût du miel','Les étincelles','Reste avec moi','Chaque instant',
           'Le cœur ouvert','Notre trésor','Le festin','Jusqu’au matin','L’aube douce']
    for i,s in enumerate(scenes):
        x=margin+(i%5)*(w+gap); y=header+(i//5)*(h+labels+rowgap)
        with Image.open(PROJECT/s['output']) as im:
            canvas.paste(im.resize((w,h),LANCZOS),(x,y))
        d.text((x,y+h+10),f'{i+1:02d}  {names[i]}',font=font(16),fill='#f4e8db')
    d.text((margin,canvas.height-36),'Retouches IA d’après la même photo originale · Version 02',font=font(16),fill='#d4beb0')
    canvas.save(PROJECT/'VIVI_OOR_V2_apercu.jpg',quality=93,subsampling=0)


def make_gallery(scenes):
    cards=[]
    slides=[]
    for i,s in enumerate(scenes):
        title=html.escape(s['title'])
        out=html.escape(s['output'],quote=True)
        preview=f"apercus/{s['slot']:02d}_{s['slug']}.jpg"
        cards.append(f'''<article class="card">
  <button class="photo" type="button" data-open="{i}" aria-label="Agrandir l’image {i+1} : {title}"><img src="{preview}" width="540" height="960" alt="Vivi OOR — {title}, portrait retouché par IA" loading="{'eager' if i<2 else 'lazy'}" decoding="async"></button>
  <div class="caption"><div><span class="number">{i+1:02d}</span><h2>{title}</h2></div><a class="download" href="{out}" download aria-label="Télécharger l’image {i+1}">PNG ↗</a></div>
</article>''')
        slides.append(dict(src=s['output'], title=s['title'], num=i+1))
    template='''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><title>Vivi OOR — Les 10 images</title>
<style>
:root{--paper:#f1ebe3;--ink:#30252b;--muted:#6f5e62;--accent:#825037;--line:#d9cfc7}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:1400px;margin:auto;padding:42px 28px 54px}.head{display:flex;align-items:flex-end;justify-content:space-between;gap:28px;padding-bottom:30px;margin-bottom:28px;border-bottom:1px solid var(--line)}.eyebrow{font-size:11px;letter-spacing:.18em;font-weight:700;color:var(--accent)}h1{font:normal clamp(50px,7vw,86px)/1.02 Georgia,serif;letter-spacing:-.05em;margin:12px 0 16px}p{font-size:14px;line-height:1.6;margin:0;color:var(--muted);max-width:620px}.pack{display:inline-flex;align-items:center;justify-content:center;gap:12px;text-decoration:none;white-space:nowrap;background:var(--ink);color:#fff7ef;padding:16px 22px;border-radius:6px;font-size:13px;font-weight:600}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:30px 22px}.card{min-width:0}.photo{padding:0;border:0;background:#d8ccc1;display:block;width:100%;cursor:zoom-in;overflow:hidden;border-radius:5px}.photo img{display:block;width:100%;height:auto;aspect-ratio:9/16;object-fit:cover;transition:transform .3s ease}.photo:hover img{transform:scale(1.012)}.photo:focus-visible{outline:3px solid var(--accent);outline-offset:4px}.caption{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:14px 0 0}.caption>div{display:flex;align-items:baseline;gap:10px;min-width:0}.number{font-size:11px;font-weight:700;color:var(--accent)}h2{font-size:13px;font-weight:500;line-height:1.35;margin:0}.download{flex-shrink:0;font-size:10px;letter-spacing:.05em;color:var(--ink);text-decoration:none;padding:5px 0;border-bottom:1px solid var(--line)}footer{margin-top:40px;padding-top:22px;border-top:1px solid var(--line);font-size:12px;color:var(--muted);line-height:1.6}dialog{width:min(1080px,96vw);max-width:none;height:96dvh;max-height:96dvh;border:0;border-radius:9px;background:#1d191c;color:#fff;padding:14px;overflow:hidden}dialog::backdrop{background:rgba(18,14,17,.92)}.modalbar{display:flex;justify-content:space-between;align-items:center;gap:18px;height:44px;font-size:12px}.modalbar button,.controls button{background:transparent;color:inherit;border:1px solid #63565e;border-radius:5px;padding:8px 13px;cursor:pointer;font:inherit}.modal-image{height:calc(100% - 100px);display:flex;align-items:center;justify-content:center}.modal-image img{display:block;width:100%;height:100%;object-fit:contain}.controls{height:56px;display:flex;justify-content:center;align-items:center;gap:15px;font-size:12px}.controls a{color:#fff0df;text-decoration:none;padding:10px}.modalbar button:focus-visible,.controls button:focus-visible,.controls a:focus-visible{outline:2px solid #e8bb8a;outline-offset:2px}@media(max-width:1100px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:650px){main{padding:26px 16px}.head{display:block;margin-bottom:22px}.pack{margin-top:22px;width:100%}.grid{grid-template-columns:1fr;gap:30px}.caption{padding:12px 2px 0}h2{font-size:14px}.modalbar{font-size:11px}dialog{padding:10px}.controls{gap:9px}.controls button{padding:8px 9px}}@media(prefers-reduced-motion:reduce){.photo img{transition:none}.photo:hover img{transform:none}}
</style></head><body><main>
<header class="head"><div><div class="eyebrow">DAÏSKY · SÉRIE VISUELLE 02</div><h1>Vivi OOR</h1><p>Les 10 images retravaillées avec l’IA. Même photo de référence, dix ambiances romantiques.<br><strong>1080 × 1920 · Sans texte.</strong> Touche une image pour l’afficher en grand.</p></div><a class="pack" href="VIVI_OOR_V2_10_images_9x16.zip" download>Télécharger les 10 images <span aria-hidden="true">↓</span></a></header>
<section class="grid" aria-label="Les dix portraits de Vivi OOR">__CARDS__</section>
<footer>Retouches photographiques par IA à partir de la photo originale validée. Cette version améliore les raccords, la lumière et le rendu photographique ; elle n’est pas une conservation pixel par pixel du visage. La première version reste disponible dans le dossier du projet.</footer>
</main><dialog id="viewer" aria-label="Image en grand"><div class="modalbar"><span id="caption"></span><button id="close" type="button" aria-label="Fermer l’image">Fermer ✕</button></div><div class="modal-image"><img id="large" alt=""></div><div class="controls"><button id="prev" type="button" aria-label="Image précédente">← Précédente</button><a id="save" download>Télécharger le PNG</a><button id="next" type="button" aria-label="Image suivante">Suivante →</button></div></dialog>
<script>
const slides=__SLIDES__;
const dialog=document.getElementById('viewer'),large=document.getElementById('large');let active=0,opener=null;
function show(i){active=(i+slides.length)%slides.length;const s=slides[active];large.src=s.src;large.alt='Vivi OOR — '+s.title;document.getElementById('caption').textContent=String(s.num).padStart(2,'0')+' / 10 · '+s.title;document.getElementById('save').href=s.src;}
document.querySelectorAll('[data-open]').forEach(b=>b.addEventListener('click',()=>{opener=b;show(Number(b.dataset.open));dialog.showModal();}));
document.getElementById('close').addEventListener('click',()=>dialog.close());
document.getElementById('prev').addEventListener('click',()=>show(active-1));document.getElementById('next').addEventListener('click',()=>show(active+1));
dialog.addEventListener('close',()=>{if(opener)opener.focus();});dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
document.addEventListener('keydown',e=>{if(!dialog.open)return;if(e.key==='ArrowLeft'){e.preventDefault();show(active-1);}if(e.key==='ArrowRight'){e.preventDefault();show(active+1);}});
</script></body></html>'''
    content=template.replace('__CARDS__','\n'.join(cards)).replace('__SLIDES__',json.dumps(slides,ensure_ascii=False).replace('</','<\\/'))
    (PROJECT/'index.html').write_text(content)


def main():
    manifest=json.loads((PROJECT/'manifest.json').read_text())
    scenes=manifest['scenes']; assert len(scenes)==10
    source=ROOT/manifest['source']; assert sha(source)==manifest['source_sha256']
    assert len(list((PROJECT/'assets/edits').glob('*.jpg')))==10
    report=dict(version=2,dimensions=list(SIZE),count=10,source_unchanged=True,
                identity_check='Visual review only; AI retouches are not pixel-identical to the original.',files=[])
    (PROJECT/'apercus').mkdir(exist_ok=True)
    for scene in scenes:
        raw=PROJECT/scene['raw']; target=PROJECT/scene['output']
        with Image.open(raw) as im:
            original_size=im.size
            image=ImageOps.fit(im.convert('RGB'),SIZE,method=LANCZOS,centering=(.5,.5))
        target.parent.mkdir(exist_ok=True,parents=True)
        info=PngImagePlugin.PngInfo()
        info.add_text('Description','AI photographic retouch using the artist original photo as reference. Not an unmodified photograph.')
        image.save(target,pnginfo=info,compress_level=6)
        image.resize((540,960),LANCZOS).save(PROJECT/'apercus'/raw.name,quality=91,subsampling=0)
        with Image.open(target) as test:
            assert test.size==SIZE and test.mode=='RGB'
        report['files'].append(dict(file=scene['output'],sha256=sha(target),bytes=target.stat().st_size,
                                    raw_size=list(original_size),raw_sha256=sha(raw)))
        print('OK',target.name,original_size,'->',SIZE)
    assert len({f['sha256'] for f in report['files']})==10
    expected={Path(s['output']).name for s in scenes}
    assert {p.name for p in (PROJECT/'livrables').iterdir() if p.is_file()}==expected
    archive=PROJECT/'VIVI_OOR_V2_10_images_9x16.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_STORED) as z:
        for scene in scenes:
            path=PROJECT/scene['output']; info=zipfile.ZipInfo(path.name,date_time=(2026,9,26,0,0,0))
            info.compress_type=zipfile.ZIP_STORED; info.external_attr=0o644<<16
            z.writestr(info,path.read_bytes())
    with zipfile.ZipFile(archive) as z:
        assert set(z.namelist())==expected and len(z.namelist())==10 and z.testzip() is None
    report['zip']=dict(file=archive.name,bytes=archive.stat().st_size,sha256=sha(archive),count=10)
    (PROJECT/'controle_qualite.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    make_sheet(scenes); make_gallery(scenes)
    print('Verified ZIP: 10 images;',round(archive.stat().st_size/1e6,1),'MB')


if __name__=='__main__':
    main()
