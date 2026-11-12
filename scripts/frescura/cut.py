import soundfile as sf, numpy as np, json, sys
a,sr=sf.read('voc_df.wav'); h=int(sr*0.01)
r=np.array([np.sqrt(np.mean(a[i:i+h]**2)) for i in range(0,len(a)-h,h)]); db=20*np.log10(r+1e-9)
thr=np.percentile(db,95)-30; sil=db<thr
P=[];i=0
while i<len(sil):
    if sil[i]:
        j=i
        while j<len(sil) and sil[j]: j+=1
        P.append([i/100,j/100]); i=j
    else: i+=1
M=[]
for p in P:
    if M and p[0]-M[-1][1]<0.08: M[-1][1]=p[1]
    else: M.append(p)
START=0.0; END=37.62
cuts=[]
for s,e in M:
    if e-s>=0.14 and s>0.3 and e<END: 
        keep=0.07; m=(s+e)/2; cuts.append((s+keep/2, e-keep/2))
keeps=[];t=START
for s,e in cuts: keeps.append((t,s)); t=e
keeps.append((t,END))
# assemble with 8ms crossfade
X=int(0.008*sr); out=np.zeros(0)
for s,e in keeps:
    seg=a[int(s*sr):int(e*sr)].copy()
    if len(out)>X:
        f=np.linspace(0,1,X); out[-X:]=out[-X:]*(1-f)+seg[:X]*f; seg=seg[X:]
    out=np.concatenate([out,seg])
sf.write('voc_cut.wav',out,sr,subtype='FLOAT')
# time map
def mp(t):
    acc=0
    for s,e in keeps:
        if t<=e: return acc+max(0,t-s)
        acc+=e-s
    return acc
json.dump(dict(keeps=keeps),open('keeps.json','w'))
d=json.load(open('tx.json')); W=[]
for sg in d:
    for w in sg['words']: W.append(dict(w=w['w'].strip(),s=mp(w['s']),e=mp(w['e'])))
json.dump(W,open('words_cut.json','w'),ensure_ascii=False)
print('cuts',len(cuts),'removed %.2f'%sum(e-s for s,e in cuts),'new len %.2f'%(len(out)/sr))
