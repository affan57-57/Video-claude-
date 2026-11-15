# Mix voice + music bed + SFX cues into assets/audio/mix.wav (48k stereo)
import numpy as np, soundfile as sf, subprocess, io, os
SR=48000; TOTAL=33.6; OFF=0.25; N=int(TOTAL*SR)
def load(p):
    if p.endswith('.mp3'):
        raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
        a=np.frombuffer(raw,np.float32).reshape(-1,2).copy()
    else:
        a,sr=sf.read(p,dtype='float32'); assert sr==SR,(p,sr)
        if a.ndim==1: a=np.stack([a,a],1)
    return a
def db(x): return 10**(x/20)
mix=np.zeros((N,2),np.float32)
voice=load('assets/audio/voice.wav'); vi=int(OFF*SR); vlen=min(len(voice),N-vi); vtrack=np.zeros((N,2),np.float32); vtrack[vi:vi+vlen]=voice[:vlen]
# music, ducked by voice envelope
music=load('assets/audio/music.wav')[:N]; music=np.vstack([music,np.zeros((N-len(music),2),np.float32)])
env=np.abs(vtrack[:,0]); k=int(0.25*SR); env=np.convolve(env,np.ones(k)/k,'same'); env=np.clip(env/0.05,0,1)
duck=db(-23)*(1-env)+db(-29)*env      # bed: -23 dB in gaps, -29 dB under speech
t=np.arange(N)/SR; duck=np.where(t>31.2, db(-18), duck)
mix+=vtrack+music*duck[:,None].astype(np.float32)
S='assets/audio/sfx/'; L='assets/audio/'
cues=[(0.00,S+'impact-bass-1.mp3',-4),(0.70,L+'whoosh_s.wav',-12),(0.85,L+'whoosh_s.wav',-13),
 (2.20,S+'whoosh-short.mp3',-12),(2.65,S+'sparkle.mp3',-10),(3.30,L+'slam.wav',-6),(4.20,S+'impact-bass-1.mp3',-4),(4.50,S+'pop.mp3',-12),
 (5.05,L+'whoosh.wav',-9),(5.30,S+'whoosh-short.mp3',-11),(6.40,L+'bubbles.wav',-14),(6.50,S+'pop.mp3',-11),
 (6.98,L+'whoosh.wav',-9),(7.25,S+'whoosh-short.mp3',-11),(8.15,S+'click-soft.mp3',-12),(9.20,S+'sparkle.mp3',-8),
 (9.45,L+'whoosh.wav',-9),(9.70,S+'whoosh-short.mp3',-11),(10.20,L+'whoosh_s.wav',-13),
 *[(11.10+i*0.21,S+'pop.mp3',-13) for i in range(7)],(12.45,S+'ping.mp3',-10),
 (13.08,S+'whoosh-short.mp3',-10),(13.70,L+'whoosh_s.wav',-14),(14.55,S+'impact-bass-1.mp3',-5),(14.60,L+'slam.wav',-8),
 (14.40,L+'riser.wav',-11),(15.40,S+'impact-bass-2.mp3',-6),(15.40,L+'swell.wav',-14),(15.90,S+'whoosh-short.mp3',-14),
 (17.82,L+'snap.wav',-16),(17.94,L+'snap.wav',-17),(18.04,S+'glitch-3.mp3',-20),(18.14,S+'sparkle.mp3',-9),
 (18.60,L+'whoosh.wav',-9),(18.80,L+'bubbles.wav',-11),(19.10,S+'pop.mp3',-14),(19.50,S+'pop.mp3',-14),(19.85,S+'pop.mp3',-14),(20.18,S+'whoosh-short.mp3',-11),
 (21.20,S+'sparkle.mp3',-12),(21.72,S+'sparkle.mp3',-12),(21.90,L+'shimmer.wav',-10),(22.20,S+'whoosh-short.mp3',-10),
 (22.45,L+'whoosh.wav',-9),(23.17,S+'click-soft.mp3',-10),(23.37,S+'click-soft.mp3',-10),(23.57,S+'click-soft.mp3',-10),(24.43,L+'slam.wav',-7),(25.38,S+'whoosh-short.mp3',-10),
 (25.60,S+'pop.mp3',-10),(26.07,S+'click.mp3',-6),(26.40,L+'whoosh_s.wav',-12),(27.87,S+'click.mp3',-7),(27.92,S+'notification.mp3',-11),
 (28.73,S+'click.mp3',-7),(28.80,S+'chime.mp3',-8),(29.02,S+'whoosh-short.mp3',-11),
 (29.30,L+'whoosh_s.wav',-12),*[(29.80+i*0.1,L+'tick.wav',-15) for i in range(8)],(30.70,S+'impact-bass-1.mp3',-3),(31.20,L+'whoosh.wav',-11),(31.30,S+'sparkle.mp3',-8),(31.70,L+'shimmer.wav',-11)]
cache={}
for t0,p,g in cues:
    if p not in cache:
        a=load(p); a=a/(np.max(np.abs(a))+1e-9)
        pk=int(np.argmax(np.abs(a[:,0])>0.5))   # first strong transient
        cache[p]=(a,pk)
    a,pk=cache[p]
    lead = pk if pk < int(0.4*SR) else 0       # only align short-attack sounds
    i=int(t0*SR)-lead+int(SR/30)
    if i<0: a=a[-i:]; i=0
    j=min(N,i+len(a)); mix[i:j]+=a[:j-i]*db(g)*db(-6)
sf.write('assets/audio/mix_pre.wav',mix,SR,subtype='FLOAT')
print('cues',len(cues))
