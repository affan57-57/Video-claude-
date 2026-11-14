import soundfile as sf, numpy as np, json
a,sr=sf.read('voice_df.wav'); h=sr//100
n=len(a)//h; r=20*np.log10(np.sqrt((a[:n*h].reshape(n,h)**2).mean(1))+1e-9)
START,END=1.52,48.45
sil=r< -42
# find silent runs
runs=[];i=0
while i<n:
    if sil[i]:
        j=i
        while j<n and sil[j]: j+=1
        runs.append((i/100,j/100)); i=j
    else: i+=1
KEEP_GAP=0.08
keep=[];cur=START
for s,e in runs:
    if e<=START or s>=END: continue
    s=max(s,START); e=min(e,END)
    if e-s>0.16:
        keep.append((cur,s+KEEP_GAP/2)); cur=e-KEEP_GAP/2
keep.append((cur,END))
keep=[(round(x,3),round(y,3)) for x,y in keep if y-x>0.02]
tot=sum(y-x for x,y in keep); print(len(keep),'segments, kept',round(tot,2),'s, removed',round(END-START-tot,2))
json.dump(keep,open('keep.json','w'))
out=[];F=int(0.006*sr)
for x,y in keep:
    seg=a[int(x*sr):int(y*sr)].copy(); w=np.linspace(0,1,F); seg[:F]*=w; seg[-F:]*=w[::-1]; out.append(seg)
sf.write('voice_cut.wav',np.concatenate(out),sr,subtype='FLOAT')
