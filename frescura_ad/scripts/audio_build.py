# Synth SFX + luxury groove BGM, then mix with studio voice -> final_mix.wav
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve
SR=48000; rng=np.random.default_rng(11); W='work/'
def t(d): return np.arange(int(d*SR))/SR
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],btype='band',fs=SR,output='sos'),x,axis=0)
def lp(x,f,o=2): return sosfilt(butter(o,f,btype='low',fs=SR,output='sos'),x,axis=0)
def hp(x,f,o=2): return sosfilt(butter(o,f,btype='high',fs=SR,output='sos'),x,axis=0)
def nrm(x,db=-1): return x/(np.max(np.abs(x))+1e-9)*10**(db/20)
def st(x,w=0.0):
    d=int(0.008*SR*w); R=np.concatenate([np.zeros(d),x])[:len(x)] if d else x
    return np.stack([x,R],1)
# small room reverb IR
irt=t(1.6); IR=rng.standard_normal(len(irt))*np.exp(-irt*4.2); IR=lp(IR,6000); IR[0]=0
def verb(x,mix=0.25):
    if x.ndim==1: x=st(x)
    y=np.stack([fftconvolve(x[:,c],IR)[:len(x)] for c in range(2)],1)
    y=nrm(y,-1)*np.max(np.abs(x))
    return x*(1-mix)+y*mix
def bell(f,d,dec=6,parts=((1,1),(2.0,.35),(3.01,.18),(4.2,.08))):
    tt=t(d); return sum(a*np.sin(2*np.pi*f*m*tt)*np.exp(-dec*m**.5*tt) for m,a in parts)*np.minimum(1,tt/0.002)
def whoosh(d=0.6,lo=250,hi=5000):
    n=rng.standard_normal(int(d*SR)); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        p=i/len(n); fc=lo+(hi-lo)*np.sin(np.pi*p)**2
        y[i:i+seg]=bp(n[i:i+seg],fc*0.6,min(fc*1.7,20000))
    tt=t(d); env=np.sin(np.pi*np.clip(tt/d,0,1))**3; x=y*env
    return np.stack([x*(1.2-tt/d),x*(0.2+tt/d)],1)
def impact(d=1.6):
    tt=t(d); f=55*np.exp(-tt*3)+32; ph=2*np.pi*np.cumsum(f)/SR
    sub=np.sin(ph)*np.exp(-tt*2.8)
    cl=lp(rng.standard_normal(len(tt)),2500)*np.exp(-tt*25)*0.6
    return verb(st(sub+cl),0.18)
def riser(d=1.0):
    tt=t(d); n=rng.standard_normal(len(tt)); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        p=i/len(n); fc=400+7000*p**2; y[i:i+seg]=bp(n[i:i+seg],fc*.7,min(fc*1.4,20000))
    tone=np.sin(2*np.pi*np.cumsum(200+900*(tt/d)**2)/SR)*0.25
    return st((y+tone)*(tt/d)**2.2)
def shimmer(d=1.4,n=18,lo=2200,hi=6500):
    x=np.zeros(int(d*SR)+SR//2)
    for k in range(n):
        o=int(rng.uniform(0,d*0.75)*SR); b=bell(rng.uniform(lo,hi),0.45,dec=11,parts=((1,1),(2.01,.25)))
        x[o:o+len(b)]+=b*rng.uniform(.35,1)
    return verb(st(hp(x,1500),1.3),0.35)
def tick():
    tt=t(0.09); x=np.sin(2*np.pi*2400*tt)*np.exp(-tt*90)+hp(rng.standard_normal(len(tt)),3000)*np.exp(-tt*200)*.4
    return st(x)
def pop():
    tt=t(0.14); f=1100*np.exp(-tt*28)+220; x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*36); return st(x)
def bubbles(d=0.8,n=14):
    x=np.zeros(int(d*SR)+SR//4)
    for k in range(n):
        o=int(rng.uniform(0,d)*SR); L=int(0.05*SR); tt=np.arange(L)/SR; f0=rng.uniform(500,1600)
        b=np.sin(2*np.pi*np.cumsum(f0*(1+tt*14))/SR)*np.exp(-tt*70); x[o:o+L]+=b*rng.uniform(.3,1)
    return st(x,0.8)
def squish(d=0.55):
    tt=t(d); n=rng.standard_normal(len(tt)); y=bp(n,600,4500)*(np.sin(np.pi*tt/d)**1.5)
    am=0.6+0.4*np.sin(2*np.pi*38*tt); b=bubbles(d,10)[:len(tt)]; return st(y*am*0.8)[:len(b)]+b*0.6
def click():
    tt=t(0.05); x=hp(rng.standard_normal(len(tt)),2000)*np.exp(-tt*300)+np.sin(2*np.pi*1500*tt)*np.exp(-tt*120)*.5; return st(x)
def kaching():
    x=np.zeros(int(1.6*SR)); 
    c=click()[:,0]; x[:len(c)]+=c
    for i,f in enumerate([2093,2637,3136]):
        b=bell(f,1.3,dec=4); o=int((0.08+i*0.05)*SR); x[o:o+len(b)]+=b*.6
    return verb(st(x,1),0.25)
def stamp():
    tt=t(0.7); th=np.sin(2*np.pi*np.cumsum(90*np.exp(-tt*10)+45)/SR)*np.exp(-tt*9)
    sl=lp(rng.standard_normal(len(tt)),1800)*np.exp(-tt*40)
    return verb(st(th+sl*.8),0.2)
def glass(): return verb(st(bell(2637,1.6,dec=3.2)+0.5*bell(3951,1.6,dec=4)),0.4)
def swish(d=0.35): return whoosh(d,1500,9000)
SFX=dict(whoosh=whoosh,impact=impact,riser=riser,shimmer=shimmer,tick=tick,pop=pop,bubbles=bubbles,squish=squish,
         click=click,kaching=kaching,stamp=stamp,glass=glass,swish=swish)
bank={k:nrm(np.atleast_2d(f()) if False else f(),-1) for k,f in SFX.items()}
for k,v in bank.items():
    if v.ndim==1: bank[k]=st(v)

# ---------------- BGM: 120bpm luxury deep-house groove ----------------
BPM=120; beat=60/BPM; DUR=40.0; N=int(DUR*SR); mus=np.zeros((N,2))
def add(buf,x,at,g=1.0):
    i=int(at*SR); 
    if i>=len(buf): return
    x=x if x.ndim==2 else st(x); L=min(len(x),len(buf)-i); buf[i:i+L]+=x[:L]*g
def kick():
    tt=t(0.45); f=120*np.exp(-tt*28)+46; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*7)*np.minimum(1,tt/0.001)
def hat(o=False):
    d=0.22 if o else 0.05; tt=t(d); return hp(rng.standard_normal(len(tt)),7500)*np.exp(-tt*(18 if o else 90))
def clap():
    tt=t(0.25); n=bp(rng.standard_normal(len(tt)),900,5000); env=np.exp(-tt*22)
    for o in (0.0,0.012,0.024): env+=np.exp(-np.clip(tt-o,0,None)*200)*(tt>=o)*.6
    return n*env
def note(m): return 440*2**((m-69)/12)
def pad(ms,d):
    tt=t(d); x=np.zeros(len(tt))
    for m in ms:
        for det in (-0.08,0.0,0.08):
            ph=2*np.pi*note(m)*(1+det/100)*tt; x+= (2*((ph/(2*np.pi))%1)-1)*0.33
    x=lp(x,1800); env=np.minimum(1,tt/0.25)*np.minimum(1,(d-tt)/0.3); return x*env
def pluck(m,d=0.3):
    tt=t(d); x=np.sin(2*np.pi*note(m)*tt)+0.3*np.sin(2*np.pi*2*note(m)*tt); return x*np.exp(-tt*12)
def bass(m,d):
    tt=t(d); x=np.sin(2*np.pi*note(m)*tt)+0.15*np.sin(2*np.pi*2*note(m)*tt); return x*np.minimum(1,tt/0.01)*np.minimum(1,(d-tt)/0.03)
# Fm9 - Dbmaj7 - Abmaj7 - Ebsus  (warm, night-luxury)
prog=[([53,56,60,63,67],41),([49,53,56,60,65],37),([44,48,51,55,60],32),([51,55,58,61,63],39)]
bar=4*beat; nb=int(DUR/bar)+1
D=np.zeros((N,2)); P=np.zeros((N,2)); B=np.zeros((N,2)); L=np.zeros((N,2))
for b in range(nb):
    t0=b*bar; ch,root=prog[b%4]
    add(P,st(pad(ch,bar),1.5),t0,0.12)
    for k in range(8):
        tb=t0+k*beat/2
        if k%2==0: add(B,bass(root,beat*0.42),tb+beat/2,0.0)
    for k in range(4):
        add(B,bass(root,beat*0.4),t0+k*beat+beat/2,0.30)
    for k in range(4):
        tb=t0+k*beat
        if t0>=0.0: add(D,st(kick()),tb,0.55)
        add(D,st(hat(True),0.5),tb+beat/2,0.10)
        if k in (1,3): add(D,st(clap(),0.7),tb,0.22)
        for s in range(4): add(D,st(hat(False),0.3),tb+s*beat/4,0.05 if s%2 else 0.03)
    arp=[ch[1],ch[3],ch[2]+12,ch[4],ch[3]+12,ch[2],ch[4],ch[1]+12]
    for k,m in enumerate(arp): add(L,st(pluck(m+12),1.2),t0+k*beat/2,0.06)
L=verb(L,0.4); P=verb(P,0.3)
mus=D+P+B+L
tt=np.arange(N)/SR
# intro: drums drop out under hook first 0.35s, outro fade
mus*=np.clip(tt/0.05,0,1)[:,None]; mus*=np.clip((DUR-tt)/1.2,0,1)[:,None]
# breakdown (filter) during urgency 33.6-37.5 handled by gain lift later
mus=nrm(mus,-3)

# ---------------- Voice ----------------
VO=0.4
v,sr=sf.read(W+'voice_studio.wav'); assert sr==SR
voice=np.zeros((N,2)); add(voice,st(v),VO,1.0)
# duck music under voice (envelope follower)
env=np.abs(voice[:,0]); win=int(0.12*SR); env=np.convolve(env,np.ones(win)/win,mode='same')
duck=1-0.55*np.clip(env/0.05,0,1)
mus*=duck[:,None]

# ---------------- SFX placement ----------------
CUES=[(0.00,'impact',-4),(0.00,'shimmer',-12),(0.58,'whoosh',-10),(1.38,'swish',-11),(2.90,'swish',-9),(3.12,'whoosh',-13),
(4.50,'impact',-9),(4.55,'shimmer',-10),(5.80,'whoosh',-9),(5.86,'tick',-8),(7.52,'tick',-8),(8.90,'tick',-8),
(11.05,'whoosh',-10),(11.10,'pop',-10),(12.52,'impact',-8),(12.58,'shimmer',-12),(14.05,'whoosh',-9),
(16.0,'riser',-10),(17.05,'impact',-6),(17.08,'shimmer',-7),(18.10,'whoosh',-9),(18.25,'glass',-11),
(20.45,'whoosh',-9),(20.55,'bubbles',-7),(21.30,'click',-6),(21.34,'squish',-5),(21.52,'click',-7),(21.56,'squish',-6),
(22.05,'pop',-9),(22.20,'pop',-10),(22.35,'pop',-11),(22.66,'whoosh',-9),(24.20,'impact',-10),(24.22,'swish',-9),
(25.06,'swish',-9),(25.08,'impact',-11),(25.82,'pop',-9),(26.42,'pop',-9),(26.96,'whoosh',-9),(29.10,'shimmer',-9),
(29.85,'whoosh',-9),(31.76,'click',-5),(31.80,'pop',-8),(32.10,'pop',-9),(33.10,'click',-5),(33.14,'kaching',-6),
(33.56,'whoosh',-9),(33.60,'impact',-8)]+[(33.9+i*0.24,'tick',-15+i*0.6) for i in range(8)]+[
(35.88,'stamp',-4),(37.22,'stamp',-6),(37.26,'shimmer',-8),(37.50,'whoosh',-8),(37.55,'impact',-7),(38.95,'click',-7),(39.0,'kaching',-9)]
fx=np.zeros((N,2))
for at,k,db in CUES: add(fx,bank[k],at,10**((db+3)/20))   # +3 dB: louder SFX per brief
mix=voice*1.0+mus*10**(-5/20)+fx*0.9
# gentle bus glue + limiter-ish soft clip
peak=np.max(np.abs(mix)); mix=mix/peak*0.98
sf.write(W+'final_mix_pre.wav',mix.astype(np.float32),SR,subtype='FLOAT')
sf.write(W+'bgm.wav',(mus*10**(-5/20)).astype(np.float32),SR,subtype='FLOAT')
sf.write(W+'sfx.wav',(fx*0.9).astype(np.float32),SR,subtype='FLOAT')
print('ok',N/SR)
