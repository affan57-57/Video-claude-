import soundfile as sf, numpy as np, json
SP=1.25
a,sr=sf.read('df24.wav'); fr=a[:len(a)//480*480].reshape(-1,480); db=20*np.log10(np.sqrt((fr**2).mean(1))+1e-9)
thr=np.percentile(db,95)-26; sil=[]; s=None
for i,v in enumerate(list(db)+[0]):
    if v<thr and s is None: s=i
    if v>=thr and s is not None:
        if i-s>=12: sil.append((s/100,i/100))
        s=None
# remove: leading silence fully, others keep 0.07s
cuts=[]
for s,e in sil:
    if s==0: cuts.append((0,e-0.03)); continue
    keep=0.07; m=(s+e)/2; cuts.append((m-(e-s-keep)/2, m+(e-s-keep)/2))
cuts.append((53.9+0.45, len(a)/sr))  # trailing tail
keep=[]; t=0
for s,e in cuts:
    if s>t: keep.append((t,s))
    t=e
out=[]; F=int(0.008*sr)
for s,e in keep:
    seg=a[int(s*sr):int(e*sr)].copy(); w=np.linspace(0,1,F); seg[:F]*=w; seg[-F:]*=w[::-1]; out.append(seg)
y=np.concatenate(out); sf.write('cut.wav',y.astype(np.float32),sr,subtype='FLOAT')
def remap(t):
    r=sum(max(0,min(t,e)-s) for s,e in cuts); return (t-r)/SP
d=json.load(open('tr.json')); W=[]
for sg in d:
    for w in sg['words']: W.append({'w':w['w'].strip(),'s':round(remap(w['s']),3),'e':round(remap(w['e']),3)})
json.dump(W,open('words_edit.json','w'),ensure_ascii=False)
print('cut len %.2f -> sped %.2f'%(len(y)/sr,len(y)/sr/SP))
