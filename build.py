#!/usr/bin/env python3
"""Build the Miome preview image set: copies the 20 source PNGs into src/, writes WebP + JPEG
into img/, and emits manifest.json. Run from the preview folder."""
import json, os, shutil, subprocess
from PIL import Image

DL = os.path.expanduser('~/Downloads')
ORDER = [
 ('01','landing','02_29_04'),('02','local-reveal','02_29_13'),('03','photo-and-size','02_29_21'),
 ('04','whats-already-here','02_29_34'),('05','who-else-uses-it','02_29_45'),
 ('06','what-could-miome-consider','02_29_54'),('07','how-far-up-for-going','02_30_06'),
 ('08','what-would-you-love','02_30_17'),('09','who-to-make-room-for','02_30_27'),
 ('10','realistic-possibilities','02_30_45'),('11','how-should-it-feel-full','02_31_29'),
 ('12','how-should-it-feel-short','02_31_20'),('13','budget-and-time','02_31_43'),
 ('14','working-it-out','02_31_55'),('15','one-trade-off','02_32_05'),
 ('16','free-diagnosis','02_32_14'),('17','the-garden-plan','02_32_23'),
 ('18','checkout','02_32_30'),('19','your-garden-record','02_32_43'),
 ('20','outside-the-beta-area','02_33_03'),
]
Q = 78
manifest = []
for n, slug, stamp in ORDER:
    srcpng = f'{DL}/ChatGPT Image Sep 9, 2026, {stamp} PM.png'
    dst = f'src/{n}-{slug}.png'
    if not os.path.exists(dst):
        shutil.copy2(srcpng, dst)
    im = Image.open(dst).convert('RGB')
    w, h = im.size
    webp, jpg = f'img/{n}.webp', f'img/{n}.jpg'
    subprocess.run(['cwebp','-quiet','-q',str(Q),'-m','6','-sharp_yuv',dst,'-o',webp], check=True)
    im.save(jpg, quality=Q, optimize=True, progressive=True)
    manifest.append({'n': n, 'slug': slug, 'w': w, 'h': h,
                     'webp': os.path.getsize(webp), 'jpg': os.path.getsize(jpg)})
    print(n, slug, w, h, manifest[-1]['webp'], manifest[-1]['jpg'])
json.dump(manifest, open('manifest.json','w'), indent=1)
print('TOTAL webp', sum(m['webp'] for m in manifest), 'jpg', sum(m['jpg'] for m in manifest))
