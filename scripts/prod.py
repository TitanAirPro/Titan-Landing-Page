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
  - photos load lazily with WebP copies (640 px for phones + full size); phones get an 800 px hero photo
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
aw, label, tap = T.get('conversion_id', '').strip(), T.get('calls_from_website_label', '').strip(), T.get('click_to_call_label', '').strip()
if aw or label:
    if not re.fullmatch(r'AW-\d{6,12}', aw) or not re.fullmatch(r'[A-Za-z0-9_-]{6,40}', label):
        sys.exit('tracking.json: conversion_id must look like AW-123456789 and the label like AbC-D_efG-h12_34-567')
    # Google swaps every "(425) 307-9165" and tel:+14253079165 on the page for ad visitors; calls from 60 s count
    tag = ('<!-- Google tag + "Calls from website" -->\n'
           '<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n'
           '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
           "gtag('js',new Date());gtag('config','%s');"
           "gtag('config','%s/%s',{'phone_conversion_number':'(425) 307-9165'});</script>") % (aw, aw, aw, label)
    if tap:
        if not re.fullmatch(r'[A-Za-z0-9_-]{6,40}', tap): sys.exit('tracking.json: click_to_call_label looks wrong')
        # every tap on a call button also counts as a "Click to call" conversion (backup to the 60-second calls)
        tag += ("\n<script>document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^=\"tel:\"]');"
                "if(a&&window.gtag)gtag('event','conversion',{'send_to':'%s/%s'});},true);</script>") % (aw, tap)
    s, k = re.subn(r'(<meta name="viewport"[^>]*>)', lambda m: m.group(1) + '\n' + tag, s, count=1)
else:
    s, k = re.subn(r'(<meta name="viewport"[^>]*>)', r'\1\n<!-- GOOGLE TAG: paste the Google Ads / Google tag (gtag.js) snippet here, right after this line -->', s, count=1)
assert k == 1

# 7. speed: photos load when they scroll near, phones get smaller WebP files, a lighter hero photo on phones
PHOTOS = {}  # name -> width of the original
def _photo(m):
    tag, name = m.group(0), m.group(1)
    w = Image.open(os.path.join(SRC, 'img', name + '.jpg')).size[0]
    PHOTOS[name] = w
    if 'loading=' not in tag: tag = tag.replace('<img ', '<img loading="lazy" ', 1)
    if 'decoding=' not in tag: tag = tag.replace('<img ', '<img decoding="async" ', 1)
    srcset = 'img/%s-640.webp 640w, img/%s.webp %dw' % (name, name, w)
    return tag.replace('<img ', '<img srcset="%s" sizes="(max-width:860px) 100vw, 600px" ' % srcset, 1)
s, k = re.subn(r'<img [^>]*src="img/((?:w\d\d|storefront|sign))\.jpg"[^>]*>', _photo, s)
assert k == 15, k
# slideshow's blurred backdrop: small WebP copies, set only when the slideshow gets near the screen
OLD_BG = "s.forEach(function(f){var im=f.querySelector('img');if(im)f.style.setProperty('--bg','url(\"'+im.getAttribute('src')+'\")');});"
assert s.count(OLD_BG) == 1
s = s.replace(OLD_BG, "var bgs=function(){s.forEach(function(f){var im=f.querySelector('img');if(im)f.style.setProperty('--bg','url(\"'+im.getAttribute('src').replace('.jpg','-640.webp')+'\")');});};"
  "if(window.IntersectionObserver){var bo=new IntersectionObserver(function(e){if(e[0].isIntersecting){bgs();bo.disconnect();}},{rootMargin:'800px'});bo.observe(root);}else bgs();")
# phone hero: an 800 px wide copy (the hero rule inside @media (max-width:640px) is the second one)
hi = [m.start() for m in re.finditer(r'url\("img/tech-fireplace\.jpg"\)', s)]
assert len(hi) == 2 and s.rfind('@media (max-width:640px)', 0, hi[1]) > s.rfind('}}', 0, hi[1])
s = s[:hi[1]] + 'url("img/tech-fireplace-800.jpg")' + s[hi[1] + len('url("img/tech-fireplace.jpg")'):]
s, k = re.subn(r'<link rel="preload" as="image" href="img/tech-fireplace\.jpg" fetchpriority="high">',
    '<link rel="preload" as="image" href="img/tech-fireplace-800.jpg" fetchpriority="high" media="(max-width:640px)">'
    '<link rel="preload" as="image" href="img/tech-fireplace.jpg" fetchpriority="high" media="(min-width:641px)">', s)
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
for name, w in sorted(PHOTOS.items()):
    im = Image.open(os.path.join(SRC, 'img', name + '.jpg')).convert('RGB')
    im.save(os.path.join(out_img, name + '.webp'), 'WEBP', quality=78, method=6)
    im.resize((640, round(im.height * 640 / im.width)), Image.LANCZOS).save(os.path.join(out_img, name + '-640.webp'), 'WEBP', quality=78, method=6)
im = Image.open(os.path.join(SRC, 'img', 'tech-fireplace.jpg')).convert('RGB')
im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS).save(os.path.join(out_img, 'tech-fireplace-800.jpg'), 'JPEG', quality=78, optimize=True, progressive=True)
shutil.copyfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prod_README.txt'), os.path.join(OUT, 'README.txt'))
print('index.html %d -> %d bytes; js/map.js %d bytes' % (n0, len(s), len(js)))
