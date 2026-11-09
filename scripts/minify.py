import re, sys
h = open(sys.argv[1]).read()
h = re.sub(r'<!--.*?-->', '', h, flags=re.S)                 # HTML comments
def css(m):
    c = re.sub(r'/\*.*?\*/', '', m.group(2), flags=re.S)
    c = re.sub(r'\s*\n\s*', '', c); c = re.sub(r'\s*([{};,>])\s*', r'\1', c); c = c.replace(';}', '}')
    return m.group(1) + c + m.group(3)
h = re.sub(r'(<style[^>]*>)(.*?)(</style>)', css, h, flags=re.S)
def js(m):
    if 'ld+json' in m.group(1): return m.group(0)
    c = re.sub(r'/\*.*?\*/', '', m.group(2), flags=re.S)
    c = re.sub(r'\n\s*', '\n', c).strip()
    return m.group(1) + c + m.group(3)
h = re.sub(r'(<script[^>]*>)(.*?)(</script>)', js, h, flags=re.S)
h = re.sub(r'\n[ \t]+', '\n', h); h = re.sub(r'\n{2,}', '\n', h)
open(sys.argv[2], 'w').write(h)
