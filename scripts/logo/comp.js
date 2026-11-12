const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [s,tx,ty,out]=process.argv.slice(2).map((v,i)=>i<3?+v:v);
const b64=f=>'data:image/png;base64,'+fs.readFileSync(f).toString('base64');
const flame=`<g transform="translate(${tx} ${ty}) scale(${s})"><path fill="#ff7a1c" d="M12 27c-5.4 0-9.2-3.8-9.2-8.9 0-4.6 3.1-7.1 4.7-11 .9 2.2 2.1 3.4 3.6 4.1-.6-4.1 1.3-8 4.4-11 .6 5.4 5.7 8.4 5.7 15.4C21.2 22.2 17.4 27 12 27z"/><path fill="#d33b2c" d="M12 25.2c-2.3 0-3.9-1.6-3.9-3.8 0-2.3 1.9-3.6 3.1-5.9 1.4 1.9 4.7 3.3 4.7 6.2 0 2.1-1.7 3.5-3.9 3.5z"/></g>`;
const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="730" viewBox="0 0 1024 730"><image href="${b64(__dirname+'/base.png')}" width="1024" height="730"/>${flame}<image href="${b64(__dirname+'/trunk.png')}" width="1024" height="730"/></svg>`;
const br=await chromium.launch();const p=await br.newPage({viewport:{width:1024,height:730}});
await p.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
await p.screenshot({path:out,omitBackground:true,clip:{x:0,y:0,width:1024,height:730}});await br.close();})();
