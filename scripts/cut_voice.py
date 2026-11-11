# Cut false starts/repeats, tighten pauses, export edited voice.
import soundfile as sf, numpy as np, sys
a,sr=sf.read(sys.argv[1]); out=sys.argv[2]
REMOVE=[(35.30,38.70),(45.25,47.92)]           # false starts "kalau nak..x2", stumbled "jadi tekan beg bok.."
h=int(0.01*sr); n=len(a)//h
db=np.array([20*np.log10(np.sqrt((a[i*h:(i+1)*h]**2).mean())+1e-9) for i in range(n)])
sp=db>-42
for s,e in REMOVE: sp[int(s*100):int(e*100)]=False
# close tiny holes (<120ms) so words aren't chopped; drop blips <40ms
def runs(m):
    r=[];i=0
    while i<len(m):
        j=i
        while j<len(m) and m[j]==m[i]: j+=1
        r.append((m[i],i,j)); i=j
    return r
for v,i,j in runs(sp):
    if not v and j-i<12 and i>0: sp[i:j]=True
for v,i,j in runs(sp):
    if v and j-i<4: sp[i:j]=False
segs=[(i,j) for v,i,j in runs(sp) if v]
PAD=3; GAP=int(0.09*sr)  # 30ms pad each side, 90ms breathing gap
fade=int(0.008*sr); pieces=[]; tmap=[]; t=0
for i,j in segs:
    s=max(0,(i-PAD)*h); e=min(len(a),(j+PAD)*h); x=a[s:e].copy()
    x[:fade]*=np.linspace(0,1,fade); x[-fade:]*=np.linspace(1,0,fade)
    tmap.append((s/sr,e/sr,t)); pieces+= [x,np.zeros(GAP)]; t+=(e-s+GAP)/sr
y=np.concatenate(pieces); sf.write(out,y.astype(np.float32),sr,subtype="FLOAT")
print("segments",len(segs),"dur",len(y)/sr)
