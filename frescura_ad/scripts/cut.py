import soundfile as sf, numpy as np, json
a,sr=sf.read('work/voc_df.wav'); h=int(sr*0.01)
r=np.array([20*np.log10(np.sqrt(np.mean(a[i:i+h]**2))+1e-9) for i in range(0,len(a)-h,h)])
q=r<-38; runs=[]; i=0
while i<len(q):
    if q[i]:
        j=i
        while j<len(q) and q[j]: j+=1
        if (j-i)>=18 and i>0: runs.append((i*0.01,j*0.01))
        i=j
    else: i+=1
# also trim leading silence and tail
keep_pause=0.09
segs=[]; cur=0.28
for s,e in runs:
    if s<0.3: continue
    d=e-s; cut_s=s+keep_pause/2; cut_e=e-keep_pause/2
    segs.append((cur,cut_s)); cur=cut_e
segs.append((cur,48.85))
print(runs); print(segs)
segs=[(s,e) for s,e in segs if e>s]
X=int(0.006*sr); out=a[int(segs[0][0]*sr):int(segs[0][1]*sr)].copy()
for s,e in segs[1:]:
    p=a[int(s*sr)-X:int(e*sr)].copy(); f=np.linspace(0,1,X)
    out[-X:]=out[-X:]*(1-f)+p[:X]*f; out=np.concatenate([out,p[X:]])
# 4ms crossfade-ish: apply tiny fades at joints
sf.write('work/voc_cut.wav',out,sr,subtype='FLOAT')
json.dump(segs,open('work/segs.json','w'))
print('dur',len(out)/sr)
