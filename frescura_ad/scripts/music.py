# Minimal luxe deep-house bed, 118 BPM, Am9 - Fmaj7 - Cmaj7 - G6. Original synthesis.
import numpy as np, soundfile as sf, sys
from scipy.signal import butter, sosfilt
SR=48000; DUR=float(sys.argv[2]); BPM=118; B=60/BPM; rng=np.random.default_rng(3)
N=int(DUR*SR); L=np.zeros(N); R=np.zeros(N)
def lp(x,f): return sosfilt(butter(2,f,btype='low',fs=SR,output='sos'),x)
def hp(x,f): return sosfilt(butter(2,f,btype='high',fs=SR,output='sos'),x)
def add(x,at,g=1.0,pan=0.0):
    i=int(at*SR); j=min(N,i+len(x));
    if i>=N: return
    L[i:j]+=x[:j-i]*g*np.sqrt(1-pan); R[i:j]+=x[:j-i]*g*np.sqrt(1+pan)
t=lambda d: np.arange(int(d*SR))/SR
def kick():
    tt=t(0.45); f=150*np.exp(-tt*28)+45; return np.tanh(1.5*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*7))
def hat(o=False):
    tt=t(0.25 if o else 0.06); return hp(rng.standard_normal(len(tt)),7000)*np.exp(-tt*(18 if o else 90))
def clap():
    tt=t(0.3); n=hp(lp(rng.standard_normal(len(tt)),5000),900)
    env=sum(np.exp(-np.maximum(0,tt-d)*(60 if d<0.03 else 14))*(tt>=d) for d in (0,0.012,0.024,0.036)); return n*env*0.5
def note(f,d,kind='pad'):
    tt=t(d)
    if kind=='pad':
        x=sum(np.sin(2*np.pi*f*dt*tt+ph) for dt,ph in ((1,0),(1.004,1),(0.996,2),(2.002,0.5)))*0.25
        env=np.minimum(1,tt/0.35)*np.minimum(1,(d-tt)/0.5); return lp(x*env,2200)
    if kind=='bass':
        x=np.sin(2*np.pi*f*tt)+0.25*np.sin(2*np.pi*2*f*tt); return x*np.minimum(1,tt/0.01)*np.exp(-tt*3)*np.minimum(1,(d-tt)/0.03)
    if kind=='pluck':
        x=sum(np.sin(2*np.pi*f*k*tt)/k for k in (1,2,3)); return x*np.exp(-tt*9)*np.minimum(1,tt/0.003)
m=lambda n: 440*2**((n-69)/12)
chords=[(57,[57,60,64,67,71]),(53,[53,57,60,64]),(48,[52,55,59,60]),(55,[55,59,62,64])]
bar=4*B; nb=int(DUR/bar)+1
for b in range(nb):
    root,ch=chords[b%4]; t0=b*bar
    for n in ch: add(note(m(n),bar+0.3),t0,0.09,pan=rng.uniform(-.4,.4))
    for s in range(8):
        at=t0+s*B/2
        if s%2==0: add(kick(),at,0.9)
        else: add(hat(s==7),at,0.18,0.3)
        add(hat(),at+B/4,0.08,-0.3)
        if s in (2,6): add(clap(),at,0.45)
        if s in (1,3,4,6): add(note(m(root-12),B/2*0.9,'bass'),at,0.42)
    arp=[ch[i%len(ch)]+12 for i in (0,2,4,1,3,0,2,4)]
    for s,n in enumerate(arp): add(note(m(n),0.5,'pluck'),t0+s*B/2+B/4,0.05,pan=0.5 if s%2 else -0.5)
x=np.stack([L,R],1); x=x/np.max(np.abs(x))*0.8
fade=int(1.2*SR); x[-fade:]*=np.linspace(1,0,fade)[:,None]; x[:int(0.3*SR)]*=np.linspace(0,1,int(0.3*SR))[:,None]
sf.write(sys.argv[1],x.astype(np.float32),SR)
