import numpy as np, soundfile as sf, sys
from scipy.signal import butter, sosfilt
SR=48000; out=sys.argv[1]; rng=np.random.default_rng(7)
t=lambda d: np.arange(int(d*SR))/SR
def norm(x,db): return x/np.max(np.abs(x))*10**(db/20)
def st(x,pan=0.0): return np.stack([x*(1-pan)**.5, x*(1+pan)**.5],1)/1.0
def bell(f,d,partials=((1,1),(2.0,.4),(3.01,.2),(4.2,.1)),decay=6):
    tt=t(d); x=sum(a*np.sin(2*np.pi*f*m*tt)*np.exp(-decay*m**.5*tt) for m,a in partials)
    return x*np.minimum(1,tt/0.003)
# whoosh: band-passed noise with sweeping center
def whoosh(d=0.7):
    n=rng.standard_normal(int(d*SR)); tt=t(d); y=np.zeros_like(n); seg=1024
    for i in range(0,len(n),seg):
        p=i/len(n); fc=300+3500*np.sin(np.pi*p)**2
        sos=butter(2,[fc*0.6,fc*1.6],btype='band',fs=SR,output='sos'); y[i:i+seg]=sosfilt(sos,n[i:i+seg])
    env=np.sin(np.pi*tt/d)**2
    x=y*env; L=x*(1-tt/d)+0.2*x; R=x*(tt/d)+0.2*x
    return np.stack([L,R],1)
def chime2():  # "ting-tong" question chime
    a=bell(1318.5,0.9); b=bell(1046.5,1.2)
    x=np.zeros(int(1.4*SR)); x[:len(a)]+=a; o=int(0.16*SR); x[o:o+len(b)]+=b; return st(x)
def sparkle(d=1.0,n=14):
    x=np.zeros(int(d*SR)+SR//2)
    for k in range(n):
        o=int(rng.uniform(0,d*0.8)*SR); f=rng.uniform(2500,6000)
        b=bell(f,0.35,partials=((1,1),(2.01,.3)),decay=14); x[o:o+len(b)]+=b*rng.uniform(.4,1)
    sos=butter(2,1500,btype='high',fs=SR,output='sos'); x=sosfilt(sos,x)
    L=x.copy(); R=np.roll(x,int(0.011*SR)); return np.stack([L,R],1)
def ding(): x=bell(1760,1.0,decay=5)+0.5*bell(2637,0.8,decay=7)[:int(1.0*SR)] if False else bell(1760,1.0,decay=5); return st(x)
def pop():
    tt=t(0.12); f=900*np.exp(-tt*30)+180; ph=2*np.pi*np.cumsum(f)/SR
    x=np.sin(ph)*np.exp(-tt*40); return st(x)
def applause(d=2.2):
    x=np.zeros((int(d*SR),2))
    for k in range(900):
        o=int(rng.uniform(0,d-0.03)*SR); L=int(0.012*SR)
        c=rng.standard_normal(L)*np.exp(-np.arange(L)/SR*350)
        p=rng.uniform(-1,1); x[o:o+L,0]+=c*(1-p)*.5; x[o:o+L,1]+=c*(1+p)*.5
    sos=butter(2,[700,7000],btype='band',fs=SR,output='sos'); x=sosfilt(sos,x,axis=0)
    tt=t(d)[:,None]; env=np.minimum(1,tt/0.25)*np.minimum(1,(d-tt)/0.9); return x*env
def tada():
    x=np.zeros(int(1.8*SR))
    for i,f in enumerate([1046.5,1318.5,1568.0,2093.0]):
        b=bell(f,1.4,decay=3.5); o=int(i*0.07*SR); x[o:o+len(b)]+=b
    return st(x)
for name,fn in dict(whoosh=whoosh,chime=chime2,sparkle=sparkle,ding=ding,pop=pop,applause=applause,tada=tada).items():
    y=fn(); y=norm(y,-1.0); sf.write(f"{out}/{name}.wav",y.astype(np.float32),SR); print(name, y.shape[0]/SR)
