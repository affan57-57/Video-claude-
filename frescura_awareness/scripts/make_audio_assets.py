"""Synthesize SFX + a minimal luxury deep-house bed (royalty-free, fully generated)."""
import numpy as np, soundfile as sf, sys
from scipy.signal import butter, sosfilt
SR=48000; OUT=sys.argv[1]; rng=np.random.default_rng(11)
T=lambda d: np.arange(int(d*SR))/SR
def norm(x,db=-1): return x/(np.max(np.abs(x))+1e-9)*10**(db/20)
def st(x,w=0.0):
    d=int(w*SR); R=np.roll(x,d) if d else x; return np.stack([x,R],1)
def bp(x,lo,hi): return sosfilt(butter(2,[lo,hi],btype='band',fs=SR,output='sos'),x,axis=0)
def lp(x,f): return sosfilt(butter(2,f,btype='low',fs=SR,output='sos'),x,axis=0)
def hp(x,f): return sosfilt(butter(2,f,btype='high',fs=SR,output='sos'),x,axis=0)
def sweep_noise(d,f0,f1,q=0.5):
    n=rng.standard_normal(int(d*SR)); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        p=i/len(n); fc=f0*(f1/f0)**p; y[i:i+seg]=bp(n[i:i+seg],fc*(1-q),fc*(1+q))
    return y
def whoosh(d=0.55,up=True):
    tt=T(d); y=sweep_noise(d,400,5000) if up else sweep_noise(d,5000,300)
    env=np.sin(np.pi*np.clip(tt/d,0,1))**1.5; x=y*env
    L=x*(1-tt/d)+.25*x; R=x*(tt/d)+.25*x; return np.stack([L,R],1)
def impact():
    tt=T(1.6); f=55+120*np.exp(-tt*18); ph=2*np.pi*np.cumsum(f)/SR
    boom=np.sin(ph)*np.exp(-tt*3.2); n=lp(rng.standard_normal(len(tt)),2500)*np.exp(-tt*14)*.5
    tail=hp(rng.standard_normal(len(tt)),3000)*np.exp(-tt*5)*.08
    return st(np.tanh(1.6*(boom+n))+tail,0.006)
def riser(d=1.4):
    tt=T(d); y=sweep_noise(d,300,9000,0.35); tone=np.sin(2*np.pi*np.cumsum(220*(4**(tt/d)))/SR)*.15
    return st((y+tone)*(tt/d)**2.2,0.009)
def pop():
    tt=T(0.09); f=1400*np.exp(-tt*45)+250; return st(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*55))
def click():
    tt=T(0.05); x=hp(rng.standard_normal(len(tt)),2000)*np.exp(-tt*300)+np.sin(2*np.pi*2800*tt)*np.exp(-tt*200)*.6
    return st(x)
def bubbles(d=1.2,n=16):
    x=np.zeros(int((d+.2)*SR))
    for k in range(n):
        o=int(rng.uniform(0,d)*SR); L=int(rng.uniform(.03,.07)*SR); tt=np.arange(L)/SR
        f0=rng.uniform(600,1800); f=f0*(1+tt*rng.uniform(8,20)); b=np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*tt/tt[-1])
        x[o:o+L]+=b*rng.uniform(.3,1)
    return st(x,0.004)
def bell(f,d,dec=5,parts=((1,1),(2.0,.35),(3.01,.15),(4.2,.07))):
    tt=T(d); return sum(a*np.sin(2*np.pi*f*m*tt)*np.exp(-dec*m**.5*tt) for m,a in parts)*np.minimum(1,tt/.002)
def shimmer(d=1.3,n=18):
    x=np.zeros(int((d+.6)*SR))
    for k in range(n):
        o=int(rng.uniform(0,d)*SR); b=bell(rng.uniform(3000,7500),.5,14,((1,1),(2.01,.25)))
        x[o:o+len(b)]+=b*rng.uniform(.3,1)*(1-o/len(x))
    return st(hp(x,2000),0.012)
def chime():
    x=np.zeros(int(1.6*SR))
    for i,f in enumerate([1318.5,1975.5,2637.0]):
        b=bell(f,1.4,4); o=int(i*.06*SR); x[o:o+len(b)]+=b
    return st(x,0.01)
def notify():
    x=np.zeros(int(.9*SR)); a=bell(1567.98,.6,7); b=bell(2093,.7,6); x[:len(a)]+=a; o=int(.11*SR); x[o:o+len(b)]+=b; return st(x)
def tick():
    tt=T(.03); return st(np.sin(2*np.pi*4200*tt)*np.exp(-tt*400))
def sub_drop():
    tt=T(1.0); f=90*np.exp(-tt*2.5)+30; return st(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*2.5))
def swipe():
    return whoosh(0.3,True)
SFX=dict(whoosh=whoosh(),whoosh_down=whoosh(0.7,False),impact=impact(),riser=riser(),pop=pop(),click=click(),
         bubbles=bubbles(),shimmer=shimmer(),chime=chime(),notify=notify(),tick=tick(),sub_drop=sub_drop(),swipe=swipe())
for k,v in SFX.items(): sf.write(f"{OUT}/{k}.wav",norm(v).astype(np.float32),SR)

# ---- music bed: 118 BPM minimal deep-house, A minor-ish lux chords ----
BPM=118; beat=60/BPM; DUR=float(sys.argv[2]) if len(sys.argv)>2 else 40
N=int(DUR*SR); mus=np.zeros((N,2))
def add(x,t,g=1.0):
    o=int(t*SR); 
    if o>=N: return
    if x.ndim==1: x=np.stack([x,x],1)
    L=min(len(x),N-o); mus[o:o+L]+=x[:L]*g
def kick():
    tt=T(.45); f=48+110*np.exp(-tt*28); return np.tanh(2*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*7))
def hat(op=False):
    tt=T(.25 if op else .05); return hp(rng.standard_normal(len(tt)),8000)*np.exp(-tt*(18 if op else 90))
def clap():
    tt=T(.25); n=bp(rng.standard_normal(len(tt)),900,5000); env=sum(np.exp(-np.clip(tt-d,0,None)*60)*(tt>=d) for d in (0,.012,.024))*.0+np.exp(-tt*25)
    return n*env
def keys(freqs,d):
    tt=T(d); x=sum(np.sin(2*np.pi*f*tt)+.25*np.sin(2*np.pi*2*f*tt)*np.exp(-tt*3) for f in freqs)
    x*=np.minimum(1,tt/.01)*np.exp(-tt*1.1); return lp(x,3500)
def pad(freqs,d):
    tt=T(d); x=sum(np.sin(2*np.pi*f*tt+np.sin(2*np.pi*.3*tt))+np.sin(2*np.pi*f*1.003*tt) for f in freqs)
    env=np.minimum(1,tt/.6)*np.minimum(1,(d-tt)/.6); return lp(x*env,1800)
def bass(f,d):
    tt=T(d); x=np.sin(2*np.pi*f*tt)+.3*np.sin(2*np.pi*2*f*tt); return np.tanh(1.5*x)*np.minimum(1,tt/.005)*np.exp(-tt*2.5)
mid=lambda n: 440*2**((n-69)/12)
prog=[([57,60,64,67],45),([53,57,60,64],41),([48,52,55,59],36),([55,59,62,65],43)]  # Am7 Fmaj7 Cmaj7 G7(ish)
bar=4*beat; nb=int(DUR/bar)+1
for b in range(nb):
    t0=b*bar; ch,bn=prog[b%4]; fr=[mid(n) for n in ch]
    add(pad(fr,bar+.4),t0,.05)
    for s in (0,1.5,2.5): add(keys(fr,1.2),t0+s*beat,.035)
    for q in range(4):
        tb=t0+q*beat
        if b>=1 or q>=2: add(kick(),tb,.42)
        add(hat(),tb+beat/2,.09); add(hat(),tb+beat/4,.035); add(hat(),tb+3*beat/4,.035)
        if q in (1,3) and b>=1: add(clap(),tb,.12)
        add(bass(mid(bn),beat*.45),tb+beat/2,.16)
# sidechain-ish pump
tt=np.arange(N)/SR; ph=(tt%beat)/beat; duck=1-.45*np.exp(-ph*9); mus[:,0]*=duck; mus[:,1]*=duck
mus[:,1]=np.roll(mus[:,1],int(.004*SR))
fo=int(2*SR); mus[-fo:]*=np.linspace(1,0,fo)[:,None]
sf.write(f"{OUT}/music_bed.wav",norm(mus,-3).astype(np.float32),SR)
print("ok")
