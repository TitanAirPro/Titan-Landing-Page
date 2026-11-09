def _mirror(d):
    import re
    out = []; isx = True
    for t in re.findall(r'[MLCQZ]|-?\d+(?:\.\d+)?', d):
        if t in 'MLCQZ': out.append(t); isx = True; continue
        out.append(('%.2f' % (100 - float(t))) if isx else t); isx = not isx
    return " ".join(out)
def bird():
    # slender crescent wing: smooth leading edge up to the wrist, long pointed tip, thin trailing edge
    L = ("M48.4 15.6 C44 12.4 38.6 8.4 31.6 6.6 C24.6 4.8 15.6 6.4 1.2 12.8 "
         "C13.4 10.4 21.6 10 28.4 11 C35 12 41.6 14.6 48.4 18.2 Z")
    R = _mirror(L)
    body = ("M50 13.4 C51 13.4 51.6 14.4 51.6 15.8 C51.6 17.8 51.1 20 50.7 22 L52 24.4 "
            "C51 24.8 49 24.8 48 24.4 L49.3 22 C48.9 20 48.4 17.8 48.4 15.8 C48.4 14.4 49 13.4 50 13.4 Z")
    return ('<svg viewBox="0 0 100 30" aria-hidden="true">'
            '<g class="wing"><path d="%s"/><path d="%s"/></g><path d="%s"/></svg>') % (L, R, body)
if __name__ == "__main__":
    import sys
    b = bird()
    flap = b.replace('<g class="wing">', '<g class="wing" style="transform-box:fill-box;transform-origin:50% 92%;transform:scaleY(-.55)">')
    cell = lambda x, w, o=1: '<div style="display:inline-block;width:%dpx;padding:18px;fill:#1d3157;opacity:%s">%s</div>' % (w, o, x)
    open(sys.argv[1], 'w').write('<html><body style="margin:0;background:linear-gradient(#6e6a84,#efc0a2)">' + cell(b, 420) + cell(flap, 420) + '<br>' + cell(b, 80) + cell(flap, 80) + cell(b, 46, .6) + '</body></html>')
