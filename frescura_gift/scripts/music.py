import numpy as np, soundfile as sf, sys
from scipy.signal import butter, sosfilt
SR=48000; BPM=122; beat=60/BPM; D=43.0; N=int(D*SR); rng=np.random.default_rng(3)
L=np.zeros(N); R=np.zeros(N)
def add(x,t,g=1.0,pan=0.0):
    i=int(t*SR); 
    if i>=N: return
    x=x[:N-i]; L[i:i+len(x)]+=x*g*(1-pan)**.5; R[i:i+len(x)]+=x*g*(1+pan)**.5
def lp(x,f,o=2): return sosfilt(butter(o,f,btype='low',fs=SR,output='sos'),x)
def hp(x,f,o=2): return sosfilt(butter(o,f,btype='high',fs=SR,output='sos'),x)
tt=lambda d: np.arange(int(d*SR))/SR
t=tt(0.4); kick=np.sin(2*np.pi*np.cumsum(48+110*np.exp(-t*35))/SR)*np.exp(-t*7); kick=np.tanh(kick*1.5)
t=tt(0.06); hat=hp(rng.standard_normal(len(t)),7000)*np.exp(-t*70)
t=tt(0.25); clap=sosfilt(butter(2,[900,4000],btype='band',fs=SR,output='sos'),rng.standard_normal(len(t)))*np.exp(-t*18)
t=tt(0.12); shk=hp(rng.standard_normal(len(t)),5000)*np.sin(np.pi*t/0.12)**2
def note(f,d,kind='pad'):
    t=tt(d)
    if kind=='pad':
        x=sum(np.sin(2*np.pi*f*(1+dt)*t+np.sin(2*np.pi*0.3*t)) for dt in (-0.004,0,0.005))
        x+= 0.3*sum(np.sin(2*np.pi*2*f*(1+dt)*t) for dt in (-0.003,0.003))
        env=np.minimum(1,t/0.25)*np.minimum(1,(d-t)/0.4)
    else: # pluck/bass
        x=np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*2*f*t); env=np.exp(-t*(6 if kind=='bass' else 9))*np.minimum(1,t/0.004)
    return x*env
mid=lambda m: 440*2**((m-69)/12)
# chords (1 bar each = 4 beats): Dm9, G13, Cmaj9, Am9
chords=[[50,53,57,60,64],[43,53,57,59,64],[48,52,55,59,62],[45,52,55,60,64]]
bassn=[38,43,36,45]
bar=4*beat; nb=int(D/bar)+1
for b in range(nb):
    t0=b*bar; ch=chords[b%4]
    pad=sum(note(mid(m+12 if m<50 else m),bar+0.3,'pad') for m in ch[1:]); add(lp(pad,2200)*0.05,t0,1,0)
    for k in range(4):
        tb=t0+k*beat
        intro = tb<1.6
        if not intro: add(kick,tb,0.9)
        add(hat,tb+beat/2,0.22,0.3)
        add(shk,tb+beat/4,0.07,-0.4); add(shk,tb+3*beat/4,0.07,0.4)
        if k in (1,3) and not intro: add(clap,tb,0.25,0.1)
    for k,off in enumerate([0,0.75,1.5,2.5,3.25]):
        add(lp(note(mid(bassn[b%4]),0.35,'bass'),600)*0.55,t0+off*beat)
    # pluck arp
    for k in range(8):
        m=ch[(k*2)%len(ch)]+24
        add(lp(note(mid(m),0.3,'pluck'),3500)*0.05,t0+k*beat/2+beat/4,1,(-0.5 if k%2 else 0.5))
x=np.stack([L,R],1); x/=np.max(np.abs(x)); x*=0.85
fade=np.ones(N); fo=int(1.5*SR); fade[-fo:]=np.linspace(1,0,fo); x*=fade[:,None]
sf.write(sys.argv[1],x.astype(np.float32),SR); print('music',D)
