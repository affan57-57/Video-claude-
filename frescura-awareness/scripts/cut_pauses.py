import json, numpy as np, soundfile as sf
a,sr=sf.read("df_full.wav"); d=json.load(open("main_words.json"))
W=[w for s in d for w in s['words']]
start=W[1]['s']-0.04   # drop "Kamu,"
# refine start: first loud frame after Kamu end
h=int(.01*sr); e=20*np.log10(np.sqrt(np.mean(a[:len(a)//h*h].reshape(-1,h)**2,1))+1e-9)
sil=e<-42
i0=int(W[0]['e']*100)
while sil[i0]: i0+=1
i0-=3
iend=int(W[-1]['e']*100)+25
keep=[]; KEEP_GAP=7   # keep 70ms of each pause
i=i0
while i<iend:
    if sil[i]:
        j=i
        while j<iend and sil[j]: j+=1
        if j-i>KEEP_GAP+3: keep.append((i,i+KEEP_GAP//2)); keep.append((j-KEEP_GAP//2,j))
        else: keep.append((i,j))
        i=j
    else:
        j=i
        while j<iend and not sil[j]: j+=1
        keep.append((i,j)); i=j
# merge contiguous
sp=[]
for s,t in keep:
    if sp and sp[-1][1]==s: sp[-1][1]=t
    else: sp.append([s,t])
out=[];tmap=[];t=0; f=int(.006*sr); r=np.linspace(0,1,f)
for s,e_ in sp:
    seg=a[s*h:e_*h].copy(); seg[:f]*=r; seg[-f:]*=r[::-1]; tmap.append((s/100,e_/100,t)); out.append(seg); t+=len(seg)/sr
y=np.concatenate(out); sf.write("voice_cut.wav",y,sr,subtype="FLOAT")
def m(x):
    best=None
    for s,e_,o in tmap:
        if s<=x<=e_: return o+x-s
        if x<s: return o   # in removed gap -> snap to next span
    return t
words=[dict(text=w['w'].strip(),start=round(m(w['s']),3),end=round(m(w['e']),3)) for w in W[1:]]
json.dump(words,open("words_cut.json","w"),ensure_ascii=False)
print(len(sp),"spans; dur %.2f"%(len(y)/sr))
