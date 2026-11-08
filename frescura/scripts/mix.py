import numpy as np, soundfile as sf
from scipy.ndimage import maximum_filter1d, uniform_filter1d
SR=48000; TOTAL=45.0; N=int(TOTAL*SR)
v,sr=sf.read('a/voice_final.wav'); assert sr==SR
if v.ndim>1: v=v.mean(1)
SPLIT=23.46; GAP=1.40
out_v=np.zeros(N)
a=v[:int(SPLIT*SR)]; b=v[int(SPLIT*SR):]
out_v[:len(a)]=a; o=int((SPLIT+GAP)*SR); out_v[o:o+len(b)]=b[:N-o]
voice=np.stack([out_v,out_v],1)
def load(n):
    x,_=sf.read(f'sfx/{n}.wav'); return x if x.ndim==2 else np.stack([x,x],1)
sfx=np.zeros((N,2))
CUES=[(0.00,'impact',-3),(0.00,'subdrop',-6),(0.62,'pop',-8),(1.38,'whoosh',-9),(2.16,'shimmer',-15),
(2.94,'whoosh',-9),(5.16,'swoosh_down',-8),(6.36,'shimmer',-11),(6.40,'glass',-13),(7.16,'whoosh_fast',-8),
(7.95,'pump',-9),(9.26,'tick',-9),(10.34,'whoosh',-9),(10.44,'shimmer',-12),(12.26,'tick',-9),
(13.56,'swipe',-8),(14.30,'pop',-8),(15.44,'pop',-8),(15.78,'glass',-12),(16.36,'whoosh_fast',-8),
(17.10,'pop',-9),(17.24,'pop',-10),(17.38,'pop',-9),(17.52,'pop',-10),(18.44,'tick',-10),
(20.94,'whoosh_fast',-9),(21.10,'pump',-9),(21.98,'swipe',-10),(22.04,'shimmer',-14),
(23.40,'foam',-7),(23.50,'pump',-10),(24.10,'foam',-9),(24.80,'whoosh',-9),(25.72,'pop',-8),
(26.98,'toggle',-7),(28.10,'toggle',-7),(28.56,'impact',-9),(28.56,'subdrop',-9),(29.10,'clock',-12),
(31.80,'tick',-9),(33.36,'whoosh',-9),(33.46,'swipe',-11),(34.62,'pop',-7),(35.52,'kaching',-8),
(36.28,'tick',-9),(36.30,'shimmer',-14),(37.44,'tick',-9),(38.86,'whoosh',-9),(38.92,'glass',-9),(38.92,'shimmer',-11),(39.0,'subdrop',-12)]
for t,n,db in CUES:
    x=load(n)*10**(db/20); i=int(t*SR); e=min(N,i+len(x)); sfx[i:e]+=x[:e-i]
m,_=sf.read('sfx/music.wav'); m=m[:N]
if len(m)<N: m=np.vstack([m,np.zeros((N-len(m),2))])
# sidechain duck from voice envelope
env=np.abs(out_v); env=maximum_filter1d(env,int(0.03*SR)); env=uniform_filter1d(env,int(0.12*SR))
act=np.clip(env/0.05,0,1)
duck=10**((-9*act)/20)
duck=uniform_filter1d(duck,int(0.15*SR))
music=m*duck[:,None]*10**(-14/20)
# music fades: gentle in, end swell then fade
t=np.arange(N)/SR
music*=np.clip(t/0.25,0,1)[:,None]
music*=np.where(t>43.2, np.clip((TOTAL-t)/1.8,0,1),1)[:,None]
mix=voice+sfx+music
sf.write('a/mix_pre.wav',mix.astype(np.float32),SR,subtype='FLOAT')
sf.write('a/stem_voice.wav',voice.astype(np.float32),SR,subtype='FLOAT')
print('ok', mix.shape[0]/SR)
