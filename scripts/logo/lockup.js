const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const S=process.argv[2],OUT=process.argv[3];
const font=fs.readFileSync(S+'/node_modules/@fontsource/zilla-slab/files/zilla-slab-latin-700-normal.woff2').toString('base64');
const mark='data:image/png;base64,'+fs.readFileSync('/home/user/Titan-Landing-Page/scripts/logo/elephant_flame_full.png').toString('base64');
const css=`@font-face{font-family:Z;src:url(data:font/woff2;base64,${font}) format('woff2');font-weight:700}
html,body{margin:0;background:transparent}#l{display:inline-flex;align-items:center;padding:60px;font:700 300px/1 Z;letter-spacing:-.01em;white-space:nowrap}
#l img{display:block}`;
const V={
 'titan-chimney-fireplace-logo-horizontal':`<div id="l" style="gap:70px;color:#1d3157"><img src="${mark}" height="640"><span>Titan Chimney &amp; Fireplace</span></div>`,
 'titan-chimney-fireplace-logo-horizontal-white-text':`<div id="l" style="gap:70px;color:#ffffff"><img src="${mark}" height="640"><span>Titan Chimney &amp; Fireplace</span></div>`,
 'titan-chimney-fireplace-logo-stacked':`<div id="l" style="flex-direction:column;gap:40px;color:#1d3157;font-size:210px"><img src="${mark}" height="731"><span>Titan Chimney &amp; Fireplace</span></div>`};
const b=await chromium.launch();const p=await b.newPage({viewport:{width:6000,height:1600}});
for(const [n,html] of Object.entries(V)){await p.setContent(`<style>${css}</style>${html}`);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
 const e=await p.$('#l');await e.screenshot({path:OUT+'/'+n+'.png',omitBackground:true});}
await b.close();})();
