import numpy as np, soundfile as sf, sys, json
from scipy.signal import butter, sosfilt
SR=48000; OUT=sys.argv[1]; rng=np.random.default_rng(11)
def t(d): return np.arange(int(d*SR))/SR
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],btype='band',fs=SR,output='sos'),x)
def lp(x,f,o=2): return sosfilt(butter(o,f,btype='low',fs=SR,output='sos'),x)
def hp(x,f,o=2): return sosfilt(butter(o,f,btype='high',fs=SR,output='sos'),x)
def nrm(x,db=-1): return x/(np.max(np.abs(x))+1e-9)*10**(db/20)
def st(x,w=0.0):
    d=int(0.008*SR*w); R=np.roll(x,d) if d else x; return np.stack([x,R],1)
def bell(f,d,dec=6,parts=((1,1),(2.0,.35),(3.01,.18),(4.2,.08))):
    tt=t(d); return sum(a*np.sin(2*np.pi*f*m*tt)*np.exp(-dec*m**.5*tt) for m,a in parts)*np.minimum(1,tt/0.002)
S={}
# boom: sub drop + noise transient
tt=t(1.8); f=110*np.exp(-tt*5)+38; ph=2*np.pi*np.cumsum(f)/SR
b=np.sin(ph)*np.exp(-tt*2.2); b+=0.5*lp(rng.standard_normal(len(tt)),900)*np.exp(-tt*28)
b=np.tanh(2.2*b); S['boom']=st(b)
# hit: punchy mid impact
tt=t(0.7); f=180*np.exp(-tt*18)+60; h=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*7)+0.6*bp(rng.standard_normal(len(tt)),400,5000)*np.exp(-tt*35)
S['hit']=st(np.tanh(2*h),0.5)
def whoosh(d,lo=250,hi=5000,rev=False):
    n=rng.standard_normal(int(d*SR)); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        p=i/len(n); fc=lo+(hi-lo)*np.sin(np.pi*p)**2; y[i:i+seg]=bp(n[i:i+seg],fc*0.6,min(fc*1.7,20000))
    tt=t(d); env=(tt/d)**2.5 if rev else np.sin(np.pi*tt/d)**2
    x=y*env; return np.stack([x*(1-tt/d)+.25*x, x*(tt/d)+.25*x],1)
S['whoosh']=whoosh(0.55); S['whoosh_low']=whoosh(0.9,120,2200); S['riser']=whoosh(1.2,300,9000,rev=True)
# tick / click
tt=t(0.05); S['tick']=st(np.sin(2*np.pi*2900*tt)*np.exp(-tt*160)+0.4*hp(rng.standard_normal(len(tt)),3000)*np.exp(-tt*300))
tt=t(0.09); S['tap']=st(np.sin(2*np.pi*(1400*np.exp(-tt*40)+500)*tt)*np.exp(-tt*60))
tt=t(0.14); f=1100*np.exp(-tt*28)+220; S['pop']=st(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*36))
tt=t(0.08); S['flip']=st(bp(rng.standard_normal(len(tt)),900,6000)*np.exp(-tt*70))
def shimmer(d=1.6,n=26,lo=2500,hi=7500):
    x=np.zeros(int((d+0.5)*SR))
    for k in range(n):
        o=int((k/n)**1.3*d*SR); fr=rng.uniform(lo,hi); bb=bell(fr,0.45,14,((1,1),(2.01,.3))); x[o:o+len(bb)]+=bb*rng.uniform(.4,1)*(1-k/n*0.5)
    x=hp(x,1800); return np.stack([x,np.roll(x,int(0.013*SR))],1)
S['shimmer']=shimmer(); S['sparkle']=shimmer(0.7,12,3500,8000)
x=np.zeros(int(1.6*SR)); a=bell(1568,1.2,4); x[:len(a)]+=a; bb=bell(2093,1.2,4); o=int(.09*SR); x[o:o+len(bb)]+=bb; S['ding']=st(x,1)
# cash / sale chime: three quick bells
x=np.zeros(int(1.6*SR))
for i,fr in enumerate([1318.5,1760,2637]): bb=bell(fr,1.2,5); o=int(i*0.06*SR); x[o:o+len(bb)]+=bb
S['cash']=st(x,1)
# bubble / foam squish
x=np.zeros(int(0.9*SR))
for k in range(9):
    d=rng.uniform(.04,.09); tt=t(d); f0=rng.uniform(500,1300); f=f0*(1+3*tt/d)
    bb=np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*tt/d); o=int(rng.uniform(0,.75)*SR); x[o:o+len(bb)]+=bb*rng.uniform(.5,1)
x+=0.25*lp(rng.standard_normal(len(x)),2500)*np.exp(-np.arange(len(x))/SR*4)
S['bubble']=st(x,0.6)
# strike swipe
S['swipe']=whoosh(0.3,1500,9000)
for k,v in S.items(): sf.write(f"{OUT}/{k}.wav",nrm(v).astype(np.float32),SR)
# ---------------- music: 122 BPM luxe deep-house groove ----------------
BPM=122; beat=60/BPM; L=41.0; N=int(L*SR); m=np.zeros((N,2))
def add(x,at,g=1.0):
    i=int(at*SR); 
    if i>=N: return
    if x.ndim==1: x=np.stack([x,x],1)
    e=min(N,i+len(x)); m[i:e]+=g*x[:e-i]
tt=t(0.45); kick=np.sin(2*np.pi*np.cumsum(55+120*np.exp(-tt*35))/SR)*np.exp(-tt*7); kick=np.tanh(1.6*kick)
tt=t(0.06); hat=hp(rng.standard_normal(len(tt)),7000)*np.exp(-tt*70)
tt=t(0.25); clap=sum(np.roll(bp(rng.standard_normal(len(tt)),900,4000)*np.exp(-tt*22),int(k*0.011*SR)) for k in range(3))
chords=[[53,57,60,64],[52,55,59,62],[50,53,57,60],[48,52,55,59]]  # Fmaj7 Em7 Dm7 Cmaj7
hz=lambda n:440*2**((n-69)/12)
bars=int(L/(4*beat))+1
for b in range(bars):
    t0=b*4*beat; ch=chords[b%4]
    for q in range(4):
        tb=t0+q*beat
        if tb<0.4: continue
        add(kick,tb,0.9); add(hat,tb+beat/2,0.22); add(hat,tb+beat*0.75,0.08)
        if q in(1,3): add(clap,tb,0.35)
    # pad
    d=4*beat; tt=t(d); pad=np.zeros(len(tt))
    for n in ch:
        for det in(-0.08,0.08): pad+=np.sin(2*np.pi*hz(n+12)*(1+det/100)*tt)+0.3*np.sin(2*np.pi*hz(n+24)*tt)
    pad*=np.minimum(1,tt/0.3)*np.minimum(1,(d-tt)/0.3); pad=lp(pad,2200)
    add(np.stack([pad,np.roll(pad,300)],1),t0,0.045)
    # bass (offbeat)
    for q in range(4):
        tt=t(beat*0.45); bs=np.sin(2*np.pi*hz(ch[0]-12)*tt)*np.exp(-tt*5)*np.minimum(1,tt/0.005)
        add(np.tanh(1.5*bs),t0+q*beat+beat/2,0.35)
    # pluck arp
    for s in range(8):
        n=ch[[0,2,1,3,2,0,3,1][s]]+24; tt=t(0.3); pl=np.sin(2*np.pi*hz(n)*tt)*np.exp(-tt*14)
        add(np.stack([pl*(0.6+0.4*(s%2)),pl*(1-0.4*(s%2))],1),t0+s*beat/2,0.06)
fade=np.minimum(1,np.arange(N)/SR/0.3)*np.minimum(1,(L-np.arange(N)/SR)/1.2).clip(0,1)
m*=fade[:,None]; sf.write(f"{OUT}/music.wav",nrm(m,-1).astype(np.float32),SR); print("ok")
