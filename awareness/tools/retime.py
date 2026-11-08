import json,re,sys,glob,os
R=json.load(open(sys.argv[1])); P=sys.argv[2]; TOTAL=float(sys.argv[3])
segs=R['segs']; F=R['factor']
def M(t):
    acc=0.0
    for s0,s1 in segs:
        if t<s0: return acc/F
        if t<=s1: return (acc+t-s0)/F
        acc+=s1-s0
    return (acc+(t-segs[-1][1]))/F
r2=lambda x: f"{x:.2f}".rstrip('0').rstrip('.') if '.' in f"{x:.2f}" else f"{x:.2f}"
peak={'impact-bass-1':0.073,'impact-bass-2':1.986,'whoosh':0.162,'whoosh-short':0.162,'sparkle':0.027,'pop':0.12,'click':0.073,'ping':0.324}
# ---- root
p=os.path.join(P,'index.html'); s=open(p).read()
hosts={}
def root_el(m):
    tag=m.group(0)
    st=float(re.search(r'data-start="([\d.]+)"',tag).group(1)); du=float(re.search(r'data-duration="([\d.]+)"',tag).group(1))
    idm=re.search(r'id="([^"]+)"',tag).group(1)
    if idm=='root': ns,nd=0,TOTAL
    elif idm=='music': ns,nd=0,TOTAL
    elif idm=='voice': ns,nd=0,34.2
    elif idm.startswith('sfx-'):
        f=re.search(r'sfx/([\w-]+)\.mp3',tag).group(1); pk=peak.get(f,0.1)
        ns=max(0,M(st+pk)-pk); nd=du
    else:
        ns=M(st); ne=M(st+du); nd=ne-ns
        if idm=='s11': nd=TOTAL-ns
        hosts[idm]=(st,ns)
    tag=re.sub(r'data-start="[\d.]+"',f'data-start="{r2(ns)}"',tag); tag=re.sub(r'data-duration="[\d.]+"',f'data-duration="{r2(nd)}"',tag)
    return tag
s=re.sub(r'<(?:div|audio)[^>]*data-start="[\d.]+"[^>]*>',root_el,s)
open(p,'w').write(s)
# ---- scenes
def fix_scene(fp,A,An):
    s=open(fp).read()
    L=lambda t: M(A+t)-An
    def el(m):
        tag=m.group(0); st=float(re.search(r'data-start="([\d.]+)"',tag).group(1)); du=float(re.search(r'data-duration="([\d.]+)"',tag).group(1))
        ns=L(st); ne=L(st+du)
        tag=re.sub(r'data-start="[\d.]+"',f'data-start="{r2(ns)}"',tag); tag=re.sub(r'data-duration="[\d.]+"',f'data-duration="{r2(ne-ns)}"',tag); return tag
    s=re.sub(r'<(?:video|div|img|audio)[^>]*data-start="[\d.]+"[^>]*>',el,s)
    def pos(m): return m.group(1)+r2(max(0,L(float(m.group(2)))))+m.group(3)
    s=re.sub(r'(\n\s*tl\.(?:to|fromTo|from|set)\(.*,\s*)([\d.]+)(\);)',pos,s)
    open(fp,'w').write(s)
for h,(A,An) in hosts.items():
    fp=os.path.join(P,'compositions',('captions' if h=='captions' else h)+'.html'); fix_scene(fp,A,An)
print({h:(round(a,2),round(b,2)) for h,(a,b) in hosts.items()})
print('M(37.92)=',round(M(37.92),2),'M(22.54)=',round(M(22.54),2))
