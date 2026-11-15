import numpy as np, soundfile as sf
a,sr=sf.read("aud/df_full.wav",dtype="float32"); hop=int(.01*sr)
rms=np.array([np.sqrt(np.mean(a[i:i+hop]**2)+1e-12) for i in range(0,len(a),hop)]); db=20*np.log10(rms)
quiet=db< -42
gaps=[];i=0
while i<len(quiet):
    if quiet[i]:
        j=i
        while j<len(quiet) and quiet[j]: j+=1
        if (j-i)*0.01>=0.10: gaps.append((i*0.01,j*0.01))
        i=j
    else: i+=1
print("gaps",[(round(s,2),round(e,2)) for s,e in gaps])
KEEP=0.06  # keep 60ms of each gap (30 each side)
segs=[];cur=0.0
gaps=[g for g in gaps if g[0]<24.0]
for s,e in gaps:
    if s<=0.01: cur=max(cur,e-0.03); continue
    segs.append((cur,s+KEEP/2)); cur=e-KEEP/2
segs.append((cur,min(len(a)/sr,24.15)))
out=[];fade=int(0.008*sr)
for s,e in segs:
    x=a[int(s*sr):int(e*sr)].copy(); w=np.ones(len(x)); w[:fade]=np.linspace(0,1,fade); w[-fade:]=np.linspace(1,0,fade); out.append(x*w)
y=np.concatenate(out); sf.write("aud/tight.wav",y,sr,subtype="FLOAT")
print("segs",[(round(s,2),round(e,2)) for s,e in segs]); print("dur",len(a)/sr,"->",len(y)/sr)
