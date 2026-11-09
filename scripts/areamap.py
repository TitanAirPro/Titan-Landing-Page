import math, random
# Regional view: Everett (north) to Olympia (south)
LON0, LAT0, LAT1 = -123.10, 48.24, 46.90
W, H = 500, 680
S = H / (LAT0 - LAT1)
K = math.cos(math.radians(47.5))
def P(lat, lon): return ((lon - LON0) * K * S, (LAT0 - lat) * S)

def smooth(pts, closed=True, t=.5):
    pts = [P(*p) for p in pts]; n = len(pts)
    d = 'M%.1f %.1f' % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if closed or i > 0 else pts[0]
        p1 = pts[i]; p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if closed or i + 2 < n else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += ' C%.1f %.1f %.1f %.1f %.1f %.1f' % (c1 + c2 + p2)
    return d + (' Z' if closed else '')

# east shore of Puget Sound, north to south
SHORE = [(48.30,-122.375),(48.20,-122.36),(48.14,-122.372),(48.09,-122.30),(48.06,-122.27),(48.045,-122.215),(48.02,-122.215),(47.99,-122.222),(47.965,-122.248),(47.948,-122.30),(47.92,-122.322),(47.88,-122.332),(47.85,-122.342),(47.812,-122.388),(47.765,-122.386),(47.712,-122.382),(47.674,-122.41),(47.662,-122.432),(47.633,-122.392),(47.612,-122.352),(47.592,-122.352),(47.582,-122.418),(47.545,-122.399),(47.50,-122.385),(47.46,-122.36),(47.40,-122.33),(47.35,-122.335),(47.32,-122.40),(47.29,-122.42),(47.268,-122.43),(47.266,-122.465),(47.29,-122.50),(47.31,-122.53),(47.27,-122.552),(47.22,-122.572),(47.18,-122.60),(47.13,-122.66),(47.10,-122.72),(47.088,-122.78),(47.07,-122.85),(47.058,-122.885),(47.045,-122.903),(47.07,-122.93),(47.11,-122.945)]
KITSAP = [(47.935,-122.565),(47.87,-122.525),(47.80,-122.495),(47.745,-122.52),(47.705,-122.595),(47.65,-122.605),(47.58,-122.585),(47.55,-122.535),(47.50,-122.515),(47.43,-122.548),(47.36,-122.575),(47.30,-122.575),(47.26,-122.585),(47.22,-122.64),(47.185,-122.71),(47.16,-122.80),(47.145,-122.88),(47.135,-122.96),(47.15,-123.2),(48.30,-123.2),(48.30,-122.76),(48.10,-122.745),(47.99,-122.665)]
BAINBRIDGE = [(47.712,-122.52),(47.68,-122.495),(47.62,-122.493),(47.59,-122.512),(47.60,-122.565),(47.655,-122.578),(47.70,-122.56)]
VASHON = [(47.51,-122.465),(47.46,-122.44),(47.40,-122.43),(47.34,-122.44),(47.33,-122.50),(47.40,-122.522),(47.47,-122.512)]
WHIDBEY = [(48.30,-122.405),(48.15,-122.415),(48.06,-122.40),(47.99,-122.375),(47.915,-122.38),(47.905,-122.43),(47.97,-122.50),(48.05,-122.60),(48.15,-122.68),(48.30,-122.70)]
LAKE_WA = [(47.758,-122.262),(47.70,-122.259),(47.672,-122.263),(47.646,-122.283),(47.60,-122.286),(47.565,-122.267),(47.54,-122.263),(47.506,-122.236),(47.502,-122.212),(47.53,-122.201),(47.565,-122.189),(47.61,-122.213),(47.632,-122.239),(47.66,-122.211),(47.70,-122.226),(47.755,-122.255)]
MERCER = [(47.597,-122.236),(47.57,-122.213),(47.535,-122.222),(47.56,-122.246)]
SAMM = [(47.655,-122.107),(47.60,-122.098),(47.551,-122.061),(47.576,-122.06),(47.625,-122.089)]
AMERICAN = [(47.14,-122.57),(47.125,-122.585),(47.11,-122.57),(47.125,-122.555)]

I5 = [(48.30,-122.185),(48.08,-122.19),(47.98,-122.195),(47.91,-122.24),(47.82,-122.288),(47.76,-122.322),(47.67,-122.322),(47.60,-122.323),(47.545,-122.306),(47.47,-122.263),(47.40,-122.27),(47.32,-122.293),(47.26,-122.36),(47.235,-122.44),(47.17,-122.52),(47.11,-122.66),(47.07,-122.75),(47.045,-122.83),(47.03,-122.90),(46.96,-122.95)]
I405 = [(47.82,-122.288),(47.78,-122.206),(47.73,-122.185),(47.64,-122.188),(47.55,-122.183),(47.49,-122.205),(47.462,-122.262)]
I90 = [(47.59,-122.323),(47.586,-122.246),(47.578,-122.185),(47.549,-122.081),(47.52,-121.95),(47.49,-121.80)]
SR520 = [(47.645,-122.322),(47.635,-122.231),(47.632,-122.186),(47.66,-122.126),(47.676,-122.116)]
SR167 = [(47.47,-122.22),(47.38,-122.24),(47.30,-122.24),(47.21,-122.29),(47.19,-122.30)]

CITIES = [  # name, lat, lon, dx, dy, anchor, big
    ("Everett", 47.979, -122.202, 9, 5, "start", 1),
    ("Lynnwood", 47.828, -122.300, 9, 5, "start", 0),
    ("Bothell", 47.762, -122.205, 9, 4, "start", 0),
    ("Seattle", 47.606, -122.332, -10, -4, "end", 1),
    ("Redmond", 47.674, -122.121, 9, 4, "start", 0),
    ("Bellevue", 47.61, -122.194, 9, 5, "start", 0),
    ("Issaquah", 47.530, -122.033, 4, 19, "middle", 0),
    ("Renton", 47.482, -122.210, 9, 5, "start", 0),
    ("Kent", 47.381, -122.235, 9, 5, "start", 0),
    ("Federal Way", 47.322, -122.313, 9, 5, "start", 0),
    ("Tacoma", 47.253, -122.444, -10, -6, "end", 1),
    ("Puyallup", 47.185, -122.293, 9, 5, "start", 0),
    ("Lakewood", 47.172, -122.518, -9, 12, "end", 0),
    ("Olympia", 47.038, -122.900, 10, 14, "start", 1),
]

def inside(pt, poly):
    x, y = pt; c = False; n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
    return c

SVC = {"Gas Fireplace": ("gas", "Gas fireplace"), "Chimney": ("chim", "Chimney"), "Air Duct / Dryer": ("duct", "Air duct & dryer vent")}
MON = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
def sample(pts, closed=True, n=10, t=.5):
    pts = [P(*p) for p in pts]; m = len(pts); out = []
    for i in (range(m) if closed else range(m - 1)):
        p0 = pts[(i - 1) % m] if closed or i > 0 else pts[0]
        p1 = pts[i]; p2 = pts[(i + 1) % m]
        p3 = pts[(i + 2) % m] if closed or i + 2 < m else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        for k in range(n):
            u = k / n; a = (1 - u) ** 3; b = 3 * u * (1 - u) ** 2; c = 3 * u * u * (1 - u); d = u ** 3
            out.append((a * p1[0] + b * c1[0] + c * c2[0] + d * p2[0], a * p1[1] + b * c1[1] + c * c2[1] + d * p2[1]))
    return out

def geo():
    sea = sample(SHORE, closed=False) + [P(48.30, -123.2) if False else P(47.11, -123.3), P(48.4, -123.3), P(48.4, -122.375)]
    islands = [sample(L) for L in (MERCER, KITSAP, BAINBRIDGE, VASHON, WHIDBEY)]
    lakes = [sample(L) for L in (LAKE_WA, SAMM, AMERICAN)]
    return sea, islands, lakes

def mass(x, y, G):
    sea, islands, lakes = G
    for k, L in enumerate(islands):
        if inside((x, y), L): return 'i%d' % k
    if any(inside((x, y), L) for L in lakes) or inside((x, y), sea): return None
    return 'main'

def solid(x, y, m, G, r=3.2):
    return all(mass(x + dx, y + dy, G) == m for dx, dy in ((0, 0), (r, 0), (-r, 0), (0, r), (0, -r)))

def snap(x, y, G):
    m = mass(x, y, G)
    if m and solid(x, y, m, G): return x, y, m
    for rad in range(2, 60, 2):
        for k in range(24):
            a = k / 24 * 6.2832; xx, yy = x + rad * math.cos(a), y + rad * math.sin(a)
            m = mass(xx, yy, G)
            if m and solid(xx, yy, m, G): return xx, yy, m
    return x, y, 'main'

CENTERS = [("Seattle",47.62,-122.33),("Seattle",47.70,-122.32),("Seattle",47.56,-122.386),("Seattle",47.53,-122.29),("Seattle",47.665,-122.385),
 ("Shoreline",47.756,-122.341),("Edmonds",47.811,-122.377),("Lynnwood",47.828,-122.30),("Mountlake Terrace",47.788,-122.308),("Mill Creek",47.860,-122.204),
 ("Mukilteo",47.945,-122.304),("Everett",47.979,-122.202),("Everett",47.91,-122.22),("Marysville",48.052,-122.177),("Arlington",48.199,-122.125),
 ("Lake Stevens",48.015,-122.064),("Snohomish",47.913,-122.098),("Monroe",47.855,-121.971),("Sultan",47.862,-121.817),("Bothell",47.762,-122.205),
 ("Kenmore",47.757,-122.244),("Lake Forest Park",47.757,-122.28),("Woodinville",47.754,-122.163),("Kirkland",47.677,-122.206),("Kirkland",47.71,-122.19),
 ("Redmond",47.674,-122.121),("Redmond",47.69,-122.04),("Duvall",47.742,-121.986),("Carnation",47.648,-121.914),("Bellevue",47.610,-122.201),("Bellevue",47.58,-122.15),
 ("Medina",47.621,-122.233),("Mercer Island",47.571,-122.222),("Sammamish",47.616,-122.036),("Issaquah",47.530,-122.033),("Snoqualmie",47.529,-121.825),
 ("North Bend",47.496,-121.787),("Newcastle",47.530,-122.155),("Renton",47.482,-122.217),("Renton",47.46,-122.15),("Tukwila",47.474,-122.261),("Burien",47.470,-122.347),
 ("SeaTac",47.444,-122.297),("Des Moines",47.401,-122.324),("Kent",47.381,-122.235),("Kent",47.36,-122.17),("Covington",47.358,-122.122),("Maple Valley",47.367,-122.044),
 ("Auburn",47.307,-122.228),("Federal Way",47.322,-122.313),("Milton",47.248,-122.313),("Fife",47.239,-122.357),("Tacoma",47.253,-122.444),("Tacoma",47.21,-122.47),
 ("University Place",47.236,-122.550),("Lakewood",47.172,-122.518),("Gig Harbor",47.329,-122.580),("Puyallup",47.185,-122.293),("Puyallup",47.13,-122.31),
 ("Bonney Lake",47.177,-122.186),("Spanaway",47.104,-122.435),("Graham",47.053,-122.294),("DuPont",47.097,-122.631),("Lacey",47.034,-122.823),
 ("Olympia",47.038,-122.900),("Olympia",47.06,-122.98),("Tumwater",47.007,-122.909),("Yelm",46.942,-122.606)]
def area_of(lat, lon):
    return min(CENTERS, key=lambda c: (c[1]-lat)**2 + ((c[2]-lon)*K)**2)[0]

def pins_svg(jobs, *_):
    import hashlib
    G = geo(); out = []
    order = sorted(range(len(jobs)), key=lambda k: jobs[k]["s"] == "Gas Fireplace")
    for k in order:
        j = jobs[k]
        cx, cy, m = snap(*P(j["lat"], j["lon"]), G)
        h = hashlib.sha256(("%d|%s|%s" % (k, j["d"], j["city"])).encode()).digest()
        r = 5.5 if j["lvl"] == "zip" else 9.0
        x, y = cx, cy
        for t in range(20):
            a = h[t % 32] / 255 * 6.2832; d = (0.3 + h[(t + 7) % 32] / 255 * 0.7) * r
            xx, yy = cx + d * math.cos(a), cy + d * math.sin(a)
            if solid(xx, yy, m, G): x, y = xx, yy; break
        if not (4 < x < W - 4 and 4 < y < H - 4): continue
        cls, word = SVC.get(j["s"], ("other", "Home service"))
        out.append('<circle class="m-job j-%s" cx="%.1f" cy="%.1f" r="%s" data-c="%s" data-m="%s"/>' % (cls, x, y, "4.6" if cls == "gas" else "3.4", area_of(j["lat"], j["lon"]), j["d"][:7]))
    return '<g class="m-jobs">' + "".join(out) + '</g>'

def build(jobs=None):
    sea_poly = [P(*p) for p in SHORE] + [P(47.11, -123.2), P(48.2, -123.2)]
    land_polys = [[P(*p) for p in L] for L in (KITSAP, BAINBRIDGE, VASHON, WHIDBEY)]
    lake_polys = [[P(*p) for p in L] for L in (LAKE_WA, SAMM)]
    sea = smooth(SHORE, closed=False) + ' L%.1f %.1f L%.1f %.1f Z' % (P(47.11, -123.2) + P(48.2, -123.2))
    lands = ''.join('<path class="m-land2" d="%s"/>' % smooth(L) for L in (KITSAP, BAINBRIDGE, VASHON, WHIDBEY))
    lakes = ''.join('<path class="m-wat" d="%s"/>' % smooth(L) for L in (LAKE_WA, SAMM, AMERICAN))
    mercer = '<path class="m-land3" d="%s"/>' % smooth(MERCER)
    roads = ''.join('<path d="%s"/>' % smooth(r, closed=False) for r in (I5, I405, I90, SR520, SR167))
    hull = [(48.215,-122.24),(48.205,-122.07),(48.02,-121.95),(47.88,-121.74),(47.70,-121.86),(47.52,-121.71),(47.42,-121.90),(47.30,-122.00),(47.12,-122.20),(46.925,-122.52),(46.925,-122.80),(46.95,-123.09),(47.12,-123.09),(47.20,-122.70),(47.35,-122.62),(47.55,-122.42),(47.72,-122.42),(47.88,-122.36),(48.05,-122.30),(48.18,-122.33)]
    area = smooth(hull)
    random.seed(11); trees = []
    tries = 0
    while len(trees) < 70 and tries < 20000:
        tries += 1
        lat = random.uniform(47.0, 48.02); lon = random.uniform(-122.98, -121.86)
        x, y = P(lat, lon)
        if not (8 < x < W - 8 and 10 < y < H - 10): continue
        on_land = (not inside((x, y), sea_poly)) or any(inside((x, y), L) for L in land_polys)
        if not on_land or any(inside((x, y), L) for L in lake_polys): continue
        if any(math.hypot(x - P(c[1], c[2])[0], y - P(c[1], c[2])[1]) < 30 for c in CITIES): continue
        if -122.36 < lon < -122.15 and 47.45 < lat < 47.80: continue  # keep Seattle/Bellevue core clear
        if any(math.hypot(x - a, y - b) < 16 for a, b in trees): continue
        if x > 380 and y > 600: continue
        if x > 430 and y < 70: continue
        trees.append((x, y))
    tr = ''.join('<path d="M%.1f %.1f l4 8.6 h-2.1 l3.4 6.1 h-10.6 l3.4 -6.1 h-2.1 Z"/>' % (x, y - 8) for x, y in trees)
    dots = labels = ''
    for n, lat, lon, dx, dy, anc, big in CITIES:
        x, y = P(lat, lon)
        dots += '<circle class="m-dot%s" cx="%.1f" cy="%.1f" r="%.1f"/>' % (' m-big' if big else '', x, y, 6 if big else 4.3)
        labels += '<text class="m-city%s" x="%.1f" y="%.1f" text-anchor="%s">%s</text>' % (' m-big' if big else '', x + dx, y + dy, anc, n)
    def shield(txt, lat, lon, kind):
        x, y = P(lat, lon); w = 10 + 7 * len(txt)
        if kind == 'i':
            return '<g class="m-sh i" transform="translate(%.1f %.1f)"><path d="M%.1f -9 h%.1f c0 7 -2 13 -%.1f 17 c-%.1f -4 -%.1f -10 -%.1f -17 Z"/><text y="3.6" text-anchor="middle">%s</text></g>' % (x, y, -w / 2, w, w / 2, w / 2, w / 2, w / 2, txt)
        return '<g class="m-sh s" transform="translate(%.1f %.1f)"><rect x="%.1f" y="-8" width="%.1f" height="16" rx="8"/><text y="3.6" text-anchor="middle">%s</text></g>' % (x, y, -w / 2, w, txt)
    shields = shield('5', 47.90, -122.248, 'i') + shield('5', 47.13, -122.62, 'i') + shield('405', 47.70, -122.184, 'i') + shield('90', 47.555, -122.09, 'i') + shield('167', 47.28, -122.245, 's')
    water = ''.join('<text class="m-water%s" transform="translate(%.1f %.1f) rotate(%d)" text-anchor="middle">%s</text>' % ((cls,) + P(la, lo) + (rot, t)) for t, la, lo, rot, cls in [
        ("Puget Sound", 47.79, -122.445, -78, ""), ("Lake Washington", 47.70, -122.252, -80, " m-xs")])
    land_lbl = ''.join('<text class="m-hood" x="%.1f" y="%.1f" text-anchor="middle">%s</text>' % (P(la, lo) + (t,)) for t, la, lo in [("Kitsap", 47.62, -122.80), ("Vashon", 47.42, -122.475)])
    pins = pins_svg(jobs or [], sea_poly, land_polys, lake_polys)
    rainier = '<g class="m-rainier" transform="translate(452 655)"><path d="M-30 8 L-14 -8 L-8 -4 L0 -14 L12 -2 L18 -6 L30 8 Z"/><path class="snow" d="M-8 -4 L0 -14 L12 -2 L6 -4 L2 0 L-3 -5 Z"/><text x="-38" y="-8" text-anchor="end">Mt. Rainier</text><text class="m-arrow" x="-38" y="6" text-anchor="end">that way ↘</text></g>'
    north = '<g class="m-n" transform="translate(32 40)"><circle r="15"/><path d="M0 -10 L5 5 L0 2 L-5 5 Z"/><text y="-19" text-anchor="middle">N</text></g>'
    return ('<svg class="amap" viewBox="0 0 %d %d" role="img" aria-label="Map of our service area along Puget Sound, from Everett to Olympia">' % (W, H) +
            '<defs><linearGradient id="amW" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#cfe2ee"/><stop offset="1" stop-color="#bcd5e6"/></linearGradient>'
            '<clipPath id="amC"><rect width="%d" height="%d" rx="18"/></clipPath></defs><g clip-path="url(#amC)">' % (W, H) +
            '<rect class="m-land" width="%d" height="%d"/>' % (W, H) +
            '<path class="m-area" d="%s"/>' % area +
            '<path class="m-wat" d="%s"/>%s%s%s' % (sea, lands, lakes, mercer) +
            '<g class="m-tree">%s</g>' % tr +
            '<path class="m-area-l" d="%s"/>' % area +
            '<g class="m-rd-c">%s</g><g class="m-rd">%s</g>' % (roads, roads) +
            water + land_lbl + pins + shields + dots + labels + rainier + north + '</g></svg>')

if __name__ == '__main__':
    open('map_test.svg', 'w').write(build())
