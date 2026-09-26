#!/usr/bin/env python3
"""Build only a portrait alpha mask. Never repaint or retouch the source RGB.

Manual trimap + OpenCV GrabCut: no downloaded model is required.
The checked-in final alpha makes normal recomposition independent of OpenCV.
"""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / 'vivi-oor'
SOURCE = ROOT / 'Samu/Snapchat-795169778.jpg'

# Approximate external silhouette, in native 720 x 1280 source coordinates.
# Not a new outline for the person: GrabCut refines it against the actual pixels.
OUTLINE = [
    (290,280),(317,280),(348,285),(377,299),(405,322),(427,354),
    (440,388),(445,420),(449,449),(456,475),(456,525),(451,563),
    (454,600),(452,628),(469,615),(484,616),(490,626),(483,638),
    (493,648),(502,666),(514,686),(550,686),(578,690),(600,699),
    (615,702),(639,695),(660,704),(675,693),(686,685),(706,689),
    (720,695),(720,1280),(0,1280),(0,1204),(12,1170),(29,1130),
    (0,1110),(0,805),(22,795),(38,783),(56,781),(72,769),
    (90,777),(143,758),(178,750),(205,739),(217,719),(226,708),
    (215,691),(216,680),(227,665),(244,658),(265,665),(262,650),
    (250,632),(235,604),(222,576),(214,549),(210,523),(204,501),
    (193,476),(190,450),(188,414),(191,383),(199,355),(212,327),
    (229,310),(248,295),(270,285),
]


def main():
    cv2.setRNGSeed(20260926)
    image = Image.open(SOURCE).convert('RGB')
    assert image.size == (720, 1280)
    rgb = np.asarray(image)
    rough = np.zeros(rgb.shape[:2], dtype=np.uint8)
    cv2.fillPoly(rough, [np.asarray(OUTLINE, np.int32)], 255)
    kernel = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n,n))
    inner = cv2.erode(rough, kernel(19))
    outer = cv2.dilate(rough, kernel(27))
    trimap = np.full(rough.shape, cv2.GC_BGD, dtype=np.uint8)
    trimap[outer > 0] = cv2.GC_PR_BGD
    trimap[rough > 0] = cv2.GC_PR_FGD
    trimap[inner > 0] = cv2.GC_FGD
    bg = np.zeros((1,65), np.float64)
    fg = np.zeros((1,65), np.float64)
    cv2.grabCut(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), trimap, None,
                bg, fg, 10, cv2.GC_INIT_WITH_MASK)
    binary = np.where((trimap == cv2.GC_FGD) | (trimap == cv2.GC_PR_FGD),
                      255, 0).astype(np.uint8)
    # Keep one connected subject and fill accidental holes inside the portrait.
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    clean = np.zeros_like(binary)
    cv2.drawContours(clean, [max(contours, key=cv2.contourArea)], -1, 255, cv2.FILLED)
    alpha = Image.fromarray(clean).filter(ImageFilter.GaussianBlur(0.65))
    # Limit feathering to the outer contour; opaque interiors remain exactly 255.
    values = np.asarray(alpha).astype(np.float32)
    values = np.clip((values - 6) * 255 / 243, 0, 255).round().astype(np.uint8)
    alpha = Image.fromarray(values)
    alpha.save(PROJECT / 'assets/portrait_alpha.png')
    work = ROOT / 'work/vivi-oor'
    work.mkdir(parents=True, exist_ok=True)
    portrait = image.convert('RGBA')
    portrait.putalpha(alpha)
    proof = Image.new('RGBA', image.size, (30,54,64,255))
    proof.alpha_composite(portrait)
    proof.convert('RGB').save(work / 'detourage_final.jpg', quality=96)
    print('Alpha saved. Source RGB has not been modified.')


if __name__ == '__main__':
    main()
