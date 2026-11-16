#!/usr/bin/env python3
"""Draw the app icons from the site's pylon logo (web/index.html brand SVG). Needs Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw
OUT = Path(__file__).resolve().parents[1] / 'app' / 'icons'
GREEN, CREAM = (39, 58, 48), (240, 232, 214)
PATHS = [[(3,31),(3,8),(15,3),(15,31)], [(25,31),(25,3),(37,8),(37,31)], [(15,14),(25,14)], [(15,27),(25,27)]]
def icon(size, pad):
    s = 4  # draw large, then downsample for smooth lines
    im = Image.new('RGB', (size*s, size*s), GREEN); d = ImageDraw.Draw(im)
    inner = size*s*(1-2*pad); k = inner/40; ox = size*s*pad; oy = size*s*pad + (inner-35*k)/2
    w = max(2, int(2.2*k))
    for path in PATHS:
        pts = [(ox+x*k, oy+y*k) for x, y in path]
        d.line(pts, fill=CREAM, width=w, joint='curve')
        for p in pts: d.ellipse([p[0]-w/2, p[1]-w/2, p[0]+w/2, p[1]+w/2], fill=CREAM)
    return im.resize((size, size), Image.LANCZOS)
OUT.mkdir(parents=True, exist_ok=True)
icon(192, .2).save(OUT/'icon-192.png'); icon(512, .2).save(OUT/'icon-512.png')
icon(512, .28).save(OUT/'icon-maskable-512.png'); icon(180, .2).save(OUT/'apple-touch-icon.png')
print('icons written to', OUT)
