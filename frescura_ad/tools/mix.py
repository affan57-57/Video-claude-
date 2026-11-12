import numpy as np, soundfile as sf, sys, subprocess
S=sys.argv[1]; SR=48000; D=39.6
L=int(D*SR); mix=np.zeros((L,2))
def load(n):
    a,sr=sf.read(f"{S}/{n}",dtype="float32"); a=a if a.ndim==2 else np.stack([a,a],1); assert sr==SR; return a
cues=[(0.00,"impact",-3),(0.00,"swoosh_fast",-8),(0.88,"swoosh",-9),(1.65,"swoosh_fast",-9),(2.05,"tick",-10),(2.44,"pop",-8),(3.25,"swoosh",-10),(3.26,"pop",-8),(4.40,"pop",-8),
(5.45,"swoosh",-9),(5.5,"tick",-11),(6.65,"swoosh_fast",-10),(7.15,"tick_lo",-8),(8.05,"swoosh_fast",-10),(8.12,"tick_lo",-8),(8.55,"swoosh_fast",-10),(8.70,"tick_lo",-8),
(9.40,"impact",-6),(9.7,"tape_stop",-12),(10.55,"shimmer",-11),(10.55,"swoosh",-9),(11.8,"tick",-10),(12.75,"swoosh",-9),(12.85,"tick",-10),(14.85,"swoosh",-9),(14.95,"tick",-10),
(15.55,"riser",-7),(16.95,"impact",-1.5),(16.95,"shimmer",-8),(17.4,"swoosh",-8),(17.75,"ping_hi",-7),(18.4,"shimmer",-13),(20.0,"shimmer",-14),
(21.35,"swoosh",-9),(21.6,"bubbles",-7),(22.0,"pop",-9),(22.6,"tick",-10),(24.25,"swoosh_fast",-9),(24.3,"shimmer",-12),(24.6,"bubbles",-11),
(25.5,"swoosh",-8),(25.95,"swoosh",-8),(27.1,"ping",-7),(29.4,"impact",-7),(29.45,"swoosh",-9),(31.4,"swoosh_fast",-9),(32.7,"impact",-5),(32.7,"swoosh",-9),
(34.1,"swoosh",-8),(34.24,"ping_hi",-9),(35.05,"swoosh",-8),(35.18,"ping",-9),(36.0,"impact",-2.5),(36.0,"shimmer",-9),(36.15,"pop",-6),(36.8,"tick",-9),(37.75,"ping_hi",-6),(38.6,"shimmer",-9)]
sfx=np.zeros((L,2))
for t,n,db in cues:
    a=load(f"sfx/{n}.wav")*10**(db/20); i=int(t*SR); j=min(L,i+len(a)); sfx[i:j]+=a[:j-i]
v=load("audio/voice_final.wav"); voice=np.zeros((L,2)); voice[:min(L,len(v))]=v[:L]
m=load("sfx/music.wav")[:L]
# duck music by voice envelope
env=np.abs(voice[:,0]); k=int(0.12*SR); env=np.convolve(env,np.ones(k)/k,mode="same"); env=env/env.max()
duck=10**((-13*np.clip(env*4,0,1))/20); g=np.ones(L)*10**(-11/20)
t=np.arange(L)/SR; g*=np.clip(t/0.4,0,1); g*=np.where(t>38.7, 1+1.2*np.clip((t-38.7)/0.3,0,1),1); g*=np.clip((D-t)/0.9,0,1)
mus=m*(g*duck)[:,None]
out=voice*1.0+sfx*0.85+mus
sf.write(f"{S}/audio/mix_pre.wav",out.astype(np.float32),SR,subtype="FLOAT")
subprocess.run(["ffmpeg","-v","error","-y","-i",f"{S}/audio/mix_pre.wav","-af","acompressor=threshold=-14dB:ratio=2:attack=10:release=150:makeup=1dB,loudnorm=I=-11:TP=-1.0:LRA=6,alimiter=limit=0.89:level=false","-ar","48000","-c:a","pcm_s24le",f"{S}/audio/final_mix.wav"],check=True)
