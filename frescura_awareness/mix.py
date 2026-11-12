# Mix voice + music bed + SFX cues into assets/audio/mix.wav (48k stereo)
import numpy as np, soundfile as sf, subprocess, io, os
SR=48000; TOTAL=37.4; OFF=0.25; N=int(TOTAL*SR)
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
t=np.arange(N)/SR; duck=np.where(t>35.0, db(-18), duck)
mix+=vtrack+music*duck[:,None].astype(np.float32)
S='assets/audio/sfx/'; L='assets/audio/'
cues=[(0.00,S+'impact-bass-1.mp3',-4),
 (0.22,S+'click-soft.mp3',-10),(0.72,S+'pop.mp3',-12),(1.74,S+'click-soft.mp3',-10),(2.24,S+'pop.mp3',-12),(2.80,S+'click-soft.mp3',-10),(3.30,S+'pop.mp3',-12),
 (4.25,S+'whoosh-short.mp3',-9),(4.50,L+'whoosh_s.wav',-12),(5.05,L+'slam.wav',-8),(5.71,L+'slam.wav',-6),(6.08,S+'impact-bass-1.mp3',-4),(6.60,L+'whoosh.wav',-9),
 *[(7.05+i*0.15,L+'tick.wav',-16) for i in range(6)],(8.29,L+'slam.wav',-8),(8.69,S+'click-soft.mp3',-12),(9.19,S+'click-soft.mp3',-12),(9.60,S+'click-soft.mp3',-12),
 (10.85,S+'pop.mp3',-10),(11.02,S+'ping.mp3',-9),(11.30,S+'whoosh-short.mp3',-9),(11.55,L+'whoosh.wav',-10),(12.65,L+'whoosh_s.wav',-12),
 (13.27,S+'pop.mp3',-11),(13.99,S+'pop.mp3',-11),(14.89,S+'pop.mp3',-11),(15.57,S+'whoosh-short.mp3',-9),
 *[(15.95+i*0.07,S+'key-press.mp3',-14) for i in range(5)],*[(16.73+i*0.12,L+'tick.wav',-15) for i in range(4)],
 (18.07,S+'error.mp3',-16),(18.10,L+'riser.wav',-11),(18.51,S+'whoosh-short.mp3',-10),(18.75,L+'slam.wav',-7),
 (19.28,S+'impact-bass-2.mp3',-4),(19.28,L+'swell.wav',-14),(19.86,L+'snap.wav',-16),(19.98,L+'snap.wav',-17),(20.08,S+'glitch-3.mp3',-20),(20.18,S+'sparkle.mp3',-9),
 (21.15,L+'whoosh.wav',-9),(21.35,L+'bubbles.wav',-11),(21.65,S+'pop.mp3',-14),(22.05,S+'pop.mp3',-14),(22.45,S+'pop.mp3',-14),(22.97,S+'whoosh-short.mp3',-11),
 (22.80,S+'sparkle.mp3',-12),(23.03,S+'pop.mp3',-13),(23.33,L+'shimmer.wav',-10),(24.36,S+'whoosh-short.mp3',-10),
 (24.60,L+'whoosh.wav',-9),(24.65,L+'slam.wav',-6),(25.26,L+'snap.wav',-11),(25.78,L+'snap.wav',-11),(26.46,S+'pop.mp3',-10),(27.66,S+'whoosh-short.mp3',-10),
 (28.20,S+'pop.mp3',-10),(28.50,S+'click.mp3',-6),(28.85,L+'whoosh_s.wav',-12),(29.34,S+'click.mp3',-7),(29.42,S+'chime.mp3',-8),
 *[(30.40+i*0.1,L+'tick.wav',-15) for i in range(5)],(30.74,S+'whoosh-short.mp3',-10),
 (30.95,L+'whoosh.wav',-8),(31.73,S+'ping.mp3',-10),(32.13,S+'pop.mp3',-10),(32.51,S+'ping.mp3',-10),
 (33.10,S+'whoosh-short.mp3',-10),(34.46,S+'impact-bass-1.mp3',-3),(35.12,L+'whoosh.wav',-11),(35.20,S+'sparkle.mp3',-8),(35.55,L+'shimmer.wav',-11)]
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
