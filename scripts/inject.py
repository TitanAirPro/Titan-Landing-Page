import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mapui2
h = open(sys.argv[1]).read()
a = 'window.__TITAN_MAPLIB__=1;'; b = 'window.__TITAN_MAPDATA__=0;'
assert h.count(a) == 1 and h.count(b) == 1
h = h.replace(a, mapui2.LIB).replace(b, 'window.__TITAN_MAPDATA__=' + mapui2.mapdata() + ';')
open(sys.argv[2], 'w').write(h)
