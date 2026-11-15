import numpy as np, soundfile as sf, sys
from scipy.signal import butter, sosfilt
SR=48000; DUR=30.5; N=int(DUR*SR); rng=np.random.default_rng(11)
W=sys.argv[1]; OUT=sys.argv[2]
def t(d): return np.arange(int(d*SR))/SR
def lp(x,f,o=2): return sosfilt(butter(o,f,'low',fs=SR,output='sos'),x,axis=0)
def hp(x,f,o=2): return sosfilt(butter(o,f,'high',fs=SR,output='sos'),x,axis=0)
def bp(x,a,b,o=2): return sosfilt(butter(o,[a,b],'band',fs=SR,output='sos'),x,axis=0)
def place(buf,x,at,g=1.0,pan=0.0):
    if x.ndim==1: x=np.stack([x*np.sqrt((1-pan)/2)*1.414, x*np.sqrt((1+pan)/2)*1.414],1)
    i=int(at*SR); j=min(N,i+len(x));
    if i<N: buf[i:j]+=x[:j-i]*g
mtof=lambda m:440*2**((m-69)/12)
# ---------------- MUSIC ----------------
BPM=60/0.5225; B=0.5225; T0=1.5   # downbeats at 1.5 + 4kB ; drop at 11.95
mus=np.zeros((N,2))
def kick():
    tt=t(0.42); f=48+110*np.exp(-tt*28); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-tt*7.5)*1.0 + 0.25*np.exp(-tt*300)*rng.standard_normal(len(tt))*0.3
def clap():
    x=np.zeros(int(0.3*SR))
    for o in (0,0.011,0.022):
        L=int(0.25*SR); n=rng.standard_normal(L)*np.exp(-np.arange(L)/SR*(60 if o==0.022 else 180)); i=int(o*SR); x[i:i+L]+=n[:len(x)-i]
    return bp(x,900,5000)*0.6
def hat(open_=False):
    d=0.22 if open_ else 0.05; tt=t(d); return hp(rng.standard_normal(len(tt)),7000)*np.exp(-tt*(14 if open_ else 90))*0.35
def shaker(): tt=t(0.07); return hp(rng.standard_normal(len(tt)),5000)*np.sin(np.pi*tt/0.07)**2*0.12
def epiano(m,d,v=0.25):
    tt=t(d); f=mtof(m); x=np.zeros(len(tt))
    for k,a in ((1,1),(2,.35),(3,.12),(4,.06)): x+=a*np.sin(2*np.pi*f*k*tt+0.3*np.sin(2*np.pi*f*tt)*np.exp(-tt*3))*np.exp(-tt*(1.4+k*0.8))
    return x*np.minimum(1,tt/0.004)*v
def pad(ms,d,v=0.05):
    tt=t(d); x=np.zeros((len(tt),2))
    for m in ms:
        for det,ch in ((-0.08,0),(0.08,1),(0,0),(0,1)):
            f=mtof(m+det); saw=2*((f*tt+rng.random())%1)-1; x[:,ch]+=saw
    x=lp(x,1800); env=np.minimum(1,tt/0.6)*np.minimum(1,(d-tt)/0.5); return x*env[:,None]*v
def sub(m,d,v=0.5):
    tt=t(d); return np.sin(2*np.pi*mtof(m)*tt)*np.minimum(1,tt/0.01)*np.minimum(1,(d-tt)/0.05)*v
# progression per bar: Am9, Fmaj9, Cmaj9/E, G6  (luxe minor)
prog=[(45,[57,60,64,67,71]),(41,[57,60,64,65,69]),(40,[55,59,60,64,67]),(43,[55,59,62,64,67])]
bar=4*B
# intro pad 0..1.5 (anacrusis) + hook
mus_pad=np.zeros((N,2))
place(mus_pad,pad([57,60,64,71],1.9,0.06),-0.0)
nb=int((DUR-T0)/bar)+1
for b in range(nb):
    s=T0+b*bar; root,ch=prog[b%4]
    if s>=DUR: break
    place(mus_pad,pad(ch[1:],bar+0.3,0.045),s)
    drop = s>=11.95-1e-3
    ending = s>=28.0
    # epiano rhythmic stabs (offbeat syncopation)
    for k,o in enumerate([0,1.5,2.5,3.5] if drop else [0,2.5]):
        for m in ch[:4]: place(mus,epiano(m,0.9,0.11 if drop else 0.08),s+o*B,pan=(-0.3 if k%2 else 0.3))
    # bass pattern
    for o,dd in ([(0,0.45),(0.75,0.2),(1.5,0.4),(2.5,0.3),(3,0.45)] if drop else [(0,0.9),(2,0.9)]):
        place(mus,sub(root+(12 if o==0.75 else 0),dd*B*2,0.32),s+o*B)
    for q in range(4):
        bt=s+q*B
        if bt>=DUR-0.3: continue
        if not ending or q<2: place(mus,kick(),bt,0.85)
        if q in (1,3): place(mus,clap(),bt,0.55 if drop else 0.4)
        place(mus,hat(True),bt+B/2,0.5 if drop else 0.3,pan=0.2)
        for e in range(4): place(mus,shaker(),bt+e*B/4,0.9 if drop else 0.6,pan=-0.4+0.25*e)
# breakdown before drop: thin out 10.9-11.95 (filter) handled by gain env
mus+=mus_pad
env=np.ones(N); tt=np.arange(N)/SR
env[(tt>10.9)&(tt<11.95)]=0.35
env*=np.clip((DUR-tt)/1.6,0,1)
mus*=env[:,None]
# sidechain-ish duck under voice
v,_=sf.read(W+'/voice_edit.wav'); v=v if v.ndim==1 else v.mean(1); v=np.pad(v,(0,max(0,N-len(v))))[:N]
e=np.sqrt(np.clip(lp(v**2,6),0,None)); e=e/np.max(e); duck=1-0.55*np.clip(e*3,0,1)
mus*=duck[:,None]
# ---------------- SFX ----------------
sfx=np.zeros((N,2))
def whoosh(d=0.5,lo=300,hi=4500,rev=False):
    n=rng.standard_normal(int(d*SR)); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        p=i/len(n); p=1-p if rev else p; fc=lo+(hi-lo)*np.sin(np.pi*p/1)**2 if False else lo*(hi/lo)**p
        y[i:i+seg]=bp(n[i:i+seg],max(60,fc*0.6),min(20000,fc*1.5))
    tt=t(d); env=np.sin(np.pi*tt/d)**1.5; x=y*env
    return np.stack([x*(1-tt/d)+0.3*x, x*(tt/d)+0.3*x],1)
def boom(d=1.6):
    tt=t(d); f=38+70*np.exp(-tt*9); x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*2.6)
    x+=lp(rng.standard_normal(len(tt)),900)*np.exp(-tt*14)*0.6
    return np.tanh(x*1.6)
def riser(d=1.0):
    tt=t(d); n=rng.standard_normal(len(tt)); y=np.zeros_like(n)
    for i in range(0,len(n),512): p=i/len(n); fc=400*(12)**p; y[i:i+512]=bp(n[i:i+512],fc*0.7,min(fc*1.4,20000))
    tone=np.sin(2*np.pi*np.cumsum(200*4**(tt/d))/SR)*0.25
    return (y+tone)*(tt/d)**2.2
def shimmer(d=1.2,n=22,lo=2500,hi=7500):
    x=np.zeros((int(d*SR)+SR//2,2))
    for k in range(n):
        o=int((k/n)*d*0.8*SR); f=lo*(hi/lo)**(k/n); tt=t(0.45)
        b=(np.sin(2*np.pi*f*tt)+0.3*np.sin(2*np.pi*f*2.01*tt))*np.exp(-tt*10); p=rng.uniform(-.8,.8)
        x[o:o+len(b),0]+=b*(1-p)/2; x[o:o+len(b),1]+=b*(1+p)/2
    return x
def tick(f=2400):
    tt=t(0.04); return np.sin(2*np.pi*f*tt)*np.exp(-tt*160)
def pop():
    tt=t(0.11); f=1000*np.exp(-tt*35)+200; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*45)
def ding(f=1760):
    tt=t(1.4); return sum(a*np.sin(2*np.pi*f*m*tt)*np.exp(-tt*(3+2*m)) for m,a in ((1,1),(2.76,.3),(5.4,.12)))
def foam(d=0.9):
    x=np.zeros(int(d*SR))
    for k in range(70):
        o=int(rng.uniform(0,d-0.05)*SR); tt=t(0.03); f=rng.uniform(600,2600)
        b=np.sin(2*np.pi*f*tt*(1+tt*20))*np.exp(-tt*170); x[o:o+len(b)]+=b*rng.uniform(.2,1)
    sq=lp(rng.standard_normal(len(x)),1200)*np.sin(np.pi*np.arange(len(x))/len(x))*0.6
    return x*0.5+sq
def pumpclick():
    tt=t(0.12); x=bp(rng.standard_normal(len(tt)),1500,6000)*np.exp(-tt*120); x+=np.sin(2*np.pi*180*tt)*np.exp(-tt*50)*0.6; return x
def swish(): return whoosh(0.28,1200,9000)*0.8
def cash():
    x=np.zeros(int(1.2*SR)); a=ding(2637); b=ding(3520); x[:len(a)]+=a[:len(x)]*.6; i=int(.07*SR); x[i:]+=b[:len(x)-i]*.5; return x
def tape_stop(): # for "strike" effect
    tt=t(0.35); f=900*np.exp(-tt*8); return np.sign(np.sin(2*np.pi*np.cumsum(f)/SR))*np.exp(-tt*6)*0.15
EV=[
 # hook
 (0.00,boom(),0.9),(0.00,shimmer(1.0),0.18),(0.02,whoosh(0.45,200,6000,True),0.35),
 (0.95,swish(),0.35),
 (1.50,whoosh(0.4),0.4),(1.95,pop(),0.35),(2.95,tick(),0.3),
 (3.45,whoosh(0.5,250,5000),0.35),(4.6,ding(1318),0.12),(5.55,shimmer(0.7,12),0.18),
 (6.15,swish(),0.35),(7.0,tape_stop(),0.6),(7.05,tick(1800),0.35),
 (8.25,whoosh(0.4),0.35),(9.05,pop(),0.35),(10.9,riser(1.05),0.45),
 (11.95,boom(),1.0),(11.95,shimmer(1.4,28),0.3),(11.95,ding(880),0.12),(12.7,swish(),0.25),
 (13.70,whoosh(0.45),0.4),(14.0,pumpclick(),0.6),(14.15,foam(1.2),0.35),(15.2,pop(),0.3),(15.6,pop(),0.28),(16.0,pop(),0.26),
 (17.30,whoosh(0.5,200,6000),0.45),(18.75,swish(),0.4),(18.85,ding(1568),0.12),(19.5,swish(),0.4),(19.6,ding(1175),0.12),
 (20.60,boom(1.0),0.5),(21.0,tick(),0.3),(21.3,tick(),0.3),(21.6,tick(),0.3),(21.9,tick(),0.3),
 (22.28,whoosh(0.4),0.4),(22.6,pop(),0.4),(23.3,cash(),0.22),(23.8,foam(0.9),0.25),
 (24.75,riser(0.5),0.25),(25.2,boom(1.4),0.6),(25.2,shimmer(1.6,30),0.3),(27.4,swish(),0.3),(27.6,ding(1760),0.14),(28.9,shimmer(1.0,14),0.15),
]
for at,x,g in EV: place(sfx,x/np.max(np.abs(x)),at,g)
# ---------------- MIX ----------------
vv=np.stack([v,v],1)*1.0
mix=vv*1.0 + mus*0.30 + sfx*0.75
sf.write(OUT+'/music.wav',(mus*0.30).astype(np.float32),SR)
sf.write(OUT+'/sfx.wav',(sfx*0.75).astype(np.float32),SR)
sf.write(OUT+'/mix_raw.wav',mix.astype(np.float32),SR)
print('peak',np.max(np.abs(mix)))
