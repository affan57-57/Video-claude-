import soundfile as sf, numpy as np, json
a,sr=sf.read('df_full.wav'); h=int(0.01*sr)
e=np.array([20*np.log10(np.sqrt(np.mean(a[i:i+h]**2))+1e-9) for i in range(0,len(a)-h,h)])
low=e<-40
# end cut: first low-energy run >=50ms after 43.5s (drop repeated CTA)
i=4350
while not low[i:i+5].all(): i+=1
END=(i+2)/100; print('END',END)
# leading silence
j=0
while low[j]: j+=1
START=max(0,j/100-0.05)
# pauses
keep=[]; t=START; k=int(START*100)
runs=[]; s=None
for idx in range(k,int(END*100)):
    if low[idx] and s is None: s=idx
    if not low[idx] and s is not None:
        if idx-s>=14: runs.append((s/100,idx/100))
        s=None
runs=sorted([r for r in runs if not (35.5<r[0]<35.9)]+[(35.56,35.95)])
segs=[]; cur=START
for (r0,r1) in runs:
    segs.append((cur,r0+0.05)); cur=r1-0.04
runs.append((34.98,35.5)) if False else None
segs.append((cur,END))

fade=int(0.008*sr); out=[]
for (x,y) in segs:
    c=a[int(x*sr):int(y*sr)].copy(); c[:fade]*=np.linspace(0,1,fade); c[-fade:]*=np.linspace(1,0,fade); out.append(c)
o=np.concatenate(out); sf.write('voice_cut.wav',o,sr,subtype='FLOAT'); print('dur',len(o)/sr)
json.dump(segs,open('segs.json','w'))

print(segs)
