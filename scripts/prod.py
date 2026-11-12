"""Production build of Variation B: a light page for the live site.

Usage: python3 prod.py SRC_DIR OUT_DIR
  SRC_DIR = site/variant-src (index.html + img/)
  OUT_DIR = site/production (made fresh)

What it changes versus the preview (nothing else):
  - removes the yellow preview bar (ad-version + font switchers) and its CSS
  - removes the keyword-swap script (the page always shows the default "repair" version)
  - loads only Zilla Slab + Public Sans from Google Fonts
  - the testimonial video downloads only when it scrolls into view (preload="none"); a smaller re-encode is used only if it is smaller
  - Leaflet + map data + map code move to js/map.js, loaded with defer
  - JPGs re-saved smaller (same pixel size, never cropped), metadata stripped
  - the Google tag + "Calls from website" number swap when scripts/tracking.json is filled in,
    otherwise a marked spot in <head> for it
"""
import os, re, sys, shutil, subprocess
from PIL import Image

SRC, OUT = sys.argv[1], sys.argv[2]
s = open(os.path.join(SRC, 'index.html'), encoding='utf-8').read()
n0 = len(s)

def cut(pattern, text, flags=re.S, count=1, need=True):
    new, k = re.subn(pattern, '', text, count=count, flags=flags)
    if need and k != count:
        sys.exit('pattern not found exactly %d time(s): %s (found %d)' % (count, pattern[:60], k))
    return new

# 1. preview bar + its CSS
s = cut(r'<div class="pv">.*?</label></div>\s*(?=<header class="top">)', s)
s = cut(r'\.pv\{[^}]*\}', s)
s = cut(r'\.pv select\{[^}]*\}', s)
assert 'class="pv"' not in s and '__titanApply(' not in s.replace('window.__titanApply', '')

# 2. keyword-swap script
s = cut(r'<script>\(function\(\)\{\nvar V=\{\nrepair:.*?\}\)\(\);</script>\s*', s)
assert 'utm_term' not in s

# 3. fonts: only the chosen pair
s, k = re.subn(r'https://fonts\.googleapis\.com/css2\?family=Zilla\+Slab[^"]*',
               'https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@600;700&amp;family=Public+Sans:wght@400;500;600;700;800&amp;display=swap', s)
assert k == 1

# 4. video: download only when in view
s, k = re.subn(r'(<video class="tvid"[^>]*?)preload="auto"', r'\1preload="none"', s)
assert k == 1

# 5. map code to an external deferred file
scripts = list(re.finditer(r'<script>(/\* @preserve\n \* Leaflet.*?)</script>\s*<script>(window\.__TITAN_MAPDATA__=.*?)</script>\s*<script>(\(function\(\)\{\nvar f=document\.querySelector\(\'\.area-mapw\'\).*?)</script>', s, re.S))
assert len(scripts) == 1, len(scripts)
m = scripts[0]
os.makedirs(os.path.join(OUT, 'js'), exist_ok=True)
js = m.group(1) + '\n;\n' + m.group(2) + '\n;\n' + m.group(3) + '\n'
# the map code waits for DOMContentLoaded only if needed; with defer the DOM is parsed already
open(os.path.join(OUT, 'js', 'map.js'), 'w', encoding='utf-8').write(js)
s = s[:m.start()] + '<script src="js/map.js" defer></script>' + s[m.end():]

# 6. Google tag + "Calls from website" number swap (from tracking.json), else a marked spot for it
import json
T = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tracking.json'), encoding='utf-8'))
aw, label = T.get('conversion_id', '').strip(), T.get('calls_from_website_label', '').strip()
if aw or label:
    if not re.fullmatch(r'AW-\d{6,12}', aw) or not re.fullmatch(r'[A-Za-z0-9_-]{6,40}', label):
        sys.exit('tracking.json: conversion_id must look like AW-123456789 and the label like AbC-D_efG-h12_34-567')
    # Google swaps every "(425) 307-9165" and tel:+14253079165 on the page for ad visitors; calls from 60 s count
    tag = ('<!-- Google tag + "Calls from website" -->\n'
           '<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n'
           '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
           "gtag('js',new Date());gtag('config','%s');"
           "gtag('config','%s/%s',{'phone_conversion_number':'(425) 307-9165'});</script>") % (aw, aw, aw, label)
    s, k = re.subn(r'(<meta name="viewport"[^>]*>)', lambda m: m.group(1) + '\n' + tag, s, count=1)
else:
    s, k = re.subn(r'(<meta name="viewport"[^>]*>)', r'\1\n<!-- GOOGLE TAG: paste the Google Ads / Google tag (gtag.js) snippet here, right after this line -->', s, count=1)
assert k == 1

open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(s)

# images
src_img, out_img = os.path.join(SRC, 'img'), os.path.join(OUT, 'img')
os.makedirs(out_img, exist_ok=True)
for f in sorted(os.listdir(src_img)):
    a, b = os.path.join(src_img, f), os.path.join(out_img, f)
    if f.endswith('.jpg'):
        im = Image.open(a)
        im.save(b, 'JPEG', quality=80, optimize=True, progressive=True)
        if os.path.getsize(b) >= os.path.getsize(a):
            shutil.copyfile(a, b)
    elif f.endswith('.mp4'):
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', a, '-c:v', 'libx264', '-crf', '27', '-preset', 'slow',
                        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '64k', '-movflags', '+faststart', b], check=True)
        if os.path.getsize(b) >= os.path.getsize(a):
            shutil.copyfile(a, b)
    else:
        shutil.copyfile(a, b)
shutil.copyfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prod_README.txt'), os.path.join(OUT, 'README.txt'))
print('index.html %d -> %d bytes; js/map.js %d bytes' % (n0, len(s), len(js)))
