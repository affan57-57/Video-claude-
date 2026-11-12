import numpy as np, soundfile as sf, sys
from scipy.ndimage import maximum_filter1d, uniform_filter1d
S=sys.argv[1]; SR=48000; V=0.15; DUR=39.8; N=int(DUR*SR)
voice,_=sf.read(f"{S}/work/voice_studio.wav",dtype='float32')
out=np.zeros((N,2),np.float32); vtrack=np.zeros(N,np.float32)
vtrack[int(V*SR):int(V*SR)+len(voice)]=voice[:N-int(V*SR)]
def load(n):
    x,_=sf.read(f"{S}/sfx/{n}.wav",dtype='float32'); return x if x.ndim==2 else np.stack([x,x],1)
def place(n,t,db):
    x=load(n)*10**(db/20); i=int((t+V)*SR); j=min(N,i+len(x)); out[i:j]+=x[:j-i]
# (name, time on voice timeline, dB)  -- SFX pushed louder per request
CUES=[("boom",-0.15,-4),("glitch",-0.1,-9),("whoosh",1.85,-10),("scrape",2.95,-12),("scrape",4.30,-11),
("hit",5.02,-5),("buzz",5.10,-13),("swoosh",6.70,-9),("whoosh",9.40,-10),("shimmer",10.7,-15),
("tick",12.28,-6),("whoosh",12.25,-12),("tick",13.80,-6),("swoosh",13.78,-12),("tick",16.76,-6),("drop",17.9,-8),
("riser",19.40,-11),("hit",22.10,-5),("shimmer",22.12,-9),("chime",22.15,-11),
("camera",23.05,-12),("shimmer",23.9,-13),("bubbles",25.8,-9),("pump",27.0,-6),("bubbles",27.6,-10),
("whoosh",29.42,-10),("pop",31.74,-9),("glitch",33.05,-12),("tick",33.5,-10),("tick",34.0,-10),("tick",34.5,-10),("tick",35.0,-10),
("hit",35.50,-6),("tap",36.62,-4),("pop",36.66,-6),("ching",37.05,-7),("whoosh",37.55,-11),("boom",37.7,-7),("shimmer",37.75,-9),("chime",38.0,-10)]
for n,t,db in CUES: place(n,t,db)
mus,_=sf.read(f"{S}/sfx/music.wav",dtype='float32'); mus=mus[:N]
# sidechain duck: -9 dB under speech, smooth
env=maximum_filter1d(np.abs(vtrack),int(0.05*SR)); act=(uniform_filter1d((env>0.03).astype(np.float32),int(0.25*SR))).clip(0,1)
g=10**((-17-9*act)/20)
mus=mus*g[:len(mus),None]
out[:len(mus)]+=mus
out+=np.stack([vtrack,vtrack],1)*0.95
sf.write(f"{S}/work/mix_pre.wav",out,SR,subtype='FLOAT')
