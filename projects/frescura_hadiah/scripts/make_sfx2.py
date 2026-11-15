import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
SR=48000; rng=np.random.default_rng(11)
T=lambda d: np.arange(int(d*SR))/SR
def st(x,w=0.0):
    L=x; R=np.roll(x,int(w*SR)) if w else x; return np.stack([L,R],1)
def norm(x,db=-1): return x/np.max(np.abs(x))*10**(db/20)
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],btype='band',fs=SR,output='sos'),x,axis=0)
def hp(x,f): return sosfilt(butter(2,f,btype='high',fs=SR,output='sos'),x,axis=0)
def lp(x,f): return sosfilt(butter(2,f,btype='low',fs=SR,output='sos'),x,axis=0)
def boom(d=1.6):
    t=T(d); f=38+70*np.exp(-t*9); ph=2*np.pi*np.cumsum(f)/SR
    sub=np.sin(ph)*np.exp(-t*2.6); click=lp(rng.standard_normal(len(t)),2500)*np.exp(-t*60)*0.6
    x=np.tanh(1.6*(sub+click)); return st(x)
def riser(d=1.6):
    t=T(d); n=rng.standard_normal(len(t)); y=np.zeros_like(n); seg=960
    for i in range(0,len(n),seg):
        p=i/len(n); fc=400+6000*p**2; y[i:i+seg]=bp(n[i:i+seg],fc*.7,min(fc*1.4,20000))
    tone=np.sin(2*np.pi*np.cumsum(200+700*(t/d)**2)/SR)*0.25
    env=(t/d)**2.2; x=(y+tone)*env; x[-int(.02*SR):]*=np.linspace(1,0,int(.02*SR)); return st(x,0.008)
def whoosh(d=0.45,lo=250,hi=5000):
    t=T(d); n=rng.standard_normal(len(t)); y=np.zeros_like(n); seg=480
    for i in range(0,len(n),seg):
        p=i/len(n); fc=lo+(hi-lo)*np.sin(np.pi*p)**1.5; y[i:i+seg]=bp(n[i:i+seg],fc*.6,min(fc*1.7,20000))
    env=np.sin(np.pi*t/d)**2; x=y*env; L=x*(1.2-t/d); R=x*(0.2+t/d); return np.stack([L,R],1)
def bell(f,d,dec=6,parts=((1,1),(2.0,.35),(3.0,.15),(4.1,.08))):
    t=T(d); return sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-dec*m**.5*t) for m,a in parts)*np.minimum(1,t/0.002)
def shimmer(d=1.4,n=22):
    x=np.zeros(int(d*SR)+SR)
    for k in range(n):
        o=int((k/n)*d*0.7*SR+rng.uniform(0,.03)*SR); f=rng.uniform(2800,7500)
        b=bell(f,.5,dec=10,parts=((1,1),(2.01,.25))); x[o:o+len(b)]+=b*rng.uniform(.3,1)*(1-k/n*.5)
    x=hp(x,1800); return np.stack([x,np.roll(x,500)],1)
def shutter():
    t=T(0.18); a=hp(rng.standard_normal(len(t)),1500)*np.exp(-t*90); b=np.zeros_like(a); o=int(.07*SR)
    b[o:]=hp(rng.standard_normal(len(t)-o),900)*np.exp(-(t[o:]-t[o])*70)*0.8; return st(a+b)
def pop(f0=700):
    t=T(0.09); f=f0*np.exp(-t*25)+f0*0.4; x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*55); return x
def bubbles(d=2.0,n=26):
    x=np.zeros(int(d*SR)+SR//5)
    for k in range(n):
        o=int(rng.uniform(0,d)*SR); p=pop(rng.uniform(500,1600))*rng.uniform(.3,1); x[o:o+len(p)]+=p
    fizz=bp(rng.standard_normal(len(x)),3000,9000)*0.08*np.minimum(1,np.arange(len(x))/(.2*SR))
    return np.stack([x+fizz,np.roll(x,300)+fizz],1)
def tap():
    t=T(0.08); x=np.sin(2*np.pi*1800*t)*np.exp(-t*90)+0.5*hp(rng.standard_normal(len(t)),3000)*np.exp(-t*200); return st(x)
def tick():
    t=T(0.03); x=hp(rng.standard_normal(len(t)),4000)*np.exp(-t*300)+np.sin(2*np.pi*3200*t)*np.exp(-t*250); return st(x)
def ding():
    x=bell(1567.98,1.6,dec=3.5)+0.6*np.pad(bell(2093,1.6,dec=4),(int(.09*SR),0))[:int(1.6*SR)]; return st(x,0.004)
def thud(): # soft deep hit for typographic stamps
    t=T(0.5); f=60+90*np.exp(-t*20); x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)+lp(rng.standard_normal(len(t)),1200)*np.exp(-t*45)*.4
    return st(np.tanh(1.4*x))
def heartbeat():
    x=np.zeros(int(0.9*SR)); t=T(0.25)
    for o,a in [(0,1),(0.22,0.7)]:
        h=np.sin(2*np.pi*55*t)*np.exp(-t*18)*a; i=int(o*SR); x[i:i+len(h)]+=h
    return st(np.tanh(2*x))
def swell(d=2.2): # reverse-cymbal-ish swell into end card
    t=T(d); n=hp(rng.standard_normal(len(t)),3000); env=(t/d)**3; x=n*env; x[-200:]*=np.linspace(1,0,200); return st(x,0.01)
fx=dict(boom=boom,riser=riser,whoosh=whoosh,whoosh_long=lambda:whoosh(0.8,150,3500),whoosh_hi=lambda:whoosh(0.3,1500,9000),
        shimmer=shimmer,shutter=shutter,bubbles=bubbles,tap=tap,tick=tick,ding=ding,thud=thud,heartbeat=heartbeat,swell=swell)
for k,f in fx.items():
    y=norm(f(),-1.0); sf.write(f"sfx/{k}.wav",y.astype(np.float32),SR); print(k,round(len(y)/SR,2))
