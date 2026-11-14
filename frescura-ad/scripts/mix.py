import numpy as np, soundfile as sf, json, sys
S=sys.argv[1]; SR=48000; L=40.0; N=int(L*SR)
v,_=sf.read(f"{S}/voice_studio.wav",dtype="float32"); v=v if v.ndim==1 else v.mean(1)
voice=np.zeros(N); voice[:min(N,len(v))]=v[:N]
mus,_=sf.read(f"{S}/sfx/music.wav",dtype="float32"); mus=mus[:N]; mus=np.pad(mus,((0,N-len(mus)),(0,0)))
# duck envelope from voice
w=int(0.03*SR); e=np.sqrt(np.convolve(voice**2,np.ones(w)/w,'same')); act=(e>0.02).astype(float)
k=int(0.25*SR); act=np.convolve(act,np.ones(k)/k,'same').clip(0,1)
g=10**((-21+(-6)*act)/20)   # music -21dB, -27dB under speech
mix=np.stack([voice,voice],1)*1.0+mus*g[:,None]
for name,at,db in json.load(open(f"{S}/cues.json")):
    x,_=sf.read(f"{S}/sfx/{name}.wav",dtype="float32"); i=int(at*SR); e=min(N,i+len(x)); mix[i:e]+=x[:e-i]*10**(db/20)
fo=int(0.6*SR); mix[-fo:]*=np.linspace(1,0,fo)[:,None]
sf.write(f"{S}/mix_pre.wav",mix.astype(np.float32),SR,subtype="FLOAT")
