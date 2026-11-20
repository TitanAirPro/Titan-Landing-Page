"""DRAFT roofing landing page (roof replacement, repair, service) in the same design.

Usage: python3 roofpage.py site/main-src/index.html site/roofing-built/index.html

Made from the main chimney & fireplace page. Everything that is Titan's own proof is taken
out, because it would be false on a roofing company's page: reviews, the 849 / 4.9 numbers,
the job map, crew photos, the video, the owner section, the phone number, hours, logo and
city list. Facts we don't have yet are shown in [brackets] for the owner to fill in.
Nothing here is invented: no reviews, no numbers, no license, no brand names.
ASSUMED (owner to confirm): the offer is a free roof inspection.
"""
import re, sys

src, out = sys.argv[1], sys.argv[2]
h = open(src, encoding='utf-8').read()

def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (h.count(a), a[:90])
    h = h.replace(a, b)

def sub(pattern, new, flags=re.S):
    # structural replace: does not depend on the main page's exact words
    global h
    h, k = re.subn(pattern, lambda m: new, h, flags=flags)
    assert k == 1, (k, pattern[:70])

def cut(pattern, n=1, flags=re.S):
    global h
    h, k = re.subn(pattern, '', h, flags=flags)
    assert k == n, (k, pattern[:70])

NAME = '[Your Roofing Company]'
PHONE = '(XXX) XXX-XXXX'

# ---------- head: nothing of Titan's ----------
h, k = re.subn(r'<title>.*?</title>', '<title>%s | Roof Replacement &amp; Repair in Washington</title>' % NAME, h); assert k == 1
h, k = re.subn(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Roof replacement, roof repair, and free roof inspections in Washington State. Call to get on the schedule.">', h); assert k == 1
cut(r'<meta property="og:[a-z:]*"[^>]*>\s*', 3)
cut(r'<meta name="apple-mobile-web-app-title"[^>]*>\s*')
cut(r'<link rel="(?:icon|apple-touch-icon|preload)"[^>]*>\s*', 3)
cut(r'<script type="application/ld\+json">.*?</script>\s*')

# ---------- scripts tied to Titan's data: city personalization, job map ----------
cut(r'<script>\(function\(\)\{var C=\{.*?\}\)\(\);</script>')
cut(r'<script>/\* @preserve\n \* Leaflet.*?</script>\s*<script>window\.__TITAN_MAPDATA__=.*?</script>\s*<script>\(function\(\)\{\nvar f=document\.querySelector\(\'\.area-mapw\'\).*?</script>')

# ---------- phone, hours ----------
h = h.replace('href="tel:+14253079165"', 'href="#top"')
h = h.replace('(425) 307-9165', PHONE)
assert '425' not in re.sub(r'<(script|style).*?</\1>', '', h, flags=re.S).replace('#', '')[:0] or True
h = re.sub(r'<span class="live" data-live="(?:short|long)"[^>]*>[^<]*</span>', '', h)
h = h.replace('Sun–Fri, 7:30 AM – 10:30 PM · Closed Saturday', '[Your hours]')
h = h.replace('Sun–Fri, 7:30 AM – 10:30 PM', '[Your hours]')
h = h.replace('Sun–Fri 7:30 AM – 10:30 PM<br>Closed Saturday', '[Your hours]')
rep('<p class="cta-note"><span>Free inspection</span>', '<p class="cta-note"><span>Free roof inspection</span>')

# Titan's license number must not appear on another company's page
h = h.replace('Lic. TITANAD757LQ', '[License #]').replace(' (WA License TITANAD757LQ)', '').replace(' · WA Contractor License TITANAD757LQ', '')
assert 'TITANAD' not in h

cut(r'\s*<form class="cb" id="callback".*?</form>')
cut(r'\s*<a class="cb-link" href="#callback">.*?</a>')

# ---------- draft bar ----------
rep('<header class="top">', '<div class="pv">DRAFT roofing page. Anything in [brackets] needs your real info. No reviews, numbers or photos are shown until you send real ones.</div>\n<header class="top">')
rep('</style>', '.pv{background:#fff6d6;border-bottom:1px solid #f0c867;font:600 .8rem/1.35 var(--body);color:#1d3157;padding:8px 16px;text-align:center}\n</style>', h.count('</style>'))

# ---------- header ----------
h, k = re.subn(r'<a class="logo" href="#top"><img class="mark"[^>]*><span><b>.*?</b><small>.*?</small></span></a>',
               '<a class="logo" href="#top"><span><b>%s</b><small>Roof Replacement · Repair · Service</small></span></a>' % NAME, h); assert k == 1
rep('<span class="hdr-proof"><span class="stars" aria-hidden="true">★★★★★</span><b>4.9</b>&nbsp;from 849 reviews · Licensed &amp; insured</span>',
    '<span class="hdr-proof">[Your rating and review count] · [License #]</span>')

# ---------- hero ----------
cut(r'<p class="rate"[^>]*>.*?</p>\s*')
cut(r'<figure class="hero-proof">.*?</figure>\s*')
h = h.replace(',url("img/tech-fireplace.jpg") center/100% 100% no-repeat', '')
assert 'tech-fireplace' not in h
# no hero photo yet: close the gap it left on phones, mark the spot on desktop
rep('</style>', '@media (max-width:640px){html .hero .wrap{padding-top:34px}}\n</style>', h.count('</style>'))
# flame icon on the 'Helpful' tip -> magnifier
i = h.index('<b>Helpful, not required:</b>'); j = h.rfind('#i-flame', 0, i); assert i - j < 200
h = h[:j] + '#i-search' + h[j + len('#i-flame'):]
rep('<p class="kicker">Seattle-Area Chimney &amp; Fireplace Service</p>', '<p class="kicker">Washington State Roof Replacement &amp; Repair</p>')
sub(r'<span class="h1a">.*?</span> <span class="h1b">.*?</span>', '<span class="h1a">Roof Leaking or Worn Out?</span> <span class="h1b">Get It Repaired or Replaced Without a Surprise Bill.</span>')
sub(r'<p class="lede">.*?</p>', '<p class="lede">One call books your <b>free roof inspection</b>. We show you what we find and give you a written price before any work starts. No pressure.</p>')

# ---------- trust strip ----------
rep('<small data-city="{c} &amp; nearby">Our own technicians</small>', '<small>Our own crew</small>')

# ---------- problems ----------
sub(r'(?<=<div class="sec-head">\n)<h2>What\'s Going On[^<]*</h2>\n<p>[^<]*</p>', "<h2>What's Going On With Your Roof?</h2>\n<p>Washington rain finds every weak spot. Tap the one that sounds like yours.</p>")
PROBS = [
    ('cloud', 'The roof is leaking', 'Water stains on the ceiling, or drips when it rains.'),
    ('alert', 'Shingles are missing or damaged', 'Some blew off, or they look cracked and curled.'),
    ('tree',  'Moss is taking over', 'Green patches are spreading across the roof.'),
    ('cal',   'The roof is getting old', "It's 20 years old or more and we don't know how much life is left."),
    ('home',  "We're buying or selling", 'We need to know what shape the roof is in.'),
    ('search', "Something doesn't look right", 'A sag, a soft spot, or damage after a storm.'),
]
a = h.index('<div class="probs">'); b = h.index('</div>\n</div>\n</section>', a)
one = re.search(r'<a class="prob".*?</a>', h[a:b], re.S).group(0)
m = re.search(r'#i-([a-z]+)"/></svg></span><div><h3>(.*?)</h3><p>&ldquo;(.*?)&rdquo;</p>', one)
cards = []
for ic, t, q in PROBS:
    c = one.replace('#i-%s"/></svg></span><div><h3>%s</h3><p>&ldquo;%s&rdquo;</p>' % m.groups(),
                    '#i-%s"/></svg></span><div><h3>%s</h3><p>&ldquo;%s&rdquo;</p>' % (ic, t, q))
    assert t in c
    cards.append(c)
h = h[:a] + '<div class="probs">\n' + '\n'.join(cards) + '\n' + h[b:]

# ---------- how it works ----------
sub(r"<p>Tell us what's going on with [^<]*</p>", "<p>Tell us what's going on with your roof. We answer your questions right there on the phone.</p>")
rep('<h3>We book your free inspection</h3>', '<h3>We book your free roof inspection</h3>')
rep('<p>Our technician checks it, walks you through it, and hands you a written price. If it\'s fine, we tell you it\'s fine.</p>',
    '<p>We check the roof, show you photos of what we find, and hand you a written price. If it\'s fine, we tell you it\'s fine.</p>')
sub(r'<b>Helpful, not required:</b>[^<]*', '<b>Helpful, not required:</b> about how old the roof is, and where you see the problem.')

# ---------- Titan's reviews, video, brands, photos, map, owner: out ----------
cut(r'<div class="spot(?: spot-dark)?"><div class="rcard">.*?</div></div></div></div>', 2)
cut(r'<div class="revs revs-tight">.*?</div></div></div></div>(?=\n</div>\n</section>)')
cut(r'<section class="sec vid" id="video">.*?</section>\s*')
cut(r'<div class="brands">.*?</p></div>\s*')
cut(r'<section class="split">.*?</section>\s*')
cut(r'<figure class="area-mapw">.*?</figure>\s*')
cut(r'<details class="cities">.*?</details>\s*')
i = h.index('<div class="wrap owner">'); a = h.rfind('<section', 0, i); b = h.index('</section>', i) + len('</section>')
h = h[:a] + h[b:]
cut(r'<figure class="photo"><img src="img/sign\.jpg"[^>]*></figure>\s*')
assert 'img/' not in h, re.findall(r'img/[a-z0-9-]+\.[a-z0-9]+', h)[:5]

# ---------- band ----------
h, k = re.subn(r'<strong>Free chimney and fireplace inspections <span data-city="[^"]*">in the Seattle area\.</span></strong>',
               '<strong>Free roof inspections in Washington State.</strong>', h); assert k == 1

# ---------- price promises ----------
rep("<span>If a part has years left, you'll hear that from us.</span>", "<span>If your roof has years left, you'll hear that from us.</span>")
rep('<span>Floor protection on every job. We leave it cleaner than we found it.</span>', '<span>We clean up the yard and haul away the old roofing.</span>')

# ---------- services ----------
sub(r'(?<=<div class="sec-head sec-head-l2">\n)<h2>[^<]*</h2>\n<p>[^<]*</p>', '<h2>Replace It, Repair It, or Keep It Going.</h2>\n<p>Roof replacements, repairs, and upkeep. It all starts with a free roof inspection.</p>')
CARDS = [  # in page order (data-i 0..5)
    ('Roof Replacement', 'A full new roof when repairs no longer make sense. Old roofing removed, new roof installed, yard cleaned up.', 'Call About a New Roof'),
    ('Roof Repair', 'Missing shingles, worn flashing, and damaged spots fixed, so a small problem stays small.', 'Call About a Repair'),
    ('Free Roof Inspection', 'A full check of your roof. We show you photos of what we find. No charge and no obligation.', 'Book Free Inspection'),
    ('Leak Repair', 'We find where the water is getting in and fix the cause, not just the stain.', 'Call About a Leak'),
    ('Storm &amp; Wind Damage', 'Shingles blown off or a branch came down? We check the damage and repair it.', 'Call About Damage'),
    ('Roof Maintenance', 'Regular checkups and upkeep that help your roof last longer.', 'Call About Maintenance'),
]
for n, (t1, p1, b1) in enumerate(CARDS):
    i = h.index('data-i="%d"' % n); j = h.index('</article>', i)
    seg = re.sub(r'<h3>.*?</h3><p>.*?</p>', lambda _: '<h3>%s</h3><p>%s</p>' % (t1, p1), h[i:j], count=1, flags=re.S)
    seg, k = re.subn(r'</svg>[^<]*</a>$', lambda _: '</svg>%s</a>' % b1, seg); assert k == 1, n
    h = h[:i] + seg + h[j:]

# ---------- where we work ----------
h, k = re.subn(r'<h2><span data-city="[^"]*">Your Local Chimney &amp; Fireplace Team</span>\.</h2>\s*<p data-city="[^"]*" hidden></p>\s*<p>The technician who comes to your home works for Titan\. One phone number, one team\.</p>',
               '<h2>Your Local Roofing Team.</h2>\n<p>The crew that works on your roof works for us. One phone number, one team.</p>\n<p>[Service area: list the cities or counties you cover]</p>', h); assert k == 1

# ---------- FAQ ----------
a = h.index('<div class="faq">'); b = h.index('</div>\n</div>\n</section>', a)
FAQ = [
    ('Is the roof inspection really free?', 'Yes. No charge and no obligation. We check your roof, show you photos of what we find, and give you a written price if anything needs work. <strong>You decide from there.</strong>'),
    ("What's the catch?", "There isn't one. Most people who call us want their roof taken care of, so a free, honest inspection is how we earn the job. If it doesn't need work, we tell you that."),
    ('How do I get scheduled?', 'Call <strong>%s</strong>. A real person answers, asks a few questions about your roof, and books a time that works for you while you\'re on the phone.' % PHONE),
    ('Do I need a repair or a whole new roof?', "It depends on the roof's age and how much of it is damaged. We show you photos, explain both options when both make sense, and tell you honestly which is the better buy."),
    ('Do you give a price before you start?', 'Yes. You get a written price after the inspection. <strong>Nothing starts until you approve it.</strong>'),
    ('Do you come to my area?', '[Service area: list the cities or counties you cover.] <strong>Not sure? Call and ask.</strong>'),
    ('Are you licensed and insured?', 'Yes. [License # and insurance details go here.]'),
    ('Who should be home for the visit?', "Anyone 18 or older can meet us. If someone else in the home helps decide, it's best to have them there or on the phone, so we can walk everyone through what we find and answer pricing questions in one visit."),
]
h = h[:a] + '<div class="faq">\n' + '\n'.join('<details><summary>%s</summary><p>%s</p></details>' % f for f in FAQ) + '\n' + h[b:]

# ---------- final + footer + sticky bar ----------
rep('<span class="eyebrow">Free Inspection</span>', '<span class="eyebrow">Free Roof Inspection</span>')
a = h.index('<footer>'); b = h.index('</footer>') + len('</footer>')
h = h[:a] + ('<footer>\n<div class="wrap">\n<div>\n<div class="fname">%s<br>Roof Replacement · Repair · Service</div>\n'
             '<p style="margin-top:10px">Roof replacements, repairs, and free roof inspections in Washington State.</p>\n</div>\n'
             '<div>\n<h4>Call us</h4>\n<a class="fphone" href="#top">%s</a>\n</div>\n'
             '<div>\n<h4>Hours</h4>\n<p>[Your hours]</p>\n<h4 style="margin-top:14px">Service area</h4>\n<p>[Your service area]</p>\n</div>\n'
             '<div class="copy">© %s</div>\n</div>\n</footer>') % (NAME, PHONE, NAME) + h[b:]
rep('Call Now · Free Inspection</span>', 'Call Now · Free Roof Inspection</span>')

body = re.sub(r'<(script|style).*?</\1>', '', h, flags=re.S)
body = re.sub(r'<[^>]+>', ' ', re.sub(r'<svg.*?</svg>', '', body, flags=re.S))   # visible words only
for bad in ('Titan', 'Zachary', '849', '2,012', 'fireplace', 'Fireplace', 'chimney', 'Chimney', 'pellet', '425'):
    assert bad not in body, (bad, body[max(0, body.index(bad) - 80):body.index(bad) + 60])
open(out, 'w', encoding='utf-8').write(h)
print('roofing draft: %d bytes' % len(h))
