# Modern luxury SFX kit + music bed, all synthesized (no external samples).
import numpy as np, soundfile as sf, sys
from scipy.signal import butter, sosfilt, fftconvolve
SR=48000; out=sys.argv[1]; rng=np.random.default_rng(11)
T=lambda d: np.arange(int(d*SR))/SR
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],btype='band',fs=SR,output='sos'),x,axis=0)
def hp(x,f,o=2): return sosfilt(butter(o,f,btype='high',fs=SR,output='sos'),x,axis=0)
def lp(x,f,o=2): return sosfilt(butter(o,f,btype='low',fs=SR,output='sos'),x,axis=0)
def norm(x,db=-1): return x/(np.max(np.abs(x))+1e-9)*10**(db/20)
def st(x,w=0.0):
    d=int(w*SR); R=np.roll(x,d) if d else x; return np.stack([x,R],1)
def verb(x,dec=1.2,mix=0.25):  # cheap stereo reverb (noise-convolution)
    n=int(dec*SR); tt=np.arange(n)/SR; ir=rng.standard_normal((n,2))*np.exp(-tt*6/dec)[:,None]; ir=lp(ir,7000)
    y=np.stack([fftconvolve(x[:,c],ir[:,c])[:len(x)+n] for c in (0,1)],1)*0.08; y=np.vstack([y,np.zeros((len(x)+n-len(y),2))])
    xx=np.vstack([x,np.zeros((n,2))]); return xx*(1-mix)+norm(y,-6)*mix*np.max(np.abs(x))
def swoosh(d=0.55,lo=400,hi=6000):
    n=rng.standard_normal(int(d*SR)); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        p=i/len(n); fc=lo*(hi/lo)**(np.sin(np.pi*p*0.9)); y[i:i+seg]=bp(n[i:i+seg],fc*0.7,min(fc*1.5,20000))
    tt=T(d); env=(tt/d)**1.5*np.exp(-((tt/d-0.62)**2)/0.05); y*=env
    return np.stack([y*(1-tt/d)+.3*y,y*(tt/d)+.3*y],1)
def impact(d=1.6):  # sub boom + transient
    tt=T(d); f=55+90*np.exp(-tt*18); ph=2*np.pi*np.cumsum(f)/SR
    sub=np.sin(ph)*np.exp(-tt*2.6); click=hp(rng.standard_normal(len(tt)),2500)*np.exp(-tt*80)*0.5
    x=np.tanh(1.6*(sub+click)); return verb(st(x,0.004),1.4,0.3)
def riser(d=1.4):
    tt=T(d); n=rng.standard_normal(len(tt)); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        fc=300*(20)**(i/len(n)); y[i:i+seg]=bp(n[i:i+seg],fc*.8,min(fc*1.3,19000))
    tone=np.sin(2*np.pi*np.cumsum(200*(4)**(tt/d))/SR)*0.25
    x=(y+tone)*(tt/d)**2.2; return st(x,0.008)
def tick(f=3200):  # glassy UI tick
    tt=T(0.09); x=np.sin(2*np.pi*f*tt)*np.exp(-tt*70)+0.4*np.sin(2*np.pi*f*2.7*tt)*np.exp(-tt*120)
    return st(x)
def ping(f=1567.98):  # luxury crystal ping
    tt=T(1.6); x=sum(a*np.sin(2*np.pi*f*m*tt)*np.exp(-tt*(2.2*m**.6)) for m,a in ((1,1),(2.0,.35),(2.76,.18),(5.4,.06)))
    x*=np.minimum(1,tt/0.002); return verb(st(x,0.006),1.6,0.35)
def shimmer(d=1.2,n=22):
    x=np.zeros(int((d+.5)*SR))
    for k in range(n):
        o=int(rng.uniform(0,d)*SR); f=rng.choice([2093,2637,3136,3520,4186])*rng.uniform(.995,1.005); tt=T(.4)
        b=np.sin(2*np.pi*f*tt)*np.exp(-tt*12)*rng.uniform(.3,1); x[o:o+len(b)]+=b
    return verb(np.stack([x,np.roll(x,500)],1),1.2,0.4)
def bubbles(d=1.4,n=26):  # foam bubble pops
    x=np.zeros(int((d+.2)*SR))
    for k in range(n):
        o=int(rng.uniform(0,d)*SR); tt=T(.05); f0=rng.uniform(500,1400)
        b=np.sin(2*np.pi*np.cumsum(f0*(1+tt*30))/SR)*np.exp(-tt*90)*rng.uniform(.3,1); x[o:o+len(b)]+=b
    return st(x,0.003)
def shutter():
    tt=T(.18); n=hp(rng.standard_normal(len(tt)),1500)
    x=n*(np.exp(-tt*120)+0.7*np.exp(-np.maximum(tt-.07,0)*150)*(tt>.07)); return st(x)
def tape_stop(d=0.5):
    tt=T(d); f=220*(1-tt/d)**2+20; x=np.sign(np.sin(2*np.pi*np.cumsum(f)/SR))*0.4; x=lp(x,1800)*(1-tt/d); return st(x)
def pop():
    tt=T(.12); f=1000*np.exp(-tt*35)+200; x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*45); return st(x)
kit=dict(swoosh=swoosh(),swoosh_fast=swoosh(0.32,600,9000),impact=impact(),riser=riser(),tick=tick(),tick_lo=tick(2100),
         ping=ping(),ping_hi=ping(2093),shimmer=shimmer(),bubbles=bubbles(),shutter=shutter(),tape_stop=tape_stop(),pop=pop())
for k,v in kit.items(): sf.write(f"{out}/{k}.wav",norm(v,-1).astype(np.float32),SR)
# ---- music bed: 120 BPM minimal luxury house (kick, offbeat hats, clap, sub bass, warm pad) ----
bpm=120; beat=60/bpm; bars=24; L=int(bars*4*beat*SR)+SR; mus=np.zeros((L,2))
def put(sig,t0,g=1.0):
    i=int(t0*SR); j=min(L,i+len(sig)); mus[i:j]+=sig[:j-i]*g
tt=T(.45); kick=np.sin(2*np.pi*np.cumsum(48+130*np.exp(-tt*28))/SR)*np.exp(-tt*7); kick=st(np.tanh(2*kick))
th=T(.06); hat=st(hp(rng.standard_normal(len(th)),8000)*np.exp(-th*70))
tc=T(.25); clap=hp(rng.standard_normal(len(tc)),1200)*(np.exp(-tc*30)); clap=verb(st(clap,0.01),0.6,0.4)
prog=[(43.65,[174.6,207.7,261.6]),(36.71,[146.8,174.6,220.0]),(41.2,[164.8,207.7,246.9]),(32.70,[130.8,164.8,196.0])]  # Fm Dm Em(ish) C - moody
for b in range(bars):
    t0=b*4*beat; root,ch=prog[(b//2)%4]
    for q in range(4):
        tq=t0+q*beat
        if b>=1: put(kick,tq,0.9)
        put(hat,tq+beat/2,0.35 if b>=1 else 0.2)
        if q in (1,3) and b>=2: put(clap,tq,0.30)
        if b>=1:
            ts=T(beat*0.9); sb=np.sin(2*np.pi*root*ts)*np.minimum(1,ts/.01)*np.exp(-ts*1.5); put(st(sb),tq+beat*0.5,0.55)
    tp=T(4*beat); pad=sum(np.sin(2*np.pi*f*tp*d) for f in ch for d in (1,1.004))/6
    pad*=np.minimum(1,tp/0.4)*np.minimum(1,(4*beat-tp)/0.4); put(st(lp(pad,2500),0.012),t0,0.25)
    for s in range(8):  # pluck arp
        f=ch[s%3]*2; tpl=T(.3); pl=np.sin(2*np.pi*f*tpl)*np.exp(-tpl*14); put(st(pl,0.015),t0+s*beat/2,0.10 if b>=2 else 0.05)
mus=verb(mus,1.0,0.15); sf.write(f"{out}/music.wav",norm(mus,-3).astype(np.float32),SR)
print("ok", list(kit), "music", len(mus)/SR)
