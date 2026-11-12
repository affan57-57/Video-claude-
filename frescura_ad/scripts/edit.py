import soundfile as sf, numpy as np, json, sys
a,sr=sf.read('raw48.wav',dtype='float32')
cuts=[(6.62,6.88),(8.58,8.70),(14.56,14.74),(22.94,23.06),(34.72,34.96),(39.06,41.12),(44.08,44.42)]
end=46.62; keep=[]; p=0.0
for s,e in cuts: keep.append((p,s)); p=e
keep.append((p,end))
X=int(0.012*sr); out=np.zeros(0,np.float32); mp=[]
for s,e in keep:
    seg=a[int(s*sr):int(e*sr)].copy()
    if len(out):
        f=np.linspace(0,1,X,dtype=np.float32); ov=out[-X:]*(1-f)+seg[:X]*f
        mp.append((s,len(out)/sr-X/sr)); out=np.concatenate([out[:-X],ov,seg[X:]])
    else: mp.append((s,0.0)); out=seg
sf.write('cut.wav',out,sr,subtype='FLOAT')
json.dump(dict(keep=keep,map=mp),open('cutmap.json','w'))
print(len(out)/sr)
