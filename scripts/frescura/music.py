import numpy as np, soundfile as sf, sys
from scipy.signal import butter, sosfilt
SR=48000; BPM=118; beat=60/BPM; D=float(sys.argv[2]); N=int(D*SR); rng=np.random.default_rng(3)
L=np.zeros(N); R=np.zeros(N)
def add(x,t,g=1.0,pan=0.0):
    i=int(t*SR); 
    if i>=N: return
    x=x[:N-i]; L[i:i+len(x)]+=x*g*np.sqrt(1-pan)/1.0; R[i:i+len(x)]+=x*g*np.sqrt(1+pan)/1.0
T=lambda d: np.arange(int(d*SR))/SR
t=T(0.45); kick=np.sin(2*np.pi*np.cumsum(48+110*np.exp(-t*28))/SR)*np.exp(-t*7); kick=np.tanh(2*kick)
t=T(0.06); hat=sosfilt(butter(2,7000,btype='high',fs=SR,output='sos'),rng.standard_normal(len(t)))*np.exp(-t*70)
t=T(0.12); shk=sosfilt(butter(2,[4000,10000],btype='band',fs=SR,output='sos'),rng.standard_normal(len(t)))*np.exp(-t*35)
t=T(0.25); clap=sosfilt(butter(2,[900,4000],btype='band',fs=SR,output='sos'),rng.standard_normal(len(t)))*np.exp(-t*22)
def ep(f,d):  # electric-piano-ish
    t=T(d); x=sum(a*np.sin(2*np.pi*f*m*t+0.3*np.sin(2*np.pi*f*t))*np.exp(-t*(1.8+m)) for m,a in ((1,1),(2,.3),(3,.08)))
    return x*np.minimum(1,t/0.004)
def bass(f,d):
    t=T(d); x=np.sin(2*np.pi*f*t)+0.25*np.sin(2*np.pi*2*f*t); return np.tanh(1.5*x)*np.minimum(1,t/0.005)*np.exp(-t*2.5)
chords=[(174.61,[349.2,440.0,523.3,659.3]),(164.81,[329.6,392.0,493.9,587.3]),(146.83,[293.7,349.2,440.0,523.3]),(130.81,[329.6,392.0,493.9,523.3])]
bar=4*beat; nb=int(D/bar)+1
for b in range(nb):
    t0=b*bar; root,ch=chords[b%4]
    for k in range(4):
        tb=t0+k*beat
        add(kick,tb,0.9); add(hat,tb+beat/2,0.25,0.3); add(shk,tb+beat*0.25,0.08,-0.4); add(shk,tb+beat*0.75,0.1,0.4)
        if k in (1,3): add(clap,tb,0.28)
        add(bass(root/2 if k%2 else root/2*1.0,beat*0.45),tb+beat/2,0.35)
    for st in (0, beat*1.5, beat*2.5):
        for j,f in enumerate(ch): add(ep(f,beat*1.6),t0+st+j*0.006,0.09,(-0.4+0.27*j))
# sidechain pump
env=np.ones(N); kl=int(beat*SR)
for b in range(int(D/beat)+1):
    i=int(b*beat*SR); seg=np.linspace(0,1,min(kl,N-i)) if i<N else []
    if len(seg): env[i:i+len(seg)]=0.55+0.45*seg**0.5
x=np.stack([L*env,R*env],1)
x=sosfilt(butter(2,30,btype='high',fs=SR,output='sos'),x,axis=0)
fi=int(0.6*SR); x[:fi]*=np.linspace(0,1,fi)[:,None]; fo=int(1.5*SR); x[-fo:]*=np.linspace(1,0,fo)[:,None]
x=x/np.max(np.abs(x))*0.8; sf.write(sys.argv[1],x.astype(np.float32),SR); print("music",D)
