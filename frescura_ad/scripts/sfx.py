import numpy as np, soundfile as sf, sys
from scipy.signal import butter, sosfilt
SR=48000; out=sys.argv[1]; rng=np.random.default_rng(11)
T=lambda d: np.arange(int(d*SR))/SR
def nrm(x,db=-1): return x/np.max(np.abs(x))*10**(db/20)
def st(x): return np.stack([x,x],1)
def bp(x,lo,hi): return sosfilt(butter(2,[lo,hi],btype='band',fs=SR,output='sos'),x,axis=0)
def hp(x,f): return sosfilt(butter(2,f,btype='high',fs=SR,output='sos'),x,axis=0)
def lp(x,f): return sosfilt(butter(2,f,btype='low',fs=SR,output='sos'),x,axis=0)
def sweepnoise(d,f0,f1,shape):
    n=rng.standard_normal(int(d*SR)); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        p=i/len(n); fc=f0*(f1/f0)**p
        y[i:i+seg]=sosfilt(butter(2,[fc*0.5,min(fc*1.8,20000)],btype='band',fs=SR,output='sos'),n[i:i+seg])
    return y*shape(T(d)/d)
def bell(f,d,dec=5,parts=((1,1),(2.76,.35),(5.4,.15))):
    t=T(d); return sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-dec*m**.4*t) for m,a in parts)*np.minimum(1,t/0.002)
def whoosh():  # fast air swish, panning L->R
    d=0.55; y=sweepnoise(d,400,6000,lambda p: np.sin(np.pi*p)**3); p=T(d)/d
    return np.stack([y*(1.1-p),y*(0.1+p)],1)
def swoosh_down():
    d=0.7; y=sweepnoise(d,7000,300,lambda p: (1-p)**1.5*np.minimum(1,p*12)); return st(y)
def riser():
    d=1.6; y=sweepnoise(d,200,9000,lambda p: p**2.2); t=T(d)
    tone=np.sin(2*np.pi*np.cumsum(120*2**(4*t/d))/SR)*(t/d)**2*0.4
    return st(y+tone)
def impact():  # sub boom + transient
    d=1.8; t=T(d); f=55+90*np.exp(-t*18); sub=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.6)
    cl=hp(rng.standard_normal(len(t)),1500)*np.exp(-t*45)*0.6
    tail=lp(rng.standard_normal(len(t)),900)*np.exp(-t*4)*0.15
    return st(np.tanh(1.6*(sub+cl+tail)))
def shimmer():  # luxury glass sparkle
    x=np.zeros(int(1.6*SR))
    for k in range(18):
        o=int(rng.uniform(0,0.9)*SR); b=bell(rng.uniform(2800,7500),0.6,dec=9); x[o:o+len(b)]+=b*rng.uniform(.3,1)
    x=hp(x,2000); return np.stack([x,np.roll(x,int(0.013*SR))],1)
def glass():  # single luxury "ting"
    x=bell(2093,1.6,dec=3.2)+0.5*bell(3136,1.6,dec=4); return st(x)
def tick():
    t=T(0.06); x=np.sin(2*np.pi*3200*t)*np.exp(-t*160)+hp(rng.standard_normal(len(t)),4000)*np.exp(-t*300)*0.5; return st(x)
def pop():
    t=T(0.14); f=1100*np.exp(-t*28)+220; x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*35); return st(x)
def bubbles():  # foam squish/bubbles
    d=1.3; x=np.zeros(int(d*SR)+SR//4)
    for k in range(40):
        o=int(rng.uniform(0,d)*SR); tt=T(rng.uniform(.02,.06)); f=rng.uniform(500,2200)*np.exp(tt*rng.uniform(8,25))
        b=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*60); x[o:o+len(b)]+=b*rng.uniform(.2,1)
    n=bp(rng.standard_normal(len(x)),1500,6000)*0.08; return st(x+n)
def pump():  # pump click + hiss
    t=T(0.5); cl=bp(rng.standard_normal(len(t)),800,4000)*np.exp(-t*90)
    hiss=bp(rng.standard_normal(len(t)),2000,9000)*np.exp(-((t-0.18)/0.1)**2)*0.35
    return st(cl+hiss)
def shutter():
    t=T(0.25); a=bp(rng.standard_normal(len(t)),1000,8000)
    env=np.exp(-t*80)+0.8*np.exp(-np.maximum(0,t-0.09)*90)*(t>0.09); return st(a*env)
def heartbeat():
    x=np.zeros(int(0.9*SR))
    for o,g in((0,1),(0.18,.7)):
        t=T(0.25); b=np.sin(2*np.pi*np.cumsum(60+40*np.exp(-t*30))/SR)*np.exp(-t*18); i=int(o*SR); x[i:i+len(b)]+=b*g
    return st(np.tanh(2*x))
def cha_ching():  # CTA bag/cart
    x=np.zeros(int(1.4*SR)); t=T(0.08); c=bp(rng.standard_normal(len(t)),2000,9000)*np.exp(-t*60); x[:len(c)]+=c
    for i,f in enumerate([2637,3520]): b=bell(f,1.1,dec=4.5)[:len(x)-int((0.06+i*0.08)*SR)]; o=int((0.06+i*0.08)*SR); x[o:o+len(b)]+=b*0.8
    return st(x)
fx=dict(whoosh=whoosh,swoosh_down=swoosh_down,riser=riser,impact=impact,shimmer=shimmer,glass=glass,tick=tick,pop=pop,bubbles=bubbles,pump=pump,shutter=shutter,heartbeat=heartbeat,cha_ching=cha_ching)
for k,f in fx.items():
    y=nrm(f()); sf.write(f"{out}/{k}.wav",y.astype(np.float32),SR); print(k,round(len(y)/SR,2))
