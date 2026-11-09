import re, sys
src, out = sys.argv[1], sys.argv[2]; h = open(src).read()
revs = re.findall(r'<div class="rcard">.*?</div></div></div>', h)
assert len(revs) == 4, len(revs)
R_FREE, R_PRICE, R_OLD, R_CONV = revs
PH = 'href="tel:+14253079165"'
def call(l2="Call now to get scheduled", l1="Call (425) 307-9165"):
    return '<a class="btn btn-call btn-big" %s><span class="l1"><svg class="ico"><use href="#i-phone"/></svg>%s</span><span class="l2">%s</span></a>' % (PH, l1, l2)
def prob(icon, title, said):
    return '<a class="prob" %s><span class="ib"><svg class="ico"><use href="#i-%s"/></svg></span><div><h3>%s</h3><p>%s</p><span class="go">Call about this <svg class="ico"><use href="#i-arrow"/></svg></span></div></a>' % (PH, icon, title, said)
def card(icon, title, body, btn, pop=False):
    global _ci
    _ci = globals().get('_ci', -1) + 1
    return '<article class="card%s" data-i="%d">%s<span class="icon-box"><svg class="ico"><use href="#i-%s"/></svg></span><h3>%s</h3><p>%s</p><a class="btn btn-navy" %s><svg class="ico"><use href="#i-phone"/></svg>%s</a></article>' % (
        " pop" if pop else "", _ci, '<span class="popular">Most Called For</span>' if pop else "", icon, title, body, PH, btn)
body = f'''
<!-- HERO -->
<section class="hero" id="top">
  <div class="wrap">
    <div class="hero-copy">
      <p class="kicker">Seattle Gas Fireplace Repair</p>
      <h1><span class="h1a">Gas Fireplace Won't Light?</span> <span class="h1b">Get It Working Again Without a Surprise Bill.</span></h1>
      <p class="lede">One call books your <b>free inspection</b>. We show you what's wrong and give you a written price before any work starts. No pressure.</p>
      <div class="hero-cta">
        {call()}
        <p class="cta-note"><span>Free inspection</span><span>A real person answers</span><span>Sun–Fri 7:30 AM – 10:30 PM</span></p>
      </div>
      <figure class="hero-proof"><span class="stars" aria-label="5 stars">★★★★★</span><blockquote>&ldquo;They found nothing wrong and didn't even charge us. Integrity like this is rare.&rdquo;</blockquote></figure>
    </div>
  </div>
</section>

<script>DYNJS</script>

<!-- TRUST STRIP -->
<div class="trust">
  <ul>
    <li><span class="ib"><svg class="ico"><use href="#i-search"/></svg></span><span>Free inspection<small>No charge, no obligation</small></span></li>
    <li><span class="ib"><svg class="ico"><use href="#i-doc"/></svg></span><span>Flat-rate price<small>Written, before any work</small></span></li>
    <li><span class="ib"><svg class="ico"><use href="#i-gear"/></svg></span><span>OEM parts<small>Whenever available</small></span></li>
    <li><span class="ib"><svg class="ico"><use href="#i-shield"/></svg></span><span>Licensed &amp; insured<small>Full coverage</small></span></li>
  </ul>
</div>

<!-- PROBLEMS (their words) -->
<section class="sec" id="problems">
  <div class="wrap">
    <div class="sec-head">
      <h2>What Is Your Fireplace Doing?</h2>
      <p>Tap the one that sounds like yours. We hear every one of these.</p>
    </div>
    <div class="probs">
      {prob("off", "It won't turn on", "&ldquo;I flip the switch and nothing happens.&rdquo;")}
      {prob("flame", "The pilot keeps going out", "&ldquo;It lights, then dies a few seconds later.&rdquo;")}
      {prob("spark", "It clicks but won't light", "&ldquo;I hear clicking, but the flame never catches.&rdquo;")}
      {prob("cloud", "Black glass or lazy flames", "&ldquo;Soot on the glass, yellow floppy flames, or an odd smell.&rdquo;")}
      {prob("fan", "The remote or fan quit", "&ldquo;The remote, wall switch, or blower stopped working.&rdquo;")}
      {prob("cal", "We haven't used it in years", "&ldquo;We moved in and never turned it on. Is it safe?&rdquo;")}
    </div>
  </div>
</section>

<!-- OBJECTION 1: what's the catch with free? -->
<section class="sec cream" id="call">
  <div class="wrap">
    <div class="sec-head">
      <h2>Free Means Free. Here's Exactly What Happens.</h2>
      <p>No catch. The inspection costs you nothing, and you never owe us for saying no.</p>
    </div>
    <div class="plan">
      <ol class="plan-steps">
        <li><div><h3>You call, a real person answers</h3><p>Tell us what your fireplace is doing. We answer your questions right there on the phone.</p></div></li>
        <li><div><h3>We book your free inspection</h3><p>Pick a time that works for you. It's booked before you hang up.</p></div></li>
        <li><div><h3>We show you what we find</h3><p>Our tech checks it, walks you through it, and hands you a written flat-rate price. If it's fine, we tell you it's fine.</p></div></li>
      </ol>
      <div class="plan-call">
        <h3>Book Your Free Inspection</h3>
        {call(l1="(425) 307-9165")}
        <p class="hours">Sun–Fri, 7:30 AM – 10:30 PM</p>
        <div class="tip"><svg class="ico"><use href="#i-users"/></svg><span><b>Make the visit count:</b> if someone else in the home helps decide, have them there or on the phone. You'll get every answer in one visit.</span></div>
      </div>
    </div>
    <div class="spot">{R_FREE}</div>
  </div>
</section>

<!-- VIDEO TESTIMONIALS -->
<section class="sec vid" id="video">
  <div class="wrap vid-grid">
    <div class="vid-txt">
      <h2>Hear It From Seattle Homeowners</h2>
      <p>Real customers, in their own homes, talking about what happened when they called.</p>
      {call()}
    </div>
    <div class="vslot">
      <div class="vframe">
        <video class="tvid" src="img/testimonial.mp4" poster="img/poster.jpg" muted playsinline loop preload="auto" aria-label="Customer video testimonials"></video>
        <button class="vsound" type="button"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg><span>Tap for sound</span></button>
      </div>
    </div>
  </div>
</section>

<!-- AMBER BAND -->
<div class="band"><strong>Free gas fireplace inspections in Seattle.</strong> <span>Call now to get on the schedule.</span> <a {PH}>Call (425) 307-9165 →</a></div>

<!-- SERVICES -->
<!-- OBJECTION 2: will they upsell me? -->
<section class="sec deep" id="price">
  <div class="wrap">
    <div class="sec-head">
      <h2>You See the Price Before Anything Gets Touched</h2>
      <p>Written flat-rate price. You approve it, or we pack up. That's it.</p>
    </div>
    <ul class="never">
      <li><span class="x">✕</span><div><strong>We never start without your OK.</strong><span>You get the written price first and decide before any work begins.</span></div></li>
      <li><span class="x">✕</span><div><strong>We never invent problems.</strong><span>If a part has years left, you'll hear that from us.</span></div></li>
      <li><span class="x">✕</span><div><strong>We never add surprise fees.</strong><span>The price we quote is the price you pay.</span></div></li>
      <li><span class="x">✕</span><div><strong>We never push you to decide.</strong><span>Take your time. We'll be here.</span></div></li>
      <li><span class="x">✕</span><div><strong>We never leave a mess.</strong><span>Floor protection on every job. We leave it cleaner than we found it.</span></div></li>
    </ul>
    <div class="spot spot-dark">{R_PRICE}</div>
  </div>
</section>

<!-- WHAT WE FIX + OBJECTION 3: is my old fireplace worth fixing? -->
<section class="sec">
  <div class="wrap">
    <div class="sec-head sec-head-l2">
      <h2>Old, New, or Never Used, We Fix Gas Fireplaces</h2>
      <p>Repairs, yearly service, inserts, and wood-to-gas conversions. It all starts with a free inspection.</p>
    </div>
    <div class="cards">
      {card("wrench", "Gas Fireplace Repair", "Pilot assemblies, thermocouples, thermopiles, gas valves, and ignition systems. Fixed with OEM parts whenever they're available.", "Call About Repair", True)}
      {card("gear", "Service &amp; Cleaning", "Yearly tune-up. We clean the burner, pilot, logs, and glass, check the safety controls, and test everything before we leave.", "Call About Service")}
      {card("search", "Free Inspection", "A full safety and operation check of your gas fireplace. We show you what we find. No charge and no obligation.", "Book Free Inspection")}
      {card("swap", "Wood-to-Gas Conversion", "Turn a wood fireplace into push-button heat. We handle permits, plans, parts, and the full install as one company.", "Call About Conversion")}
      {card("box", "Gas Inserts &amp; Installs", "New gas fireplaces and inserts, venting, and gas line hookup. Code-compliant, tested, and walked through with you.", "Call About Installs")}
      {card("sliders", "Logs, Remotes &amp; Blowers", "Gas log sets, remotes, wall switches, thermostats, and blower fans, repaired or replaced.", "Call for a Price")}
    </div>
    <div class="revs revs-tight">{R_OLD}{R_CONV}</div>
  </div>
</section>

<!-- OBJECTION 4: who is coming into my home? -->
<section class="split">
  <div class="wrap">
    <div class="slides" aria-roledescription="carousel" aria-label="Our crew at work">
      <div class="slides-track">
        <figure class="slide is-on"><img src="img/w01.jpg" alt="Titan tech relighting a gas fireplace after a repair" width="1200" height="900"></figure>
        <figure class="slide"><img src="img/w02.jpg" alt="Titan tech working on a gas fireplace with floor protection down" width="1200" height="900"></figure>
        <figure class="slide"><img src="img/w03.jpg" alt="Titan tech repairing a Heat & Glo gas fireplace" width="1200" height="900"></figure>
        <figure class="slide"><img src="img/w04.jpg" alt="Titan crew on a Seattle-area roof servicing a chimney" width="1200" height="900"></figure>
        <figure class="slide"><img src="img/w05.jpg" alt="Titan tech replacing gas fireplace parts" width="1200" height="900"></figure>
        <figure class="slide"><img src="img/w06.jpg" alt="Titan tech testing a gas valve with shoe covers on" width="1200" height="900"></figure>
        <figure class="slide"><img src="img/w07.jpg" alt="Titan tech walking a homeowner through a gas insert" width="1200" height="900"></figure>
        <figure class="slide"><img src="img/w08.jpg" alt="Titan tech working under a gas fireplace burner" width="1200" height="900"></figure>
        <figure class="slide"><img src="img/w09.jpg" alt="Titan tech cleaning fireplace glass" width="1200" height="900"></figure>
        <figure class="slide"><img src="img/w10.jpg" alt="Gas fireplace repair setup with parts and tools on a tarp" width="1200" height="900"></figure>
        <figure class="slide"><img src="img/w11.jpg" alt="Titan tech inspecting a fireplace insert" width="1200" height="900"></figure>
        <figure class="slide"><img src="img/w12.jpg" alt="Titan tech cleaning a brick fireplace" width="1200" height="900"></figure>
        <figure class="slide"><img src="img/w13.jpg" alt="Fireplace glass and new gasket during a repair" width="1200" height="900"></figure>
      </div>
      <div class="slides-dots"></div>
    </div>
    <div class="split-txt">
      <h2>Local Techs in Your Home. Not a Call Center.</h2>
      <ul>
        <li><svg class="ico"><use href="#i-check"/></svg>Gas fireplace specialists, not generalists</li>
        <li><svg class="ico"><use href="#i-check"/></svg>Licensed and insured, with real Titan techs</li>
        <li><svg class="ico"><use href="#i-check"/></svg>Floor protection, clean work, tested before we leave</li>
        <li><svg class="ico"><use href="#i-check"/></svg>Something not right? We come back and make it right</li>
      </ul>
      <div class="cta-stack">
        {call()}
        <p class="hours">Sun–Fri, 7:30 AM – 10:30 PM</p>
      </div>
    </div>
  </div>
</section>

<!-- OWNER -->
<section class="sec cream">
  <div class="wrap owner">
    <figure class="photo"><img src="img/storefront.jpg" alt="Zachary, owner of Titan Gas Fireplace, outside the shop" loading="lazy" width="1024" height="572"><figcaption>Zachary, Owner</figcaption></figure>
    <div class="owner-txt">
      <span class="eyebrow">From the Owner</span>
      <h2>My Name Is on Every Job</h2>
      <p>I'm Zachary, and I run Titan Gas Fireplace. We focus on gas fireplaces: pilots, valves, ignition, service, conversions, and new installs.</p>
      <p>Every job starts with a free inspection. We show you what we find and give you a written, flat-rate price before we start. If your fireplace is fine, we tell you it's fine. And if something isn't right after we leave, we come back and make it right.</p>
      <p class="sig">— Zachary, Owner</p>
      {call()}
    </div>
  </div>
</section>

<!-- FAQ -->
<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>Questions People Ask Before They Call</h2></div>
    <div class="faq">
      <details><summary>Is the inspection really free?</summary><p>Yes. No charge and no obligation. We check your fireplace, show you what we find, and give you a written price if anything needs work. <strong>You decide from there.</strong></p></details>
      <details><summary>What's the catch?</summary><p>There isn't one. Most people who call us want their fireplace fixed, so a free, honest inspection is how we earn the job. If it doesn't need work, we tell you that.</p></details>
      <details><summary>How do I get scheduled?</summary><p>Call <strong>(425) 307-9165</strong>. A real person answers, asks a few questions about your fireplace, and books a time that works for you while you're on the phone.</p></details>
      <details><summary>Who should be home for the visit?</summary><p>Anyone 18 or older can let us in. If someone else in the home helps decide, it's best to have them there or on the phone, so we can walk everyone through what we find and answer pricing questions in one visit.</p></details>
      <details><summary>Why won't my gas fireplace pilot stay lit?</summary><p>The most common causes are a worn thermocouple or thermopile, a dirty pilot, or a weak gas supply to the pilot. <strong>We'll find the cause during your free inspection.</strong></p></details>
      <details><summary>Is my old fireplace worth fixing?</summary><p>Usually, yes. We've restored fireplaces close to 40 years old. We'll tell you honestly if a repair makes sense or if replacing it is the better buy.</p></details>
      <details><summary>Do you give a price before you start?</summary><p>Yes. You get a written, flat-rate price after the inspection. <strong>Nothing starts until you approve it.</strong></p></details>
      <details><summary>Can you convert my wood fireplace to gas?</summary><p>Yes. We handle the whole project: permits, plans, parts, gas line, venting, and installation, then test everything before we leave.</p></details>
      <details><summary>I smell gas. What should I do?</summary><p><strong>Leave the house right away.</strong> Don't flip switches or use the fireplace. Call 911 or your gas company from outside. Once it's safe, call us to find and fix the problem.</p></details>
    </div>
  </div>
</section>

<!-- FINAL CTA -->
<section class="sec final">
  <div class="wrap final-grid">
    <figure class="photo"><img src="img/sign.jpg" alt="Titan Gas Fireplace sign" loading="lazy" width="1024" height="572"></figure>
    <div class="final-txt">
      <span class="eyebrow">Free Inspection</span>
      <h2>Call Now to Get Scheduled</h2>
      <p>A real person answers · Written flat-rate price · Licensed &amp; insured</p>
      {call(l1="(425) 307-9165")}
      <p class="hours">Sun–Fri, 7:30 AM – 10:30 PM · Closed Saturday</p>
    </div>
  </div>
</section>

'''
i = h.index('<!-- HERO -->'); j = h.index('<!-- FOOTER -->')
h = h[:i] + body.lstrip('\n').replace('DYNJS', open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'dyn.js')).read()) + h[j:]
PV = '<div class="pv"><label>Preview ad version (this bar is not on the live site): <select onchange="__titanApply(this.value,\'\');scrollTo(0,0)"><option value="repair">Gas fireplace repair (default)</option><option value="pilot">Pilot / won\'t light / clicking</option><option value="service">Service / cleaning</option><option value="inspection">Inspection</option><option value="insert">New fireplace / insert</option><option value="conversion">Wood-to-gas conversion</option></select></label> <label style="margin-left:10px">Font: <select onchange="document.documentElement.dataset.font=this.value"><option value="slab">Slab Heritage (recommended)</option><option value="signage">Signage Condensed</option><option value="news">Newspaper Grotesk</option><option value="current">Current (Barlow)</option></select></label></div>'
h = h.replace('<header class="top">', PV + '\n<header class="top">', 1)
h = h.replace('<html lang="en">', '<html lang="en" data-font="slab">', 1)
css = '''
.pv{background:#fff6d6;border-bottom:1px solid #f0c867;font:600 .8rem/1.3 var(--body);color:#1d3157;padding:8px 16px;text-align:center}.pv select{font:inherit;margin-left:6px;padding:4px 6px;border-radius:6px;border:1px solid #c9b46a;background:#fff;max-width:100%}
.pains{margin:0;font:600 .92rem/1.4 var(--body);color:#ffd690;letter-spacing:.01em;text-wrap:balance}
@media (max-width:640px){.pains{text-align:center}}
.spot{max-width:760px;margin:36px auto 0}
.spot .rcard{box-shadow:0 22px 44px -30px rgba(29,49,87,.55)}
.spot-dark .rcard{background:rgba(255,255,255,.96)}
.revs-tight{margin-top:28px}
.vid{background:linear-gradient(180deg,var(--white),#f6f1ee)}
.vid-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.8fr);gap:44px;align-items:center}
.vid-txt{display:grid;gap:16px;justify-items:start}
.vid-txt p{color:var(--muted);font-size:1.02rem}
.vslot{display:flex;justify-content:center}
.vframe{position:relative;width:min(100%,340px);aspect-ratio:9/16;border-radius:20px;overflow:hidden;background:linear-gradient(160deg,#1d3157,#3b3a74 60%,#a8708a);box-shadow:0 30px 60px -30px rgba(16,28,51,.7)}
.vframe video{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;background:#000;display:block}
.vsound{position:absolute;left:50%;bottom:16px;transform:translateX(-50%);display:inline-flex;align-items:center;gap:8px;border:0;border-radius:999px;padding:10px 16px;background:rgba(16,28,51,.78);color:#fff;font:600 .85rem/1 var(--body);cursor:pointer;backdrop-filter:blur(6px);transition:opacity .3s}
.vsound svg{width:18px;height:18px;fill:currentColor}
.vsound.off{opacity:0;pointer-events:none}
.vph{position:absolute;inset:0;display:grid;place-content:center;justify-items:center;gap:8px;color:#fff;text-align:center;padding:20px}
.vph .play{width:64px;height:64px;border-radius:50%;background:rgba(255,255,255,.18);display:grid;place-items:center;border:1px solid rgba(255,255,255,.4)}
.vph .play svg{width:26px;height:26px;fill:#fff;margin-left:3px}
.vph b{font:700 1.15rem/1.2 var(--display);letter-spacing:.02em}
.vph small{color:#d7dcea;font-size:.8rem}
@media (max-width:820px){.vid-grid{grid-template-columns:1fr;gap:26px}.vid-txt{justify-items:center;text-align:center}.vid-txt .btn-call{width:100%}}
.slides{position:relative}
.slides-track{position:relative;aspect-ratio:4/3;border-radius:14px;overflow:hidden;box-shadow:0 26px 50px -26px rgba(0,0,0,.6);background:#0c1528}
.slide{position:absolute;inset:0;margin:0;opacity:0;transition:opacity .45s ease;overflow:hidden}
.slide::before{content:"";position:absolute;inset:-30px;background:var(--bg) center/cover;filter:blur(22px) brightness(.55);transform:scale(1.1)}
.slide img{position:relative}
.slide.is-on{opacity:1}
.slide img{width:100%;height:100%;object-fit:contain;display:block}
.slides-dots{display:flex;gap:8px;justify-content:center;margin-top:14px}
.slides-dots button{width:9px;height:9px;border-radius:50%;border:0;padding:0;background:rgba(255,255,255,.35);cursor:pointer;transition:background .3s,transform .3s}
.slides-dots button.on{background:var(--gold);transform:scale(1.25)}
@media (min-width:861px){.sec-head-l2{justify-items:start;text-align:left;margin-left:0;max-width:760px}}
'''
h = h.replace('\n/* footer */', css + '\n/* footer */', 1)
slides_js = '''<script>
(function(){
  var root=document.querySelector('.slides');if(!root)return;
  var s=[].slice.call(root.querySelectorAll('.slide')),dots=root.querySelector('.slides-dots'),i=0,tm=0;
  var still=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  s.forEach(function(f){var im=f.querySelector('img');if(im)f.style.setProperty('--bg','url("'+im.getAttribute('src')+'")');});
  s.forEach(function(_,k){var b=document.createElement('button');b.setAttribute('aria-label','Photo '+(k+1));b.onclick=function(){go(k);restart();};dots.appendChild(b);});
  function go(k){s[i].classList.remove('is-on');dots.children[i].classList.remove('on');i=(k+s.length)%s.length;s[i].classList.add('is-on');dots.children[i].classList.add('on');}
  function restart(){clearInterval(tm);if(!still)tm=setInterval(function(){go(i+1);},2200);}
  var x0=null;root.addEventListener('touchstart',function(e){x0=e.touches[0].clientX;},{passive:true});
  root.addEventListener('touchend',function(e){if(x0==null)return;var d=e.changedTouches[0].clientX-x0;if(Math.abs(d)>40){go(i+(d<0?1:-1));restart();}x0=null;});
  go(0);restart();
})();
(function(){
  var v=document.querySelector('.tvid'),b=document.querySelector('.vsound');if(!v)return;
  var still=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){if(!still||!v.muted)v.play().catch(function(){});}else v.pause();});},{threshold:.35}).observe(v);
  b.addEventListener('click',function(){v.muted=false;v.currentTime=0;v.loop=false;v.controls=true;v.play().catch(function(){});b.classList.add('off');});
})();
</script>
'''
h = h.replace('</body>', slides_js + '</body>', 1)
k = h.index('/* ---------- PHONE layout'); e = h.index('</style>', k)
h = h[:e] + '\n/* ---------- type system ---------- */\nhtml{--ls-d:0;--ls-btn:.01em}\nhtml[data-font="slab"]{--display:"Zilla Slab",Rockwell,Georgia,serif;--body:"Public Sans","Helvetica Neue",Arial,sans-serif}\nhtml[data-font="signage"]{--display:"Archivo","Arial Narrow",sans-serif;--body:"Archivo","Helvetica Neue",Arial,sans-serif}\nhtml[data-font="news"]{--display:"Schibsted Grotesk","Helvetica Neue",Arial,sans-serif;--body:"Schibsted Grotesk","Helvetica Neue",Arial,sans-serif}\nhtml[data-font="current"]{--display:"Barlow Condensed","Arial Narrow",sans-serif;--body:"Barlow","Helvetica Neue",Arial,sans-serif}\n/* readable body: bigger, comfortable line length */\nbody{font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased;font-feature-settings:"kern","liga"}\n.sec-head p,.lede,.owner-txt p,.faq p{max-width:62ch}\n/* phone numbers line up and read cleanly */\n.btn-call,.btn-big .l1,.fphone,.hdr-call .btn,.band a{font-variant-numeric:tabular-nums lining-nums}\n/* fewer shouty tracked capitals (an AI-template tell) */\n.eyebrow{letter-spacing:.08em}\nhtml .hero .kicker{letter-spacing:.02em;text-transform:none;font-size:1rem;font-weight:700}\n.logo small{letter-spacing:.06em}\n/* slab heritage */\nhtml[data-font="slab"] h1,html[data-font="slab"] h2,html[data-font="slab"] h3{letter-spacing:-.01em;font-weight:700;line-height:1.08}\nhtml[data-font="slab"] .hero .h1a{font-weight:700;font-size:clamp(2.6rem,5vw,4rem);line-height:1.02}\nhtml[data-font="slab"] .hero .h1b{font-weight:600;font-size:clamp(1.5rem,2.5vw,2.05rem);line-height:1.15}\nhtml[data-font="slab"] .btn-call,html[data-font="slab"] .btn-big .l1,html[data-font="slab"] .hdr-call .btn{letter-spacing:0}\nhtml[data-font="slab"] h2{font-size:clamp(1.95rem,4.2vw,2.7rem)}\n/* signage condensed: tall, punchy headlines; normal-width body */\nhtml[data-font="signage"] h1,html[data-font="signage"] h2,html[data-font="signage"] h3,html[data-font="signage"] .btn-call,html[data-font="signage"] .btn-big .l1,html[data-font="signage"] .hdr-call .btn,html[data-font="signage"] .logo b,html[data-font="signage"] .fphone,html[data-font="signage"] .fname,html[data-font="signage"] .band a{font-stretch:68%;letter-spacing:0}\nhtml[data-font="signage"] h1,html[data-font="signage"] h2,html[data-font="signage"] h3{font-weight:800}\nhtml[data-font="signage"] .hero .h1a{font-weight:800;line-height:.96;font-stretch:68%}\nhtml[data-font="signage"] .hero .h1b{font-weight:700;font-stretch:75%}\nhtml[data-font="signage"] .cta-note,html[data-font="signage"] .btn-big .l2{font-stretch:100%}\n/* newspaper grotesk: credible, editorial */\nhtml[data-font="news"] h1,html[data-font="news"] h2,html[data-font="news"] h3{letter-spacing:-.02em;font-weight:800;line-height:1.04}\nhtml[data-font="news"] .hero .h1a{font-weight:800;font-size:clamp(2.5rem,4.9vw,3.9rem);letter-spacing:-.03em}\nhtml[data-font="news"] .hero .h1b{font-weight:700;font-size:clamp(1.45rem,2.4vw,2rem);letter-spacing:-.015em}\nhtml[data-font="news"] .btn-call,html[data-font="news"] .btn-big .l1,html[data-font="news"] .hdr-call .btn{letter-spacing:-.01em;font-weight:800}\nhtml[data-font="news"] h2{font-size:clamp(1.9rem,4vw,2.6rem)}\n@media (max-width:640px){\n  body{font-size:17px}\n  html[data-font="slab"] .hero .h1a{font-size:clamp(2.15rem,9.6vw,2.55rem)}\n  html[data-font="slab"] .hero .h1b{font-size:clamp(1.25rem,5.5vw,1.45rem)}\n  html[data-font="news"] .hero .h1a{font-size:clamp(2.1rem,9.4vw,2.5rem)}\n  html[data-font="news"] .hero .h1b{font-size:clamp(1.2rem,5.3vw,1.4rem)}\n  html[data-font="slab"] h2,html[data-font="news"] h2{font-size:clamp(1.65rem,7.2vw,2rem)}\n  html .hero .kicker{font-size:.9rem}\n}\n' + '\n/* hero v2 */\n.hero .kicker{margin:0;font:700 .78rem/1 var(--body);letter-spacing:.18em;text-transform:uppercase;color:var(--gold)}\n.hero h1{display:grid;gap:.18em;font-size:inherit;line-height:1;margin:0}\n.hero .h1a{font:800 clamp(2.9rem,5.6vw,4.3rem)/.98 var(--display);color:#fff;letter-spacing:-.01em;text-wrap:balance}\n.hero .h1b{font:700 clamp(1.7rem,2.9vw,2.35rem)/1.08 var(--display);color:var(--gold);text-wrap:balance;max-width:16em}\n.hero .lede{font-size:1.1rem;line-height:1.55;max-width:31em;color:#dfe5f0;margin:0}\n.hero .lede b{color:#fff;font-weight:700}\n.hero-cta{display:grid;gap:10px;justify-items:start}\n.cta-note{margin:0;display:flex;flex-wrap:wrap;gap:4px 0;font:500 .84rem/1.3 var(--body);color:#b8c3d8}\n.cta-note span+span::before{content:"·";margin:0 8px;color:#7f8aa1}\n.hero-proof{margin:4px 0 0;display:flex;align-items:center;gap:10px;max-width:34em}\n.hero-proof .stars{font-size:.95rem;flex:none}\n.hero-proof blockquote{margin:0;font:italic 500 .92rem/1.4 var(--body);color:#e6ebf4}\n.hero .checks,.hero .pill,.hero .hero-hours,.hero .proof,.hero .pains{display:none}\n@media (max-width:640px){\n  .hero .wrap{padding-top:calc(55.86vw - 40px);padding-bottom:26px}\n  .hero-copy{gap:12px}\n  .hero .kicker{font-size:.7rem;letter-spacing:.16em}\n  .hero .h1a{font-size:clamp(2.45rem,11.2vw,2.95rem)}\n  .hero .h1b{font-size:clamp(1.38rem,6.3vw,1.62rem);max-width:none}\n  .hero .lede{font-size:clamp(.94rem,4.15vw,1.02rem);line-height:1.5}\n  .hero-cta{justify-items:stretch;width:100%;gap:8px}\n  .cta-note{justify-content:center;font-size:.76rem}\n  .hero-proof{flex-direction:column;gap:3px;text-align:center}\n  .hero-proof blockquote{font-size:.86rem}\n}\n' + h[e:]
open(out, 'w').write(h)
