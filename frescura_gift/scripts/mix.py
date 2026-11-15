import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
SR=48000; D=30.8; N=int(D*SR); out=np.zeros((N,2))
def ld(p):
    a,sr=sf.read(p,dtype='float64'); assert sr==SR,(p,sr)
    return a if a.ndim==2 else np.stack([a,a],1)
def put(a,t,db):
    i=int(t*SR); a=a[:max(0,N-i)]; out[i:i+len(a)]+=a*10**(db/20)
v=ld('work/voice.wav'); vt=np.zeros((N,2)); i=int(.5*SR); vt[i:i+len(v)]=v[:N-i]
cues=[('boom',.02,-2),('whoosh',.9,-10),('shimmer',1.3,-15),('whoosh_r',3.0,-11),('pop',3.2,-10),('shimmer',3.35,-14),
('whoosh',4.32,-8),('tick',4.62,-12),('scratch',5.36,-8),('pop',5.55,-9),('whoosh',6.42,-8),('boom',6.48,-11),('tick',6.7,-13),
('whoosh',8.52,-9),('tick',8.62,-11),('tick',9.24,-11),('heart',9.85,-6),('whoosh',11.02,-8),('foam',11.25,-6),('pop',12.05,-9),
('tick',12.5,-11),('tick',12.75,-11),('tick',13.0,-11),('whoosh',13.48,-8),('shimmer',13.95,-12),('shimmer',14.85,-12),
('whoosh',15.88,-8),('boom',15.92,-9),('pop',16.3,-10),('riser',16.5,-18),('chime',17.65,-9),('shimmer',17.7,-10),
('whoosh',18.1,-8),('foam',18.2,-9),('pop',19.0,-9),('whoosh',19.9,-8),('whoosh_r',20.05,-12),('chime',20.75,-10),
('whoosh',21.75,-8),('boom',21.8,-9),('pop',22.6,-9),('tick',23.2,-10),('clock',23.4,-9),('pop',24.2,-8),('tap',24.72,-5),
('kaching',25.1,-6),('boom',26.1,-3),('shimmer',26.4,-9),('chime',27.3,-10),('pop',27.9,-11)]
sfx=np.zeros((N,2))
for n,t,db in cues:
    a=ld(f'sfx/{n}.wav'); i=int(t*SR); a=a[:max(0,N-i)]; sfx[i:i+len(a)]+=a*10**(db/20)
m=ld('sfx/music.wav')[:N]; m=np.pad(m,((0,N-len(m)),(0,0)))
# sidechain envelope from voice
env=np.abs(vt).max(1); win=int(.03*SR); env=np.convolve(env,np.ones(win)/win,'same')
att=np.exp(-1/(.01*SR)); rel=np.exp(-1/(.25*SR)); e=np.zeros(N); x=0
for k in range(0,N,48):
    s=env[k:k+48].max(); x = s if s>x else x*rel**48; e[k:k+48]=x
lvl=20*np.log10(e+1e-6); duck=np.clip((lvl+38)/14,0,1)*-9.0  # up to -9 dB under voice
g=10**((-17+duck)/20)
t=np.arange(N)/SR
g*= np.minimum(1,t/.25)                       # music in fast
g*= np.where(t>26.1, 10**(7/20)*np.minimum(1,(t-26.1)/.4)+ (1-np.minimum(1,(t-26.1)/.4)), 1)  # lift on end card
g*= np.clip((D-t)/1.2,0,1)                    # fade out
mix=vt*1.0 + sfx + m*g[:,None]
sf.write('work/premix.wav',mix.astype(np.float32),SR,subtype='FLOAT'); print('peak',np.abs(mix).max())
