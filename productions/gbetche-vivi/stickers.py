# -*- coding: utf-8 -*-
"""
stickers.py - calques « papier collant / feutre / icone dessinee ».

Tout est trace a la main (PIL), aucun emoji, aucune bitmap externe : les icones sont des
contours vectoriels pour rester nets en 1080x1920.

Deux regles qui viennent de la pratique :
  * apres un Image.alpha_composite, l'ImageDraw precedent est perime -> le creer APRES ;
  * ne JAMAIS travailler en pleine image (1080x1920 RGBA = 8 Mo) quand le dessin tient dans
    une boite de 200 px : flou et rotation coute 30 a 120 ms par frame, donc 12 mn de rendu
    pour rien. Chaque primitive calcule sa boite, dessine dedans, puis se recolle via _put().
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BEIGE = (226, 212, 178, 215)
GOLD = (255, 211, 90, 255)
ORANGE = (255, 138, 66, 235)
ROUGE = (232, 66, 66, 235)
CREME = (243, 236, 217, 255)
ENCRE = (16, 16, 18, 235)


def _put(d, lay, off=(0, 0)):
    """colle un sous-calque dans l'image du draw (ImageDraw.im = ImagingCore -> pas d'alpha_composite)."""
    im = getattr(d, "_image", None)
    if im is None or not hasattr(im, "alpha_composite"):
        raise RuntimeError("creer ImageDraw.Draw(layer) puis passer layer a _put")
    if off == (0, 0):
        im.alpha_composite(lay)
    else:
        im.alpha_composite(lay, dest=off)


def _box(cx, cy, w, h, m=0):
    """boite entiere centree, margee, clippee aux bords ; renvoie (x0,y0,x1,y1)."""
    im_w, im_h = 10 ** 6, 10 ** 6
    x0 = int(math.floor(cx - w / 2 - m)); y0 = int(math.floor(cy - h / 2 - m))
    x1 = int(math.ceil(cx + w / 2 + m)); y1 = int(math.ceil(cy + h / 2 + m))
    return max(0, x0), max(0, y0), x1, y1


def _local(bx, pad=6):
    x0, y0, x1, y1 = bx
    x0 = max(0, int(x0) - pad); y0 = max(0, int(y0) - pad)
    x1 = int(x1) + pad; y1 = int(y1) + pad
    return x0, y0, max(1, x1 - x0), max(1, y1 - y0)


def tape(d, cx, cy, w=118, h=34, ang=-7, col=BEIGE):
    """bande de masking tape, bords dechires."""
    x0, y0, lw, lh = _local((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 10)
    lay = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    dd = ImageDraw.Draw(lay)
    rng = np.random.default_rng(abs(int(cx * 7 + cy * 13)) % 9973)
    pts = []
    for (x, y) in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]:
        pts.append((x + rng.uniform(-5, 5), y + rng.uniform(-5, 5)))
    poly = [(cx - x0 + p[0], cy - y0 + p[1]) for p in pts]
    dd.polygon(poly, fill=col)
    dd.line([(cx - x0 - w / 2, cy - y0 - h / 2 + 2), (cx - x0 - w / 2, cy - y0 + h / 2 - 2)],
            fill=(255, 255, 255, 60), width=2)
    lay = lay.rotate(ang, resample=Image.BICUBIC, expand=False)
    _put(d, lay, (x0, y0))


def star(d, cx, cy, r=54, points=9, col=GOLD, rot=8, alpha=235):
    """autocollant en etoile (crans courts), plat, facon papier decoupe."""
    x0, y0, lw, lh = _local((cx - r, cy - r, cx + r, cy + r), 6)
    lay = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    dd = ImageDraw.Draw(lay)
    pts = []
    rng = np.random.default_rng(int(cx + cy * 3) % 9973)
    for k in range(points * 2):
        a = math.tau * k / (points * 2) + math.radians(rot)
        rad = r if k % 2 == 0 else r * rng.uniform(0.62, 0.74)
        pts.append((cx - x0 + rad * math.cos(a), cy - y0 + rad * math.sin(a)))
    dd.polygon(pts, fill=col[:3] + (alpha,))
    dd.polygon(pts, outline=(255, 255, 255, 90))
    _put(d, lay, (x0, y0))


def burst(d, cx, cy, r=88, col=GOLD, n=12, alpha=225):
    """rayons de lumiere autour d'un point."""
    x0, y0, lw, lh = _local((cx - r * 1.4, cy - r * 1.4, cx + r * 1.4, cy + r * 1.4), 4)
    lay = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    dd = ImageDraw.Draw(lay)
    rng = np.random.default_rng(int(cx + cy) % 9973)
    for k in range(n):
        a = math.tau * k / n + math.radians(6)
        r0, r1 = r * rng.uniform(0.55, 0.7), r * rng.uniform(1.0, 1.35)
        dd.line([(cx - x0 + r0 * math.cos(a), cy - y0 + r0 * math.sin(a)),
                 (cx - x0 + r1 * math.cos(a), cy - y0 + r1 * math.sin(a))],
                fill=col[:3] + (alpha,), width=5)
    _put(d, lay, (x0, y0))


def squiggle(d, x0_, y, x1_, col=GOLD, width=7, wob=6.0, seed=0):
    """souligne au feutre : ondule, epaisseur variable."""
    bx = (min(x0_, x1_) - 8, y - wob * 2 - width, max(x0_, x1_) + 8, y + wob * 2 + width)
    lx0, ly0, lw, lh = _local(bx, 2)
    lay = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    dd = ImageDraw.Draw(lay)
    rng = np.random.default_rng(seed % 9973)
    n = max(12, int((x1_ - x0_) / 14))
    pts = []
    for i in range(n + 1):
        u = i / n
        x = x0_ + (x1_ - x0_) * u
        yy = y + math.sin(u * math.pi * 1.6) * wob * 0.5 + rng.uniform(-wob * .25, wob * .25) + u * wob * 0.8
        pts.append((x - lx0, yy - ly0))
    for i in range(len(pts) - 1):
        w = int(width * (0.72 + 0.5 * math.sin(math.pi * i / max(1, len(pts) - 1))))
        dd.line([pts[i], pts[i + 1]], fill=col[:3] + (235,), width=max(3, w))
    _put(d, lay, (lx0, ly0))


def highlight(d, box, col=(255, 211, 90), pad=8, alpha=110, seed=0):
    """coup de surligneur derriere un mot (parallelogramme flou, legerement depasse)."""
    x0, y0, x1, y1 = box
    rng = np.random.default_rng(seed % 9973)
    sk = rng.uniform(9, 16)
    lx0, ly0, lw, lh = _local((x0 - pad, y0 - pad - sk, x1 + pad, y1 + pad + sk), 5)
    lay = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    dd = ImageDraw.Draw(lay)
    poly = [(x0 - lx0 - pad, y0 - ly0 - pad * .4 + sk), (x1 - lx0 + pad, y0 - ly0 - pad * .4 - sk * .4),
            (x1 - lx0 + pad, y1 - ly0 + pad * .4 - sk * .3), (x0 - lx0 - pad, y1 - ly0 + pad * .4 + sk * .3)]
    dd.polygon(poly, fill=col[:3] + (alpha,))
    lay = lay.filter(ImageFilter.GaussianBlur(3.2))
    _put(d, lay, (lx0, ly0))


def dashed(d, box, col=CREME, width=4, dash=16, gap=11, rad=18, alpha=215):
    """cadre en pointilles, trace a la main, coins arrondis."""
    x0, y0, x1, y1 = [v + p for v, p in zip(box, (-rad, -rad, rad, rad))]
    lx0, ly0, lw, lh = _local((x0, y0, x1, y1), width + 2)
    lay = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    dd = ImageDraw.Draw(lay)
    pts = [(x0, y0 + rad), (x0 + rad, y0), (x1 - rad, y0), (x1, y0 + rad), (x1, y1 - rad),
           (x1 - rad, y1), (x0 + rad, y1), (x0, y1 - rad), (x0, y0 + rad)]
    per = []
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        L = math.hypot(bx - ax, by - ay)
        n = max(2, int(L / 7))
        for i in range(n):
            u = i / n
            per.append((ax + (bx - ax) * u, ay + (by - ay) * u))
    step = max(2, int(dash / 7))
    for i in range(len(per) - 1):
        if (i % (step + max(1, int(gap / 7)))) < step:
            dd.line([(per[i][0] - lx0, per[i][1] - ly0), (per[i + 1][0] - lx0, per[i + 1][1] - ly0)],
                    fill=col[:3] + (alpha,), width=width)
    _put(d, lay, (lx0, ly0))


def arrow(d, p0, p1, col=ORANGE, width=7, curve=44, head=22, alpha=235):
    """fleche courbe dessinee, tete en V."""
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 - curve
    bx = (min(p0[0], p1[0], mx) - head - 8, min(p0[1], p1[1], my) - head - 8,
          max(p0[0], p1[0], mx) + head + 8, max(p0[1], p1[1], my) + head + 8)
    lx0, ly0, lw, lh = _local(bx, 2)
    lay = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    dd = ImageDraw.Draw(lay)
    pts = []
    for i in range(27):
        u = i / 26
        a, b = 1 - u, u
        pts.append((a * a * p0[0] + 2 * a * b * mx + b * b * p1[0] - lx0,
                    a * a * p0[1] + 2 * a * b * my + b * b * p1[1] - ly0))
    for i in range(len(pts) - 1):
        dd.line([pts[i], pts[i + 1]], fill=col[:3] + (alpha,), width=width)
    ang = math.atan2(pts[-1][1] - pts[-3][1], pts[-1][0] - pts[-3][0])
    for s in (-1, 1):
        dd.line([pts[-1], (pts[-1][0] - head * math.cos(ang + s * .55), pts[-1][1] - head * math.sin(ang + s * .55))],
                fill=col[:3] + (alpha,), width=width)
    _put(d, lay, (lx0, ly0))


def icon(d, cx, cy, kind="bell", s=40, col=GOLD, width=5, alpha=255):
    """contours vectoriels : bell, share, bookmark, play, eye, check, spark."""
    x0, y0, lw, lh = _local((cx - s * 1.9, cy - s * 1.6, cx + s * 1.9, cy + s * 1.3), 4)
    lay = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    dd = ImageDraw.Draw(lay)
    c = col[:3] + (alpha,)

    def E(r):   # ellipse translatee
        return [r[0] - x0, r[1] - y0, r[2] - x0, r[3] - y0]

    def P(p):
        return (p[0] - x0, p[1] - y0)
    if kind == "bell":
        dd.arc(E([cx - s, cy - s * 1.15, cx + s, cy + s * .75]), 195, 345, fill=c, width=width)
        dd.line([P((cx - s, cy + s * .1)), P((cx - s * 1.18, cy + s * .62))], fill=c, width=width)
        dd.line([P((cx + s, cy + s * .1)), P((cx + s * 1.18, cy + s * .62))], fill=c, width=width)
        dd.line([P((cx - s * 1.2, cy + s * .62)), P((cx + s * 1.2, cy + s * .62))], fill=c, width=width)
        dd.arc(E([cx - s * .3, cy + s * .55, cx + s * .3, cy + s * 1.15]), 20, 160, fill=c, width=width)
        dd.line([P((cx, cy - s * 1.5)), P((cx, cy - s * 1.15))], fill=c, width=width)
        for k in (-1, 1):
            dd.line([P((cx + k * s * 1.5, cy - s * 1.1)), P((cx + k * s * 1.9, cy - s * 1.5))],
                    fill=c, width=width - 1)
    elif kind == "share":
        for (ax, ay) in [(cx + s, cy - s * .9), (cx - s * .8, cy), (cx + s, cy + s * .9)]:
            dd.ellipse(E([ax - s * .34, ay - s * .34, ax + s * .34, ay + s * .34]), outline=c, width=width)
        dd.line([P((cx - s * .6, cy - s * .12)), P((cx + s * .75, cy - s * .78))], fill=c, width=width - 1)
        dd.line([P((cx - s * .6, cy + s * .12)), P((cx + s * .75, cy + s * .78))], fill=c, width=width - 1)
    elif kind == "bookmark":
        dd.polygon([P((cx - s * .7, cy - s)), P((cx + s * .7, cy - s)), P((cx + s * .7, cy + s)),
                    P((cx, cy + s * .4)), P((cx - s * .7, cy + s))], outline=c, width=width)
    elif kind == "play":
        dd.polygon([P((cx - s * .6, cy - s * .8)), P((cx + s * .8, cy)), P((cx - s * .6, cy + s * .8))],
                   fill=c, outline=c)
    elif kind == "eye":
        dd.arc(E([cx - s, cy - s, cx + s, cy + s]), 215, 325, fill=c, width=width)
        dd.arc(E([cx - s, cy - s * 1.9, cx + s, cy + s * .1]), 35, 145, fill=c, width=width)
        dd.ellipse(E([cx - s * .26, cy - s * .26, cx + s * .26, cy + s * .26]), fill=c)
    elif kind == "check":
        dd.line([P((cx - s * .85, cy)), P((cx - s * .18, cy + s * .62)), P((cx + s * .9, cy - s * .72))],
                fill=c, width=width + 1)
    elif kind == "spark":
        dd.line([P((cx, cy - s)), P((cx, cy + s))], fill=c, width=width)
        dd.line([P((cx - s, cy)), P((cx + s, cy))], fill=c, width=width)
        for k in (-1, 1):
            dd.line([P((cx + k * s * .62, cy - s * .62)), P((cx + k * s * .95, cy - s * .95))],
                    fill=c, width=width - 2)
            dd.line([P((cx + k * s * .62, cy + s * .62)), P((cx + k * s * .95, cy + s * .95))],
                    fill=c, width=width - 2)
    _put(d, lay, (x0, y0))


def tag(d, cx, cy, txt, font, bg=(24, 24, 28), fg=GOLD, rot=-6, pad=(20, 10), alpha=245,
        outline=(255, 211, 90, 150), width=3):
    """etiquette sticker (REFRAIN / ADLIB / code), legerement inclinnee."""
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    bb = probe.textbbox((0, 0), txt, font=font)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    bx = (cx - w / 2 - pad[0], cy - h / 2 - pad[1], cx + w / 2 + pad[0], cy + h / 2 + pad[1])
    x0, y0, lw, lh = _local(bx, 4)
    lay = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    dd = ImageDraw.Draw(lay)
    r = [bx[0] - x0, bx[1] - y0, bx[2] - x0, bx[3] - y0]
    dd.rounded_rectangle(r, radius=16, fill=bg[:3] + (alpha,), outline=outline, width=width)
    dd.text((cx - x0 - (w / 2 + bb[0]), cy - y0 - (h / 2 + bb[1])), txt, font=font, fill=fg[:3] + (255,))
    lay = lay.rotate(rot, resample=Image.BICUBIC, expand=False)
    _put(d, lay, (x0, y0))


def sparkles(size, t, zones, rng_seed=7, n=3, m=46):
    """etincelles qui clignotent autour des zones -> (calque local, offset)."""
    x0 = int(min(z[0] for z in zones)) - m; y0 = int(min(z[1] for z in zones)) - m
    x1 = int(max(z[2] for z in zones)) + m; y1 = int(max(z[3] for z in zones)) + m
    if size is not None:
        x0 = max(0, x0); y0 = max(0, y0)
    lay = Image.new("RGBA", (max(1, x1 - x0), max(1, y1 - y0)), (0, 0, 0, 0))
    dd = ImageDraw.Draw(lay)
    rng = np.random.default_rng(rng_seed % 9973)
    for zi, (zx0, zy0, zx1, zy1) in enumerate(zones):
        for k in range(n):
            ph = rng.uniform(0, math.tau)
            u = (math.sin(t * 2.1 + ph) + 1) / 2
            a = int(210 * u)
            if a < 24:
                continue
            cx = zx0 + (zx1 - zx0) * (0.16 + 0.68 * ((k * 0.37 + zi * 0.13 + 0.21) % 1.0))
            cy = zy0 + (zy1 - zy0) * (0.18 + 0.64 * ((k * 0.53 + zi * 0.29 + 0.44) % 1.0))
            s = 7 + 13 * u
            cx -= x0; cy -= y0
            dd.line([(cx, cy - s * 1.7), (cx, cy + s * 1.7)], fill=(255, 240, 190, a), width=2)
            dd.line([(cx - s * 1.7, cy), (cx + s * 1.7, cy)], fill=(255, 240, 190, a), width=2)
            dd.line([(cx - s, cy - s), (cx + s, cy + s)], fill=(255, 240, 190, int(a * .6)), width=2)
            dd.line([(cx - s, cy + s), (cx + s, cy - s)], fill=(255, 240, 190, int(a * .6)), width=2)
    return lay, (x0, y0)
