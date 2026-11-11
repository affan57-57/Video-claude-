import json, numpy as np, soundfile as sf, sys
a,sr=sf.read(sys.argv[1]); h=int(.01*sr)
e=20*np.log10(np.sqrt(np.mean(a[:len(a)//h*h].reshape(-1,h)**2,1))+1e-9)
sil=e<-45
START=0.86; END=41.45
i0=int(START*100); iend=int(END*100)
MINP, KEEP = 30, 20   # only pauses >=300ms are shortened, to 200ms
keep=[]; i=i0
while i<iend:
    j=i
    if sil[i]:
        while j<iend and sil[j]: j+=1
        if j-i>=MINP: keep += [(i,i+KEEP//2),(j-KEEP//2,j)]
        else: keep.append((i,j))
    else:
        while j<iend and not sil[j]: j+=1
        keep.append((i,j))
    i=j
sp=[]
for s,t in keep:
    if sp and sp[-1][1]==s: sp[-1][1]=t
    else: sp.append([s,t])
f=int(.03*sr); out=[]
for k,(s,t) in enumerate(sp):
    seg=a[s*h:t*h].copy()
    if k>0: seg[:f]*=np.linspace(0,1,f)
    if k<len(sp)-1: seg[-f:]*=np.linspace(1,0,f)
    out.append(seg)
y=np.concatenate(out); sf.write(sys.argv[2],y,sr,subtype="FLOAT")
print(len(sp),"spans; removed %.2fs; dur %.2f"%((iend-i0)/100-len(y)/sr, len(y)/sr))
