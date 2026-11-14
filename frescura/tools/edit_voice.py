# Cut pauses, drop repeated tail, speed up; write map for word retiming.
import soundfile as sf, numpy as np, json, subprocess, sys
W='/home/user/work/aud/'
a,sr=sf.read(W+'voc_df.wav',dtype='float32')
h=int(0.01*sr); n=len(a)//h
e=np.array([20*np.log10(np.sqrt(np.mean(a[i*h:(i+1)*h]**2))+1e-9) for i in range(n)])
floor=np.percentile(e,8); thr=floor+10
print('floor',floor,'thr',thr)
START,END=0.30,46.08
low=e<thr; gaps=[]; i=0
while i<n:
    if low[i]:
        j=i
        while j<n and low[j]: j+=1
        s,t=i*0.01,j*0.01
        if t-s>=0.17 and s>START and t<END: gaps.append((s,t))
        i=j
    else: i+=1
KEEP=0.07
segs=[]; cur=START
for s,t in gaps:
    mid=(s+t)/2
    segs.append((cur,mid-KEEP/2+0.0)); cur=mid+KEEP/2
segs.append((cur,END))
# assemble with 8ms crossfades
fade=int(0.008*sr); out=[]
for s,t in segs:
    x=a[int(s*sr):int(t*sr)].copy()
    r=np.linspace(0,1,fade); x[:fade]*=r; x[-fade:]*=r[::-1]; out.append(x)
y=np.concatenate(out); sf.write(W+'voc_cut.wav',y,sr,subtype='FLOAT')
print('gaps removed',len(gaps),'cut length',len(y)/sr)
json.dump(segs,open(W+'segs.json','w'))
