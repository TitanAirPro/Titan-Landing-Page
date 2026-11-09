import random, sys, math
SRC, OUT = sys.argv[1], sys.argv[2]
W = 1440
def f(v): return "%.1f" % v

# ---------- shapes ----------
def fir(x, base, h, w, r):
    n = max(5, int(h / 12)); top = base - h; lean = (r.random() - .5) * w * .08
    def tiers(sign):
        out = []
        for i in range(1, n + 1):
            t = i / n; y = top + h * .965 * t
            hw = w / 2 * (.12 + .88 * t ** .92) * (.76 + .48 * r.random())
            tip = (x + sign * hw, y + h * .022 * (.4 + r.random()))
            ctrl = (x + sign * hw * .6, y - h * .055 * (1 - t * .45))
            inner = (x + sign * hw * (.3 + .14 * r.random()), y - h * .01)
            out.append((ctrl, tip, inner))
        return out
    R = tiers(1); L = tiers(-1); tw = max(1.2, w * .05); apex = (x + lean, top)
    d = "M%s %s" % (f(apex[0]), f(apex[1]))
    for c, tp, inn in R[:-1]:
        d += " Q%s %s %s %s L%s %s" % (f(c[0]), f(c[1]), f(tp[0]), f(tp[1]), f(inn[0]), f(inn[1]))
    c, tp, inn = R[-1]
    d += " Q%s %s %s %s" % (f(c[0]), f(c[1]), f(tp[0]), f(tp[1]))
    d += " L%s %s L%s %s L%s %s L%s %s" % (f(x + tw), f(base - h * .02), f(x + tw), f(base + 2), f(x - tw), f(base + 2), f(x - tw), f(base - h * .02))
    c, tp, inn = L[-1]
    d += " L%s %s" % (f(tp[0]), f(tp[1]))
    for i in range(n - 1, -1, -1):
        c, tp, inn = L[i]
        prev = L[i - 1][2] if i > 0 else apex
        if i < n - 1: d += " L%s %s" % (f(tp[0]), f(tp[1]))
        d += " Q%s %s %s %s" % (f(c[0]), f(c[1]), f(prev[0]), f(prev[1]))
    return d + "Z"
def grad(id, y1, c1, y2, c2):
    return '<defs><linearGradient id="%s" gradientUnits="userSpaceOnUse" x1="0" y1="%d" x2="0" y2="%d"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs>' % (id, y1, y2, c1, c2)
BLUR = '<defs><filter id="pnwBlur" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="5"/></filter></defs>'

def row(seed, base, hmin, hmax, gap, wavy=0, ground=True, gaps=(), only=None, ground_h=900):
    r = random.Random(seed); d = []; x = -40
    while x < W + 40:
        h = r.uniform(hmin, hmax); b = base + wavy * (r.random() - .5)
        ok = not any(a <= x <= c for a, c in gaps) and (only is None or any(a <= x <= c for a, c in only))
        if ok: d.append(fir(x, b, h, h * r.uniform(.36, .46), r))
        x += gap * r.uniform(.6, 1.3)
    if ground:
        d.append("M-60 %d Q360 %d 720 %d T1500 %d L1500 %d L-60 %d Z" % (base, base - 6, base, base, base + ground_h, base + ground_h))
    return " ".join(d)

def smooth(pts):
    # quadratic smoothing through midpoints
    s = "M%s %s" % (f(pts[0][0]), f(pts[0][1]))
    for i in range(1, len(pts) - 1):
        mx = (pts[i][0] + pts[i + 1][0]) / 2; my = (pts[i][1] + pts[i + 1][1]) / 2
        s += " Q%s %s %s %s" % (f(pts[i][0]), f(pts[i][1]), f(mx), f(my))
    s += " L%s %s" % (f(pts[-1][0]), f(pts[-1][1]))
    return s

# ---------- Scene A: Rainier at dusk ----------
import sys as _sys; _sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from rainier import build as _rainier
mountain = _rainier()
lenticular = '<g><path fill="#e2d6dd" opacity=".75" d="M712 101 Q834 72 956 101 Q834 117 712 101 Z"/><path fill="#fff" opacity=".92" d="M714 98 Q834 70 954 98 Q834 112 714 98 Z"/><path fill="#fff" opacity=".8" d="M760 82 Q838 62 916 82 Q838 92 760 82 Z"/></g>'
def cloud(cx, cy, s, o, col="#fff"):
    parts = [(0,0,60,16),(-38,4,34,11),(40,5,38,12),(-8,-10,30,12),(18,-8,26,10)]
    return '<g class="pnw-cloud" filter="url(#pnwBlur)" fill="%s" opacity="%s">' % (col, o) + "".join('<ellipse cx="%s" cy="%s" rx="%s" ry="%s"/>' % (f(cx+a*s), f(cy+b*s), f(c*s), f(d*s)) for a, b, c, d in parts) + "</g>"
clouds_far = cloud(250, 118, 1.3, .8, "#f7dfe4") + cloud(1230, 92, 1.0, .75, "#f4dbe3")
clouds_near = cloud(560, 60, .9, .5, "#f1d3dd") + cloud(1080, 150, .8, .45, "#fbe4e0")
hills = ('<g transform="translate(0 40)"><path fill="#a7a6c6" d="M0 288 C110 266 210 282 320 270 C430 258 520 288 640 284 C760 280 860 300 980 288 C1100 276 1210 292 1300 282 C1370 274 1410 278 1440 276 L1440 900 L0 900 Z"/>'
  '<path fill="#9294b8" d="' + row(9, 300, 8, 16, 7, ground=False) + '"/>'
  '<path fill="#9294b8" d="M0 306 C160 294 300 304 460 298 C640 292 780 310 960 302 C1120 296 1280 306 1440 300 L1440 900 L0 900 Z"/></g>')
back = row(11, 330, 38, 70, 26, wavy=10)
mid = row(23, 365, 60, 110, 34, wavy=8)
front = row(37, 410, 95, 170, 44, wavy=4, gaps=[(950, 1078)], ground=False)
cabin = '''<defs><radialGradient id="pnwWin"><stop offset="0" stop-color="#ffc46b" stop-opacity=".85"/><stop offset="1" stop-color="#ffc46b" stop-opacity="0"/></radialGradient></defs>
<radialGradient id="pnwPuff"><stop offset="0" stop-color="#eef1f6" stop-opacity=".9"/><stop offset="1" stop-color="#eef1f6" stop-opacity="0"/></radialGradient><g class="pnw-smoke" fill="url(#pnwPuff)"><circle cx="1025" cy="342" r="9"/><circle cx="1025" cy="342" r="9"/><circle cx="1025" cy="342" r="9"/><circle cx="1025" cy="342" r="9"/><circle cx="1025" cy="342" r="9"/></g>
<circle cx="997" cy="385" r="26" fill="url(#pnwWin)"/>
<rect x="1021" y="346" width="7" height="20" fill="#14233f"/>
<rect x="985" y="372" width="48" height="27" fill="#2a3f5f"/>
<path fill="#14233f" d="M977 375 L1009 350 L1041 375 Z"/>
<path fill="#e9edf3" opacity=".85" d="M984 369 L1009 350 L1034 369 L1028 369 L1009 355 L990 369 Z"/>
<rect class="pnw-glow" x="991" y="379" width="12" height="10" rx="1" fill="#ffc46b"/>
<rect x="1013" y="382" width="9" height="17" fill="#14233f"/>'''

def bird_svg():
    return '<svg viewBox="0 0 100 30" aria-hidden="true"><g class="wing"><path d="M48.4 15.6 C44 12.4 38.6 8.4 31.6 6.6 C24.6 4.8 15.6 6.4 1.2 12.8 C13.4 10.4 21.6 10 28.4 11 C35 12 41.6 14.6 48.4 18.2 Z"/><path d="M 51.60 15.6 C 56.00 12.4 61.40 8.4 68.40 6.6 C 75.40 4.8 84.40 6.4 98.80 12.8 C 86.60 10.4 78.40 10 71.60 11 C 65.00 12 58.40 14.6 51.60 18.2 Z"/></g><path d="M50 13.4 C51 13.4 51.6 14.4 51.6 15.8 C51.6 17.8 51.1 20 50.7 22 L52 24.4 C51 24.8 49 24.8 48 24.4 L49.3 22 C48.9 20 48.4 17.8 48.4 15.8 C48.4 14.4 49 13.4 50 13.4 Z"/></svg>'
def gull_svg():
    return '<svg viewBox="0 0 40 14" aria-hidden="true"><path class="gull" d="M2 9 Q10 1 20 8 Q30 1 38 9" fill="none" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'

V = 'viewBox="0 0 1440 420" preserveAspectRatio="xMidYMax slice"'
rs2 = random.Random(17)
DUSKSTARS = '<svg class="pnw-stars" viewBox="0 0 1440 240" preserveAspectRatio="xMidYMin slice"><g fill="#fff">' + "".join('<circle class="tw" style="animation-delay:%.1fs;opacity:%.2f" cx="%d" cy="%d" r="%.1f"/>' % (rs2.random() * 4, rs2.uniform(.35, .9) * (1 - y / 260), rs2.uniform(0, 1440), y, rs2.uniform(.7, 1.6)) for y in [rs2.uniform(10, 190) for _ in range(54)]) + '</g></svg>'
sceneA = f'''
<!-- PNW SCENE A: Mount Rainier at dusk (scroll-animated, decorative) -->
<div class="pnw pnw-dusk" data-pnw aria-hidden="true">
  DUSKSTARS
  <svg class="ly" data-speed="40" {V}><defs><radialGradient id="pnwSun"><stop offset="0" stop-color="#ffd690" stop-opacity=".95"/><stop offset=".45" stop-color="#ffc77a" stop-opacity=".45"/><stop offset="1" stop-color="#ffc77a" stop-opacity="0"/></radialGradient></defs><circle cx="1110" cy="262" r="190" fill="url(#pnwSun)"/><circle cx="1110" cy="276" r="32" fill="#ffe2a8" opacity=".9"/></svg>
  <svg class="ly" data-speed="115" data-drift="40" {V}>{BLUR}{clouds_far}</svg>
  <svg class="ly" {V}>{mountain}</svg>
  <svg class="ly" data-speed="0" data-drift="-26" {V}><defs><filter id="pnwSoft" x="-10%" y="-80%" width="120%" height="260%"><feGaussianBlur stdDeviation="2.2"/></filter></defs><g filter="url(#pnwSoft)">{lenticular}</g></svg>
  <svg class="ly" data-speed="80" data-drift="70" {V}>{BLUR}{clouds_near}</svg>
  <svg class="ly" {V}>{hills}</svg>
  <div class="ly pnw-mist" data-speed="18"><div class="pnw-fog"></div></div>
  <svg class="ly" data-speed="26" {V}>{grad("gA1", 262, "#7880a6", 332, "#b6aecb")}<path fill="url(#gA1)" d="{back}"/></svg>
  <div class="pnw-bird far-bird" data-v="18" data-dir="-1" data-off=".7" data-y=".46" data-amp=".03" data-px=".03">{bird_svg()}</div>
  <div class="pnw-bird" data-v="34" data-dir="1" data-off=".28" data-y=".36" data-amp=".055" data-px=".09">{bird_svg()}</div>
  <svg class="ly" data-speed="12" {V}>{grad("gA2", 258, "#3c4a76", 366, "#68709a")}<path fill="url(#gA2)" d="{mid}"/></svg>
  <svg class="ly" {V}>{grad("gA3", 245, "#2c446b", 400, "#1d3157")}<path fill="url(#gA3)" d="{front}"/>{grad("gAG", 403, "#d3dce6", 419, "#ffffff")}<path fill="url(#gAG)" d="M-60 409 Q360 403 720 409 T1500 409 L1500 900 L-60 900 Z"/><path fill="none" stroke="#b9c6d4" stroke-width="1.2" opacity=".7" d="M-60 409 Q360 403 720 409 T1500 409"/><g transform="translate(-249.3 -88.8) scale(1.25)">{cabin}</g></svg>
  <div class="ly pnw-rain far"></div>
  <div class="ly pnw-rain near"></div>
</div>
'''

# ---------- Scene B: Puget Sound in drizzle, ferry crossing ----------
r = random.Random(91); pk = []; x = -30
while x < W + 60:
    pk.append((x, 300 - r.uniform(30, 90) * (0.6 + 0.4 * math.sin(x / 260) ** 2))); x += r.uniform(38, 80)
oly = "M-40 300 " + " ".join("L%s %s L%s %s" % (f(a), f(b), f(a + r.uniform(14, 30)), f(b + r.uniform(18, 34))) for a, b in pk) + " L1480 300 L1480 900 L-40 900 Z"
caps = " ".join("M%s %s L%s %s L%s %s L%s %s Z" % (f(a - 9), f(b + 13), f(a), f(b), f(a + 10), f(b + 14), f(a + 1), f(b + 9)) for a, b in pk if b < 248)
oly_svg = f'{grad("gOly", 210, "#a596bd", 300, "#c4b4d2")}<path fill="url(#gOly)" d="{oly}"/><path fill="#fdeeee" opacity=".95" d="{caps}"/>'
isl_trees = row(5, 296, 9, 18, 9, ground=False, only=[(-40, 470), (1000, 1480)])
islands = f'<path fill="#7f7aa2" d="M-40 302 C40 284 140 276 250 280 C340 283 420 290 480 302 Z M990 302 C1060 290 1160 282 1260 284 C1350 286 1420 292 1480 300 Z"/><path fill="#7f7aa2" d="{isl_trees}"/>'

rg = random.Random(44); glints = []
for i in range(46):
    t = (i + rg.random()) / 46; y = 302 + t ** 1.5 * 70
    spread = 6 + (y - 300) * 1.05; x = 720 + rg.gauss(0, .42) * spread
    ln = (3 + (y - 300) * .42) * rg.uniform(.55, 1.25); th = 1.2 + (y - 300) * .032
    glints.append('<rect class="pnw-glint g%d" x="%s" y="%s" width="%s" height="%s" rx="%s"/>' % (rg.randrange(4), f(x - ln / 2), f(y), f(ln), f(th), f(th / 2)))
GLITTER = ('<defs><radialGradient id="pnwGlow"><stop offset="0" stop-color="#ffd9b0" stop-opacity=".55"/><stop offset="1" stop-color="#ffd9b0" stop-opacity="0"/></radialGradient></defs>'
  '<ellipse cx="720" cy="306" rx="150" ry="16" fill="url(#pnwGlow)"/>'
  '<ellipse cx="720" cy="340" rx="70" ry="44" fill="url(#pnwGlow)" opacity=".7"/>'
  '<g class="pnw-glitter" fill="#fff6e8">' + "".join(glints) + '</g>')
water = '''<defs><linearGradient id="pnwWater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c7a9c6"/><stop offset=".45" stop-color="#a8aed0"/><stop offset="1" stop-color="#cdd7e8"/></linearGradient><linearGradient id="pnwSunPath" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd7ae" stop-opacity=".75"/><stop offset="1" stop-color="#ffd7ae" stop-opacity="0"/></linearGradient></defs>
<rect x="-60" y="300" width="1560" height="600" fill="url(#pnwWater)"/>
GLITTERHERE<g class="pnw-shimmer" stroke="#fff" stroke-linecap="round" opacity=".55" stroke-width="1.6"><path d="M90 318 h70 M260 330 h110 M520 314 h60 M700 340 h130 M980 322 h80 M1160 336 h120 M1330 316 h60 M420 352 h90 M860 358 h70"/></g>'''
water = water.replace('GLITTERHERE', GLITTER)
shore_back = row(78, 388, 100, 170, 26, ground=False, only=[(-40, 280), (300, 450), (1010, 1140), (1200, 1480)])
shore_trees = row(77, 392, 120, 210, 30, ground=False, only=[(-40, 250), (325, 430), (1035, 1125), (1225, 1480)])
shore = f'''{grad("gB1", 230, "#6a6f98", 388, "#a29fc0")}{grad("gB2", 190, "#273659", 392, "#3d4672")}<path fill="url(#gB1)" d="{shore_back}"/><path fill="url(#gB2)" d="{shore_trees}"/>
<defs><linearGradient id="pnwSand" gradientUnits="userSpaceOnUse" x1="0" y1="380" x2="0" y2="418"><stop offset="0" stop-color="#f7e3da"/><stop offset=".45" stop-color="#fbf8f3"/><stop offset="1" stop-color="#ffffff"/></linearGradient></defs><path fill="url(#pnwSand)" d="M-60 380 C200 366 420 390 720 382 C1000 374 1220 392 1500 378 L1500 900 L-60 900 Z"/>
<path fill="none" stroke="#fff" stroke-width="3" opacity=".9" d="M-60 378 C200 364 420 388 720 380 C1000 372 1220 390 1500 376"/>
<g fill="#b6a797"><rect x="560" y="392" width="120" height="9" rx="4.5" transform="rotate(-4 620 396)"/><rect x="842" y="398" width="76" height="7" rx="3.5" transform="rotate(6 880 401)"/></g>
<g fill="#a3927f"><rect x="590" y="402" width="70" height="6" rx="3" transform="rotate(3 625 405)"/><circle cx="566" cy="394" r="6"/></g>'''
ferry = '''<div class="pnw-ferry" data-vy="326" data-v="6" data-dir="-1" data-off=".52" data-px=".02"><svg viewBox="0 0 150 42" aria-hidden="true">
<g class="wake"><path d="M-70 36 Q-30 33 6 35" stroke="#fff" stroke-width="2" fill="none" opacity=".8"/><path d="M-46 39 Q-18 37 8 38" stroke="#fff" stroke-width="1.5" fill="none" opacity=".6"/></g>
<path fill="#fff" stroke="#8ea2b6" stroke-width=".8" d="M3 27 L147 27 L139 37 L11 37 Z"/>
<rect x="9" y="29.5" width="132" height="2.6" fill="#1f6f4a"/>
<rect x="13" y="19" width="124" height="8" fill="#f3f5f7" stroke="#8ea2b6" stroke-width=".6"/>
<g fill="#44607f">WIN</g>
<rect x="33" y="12" width="84" height="7" fill="#fff" stroke="#8ea2b6" stroke-width=".6"/>
<rect x="61" y="6" width="28" height="6" fill="#fff" stroke="#8ea2b6" stroke-width=".6"/>
<rect x="72" y="0" width="6" height="7" fill="#1f6f4a"/>
</svg></div>'''.replace("WIN", "".join('<rect x="%d" y="21.5" width="5" height="3"/>' % (17 + i * 8) for i in range(15)))
gulls = ''.join(f'<div class="pnw-bird gull-bird" data-v="{k}" data-dir="-1" data-off="{o}" data-y="{y}" data-amp="{a}" data-px=".05">{gull_svg()}</div>' for k, o, y, a in ((30, .40, .21, .025), (30.6, .47, .26, .02), (29.4, .53, .17, .022)))
PLANE_SVG = '<div class="pnw-bird pnw-plane" data-v="46" data-dir="1" data-off=".18" data-y=".11" data-amp=".018" data-px=".05"><svg viewBox="0 0 140 60" aria-hidden="true">\n<defs><linearGradient id="pnwFus" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#eef2f6"/><stop offset="1" stop-color="#cfd8e2"/></linearGradient>\n<linearGradient id="pnwFlt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f6f9"/><stop offset="1" stop-color="#c3cdd9"/></linearGradient></defs>\n<path fill="#c9d2dd" d="M38 44.6 C38 43 40 42.2 43 42.2 L114 42.2 C119 42.2 122.6 43.2 125.4 45 C121.6 47 117 47.6 110 47.6 L74 47.6 L70.6 48.8 L45 48.8 C40.6 48.8 38 47.2 38 44.6 Z"/>\n<g stroke="#61768f" stroke-width="1" stroke-linecap="round"><path d="M64 35.4 L59 45.6M90 35.6 L94 45.6M61.6 41.2 L91.6 41.2"/></g>\n<path fill="url(#pnwFlt)" stroke="#7d92a8" stroke-width=".7" d="M31 47.4 C31 45.6 33 44.8 36.4 44.8 L111 44.8 C117 44.8 121 45.9 124.2 48 C120.4 50.2 115.6 50.9 108 50.9 L71 50.9 L67.4 52.4 L39 52.4 C34 52.4 31 50.4 31 47.4 Z"/>\n<path fill="none" stroke="#9aabbe" stroke-width=".6" d="M71 50.9 L71 45"/>\n<path fill="#dfe5ec" stroke="#7d92a8" stroke-width=".6" d="M11.6 27.6 L33 26.4 L33 28.6 L12.4 29.8 Z"/>\n<path fill="url(#pnwFus)" stroke="#7d92a8" stroke-width=".7" d="M16 28.6 L10.2 12.6 C9.9 11.6 10.6 10.9 11.7 10.9 L17.2 10.9 C18.7 10.9 19.7 11.6 20.5 12.8 L31 25.8 Z"/>\n<path fill="#ff7a1c" d="M10.5 12.2 C10.6 11.3 11 10.9 11.7 10.9 L17.2 10.9 C18.7 10.9 19.7 11.6 20.5 12.8 L22.6 15.6 L11.8 15.6 Z"/>\n<path fill="url(#pnwFus)" stroke="#7d92a8" stroke-width=".7" d="M16 28.6 C22 26.4 36 24.6 54 23.2 L60.4 18.4 C64.4 16 70.4 15.2 78.4 15.2 L96 15.4 C101 15.6 104.4 17.8 105.8 21.2 L104.8 33 C100.2 35.4 94 36.3 86 36.3 L58 35.9 C42 35.1 28 32.7 16 30.5 Z"/>\n<path fill="#ff7a1c" d="M21 29 C40 27.6 70 26.6 104.8 26.9 L104.8 29.2 C70 29 40 30 21 31.3 Z"/>\n<path fill="#1d3157" d="M22.4 31.6 C40 30.6 70 29.8 104.7 30 L104.6 31.3 C70 31.2 40 32 23.4 32.8 Z"/>\n<g fill="#5d7896"><path d="M88.6 17.6 L97.4 17.6 C99.8 17.8 101.6 19 102.6 21.2 L88.6 21.4 Z"/><rect x="70" y="18.2" width="7.6" height="4" rx="1.1"/><rect x="79.4" y="18" width="7.4" height="4.2" rx="1.1"/></g>\n<path fill="#fff" opacity=".55" d="M89.4 18.2 L93 18.2 L91 20.8 L89.4 20.8 Z"/>\n<path fill="none" stroke="#9aabbe" stroke-width=".6" d="M67.6 23.4 L67.6 33.6M87.6 22.6 L87.6 34"/>\n<path fill="#2c3e57" d="M104.8 20.4 C108.4 20.6 111.2 21.6 112.6 23.2 L112.6 30.8 C111.2 32.4 108.4 33.2 104.8 33.4 Z"/>\n<path fill="#44607f" d="M112.6 24.4 L116.6 27 L112.6 29.6 Z"/>\n<ellipse class="prop" cx="116.8" cy="27" rx="1.5" ry="12.5" fill="#8ea2b6" opacity=".45"/>\n<path fill="#f6f8fa" stroke="#7d92a8" stroke-width=".7" d="M48.6 14.6 L95 13.4 C96.8 13.4 97.8 14 97.8 14.9 L97.2 16.2 L50.6 17.4 C49.2 17.4 48.6 16.6 48.6 15.7 Z"/>\n<path fill="none" stroke="#61768f" stroke-width="1" stroke-linecap="round" d="M78 16.8 L67.4 31.4"/>\n</svg></div>'
SALMON_SVG = '<div class="pnw-jump"><div class="pnw-salmon"><svg viewBox="0 0 60 22" aria-hidden="true">\n<path fill="#5c7591" d="M8 11 C14 4.5 30 3 44 6.5 C50 8 54 9.6 57 11.2 C54 13 50 14.6 44 15.8 C30 18.6 14 17.4 8 11 Z"/>\n<path fill="#f3e6e1" d="M10 12 C18 15.8 32 16.6 46 14.2 C50 13.4 53 12.6 55.6 11.6 C52 14.4 46 16.2 38 17 C26 18 16 16.4 10 12 Z"/>\n<path fill="#e0867a" opacity=".75" d="M14 11.2 C24 10.4 36 10.4 50 11 C38 12.8 24 12.8 14 11.2 Z"/>\n<path fill="#4b6380" d="M9 11 L1 3.5 L3.5 11 L1 18.5 Z"/>\n<path fill="#4b6380" d="M26 4.6 L31 0.8 L34 4.4 Z"/>\n<circle cx="50.5" cy="9.6" r="1.1" fill="#1d3157"/>\n<g fill="#5f7590" opacity=".6"><circle cx="30" cy="7.6" r=".6"/><circle cx="35" cy="7.2" r=".6"/><circle cx="39" cy="7.8" r=".6"/><circle cx="25" cy="8.4" r=".6"/></g>\n</svg></div></div>\n<div class="pnw-splash"><svg viewBox="0 0 60 30" aria-hidden="true"><ellipse class="ring" cx="30" cy="22" rx="22" ry="4" fill="none" stroke="#fff" stroke-width="1.6"/><ellipse class="ring r2" cx="30" cy="22" rx="14" ry="2.6" fill="none" stroke="#fff" stroke-width="1.2"/><g class="drops" fill="#fff"><circle cx="24" cy="18" r="1.4"/><circle cx="30" cy="15" r="1.7"/><circle cx="36" cy="18" r="1.3"/><circle cx="20" cy="20" r="1"/><circle cx="40" cy="20" r="1"/></g></svg></div>\n<div class="pnw-splash"><svg viewBox="0 0 60 30" aria-hidden="true"><ellipse class="ring" cx="30" cy="22" rx="22" ry="4" fill="none" stroke="#fff" stroke-width="1.6"/><ellipse class="ring r2" cx="30" cy="22" rx="14" ry="2.6" fill="none" stroke="#fff" stroke-width="1.2"/><g class="drops" fill="#fff"><circle cx="24" cy="18" r="1.4"/><circle cx="30" cy="15" r="1.7"/><circle cx="36" cy="18" r="1.3"/><circle cx="20" cy="20" r="1"/><circle cx="40" cy="20" r="1"/></g></svg></div>'
sceneB = f'''
<!-- PNW SCENE B: Puget Sound in drizzle, ferry crossing (scroll-animated, decorative) -->
<div class="pnw pnw-sound" data-pnw aria-hidden="true">
  <svg class="ly" data-speed="0" {V}><defs><radialGradient id="pnwSun2"><stop offset="0" stop-color="#ffd9a8" stop-opacity=".95"/><stop offset=".5" stop-color="#ffc9a0" stop-opacity=".4"/><stop offset="1" stop-color="#ffc9a0" stop-opacity="0"/></radialGradient></defs><circle cx="720" cy="282" r="210" fill="url(#pnwSun2)"/></svg>
  <svg class="ly" data-speed="110" data-drift="50" {V}>{BLUR}{cloud(300, 130, 1.4, .85, "#fff1ec")}{cloud(1150, 110, 1.2, .8, "#fdeae8")}</svg>
  <svg class="ly" {V}>{oly_svg}</svg>
  <svg class="ly" {V}>{islands}</svg>
  <svg class="ly" {V}>{water}</svg>
  <div class="ly pnw-mist pnw-mist-sea" data-speed="30"><div class="pnw-fog"></div></div>
  {ferry}
  SALMON
  {gulls}
  PLANE
  <svg class="ly" {V}>{shore}</svg>
  <div class="ly pnw-rain far"></div>
  <div class="ly pnw-rain near"></div>
</div>
'''

# ---------- Twilight tree line (above the final call section) ----------
NV = 'viewBox="0 0 1440 140" preserveAspectRatio="xMidYMax slice"'
night = f'''
<!-- PNW TWILIGHT TREE LINE (decorative) -->
<div class="pnw pnw-night" data-pnw aria-hidden="true">
  <svg class="ly" data-speed="20" {NV}>{grad("gN1", 40, "#8a82ab", 112, "#bfaecb")}<path fill="url(#gN1)" d="{row(101, 112, 44, 84, 22)}"/></svg>
  <div class="ly pnw-mist pnw-mist-ridge" data-speed="10"><div class="pnw-fog"></div></div>
  <svg class="ly" data-speed="10" {NV}>{grad("gN2", 50, "#454c7c", 128, "#1f3459")}<path fill="url(#gN2)" d="{row(103, 126, 40, 76, 26)}"/></svg>
  <svg class="ly" {NV}>{grad("gN3", 60, "#2a3463", 140, "#1d3157")}<path fill="url(#gN3)" d="{row(107, 133, 38, 72, 30)}"/></svg>
</div>
'''

# ---------- Footer tree line with stars and moon ----------
FV = 'viewBox="0 0 1440 90" preserveAspectRatio="xMidYMax slice"'
rs = random.Random(9)
fstars = "".join('<circle class="tw" style="animation-delay:%.1fs" cx="%d" cy="%d" r="%.1f"/>' % (rs.random() * 4, rs.uniform(0, 1440), rs.uniform(5, 44), rs.uniform(.7, 1.5)) for _ in range(40))
footline = f'''
<!-- PNW FOOTER TREE LINE (decorative) -->
<div class="pnw pnw-line" data-pnw aria-hidden="true">
  <svg class="ly" data-speed="26" {FV}><g fill="#fff" opacity=".8">{fstars}</g><circle cx="860" cy="24" r="10" fill="#f4ecd8"/><circle cx="866" cy="20" r="9" fill="#1d3157"/></svg>
  <svg class="ly" data-speed="16" {FV}><path fill="#16284a" d="{row(51, 80, 30, 54, 18)}"/></svg>
  <svg class="ly" {FV}><path fill="#101c33" d="{row(67, 92, 36, 70, 24)}"/></svg>
</div>
'''

def rain_tile(n, ln, col, sw, seed, size):
    rr = random.Random(seed)
    return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='" + str(size) + "' height='" + str(size) + "'%3E%3Cg stroke='%23" + col + "' stroke-width='" + str(sw) + "' stroke-linecap='round'%3E" + "".join("%%3Cpath d='M%d %d l-%.1f %d'/%%3E" % (rr.uniform(4, size - 4), rr.uniform(2, size - ln - 2), ln / 3.2, ln) for _ in range(n)) + "%3C/g%3E%3C/svg%3E"
rain_far = rain_tile(12, 7, "b4c3d3", .8, 21, 110)
rain_near = rain_tile(5, 16, "9fb1c4", 1.1, 22, 170)
NOISE = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .6 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"

css = '''
/* PNW scenes: Rainier at dusk, Puget Sound with a ferry, snowy and starry tree lines. All drawn in code (no photos).
   Layers move at different speeds on scroll; birds and the ferry cross as you scroll and face the way you scroll. */
.pnw{position:relative;overflow:hidden;pointer-events:none}
.pnw .ly{position:absolute;inset:0;width:100%;height:100%;display:block;will-change:transform}
.pnw svg.ly{overflow:visible}
.pnw-dusk{--skyx:clamp(110px,15vw,210px);height:calc(clamp(240px,30vw,420px) + var(--skyx));background:linear-gradient(180deg,#101c33 0%,#121e38 9%,#18244a 17%,#232c58 25%,#363866 33%,#53496f 41%,#7d6380 49%,#ad8090 57%,#d79f9c 65%,#ecb8a2 73%,#f6c8a8 83%,#f2ba92 100%)}
.pnw-dusk>.ly:not(.pnw-rain){top:var(--skyx);height:calc(100% - var(--skyx))}
.pnw-stars{position:absolute;left:0;top:0;width:100%;height:calc(var(--skyx) + 70px);display:block;pointer-events:none;-webkit-mask-image:linear-gradient(180deg,#000 55%,transparent);mask-image:linear-gradient(180deg,#000 55%,transparent)}
.pnw-dusk .pnw-rain{-webkit-mask-image:linear-gradient(180deg,transparent 0%,transparent 12%,#000 38%,#000 86%,transparent 97%);mask-image:linear-gradient(180deg,transparent 0%,transparent 12%,#000 38%,#000 86%,transparent 97%)}
.pnw-dusk .pnw-rain.far{opacity:.42}.pnw-dusk .pnw-rain.near{opacity:.36}
.pnw-dusk::after{-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 20%,#000 70%,transparent 100%);mask-image:linear-gradient(180deg,transparent 0,#000 20%,#000 70%,transparent 100%)}
.pnw-sound{height:clamp(220px,27vw,390px);background:linear-gradient(180deg,#fff8ef 0%,#fde8da 24%,#f8d2cf 48%,#e7bccb 64%,#cdb7d3 74%)}
.pnw-sound .pnw-rain.far{opacity:.2}.pnw-sound .pnw-rain.near{opacity:.16}
.pnw-night{height:clamp(104px,11vw,160px);background:linear-gradient(180deg,#fff 0%,#fdeee3 26%,#f8d3c9 50%,#e2b4c6 72%,#a99ac2 100%)}
.pnw-mist-ridge{background:none}.pnw-mist-ridge .pnw-fog{top:55%;height:30%;opacity:.55}
.pnw-line{height:clamp(72px,6.5vw,92px);background:radial-gradient(ellipse 70% 90% at 50% 100%,rgba(214,128,160,.34),rgba(214,128,160,0) 70%),repeating-linear-gradient(135deg,rgba(255,255,255,.02) 0 2px,transparent 2px 7px),var(--navy)}
.pnw-mist{background:linear-gradient(180deg,transparent 50%,rgba(255,255,255,.6) 66%,transparent 82%)}
.pnw-bird{position:absolute;left:0;top:0;width:clamp(66px,7vw,108px);will-change:transform}
.pnw-bird.far-bird{width:clamp(36px,3.8vw,56px);opacity:.6}
.pnw-bird.gull-bird{width:clamp(20px,2.2vw,32px)}
.pnw-bird svg{display:block;width:100%;height:auto;fill:#1d3157;overflow:visible;will-change:transform}
.pnw-bird .gull{stroke:#5a5784}
.pnw-bird .wing{transform-box:fill-box;will-change:transform}
.pnw-bird .wing{transform-origin:50% 92%}
.pnw-bird .gull{transform-box:fill-box;transform-origin:50% 70%;will-change:transform}
.pnw-ferry{position:absolute;left:0;top:0;will-change:transform}
.pnw-bird.pnw-plane{width:clamp(96px,10vw,150px)}
.pnw-plane .prop{transform-box:fill-box;transform-origin:center;animation:pnwProp .09s linear infinite alternate}
@keyframes pnwProp{from{transform:scaleY(1)}to{transform:scaleY(.15)}}
.pnw-jump{position:absolute;left:0;top:0;width:100%;overflow:hidden;pointer-events:none}
.pnw-salmon{position:absolute;left:0;top:0;opacity:0;will-change:transform}
.pnw-salmon svg{display:block;width:100%;height:auto;overflow:visible}
.pnw-splash{position:absolute;left:0;top:0;opacity:0;pointer-events:none}
.pnw-splash svg{display:block;width:100%;height:auto;overflow:visible}
.pnw-splash .ring,.pnw-splash .drops{transform-box:fill-box;transform-origin:50% 100%}
.pnw-splash.go{opacity:1}
.pnw-splash.go .ring{animation:pnwRing 1.3s ease-out forwards}
.pnw-splash.go .r2{animation-delay:.12s}
.pnw-splash.go .drops{animation:pnwDrops .7s ease-out forwards}
@keyframes pnwRing{0%{transform:scale(.25);opacity:.95}100%{transform:scale(1.5);opacity:0}}
@keyframes pnwDrops{0%{transform:translateY(4px) scale(.6);opacity:1}60%{opacity:.9}100%{transform:translateY(-6px) scale(1.1);opacity:0}}
.pnw-ferry svg{display:block;width:100%;height:auto;overflow:visible}
.pnw-ferry .wake{transform-box:view-box;transform-origin:75px 0;transform:scaleX(var(--dir,1));transition:transform .4s ease}
.pnw-smoke circle{transform-box:fill-box;transform-origin:center;opacity:0;animation:pnwSmoke 7s ease-out infinite}
.pnw-smoke circle:nth-child(2){animation-delay:1.4s}.pnw-smoke circle:nth-child(3){animation-delay:2.8s}.pnw-smoke circle:nth-child(4){animation-delay:4.2s}.pnw-smoke circle:nth-child(5){animation-delay:5.6s}
@keyframes pnwSmoke{0%{transform:translate(0,0) scale(.5);opacity:0}15%{opacity:.9}60%{opacity:.5}100%{transform:translate(-34px,-96px) scale(2.6);opacity:0}}
.pnw-glow{animation:pnwFlicker 3.2s ease-in-out infinite}
@keyframes pnwFlicker{0%,100%{fill:#ffc46b}40%{fill:#ffb347}70%{fill:#ffd38a}}
.pnw .tw{animation:pnwTw 3.4s ease-in-out infinite}
@keyframes pnwTw{0%,100%{opacity:.9}50%{opacity:.25}}
.pnw-rain{-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 18%,#000 72%,transparent 92%);mask-image:linear-gradient(180deg,transparent 0,#000 18%,#000 72%,transparent 92%)}
.pnw-rain.far{background:url("RAINF") 0 0/110px 110px;opacity:.34;animation:pnwRainF 1.25s linear infinite}
.pnw-rain.near{background:url("RAINN") 0 0/170px 170px;opacity:.3;animation:pnwRainN .62s linear infinite}
@keyframes pnwRainF{to{background-position:-34px 110px}}
@keyframes pnwRainN{to{background-position:-53px 170px}}
.pnw::after{content:"";position:absolute;inset:0;background:url("NOISE") 0 0/180px 180px;opacity:.07;mix-blend-mode:multiply;pointer-events:none;-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 30%,#000 70%,transparent 100%);mask-image:linear-gradient(180deg,transparent 0,#000 30%,#000 70%,transparent 100%)}
.pnw-fog{position:absolute;left:-50%;right:-50%;top:52%;height:26%;background:radial-gradient(closest-side,rgba(255,255,255,.65),rgba(255,255,255,0)) 0 50%/520px 100% repeat-x;opacity:.6;animation:pnwFog 70s linear infinite;will-change:transform}
.pnw-mist-sea{background:none}.pnw-mist-sea .pnw-fog{top:62%;height:18%;opacity:.5;animation-duration:95s}
@keyframes pnwFog{to{transform:translateX(520px)}}
.pnw-cloud{animation:pnwCloud 46s ease-in-out infinite alternate}
@keyframes pnwCloud{from{transform:translateX(-18px)}to{transform:translateX(22px)}}
.pnw-shimmer{animation:pnwShim 9s ease-in-out infinite alternate}
.pnw-glitter{animation:pnwSway 7s ease-in-out infinite alternate}
.pnw-glint{opacity:.5;animation:pnwGlint 2.6s ease-in-out infinite}
.pnw-glint.g1{animation-duration:3.1s;animation-delay:-.8s}.pnw-glint.g2{animation-duration:2.2s;animation-delay:-1.5s}.pnw-glint.g3{animation-duration:3.7s;animation-delay:-2.3s}
@keyframes pnwGlint{0%,100%{opacity:.25}45%{opacity:1}70%{opacity:.5}}
@keyframes pnwSway{from{transform:translateX(-3px)}to{transform:translateX(3px)}}
@keyframes pnwShim{0%{transform:translateX(-10px);opacity:.35}50%{opacity:.65}100%{transform:translateX(12px);opacity:.4}}
@media (prefers-reduced-motion:reduce){.pnw-rain,.pnw-jump,.pnw-splash{display:none}}
'''.replace("RAINF", rain_far).replace("RAINN", rain_near).replace("NOISE", NOISE)

js = '''
<script>
(function(){
  var els=[].slice.call(document.querySelectorAll('[data-pnw]'));
  if(!els.length)return;
  var still=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var TAU=Math.PI*2;
  function clamp(v,a,b){return v<a?a:v>b?b:v;}
  function damp(dt,tau){return 1-Math.exp(-dt/tau);}
  function rnd(a,b){return a+Math.random()*(b-a);}
  var scenes=els.map(function(s){
    return {el:s,vis:false,pc:null,top:0,W:0,H:0,s:1,
      layers:[].slice.call(s.querySelectorAll('[data-speed]')).map(function(l){return {el:l,sp:+l.dataset.speed||0,dr:+l.dataset.drift||0};}),
      movers:[].slice.call(s.querySelectorAll('.pnw-bird,.pnw-ferry')).map(function(m){
        var d=m.dataset,bird=m.classList.contains('pnw-bird')&&!m.classList.contains('pnw-plane');
        return {el:m,svg:m.querySelector('svg'),ferry:m.classList.contains('pnw-ferry'),plane:m.classList.contains('pnw-plane'),bird:bird,
          gull:m.classList.contains('gull-bird'),wings:[].slice.call(m.querySelectorAll('.wing')),stroke:m.querySelector('.gull'),
          v:+d.v||30,dir:+d.dir||1,off:+d.off||.5,y:+d.y||.2,amp:+d.amp||0,px:+d.px||0,vy:+d.vy||0,
          x:null,w:0,wait:0,ph1:rnd(0,TAU),ph2:rnd(0,TAU),f1:rnd(.16,.24),f2:rnd(.37,.52),flap:0,wp:rnd(0,TAU),rot:0,burst:rnd(0,4)};
      }),
      fish:(function(){var f=s.querySelector('.pnw-salmon');return f?{el:f,box:f.parentNode,svg:f.querySelector('svg'),sp:[].slice.call(s.querySelectorAll('.pnw-splash')),k:0,wait:1.6,u:-1}:null;})()};
  });
  /* measure once (and again when the page reflows), never inside the animation frame */
  function measure(){
    var sy=window.scrollY;
    scenes.forEach(function(sc){
      var r=sc.el.getBoundingClientRect();
      sc.top=r.top+sy;sc.W=r.width;sc.H=r.height;var art=sc.el.querySelector('svg.ly'),ah=art?art.getBoundingClientRect().height:sc.H;sc.s=Math.max(sc.W/1440,ah/420);
      sc.movers.forEach(function(m){
        if(m.ferry){m.w=150*sc.s;m.el.style.width=m.w.toFixed(1)+'px';m.el.style.setProperty('--dir',m.dir);}
        else m.w=m.el.offsetWidth;
        if(m.svg&&!m.ferry)m.svg.style.transform='scaleX('+m.dir+')';
        if(m.x==null)m.x=sc.W*m.off-m.w/2;
      });
      if(sc.fish){sc.fish.fw=54*sc.s;sc.fish.wy=sc.H-(420-354)*sc.s;sc.fish.el.style.width=sc.fish.fw.toFixed(1)+'px';sc.fish.box.style.height=sc.fish.wy.toFixed(1)+'px';}
    });
  }
  function splash(F,x,sc){
    var e=F.sp[F.k++%F.sp.length],w=46*sc.s;
    e.style.width=w.toFixed(1)+'px';
    e.style.transform='translate3d('+(x-w/2).toFixed(1)+'px,'+(F.wy-w*.38).toFixed(1)+'px,0)';
    e.classList.remove('go');void e.offsetWidth;e.classList.add('go');
  }
  function fishStep(sc,dt,ferryX,ferryW){
    var F=sc.fish,s=sc.s,W=sc.W;
    if(F.u<0){
      F.wait-=dt;if(F.wait>0)return;
      F.x=W*rnd(.28,.72);
      if(ferryW&&Math.abs(F.x-ferryX)<ferryW*.95){F.x=ferryX+(F.x<ferryX?-1:1)*ferryW*1.05;if(F.x<W*.15||F.x>W*.85)F.x=2*ferryX-F.x;}
      F.dir=Math.random()<.5?-1:1;F.h=rnd(50,80)*s;F.span=rnd(70,110)*s;F.T=rnd(.95,1.2);F.u=0;
      F.svg.style.transform='scaleX('+F.dir+')';F.el.style.opacity=1;splash(F,F.x-F.dir*F.span/2,sc);
    }
    F.u+=dt/F.T;var u=Math.min(1,F.u);
    /* true projectile arc: constant horizontal speed, gravity on the vertical */
    var x=F.x+F.dir*(u-.5)*F.span,y=F.wy-4*F.h*u*(1-u)+F.fw*.12;
    var vy=-4*F.h*(1-2*u),rot=F.dir*Math.atan2(vy,F.span)*57.3;
    F.el.style.transform='translate3d('+(x-F.fw/2).toFixed(1)+'px,'+(y-F.fw*.18).toFixed(1)+'px,0) rotate('+rot.toFixed(1)+'deg)';
    if(F.u>=1){splash(F,x,sc);F.u=-1;F.wait=rnd(3.5,7.5);F.el.style.opacity=0;}
  }
  var t=0,prev=0,raf=0;
  function render(sc,dt){
    var vh=window.innerHeight,y=window.scrollY,W=sc.W,H=sc.H,s=sc.s;
    var target=clamp((y+vh-sc.top)/(vh+H),0,1);
    sc.pc=(sc.pc==null||!dt)?target:sc.pc+(target-sc.pc)*damp(dt,.22);
    var q=sc.pc-.5;
    for(var i=0;i<sc.layers.length;i++){var L=sc.layers[i];
      L.el.style.transform='translate3d('+(q*L.dr).toFixed(2)+'px,'+(q*L.sp).toFixed(2)+'px,0)';}
    var ferryX=0,ferryW=0;
    for(var j=0;j<sc.movers.length;j++){var m=sc.movers[j];
      if(dt){
        if(m.wait>0){m.wait-=dt;}
        else{
          m.x+=m.dir*m.v*s*dt;
          if(m.dir>0&&m.x>W+m.w){m.x=-m.w*1.4;m.wait=m.ferry?rnd(1,3):rnd(1.5,5);m.y0=null;}
          if(m.dir<0&&m.x<-m.w*1.4){m.x=W+m.w;m.wait=m.ferry?rnd(1,3):rnd(1.5,5);m.y0=null;}
        }
      }
      var px=-q*m.px*W, x=m.x+px;
      if(m.ferry){
        ferryX=x+m.w/2;ferryW=m.w;
        var fy=H-(420-m.vy)*s-m.w*.25+Math.sin(t*.8+m.ph1)*.5*s;
        m.el.style.transform='translate3d('+x.toFixed(1)+'px,'+fy.toFixed(1)+'px,0) rotate('+(Math.sin(t*.6+m.ph2)*.4).toFixed(2)+'deg)';
        continue;
      }
      /* flight path: two slow sine waves of different speed give an organic, non-repeating glide */
      var a1=m.amp*H,a2=m.amp*.45*H,w1=TAU*m.f1,w2=TAU*m.f2;
      var yy=H*m.y+a1*Math.sin(w1*t+m.ph1)+a2*Math.sin(w2*t+m.ph2);
      var vy=a1*w1*Math.cos(w1*t+m.ph1)+a2*w2*Math.cos(w2*t+m.ph2), vx=m.v*s;
      var bank=clamp(Math.atan2(vy,vx)*57.3*(m.plane?.55:.8),-16,16)*m.dir;
      m.rot+=(bank-m.rot)*damp(dt||.016,.25);
      m.el.style.transform='translate3d('+x.toFixed(1)+'px,'+yy.toFixed(1)+'px,0) rotate('+m.rot.toFixed(2)+'deg)';
      if(m.bird&&dt){
        /* flap while climbing or on a short random burst, glide while sinking */
        m.burst-=dt;var want=(vy<-a1*w1*.25||m.burst>-.9&&m.burst<0)?1:0;if(m.burst<-.9)m.burst=rnd(2.5,6);
        m.flap+=(want-m.flap)*damp(dt,.28);
        m.wp+=dt*TAU*(m.gull?2.6:2.3);
        var beat=.5-.5*Math.cos(m.wp);
        if(m.gull){if(m.stroke)m.stroke.style.transform='scaleY('+(1-.5*m.flap*beat).toFixed(3)+')';}
        else if(m.wings.length){
          m.wings[0].style.transform='scaleY('+(1-1.5*m.flap*beat).toFixed(3)+')';
        }
      }
    }
    if(sc.fish&&dt)fishStep(sc,dt,ferryX,ferryW);
  }
  function frame(ts){
    raf=0;var dt=prev?Math.min(.05,(ts-prev)/1000):0;prev=ts;t+=dt;
    var any=false;
    for(var i=0;i<scenes.length;i++){if(scenes[i].vis){any=true;render(scenes[i],dt);}}
    if(any)raf=requestAnimationFrame(frame);else prev=0;
  }
  measure();
  if(still){scenes.forEach(function(sc){render(sc,0);});return;}
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){scenes.forEach(function(sc){if(sc.el===e.target)sc.vis=e.isIntersecting;});});
    if(!raf)raf=requestAnimationFrame(frame);
  },{rootMargin:'160px 0px'});
  scenes.forEach(function(sc){render(sc,0);io.observe(sc.el);});
  var mt=0;function remeasure(){clearTimeout(mt);mt=setTimeout(measure,120);}
  addEventListener('resize',remeasure);addEventListener('load',measure);
  if(window.ResizeObserver)new ResizeObserver(remeasure).observe(document.body);
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(measure);
})();
</script>
'''

h = open(SRC).read()
assert 'data-pnw' not in h
def put(anchor, text, before=True):
    global h
    assert h.count(anchor) == 1, anchor
    h = h.replace(anchor, text + anchor if before else anchor + text, 1)
put('\n/* footer */', css)
put('\n<!-- TRUST STRIP -->', sceneA.replace('DUSKSTARS', DUSKSTARS))
put('\n<!-- SERVICES -->', sceneB.replace('PLANE', PLANE_SVG).replace('SALMON', SALMON_SVG))
put('<!-- FINAL CTA -->\n<section class="sec final">', night)
put('<!-- FOOTER -->\n<footer>', footline)
put('</body>', js)
open(OUT, 'w').write(h)
