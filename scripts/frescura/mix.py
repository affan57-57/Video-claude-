import numpy as np, soundfile as sf, sys
SR=48000; D=32.0; N=int(D*SR); S=sys.argv[1]; W=sys.argv[2]
def ld(p):
    a,sr=sf.read(p,dtype='float32'); assert sr==SR,p
    return a if a.ndim==2 else np.stack([a,a],1)
mix=np.zeros((N,2),np.float32)
v=ld(W+'/voice_final.wav'); VO=int(0.6*SR); voice=np.zeros((N,2),np.float32); voice[VO:VO+len(v)]=v[:N-VO]
m=ld(W+'/music.wav')[:N]
# sidechain duck: envelope of voice
env=np.abs(voice[:,0]); k=int(0.05*SR); env=np.convolve(env,np.ones(k)/k,'same')
duck=np.clip(env/0.06,0,1); a=int(0.25*SR); duck=np.convolve(duck,np.ones(a)/a,'same')
mg=10**(-9/20)*(1-0.55*duck)       # music: loud-ish when no voice, ducked ~-7dB under voice
mix+=m*mg[:,None]+voice
cues=[('impact',0.0,-3),('sparkle',0.05,-12),('boom',0.08,-6),('swish',0.62,-10),('tick',1.19,-12),
('whoosh',1.58,-8),('pop',1.66,-10),('swish',3.05,-9),('tick',3.08,-10),('tick',3.72,-12),('boom',4.22,-7),('ting',4.25,-12),('sparkle',5.6,-12),
('whoosh',6.13,-8),('pop',6.55,-10),('impact',7.75,-9),('swish',7.98,-9),
('swell',7.3,-10),('impact',8.15,-5),('sparkle',8.25,-11),('ting',9.62,-11),
('whoosh',11.18,-8),('boom',11.2,-7),('foam',11.5,-8),('swish',12.0,-10),('pop',12.9,-9),('pop',13.25,-9),('pop',13.6,-9),('foam',13.55,-9),('sparkle',15.05,-10),('ting',15.1,-11),
('whoosh',16.18,-7),('boom',16.3,-7),('sparkle',16.4,-14),('tick',17.7,-12),
('whoosh',18.53,-7),('boom',18.6,-7),('sparkle',19.85,-11),
('swish',20.78,-9),('ting',21.95,-10),('sparkle',22.15,-12),
('riser',21.12,-9),('impact',22.72,-5),('pop',22.8,-8),('tap',23.55,-6),('tap',24.1,-6),('ching',24.05,-9),('tick',25.0,-11),('tap',25.3,-6),('tick',25.6,-13),('tick',26.0,-13),('tick',26.4,-13),
('swell',26.5,-10),('impact',27.3,-4),('whoosh',27.3,-8),('sparkle',27.55,-9),('ting',28.0,-11),('ching',28.8,-8),('pop',28.8,-10)]
for n,t,db in cues:
    x=ld(f'{S}/{n}.wav'); i=int(t*SR); L=min(len(x),N-i); mix[i:i+L]+=x[:L]*10**(db/20)
# soft limiter
pk=np.max(np.abs(mix)); print('peak before',pk)
pass
fo=int(31.4*SR); mix[fo:]*=np.linspace(1,0,N-fo)[:,None]
sf.write(W+'/mix_pre.wav',mix,SR,subtype='FLOAT')
