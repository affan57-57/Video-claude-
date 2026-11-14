import numpy as np, soundfile as sf, sys
from scipy.signal import butter, sosfilt
SR=48000; out=sys.argv[1]; R=np.random.default_rng(11)
T=lambda d: np.arange(int(d*SR))/SR
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],btype='band',fs=SR,output='sos'),x,axis=0)
def lp(x,f,o=2): return sosfilt(butter(o,f,btype='low',fs=SR,output='sos'),x,axis=0)
def hp(x,f,o=2): return sosfilt(butter(o,f,btype='high',fs=SR,output='sos'),x,axis=0)
def st(x,w=0.0):
    d=int(w*SR); return np.stack([x,np.roll(x,d)],1)
def norm(x,db=-1): return x/np.max(np.abs(x))*10**(db/20)
def bell(f,d,decay=6,parts=((1,1),(2.0,.35),(3.01,.18),(4.2,.08))):
    t=T(d); return sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-decay*m**.5*t) for m,a in parts)*np.minimum(1,t/0.002)
def whoosh(d=0.55,lo=250,hi=5200):
    n=R.standard_normal(int(d*SR)); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        p=i/len(n); fc=lo+(hi-lo)*np.sin(np.pi*min(1,p*1.1))**2
        y[i:i+seg]=sosfilt(butter(2,[fc*.6,min(fc*1.7,23000)],btype='band',fs=SR,output='sos'),n[i:i+seg])
    t=T(d); e=np.sin(np.pi*t/d)**1.5; x=y*e
    return np.stack([x*(1-t/d)+.3*x, x*(t/d)+.3*x],1)
def impact():
    t=T(1.6); f=70*np.exp(-t*3)+38; ph=2*np.pi*np.cumsum(f)/SR
    sub=np.sin(ph)*np.exp(-t*2.6); n=lp(R.standard_normal(len(t)),900)*np.exp(-t*14)*.6
    c=hp(R.standard_normal(len(t)),3000)*np.exp(-t*60)*.25
    return st(np.tanh(1.6*(sub+n+c)),0.006)
def riser(d=1.2):
    t=T(d); n=R.standard_normal(len(t)); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        p=i/len(n); fc=300+6000*p**2
        y[i:i+seg]=sosfilt(butter(2,[fc*.7,fc*1.5],btype='band',fs=SR,output='sos'),n[i:i+seg])
    tone=np.sin(2*np.pi*np.cumsum(220+660*(t/d)**2)/SR)*.25
    return st((y+tone)*(t/d)**2,0.009)
def pop():
    t=T(0.14); f=1100*np.exp(-t*35)+250; x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*38); return st(x)
def tick():
    t=T(0.06); x=bp(R.standard_normal(len(t)),2500,7000)*np.exp(-t*120)+np.sin(2*np.pi*1800*t)*np.exp(-t*90)*.5; return st(x)
def ding(f=1568): return st(bell(f,1.4,4)+.5*bell(f*1.5,1.4,6),0.004)
def sparkle(d=1.3,n=18):
    x=np.zeros(int((d+.5)*SR))
    for k in range(n):
        o=int(R.uniform(0,d*.8)*SR); b=bell(R.uniform(2600,6500),.4,14,((1,1),(2.01,.3))); x[o:o+len(b)]+=b*R.uniform(.3,1)
    return st(hp(x,1500),0.011)
def bubbles(d=1.4,n=22):
    x=np.zeros(int((d+.2)*SR))
    for k in range(n):
        o=int(R.uniform(0,d)*SR); L=int(R.uniform(.03,.07)*SR); t=np.arange(L)/SR
        f0=R.uniform(500,1400); f=f0*(1+t*R.uniform(8,20)); b=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*60)*np.minimum(1,t/0.003)
        x[o:o+L]+=b*R.uniform(.3,1)
    x+=lp(R.standard_normal(len(x)),2500)*.04*np.sin(np.pi*np.arange(len(x))/len(x))
    return st(x,0.007)
def chaching():
    x=np.zeros(int(1.6*SR)); a=bell(2093,1.2,5); b=bell(2637,1.4,4.5)
    x[:len(a)]+=a; o=int(.09*SR); x[o:o+len(b)]+=b
    c=bp(R.standard_normal(int(.08*SR)),3000,9000)*np.exp(-np.arange(int(.08*SR))/SR*60); x[:len(c)]+=c*.8
    return st(x,0.005)
def shimmer(d=2.2):
    t=T(d); x=sum(np.sin(2*np.pi*f*t+R.uniform(0,6))*a for f,a in [(880,1),(1318.5,.7),(1760,.5),(2637,.3)])
    e=np.minimum(1,t/.4)*np.exp(-t*1.4); return st(x*e*(1+.3*np.sin(2*np.pi*6*t)),0.013)
def boom_soft():
    t=T(1.2); f=55*np.exp(-t*2)+40; x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*3); return st(x)
for name,fn in dict(whoosh=whoosh,whoosh_s=lambda:whoosh(.35,600,7000),whoosh_l=lambda:whoosh(.9,150,4000),impact=impact,riser=riser,pop=pop,tick=tick,ding=ding,ding2=lambda:ding(2093),sparkle=sparkle,bubbles=bubbles,chaching=chaching,shimmer=shimmer,boom=boom_soft).items():
    y=norm(fn()); sf.write(f"{out}/{name}.wav",y.astype(np.float32),SR)

# ---- music bed: 122 BPM luxury deep-house groove ----
BPM=122; beat=60/BPM; D=40.0; N=int(D*SR); m=np.zeros((N,2))
def add(x,t0,g=1.0):
    i=int(t0*SR); 
    if i>=N: return
    x=x if x.ndim==2 else st(x); L=min(len(x),N-i); m[i:i+L]+=x[:L]*g
def kick():
    t=T(.45); f=120*np.exp(-t*28)+48; return np.tanh(1.4*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7))
def hat(o=False):
    t=T(.25 if o else .06); return hp(R.standard_normal(len(t)),7000)*np.exp(-t*(18 if o else 90))
def clap():
    t=T(.3); n=bp(R.standard_normal(len(t)),900,5000); e=np.exp(-t*22)
    for k in (0.0,.011,.022): e+=np.exp(-np.maximum(0,t-k)*200)*(t>=k)*.6
    return n*e*.7
def mtof(n): return 440*2**((n-69)/12)
chords=[[57,60,64,67,71],[53,57,60,64,67],[48,55,59,64,67],[55,59,62,64,69]]  # Am9 Fmaj9 Cmaj7 G6/9
bass=[45,41,36,43]
def pad(notes,d):
    t=T(d); x=np.zeros(len(t))
    for n in notes:
        for dt in (-0.08,0.08):
            f=mtof(n)*2**(dt/12); x+=np.sign(np.sin(2*np.pi*f*t))*.15+np.sin(2*np.pi*f*t)
    x=lp(x,1800); e=np.minimum(1,t/.25)*np.minimum(1,(d-t)/.3); return x*e
def pluck(n,d=.35):
    t=T(d); f=mtof(n); x=(np.sin(2*np.pi*f*t)+.4*np.sin(4*np.pi*f*t))*np.exp(-t*9); return x
def bassn(n,d):
    t=T(d); f=mtof(n); x=np.tanh(2*np.sin(2*np.pi*f*t))*np.minimum(1,t/.01)*np.exp(-t*2.5); return lp(x,500)
bar=4*beat; nb=int(D/bar)+1
for b in range(nb):
    t0=b*bar; c=b%4
    add(st(pad(chords[c],bar+.2),0.012),t0,.05)
    for k in range(4):
        tb=t0+k*beat
        if b>=1 or k>=2: add(kick(),tb,.55)
        add(hat(),tb+beat/2,.18); add(hat(),tb+beat/4,.07); add(hat(),tb+3*beat/4,.07)
        if k in (1,3) and b>=1: add(st(clap(),.004),tb,.25)
        add(bassn(bass[c],beat*.45),tb+beat/2,.3)
    arp=[0,2,4,3,1,4,2,3]
    for k in range(8):
        add(st(pluck(chords[c][arp[k]]+12),0.009),t0+k*beat/2,.06)
sf.write(f"{out}/music.wav",norm(m,-1).astype(np.float32),SR)
print('ok')
