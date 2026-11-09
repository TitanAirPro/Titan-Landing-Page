import json, shapely, math, hashlib, sys
from shapely.geometry import Polygon, box, shape, mapping, Point, LineString
from shapely.ops import unary_union
X0,Y0,X1,Y1=-124.4,46.2,-120.6,48.95
d=json.load(open('seas100.json')); gs=d['geometries'] if 'geometries' in d else [d]
land=[]
for g in gs:
    for p in ([g['coordinates']] if g['type']=='Polygon' else g['coordinates']):
        for ring in p[1:]:
            xs=[c[0] for c in ring]
            if max(xs)<X0 or min(xs)>X1: continue
            ys=[c[1] for c in ring]
            if max(ys)<Y0 or min(ys)>Y1: continue
            c=shapely.clip_by_rect(Polygon(ring),X0,Y0,X1,Y1)
            if not c.is_empty: land.append(shapely.make_valid(c))
LAND=unary_union(land)
SEA=box(X0,Y0,X1,Y1).difference(LAND).simplify(0.0012, preserve_topology=True)
lw=[shape(f['geometry']) for f in json.load(open('ne_10m_lakes_north_america.json'))['features'] if f['properties'].get('name')=='Lake Washington'][0]
def poly(pts): return Polygon([(lo,la) for la,lo in pts])
SAMM=poly([(47.655,-122.107),(47.64,-122.113),(47.62,-122.106),(47.60,-122.098),(47.58,-122.086),(47.562,-122.072),(47.551,-122.061),(47.556,-122.05),(47.576,-122.06),(47.60,-122.075),(47.625,-122.089),(47.646,-122.099)])
UNION=poly([(47.649,-122.336),(47.641,-122.346),(47.629,-122.342),(47.625,-122.336),(47.635,-122.326),(47.648,-122.328)])
GREEN=poly([(47.686,-122.338),(47.681,-122.345),(47.674,-122.342),(47.676,-122.334),(47.683,-122.332)])
AMER=poly([(47.14,-122.575),(47.125,-122.59),(47.108,-122.575),(47.125,-122.553)])
TAPPS=poly([(47.25,-122.18),(47.235,-122.20),(47.22,-122.17),(47.237,-122.15)])
MERCER=poly([(47.597,-122.236),(47.588,-122.219),(47.57,-122.213),(47.548,-122.216),(47.529,-122.226),(47.536,-122.241),(47.56,-122.246),(47.585,-122.249)])
LAKES=unary_union([lw.difference(MERCER),SAMM,UNION,GREEN,AMER,TAPPS]).simplify(0.0006)
WATER=unary_union([SEA,LAKES])
def rnd(geom,n=4):
    m=mapping(geom)
    def r(c):
        if isinstance(c[0],(int,float)): return [round(c[0],n),round(c[1],n)]
        return [r(x) for x in c]
    m['coordinates']=r(m['coordinates']); return m
roads=[]
for f in json.load(open('ne_10m_roads.json'))['features']:
    p=f['properties']; g=shape(f['geometry'])
    if not g.intersects(box(X0,Y0,X1,Y1)): continue
    t=p.get('type'); 
    if t not in ('Major Highway','Secondary Highway','Ferry Route'): continue
    g=shapely.clip_by_rect(g,X0,Y0,X1,Y1).simplify(0.0008)
    if g.is_empty: continue
    ref=p.get('name') or ''
    k='ferry' if t=='Ferry Route' else ('i' if ref in ('5','405','90') else 'h')
    roads.append({'k':k,'ref':ref,'g':rnd(g)})
out={'water':rnd(WATER),'roads':roads}
s=json.dumps(out,separators=(',',':'))
open('mapdata.json','w').write(s); print('mapdata bytes',len(s), 'roads',len(roads))
# jobs: jitter near zip centroid, must be on land (not water)
from shapely.prepared import prep
PW=prep(WATER.buffer(0.004))
jobs=json.load(open('../jobs_loc.json'))
sys.path.insert(0,'..'); import areamap
MON="Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
SV={"Gas Fireplace":"gas","Chimney":"chim","Air Duct / Dryer":"duct"}
res=[]; moved=0
for k,j in enumerate(jobs):
    h=hashlib.sha256(("%d|%s|%s"%(k,j['d'],j['city'])).encode()).digest()
    lat,lon=j['lat'],j['lon']
    if PW.contains(Point(lon,lat)):
        best=None
        for rr in [i*0.003 for i in range(1,40)]:
            for a in range(24):
                q=Point(lon+rr*math.cos(a/24*6.283)/0.674, lat+rr*math.sin(a/24*6.283))
                if not PW.contains(q): best=q;break
            if best: break
        lon,lat=best.x,best.y; moved+=1
    R=0.006 if j['lvl']=='zip' else 0.011
    for t in range(30):
        a=h[t%32]/255*6.283; dd=(0.25+h[(t+5)%32]/255*0.75)*R
        q=Point(lon+dd*math.cos(a)/0.674, lat+dd*math.sin(a))
        if not PW.contains(q): lon2,lat2=q.x,q.y; break
    else: lon2,lat2=lon,lat
    if not (46.85<lat2<48.3 and -123.3<lon2<-121.5): continue
    res.append([round(lat2,4),round(lon2,4),SV.get(j['s'],'other'),j['d'][:7],areamap.area_of(j['lat'],j['lon'])])
print('jobs',len(res),'centroids moved off water',moved)
bad=sum(1 for r in res if WATER.contains(Point(r[1],r[0]))); print('in water after',bad)
json.dump(res,open('jobs_pts.json','w'),separators=(',',':'))
