import sys,re,base64,os
src,out=sys.argv[1],sys.argv[2]
d=os.path.dirname(src); h=open(src).read()
def emb(p):
    ext=p.rsplit('.',1)[1]; mt={'jpg':'image/jpeg','png':'image/png','mp4':'video/mp4'}[ext]
    return 'data:%s;base64,'%mt+base64.b64encode(open(os.path.join(d,p),'rb').read()).decode()
# leave JSON-LD and preload untouched (invisible; served from published img/ files)
skip=re.compile(r'<script type="application/ld\+json">.*?</script>|<link rel="preload"[^>]*>',re.S)
parts=[];last=0
for m in skip.finditer(h):
    parts.append(re.sub(r'img/[A-Za-z0-9_-]+\.(?:jpg|png|mp4)',lambda x:emb(x.group(0)),h[last:m.start()])); parts.append(m.group(0)); last=m.end()
parts.append(re.sub(r'img/[A-Za-z0-9_-]+\.(?:jpg|png|mp4)',lambda x:emb(x.group(0)),h[last:]))
open(out,'w').write(''.join(parts))
