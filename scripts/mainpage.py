"""Main landing page: chimney & fireplace (wood, gas, pellet), made from the finished gas page.

Usage: python3 mainpage.py site/variant-src/index.html site/main-src/index.html

Same design, map, city personalization, reviews and offer structure as the gas page.
Only the words change: headline, problems, services, FAQ, titles. No preview bar and no
keyword-swap script on this page.

Confirmed by the owner (Nov 20): the free inspection also covers chimneys and wood fireplaces.
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
    '<meta name="description" content="Chimney sweeping, free inspections, and repairs for wood-burning chimneys and fireplaces in the Seattle area. Call (425) 307-9165 to get on the schedule.">')
rep('<meta property="og:description" content="Free gas fireplace inspection in Seattle. Call (425) 307-9165.">',
    '<meta property="og:description" content="Chimney sweeping, free inspections, and fireplace repair in the Seattle area. Call (425) 307-9165.">')
rep('"description": "Free gas fireplace inspection in Seattle. Gas fireplace repair, service, pilot, ignition, gas valves, wood-to-gas conversions and gas inserts."',
    '"description": "Chimney sweeping, free inspections, and repairs for wood-burning chimneys and fireplaces in the Seattle area. Gas fireplace service too."')

# ---------- header + hero ----------
rep('<b>Titan Chimney &amp; Fireplace</b><small>Gas Fireplace Service &amp; Repair</small>',
    '<b>Titan Chimney &amp; Fireplace</b><small>Sweep · Inspection · Repair</small>')
rep('<p class="kicker">Seattle-Area Gas Fireplace Repair</p>', '<p class="kicker">Seattle-Area Chimney &amp; Fireplace Service</p>')
rep('var x="Gas Fireplace Repair in "+c;', 'var x="Chimney & Fireplace Service in "+c;')
rep('<span class="h1a">Gas Fireplace Won\'t Light?</span> <span class="h1b">Get It Working Again Without a Surprise Bill.</span>',
    '<span class="h1a">Chimney Problems?</span> <span class="h1b">Get It Swept, Inspected, and Fixed Without a Surprise Bill.</span>')
rep("We show you what's wrong and give you a written price before any work starts. No pressure.</p>",
    "We sweep, inspect, and repair wood-burning chimneys and fireplaces. You get a written price before any work starts. No pressure.</p>")

# ---------- problems ----------
rep('<h2>What Is Your Fireplace Doing?</h2>', "<h2>What's Going On With Your Chimney or Fireplace?</h2>")
rep('<p>The first cold, wet nights of the season are when fireplaces act up. Tap the one that sounds like yours.</p>',
    '<p>The first cold, wet nights of the season are when chimneys and fireplaces act up. Tap the one that sounds like yours.</p>')
PROBS = [
    ('cal',   "It hasn't been cleaned in years", "We can't remember the last time the chimney was swept."),
    ('cloud', 'Smoke comes back into the room', 'When we light a fire, smoke comes out the front.'),
    ('home',  'We just bought the house', 'Is the chimney and fireplace safe to use?'),
    ('alert', 'A smell from the fireplace', "A smoky or damp smell, even when it's not in use."),
    ('flame', 'We need help with a gas fireplace', "It won't light, or it hasn't been serviced in years."),
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
# calmer about 'free' on this page (owner, Nov 20): the inspection is free, but the page doesn't shout it
rep("<h2>Free Means Free. Here's Exactly What Happens.</h2>", "<h2>Here's Exactly What Happens When You Call.</h2>")
rep('<p>No catch. The inspection costs you nothing, and you never owe us for saying no.</p>', "<p>Three simple steps. The inspection is free, and nothing starts until you approve the price.</p>")
rep('<h3>Book Your Free Inspection</h3>', '<h3>Book Your Inspection</h3>')

rep('<p>Tell us what your fireplace is doing. We answer your questions right there on the phone.</p>',
    "<p>Tell us what's going on with your chimney or fireplace. We answer your questions right there on the phone.</p>")
rep("<b>Helpful, not required:</b> the brand name. It's usually on a sticker behind the lower grille.",
    '<b>Helpful, not required:</b> tell us when the chimney was last swept, and how often you use the fireplace.')

# ---------- band ----------
rep('<strong>Free gas fireplace inspections <span', '<strong>Free chimney and fireplace inspections <span')

# ---------- services ----------
rep('<h2>Old, New, or Never Used. We Fix Gas Fireplaces.</h2>', '<h2>Wood-Burning Chimneys and Fireplaces Are What We Do.</h2>')
rep("<p>Gas fireplaces are our specialty, and we also take care of what they sit in: the chimney or vent pipe and the fireplace box around it. Repairs, yearly service, inserts, and wood-to-gas conversions. It all starts with a free inspection.</p>",
    '<p>Sweeping, inspections, and repairs for wood-burning chimneys and fireplaces. We service gas fireplaces too. It all starts with a free inspection.</p>')
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
     'Chimney Repair',
     'Crowns, flashing, brickwork, tuckpointing, dampers, caps, and more. We fix what the inspection finds, with a written price first.',
     'Call About a Repair'),
    ('Free Inspection',
     'A full safety and operation check of your gas fireplace. We show you what we find. No charge and no obligation.',
     'Book Free Inspection',
     'Free Chimney Inspection',
     'A full safety check of your chimney and fireplace. We show you what we find. No charge and no obligation.',
     'Book Free Inspection'),
    ('Wood-to-Gas Conversion',
     'Turn a wood fireplace into push-button heat. We handle permits, plans, parts, and the full install as one company.',
     'Call About Conversion',
     'Wood Fireplace Service &amp; Repair',
     'Cleaning, a safety check, and repairs for wood-burning fireplaces, so you can light a fire without worrying about it.',
     'Call About Your Fireplace'),
    ('Gas Inserts &amp; Installs',
     'New gas fireplaces and inserts, venting, and gas line hookup. Installed to code, tested, and explained to you.',
     'Call About Installs',
     'Gas Fireplaces Too',
     "Have a gas fireplace that won't light or needs service? We repair and service those as well.",
     'Call About Gas Fireplaces'),
    ('Logs, Remotes &amp; Blowers',
     'Gas log sets, remotes, wall switches, thermostats, and blower fans, repaired or replaced.',
     'Call for a Price',
     'Wood-to-Gas Conversion',
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

rep('</svg>Gas fireplace specialists</li>', '</svg>Chimney and wood fireplace specialists</li>')

# ---------- where we work + owner ----------
rep('<span data-city="Your {c} Gas Fireplace Team">Your Local Gas Fireplace Team</span>',
    '<span data-city="Your {c} Chimney &amp; Fireplace Team">Your Local Chimney &amp; Fireplace Team</span>')
rep('Our gas fireplace work covers pilots, valves, ignition, service, conversions, and new installs.</p>',
    'We sweep, inspect, and repair wood-burning chimneys and fireplaces, and we service gas fireplaces too.</p>')
rep("If your fireplace is fine, we tell you it's fine. And if something", "If everything is fine, we tell you it's fine. And if something")

# ---------- FAQ ----------
rep('We check your fireplace, show you what we find,', 'We check your chimney and fireplace, show you what we find,')
rep('Most people who call us want their fireplace fixed, so', 'Most people who call us want their chimney or fireplace taken care of, so')
rep('asks a few questions about your fireplace, and books', 'asks a few questions about your chimney or fireplace, and books')
NEWQ = ('<details><summary>How often should a chimney be cleaned?</summary><p>The national fire safety standard (NFPA 211) says chimneys, fireplaces, and vents should be inspected at least once a year and cleaned when needed. <strong>If you burn wood often, have it checked before each season.</strong></p></details>\n'
    '<details><summary>What is creosote, and why does it matter?</summary><p>Creosote is the black, tar-like buildup that wood smoke leaves inside a chimney. It can catch fire, which is why chimneys need regular sweeping.</p></details>\n'
    '<details><summary>Why does smoke come back into the room?</summary><p>The most common causes are a dirty or blocked chimney, a damper that is closed or stuck, or a draft problem. <strong>We\'ll find the cause during your free inspection.</strong></p></details>\n'
    '<details><summary>Water is getting in around my chimney. Can you fix it?</summary><p>Yes. Leaks usually come from the crown, the flashing, the cap, or the brickwork. We find where the water gets in and give you a written price to fix it.</p></details>\n'
    '<details><summary>Will the cleaning make a mess?</summary><p>No. Floor protection goes down before we start, and we leave the area cleaner than we found it.</p></details>\n'
    '<details><summary>Do you work on gas fireplaces too?</summary><p>Yes. We repair and service gas fireplaces and check their vents.</p></details>\n')
# gas-only questions from the gas page come out; the new wood questions go in their place
for q in ('Do you work on condo and townhome fireplaces?', "Why won't my gas fireplace pilot stay lit?", 'Is a smell normal the first time we turn it on in the fall?'):
    k = h.count('<details><summary>%s</summary>' % q); assert k == 1, q
    a = h.index('<details><summary>%s</summary>' % q); b = h.index('</details>', a) + len('</details>')
    h = h[:a] + (NEWQ if q.startswith('Why') else '') + h[b:].lstrip('\n') if q.startswith('Why') else h[:a] + h[b:].lstrip('\n')

# gas-only pieces that stay on the gas page: the gas brand strip and the 'I smell gas' question
# the gas brand strip becomes the list of chimney repairs (owner's list, Nov 20)
REPAIRS = ['Crown repair', 'Flashing', 'Brickwork', 'Tuckpointing', 'Waterproofing', 'Damper installation', 'Cap replacement',
           'Chase covers', 'Storm collars', 'Pipe replacement', 'New installations', 'and more']
h, k = re.subn(r'<div class="brands">.*?</p></div>', lambda m: '<div class="brands"><span>Chimney repairs we do</span><p>' + ''.join('<b>%s</b>' % x for x in REPAIRS) + '</p></div>', h, flags=re.S)
assert k == 1
cut(r'<details><summary>I smell gas\. What should I do\?</summary>.*?</details>\s*')

# ---------- footer ----------
rep('<div class="fname">Titan Chimney &amp; Fireplace<br>Gas Fireplace Service &amp; Repair</div>',
    '<div class="fname">Titan Chimney &amp; Fireplace<br>Sweep · Inspection · Repair</div>')
rep('Gas fireplace inspection, repair, service, and conversions.</p>',
    'Sweeping, inspections, and repairs for wood-burning chimneys and fireplaces.</p>')

assert 'Gas Fireplace Service &amp; Repair' not in h
open(out, 'w', encoding='utf-8').write(h)
print('main page: %d bytes' % len(h))
