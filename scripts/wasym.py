import json, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- Orca pod surfacing in Puget Sound (scene B) ----------
def orca_body(scale=1.0, cls="orca"):
    # side view, facing left; waterline is y=0 in local coords (body sits above when surfaced)
    return ('<g class="%s"><g class="o-body" transform="scale(%.2f)">'
            '<path fill="#151a24" d="M-58 4 C-50 -6 -30 -13 -6 -14 C14 -15 34 -11 52 -2 C56 0 58 3 58 4 Z"/>'
            '<path fill="#151a24" d="M-4 -13 C-3 -22 0 -33 6 -44 C8 -36 10 -24 18 -13 Z"/>'
            '<path fill="#9aa3b2" opacity=".9" d="M14 -12 C22 -12 30 -9 34 -5 C27 -5 20 -6 14 -8 Z"/>'
            '</g><g class="o-blow"><circle cx="%.1f" cy="-18" r="4"/><circle cx="%.1f" cy="-26" r="5.5"/><circle cx="%.1f" cy="-34" r="4.5"/></g></g>'
            % (cls, scale, -42 * scale, -44 * scale, -40 * scale))

def orcas():
    return ('<svg class="ly wa-orcas" viewBox="0 0 1440 420" preserveAspectRatio="xMidYMax slice" aria-hidden="true">'
            '<defs><clipPath id="waSea"><rect x="0" y="0" width="1440" height="347"/></clipPath></defs>'
            '<g clip-path="url(#waSea)"><g transform="translate(905 347)">' + orca_body(1.0, "orca o1") +
            '</g><g transform="translate(985 349)">' + orca_body(.68, "orca o2") + '</g></g>'
            '<g class="wa-rip"><ellipse cx="905" cy="348" rx="70" ry="3.2"/><ellipse cx="985" cy="350" rx="46" ry="2.4"/></g></svg>')

# ---------- Lighthouse with sweeping beam (twilight tree line) ----------
def lighthouse():
    return ('<svg class="ly wa-light" viewBox="0 0 1440 140" preserveAspectRatio="xMidYMax slice" aria-hidden="true">'
            '<defs><linearGradient id="waBeam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff4cf" stop-opacity=".55"/><stop offset="1" stop-color="#fff4cf" stop-opacity="0"/></linearGradient>'
            '<radialGradient id="waLamp"><stop offset="0" stop-color="#fff6d6"/><stop offset=".4" stop-color="#ffd27a" stop-opacity=".8"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient></defs>'
            '<g transform="translate(898 58)">'
            '<g class="wa-beam"><path d="M0 0 L300 -26 L300 26 Z" fill="url(#waBeam)"/><path d="M0 0 L-300 -26 L-300 26 Z" fill="url(#waBeam)" transform="scale(-1 1) rotate(180)" opacity=".0"/></g>'
            '<circle r="22" fill="url(#waLamp)" class="wa-glow"/>'
            '</g>'
            '<path fill="#1d3157" d="M830 140 C842 112 860 98 880 94 C902 90 926 96 942 110 C952 118 960 130 964 140 Z"/>'
            '<g transform="translate(898 58)">'
            '<path fill="#f4efe6" d="M-8 38 L-5.5 6 L5.5 6 L8 38 Z"/>'
            '<path fill="#c8463a" d="M-7.2 27 L-6.4 18 L6.4 18 L7.2 27 Z"/>'
            '<rect x="-7" y="1" width="14" height="5" fill="#2b3550"/>'
            '<rect x="-4.5" y="-6" width="9" height="7" fill="#ffe7a3"/>'
            '<path fill="#c8463a" d="M-7 -6 L0 -13 L7 -6 Z"/>'
            '<rect x="-0.6" y="-16" width="1.2" height="4" fill="#2b3550"/>'
            '<path fill="#e9e1d2" d="M10 38 L10 28 L22 28 L22 38 Z"/><path fill="#c8463a" d="M8.5 28.5 L16 22 L23.5 28.5 Z"/><rect x="14" y="31" width="3.5" height="4" fill="#ffd27a" class="wa-win"/>'
            '</g></svg>')

# ---------- Willow goldfinch (state bird) perched on the booking card ----------
GOLDFINCH = ('<div class="wa-finch" aria-hidden="true" title="Willow goldfinch, Washington\'s state bird"><svg viewBox="0 0 64 44">'
    '<g class="f-bird">'
    '<path fill="#1a1d24" d="M44 25 L62 31 L60 34 L42 29 Z"/>'
    '<path fill="#f7c815" d="M12 22 C12 13 20 8 28 9 C38 10 46 16 47 25 C48 32 40 37 30 37 C20 37 12 31 12 22 Z"/>'
    '<path fill="#f9da4a" d="M16 27 C20 34 30 37 38 34 C30 36 20 33 16 27 Z"/>'
    '<path fill="#1a1d24" d="M27 18 C33 16 42 18 47 25 C44 30 36 31 30 28 C27 25 26 21 27 18 Z"/>'
    '<path fill="#fff" d="M31 22 C35 21 40 22 43 24 L42 25.4 C39 23.6 35 23 31 23.6 Z"/><path fill="#fff" d="M32 26 C36 25.6 40 26.4 42.5 27.6 L41.6 28.8 C39 27.8 36 27.2 32.6 27.4 Z"/>'
    '<g class="f-head"><path fill="#f7c815" d="M8 14 C8 7 13 3 19 3 C25 3 29 8 28 14 C27 19 22 22 16 22 C11 22 8 19 8 14 Z"/>'
    '<path fill="#1a1d24" d="M10 9 C12 4.6 17 2.8 21 3.4 C20.4 6.4 17 8.6 12.6 9.6 Z"/>'
    '<circle cx="14.6" cy="12.6" r="1.7" fill="#1a1d24"/><circle cx="14.1" cy="12.1" r=".5" fill="#fff"/>'
    '<path fill="#f0a35e" d="M8.4 13 L1.6 15.4 L8.6 17.2 Z"/></g>'
    '<path stroke="#7a5a3a" stroke-width="1.6" stroke-linecap="round" fill="none" d="M26 37 L24 43 M32 37 L33 43"/>'
    '</g></svg></div>')

# ---------- Coast rhododendron (state flower) ----------
def rhodo():
    r = random.Random(4)
    leaves = ''
    for ang, ln in [(-150, 58), (-120, 64), (-60, 62), (-28, 56), (160, 50), (20, 54), (100, 44)]:
        a = math.radians(ang); x2, y2 = 70 + ln * math.cos(a), 70 + ln * math.sin(a)
        nx, ny = -math.sin(a) * 11, math.cos(a) * 11; mx, my = (70 + x2) / 2, (70 + y2) / 2
        leaves += '<path d="M70 70 Q%.1f %.1f %.1f %.1f Q%.1f %.1f 70 70 Z"/>' % (mx + nx, my + ny, x2, y2, mx - nx, my - ny)
    flowers = ''
    for cx, cy, s in [(70, 52, 1), (52, 62, .92), (88, 60, .95), (60, 40, .85), (82, 40, .88), (70, 72, .8), (46, 46, .75), (95, 76, .7)]:
        pet = ''.join('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%d %.1f %.1f)"/>' % (cx, cy - 7 * s, 5.4 * s, 7.6 * s, k * 72 + r.randint(-8, 8), cx, cy) for k in range(5))
        flowers += '<g class="r-fl">%s<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#f9d7e3"/><circle cx="%.1f" cy="%.1f" r="1.2" fill="#9c2f5a"/></g>' % (pet, cx, cy, 2.6 * s, cx + 1.5, cy - 1.5)
    return ('<div class="wa-rhodo" aria-hidden="true" title="Coast rhododendron, Washington\'s state flower"><svg viewBox="0 0 140 140">'
            '<g fill="#2f6b4c">' + leaves + '</g><g fill="none" stroke="#24563c" stroke-width="1" opacity=".5">' +
            '</g><g fill="#e8779f">' + flowers + '</g></svg></div>')

# ---------- Western hemlock bough (state tree) ----------
def hemlock():
    r = random.Random(11)
    stem = 'M2 6 C40 10 80 22 120 46 C140 58 156 72 168 90'
    def pt(t):
        # cubic points
        P = [(2, 6), (40, 10), (80, 22), (120, 46)] if t < .7 else [(120, 46), (140, 58), (156, 72), (168, 90)]
        u = t / .7 if t < .7 else (t - .7) / .3
        x = sum(c[0] * w for c, w in zip(P, [(1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3]))
        y = sum(c[1] * w for c, w in zip(P, [(1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3]))
        return x, y
    nd = ''
    for i in range(70):
        t = .04 + i / 72; x, y = pt(t); L = 9 * (1 - t * .55)
        for sgn in (-1, 1):
            a = math.radians(70 * sgn + 30 + r.uniform(-12, 12))
            nd += 'M%.1f %.1f l%.1f %.1f' % (x, y, L * math.cos(a), L * math.sin(a))
    twigs = ''
    for t0, ang, ln in [(.25, 70, 34), (.45, 60, 40), (.62, 75, 30), (.35, -20, 26)]:
        x, y = pt(t0); a = math.radians(ang)
        x2, y2 = x + ln * math.cos(a), y + ln * math.sin(a); twigs += 'M%.1f %.1f L%.1f %.1f' % (x, y, x2, y2)
        for k in range(10):
            u = (k + 1) / 11; xx, yy = x + (x2 - x) * u, y + (y2 - y) * u; L = 7 * (1 - u * .5)
            for sgn in (-1, 1):
                b = a + math.radians(65 * sgn); nd += 'M%.1f %.1f l%.1f %.1f' % (xx, yy, L * math.cos(b), L * math.sin(b))
    cones = ''.join('<ellipse cx="%.1f" cy="%.1f" rx="3.2" ry="5" fill="#8a6a45"/>' % (pt(t)[0] + dx, pt(t)[1] + 9) for t, dx in [(.5, 2), (.56, -3), (.82, 1)])
    return ('<div class="wa-hem" aria-hidden="true" title="Western hemlock, Washington\'s state tree"><svg viewBox="0 0 180 120">'
            '<path d="%s%s" fill="none" stroke="#5a4632" stroke-width="2.2" stroke-linecap="round"/>' % (stem, twigs) +
            '<path d="%s" fill="none" stroke="#2f5d46" stroke-width="2" stroke-linecap="round"/>' % nd + cones + '</svg></div>')

# ---------- Washington outline (footer) ----------
def wa_outline():
    d = json.load(open(os.path.join(HERE, 'geo/wa_outline.json')))
    sx, sy = d['sea']
    return ('<div class="wa-made"><svg viewBox="-2 -2 %d %d" aria-hidden="true"><path d="%s" fill="#1d3a66" stroke="#4d6a96" stroke-width="1.2" stroke-linejoin="round"/>'
            '<circle cx="%.1f" cy="%.1f" r="9" fill="#ff7a1c" opacity=".25"/><circle cx="%.1f" cy="%.1f" r="4.2" fill="#ff7a1c" stroke="#fff" stroke-width="1.6"/></svg>'
            '<span>Locally owned and operated<br>in Washington State</span></div>') % (d['w'] + 4, d['h'] + 4, d['d'], sx, sy, sx, sy)

CSS = '''
/* ---------- Washington symbols ---------- */
.wa-orcas .orca{animation:waOrca 12s cubic-bezier(.45,.05,.4,1) infinite}
.wa-orcas .o2{animation-delay:.9s}
.wa-orcas .o-blow circle{fill:#fff;opacity:0;transform-box:fill-box;transform-origin:center;animation:waBlow 12s ease-out infinite}
.wa-orcas .o2 .o-blow circle{animation-delay:.9s}
.wa-orcas .o-blow circle:nth-child(2){animation-name:waBlow2}.wa-orcas .o-blow circle:nth-child(3){animation-name:waBlow3}
@keyframes waOrca{0%{transform:translate(18px,48px) rotate(9deg)}9%{transform:translate(8px,10px) rotate(5deg)}17%{transform:translate(-6px,1px) rotate(0)}27%{transform:translate(-20px,6px) rotate(-6deg)}36%,100%{transform:translate(-34px,52px) rotate(-12deg)}}
@keyframes waBlow{0%,9%{opacity:0;transform:scale(.4)}12%{opacity:.85;transform:scale(1)}22%,100%{opacity:0;transform:scale(1.8) translateY(-6px)}}
@keyframes waBlow2{0%,10%{opacity:0;transform:scale(.4)}13%{opacity:.7;transform:scale(1)}24%,100%{opacity:0;transform:scale(2) translateY(-8px)}}
@keyframes waBlow3{0%,11%{opacity:0;transform:scale(.4)}14%{opacity:.55;transform:scale(1)}26%,100%{opacity:0;transform:scale(2.2) translateY(-10px)}}
.wa-rip ellipse{fill:none;stroke:#fff;stroke-width:1.2;opacity:0;transform-box:fill-box;transform-origin:center;animation:waRip 12s ease-out infinite}
.wa-rip ellipse:nth-child(2){animation-delay:.9s}
@keyframes waRip{0%,8%{opacity:0;transform:scaleX(.4)}14%{opacity:.7}40%,100%{opacity:0;transform:scaleX(1.25)}}
.wa-light .wa-beam{transform-box:view-box;transform-origin:898px 58px;animation:waBeam 9s ease-in-out infinite;mix-blend-mode:screen}
@keyframes waBeam{0%{transform:rotate(-168deg)}50%{transform:rotate(-12deg)}100%{transform:rotate(-168deg)}}
.wa-light .wa-glow{animation:waGlow 3s ease-in-out infinite}
@keyframes waGlow{0%,100%{opacity:.75}50%{opacity:1}}
.plan-call{position:relative}
.wa-finch{position:absolute;right:26px;top:-34px;width:62px;z-index:2;pointer-events:none}
.wa-finch svg{display:block;width:100%;height:auto;overflow:visible}
.wa-finch .f-bird{transform-box:fill-box;transform-origin:50% 100%;animation:waHop 7s ease-in-out infinite}
.wa-finch .f-head{transform-box:fill-box;transform-origin:70% 80%;animation:waTilt 7s ease-in-out infinite}
@keyframes waHop{0%,62%,72%,100%{transform:translateY(0)}66%{transform:translateY(-7px)}69%{transform:translateY(0) scaleY(.94)}}
@keyframes waTilt{0%,20%,34%,100%{transform:rotate(0)}24%,30%{transform:rotate(-12deg)}80%,88%{transform:rotate(8deg)}}
#call{position:relative;overflow:hidden}
.wa-rhodo{position:absolute;right:-26px;top:-18px;width:170px;opacity:.95;pointer-events:none;transform-origin:80% 20%;animation:waSway 9s ease-in-out infinite}
.wa-rhodo svg{display:block;width:100%;height:auto}
@keyframes waSway{0%,100%{transform:rotate(0)}50%{transform:rotate(2.5deg)}}
.owner-sec{position:relative;overflow:hidden}
.wa-hem{position:absolute;left:-10px;top:-6px;width:230px;opacity:.9;pointer-events:none;transform-origin:0 0;animation:waSway 11s ease-in-out infinite}
.wa-hem svg{display:block;width:100%;height:auto}
.wa-made{display:flex;align-items:center;gap:12px;margin-top:16px}
.wa-made svg{width:74px;height:auto;flex:none}
.wa-made span{font:600 .8rem/1.35 var(--body);color:#c9d2e3}
.split-txt li .ico.ev{stroke-width:1.6;color:#8fd1a8}
@media (max-width:820px){footer .wa-made{justify-content:center}}
@media (max-width:640px){.wa-rhodo{width:84px;right:-24px;top:-22px}.wa-hem{width:150px}.wa-finch{width:52px;top:-29px;right:18px}}
@media (prefers-reduced-motion:reduce){.wa-orcas .orca,.wa-orcas .o-blow circle,.wa-rip ellipse,.wa-light .wa-beam,.wa-light .wa-glow,.wa-finch .f-bird,.wa-finch .f-head,.wa-rhodo,.wa-hem{animation:none}.wa-orcas .orca{transform:translate(-6px,1px)}}
'''

def apply(h, rep):
    # orcas: behind the shore layer of the Puget Sound scene
    i = h.index('id="pnwSand"'); k = h.rindex('<svg class="ly"', 0, i)
    h = h[:k] + orcas() + '\n  ' + h[k:]
    # lighthouse: on top of the twilight tree line
    a = h.index('<div class="pnw pnw-night"'); b = h.index('\n</div>', a)
    h = h[:b] + '\n  ' + lighthouse() + h[b:]
    return h

# ================= v2: symbols live inside the scenes =================
def heron(x, y, s=1.0, col="#2b3658"):
    return ('<g transform="translate(%.1f %.1f) scale(%.2f)" class="wa-heron">'
            '<path d="M1 0 L3 -27 M7 0 L6 -27 M-3 0 L5 0 M3 0 L11 0" stroke="%s" stroke-width="1.5" stroke-linecap="round" fill="none"/>'
            '<path fill="%s" d="M-5 -27 C-9 -35 -5 -45 7 -47 C19 -49 29 -41 33 -30 C34 -27 31 -25 27 -26 C17 -25 6 -24 -5 -27 Z"/>'
            '<g class="wa-hneck"><path d="M-1 -44 C-9 -51 -1 -58 -5 -65 C-9 -72 -5 -78 1 -79" stroke="%s" stroke-width="4.6" stroke-linecap="round" fill="none"/>'
            '<ellipse cx="1" cy="-79.5" rx="4.6" ry="3.6" fill="%s"/><path fill="%s" d="M-2.6 -81 L-20 -78.6 L-2.6 -77.2 Z"/>'
            '<path d="M4 -82 L14 -85.5" stroke="%s" stroke-width="1.1" stroke-linecap="round"/></g></g>') % (x, y, s, col, col, col, col, col, col)

def shrub(x, y, w, h, seed):
    """Low rhododendron shrub at the foot of the forest, in the scene's own tree colour."""
    r = random.Random(seed); n = 6; pts = []
    for i in range(n + 1):
        u = i / n; pts.append((x + u * w, y - h * (0.45 + 0.55 * math.sin(math.pi * u)) * r.uniform(.85, 1.05)))
    d = 'M%.1f %.1f' % (x - 4, y)
    for i in range(n):
        (x1, y1), (x2, y2) = pts[i], pts[i + 1]
        d += ' Q%.1f %.1f %.1f %.1f' % ((x1 + x2) / 2, min(y1, y2) - h * .3, x2, y2)
    d += ' L%.1f %.1f Z' % (x + w + 4, y)
    blooms = ''
    for i in range(6):
        tx = x + (i + .5) / 6 * w + r.uniform(-5, 5); ty = y - h * (.55 + .4 * math.sin(math.pi * (i + .5) / 6)) + r.uniform(1, 5)
        for k in range(6):
            a = k / 6 * 6.283 + r.uniform(0, .6); rr = r.uniform(1.6, 3.6)
            blooms += '<circle cx="%.1f" cy="%.1f" r="%.1f"/>' % (tx + math.cos(a) * rr, ty + math.sin(a) * rr * .75, r.uniform(1.7, 2.5))
    return '<g class="wa-shrub"><path fill="#34406a" d="%s"/><g fill="#d98aa8" opacity=".95">%s</g></g>' % (d, blooms)

def scene_b_extras():
    return ('<svg class="ly wa-shore" viewBox="0 0 1440 420" preserveAspectRatio="xMidYMax slice" aria-hidden="true">' +
            heron(566, 377, .62, '#3b4772') + '<g stroke="#fff" stroke-linecap="round" opacity=".55"><path d="M556 379.5 h20 M560 382.5 h12" stroke-width="1"/></g>' + shrub(418, 386, 92, 18, 5) + shrub(996, 386, 84, 16, 9) + '</svg>')

def lighthouse2():
    firs = ''
    for fx, fh in [(846, 30), (858, 38), (934, 34), (946, 26), (872, 22)]:
        firs += '<path d="M%d %d L%d %d L%d %d Z M%d %d L%d %d L%d %d Z"/>' % (fx - 7, 112, fx, 112 - fh, fx + 7, 112, fx - 9, 118, fx, 112 - fh * .55, fx + 9, 118)
    return ('<svg class="ly wa-light" viewBox="0 0 1440 140" preserveAspectRatio="xMidYMax slice" aria-hidden="true">'
            '<defs><linearGradient id="waBeam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff2c4" stop-opacity=".7"/><stop offset=".55" stop-color="#ffe7a8" stop-opacity=".18"/><stop offset="1" stop-color="#ffe7a8" stop-opacity="0"/></linearGradient>'
            '<radialGradient id="waLamp"><stop offset="0" stop-color="#fff8e0"/><stop offset=".35" stop-color="#ffd98a" stop-opacity=".85"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="waHead" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3463"/><stop offset="1" stop-color="#1d3157"/></linearGradient></defs>'
            '<g transform="translate(898 64)"><g class="wa-beam"><path d="M0 0 L360 -30 L360 30 Z" fill="url(#waBeam)"/></g><circle r="26" fill="url(#waLamp)" class="wa-glow"/></g>'
            '<path fill="url(#waHead)" d="M790 140 C808 124 826 114 852 110 C872 107 884 104 898 104 C914 104 930 108 950 114 C972 120 992 130 1006 140 Z"/>'
            '<g fill="#1d3157">' + firs + '</g>'
            '<g transform="translate(898 64)">'
            '<path fill="#f1ece2" d="M-7.5 40 L-5.2 7 L5.2 7 L7.5 40 Z"/><path fill="#d9d1c2" d="M1.5 40 L1.2 7 L5.2 7 L7.5 40 Z"/>'
            '<path fill="#c24a3e" d="M-6.8 29 L-6 20 L6 20 L6.8 29 Z"/>'
            '<rect x="-7.5" y="3" width="15" height="4" rx="1" fill="#26304f"/>'
            '<rect x="-4.6" y="-5" width="9.2" height="8" fill="#fff0c2"/><path d="M-4.6 -1 H4.6 M-1.5 -5 V3 M1.5 -5 V3" stroke="#e6c47c" stroke-width=".5"/>'
            '<path fill="#c24a3e" d="M-6.5 -5 L0 -12 L6.5 -5 Z"/><circle cx="0" cy="-13" r="1.2" fill="#26304f"/>'
            '<path fill="#e9e2d4" d="M11 40 V31 H24 V40 Z"/><path fill="#c24a3e" d="M9.5 31.6 L17.5 25 L25.5 31.6 Z"/><rect x="15.5" y="33.5" width="3.4" height="4" fill="#ffd98a" class="wa-win"/>'
            '</g></svg>')

def wa_outline2():
    d = json.load(open(os.path.join(HERE, 'geo/wa_outline.json')))
    sx, sy = d['sea']
    return ('<div class="wa-made"><svg viewBox="-3 -3 %d %d" aria-hidden="true"><path d="%s" fill="rgba(143,166,201,.10)" stroke="#8fa6c9" stroke-width="1.1" stroke-linejoin="round"/>'
            '<circle class="wa-ping" cx="%.1f" cy="%.1f" r="5" fill="none" stroke="#ff7a1c" stroke-width="1.5"/><circle cx="%.1f" cy="%.1f" r="3.6" fill="#ff7a1c"/></svg>'
            '<span>Locally owned and operated<br>in Washington State</span></div>') % (d['w'] + 6, d['h'] + 6, d['d'], sx, sy, sx, sy)

CSS2 = '''
/* ---------- Washington symbols (v2: inside the scenes) ---------- */
.wa-orcas .orca{animation:waOrca 12s cubic-bezier(.45,.05,.4,1) infinite}
.wa-orcas .o2{animation-delay:.9s}
.wa-orcas .o-blow circle{fill:#fff;opacity:0;transform-box:fill-box;transform-origin:center;animation:waBlow 12s ease-out infinite}
.wa-orcas .o2 .o-blow circle{animation-delay:.9s}
.wa-orcas .o-blow circle:nth-child(2){animation-name:waBlow2}.wa-orcas .o-blow circle:nth-child(3){animation-name:waBlow3}
@keyframes waOrca{0%{transform:translate(18px,48px) rotate(9deg)}9%{transform:translate(8px,10px) rotate(5deg)}17%{transform:translate(-6px,1px) rotate(0)}27%{transform:translate(-20px,6px) rotate(-6deg)}36%,100%{transform:translate(-34px,52px) rotate(-12deg)}}
@keyframes waBlow{0%,9%{opacity:0;transform:scale(.4)}12%{opacity:.85;transform:scale(1)}22%,100%{opacity:0;transform:scale(1.8) translateY(-6px)}}
@keyframes waBlow2{0%,10%{opacity:0;transform:scale(.4)}13%{opacity:.7;transform:scale(1)}24%,100%{opacity:0;transform:scale(2) translateY(-8px)}}
@keyframes waBlow3{0%,11%{opacity:0;transform:scale(.4)}14%{opacity:.55;transform:scale(1)}26%,100%{opacity:0;transform:scale(2.2) translateY(-10px)}}
.wa-rip ellipse{fill:none;stroke:#fff;stroke-width:1.2;opacity:0;transform-box:fill-box;transform-origin:center;animation:waRip 12s ease-out infinite}
.wa-rip ellipse:nth-child(2){animation-delay:.9s}
@keyframes waRip{0%,8%{opacity:0;transform:scaleX(.4)}14%{opacity:.7}40%,100%{opacity:0;transform:scaleX(1.25)}}
.wa-hneck{transform-box:fill-box;transform-origin:50% 100%;animation:waPreen 14s ease-in-out infinite}
@keyframes waPreen{0%,70%,100%{transform:rotate(0)}76%,84%{transform:rotate(-7deg)}}
.wa-light .wa-beam{transform-box:view-box;transform-origin:898px 64px;animation:waBeam 10s ease-in-out infinite}
@keyframes waBeam{0%{transform:rotate(-172deg)}50%{transform:rotate(-8deg)}100%{transform:rotate(-172deg)}}
.wa-light .wa-glow{animation:waGlow 3s ease-in-out infinite}
@keyframes waGlow{0%,100%{opacity:.8}50%{opacity:1}}
.wa-made{display:flex;align-items:center;gap:12px;margin-top:16px}
.wa-made svg{width:70px;height:auto;flex:none;overflow:visible}
.wa-made span{font:600 .8rem/1.35 var(--body);color:#c9d2e3}
.wa-ping{transform-box:fill-box;transform-origin:center;animation:waPing 2.6s ease-out infinite}
@keyframes waPing{0%{transform:scale(.6);opacity:1}100%{transform:scale(2.6);opacity:0}}
.split-txt li .ico.ev{stroke-width:1.6;color:#8fd1a8}
@media (max-width:820px){footer .wa-made{justify-content:center}}
@media (prefers-reduced-motion:reduce){.wa-orcas .orca,.wa-orcas .o-blow circle,.wa-rip ellipse,.wa-light .wa-beam,.wa-light .wa-glow,.wa-hneck,.wa-ping{animation:none}.wa-orcas .orca{transform:translate(-6px,1px)}}
'''

def apply2(h):
    i = h.index('id="pnwSand"'); k = h.rindex('<svg class="ly"', 0, i)
    h = h[:k] + orcas() + '\n  ' + h[k:]
    i = h.index('id="pnwSand"'); e = h.index('</svg>', i) + 6
    h = h[:e] + '\n  ' + scene_b_extras() + h[e:]
    a = h.index('<div class="pnw pnw-night"'); b = h.index('\n</div>', a)
    h = h[:b] + '\n  ' + lighthouse2() + h[b:]
    return h
