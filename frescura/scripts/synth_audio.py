# Synthesized SFX + minimal luxury music bed (all original, no samples).
import numpy as np, soundfile as sf, sys, os
from scipy.signal import butter, sosfilt, fftconvolve
SR=48000; out=sys.argv[1]; os.makedirs(out,exist_ok=True); rng=np.random.default_rng(11)
T=lambda d: np.arange(int(d*SR))/SR
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],btype='band',fs=SR,output='sos'),x,axis=0)
def lp(x,f,o=2): return sosfilt(butter(o,f,btype='low',fs=SR,output='sos'),x,axis=0)
def hp(x,f,o=2): return sosfilt(butter(o,f,btype='high',fs=SR,output='sos'),x,axis=0)
def norm(x,db=-1): return x/(np.max(np.abs(x))+1e-9)*10**(db/20)
def st(x,w=0.0):
    d=int(0.013*SR*w); R=np.concatenate([np.zeros(d),x])[:len(x)] if d else x
    return np.stack([x,R],1)
def verb(x,dur=1.6,mix=0.25):
    n=int(dur*SR); ir=rng.standard_normal((n,2))*np.exp(-np.arange(n)/SR*4.5)[:,None]; ir=lp(ir,7000)
    if x.ndim==1: x=st(x)
    w=np.stack([fftconvolve(x[:,c],ir[:,c])[:len(x)+n] for c in range(2)],1)
    y=np.zeros_like(w); y[:len(x)]=x; return y*(1-mix)+norm(w,-1)*np.max(np.abs(x))*mix
def bell(f,d,decay=6,parts=((1,1),(2.0,.35),(3.0,.15),(4.17,.08))):
    t=T(d); return sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-decay*m**.5*t) for m,a in parts)*np.minimum(1,t/0.002)
def sweep_noise(d,f0,f1,q=0.5):
    n=rng.standard_normal(int(d*SR)); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        p=i/len(n); fc=f0*(f1/f0)**p; y[i:i+seg]=bp(n[i:i+seg],fc*(1-q),fc*(1+q))
    return y
S={}
def whoosh(d=0.55,f0=500,f1=5000):
    t=T(d); y=sweep_noise(d,f0,f1)*np.sin(np.pi*t/d)**1.5; p=t/d
    return np.stack([y*(1-p)+.3*y, y*p+.3*y],1)
S['whoosh']=whoosh(); S['whoosh_fast']=whoosh(0.32,900,7000); S['swoosh_down']=whoosh(0.5,6000,400)
def riser(d=1.4):
    t=T(d); n=sweep_noise(d,300,9000,0.35)*(t/d)**2.2
    tone=np.sin(2*np.pi*np.cumsum(220*(4**(t/d)))/SR)*(t/d)**3*0.25
    return verb(n+tone,1.0,0.3)
S['riser']=riser()
def impact():
    t=T(2.2); f=38+90*np.exp(-t*9); sub=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.2)
    click=hp(rng.standard_normal(len(t)),2500)*np.exp(-t*90)*0.6
    body=bp(rng.standard_normal(len(t)),80,900)*np.exp(-t*12)*0.7
    x=np.tanh(1.6*(sub+click+body)); return verb(x,1.8,0.22)
S['impact']=impact()
def tick():
    t=T(0.05); x=np.sin(2*np.pi*2400*t)*np.exp(-t*260)+hp(rng.standard_normal(len(t)),4000)*np.exp(-t*500)*.4; return st(x)
S['tick']=tick()
def pop():
    t=T(0.14); f=1100*np.exp(-t*28)+220; x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*34); return st(x)
S['pop']=pop()
def shimmer(d=1.3,n=22):
    x=np.zeros(int((d+0.6)*SR))
    for k in range(n):
        o=int(rng.uniform(0,d*0.85)*SR); f=rng.choice([1567.98,2093,2349.3,2637,3135.9,4186])*rng.uniform(.998,1.002)
        b=bell(f,0.5,decay=9)*rng.uniform(.3,1)*(1-o/len(x)); x[o:o+len(b)]+=b
    return verb(hp(x,1200),1.4,0.35)
S['shimmer']=shimmer()
def glass():
    x=bell(2093,1.8,decay=2.6,parts=((1,1),(2.76,.4),(5.4,.2),(8.9,.08)))+0.5*bell(3136,1.8,decay=3.2)
    return verb(x,2.0,0.3)
S['glass']=glass()
def foam(d=1.1):
    x=np.zeros(int(d*SR)); 
    for k in range(70):
        o=int(rng.uniform(0,d-0.06)*SR); L=int(rng.uniform(0.008,0.03)*SR); t=np.arange(L)/SR
        f=rng.uniform(500,2500); b=np.sin(2*np.pi*f*(1+t*30)*t)*np.exp(-t*120); x[o:o+L]+=b*rng.uniform(.2,1)
    air=bp(rng.standard_normal(len(x)),800,6000)*0.35*np.sin(np.pi*T(d)/d)
    return st(x+air,0.6)
S['foam']=foam()
def pump_click():
    t=T(0.18); x=hp(rng.standard_normal(len(t)),1500)*np.exp(-t*120)+np.sin(2*np.pi*180*t)*np.exp(-t*40)*.8
    t2=T(0.12); y=np.concatenate([x,np.zeros(int(0.05*SR)),0.6*np.sin(2*np.pi*1400*t2)*np.exp(-t2*80)]); return st(y)
S['pump']=pump_click()
def toggle():
    a=tick()[:,0]; b=np.sin(2*np.pi*880*T(0.25))*np.exp(-T(0.25)*18)*.6+np.sin(2*np.pi*1318.5*T(0.25))*np.exp(-T(0.25)*18)*.4
    x=np.zeros(int(0.4*SR)); x[:len(a)]+=a; x[int(.06*SR):int(.06*SR)+len(b)]+=b; return st(x,0.5)
S['toggle']=toggle()
def clock(n=6,bpm=150):
    x=np.zeros(int((n*60/bpm+0.3)*SR))
    for k in range(n):
        f=3200 if k%2==0 else 2600; t=T(0.04); b=np.sin(2*np.pi*f*t)*np.exp(-t*300)+hp(rng.standard_normal(len(t)),5000)*np.exp(-t*600)*.5
        o=int(k*60/bpm*SR); x[o:o+len(b)]+=b
    return st(x)
S['clock']=clock()
def kaching():
    x=np.zeros(int(1.4*SR)); c=hp(rng.standard_normal(int(0.08*SR)),2000)*np.exp(-T(0.08)*60); x[:len(c)]+=c*0.7
    for i,f in enumerate([2637,3520]):
        b=bell(f,1.2,decay=4); o=int((0.05+i*0.09)*SR); x[o:o+len(b)]+=b*0.7
    return verb(x,1.2,0.25)
S['kaching']=kaching()
def sub_drop():
    t=T(1.2); f=90*np.exp(-t*2.5)+30; return st(np.tanh(2*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.8)))
S['subdrop']=sub_drop()
def swipe_up():
    t=T(0.35); x=sweep_noise(0.35,1500,9000,0.4)*np.sin(np.pi*t/0.35)
    tone=np.sin(2*np.pi*np.cumsum(600*(3**(t/0.35)))/SR)*np.exp(-((t-0.2)/0.08)**2)*0.3
    return st(x+tone,0.4)
S['swipe']=swipe_up()
for k,v in S.items():
    v=np.asarray(v); v=v if v.ndim==2 else st(v); sf.write(f"{out}/{k}.wav",norm(v,-1).astype(np.float32),SR); print(k, round(len(v)/SR,2))

# ---------- music bed: minimal luxury deep-house, 118 BPM, ~60 s ----------
BPM=118; beat=60/BPM; bars=30; L=int(bars*4*beat*SR)+SR*2; M=np.zeros((L,2))
def kick():
    t=T(0.45); f=48+110*np.exp(-t*30); return np.tanh(1.4*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*6.5))
def hat(open_=False):
    d=0.22 if open_ else 0.05; t=T(d); return hp(rng.standard_normal(len(t)),8000)*np.exp(-t*(14 if open_ else 90))
def clap():
    t=T(0.3); n=bp(rng.standard_normal(len(t)),900,5000); env=np.zeros_like(t)
    for o in (0,0.011,0.022): env+=np.exp(-np.clip(t-o,0,None)*55)*(t>=o)
    return n*env*0.6
def add(x,pos,g=1.0,pan=0.0):
    i=int(pos*SR); x=x if x.ndim==2 else np.stack([x*(1-pan),x*(1+pan)],1); e=min(L,i+len(x)); M[i:e]+=x[:e-i]*g
nf=lambda n: 440*2**((n-69)/12)
chords=[[57,60,64,67,71],[53,57,60,64,67],[48,52,55,59,62],[55,59,62,65,69]]  # Am9 Fmaj9 Cmaj9 G9-ish
bass=[33,29,36,31]
for b in range(bars):
    t0=b*4*beat; ch=chords[b%4]
    # pad (soft saw stack, lowpassed) for the whole bar
    d=4*beat; t=T(d); pad=np.zeros(len(t))
    for n in ch:
        for det in (-0.07,0.07): pad+=np.sin(2*np.pi*nf(n+det)*t)+0.3*np.sin(2*np.pi*2*nf(n+det)*t)
    pad*=np.minimum(1,t/0.25)*np.minimum(1,(d-t)/0.3); add(lp(pad,1800)*0.022,t0,pan=0)
    for q in range(4):
        tb=t0+q*beat
        if b>=1: add(kick()*0.55,tb)
        if b>=2 and q in (1,3): add(clap()*0.32,tb,pan=0.1)
        if b>=1: add(hat()*0.12,tb+beat/2,pan=0.3); add(hat()*0.06,tb+beat*0.75,pan=-0.3)
        # plucky bass on offbeats
        if b>=1:
            tt=T(beat*0.45); bs=np.sin(2*np.pi*nf(bass[b%4]+12)*tt); bs=np.tanh(2*bs)*np.exp(-tt*7)
            add(lp(bs,600)*0.22,tb+beat/2)
    # bell arp every other bar
    if b%2==1:
        for i,n in enumerate([ch[4]+12,ch[2]+12,ch[3]+12,ch[1]+24]):
            add(verb(bell(nf(n),0.9,decay=5)*0.05,0.8,0.4),t0+i*beat*0.5+2*beat,pan=(-1)**i*0.4)
M=norm(M,-3); sf.write(f"{out}/music.wav",M.astype(np.float32),SR); print('music', round(L/SR,1),'s @',BPM,'bpm')
