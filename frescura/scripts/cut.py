import numpy as np, soundfile as sf, json
x,sr=sf.read('aud/df.wav',dtype='float32'); x=x[:int(46.98*sr)]
hop=int(0.01*sr); n=len(x)//hop
rms=np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2)+1e-12) for i in range(n)])
db=20*np.log10(rms); thr=-41
sil=db<thr
# silent runs
runs=[];i=0
while i<n:
    if sil[i]:
        j=i
        while j<n and sil[j]: j+=1
        runs.append((i,j)); i=j
    else: i+=1
KEEP=0.10  # keep 90ms of silence max (split as 45ms each side)
cuts=[]
for a,b in runs:
    d=(b-a)*0.01
    if a==0: cuts.append((0,max(0,b*0.01-0.03)))
    elif d>KEEP+0.04: cuts.append((a*0.01+KEEP/2, b*0.01-KEEP/2))
print('cuts',[(round(a,2),round(b,2)) for a,b in cuts])
keep=[];t=0
for a,b in cuts:
    if a>t: keep.append((t,a))
    t=b
keep.append((t,len(x)/sr))
fade=int(0.008*sr); out=[]
for a,b in keep:
    s=x[int(a*sr):int(b*sr)].copy()
    if len(s)>2*fade:
        s[:fade]*=np.linspace(0,1,fade); s[-fade:]*=np.linspace(1,0,fade)
    out.append(s)
y=np.concatenate(out); sf.write('aud/cut.wav',y,sr,subtype='FLOAT')
json.dump(keep,open('keep.json','w'))
print('dur',len(y)/sr, 'removed',len(x)/sr-len(y)/sr)
