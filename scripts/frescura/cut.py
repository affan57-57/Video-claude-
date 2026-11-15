import json, numpy as np, soundfile as sf
W=json.load(open('words.json')); a,sr=sf.read('voc_df.wav',dtype='float32')
TEMPO=1.06; PAD=0.06
# keep intervals
keep=[]; s=max(0,W[0]['s']-0.05)
for i in range(len(W)-1):
    g=W[i+1]['s']-W[i]['e']
    if g>0.14: keep.append((s,W[i]['e']+PAD)); s=W[i+1]['s']-PAD
keep.append((s,W[-1]['e']+0.25))
fade=int(0.012*sr); out=[]; tmap=[]; t=0
for (x,y) in keep:
    seg=a[int(x*sr):int(y*sr)].copy(); seg[:fade]*=np.linspace(0,1,fade); seg[-fade:]*=np.linspace(1,0,fade)
    tmap.append((x,y,t)); out.append(seg); t+=len(seg)/sr
sf.write('voc_cut.wav',np.concatenate(out),sr,subtype='FLOAT')
def m(tt):
    for x,y,o in tmap:
        if tt<=y+1e-6: return (o+max(0,tt-x))/TEMPO
    return t/TEMPO
nw=[dict(w=w['w'],s=round(m(w['s']),3),e=round(m(w['e']),3)) for w in W]
json.dump(nw,open('words_new.json','w'),ensure_ascii=False)
print('cut len',t,'final',t/TEMPO, keep)
