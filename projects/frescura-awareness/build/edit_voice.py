# Cut repeated CTA + awkward phrase, compress pauses, crossfade joins. Writes edited voice + EDL json.
import soundfile as sf, numpy as np, json, sys
a,sr=sf.read(sys.argv[1]); out=sys.argv[2]
KEEP=[(0.0,29.46),(32.60,37.95),(40.26,43.70)]
MAXGAP=0.12; FR=0.01
def rms(x): return 20*np.log10(np.sqrt((x**2).mean())+1e-9)
pieces=[]; edl=[]
for k0,k1 in KEEP:
    # find low-energy runs inside, shrink them
    t=k0; cur=k0
    n=int((k1-k0)/FR); lv=np.array([rms(a[int((k0+i*FR)*sr):int((k0+(i+1)*FR)*sr)]) for i in range(n)])
    q=lv<-46; i=0; segs=[]
    while i<n:
        if q[i]:
            j=i
            while j<n and q[j]: j+=1
            g0,g1=k0+i*FR,k0+j*FR
            if g1-g0>MAXGAP+0.04 and i>0 and j<n:
                cut0=g0+MAXGAP/2; cut1=g1-MAXGAP/2
                segs.append((cur,cut0)); cur=cut1
            i=j
        else: i+=1
    segs.append((cur,k1)); edl+=segs
X=int(0.008*sr); y=np.zeros(0)
for s0,s1 in edl:
    p=a[int(s0*sr):int(s1*sr)].copy()
    if len(y)>X:
        f=np.linspace(0,1,X); y[-X:]=y[-X:]*(1-f)+p[:X]*f; p=p[X:]
    y=np.concatenate([y,p])
sf.write(out,y.astype(np.float32),sr,subtype='FLOAT')
json.dump(edl,open(out+'.edl.json','w'))
print(len(edl),'segments; out dur',len(y)/sr)
