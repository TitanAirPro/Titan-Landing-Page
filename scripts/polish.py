import re, sys
sys.path.insert(0, sys.argv[3]); from icons import symbols, LOGO_FLAME, FAVICON
src, out = sys.argv[1], sys.argv[2]; h = open(src).read()
def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)
def srep(a, b):
    global h
    h = h.replace(a, b)
def resub(pat, b, flags=re.S):
    global h
    h2, k = re.subn(pat, lambda m: b, h, count=1, flags=flags); assert k == 1, pat[:60]; h = h2
# custom icon set
first = h.index('<symbol id="i-phone"'); last = h.index('</symbol>', h.index('<symbol id="i-users"')) + len('</symbol>')
h = h[:first] + symbols() + h[last:]
rep('.ico{width:20px;height:20px;flex:none;stroke:currentColor;fill:none;stroke-width:2;', '.ico{width:20px;height:20px;flex:none;stroke:currentColor;fill:none;stroke-width:1.8;')
# icons sit on the page, no tinted boxes/circles
rep('.trust .ib{width:38px;height:38px;flex:none;border-radius:50%;background:#fff1e6;color:var(--orange);display:grid;place-items:center}', '.trust .ib{width:30px;height:30px;flex:none;color:var(--orange);display:grid;place-items:center}.trust .ib .ico{width:28px;height:28px}')
rep('  .trust .ib{width:38px;height:38px}', '  .trust .ib{width:28px;height:28px}')
rep('.prob .ib{width:44px;height:44px;border-radius:10px;background:var(--navy);color:var(--white);display:grid;place-items:center}', '.prob .ib{width:44px;height:44px;color:var(--red);display:grid;place-items:center}.prob .ib .ico{width:32px;height:32px}')
rep('  .prob .ib{width:38px;height:38px}', '  .prob .ib{width:36px;height:36px}.prob .ib .ico{width:28px;height:28px}')
rep('.icon-box{width:40px;height:40px;border-radius:9px;background:var(--red);color:var(--white);display:grid;place-items:center}', '.icon-box{width:40px;height:40px;color:var(--red);display:grid;place-items:start}.icon-box .ico{width:34px;height:34px}')
# logo: the Titan elephant with a flame on its trunk (img/logo.png, made in scripts/logo/); new favicon
rep('<span class="mark">TG</span>', '<img class="mark" src="img/logo.png" alt="" width="153" height="132">')
rep('.mark{width:40px;height:40px;flex:none;border-radius:8px;background:var(--red);color:var(--white);display:grid;place-items:center;font:400 1.15rem/1 var(--display)}', '.mark{width:46px;height:40px;flex:none;display:block}')
rep('.mark{width:34px;height:34px;font-size:1rem}', '.mark{width:39px;height:34px}')
resub(r'<link rel="icon" href="[^"]*">', '<link rel="icon" href="%s">' % FAVICON)
# type: Barlow / Barlow Condensed instead of Anton + Inter
rep('family=Anton&family=Inter:wght@400;500;600;700;800', 'family=Zilla+Slab:wght@600;700&family=Public+Sans:wght@400;500;600;700;800&family=Archivo:wdth,wght@62..100,400..800&family=Schibsted+Grotesk:wght@400..800&family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600;700')
rep('--display:"Anton","Impact","Arial Narrow Bold",sans-serif;', '--display:"Barlow Condensed","Arial Narrow",sans-serif;')
rep('--body:"Inter","Helvetica Neue",Arial,sans-serif;', '--body:"Barlow","Helvetica Neue",Arial,sans-serif;')
rep('h1,h2,h3{font-family:var(--display);font-weight:400;color:var(--ink);margin:0;line-height:1.06;text-wrap:balance;letter-spacing:.005em}', 'h1,h2,h3{font-family:var(--display);font-weight:700;color:var(--ink);margin:0;line-height:1.02;text-wrap:balance;letter-spacing:-.005em}')
h, k = re.subn(r'font:400 ([^;{}]*?var\(--display\))', r'font:700 \1', h); assert k >= 8, k
rep('h2{font-size:clamp(2rem,4.6vw,2.8rem)}', 'h2{font-size:clamp(2.15rem,4.8vw,3rem)}')
# quieter CTA shadow
rep('box-shadow:0 12px 26px -12px rgba(255,122,28,.8)}', 'box-shadow:0 6px 14px -8px rgba(200,90,10,.55)}')
# drop the 6-tile "Why" grid (repeats the trust strip and promise list)
h = re.sub(r'\n<!-- WHY US -->\n<section class="sec">.*?</section>\n', '\n', h, flags=re.S)
rep('.card,.why div{transition', '.card{transition'); rep('.card:hover,.why div:hover{', '.card:hover{')
rep('@media (max-width:860px) and (min-width:641px){.why{grid-template-columns:repeat(2,1fr)}.revs{grid-template-columns:1fr}}', '@media (max-width:860px) and (min-width:641px){.revs{grid-template-columns:1fr}}')
rep('@media (max-width:360px){.probs,.why{grid-template-columns:1fr}', '@media (max-width:360px){.probs{grid-template-columns:1fr}')
h = re.sub(r'\n[ ]*\.(why|circ)\b[^\n]*', '', h)
h = re.sub(r'\n/\* why \*/', '', h)
# fewer section labels; vary alignment
for lab in ('How It Works', 'Sound Familiar?', 'Customer Reviews', 'Our Promise'):
    srep('\n      <span class="eyebrow">%s</span>' % lab, '')
srep('<div class="sec-head">\n      <span class="eyebrow">Our Services</span>', '<div class="sec-head sec-head-l">')
srep('<div class="sec-head"><span class="eyebrow">Questions</span>', '<div class="sec-head sec-head-l">')
rep('\n/* footer */', '\n@media (min-width:861px){.sec-head-l{justify-items:start;text-align:left;margin-left:0;max-width:760px}}\n/* footer */')
# warm glow behind the final call to action (draws the eye to the button)
rep('.final{background:repeating-linear-gradient(135deg,rgba(255,255,255,.02) 0 2px,transparent 2px 7px),var(--navy);color:#d5dcea}',
    '.final{background:radial-gradient(ellipse 46% 52% at 74% 56%,rgba(255,138,92,.2),rgba(255,138,92,0) 70%),radial-gradient(ellipse 40% 46% at 70% 60%,rgba(206,120,170,.16),rgba(206,120,170,0) 72%),repeating-linear-gradient(135deg,rgba(255,255,255,.02) 0 2px,transparent 2px 7px),var(--navy);color:#d5dcea}')
rep('@media (max-width:820px){.final-grid{grid-template-columns:1fr;gap:28px}}','@media (max-width:820px){.final-grid{grid-template-columns:1fr;gap:28px}.final{background:radial-gradient(ellipse 90% 30% at 50% 74%,rgba(255,138,92,.2),rgba(255,138,92,0) 70%),radial-gradient(ellipse 80% 26% at 50% 80%,rgba(206,120,170,.15),rgba(206,120,170,0) 72%),repeating-linear-gradient(135deg,rgba(255,255,255,.02) 0 2px,transparent 2px 7px),var(--navy)}}')
# dead footer links
rep(' · <a href="#">Privacy</a> · <a href="#">Terms</a>', '')
open(out, 'w').write(h)
