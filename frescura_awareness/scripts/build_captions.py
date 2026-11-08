"""Turn the whisper word timings of the cleaned voice into caption groups (with brand-name fixes) and inject into comp/index.html."""
import json, re, sys
OFF=float(sys.argv[1]) if len(sys.argv)>1 else 0.3
d=json.load(open('scripts/transcript_voice.json'))
W=[[w[0],w[1],w[2].strip()] for s in d for w in s['w']]
FIX=[(['Fresh','Cura','Body.'],['Frescura','Body.']),(['Balm','Share'],['Bombshell']),(['Minat','Fantasi'],['Midnight','Fantasy.']),
     (['semua'],['semula']),(['stoppage'],['stok','batch']),(['bekun','ni'],['beg','kuning']),(['misteri.'],['misteri.'])]
def fix(W):
    out=[];i=0
    while i<len(W):
        for src,dst in FIX:
            if [x[2] for x in W[i:i+len(src)]]==src:
                t0,t1=W[i][0],W[i+len(src)-1][1]; n=len(dst)
                for k,w in enumerate(dst): out.append([t0+(t1-t0)*k/n,t0+(t1-t0)*(k+1)/n,w])
                i+=len(src); break
        else: out.append(W[i]); i+=1
    return out
W=fix(W)
for w in W: w[2]=w[2].replace('-sangat','sangat')
GOLD={'spa','garam','laut','mineral','kulit','frescura','body','foaming','lembut','selesa','wangi','woman','glory','bombshell',
      'noche','midnight','fantasy','misteri','terhad','beg','kuning','sekarang','perfume','feminine','menyerlah','setiap','hari'}
groups=[];cur=[]
for w in W:
    cur.append(w); txt=w[2]
    if len(cur)>=3 or txt[-1] in '.,?' or sum(len(x[2]) for x in cur)>15:
        groups.append(cur); cur=[]
if cur: groups.append(cur)
G=[]
for g in groups:
    G.append(dict(s=round(g[0][0]+OFF,3),e=round(g[-1][1]+OFF,3),w=[dict(t=re.sub(r'[.,]$','',x[2]),s=round(x[0]+OFF,3),
             g=re.sub(r'[^a-z]','',x[2].lower()) in GOLD) for x in g]))
for i in range(len(G)-1): G[i]['e']=min(G[i+1]['s'],max(G[i]['e'],G[i]['s']+0.35))
p='comp/index.html'; h=open(p).read()
h=re.sub(r'/\*CAPS\*/.*?/\*ENDCAPS\*/','/*CAPS*/'+json.dumps(G,ensure_ascii=False)+'/*ENDCAPS*/',h,flags=re.S)
open(p,'w').write(h); print(len(G),'groups'); [print(g['s'],' '.join(x['t'] for x in g['w'])) for g in G]
