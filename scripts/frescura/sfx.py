import numpy as np, soundfile as sf, sys
from scipy.signal import butter, sosfilt
SR=48000; out=sys.argv[1]; rng=np.random.default_rng(11)
T=lambda d: np.arange(int(d*SR))/SR
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],btype='band',fs=SR,output='sos'),x,axis=0)
def lp(x,f,o=2): return sosfilt(butter(o,f,btype='low',fs=SR,output='sos'),x,axis=0)
def hp(x,f,o=2): return sosfilt(butter(o,f,btype='high',fs=SR,output='sos'),x,axis=0)
def st(x,w=0.008): return np.stack([x,np.roll(x,int(w*SR))*0.95],1)
def norm(x,db=-1): return x/(np.max(np.abs(x))+1e-9)*10**(db/20)
def bell(f,d,dec=6,parts=((1,1),(2.0,.35),(3.01,.18),(4.2,.08))):
    t=T(d); return sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-dec*m**.5*t) for m,a in parts)*np.minimum(1,t/0.002)
def sweepnoise(d,f0,f1,q=0.5,env=None):
    n=rng.standard_normal(int(d*SR)); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        p=i/len(n); fc=f0*(f1/f0)**p
        y[i:i+seg]=sosfilt(butter(2,[fc*(1-q),fc*(1+q)],btype='band',fs=SR,output='sos'),n[i:i+seg])
    return y
S={}
# swoosh: fast airy pass L->R
def swoosh(d=0.55,f0=500,f1=5000):
    t=T(d); y=sweepnoise(d,f0,f1); e=np.sin(np.pi*(t/d)**0.7)**3; x=y*e
    return np.stack([x*(1-t/d)+.3*x, x*(t/d)+.3*x],1)
S['swoosh']=swoosh(); S['swoosh_low']=swoosh(0.8,200,1800)
# impact: sub drop + noise crack + tail
def impact():
    t=T(2.2); f=55+120*np.exp(-t*18); sub=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.2)
    crack=hp(rng.standard_normal(len(t)),1500)*np.exp(-t*35)*0.6
    tail=lp(rng.standard_normal(len(t)),900)*np.exp(-t*3)*0.12
    return st(np.tanh(1.6*(sub+crack+tail)),0.012)
S['impact']=impact()
# riser: rising filtered noise + rising tone
def riser(d=1.3):
    t=T(d); n=sweepnoise(d,300,9000,0.35)*(t/d)**2.2
    f=200*(8)**(t/d); tone=np.sin(2*np.pi*np.cumsum(f)/SR)*(t/d)**3*0.25
    return st(n+tone,0.01)
S['riser']=riser()
# tick (clock) and tap (button)
def tick():
    t=T(0.06); return st(hp(rng.standard_normal(len(t)),2500)*np.exp(-t*160)+0.5*np.sin(2*np.pi*2400*t)*np.exp(-t*120))
S['tick']=tick()
def tap():
    t=T(0.18); f=1400*np.exp(-t*25)+300; x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*30)
    x+=hp(rng.standard_normal(len(t)),3000)*np.exp(-t*250)*0.5; return st(x)
S['tap']=tap()
def pop():
    t=T(0.14); f=700*np.exp(-t*28)+220; return st(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*38))
S['pop']=pop()
# shimmer: cluster of high bells
def shimmer(d=1.4,n=22):
    x=np.zeros(int((d+0.6)*SR))
    for k in range(n):
        o=int(rng.uniform(0,d*0.75)*SR); f=rng.choice([2093,2637,3136,3520,4186,5274])*rng.uniform(.995,1.005)
        b=bell(f,0.5,dec=10,parts=((1,1),(2.01,.25))); x[o:o+len(b)]+=b*rng.uniform(.3,1)
    x=hp(x,1800); return np.stack([x,np.roll(x,int(0.013*SR))],1)
S['shimmer']=shimmer()
# lux ding (soft two-note)
def ding():
    a=bell(1567.98,1.6,4); b=bell(2093,1.6,4); x=np.zeros(int(1.9*SR)); x[:len(a)]+=a; o=int(.09*SR); x[o:o+len(b)]+=b*.8; return st(x,0.01)
S['ding']=ding()
# check / success chime (3 up)
def success():
    x=np.zeros(int(1.6*SR))
    for i,f in enumerate([1318.5,1661.2,1975.5]):
        b=bell(f,1.2,5); o=int(i*0.075*SR); x[o:o+len(b)]+=b
    return st(x,0.01)
S['success']=success()
# cash/checkout: register ka-ching
def kaching():
    x=np.zeros(int(1.4*SR)); t=T(0.05); c=hp(rng.standard_normal(len(t)),2000)*np.exp(-t*90); x[:len(c)]+=c*.8
    for f in (2637,3951): b=bell(f,1.2,4.5); o=int(.06*SR); x[o:o+len(b)]+=b*.6
    return st(x)
S['kaching']=kaching()
# heartbeat-ish soft thump for emotional line
def thump():
    t=T(0.5); f=50+60*np.exp(-t*30); return st(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9))
S['thump']=thump()
# bubbles (foam)
def bubbles(d=1.2,n=28):
    x=np.zeros(int((d+.3)*SR))
    for k in range(n):
        o=int(rng.uniform(0,d)*SR); tt=T(rng.uniform(.03,.07)); f0=rng.uniform(500,1600)
        f=f0*(1+tt*rng.uniform(6,14)); b=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*60)*np.sin(np.pi*tt/tt[-1])
        x[o:o+len(b)]+=b*rng.uniform(.3,1)
    return np.stack([x,np.roll(x,int(.006*SR))],1)
S['bubbles']=bubbles()
# glitch/tape stop for transition
def boom_rev():
    i=impact()[::-1][-int(0.9*SR):]; return i*np.linspace(0,1,len(i))[:,None]**2
S['reverse']=boom_rev()
for k,v in S.items():
    v=norm(v,-1.0); sf.write(f"{out}/{k}.wav",v.astype(np.float32),SR); print(k, round(len(v)/SR,2))
