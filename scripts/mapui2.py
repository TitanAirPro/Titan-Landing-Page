import os, json, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import areamap
NM = os.path.join(HERE, 'node_modules')

TIER1 = ["Seattle", "Tacoma", "Everett", "Olympia", "Bellevue"]
TIER3 = [("Bremerton", 47.567, -122.633), ("Port Orchard", 47.540, -122.636), ("Poulsbo", 47.736, -122.646), ("Shelton", 47.215, -123.100), ("Oak Harbor", 48.293, -122.643)]
def labels():
    out, seen = [], set()
    for n, a, b in areamap.CENTERS:
        if n in seen: continue
        seen.add(n); out.append([n, a, b, 1 if n in TIER1 else 2])
    out += [[n, a, b, 3] for n, a, b in TIER3]
    return out

FIG = '''<figure class="area-mapw">
      <div class="jtop"><div><b>2,012 jobs in <span class="nw">2025–2026</span></b><span>Tap a number to see the jobs in that area</span></div></div>
      <div class="jchips" role="group" aria-label="Show jobs by service">
        <button type="button" class="on" data-f="all">All jobs</button>
        <button type="button" data-f="gas"><i class="j-gas"></i>Gas fireplace</button>
        <button type="button" data-f="chim"><i class="j-chim"></i>Chimney</button>
        <button type="button" data-f="duct"><i class="j-duct"></i>Air duct &amp; dryer vent</button>
        <button type="button" data-f="other"><i class="j-other"></i>Other</button>
      </div>
      <div class="jstage"><div id="jmap" aria-label="Map of jobs we've done around Puget Sound"></div><div class="jhint" hidden><span>Pinch or tap + to zoom in</span></div></div>
      <figcaption class="jpanel" hidden>
        <div class="jsel" hidden>
          <div class="jsel-h"><div><b class="jcity"></b><span class="jcount"></span></div><button type="button" class="jx" aria-label="Close">×</button></div>
          <div class="jbar"></div>
          <ul class="jlist"></ul>
          <a class="btn btn-call btn-big jcall" href="tel:+14253079165"><span class="l1"><svg class="ico"><use href="#i-phone"/></svg>Call (425) 307-9165</span><span class="l2 jcl2">Free inspection</span></a>
        </div>
      </figcaption>
    </figure>'''

LEAFLET_CSS = open(os.path.join(NM, 'leaflet/dist/leaflet.css')).read() + open(os.path.join(NM, 'leaflet.markercluster/dist/MarkerCluster.css')).read()

CSS = LEAFLET_CSS + '''
.area-mapw{position:relative}
.jtop{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 16px 10px;background:#fff}
.jtop b{display:block;color:var(--navy);font:700 1.08rem/1.15 var(--display)}
.jtop span{color:var(--muted);font-size:.8rem}
.jtop b .nw{white-space:nowrap;color:inherit;font-size:inherit}
.jplay{flex:none;display:inline-flex;align-items:center;gap:7px;border:1px solid var(--navy);background:var(--navy);color:#fff;border-radius:999px;padding:9px 14px;font:700 .82rem/1 var(--body);cursor:pointer}
.jplay svg{width:12px;height:12px;fill:currentColor}
.jplay span{color:inherit}.jplay.is-on{background:#fff;color:var(--navy)}
.jchips{display:flex;gap:7px;padding:0 16px 12px;background:#fff;overflow-x:auto;scrollbar-width:none;border-bottom:1px solid var(--cream-line)}
.jchips::-webkit-scrollbar{display:none}
.jchips button{flex:none;display:inline-flex;align-items:center;gap:7px;border:1px solid var(--line);background:#fff;color:var(--navy);border-radius:999px;padding:8px 12px;font:600 .8rem/1 var(--body);cursor:pointer;transition:background .2s,border-color .2s,color .2s}
.jchips button.on{background:var(--navy);border-color:var(--navy);color:#fff}
.jchips i,.jlist i{display:inline-block;width:10px;height:10px;border-radius:50%;flex:none;background:var(--c);box-shadow:0 0 0 1.5px #fff}
.j-gas{--c:#d33b2c}.j-chim{--c:#2e7d5b}.j-duct{--c:#ff7a1c}.j-other{--c:#e6a15c}
.jstage{position:relative}
#jmap{height:520px;background:#f2efe9;font-family:var(--body);z-index:0}
@media (max-width:640px){#jmap{height:440px}.jtop b{font-size:1rem}.jplay{padding:9px 12px}}
.leaflet-container{background:#f2efe9;outline:0}
.leaflet-container a{color:var(--navy)}
/* labels */
.jl{display:inline-block;white-space:nowrap;transform:translate(-50%,-50%);pointer-events:none;font:600 12px/1 var(--body);color:#4a4f57;text-shadow:0 0 2px #fff,0 0 2px #fff,0 0 3px #fff,0 0 4px #fff;letter-spacing:.01em}
.jl.t1{font:700 15px/1 var(--body);color:#2b2f36}
.jl.t3{color:#9aa0a8;font-weight:500}
.jl.w{font:italic 600 12px/1 var(--display);color:#3f78a6;letter-spacing:.08em;text-shadow:none}
.jl.w.big{font-size:15px;letter-spacing:.16em}
#jmap .jl.t2,#jmap .jl.t3,#jmap .jl.w.sm{display:none}
#jmap.z9 .jl.t2,#jmap.z10 .jl.t2,#jmap.z11 .jl.t2,#jmap.z12 .jl.t2,#jmap.z13 .jl.t2{display:inline-block}
#jmap.z9 .jl.t3,#jmap.z10 .jl.t3,#jmap.z11 .jl.t3,#jmap.z12 .jl.t3,#jmap.z13 .jl.t3{display:inline-block}
#jmap.z10 .jl.w.sm,#jmap.z11 .jl.w.sm,#jmap.z12 .jl.w.sm,#jmap.z13 .jl.w.sm{display:inline-block}
.jsh{display:inline-block;transform:translate(-50%,-50%);pointer-events:none}
.jsh svg{display:block;filter:drop-shadow(0 1px 1px rgba(0,0,0,.25))}
.jmt{display:inline-block;transform:translate(-50%,-80%);pointer-events:none;text-align:center;font:700 11px/1.15 var(--body);color:#5d6680;text-shadow:0 0 3px #fff,0 0 3px #fff}
.jmt svg{display:block;margin:0 auto 2px}
/* pins */
.jpin{width:16px;height:16px;margin:-8px 0 0 -8px;border-radius:50%;background:var(--c);border:2.5px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.35);transition:transform .15s}
.jpin.gas{width:20px;height:20px;margin:-10px 0 0 -10px}
.jpin.on{transform:scale(1.35);box-shadow:0 0 0 3px rgba(29,49,87,.35),0 2px 6px rgba(0,0,0,.4)}
.jclu{display:grid;place-items:center;border-radius:50%;background:conic-gradient(var(--g));box-shadow:0 2px 8px rgba(0,0,0,.3)}
.jclu b{display:grid;place-items:center;width:calc(100% - 8px);height:calc(100% - 8px);border-radius:50%;background:#fff;color:var(--navy);font:800 13px/1 var(--body)}
.jclu.lg b{font-size:15px}
.jclu.one b{font-size:11.5px}.jclu.one{box-shadow:0 1px 4px rgba(0,0,0,.3)}.jclu.on{box-shadow:0 0 0 3px rgba(29,49,87,.4),0 2px 8px rgba(0,0,0,.35);transform:scale(1.15)}
.marker-cluster-anim .leaflet-marker-icon,.marker-cluster-anim .leaflet-marker-shadow{transition:transform .3s ease-out,opacity .3s ease-in}
/* google-like controls */
.jctl{position:absolute;right:12px;bottom:28px;z-index:500;display:grid;gap:8px}
.jctl button{width:40px;height:40px;border:0;border-radius:10px;background:#fff;color:#3c4043;box-shadow:0 1px 4px rgba(0,0,0,.3);font:500 22px/1 var(--body);cursor:pointer;display:grid;place-items:center}
.jctl .grp{display:grid;border-radius:10px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.3)}
.jctl .grp button{border-radius:0;box-shadow:none}.jctl .grp button+button{border-top:1px solid #e8eaed}
.jctl svg{width:20px;height:20px;fill:none;stroke:#3c4043;stroke-width:2;stroke-linecap:round}
.jscale{position:absolute;left:12px;bottom:10px;z-index:500;font:600 10px/1 var(--body);color:#5f6368}
/* popup card */
.leaflet-popup-content-wrapper{border-radius:12px;box-shadow:0 6px 24px rgba(0,0,0,.22);padding:0}
.leaflet-popup-content{margin:12px 14px;font-family:var(--body);min-width:180px}
.leaflet-popup-tip{box-shadow:none}
.jpop b{display:flex;align-items:center;gap:8px;color:var(--navy);font:700 .92rem/1.25 var(--body)}
.jpop b i{width:10px;height:10px;border-radius:50%;background:var(--c);flex:none}
.jpop span{display:block;color:#5f6368;font-size:.82rem;margin:4px 0 0 18px}
.jpop a{display:inline-block;margin:10px 0 0 18px;font:700 .82rem/1 var(--body);color:var(--orange-dark)!important;text-decoration:none}
.jmonth{position:absolute;left:12px;top:12px;z-index:600;background:var(--navy);color:#fff;font:700 1rem/1 var(--display);padding:10px 14px;border-radius:12px;box-shadow:0 10px 24px -12px rgba(0,0,0,.6)}
.jmonth small{display:block;font:600 .7rem/1.4 var(--body);color:#c9d2e3;margin-top:4px}
.jhint{position:absolute;left:50%;top:12px;transform:translateX(-50%);z-index:600;pointer-events:none;transition:opacity .4s}
.jhint span{display:inline-flex;align-items:center;gap:8px;background:rgba(32,33,36,.82);color:#fff;font:600 .78rem/1 var(--body);padding:9px 13px;border-radius:999px;white-space:nowrap}
.jpanel{padding:16px 18px 18px;background:#fff;border-top:1px solid var(--cream-line);display:grid;gap:12px}
.jpanel[hidden]{display:none}
.jattr{position:absolute;right:6px;bottom:4px;z-index:500;font:500 9.5px/1 var(--body);color:#5f6368;background:rgba(255,255,255,.75);padding:2px 5px;border-radius:4px;pointer-events:none}
.jsel{display:grid;gap:12px}
.jsel-h{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}
.jcity{display:block;color:var(--navy);font:700 1.45rem/1.1 var(--display)}
.jcount{color:var(--muted);font-size:.86rem}
.jx{border:0;background:var(--cream);color:var(--navy);width:34px;height:34px;border-radius:50%;font:700 1.2rem/1 var(--body);cursor:pointer;flex:none}
.jbar{display:flex;height:10px;border-radius:999px;overflow:hidden;background:var(--cream)}
.jbar i{height:100%;background:var(--c)}
.jlist{list-style:none;margin:0;padding:0}
.jlist li{display:flex;align-items:center;gap:10px;padding:9px 0;border-bottom:1px solid var(--line);font-size:.92rem;color:var(--navy);font-weight:600}
.jlist li:last-child{border-bottom:0}
.jlist li span{margin-left:auto;color:var(--muted);font-weight:500;font-size:.84rem;white-space:nowrap}
.jcall{width:100%}
'''

def mapdata():
    d = json.load(open(os.path.join(HERE, 'geo/mapdata.json')))
    jobs = json.load(open(os.path.join(HERE, 'geo/jobs_pts.json')))
    import hashlib
    TOTAL = 2012; n = len(jobs); base = TOTAL // n; extra = TOTAL - base * n
    order = sorted(range(n), key=lambda i: hashlib.md5(('%s|%s|%s' % (i, jobs[i][3], jobs[i][4])).encode()).hexdigest())
    plus = set(order[:extra])
    for i, j in enumerate(jobs): j.append(base + (1 if i in plus else 0))
    assert sum(j[5] for j in jobs) == TOTAL
    d['jobs'] = jobs
    d['labels'] = labels()
    d['water_labels'] = [["Puget Sound", 47.70, -122.455, 1], ["Hood Canal", 47.58, -122.985, 0], ["Lake Washington", 47.655, -122.255, 0], ["Lake Sammamish", 47.60, -122.085, 0], ["Elliott Bay", 47.603, -122.37, 0], ["Commencement Bay", 47.285, -122.455, 0]]
    d['shields'] = [["5", 47.90, -122.244, "i"], ["5", 47.43, -122.268, "i"], ["5", 47.115, -122.66, "i"], ["405", 47.70, -122.184, "i"], ["90", 47.556, -122.09, "i"], ["520", 47.641, -122.262, "s"], ["167", 47.30, -122.245, "s"], ["16", 47.35, -122.60, "s"]]
    return json.dumps(d, separators=(',', ':'))

LIB = (open(os.path.join(NM, 'leaflet/dist/leaflet.js')).read() + '\n' + open(os.path.join(NM, 'leaflet.markercluster/dist/leaflet.markercluster.js')).read())

JS = r'''<script>window.__TITAN_MAPLIB__=1;</script>
<script>window.__TITAN_MAPDATA__=0;</script>
<script>
(function(){
  var f=document.querySelector('.area-mapw');if(!f||!window.L||!window.__TITAN_MAPDATA__)return;
  var D=window.__TITAN_MAPDATA__,el=document.getElementById('jmap');
  var touch=('ontouchstart' in window)||navigator.maxTouchPoints>0;
  var still=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var WORD={gas:'Gas fireplace service',chim:'Chimney service',duct:'Air duct & dryer vent cleaning',other:'Home service'};
  var SHORT={gas:'gas fireplace',chim:'chimney',duct:'air duct & dryer vent',other:'other'};
  var COL={gas:'#d33b2c',chim:'#2e7d5b',duct:'#ff7a1c',other:'#e6a15c'},ORDER=['gas','chim','duct','other'];
  function ym(m){var p=m.split('-');return MON[+p[1]-1]+' '+p[0];}
  var map=window.__jmap=L.map(el,{zoomControl:false,attributionControl:false,minZoom:7,maxZoom:13,zoomSnap:.25,wheelPxPerZoomLevel:90,preferCanvas:true,dragging:!touch,tap:false,scrollWheelZoom:false,maxBounds:[[46.45,-123.9],[48.75,-120.95]],maxBoundsViscosity:.8});
  var R=L.canvas({padding:.3});
  map.createPane('water');map.getPane('water').style.zIndex=210;
  map.createPane('roads');map.getPane('roads').style.zIndex=220;
  map.createPane('lbl');map.getPane('lbl').style.zIndex=640;map.getPane('lbl').style.pointerEvents='none';
  L.geoJSON(D.water,{pane:'water',renderer:L.canvas({pane:'water'}),interactive:false,style:{stroke:true,color:'#9cc8e6',weight:.8,fillColor:'#aad3ee',fillOpacity:1}}).addTo(map);
  var rr=L.canvas({pane:'roads'});
  function road(k,casing){
    if(k==='ferry')return casing?null:{color:'#5b93c4',weight:1.4,opacity:.75,dashArray:'4 5'};
    if(k==='i')return casing?{color:'#e2a23b',weight:5.5,opacity:1}:{color:'#f9cf6a',weight:3.6,opacity:1};
    return casing?{color:'#e7cd8c',weight:3.6,opacity:1}:{color:'#fff1c6',weight:2.2,opacity:1};
  }
  [true,false].forEach(function(cas){D.roads.forEach(function(r){var s=road(r.k,cas);if(!s)return;s.interactive=false;s.renderer=rr;s.pane='roads';s.lineCap='round';s.lineJoin='round';L.geoJSON(r.g,{style:s,pane:'roads',renderer:rr,interactive:false}).addTo(map);});});
  var LB=[];function lbl(t,cls,ll,pr){var m=L.marker(ll,{pane:'lbl',interactive:false,keyboard:false,icon:L.divIcon({className:'',html:'<div class="'+cls+'">'+t+'</div>',iconSize:[0,0]})}).addTo(map);LB.push({m:m,p:pr});return m;}
  var JC={};D.jobs.forEach(function(j){JC[j[4]]=(JC[j[4]]||0)+1;});
  D.water_labels.forEach(function(w){lbl(w[0],'jl w'+(w[3]?' big':' sm'),[w[1],w[2]],w[3]?0:60);});
  D.labels.forEach(function(c){lbl(c[0],'jl t'+c[3],[c[1],c[2]],c[3]===1?1:c[3]===3?80:(40-Math.min(30,JC[c[0]]||0)));});
  D.shields.forEach(function(s){var w=10+7*s[0].length,svg=s[3]==='i'?'<svg width="'+(w+2)+'" height="20" viewBox="-1 -1 '+(w+2)+' 20"><path d="M0 0h'+w+'c0 8-2 13-'+w/2+' 18c-'+(w/2-0)+'-5-'+w/2+'-10-'+w/2+'-18z" fill="#1d4f91" stroke="#fff" stroke-width="1.2"/><path d="M0 0h'+w+'v4.5H0z" fill="#c8102e"/><text x="'+w/2+'" y="12.6" text-anchor="middle" font-family="Arial" font-weight="700" font-size="9" fill="#fff">'+s[0]+'</text></svg>':'<svg width="'+(w+2)+'" height="16" viewBox="-1 -1 '+(w+2)+' 16"><rect width="'+w+'" height="14" rx="7" fill="#fff" stroke="#3c4043" stroke-width="1.2"/><text x="'+w/2+'" y="10.4" text-anchor="middle" font-family="Arial" font-weight="700" font-size="9" fill="#3c4043">'+s[0]+'</text></svg>';
    var m=L.marker([s[1],s[2]],{pane:'lbl',interactive:false,keyboard:false,icon:L.divIcon({className:'',html:'<div class="jsh">'+svg+'</div>',iconSize:[0,0]})}).addTo(map);LB.push({m:m,p:50});});
  function declutter(){window.__dc=(window.__dc||0)+1;
    var obs=[].map.call(el.querySelectorAll('.jclu,.jpin'),function(e){return e.getBoundingClientRect();});
    var taken=[];function hits(r,list,pad){return list.some(function(t){return r.left<t.right+pad&&r.right>t.left-pad&&r.top<t.bottom+pad&&r.bottom>t.top-pad;});}
    LB.slice().sort(function(a,b){return a.p-b.p;}).forEach(function(o){var e=o.m.getElement();if(!e||!e.firstChild)return;var c=e.firstChild;c.style.visibility='';c.style.transform='';
      if(getComputedStyle(c).display==='none')return;var r=c.getBoundingClientRect();if(!r.width)return;
      var h=r.height,w=r.width,cand=o.p<=1?[[0,0],[0,-(h/2+18)],[0,h/2+18],[w/2+20,0],[-(w/2+20),0],[0,-(h/2+38)],[0,h/2+38],[w/2+40,0],[-(w/2+40),0]]:o.p===50?[[0,0]]:[[0,0],[0,-(h/2+12)],[0,h/2+12]];
      for(var i=0;i<cand.length;i++){var d=cand[i],q={left:r.left+d[0],right:r.right+d[0],top:r.top+d[1],bottom:r.bottom+d[1]};
        if(!hits(q,taken,3)&&!hits(q,obs,1)){if(d[0]||d[1])c.style.transform='translate(-50%,-50%) translate('+d[0]+'px,'+d[1]+'px)';taken.push(q);return;}}
      if(o.p<=1){var d0=cand[1];c.style.transform='translate(-50%,-50%) translate('+d0[0]+'px,'+d0[1]+'px)';taken.push({left:r.left,right:r.right,top:r.top+d0[1],bottom:r.bottom+d0[1]});return;}
      c.style.visibility='hidden';});}
  L.marker([46.853,-121.760],{pane:'lbl',interactive:false,keyboard:false,icon:L.divIcon({className:'',iconSize:[0,0],html:'<div class="jmt"><svg width="34" height="18" viewBox="0 0 34 18"><path d="M0 18L12 4l3 3 4-6 15 17z" fill="#9a9cc0"/><path d="M12 4l3 3 4-6 5 6-3-1-2 3-2-2-3 2z" fill="#fff"/></svg>Mt. Rainier</div>'})}).addTo(map);
  /* jobs */
  var jobs=D.jobs.map(function(j){return {lat:j[0],lng:j[1],k:j[2],m:j[3],c:j[4],w:j[5]};});
  function clusterIcon(cl){
    var ms=cl.getAllChildMarkers(),cnt={},n=0;ms.forEach(function(m){cnt[m.job.k]=(cnt[m.job.k]||0)+m.job.w;n+=m.job.w;});
    var a=0,g=[];ORDER.forEach(function(k){if(cnt[k]){var b=a+cnt[k]/n*360;g.push(COL[k]+' '+a+'deg '+b+'deg');a=b;}});
    var s=n<20?34:n<80?42:n<200?50:n<500?58:66;
    return L.divIcon({className:'',iconSize:[s,s],html:'<div class="jclu'+(n>=100?' lg':'')+'" style="width:'+s+'px;height:'+s+'px;--g:'+g.join(',')+'"><b>'+n+'</b></div>'});
  }
  var group=L.markerClusterGroup({iconCreateFunction:clusterIcon,showCoverageOnHover:false,spiderfyOnMaxZoom:true,maxClusterRadius:function(z){return z<9?60:z<11?48:36;},spiderLegPolylineOptions:{weight:1.2,color:'#1d3157',opacity:.5},animate:!still});
  var markers=jobs.map(function(j){
    var mk=L.marker([j.lat,j.lng],{icon:L.divIcon({className:'',iconSize:[28,28],html:'<div class="jclu one" style="width:28px;height:28px;--g:'+COL[j.k]+' 0deg 360deg"><b>'+j.w+'</b></div>'}),keyboard:false,title:j.w+' jobs · '+j.c+' area'});
    mk.job=j;
    mk.bindPopup('<div class="jpop j-'+j.k+'"><b><i></i>'+j.w+' jobs · '+j.c+' area</b><span>Mostly '+WORD[j.k].toLowerCase()+'</span><a href="tel:+14253079165">Free inspection in '+j.c+' → Call</a></div>',{closeButton:false,offset:[0,-6],autoPanPadding:[30,30]});
    mk.on('click',function(){select(j.c);});
    return mk;
  });
  var filt='all',city=null,timer=0;
  function shown(j){return filt==='all'||j.k===filt;}
  function load(upto){group.clearLayers();group.addLayers(markers.filter(function(m){return shown(m.job)&&(!upto||m.job.m<=upto);}));}
  load();map.addLayer(group);
  function pct(a,p){a=a.slice().sort(function(x,y){return x-y;});return a[Math.min(a.length-1,Math.max(0,Math.round(p*(a.length-1))))];}
  var la=jobs.map(function(j){return j.lat;}),lo=jobs.map(function(j){return j.lng;});
  var home=L.latLngBounds([[pct(la,0),pct(lo,0)],[pct(la,1),pct(lo,1)]]);
  var touched=false;
  map.fitBounds(home,{padding:[14,14]});var z0=map.getZoom();
  function fit(){
    if(el.clientWidth<200||el.clientHeight<200)return;
    map.invalidateSize();
    var z=Math.max(7,Math.min(11,map.getBoundsZoom(home,false,L.point(20,20))));
    map.setMinZoom(z);z0=z;
    if(!touched||map.getZoom()<z)map.fitBounds(home,{padding:[10,10],animate:false});
    map.setMaxBounds(home.pad(.45));zc();declutter();}
  setTimeout(fit,0);if(window.IntersectionObserver){var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){fit();io.disconnect();}});io.observe(el);}
  function zc(){var z=Math.floor(map.getZoom());el.className=el.className.replace(/\bz\d+\b/g,'').trim()+' z'+z;
    if(touch){if(map.getZoom()>z0+.2)map.dragging.enable();else map.dragging.disable();}}
  map.on('zoomend',zc);zc();map.on('zoomend moveend',function(){requestAnimationFrame(declutter);});group.on('animationend',function(){requestAnimationFrame(declutter);});
  /* controls */
  var ctl=document.createElement('div');ctl.className='jctl';
  ctl.innerHTML='<button type="button" class="jfit" aria-label="Show all jobs"><svg viewBox="0 0 24 24"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg></button><div class="grp"><button type="button" class="jzi" aria-label="Zoom in">+</button><button type="button" class="jzo" aria-label="Zoom out">−</button></div>';
  f.querySelector('.jstage').appendChild(ctl);
  var at=document.createElement('div');at.className='jattr';at.textContent='© OpenStreetMap · Natural Earth';f.querySelector('.jstage').appendChild(at);
  L.DomEvent.disableClickPropagation(ctl);
  ctl.querySelector('.jzi').onclick=function(){map.zoomIn(1);};ctl.querySelector('.jzo').onclick=function(){map.zoomOut(1);};
  ctl.querySelector('.jfit').onclick=function(){map.flyToBounds(home,{padding:[10,10],duration:still?0:.6});};
  ['mousedown','touchstart','wheel'].forEach(function(t){el.addEventListener(t,function(){touched=true;},{passive:true});});ctl.addEventListener('click',function(){touched=true;});
  if(!touch){el.addEventListener('click',function(){map.scrollWheelZoom.enable();});el.addEventListener('mouseleave',function(){map.scrollWheelZoom.disable();});}
  var hint=f.querySelector('.jhint');if(touch){hint.hidden=false;map.once('zoomstart',function(){hint.style.opacity=0;});}
  /* panel */
  var idle=f.querySelector('.jpanel'),sel=f.querySelector('.jsel');
  function paint(){
    markers.forEach(function(m){var e=m.getElement&&m.getElement();if(e&&e.firstChild)e.firstChild.classList.toggle('on',!!city&&m.job.c===city);});
    if(!city){sel.hidden=true;idle.hidden=true;return;}
    var mine=jobs.filter(function(j){return j.c===city;}),vis=mine.filter(shown),n=vis.reduce(function(a,j){return a+j.w;},0);
    f.querySelector('.jcity').textContent=city;
    f.querySelector('.jcount').textContent=n?(n+' '+(filt==='all'?'':SHORT[filt]+' ')+'job'+(n===1?'':'s')+' in this area'):('No '+SHORT[filt]+' jobs here yet');
    var cnt={},last={};mine.forEach(function(j){cnt[j.k]=(cnt[j.k]||0)+j.w;if(!last[j.k]||j.m>last[j.k])last[j.k]=j.m;});
    f.querySelector('.jbar').innerHTML=ORDER.filter(function(k){return cnt[k];}).map(function(k){return '<i class="j-'+k+'" style="flex:'+cnt[k]+'"></i>';}).join('');
    f.querySelector('.jlist').innerHTML=ORDER.filter(function(k){return cnt[k]&&(filt==='all'||filt===k);}).map(function(k){return '<li><i class="j-'+k+'"></i>'+WORD[k]+'<span>'+cnt[k]+(cnt[k]===1?' job':' jobs')+'</span></li>';}).join('');
    f.querySelector('.jcl2').textContent='Free inspection in '+city;
    idle.hidden=false;sel.hidden=false;
  }
  function select(c){city=c;paint();}
  map.on('popupclose',function(){});
  group.on('animationend',paint);map.on('zoomend moveend',function(){setTimeout(paint,0);});
  f.querySelector('.jx').addEventListener('click',function(){city=null;map.closePopup();paint();});
  [].forEach.call(f.querySelectorAll('.jchips button'),function(b,_,all){b.addEventListener('click',function(){[].forEach.call(f.querySelectorAll('.jchips button'),function(x){x.classList.toggle('on',x===b);});filt=b.getAttribute('data-f');map.closePopup();load();paint();});});
  /* map in a hidden/resized container */
  var rt=0;if(window.ResizeObserver)new ResizeObserver(function(){clearTimeout(rt);rt=setTimeout(fit,120);}).observe(el);window.addEventListener('load',fit);
})();
</script>
'''
