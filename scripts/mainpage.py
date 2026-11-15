"""Main landing page: chimney & fireplace (wood, gas, pellet), made from the finished gas page.

Usage: python3 mainpage.py site/variant-src/index.html site/main-src/index.html

Same design, map, city personalization, reviews and offer structure as the gas page.
Only the words change: headline, problems, services, FAQ, titles. No preview bar and no
keyword-swap script on this page.

ASSUMED (owner to confirm): the free inspection also covers chimneys and wood/pellet units.
Services named here are only ones the job mix shows (chimney, gas fireplace, pellet stove)
plus what the gas page already says (conversions, inserts).
"""
import re, sys

src, out = sys.argv[1], sys.argv[2]
h = open(src, encoding='utf-8').read()

def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (h.count(a), a[:90])
    h = h.replace(a, b)

def cut(pattern, flags=re.S):
    global h
    h, k = re.subn(pattern, '', h, count=1, flags=flags)
    assert k == 1, pattern[:60]

# ---------- no preview bar, no keyword swap ----------
cut(r'<div class="pv">.*?</label></div>\s*(?=<header class="top">)')
cut(r'<script>\(function\(\)\{\nvar V=\{\nrepair:.*?\}\)\(\);</script>\s*')

# ---------- head ----------
rep('<title>Titan Chimney &amp; Fireplace | Gas Fireplace Service &amp; Repair</title>',
    '<title>Titan Chimney &amp; Fireplace | Chimney Sweep, Inspection &amp; Fireplace Repair</title>')
rep('og:title" content="Titan Chimney &amp; Fireplace | Gas Fireplace Service &amp; Repair"',
    'og:title" content="Titan Chimney &amp; Fireplace | Chimney Sweep, Inspection &amp; Fireplace Repair"')
rep('<meta name="description" content="Free gas fireplace inspection in Seattle. Repair, service, pilot, ignition, gas valves and wood-to-gas conversions. Call (425) 307-9165 to get on the schedule.">',
    '<meta name="description" content="Chimney sweeping, free inspections, and fireplace repair for wood, gas, and pellet in the Seattle area. Call (425) 307-9165 to get on the schedule.">')
rep('<meta property="og:description" content="Free gas fireplace inspection in Seattle. Call (425) 307-9165.">',
    '<meta property="og:description" content="Chimney sweeping, free inspections, and fireplace repair in the Seattle area. Call (425) 307-9165.">')
rep('"description": "Free gas fireplace inspection in Seattle. Gas fireplace repair, service, pilot, ignition, gas valves, wood-to-gas conversions and gas inserts."',
    '"description": "Chimney sweeping, free chimney and fireplace inspections, and repair and service for wood, gas, and pellet fireplaces in the Seattle area."')

# ---------- header + hero ----------
rep('<b>Titan Chimney &amp; Fireplace</b><small>Gas Fireplace Service &amp; Repair</small>',
    '<b>Titan Chimney &amp; Fireplace</b><small>Sweep · Inspection · Repair</small>')
rep('<p class="kicker">Seattle-Area Gas Fireplace Repair</p>', '<p class="kicker">Seattle-Area Chimney &amp; Fireplace Service</p>')
rep('var x="Gas Fireplace Repair in "+c;', 'var x="Chimney & Fireplace Service in "+c;')
rep('<span class="h1a">Gas Fireplace Won\'t Light?</span> <span class="h1b">Get It Working Again Without a Surprise Bill.</span>',
    '<span class="h1a">Chimney or Fireplace Need Attention?</span> <span class="h1b">Get It Cleaned, Checked, and Working Without a Surprise Bill.</span>')
rep("We show you what's wrong and give you a written price before any work starts. No pressure.</p>",
    "Wood, gas, or pellet: we show you what we find and give you a written price before any work starts. No pressure.</p>")

# ---------- problems ----------
rep('<h2>What Is Your Fireplace Doing?</h2>', "<h2>What's Going On With Your Chimney or Fireplace?</h2>")
rep('<p>The first cold, wet nights of the season are when fireplaces act up. Tap the one that sounds like yours.</p>',
    '<p>The first cold, wet nights of the season are when chimneys and fireplaces act up. Tap the one that sounds like yours.</p>')
PROBS = [
    ('cal',   "It hasn't been cleaned in years", "We can't remember the last time the chimney was swept."),
    ('cloud', 'Smoke comes back into the room', 'When we light a fire, smoke comes out the front.'),
    ('home',  'We just bought the house', 'Is the chimney and fireplace safe to use?'),
    ('alert', 'A smell from the fireplace', "A smoky or damp smell, even when it's not in use."),
    ('flame', "The gas fireplace won't light", 'It clicks, the pilot goes out, or nothing happens.'),
    ('search', "Something doesn't look right", 'Stains, cracks, or loose bricks we want checked.'),
]
a = h.index('<div class="probs">'); b = h.index('</div>\n</div>\n</section>', a)
one = re.search(r'<a class="prob".*?</a>', h[a:b], re.S).group(0)
assert '#i-off' in one and "It won't turn on" in one
cards = []
for ic, t, q in PROBS:
    c = one.replace('#i-off', '#i-' + ic).replace("It won't turn on", t).replace('I flip the switch and nothing happens.', q)
    assert c.count(t) == 1 and c.count(q) == 1
    cards.append(c)
h = h[:a] + '<div class="probs">\n' + '\n'.join(cards) + '\n' + h[b:]

# ---------- how it works ----------
rep('<p>Tell us what your fireplace is doing. We answer your questions right there on the phone.</p>',
    "<p>Tell us what's going on with your chimney or fireplace. We answer your questions right there on the phone.</p>")
rep("<b>Helpful, not required:</b> the brand name. It's usually on a sticker behind the lower grille.",
    '<b>Helpful, not required:</b> tell us if it burns wood, gas, or pellets, and when it was last cleaned.')

# ---------- band ----------
rep('<strong>Free gas fireplace inspections <span', '<strong>Free chimney and fireplace inspections <span')

# ---------- services ----------
rep('<h2>Old, New, or Never Used. We Fix Gas Fireplaces.</h2>', '<h2>Wood, Gas, or Pellet. One Team for All of It.</h2>')
rep("<p>Gas fireplaces are our specialty, and we also take care of what they sit in: the chimney or vent pipe and the fireplace box around it. Repairs, yearly service, inserts, and wood-to-gas conversions. It all starts with a free inspection.</p>",
    '<p>Chimney sweeping, inspections, and fireplace repair and service. It all starts with a free inspection.</p>')
CARDS = [
    ('Gas Fireplace Repair',
     "Pilot lights, gas valves, and ignition parts like thermocouples and thermopiles. Fixed with original manufacturer parts whenever they're available.",
     'Call About Repair',
     'Chimney Sweep &amp; Cleaning',
     'We sweep the chimney from top to bottom and clear out soot and buildup. Floor protection goes down before we start.',
     'Call About a Sweep'),
    ('Service &amp; Cleaning',
     'Yearly tune-up. We clean the burner, pilot, logs, and glass, check the safety controls, and test everything before we leave.',
     'Call About Service',
     'Wood Fireplace Service',
     'Cleaning and a safety check for wood-burning fireplaces, so you can light a fire without worrying about it.',
     'Call About Wood Fireplaces'),
    ('Free Inspection',
     'A full safety and operation check of your gas fireplace. We show you what we find. No charge and no obligation.',
     'Book Free Inspection',
     'Free Inspection',
     'A full safety check of your chimney and fireplace. We show you what we find. No charge and no obligation.',
     'Book Free Inspection'),
    ('Wood-to-Gas Conversion',
     'Turn a wood fireplace into push-button heat. We handle permits, plans, parts, and the full install as one company.',
     'Call About Conversion',
     'Gas Fireplace Repair &amp; Service',
     "Won't light, pilot keeps going out, or clicking? We repair and service gas fireplaces and inserts, with original manufacturer parts whenever they're available.",
     'Call About Gas Fireplaces'),
    ('Gas Inserts &amp; Installs',
     'New gas fireplaces and inserts, venting, and gas line hookup. Installed to code, tested, and explained to you.',
     'Call About Installs',
     'Pellet Stove Service',
     'Cleaning and service for pellet stoves, so they feed, light, and burn the way they should.',
     'Call About Pellet Stoves'),
    ('Logs, Remotes &amp; Blowers',
     'Gas log sets, remotes, wall switches, thermostats, and blower fans, repaired or replaced.',
     'Call for a Price',
     'Wood-to-Gas Conversion &amp; Inserts',
     'Turn a wood fireplace into push-button heat. We handle permits, plans, parts, and the full install as one company.',
     'Call About Conversion'),
]
for t0, p0, b0, t1, p1, b1 in CARDS:
    old = '<h3>%s</h3><p>%s</p>' % (t0, p0)
    assert h.count(old) == 1, t0
    i = h.index(old); j = h.index('</article>', i)
    seg = h[i:j].replace(old, '<h3>%s</h3><p>%s</p>' % (t1, p1))
    assert seg.count('</svg>' + b0 + '</a>') == 1, b0
    seg = seg.replace('</svg>' + b0 + '</a>', '</svg>' + b1 + '</a>')
    h = h[:i] + seg + h[j:]

# ---------- crew slideshow: chimney photos first ----------
figs = re.findall(r'<figure class="slide(?: is-on)?"><img src="img/w\d\d\.jpg"[^>]*></figure>', h)
assert len(figs) == 13
a = h.index(figs[0]); b = h.index(figs[-1]) + len(figs[-1])
key = lambda f: re.search(r'img/(w\d\d)', f).group(1)
order = ['w04', 'w12', 'w11', 'w01', 'w09', 'w02', 'w03', 'w05', 'w06', 'w07', 'w08', 'w10', 'w13']
by = {key(f): f.replace('class="slide is-on"', 'class="slide"') for f in figs}
new = [by[k] for k in order]
new[0] = new[0].replace('class="slide"', 'class="slide is-on"')
h = h[:a] + '\n'.join(new) + h[b:]

rep('</svg>Gas fireplace specialists</li>', '</svg>Chimney, wood, gas, and pellet: one team</li>')

# ---------- where we work + owner ----------
rep('<span data-city="Your {c} Gas Fireplace Team">Your Local Gas Fireplace Team</span>',
    '<span data-city="Your {c} Chimney &amp; Fireplace Team">Your Local Chimney &amp; Fireplace Team</span>')
rep('Our gas fireplace work covers pilots, valves, ignition, service, conversions, and new installs.</p>',
    'We sweep and inspect chimneys, and we repair and service wood, gas, and pellet fireplaces.</p>')
rep("If your fireplace is fine, we tell you it's fine. And if something", "If everything is fine, we tell you it's fine. And if something")

# ---------- FAQ ----------
rep('We check your fireplace, show you what we find,', 'We check your chimney and fireplace, show you what we find,')
rep('Most people who call us want their fireplace fixed, so', 'Most people who call us want their chimney or fireplace taken care of, so')
rep('asks a few questions about your fireplace, and books', 'asks a few questions about your chimney or fireplace, and books')
rep('<details><summary>Why won\'t my gas fireplace pilot stay lit?</summary>',
    '<details><summary>How often should a chimney be cleaned?</summary><p>The national fire safety standard (NFPA 211) says chimneys, fireplaces, and vents should be inspected at least once a year and cleaned when needed. <strong>If you burn wood often, have it checked before each season.</strong></p></details>\n'
    '<details><summary>Will the cleaning make a mess?</summary><p>No. Floor protection goes down before we start, and we leave the area cleaner than we found it.</p></details>\n'
    '<details><summary>Does a gas fireplace need its chimney or vent checked too?</summary><p>Yes. Gas burns cleaner than wood, but the vent or chimney can still get blocked or wear out. We check it as part of the free inspection.</p></details>\n'
    '<details><summary>Do you work on pellet stoves?</summary><p>Yes. We clean and service pellet stoves.</p></details>\n'
    '<details><summary>Why won\'t my gas fireplace pilot stay lit?</summary>')
rep('<summary>Is a smell normal the first time we turn it on in the fall?</summary><p>A light, dusty smell',
    '<summary>Is a smell normal the first time we turn on the gas fireplace in the fall?</summary><p>A light, dusty smell')

# ---------- footer ----------
rep('<div class="fname">Titan Chimney &amp; Fireplace<br>Gas Fireplace Service &amp; Repair</div>',
    '<div class="fname">Titan Chimney &amp; Fireplace<br>Sweep · Inspection · Repair</div>')
rep('Gas fireplace inspection, repair, service, and conversions.</p>',
    'Chimney sweeping, inspections, and fireplace repair for wood, gas, and pellet.</p>')

assert 'Gas Fireplace Service &amp; Repair' not in h
open(out, 'w', encoding='utf-8').write(h)
print('main page: %d bytes' % len(h))
