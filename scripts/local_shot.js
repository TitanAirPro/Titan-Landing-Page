const {chromium}=require('playwright');const N=process.cwd()+'/node_modules/';
const f=(fam,path,w)=>`@font-face{font-family:"${fam}";font-weight:${w};src:url(file://${N}${path})}`;
const css=[f('Zilla Slab','@fontsource/zilla-slab/files/zilla-slab-latin-600-normal.woff2',600),f('Zilla Slab','@fontsource/zilla-slab/files/zilla-slab-latin-700-normal.woff2',700),...[400,500,600,700,800].map(w=>f('Public Sans',`@fontsource/public-sans/files/public-sans-latin-${w}-normal.woff2`,w))].join('');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'});const errs=[];
for(const [n,vw,vh,when] of [['m',390,844,'2026-10-18T16:30:00-07:00'],['d',1440,900,'2026-10-18T16:30:00-07:00'],['mc',390,844,'2026-10-23T23:30:00-07:00']]){
const p=await b.newPage({viewport:{width:vw,height:vh},deviceScaleFactor:2});p.on('pageerror',e=>errs.push(e.message));
await p.clock.setFixedTime(new Date(when));
await p.route(/fonts\.(googleapis|gstatic)/,r=>r.abort());await p.goto('file:///home/claude/site/variant/index.html',{timeout:90000});await p.addStyleTag({content:css});await p.waitForTimeout(800);
await p.screenshot({path:`L-${n}-hero.png`});
if(n==='mc'){console.log(await p.evaluate(()=>[...document.querySelectorAll('[data-live]')].map(e=>e.hidden+':'+e.textContent)));continue;}
console.log(await p.evaluate(()=>[...document.querySelectorAll('[data-live]')].map(e=>e.hidden+':'+e.textContent)));
await p.evaluate(()=>document.querySelector('.cities').open=true);for(const sel of ['#area','.trust']){const el=await p.$(sel);await el.scrollIntoViewIfNeeded();await p.waitForTimeout(300);
 await el.screenshot({path:`L-${n}-${sel.replace(/[^a-z]/g,'')}.png`});}
}
console.log('errors',errs);await b.close();})();
