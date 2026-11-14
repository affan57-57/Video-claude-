import numpy as np, soundfile as sf
from scipy.ndimage import maximum_filter1d, uniform_filter1d
SR=48000; TOT=41.7; N=int(TOT*SR); VOFF=0.2; P='hf/proj/assets/'
v,_=sf.read('voice.wav'); v=v if v.ndim==1 else v.mean(1)
voice=np.zeros(N); i=int(VOFF*SR); voice[i:i+len(v)]=v[:N-i]
m,_=sf.read(P+'music.wav'); mus=np.zeros((N,2)); mus[:min(N,len(m))]=m[:N]
# sidechain duck
env=np.abs(voice); env=maximum_filter1d(env,int(0.05*SR)); env=uniform_filter1d(env,int(0.12*SR))
act=np.clip(env/0.05,0,1); duck=10**((-9*act)/20)
mus*=duck[:,None]*10**(-17/20)
CUES=[(0.15,'impact',-5),(0.15,'subdrop',-8),(0.9,'whoosh_up',-12),(1.85,'pop',-10),(3.0,'swish',-14),
(4.30,'pop',-12),(4.62,'scribble',-12),(5.25,'pop',-12),(5.55,'scribble',-12),(5.80,'whoosh_long',-8),
(7.40,'tap',-8),(7.62,'scribble',-14),(8.22,'whoosh_dn',-10),(9.55,'pop',-10),(12.35,'shimmer',-10),
(12.80,'whoosh_up',-10),(14.75,'tap',-10),(15.30,'tap',-10),(16.22,'whoosh_long',-8),(17.0,'shimmer',-14),
(18.05,'riser',-8),(19.02,'impact',-4),(19.02,'shimmer',-10),(19.98,'swish',-10),(20.3,'bubbles',-10),
(21.58,'whoosh_dn',-12),(21.67,'pop',-12),(22.33,'pump',-6),(22.50,'pump',-6),(22.9,'bubbles',-8),(23.3,'pop',-10),
(24.05,'impact',-7),(24.3,'ticks',-14),(26.05,'shimmer',-10),(27.38,'whoosh_up',-8),(27.88,'whoosh_dn',-8),
(28.88,'swish',-10),(29.10,'tap',-12),(29.45,'tap',-12),(29.80,'tap',-12),(30.15,'tap',-12),
(30.62,'whoosh_long',-8),(32.78,'pop',-8),(33.38,'tap',-4),(33.40,'pop',-9),(34.02,'tap',-4),(34.10,'ding',-8),
(34.45,'impact',-6),(34.45,'whoosh_up',-10),(35.45,'impact',-10),(36.90,'pop',-10),(37.60,'ticks',-10),(38.0,'ticks',-10),
(39.03,'whoosh_up',-10),(40.32,'shimmer',-8),(40.32,'impact',-8)]
sfx=np.zeros((N,2)); cache={}
for t,n,g in CUES:
    if n not in cache: cache[n]=sf.read(P+f'sfx/{n}.wav')[0]
    x=cache[n]; x=x if x.ndim==2 else np.stack([x,x],1); i=int(t*SR); x=x[:N-i]
    sfx[i:i+len(x)]+=x*10**(g/20)
mix=np.stack([voice,voice],1)*0.707+mus+sfx*0.9
sf.write('mix_pre.wav',mix.astype(np.float32),SR,subtype='FLOAT')
import json; json.dump(CUES,open('cues.json','w'))
print('peak',np.abs(mix).max())
