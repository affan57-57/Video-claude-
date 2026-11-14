import numpy as np, soundfile as sf, json, sys
S=sys.argv[1]; a,sr=sf.read(f"{S}/voice_df.wav",dtype="float32")
K=[(0.22,1.22),(1.46,6.50),(6.72,10.18),(10.26,17.10),(17.36,24.36),(24.40,25.32),(25.48,34.40),(36.56,39.72),(39.94,42.50),(42.64,50.16)]
win=int(0.02*sr)
def rms(t): i=int(t*sr); return np.sqrt(np.mean(a[max(0,i-win//2):i+win//2]**2)+1e-12)
def snap(t):
    c=np.arange(t-0.08,t+0.081,0.005); return float(c[np.argmin([rms(x) for x in c])])
K=[(snap(s),snap(e)) for s,e in K]
fd=int(0.012*sr); parts=[]; amap=[]; cum=0
for s,e in K:
    x=a[int(s*sr):int(e*sr)].copy(); x[:fd]*=np.linspace(0,1,fd); x[-fd:]*=np.linspace(1,0,fd)
    parts.append(x); parts.append(np.zeros(int(0.07*sr),np.float32))
    amap.append((s,e,cum)); cum+=len(x)/sr+0.07
y=np.concatenate(parts); sf.write(f"{S}/voice_cut.wav",y,sr,subtype="FLOAT")
json.dump(amap,open(f"{S}/cutmap.json","w")); print("len",len(y)/sr, "->", len(y)/sr/1.2)
for k in K: print("%.3f-%.3f  edge rms %.4f %.4f"%(k[0],k[1],rms(k[0]),rms(k[1])))
