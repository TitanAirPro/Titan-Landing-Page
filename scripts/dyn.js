(function(){
  var V={
    repair:{k:"Seattle-Area Gas Fireplace Repair",a:"Gas Fireplace Won't Light?",b:"Get It Working Again Without a Surprise Bill.",l:"One call books your <b>free inspection</b>. We show you what's wrong and give you a written price before any work starts. No pressure.",p:["off","flame","spark","cloud","fan","cal"],c:0},
    pilot:{k:"Seattle-Area Gas Fireplace Repair",a:"Pilot Won't Stay Lit?",b:"Get It Lighting Again Without a Surprise Bill.",l:"Most of the time it's a worn thermocouple, thermopile, or a dirty pilot. One call books your <b>free inspection</b>. We find the cause and give you a written price before any work starts.",p:["flame","spark","off","cloud","fan","cal"],c:0},
    service:{k:"Seattle Gas Fireplace Service",a:"Gas Fireplace Due for Service?",b:"Get It Cleaned, Checked and Ready for the Season.",l:"We clean the burner, pilot, logs and glass, check the safety controls, and test everything before we leave. It starts with a <b>free inspection</b> and a written price.",p:["cloud","cal","fan","flame","spark","off"],c:1},
    inspection:{k:"Free Gas Fireplace Inspection · Seattle",a:"Is Your Gas Fireplace Safe to Use?",b:"Get a Free Inspection. No Charge, No Obligation.",l:"We check it top to bottom, show you what we find, and give you a written price only if something needs work. If it's fine, we tell you it's fine.",p:["cal","cloud","off","flame","spark","fan"],c:2},
    insert:{k:"Seattle Gas Fireplace & Insert Installation",a:"Want a New Gas Fireplace or Insert?",b:"Get It Installed Right, With a Written Price First.",l:"New gas fireplaces and inserts, venting, and gas line hookup, code-compliant and tested with you. It starts with a <b>free inspection</b> and a written price.",p:["cal","off","flame","spark","cloud","fan"],c:4},
    conversion:{k:"Seattle Wood-to-Gas Conversions",a:"Done Hauling Firewood?",b:"Switch to Push-Button Gas Heat. One Company Handles Everything.",l:"Permits, plans, parts, gas line, venting and install. It starts with a <b>free inspection</b> and a written price before any work begins.",p:["cal","off","flame","spark","cloud","fan"],c:3}
  };
  var BRANDS=["Heat & Glo","Napoleon","Regency","Valor","Mendota","Lennox","Majestic","Travis","Lopi","FireplaceX","Kozy Heat","Superior","Vermont Castings","Monessen","Empire","Heatilator"];
  function pick(){
    var q=new URLSearchParams(location.search),v=(q.get('v')||'').toLowerCase();
    if(V[v])return v;
    var kw=(q.get('kw')||q.get('utm_term')||'').toLowerCase();
    if(/pilot|thermocouple|thermopile|won.?t (light|stay)|click|ignit|spark/.test(kw))return 'pilot';
    if(/wood.{0,4}gas|convert|conversion/.test(kw))return 'conversion';
    if(/\binsert|\binstall|\bnew (gas )?fireplace|\breplac(e|ement)\b/.test(kw))return 'insert';
    if(/\binspect|\bsafety\b|\bsafe to use/.test(kw))return 'inspection';
    if(/clean|service|tune|maint|annual|yearly/.test(kw))return 'service';
    return 'repair';
  }
  function brand(){
    var b=(new URLSearchParams(location.search).get('brand')||'').toLowerCase();
    for(var i=0;i<BRANDS.length;i++)if(BRANDS[i].toLowerCase()===b)return BRANDS[i];return '';
  }
  function apply(v,br){
    var d=V[v]||V.repair,h=document.querySelector('.hero');if(!h)return;
    h.querySelector('.kicker').textContent=d.k;
    h.querySelector('.h1a').textContent=br?(br+" Fireplace Not Working?"):d.a;
    h.querySelector('.h1b').textContent=d.b;
    h.querySelector('.lede').innerHTML=d.l;
    document.documentElement.setAttribute('data-v',v);
    var sel=document.querySelector('.pv select');if(sel)sel.value=v;
    var probs=document.querySelector('.probs');
    if(probs){d.p.forEach(function(ic){var u=probs.querySelector('use[href="#i-'+ic+'"]');if(u){var a=u.closest('.prob');probs.appendChild(a);}});}
    var cards=document.querySelector('.cards');
    if(cards){var all=[].slice.call(cards.children),badge=cards.querySelector('.popular');
      all.forEach(function(c){c.classList.remove('pop');});
      var tgt=cards.querySelector('[data-i="'+d.c+'"]')||all[0];
      tgt.classList.add('pop');if(badge)tgt.insertBefore(badge,tgt.firstChild);cards.insertBefore(tgt,cards.firstChild);}
  }
  window.__titanApply=apply;
  var ready=function(){apply(pick(),brand());};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',ready);else ready();
})();
