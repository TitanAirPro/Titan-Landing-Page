import random, math
def f(v): return "%.1f" % v
# Rainier from Seattle (north-northwest view): very broad glaciated dome, Liberty Cap shoulder on the left,
# summit dome (Columbia Crest), Little Tahoma as a sharp sub-peak low on the right flank.
OUT = [(100,372),(190,346),(280,318),(370,286),(450,252),(520,218),(580,186),(630,158),(668,136),
       (694,122),(712,112),(728,106),(744,104),(758,105),(772,102),(790,96),(808,91),(826,88),(844,88),
       (862,90),(880,95),(900,103),(922,114),(946,128),(968,142),(984,150),(994,140),(1002,126),(1008,116),
       (1013,113),(1018,120),(1026,138),(1036,158),(1060,172),(1100,190),(1150,210),(1210,234),(1280,262),
       (1360,294),(1440,326),(1520,356)]
def yat(x):
    for (x0,y0),(x1,y1) in zip(OUT, OUT[1:]):
        if x0 <= x <= x1: return y0 + (y1-y0)*(x-x0)/(x1-x0)
    return 420
def smooth(pts):
    s = "M%s %s" % (f(pts[0][0]), f(pts[0][1]))
    for i in range(1, len(pts) - 1):
        mx = (pts[i][0] + pts[i+1][0]) / 2; my = (pts[i][1] + pts[i+1][1]) / 2
        s += " Q%s %s %s %s" % (f(pts[i][0]), f(pts[i][1]), f(mx), f(my))
    return s + " L%s %s" % (f(pts[-1][0]), f(pts[-1][1]))
def build():
    r = random.Random(31)
    body = "M" + " L".join("%d %d" % p for p in OUT) + " L1520 900 L100 900 Z"
    # snowline: high, with broad rounded glacier tongues reaching down the slopes
    xs = list(range(330, 1371, 24)); sn = []
    for x in xs:
        base = 268 + 16 * math.sin(x / 70.0) + 9 * math.sin(x / 31.0 + 1.3)
        tongue = (r.random() ** 2) * 34
        sn.append(max(yat(x) + 10, base + tongue))
    top = [(x, yat(x)) for x in range(330, 1371, 8)]
    low = list(reversed(list(zip(xs, sn))))
    snow = smooth(top) + " " + smooth(low).replace("M", "L", 1) + " Z"
    # rock ridges (cleavers): broken, irregular rock spines, widest mid-slope, tapering both ends
    cleavers = []
    def spine(x0, y0, x1, y1, w, segs=7):
        L = []; R = []
        for k in range(segs + 1):
            t = k / segs; x = x0 + (x1 - x0) * t + r.uniform(-2.5, 2.5); y = y0 + (y1 - y0) * t
            ww = w * math.sin(math.pi * (0.08 + 0.84 * t)) * r.uniform(.6, 1.15)
            L.append((x - ww / 2, y)); R.append((x + ww / 2, y + r.uniform(-1.5, 1.5)))
        return "M" + " L".join("%s %s" % (f(a), f(b)) for a, b in L + list(reversed(R))) + "Z"
    for x0, y0, x1, y1, w in ((664, 156, 600, 238, 15), (742, 124, 716, 232, 10), (872, 118, 930, 214, 16),
                              (930, 140, 1010, 232, 13), (1080, 196, 1150, 252, 12), (612, 186, 560, 250, 9),
                              (812, 132, 806, 196, 6)):
        cleavers.append(spine(x0, y0, x1, y1, w))
    for cx, cy, rw in ((560, 254, 22), (700, 244, 16), (980, 240, 20), (1180, 262, 18), (840, 236, 12)):
        pts = []
        for k in range(9):
            a = k / 9 * math.tau; rr = rw * r.uniform(.55, 1.0)
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr * .38))
        cleavers.append("M" + " L".join("%s %s" % (f(a), f(b)) for a, b in pts) + "Z")
    # Willis Wall: dark cliff band set into the face below Liberty Cap, following the slope
    willis = ("M676 150 C690 140 706 133 722 129 C736 126 750 126 764 128 L770 140 "
              "C758 146 748 152 738 160 C724 168 708 170 694 168 C686 166 680 160 676 150 Z")
    # ridge-and-gully texture: dozens of thin spines radiating from the summit, each with a shadowed gully on its far side
    rr = random.Random(77); gullies = []; lights = []
    for k in range(78):
        xs0 = rr.uniform(470, 1250); y0 = yat(xs0) + rr.uniform(3, 22)
        if y0 > 262: continue
        ln = rr.uniform(46, 150) * (1.15 if abs(xs0 - 832) < 160 else 1)
        dx = (xs0 - 832) * rr.uniform(.12, .3); x1 = xs0 + dx * ln / 100; y1 = min(y0 + ln, 300)
        w = rr.uniform(3.4, 11)
        pts = []
        for q in range(7):
            t = q / 6; pts.append((xs0 + (x1 - xs0) * t + rr.uniform(-1.6, 1.6), y0 + (y1 - y0) * t))
        sh = [(x + w * math.sin(math.pi * (.1 + .8 * i / 6)), y) for i, (x, y) in enumerate(pts)]
        gullies.append("M" + " L".join("%s %s" % (f(a), f(b)) for a, b in pts + list(reversed(sh))) + "Z")
        hl = [(x - w * .45 * math.sin(math.pi * (.1 + .8 * i / 6)), y) for i, (x, y) in enumerate(pts)]
        lights.append("M" + " L".join("%s %s" % (f(a), f(b)) for a, b in pts + list(reversed(hl))) + "Z")
    outcrops = []
    for k in range(34):
        cx = rr.uniform(500, 1220); cy = rr.uniform(yat(cx) + 30, 258)
        if cy < yat(cx) + 24: continue
        rw = rr.uniform(6, 18); pts = []
        for q in range(8):
            a = q / 8 * math.tau; rad = rw * rr.uniform(.5, 1.0)
            pts.append((cx + math.cos(a) * rad, cy + math.sin(a) * rad * rr.uniform(.3, .55)))
        outcrops.append("M" + " L".join("%s %s" % (f(a), f(b)) for a, b in pts) + "Z")
    # glacier flow lines on the snow (subtle)
    flows = []
    for x0 in (610, 680, 760, 800, 870, 930, 990, 1080, 1160):
        y0 = yat(x0) + 10; x1 = x0 + (x0 - 832) * .32; y1 = y0 + r.uniform(70, 110)
        flows.append("M%s %s Q%s %s %s %s" % (f(x0), f(y0), f((x0 + x1) / 2 + r.uniform(-10, 10)), f((y0 + y1) / 2), f(x1), f(y1)))
    # shadow side: everything east of a line from the summit down the north-east ridge
    shade = "M846 86 L862 90 L880 95 L900 103 L922 114 L946 128 L968 142 L984 150 L1520 356 L1520 900 L920 900 L890 300 L866 170 Z"
    # Little Tahoma: darker rocky spike
    tahoma = "M984 150 L994 140 L1002 126 L1008 116 L1013 113 L1018 120 L1026 138 L1036 158 L1018 166 L1004 160 Z"
    svg = ('<defs>'
      '<filter id="pnwSoftM" x="-30%%" y="-80%%" width="160%%" height="260%%"><feGaussianBlur stdDeviation="8"/></filter><clipPath id="pnwMtn"><path d="%s"/></clipPath>'
      '<linearGradient id="pnwRock" x1="0" x2="1"><stop offset="0" stop-color="#a9a9c6"/><stop offset=".55" stop-color="#8f93b5"/><stop offset="1" stop-color="#737a9f"/></linearGradient>'
      '<linearGradient id="pnwSnow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff3ea"/><stop offset=".5" stop-color="#ffdcca"/><stop offset="1" stop-color="#f1c2bd"/></linearGradient>'
      '<radialGradient id="pnwGlowM" cx="560" cy="150" r="420" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ffb08a" stop-opacity=".42"/><stop offset="1" stop-color="#ffc2b0" stop-opacity="0"/></radialGradient>'
      '<linearGradient id="pnwShade" x1="0" x2="1"><stop offset="0" stop-color="#3b3a74" stop-opacity=".26"/><stop offset="1" stop-color="#3b3a74" stop-opacity=".42"/></linearGradient>'
      '</defs><g transform="translate(1670 40) scale(-1 1)">'
      '<path fill="url(#pnwRock)" d="%s"/>'
      '<g clip-path="url(#pnwMtn)">'
      '<path fill="url(#pnwSnow)" d="%s"/>'
      '<ellipse cx="724" cy="150" rx="70" ry="20" fill="#8e8fb3" opacity=".28" filter="url(#pnwSoftM)" data-w="%s"/>'
      '<path fill="#73769c" opacity=".72" d="%s"/>'
      '<path fill="#66628f" opacity=".5" d="%s"/>'
      '<path fill="#fff6ef" opacity=".55" d="%s"/>'
      '<path fill="#6f6b95" opacity=".55" d="%s"/>'
      '<path fill="none" stroke="#d9d3e4" stroke-width="1.3" stroke-linecap="round" opacity=".7" d="%s"/>'
      '<path fill="#6f7299" d="%s"/>'
      '<path fill="#fff" opacity=".8" d="M1008 116 L1013 113 L1018 120 L1013 124 Z"/>'
      '<path fill="url(#pnwShade)" d="%s"/>'
      '<rect x="100" y="0" width="1420" height="420" fill="url(#pnwGlowM)"/>'
      '</g></g>') % (body, body, snow, willis, " ".join(cleavers), " ".join(gullies), " ".join(lights), " ".join(outcrops), " ".join(flows), tahoma, shade)
    return svg
