"""A new 'Washington shoreline at morning' mural: orcas, great blue heron, coast rhododendron."""
import os, random, math
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, 'gen.py')).read()
_src = _src[:_src.index('# ---------- Scene A')].replace('SRC, OUT = sys.argv[1], sys.argv[2]', '')
G = {}; exec(_src, G)
fir, grad, row, f = G['fir'], G['grad'], G['row'], G['f']
import wasym

V = 'viewBox="0 0 1440 420" preserveAspectRatio="xMidYMax slice"'

def ridge(seed, base, amp, n=26):
    r = random.Random(seed); pts = []
    for i in range(n + 1):
        x = -40 + i * (1520 / n); pts.append((x, base - r.uniform(.2, 1) * amp * (0.5 + 0.5 * math.sin(i * .9 + seed))))
    d = 'M-40 %d' % (base + 200)
    for x, y in pts: d += ' L%.1f %.1f' % (x, y)
    return d + ' L1480 %d Z' % (base + 200)

def snowcaps(seed, base, amp, n=26):
    r = random.Random(seed); d = ''
    for i in range(n + 1):
        x = -40 + i * (1520 / n); y = base - r.uniform(.2, 1) * amp * (0.5 + 0.5 * math.sin(i * .9 + seed))
        if base - y > amp * .62:
            d += 'M%.1f %.1f l-9 13 l5 -2 l4 4 l4 -4 l5 2 Z ' % (x, y)
    return d

def forest(seed, x0, x1, base, hmin, hmax, gap):
    r = random.Random(seed); d = []; x = x0
    while x < x1:
        h = r.uniform(hmin, hmax); d.append(fir(x, base + r.uniform(-3, 3), h, h * r.uniform(.36, .46), r)); x += gap * r.uniform(.6, 1.3)
    return ' '.join(d)

def build():
    sky = grad('mSky', 0, '#faf7f2', 300, '#dfe9ef')
    o = []
    o.append('<svg class="ly" %s>%s<rect width="1440" height="420" fill="url(#mSky)"/>'
             '<defs><radialGradient id="mSun"><stop offset="0" stop-color="#fff3d9" stop-opacity=".95"/><stop offset=".35" stop-color="#fde9cf" stop-opacity=".5"/><stop offset="1" stop-color="#fde9cf" stop-opacity="0"/></radialGradient></defs><circle cx="930" cy="230" r="300" fill="url(#mSun)"/></svg>' % (V, sky))
    # Olympics + snow
    o.append('<svg class="ly" %s>%s<path fill="url(#mOly)" d="%s"/><path fill="#fbfcfd" opacity=".9" d="%s"/></svg>'
             % (V, grad('mOly', 200, '#aeb9d2', 290, '#c6cfdf'), ridge(3, 286, 70), snowcaps(3, 286, 70)))
    # far island trees
    o.append('<svg class="ly" %s>%s<path fill="url(#mFar)" d="%s"/></svg>'
             % (V, grad('mFar', 268, '#8296b1', 300, '#93a6bf'), row(41, 300, 10, 22, 9, ground=True, ground_h=8)))
    # water
    shimmer = ''.join('<path d="M%d %d h%d"/>' % (x, y, l) for x, y, l in [(120, 318, 80), (420, 330, 120), (700, 314, 60), (980, 336, 140), (1240, 322, 70), (560, 352, 90), (860, 360, 70), (300, 346, 60)])
    o.append('<svg class="ly" %s>%s<rect y="300" width="1440" height="120" fill="url(#mSea)"/><ellipse cx="930" cy="318" rx="220" ry="22" fill="#fff3dc" opacity=".35"/><g stroke="#fff" stroke-width="1.4" stroke-linecap="round" opacity=".55" class="m-shim">%s</g></svg>'
             % (V, grad('mSea', 300, '#c3d6e1', 384, '#a8c2d3'), shimmer))
    # orcas (re-use the animated pod, moved into this water)
    orc = wasym.orcas().replace('id="waSea"', 'id="mOrcaClip"').replace('url(#waSea)', 'url(#mOrcaClip)').replace('height="347"', 'height="345"')
    orc = orc.replace('translate(905 347)', 'translate(770 345) scale(1.3)').replace('translate(985 349)', 'translate(866 347) scale(1.3)')
    orc = orc.replace('cx="905" cy="348"', 'cx="770" cy="346"').replace('cx="985" cy="350"', 'cx="866" cy="348"')
    o.append(orc)
    # foreground: forests left and right, with rhododendron shrubs at their feet
    o.append('<svg class="ly" %s>%s<path fill="url(#mTree)" d="%s"/><path fill="url(#mTree)" d="%s"/></svg>'
             % (V, grad('mTree', 190, '#41567a', 392, '#2b3d5e'), forest(7, -30, 470, 392, 120, 210, 34), forest(9, 1080, 1480, 392, 120, 220, 34)))
    o.append('<svg class="ly" %s>%s</svg>' % (V, wasym.shrub(388, 394, 120, 22, 5) + wasym.shrub(1040, 395, 110, 20, 9)))
    # driftwood log with a great blue heron on it, near the water's edge
    log = ('<g fill="#9c8a74"><path d="M552 382 h86 a4.5 4.5 0 0 1 0 9 h-86 a4.5 4.5 0 0 1 0 -9 Z"/><circle cx="553" cy="386.5" r="5" fill="#b4a38c"/></g>'
           '<path d="M630 383 l14 -9" stroke="#9c8a74" stroke-width="3" stroke-linecap="round"/>')
    o.append('<svg class="ly" %s>%s%s</svg>' % (V, log, wasym.heron(596, 382, .74, '#34436b')))
    # sand + edge to white
    o.append('<svg class="ly" %s>%s<path fill="url(#mSand)" d="M-60 388 C240 380 520 394 760 388 C1000 382 1220 394 1500 386 L1500 430 L-60 430 Z"/>'
             '<path fill="none" stroke="#fff" stroke-width="2.4" opacity=".9" d="M-60 387 C240 379 520 393 760 387 C1000 381 1220 393 1500 385"/></svg>'
             % (V, grad('mSand', 384, '#f3ece2', 420, '#ffffff')))
    return ('<!-- WA MURAL: morning shoreline (decorative) -->\n<div class="pnw wa-mural" aria-hidden="true">\n  ' + '\n  '.join(o) + '\n</div>\n')

CSS = '''
.wa-mural{height:clamp(210px,24vw,350px);background:linear-gradient(180deg,#faf7f2,#e3ecf1)}
.wa-mural .m-shim path{animation:mShim 6s ease-in-out infinite}
.wa-mural .m-shim path:nth-child(2n){animation-delay:-2s}.wa-mural .m-shim path:nth-child(3n){animation-delay:-4s}
@keyframes mShim{0%,100%{opacity:.25}50%{opacity:.8}}
/* orcas stay at the surface most of the loop, with one short dive */
.wa-mural .wa-orcas .orca{animation:waOrca2 16s ease-in-out infinite}
.wa-mural .wa-orcas .o2{animation-delay:-1.2s}
.wa-mural .wa-orcas .o-blow circle{animation:waBlowB 16s ease-out infinite}
.wa-mural .wa-orcas .o2 .o-blow circle{animation-delay:-1.2s}
.wa-mural .wa-orcas .o-blow circle:nth-child(2){animation-name:waBlowB2}.wa-mural .wa-orcas .o-blow circle:nth-child(3){animation-name:waBlowB3}
.wa-mural .wa-rip ellipse{animation:waRipB 4s ease-in-out infinite}
.wa-mural .wa-rip ellipse:nth-child(2){animation-delay:-1.5s}
@keyframes waOrca2{0%{transform:translate(26px,44px) rotate(8deg)}7%{transform:translate(20px,3px) rotate(3deg)}12%{transform:translate(16px,0) rotate(0)}28%{transform:translate(9px,2.5px) rotate(-1deg)}44%{transform:translate(2px,0) rotate(.6deg)}60%{transform:translate(-5px,2.5px) rotate(-1deg)}76%{transform:translate(-12px,0) rotate(0)}86%{transform:translate(-20px,7px) rotate(-6deg)}93%,100%{transform:translate(-30px,46px) rotate(-12deg)}}
@keyframes waBlowB{0%,8%{opacity:0;transform:scale(.4)}11%{opacity:.85;transform:scale(1)}20%{opacity:0;transform:scale(1.8) translateY(-6px)}46%{opacity:0;transform:scale(.4)}49%{opacity:.75;transform:scale(1)}58%,100%{opacity:0;transform:scale(1.8) translateY(-6px)}}
@keyframes waBlowB2{0%,9%{opacity:0;transform:scale(.4)}12%{opacity:.7;transform:scale(1)}22%{opacity:0;transform:scale(2) translateY(-8px)}47%{opacity:0;transform:scale(.4)}50%{opacity:.6;transform:scale(1)}60%,100%{opacity:0;transform:scale(2) translateY(-8px)}}
@keyframes waBlowB3{0%,10%{opacity:0;transform:scale(.4)}13%{opacity:.55;transform:scale(1)}24%{opacity:0;transform:scale(2.2) translateY(-10px)}48%{opacity:0;transform:scale(.4)}51%{opacity:.45;transform:scale(1)}62%,100%{opacity:0;transform:scale(2.2) translateY(-10px)}}
@keyframes waRipB{0%,100%{opacity:.25;transform:scaleX(.85)}50%{opacity:.6;transform:scaleX(1.1)}}
@media (prefers-reduced-motion:reduce){.wa-mural .m-shim path,.wa-mural .wa-orcas .orca,.wa-mural .wa-orcas .o-blow circle,.wa-mural .wa-rip ellipse{animation:none}.wa-mural .wa-orcas .orca{transform:none}}
'''
