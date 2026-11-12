import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import areamap, json, mapui2 as mapui
JOBS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jobs_loc.json')))
src, out = sys.argv[1], sys.argv[2]; h = open(src).read()
def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (h.count(a), a[:80])
    h = h.replace(a, b)
PH = 'href="tel:+14253079165"'
CALL = '<a class="btn btn-call btn-big" %s><span class="l1"><svg class="ico"><use href="#i-phone"/></svg>Call (425) 307-9165</span><span class="l2">Call now to get scheduled</span></a>' % PH
LIVE = '<span class="live" data-live="short" hidden></span>'

# hero: more local kicker + live phone status
rep('<p class="kicker">Seattle Gas Fireplace Repair</p>', '<p class="kicker">Seattle-Area Gas Fireplace Repair</p>')

# hero: the visitor's own city from Google Ads (Final URL suffix: loc={loc_physical_ms}&iloc={loc_interest_ms})
# city_ids.json = Google Ads location IDs for our 60 cities (geotargets-2026-10-06.csv). City name only, no office claims.
CITY_IDS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'city_ids.json')))
assert len(CITY_IDS) == 60
CITYJS = ('<script>(function(){var C=%s;'
  'var q=new URLSearchParams(location.search),c=C[q.get("iloc")]||C[q.get("loc")]||"",t=(q.get("city")||"").toLowerCase();'
  'for(var k in C)if(C[k].toLowerCase()===t)c=C[k];if(!c)return;'
  'var x="Gas Fireplace Repair in "+c;function set(){var e=document.querySelector(".hero .kicker");if(e)e.textContent=x;}'
  'set();document.addEventListener("DOMContentLoaded",function(){setTimeout(set,0);var a=window.__titanApply;'
  'if(a)window.__titanApply=function(){a.apply(this,arguments);set();};});})();</script>') % json.dumps(CITY_IDS, separators=(',', ':'))
rep('<p class="kicker">Seattle-Area Gas Fireplace Repair</p>', '<p class="kicker">Seattle-Area Gas Fireplace Repair</p>' + CITYJS)
rep('<p class="cta-note"><span>Free inspection</span><span>A real person answers</span><span>Sun–Fri 7:30 AM – 10:30 PM</span></p>',
    '<p class="cta-note"><span class="live" data-live="long">Sun–Fri 7:30 AM – 10:30 PM</span><span>Free inspection</span><span>A real person answers</span></p>')

# trust strip: local team instead of OEM (OEM stays in services + reviews)
rep('<li><span class="ib"><svg class="ico"><use href="#i-gear"/></svg></span><span>OEM parts<small>Whenever available</small></span></li>',
    '<li><span class="ib"><svg class="ico"><use href="#i-pin"/></svg></span><span>Local team<small>Tacoma to Marysville</small></span></li>')

# problems: seasonal, local framing
rep('<p>Tap the one that sounds like yours. We hear every one of these.</p>',
    '<p>The first cold, wet nights of the season are when fireplaces act up. Tap the one that sounds like yours.</p>')

# live status next to every hours line
rep('<p class="hours">Sun–Fri, 7:30 AM – 10:30 PM</p>', '<p class="hours">%sSun–Fri, 7:30 AM – 10:30 PM</p>' % LIVE, 2)
rep('<p class="hours">Sun–Fri, 7:30 AM – 10:30 PM · Closed Saturday</p>', '<p class="hours">%sSun–Fri, 7:30 AM – 10:30 PM · Closed Saturday</p>' % LIVE)

# booking box: one helpful (not required) detail that makes the call faster
rep("You'll get every answer in one visit.</span></div>",
    "You'll get every answer in one visit.</span></div>\n        <div class=\"tip\"><svg class=\"ico\"><use href=\"#i-flame\"/></svg><span><b>Helpful, not required:</b> the brand name. It's usually on a sticker behind the lower grille.</span></div>")

# video: neighbors
rep('<h2>Hear It From Seattle Homeowners</h2>\n      <p>Real customers, in their own homes, talking about what happened when they called.</p>',
    '<h2>Hear It From Your Neighbors</h2>\n      <p>Seattle-area homeowners, in their own homes, talking about what happened when they called.</p>')

# services: cleaner headline + brands we work on
rep('<h2>Old, New, or Never Used, We Fix Gas Fireplaces</h2>', '<h2>Old, New, or Never Used. We Fix Gas Fireplaces.</h2>')
rep('    <div class="revs revs-tight">',
    '    <div class="brands"><span>Brands we work on</span><p><b>Heat &amp; Glo</b><b>Lennox</b><b>Majestic</b><b>Napoleon</b><b>Regency</b><b>Mendota</b><b>Travis (Lopi, Avalon, FPX)</b><b>Valor</b><b>Heatilator</b><b>Kozy Heat</b><b>and more</b></p></div>\n    <div class="revs revs-tight">')

# NEW: where we work (service-area map)
GROUPS = [
 ("Snohomish County", "Arlington, Smokey Point, Marysville, Granite Falls, Lake Stevens, Snohomish, Monroe, Everett, Mukilteo, Mill Creek, Lynnwood, Edmonds, Mountlake Terrace, Brier"),
 ("King County", "Shoreline, Lake Forest Park, Kenmore, Bothell, Woodinville, Duvall, Kirkland, Redmond, Sammamish, Issaquah, Bellevue, Mercer Island, Newcastle, Seattle, Renton, Tukwila, SeaTac, Burien, Normandy Park, Des Moines, Kent, Covington, Maple Valley, Black Diamond, Auburn, Algona, Pacific, Federal Way"),
 ("Pierce County", "Milton, Fife, Edgewood, Sumner, Bonney Lake, Puyallup, South Hill, Frederickson, Orting, Graham, Spanaway, Parkland, Lakewood, University Place, Fircrest, Steilacoom, Tacoma, Gig Harbor"),
]
CITIES = [c for g, l in GROUPS for c in l.split(", ")]
assert len(CITIES) == 60, len(CITIES)
area = '''<!-- WHERE WE WORK -->
<section class="sec area" id="area">
  <div class="wrap area-grid">
    <div class="area-head">
      <span class="eyebrow">Where We Work</span>
      <h2>Tacoma Area to Marysville Area. One Local Team.</h2>
      <p>We started in Seattle and grew from there, city by city, until we covered the whole metro. We're still one company: one phone number, one office, and the technician at your door works for Titan. No lead sites, no call center passing your number around.</p>
      <p>Same crew whether you're in a Ballard Craftsman, a Sammamish cul-de-sac, or a Tacoma bungalow. Every number on this map is a real job our team has done.</p>
    </div>
    %s
    <div class="area-rest">
      <details class="cities"><summary>See all 60 cities we serve</summary><div class="cities-in">%s</div></details>
      <div><h3 class="homes-h">The fireplaces we see around here</h3>
      <ul class="homes">
        <li><svg class="ico"><use href="#i-building"/></svg><div><b>Condos and townhomes</b><span>Direct-vent gas fireplaces from Capitol Hill to downtown Bellevue.</span></div></li>
        <li><svg class="ico"><use href="#i-home"/></svg><div><b>Older homes</b><span>Craftsman and mid-century houses in Seattle and Tacoma where the wood fireplace was converted to gas years ago.</span></div></li>
        <li><svg class="ico"><use href="#i-tree"/></svg><div><b>Suburban builds</b><span>'90s and 2000s builder fireplaces in Mill Creek, Sammamish, and Puyallup that haven't been serviced in years.</span></div></li>
      </ul></div>
      <div class="area-cta">%s<p class="hours">Not sure you're in our area? Call and ask.</p></div>
    </div>
  </div>
</section>

''' % (mapui.FIG, ''.join('<div><h4>%s</h4><p>%s</p></div>' % g for g in GROUPS), CALL)
rep('<!-- OWNER -->', area + '<!-- OWNER -->')

# owner: local, own team
rep("conversions, and new installs.</p>\n      <p>Every job starts",
    "conversions, and new installs.</p>\n      <p>We started in Seattle and grew across the metro, from the Marysville area down to the Tacoma area. We're still one company with our own team. When you call (425) 307-9165, you reach us, not a national call center or a lead service.</p>\n      <p>Every job starts")

# FAQ: local questions
rep('</p></details>\n      <details><summary>Who should be home for the visit?</summary>',
    '</p></details>\n      <details><summary>Do you come to my area?</summary><p>We cover 60 cities from the Marysville area down to the Tacoma area, across Snohomish, King, and Pierce counties: from Arlington and Lake Stevens through Seattle and the Eastside to Kent, Puyallup, and Gig Harbor. <strong>Not sure? Call and ask.</strong></p></details>'
    '\n      <details><summary>Are you really a local company?</summary><p>Yes. Titan started in Seattle and grew from there. We\'re one company with our own office, our own team, and one phone number. We don\'t sell your information or pass your call to whoever is free. The person who answers works for Titan, and so does the technician who comes to your home.</p></details>'
    '\n      <details><summary>Do you work on condo and townhome fireplaces?</summary><p>Yes. We work on direct-vent gas fireplaces in condos and townhomes. If your building has rules for contractors, tell us when you call and we\'ll follow them.</p></details>'
    '\n      <details><summary>Who should be home for the visit?</summary>')
rep('<details><summary>I smell gas. What should I do?</summary>',
    '<details><summary>Is a smell normal the first time we turn it on in the fall?</summary><p>A light, dusty smell for the first hour of the season is common. It\'s dust burning off the burner. If the smell is strong, keeps coming back, or the glass turns black, have it checked. <strong>If it smells like rotten eggs, that\'s gas. See the next question.</strong></p></details>\n      <details><summary>I smell gas. What should I do?</summary>')

# footer + schema: name the cities
rep('conversions in Seattle.</p>', 'conversions from the Tacoma area to the Marysville area.</p>')
rep('<p>Seattle and surrounding areas</p>', '<p>Tacoma Area to Marysville Area: 60 cities in Snohomish, King, and Pierce counties</p>')
rep('"areaServed": {"@type": "City", "name": "Seattle, WA"}', '"areaServed": [%s]' % ', '.join('{"@type": "City", "name": "%s, WA"}' % c for c in CITIES))

# sticky bar: show "Open now" when phones are open
rep('Call Now · Free Inspection</span><span class="l2">(425) 307-9165</span>', 'Call Now · Free Inspection</span><span class="l2">(425) 307-9165%s</span>' % LIVE)

css = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'areamap.css')).read() + '''
/* live phone status */
.live{display:inline-flex;align-items:center;gap:7px}
.live[hidden]{display:none!important}
.live.is-open::before{content:"";width:8px;height:8px;border-radius:50%;background:#2fd27a;flex:none;animation:livep 2.4s ease-out infinite}
@keyframes livep{0%{box-shadow:0 0 0 0 rgba(47,210,122,.55)}70%,100%{box-shadow:0 0 0 7px rgba(47,210,122,0)}}
@media (prefers-reduced-motion:reduce){.live.is-open::before{animation:none}}
.hero .live.is-open{color:#c4f5da;font-weight:700}
.hours .live{margin-right:10px;font-weight:700;color:#178048}
.split .hours .live,.final .hours .live,.plan-call .hours .live{color:#8ff0bb}
.mbar .live{margin-left:10px;font:700 .74rem/1 var(--body);letter-spacing:.02em;color:#fff}
.mbar .live.is-open::before{background:#b9ffd6}
/* brands */
.brands{margin-top:30px;padding:18px 22px;border:1px solid var(--cream-line);border-radius:14px;background:var(--cream);display:grid;gap:8px;text-align:center}
.brands span{font:700 .76rem/1 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.brands p{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 20px;font:700 1.05rem/1.5 var(--display);color:var(--navy)}
.brands b{font-weight:inherit;white-space:nowrap}

/* where we work */
'''+mapui.CSS+'''.cities{border-top:1px solid var(--cream-line);border-bottom:1px solid var(--cream-line)}
.cities summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:15px 2px;font:700 .95rem/1.2 var(--body);color:var(--navy)}
.cities summary::-webkit-details-marker{display:none}
.cities summary::after{content:"";width:8px;height:8px;margin-right:4px;border-right:2px solid var(--orange);border-bottom:2px solid var(--orange);transform:translateY(-3px) rotate(45deg);transition:transform .25s}
.cities[open] summary::after{transform:translateY(2px) rotate(225deg)}
.cities-in{display:grid;grid-template-columns:1fr 1fr;gap:16px 26px;padding:2px 2px 18px}
.cities h4{margin:0 0 5px;font:700 .72rem/1 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.cities-in p{margin:0;font-size:.88rem;line-height:1.55;color:var(--text)}
@media (max-width:640px){.cities-in{grid-template-columns:1fr;gap:14px}}
.area{background:linear-gradient(180deg,#fff 0%,var(--cream) 100%)}
.area-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.02fr);grid-template-areas:"head map" "rest map";gap:26px 56px;align-items:start}
.area-head{grid-area:head;display:grid;gap:12px;justify-items:start}
.area-head p{color:var(--muted);font-size:1.02rem;max-width:62ch}
.area-mapw{grid-area:map;margin:0;border-radius:20px;overflow:hidden;background:#fbf7f0;border:1px solid var(--cream-line);box-shadow:0 34px 60px -36px rgba(29,49,87,.6)}
.area-rest{grid-area:rest;display:grid;gap:26px}
.hoods h3,.homes-h{margin:0 0 12px;font:700 .76rem/1 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.hoods ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:7px}
.hoods li{font:600 .86rem/1 var(--body);color:var(--navy);background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 12px}
.homes{list-style:none;margin:0;padding:0;display:grid;gap:16px}
.homes li{display:flex;gap:14px;align-items:flex-start}
.homes .ico{width:30px;height:30px;color:var(--red);margin-top:1px}
.homes b{display:block;color:var(--navy);font:700 1.08rem/1.25 var(--display);margin-bottom:2px}
.homes span{display:block;color:var(--text);font-size:.96rem;line-height:1.5}
.area-cta{display:grid;gap:10px;justify-items:start}
.area-cta .hours{color:var(--muted);font-size:.9rem;margin:0}
@media (max-width:860px){
  .area-grid{grid-template-columns:1fr;grid-template-areas:"head" "map" "rest";gap:24px}
  .area-head{justify-items:center;text-align:center}
  .hoods{text-align:center}.hoods ul{justify-content:center}
  .area-cta{justify-items:stretch;text-align:center}.area-cta .btn-call{width:100%}
}
@media (max-width:640px){.hoods li{font-size:.8rem;padding:7px 10px}.brands p{font-size:.98rem}.brands p{gap:4px 16px}
  .cta-note .live{flex-basis:100%;justify-content:center}.cta-note .live+span::before{content:none}
  .m-city{font-size:17px}.m-city.m-big{font-size:27px}.m-hood{font-size:12.5px}.m-water{font-size:17px}.m-water.m-sm{font-size:13px}.m-sh text{font-size:11px}}
'''
rep('\n/* footer */', css + '\n/* footer */')

js = '''<script>
(function(){
  var D=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
  function now(){try{var o={};new Intl.DateTimeFormat('en-US',{timeZone:'America/Los_Angeles',weekday:'short',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(new Date()).forEach(function(x){o[x.type]=x.value;});var d=D.indexOf(o.weekday);return d<0?null:{d:d,m:(+o.hour%24)*60+(+o.minute)};}catch(e){return null;}}
  function paint(){
    var t=now();if(!t)return;
    var open=t.d!==6&&t.m>=450&&t.m<1350,msg;
    if(open)msg='Open now till 10:30 PM';
    else if(t.d!==6&&t.m<450)msg='Phones open at 7:30 AM';
    else if(t.d===5||t.d===6)msg='Phones open Sunday 7:30 AM';
    else msg='Phones open tomorrow 7:30 AM';
    [].forEach.call(document.querySelectorAll('[data-live]'),function(e){
      var s=e.getAttribute('data-live')==='short';
      e.textContent=s?'Open now':msg;e.hidden=s&&!open;e.classList.toggle('is-open',open);
    });
  }
  paint();setInterval(paint,60000);
})();
</script>
'''
rep('</body>', js + mapui.JS + '</body>')

# ---------- Washington symbols (inside the scenes) ----------
import wasym
import mural
_a = h.index('<div class="pnw pnw-night"'); _b = h.index('\n</div>', _a)
h = h[:_b] + '\n  ' + wasym.lighthouse2() + h[_b:]
rep('<!-- FAQ -->', mural.build() + '<!-- FAQ -->')
rep('\n/* footer */', mural.CSS + '\n/* footer */')
rep('conversions from the Tacoma area to the Marysville area.</p>', 'conversions from the Tacoma area to the Marysville area.</p>' + wasym.wa_outline2())
rep('<svg class="ico"><use href="#i-check"/></svg>', '<svg class="ico ev"><use href="#i-tree"/></svg>', 4)
rep('\n/* footer */', wasym.CSS2 + '\n/* footer */')

# ---------- reviews at the top: 849 reviews, 4.9 average (all platforms) ----------
rep('<span class="hdr-proof"><span class="stars">★★★★★</span>5-star reviews · Licensed &amp; insured</span>',
    '<span class="hdr-proof"><span class="stars" aria-hidden="true">★★★★★</span><b>4.9</b>&nbsp;from 849 reviews · Licensed &amp; insured</span>')
_k = h.index('<p class="kicker">')
h = h[:_k] + '<p class="rate" aria-label="Rated 4.9 out of 5 from 849 reviews"><span class="rate-stars" aria-hidden="true">★★★★★</span><b>4.9</b><span class="rate-n">849 reviews</span></p>\n      ' + h[_k:]
rep('\n/* footer */', '''
.hero .rate{margin:0;display:inline-flex;align-items:center;gap:8px;padding:7px 14px 7px 12px;border-radius:999px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);backdrop-filter:blur(6px);color:#fff;font:600 .9rem/1 var(--body)}
.hero .rate-stars{color:#ffc24b;letter-spacing:.06em;font-size:.95rem}
.hero .rate b{font:800 1rem/1 var(--body);color:#fff}
.hero .rate-n{color:#dfe5f0;font-weight:500}
.hero .rate-n::before{content:"·";margin-right:8px;color:#9aa6bd}
.hdr-proof b{color:var(--navy);font-weight:800;margin-left:2px}
@media (max-width:640px){.hero .rate{font-size:.82rem;padding:6px 12px 6px 10px;gap:6px}.hero .rate b{font-size:.92rem}.hero .rate-stars{font-size:.85rem}}
''' + '\n/* footer */')

# ---------- reviewer names + photos ----------
for _ic, _cls, _title, _img, _name in [
    ('i-search', 'av', 'Gas fireplace inspection', 'rv1', 'Jessica Brown'),
    ('i-wrench', 'av c2', 'Gas valve &amp; pilot assembly replaced', 'rv2', 'Mohit Parul'),
    ('i-flame', 'av c3', '37-year-old gas fireplace restored', 'rv3', 'Ashley Scheer'),
    ('i-swap', 'av c4', 'Wood-to-gas conversion', 'rv4', 'Elizabeth Phelps')]:
    rep('<span class="%s"><svg class="ico"><use href="#%s"/></svg></span><div><b>%s</b><small>Customer review</small></div>' % (_cls, _ic, _title),
        '<img class="av-img" src="img/%s.png" alt="%s" width="44" height="44" loading="lazy"><div><b>%s</b><small>%s</small></div>' % (_img, _name, _name, _title))
rep('Integrity like this is rare.&rdquo;</blockquote></figure>', 'Integrity like this is rare.&rdquo; <cite>— Jessica B.</cite></blockquote></figure>')
rep('\n/* footer */', '''
.av-img{width:44px;height:44px;border-radius:50%;object-fit:cover;flex:none;display:block;box-shadow:0 0 0 2px #fff,0 2px 6px rgba(29,49,87,.25);background:#e8ecf2}
.who b{font-size:.95rem}
.hero-proof cite{font-style:normal;font-weight:700;color:#fff;white-space:nowrap}
''' + '\n/* footer */')

# ---------- company name: Titan Chimney & Fireplace (this page = the gas fireplace page) ----------
rep('<title>Titan Gas Fireplace Service &amp; Repair</title>', '<title>Titan Chimney &amp; Fireplace | Gas Fireplace Service &amp; Repair</title>')
rep('og:title" content="Titan Gas Fireplace Service &amp; Repair"', 'og:title" content="Titan Chimney &amp; Fireplace | Gas Fireplace Service &amp; Repair"')
rep('apple-mobile-web-app-title" content="Titan Gas"', 'apple-mobile-web-app-title" content="Titan"')
rep('"name": "Titan Gas Fireplace Service & Repair"', '"name": "Titan Chimney & Fireplace"')
rep('<b>Titan Gas Fireplace</b><small>Service &amp; Repair · Seattle</small>', '<b>Titan Chimney &amp; Fireplace</b><small>Gas Fireplace Service &amp; Repair</small>')
rep('<div class="fname">Titan Gas Fireplace<br>Service &amp; Repair</div>', '<div class="fname">Titan Chimney &amp; Fireplace<br>Gas Fireplace Service &amp; Repair</div>')
rep('<div class="copy">© Titan Gas Fireplace Service &amp; Repair</div>', '<div class="copy">© Titan Chimney &amp; Fireplace</div>')
rep("I run Titan Gas Fireplace. We focus on gas fireplaces: pilots, valves, ignition, service, conversions, and new installs.",
    "I run Titan Chimney &amp; Fireplace. Our gas fireplace work covers pilots, valves, ignition, service, conversions, and new installs.")
rep('alt="Zachary, owner of Titan Gas Fireplace, outside the shop"', 'alt="Zachary, owner of Titan Chimney &amp; Fireplace, outside the shop"')
rep('alt="Titan Gas Fireplace sign"', 'alt="Titan sign on the shop wall"')
# the longer name still fits beside the Call button on small phones
rep('\n/* footer */', '\n@media (max-width:389px){.logo{gap:7px}.logo b{font-size:.9rem}.logo small{font-size:.5rem;letter-spacing:.04em}.mark{width:34px;height:29px}}\n@media (max-width:350px){.logo{gap:5px}.logo b{font-size:.74rem}.logo small{font-size:.42rem}.mark{width:30px;height:26px}}\n' + '\n/* footer */')
open(out, 'w').write(h)
