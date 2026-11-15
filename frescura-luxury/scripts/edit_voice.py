import soundfile as sf, numpy as np, json, sys
W=sys.argv[1]; a,sr=sf.read(W+'/df.wav')
h=sr//100
e=np.array([20*np.log10(np.sqrt(np.mean(a[i:i+h]**2))+1e-9) for i in range(0,len(a)-h,h)])
# gaps (low energy >=0.13s) -> shrink to 0.07
gaps=[];lo=e<-38;i=0
while i<len(lo):
    if lo[i]:
        j=i
        while j<len(lo) and lo[j]: j+=1
        if j-i>=13: gaps.append((i/100+0.035,j/100-0.035))
        i=j
    else: i+=1
cuts=[g for g in gaps if g[0]>0.6 and g[1]<38.7]
cuts+= [(17.73,17.97),(23.68,24.00)]   # filler "So"
cuts=sorted(cuts); merged=[]
for c in cuts:
    if merged and c[0]<=merged[-1][1]: merged[-1]=(merged[-1][0],max(merged[-1][1],c[1]))
    else: merged.append(c)
START,END=0.52,38.72
keeps=[];t=START
for c0,c1 in merged:
    keeps.append((t,c0)); t=c1
keeps.append((t,END))
X=int(0.012*sr); out=np.zeros(0)
fade=np.linspace(0,1,X)
for k0,k1 in keeps:
    seg=a[int(k0*sr):int(k1*sr)].copy()
    if len(out)>=X:
        out[-X:]=out[-X:]*(1-fade)+seg[:X]*fade; out=np.concatenate([out,seg[X:]])
    else: out=np.concatenate([out,seg])
sf.write(W+'/voice_cut.wav',out,sr,subtype='FLOAT')
json.dump(dict(keeps=keeps,xfade=X/sr),open(W+'/keeps.json','w'))
print(len(keeps),'segments; cut len %.2fs'%(len(out)/sr)); print(merged)
