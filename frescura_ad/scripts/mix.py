import numpy as np, soundfile as sf
from scipy.signal import fftconvolve
SR=48000; D='proj/assets/sfx/'; DUR=40.0; N=int(DUR*SR)
def load(f):
    a,sr=sf.read(f,dtype='float32'); assert sr==SR, (f,sr)
    return a if a.ndim==2 else np.stack([a,a],1)
voice=load('proj/assets/voice.wav'); vo=np.zeros((N,2)); i=int(0.10*SR); vo[i:i+len(voice)]=voice[:N-i]
music=load(D+'music.wav')[:N]; mu=np.zeros((N,2)); mu[:len(music)]=music
# ducking envelope from voice
env=np.abs(vo).max(1); k=int(0.05*SR); env=np.convolve(env,np.ones(k)/k,'same')
duck=np.where(env>0.02,1.0,0.0); r=int(0.25*SR); duck=np.convolve(duck,np.ones(r)/r,'same')
mg=10**(-17/20)*(1-duck*0.55)  # music -17 dB, ducks a further ~7 dB under speech
mu*=mg[:,None]
S=[('boom',0.0,-6),('shimmer',0.05,-12),('riser',1.56,-12),('boom',2.76,-5),('whoosh',2.55,-9),('heart',5.5,-6),('boom',5.62,-10),
 ('whoosh',5.9,-9),('pop',7.68,-11),('pop',8.28,-11),('pop',8.82,-11),('pop',9.38,-11),('pop',9.92,-11),('pop',10.68,-11),('tick',7.74,-14),
 ('whoosh',11.15,-10),('tick',12.76,-9),('tick',13.48,-9),('tick',14.2,-9),('sparkle',14.25,-12),('shimmer',14.72,-12),
 ('whoosh',15.45,-9),('boom',15.95,-11),('swipe',17.5,-12),('shimmer',17.86,-10),('sparkle',18.2,-12),
 ('swipe',18.85,-10),('whoosh',21.05,-9),('boom',21.3,-9),('bubbles',21.6,-10),('pop',22.46,-9),('pop',22.76,-9),('pop',23.1,-9),('bubbles',22.75,-11),
 ('whoosh',23.7,-9),('boom',24.1,-9),('swipe',25.15,-10),('sparkle',25.5,-11),('pop',27.22,-10),('pop',27.46,-10),
 ('whoosh',28.0,-10),('sparkle',28.3,-10),('whoosh',29.15,-10),('swipe',31.0,-13),('tap',32.38,-7),('tap',33.5,-7),('cash',33.55,-9),
 ('whoosh',34.45,-9),('boom',34.75,-8),('pop',36.3,-9),('clock',36.8,-13),('whoosh',38.65,-9),('shimmer',39.0,-9),('boom',39.05,-8)]
fx=np.zeros((N,2))
for name,t,db in S:
    a=load(D+name+'.wav')
    if name=='clock': a=a[:int(1.9*SR)]
    i=int(t*SR); j=min(N,i+len(a)); fx[i:j]+=a[:j-i]*10**(db/20)
# small room reverb send for SFX only (luxury airy tail)
ir_t=np.arange(int(1.2*SR))/SR; rng=np.random.default_rng(3)
ir=rng.standard_normal((len(ir_t),2))*np.exp(-ir_t*5)[:,None]*0.02
wet=np.stack([fftconvolve(fx[:,c],ir[:,c])[:N] for c in range(2)],1)
mix=vo+mu+fx+wet*0.6
fade=np.minimum(1,(DUR-np.arange(N)/SR)/0.6); mix*=fade[:,None]
sf.write('work/mix_pre.wav',mix.astype(np.float32),SR,subtype='FLOAT'); print('peak',np.abs(mix).max())
