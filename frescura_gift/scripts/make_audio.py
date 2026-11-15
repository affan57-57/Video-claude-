# Synth SFX kit + luxury deep-house bed (deterministic)
import numpy as np, soundfile as sf, sys
from scipy.signal import butter, sosfilt
SR=48000; out=sys.argv[1]; R=np.random.default_rng(11)
T=lambda d: np.arange(int(d*SR))/SR
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],'band',fs=SR,output='sos'),x,axis=0)
def lp(x,f,o=2): return sosfilt(butter(o,f,'low',fs=SR,output='sos'),x,axis=0)
def hp(x,f,o=2): return sosfilt(butter(o,f,'high',fs=SR,output='sos'),x,axis=0)
def st(x,w=0.0):
    d=int(0.012*SR*w); return np.stack([x,np.roll(x,d)],1)
def nz(n): return R.standard_normal(n)
def norm(x,db=-1): return x/np.max(np.abs(x))*10**(db/20)
def bell(f,d,dec=5,parts=((1,1),(2.0,.35),(3.01,.15))):
    t=T(d); return sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-dec*m**.5*t) for m,a in parts)*np.minimum(1,t/0.002)
def boom(d=2.2):  # cinematic sub impact
    t=T(d); f=38+70*np.exp(-t*9); ph=2*np.pi*np.cumsum(f)/SR
    sub=np.sin(ph)*np.exp(-t*2.2); n=lp(nz(len(t)),900)*np.exp(-t*7)*0.6
    crack=hp(nz(len(t)),2500)*np.exp(-t*40)*0.5
    x=np.tanh(1.6*(sub+n+crack)); return st(x,0.6)
def whoosh(d=0.55,rev=False):
    n=nz(int(d*SR)); y=np.zeros_like(n); seg=512; t=T(d)
    for i in range(0,len(n),seg):
        p=i/len(n); fc=250+5000*np.sin(np.pi*p)**3
        y[i:i+seg]=sosfilt(butter(2,[fc*.6,min(fc*1.7,20000)],'band',fs=SR,output='sos'),n[i:i+seg])
    e=np.sin(np.pi*t/d)**2.5; x=y*e
    if rev: x=x[::-1]
    return np.stack([x*(1-t/d)+.3*x, x*(t/d)+.3*x],1)
def riser(d=1.2):
    t=T(d); n=nz(len(t)); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        fc=400+7000*(i/len(n))**2; y[i:i+seg]=sosfilt(butter(2,[fc*.7,min(fc*1.5,20000)],'band',fs=SR,output='sos'),n[i:i+seg])
    tone=np.sin(2*np.pi*np.cumsum(200+900*(t/d)**2)/SR)*0.25
    return st((y+tone)*(t/d)**2,0.5)
def tick():
    t=T(0.05); x=np.sin(2*np.pi*3200*t)*np.exp(-t*160)+hp(nz(len(t)),4000)*np.exp(-t*300)*.5; return st(x)
def pop():
    t=T(0.14); f=1100*np.exp(-t*28)+220; x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*35); return st(x)
def shimmer(d=1.6,n=22):
    x=np.zeros(int((d+.5)*SR))
    for k in range(n):
        o=int((k/n)*d*.75*SR+R.uniform(0,.04)*SR); f=R.uniform(2600,7000)
        b=bell(f,.45,14,((1,1),(2.01,.3))); x[o:o+len(b)]+=b*R.uniform(.4,1)
    x=hp(x,1800); return np.stack([x,np.roll(x,int(.013*SR))],1)
def scratch():  # pen strike-through
    t=T(0.42); n=bp(nz(len(t)),1500,6000)
    am=0.6+0.4*np.sin(2*np.pi*55*t); x=n*am*np.sin(np.pi*t/0.42)**.7; return st(x,.3)
def heart():
    x=np.zeros(int(1.0*SR))
    for o,a in [(0,1),(0.22,.7)]:
        t=T(.25); b=np.sin(2*np.pi*np.cumsum(70*np.exp(-t*8)+45)/SR)*np.exp(-t*16)*a; i=int(o*SR); x[i:i+len(b)]+=b
    return st(np.tanh(2*x))
def foam(d=1.1):  # pump pssht + bubbly squish
    t=T(d); air=bp(nz(len(t)),1800,9000)*np.exp(-((t-.12)/.09)**2)*0.9
    clk=np.zeros_like(t); clk[:int(.03*SR)]=hp(nz(int(.03*SR)),2000)*np.exp(-T(.03)*150)
    bub=np.zeros_like(t)
    for k in range(40):
        o=R.uniform(.15,d-.15); f=R.uniform(500,1800); tt=T(.05)
        b=np.sin(2*np.pi*np.cumsum(f*(1+3*tt))/SR)*np.exp(-tt*90); i=int(o*SR); bub[i:i+len(b)]+=b*R.uniform(.1,.35)
    sq=lp(nz(len(t)),1200)*np.exp(-((t-.5)/.3)**2)*.35
    return st(air+clk+bub+sq,.4)
def chime():
    x=np.zeros(int(2.2*SR))
    for i,f in enumerate([1046.5,1318.5,1568.0,2093.0,2637.0]):
        b=bell(f,1.6,3.2); o=int(i*.06*SR); x[o:o+len(b)]+=b*(1-.1*i)
    return np.stack([x,np.roll(x,int(.009*SR))],1)
def kaching():
    x=np.zeros(int(1.4*SR)); 
    m=hp(nz(int(.08*SR)),3000)*np.exp(-T(.08)*60); x[:len(m)]+=m*.8
    for f,o in [(2637,.06),(3520,.09),(4186,.12)]:
        b=bell(f,1.2,4); i=int(o*SR); x[i:i+len(b)]+=b*.7
    return st(x,.5)
def tap():
    t=T(.09); x=np.sin(2*np.pi*np.cumsum(500*np.exp(-t*40)+120)/SR)*np.exp(-t*50)+hp(nz(len(t)),3000)*np.exp(-t*200)*.3; return st(x)
def clocktick(n=6,gap=.25):
    x=np.zeros(int((n*gap+.2)*SR))
    for k in range(n):
        t=T(.04); b=(np.sin(2*np.pi*(2400 if k%2 else 1800)*t)*np.exp(-t*180)); i=int(k*gap*SR); x[i:i+len(b)]+=b
    return st(x)
kit=dict(boom=boom,whoosh=whoosh,whoosh_r=lambda:whoosh(.7,True),riser=riser,tick=tick,pop=pop,shimmer=shimmer,
         scratch=scratch,heart=heart,foam=foam,chime=chime,kaching=kaching,tap=tap,clock=clocktick)
for k,f in kit.items(): sf.write(f'{out}/{k}.wav',norm(f(),-1).astype(np.float32),SR)
# ---- music: 122bpm luxe deep-house, F minor, length L
L=float(sys.argv[2]); bpm=122; b=60/bpm; N=int(L*SR); M=np.zeros((N,2))
def put(sig,t0,g=1.0):
    i=int(t0*SR); 
    if i>=N: return
    s=sig[:N-i]; 
    if s.ndim==1: s=np.stack([s,s],1)
    M[i:i+len(s)]+=s*g
kick=lambda: (lambda t: np.tanh(2.2*np.sin(2*np.pi*np.cumsum(48+110*np.exp(-t*30))/SR)*np.exp(-t*7)))(T(.45))
hat=lambda d=.07: hp(nz(int(d*SR)),7000)*np.exp(-T(d)*(45 if d<.1 else 14))
clap=lambda: bp(sum(np.pad(nz(int(.012*SR))*np.exp(-T(.012)*200),(int(k*.009*SR),0))[:int(.2*SR)] if False else 0 for k in range(1)) + nz(int(.2*SR))*np.exp(-T(.2)*22),900,5000)
def note(f,d,typ='bass'):
    t=T(d)
    if typ=='bass':
        x=np.sin(2*np.pi*f*t)+.35*np.sin(4*np.pi*f*t); x=np.tanh(1.5*x)*np.minimum(1,t/.005)*np.exp(-t*2.5); return lp(x,500)
    if typ=='pad':
        x=sum(np.sin(2*np.pi*f*(1+dt)*t+ph) for dt,ph in [(-.004,0),(0,1),(.005,2)])/3
        env=np.minimum(1,t/.35)*np.minimum(1,(d-t)/.5); return lp(x*env,2200)
    if typ=='key':
        x=sum(a*np.sin(2*np.pi*f*m*t) for m,a in [(1,1),(2,.4),(3,.15),(4,.08)])*np.exp(-t*3.2)*np.minimum(1,t/.003); return x
fm=lambda n: 440*2**((n-69)/12)
prog=[(53,[65,68,72,75]),(49,[61,65,68,72]),(56,[63,68,72,75]),(51,[63,67,70,74])]  # Fm9 Db Ab Eb
bar=4*b; nb=int(np.ceil(L/bar))+1; start_drums=0.0
for k in range(nb):
    t0=k*bar; root,ch=prog[k%4]
    for n in ch: put(np.stack([note(fm(n),bar+.4,'pad')*.9, note(fm(n)*1.002,bar+.4,'pad')*.9],1),t0,.10)
    for s in range(8):
        if s in (0,3,5,6): put(note(fm(root-12),b*.45),t0+s*b/2,.32)
    for q in range(4):
        put(kick(),t0+q*b,.55); put(hat(.06),t0+q*b+b/2,.16)
        put(hat(.025),t0+q*b+b*.25,.06); put(hat(.025),t0+q*b+b*.75,.06)
        if q in (1,3): put(clap(),t0+q*b,.22)
    for i,s in enumerate([0,1.5,3,3.5]):  # keys stabs
        for n in ch[1:]: put(np.stack([note(fm(n+12),.6,'key'),np.roll(note(fm(n+12),.6,'key'),300)],1),t0+s*b,.045)
M=np.tanh(M*1.2)
sf.write(f'{out}/music.wav',(norm(M,-3)).astype(np.float32),SR); print('ok', bar)
