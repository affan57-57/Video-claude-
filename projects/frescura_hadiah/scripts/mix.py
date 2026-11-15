import numpy as np, soundfile as sf
SR=48000; DUR=30.6; N=int(DUR*SR)
def ld(p):
    a,sr=sf.read(p,dtype="float32"); assert sr==SR,(p,sr)
    return a if a.ndim==2 else np.stack([a,a],1)
out=np.zeros((N,2),np.float32)
def put(x,t,db=0.0):
    i=int(t*SR); x=x[:max(0,N-i)]; out[i:i+len(x)]+=x*10**(db/20)
v=ld("aud/voice.wav"); cut=int(10.76*SR)
vt=np.zeros((N,2),np.float32)
A=v[:cut]; B=v[cut:]
i=int(1.70*SR); vt[i:i+len(A)]+=A; i=int(15.96*SR); vt[i:i+len(B)]+=B[:N-i]
# music with ducking envelope
m=ld("aud/music.wav")[:N]; t=np.arange(N)/SR
loud=lambda a,b: (t>=a)&(t<b)
g=np.full(N,-13.0); g[loud(0,1.62)]=-7; g[loud(12.55,15.85)]=-8; g[loud(26.65,30.6)]=-7
k=int(0.15*SR); g=np.convolve(g,np.ones(k)/k,mode="same")
g[t>28.6]+= (t[t>28.6]-28.6)/2.0*-30
m=m*(10**(g/20))[:,None]
out+=m; out+=vt*1.0
S=lambda n: ld(f"sfx/{n}.wav")
ev=[("boom",0.10,-4),("whoosh_hi",0.38,-6),("thud",0.44,-3),("shimmer",0.6,-10),("riser",0.15,-14),("whoosh_long",1.40,-8),
("whoosh",2.95,-10),("boom",4.34,-6),("thud",4.36,-4),("thud",4.80,-4),("thud",5.18,-3),("whoosh",5.36,-9),
("tick",6.18,-6),("tick",6.80,-6),("tick",7.42,-6),("ding",7.60,-12),
("riser",6.6,-16),("boom",8.02,-4),("shutter",8.12,-6),("shimmer",8.70,-9),
("whoosh",9.62,-8),("tap",10.05,-10),("tap",10.20,-10),("tap",10.35,-10),("whoosh",11.22,-8),("shimmer",11.40,-11),
("whoosh_long",12.36,-7),("tap",12.80,-8),("tap",13.0,-8),("tap",13.2,-8),("tap",13.4,-8),("bubbles",12.9,-8),("whoosh_hi",14.42,-8),("bubbles",14.5,-9),
("riser",14.4,-12),("boom",15.94,-6),("whoosh",15.92,-9),("tick",16.6,-12),("tick",17.1,-12),("tick",17.6,-12),("tick",18.1,-12),
("whoosh",18.52,-10),("heartbeat",18.7,-4),("heartbeat",19.6,-6),("whoosh",19.76,-11),("shimmer",19.85,-12),
("whoosh",20.82,-9),("thud",21.0,-5),
("boom",22.44,-5),("whoosh_long",22.36,-9),("tap",23.0,-4),("tap",23.9,-7),("ding",23.62,-9),("tap",24.05,-6),
("tick",24.6,-10),("tick",24.85,-10),("tick",25.1,-10),("thud",25.25,-4),("heartbeat",25.4,-5),
("swell",24.4,-10),("boom",26.53,-3),("shimmer",26.65,-8),("whoosh_long",26.5,-9),("shimmer",28.0,-11),("ding",27.3,-14)]
for n,tt,db in ev: put(S(n),tt,db)
sf.write("aud/premix.wav",out,SR,subtype="FLOAT")
