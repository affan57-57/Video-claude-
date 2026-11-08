# Collapse awkward pauses (>0.22s -> 0.13s), keep breaths natural, write time-map for captions.
import numpy as np, soundfile as sf, json
x,sr=sf.read('a/voc_df.wav'); hop=int(0.01*sr)
db=20*np.log10(np.array([np.sqrt(np.mean(x[i:i+hop]**2)+1e-12) for i in range(0,len(x)-hop,hop)]))
thr=np.percentile(db,95)-34; sp=db>thr
# runs of silence
R=[];s=None
for i,v in enumerate(sp):
    if v and s is None: s=i
    if not v and s is not None: R.append([s,i]); s=None
if s is not None: R.append([s,len(sp)])
R=[r for r in R if r[1]-r[0]>=5]          # drop clicks/breath blips < 50ms
M=[R[0]]
for r in R[1:]:
    if r[0]-M[-1][1]<6: M[-1][1]=r[1]
    else: M.append(r)
sil=[(0,M[0][0]/100)]+[(M[i][1]/100,M[i+1][0]/100) for i in range(len(M)-1)]+[(M[-1][1]/100,len(sp)/100)]
cuts=[]  # (start,end) to remove
for a,b in sil:
    if a<0.01:  # leading silence: trim to 0.05
        if b>0.08: cuts.append((0,b-0.05)); continue
    if b>=len(x)/sr-0.02: cuts.append((a+0.25,len(x)/sr)); continue
    if b-a>0.20:
        cuts.append((a+0.06, b-0.06))
cuts=[(round(a,3),round(b,3)) for a,b in cuts if b-a>0.02]
print('cuts',cuts, 'removed', round(sum(b-a for a,b in cuts),2))
segs=[];t=0
for a,b in cuts: segs.append((t,a)); t=b
segs.append((t,len(x)/sr)); segs=[s for s in segs if s[1]-s[0]>0.01]
F=int(0.008*sr); out=[]
for a,b in segs:
    y=x[int(a*sr):int(b*sr)].copy(); y[:F]*=np.linspace(0,1,F); y[-F:]*=np.linspace(1,0,F); out.append(y)
y=np.concatenate(out); sf.write('a/voc_tight.wav',y.astype(np.float32),sr,subtype='FLOAT')
json.dump(segs,open('a/segs.json','w')); print('new dur',round(len(y)/sr,2))
