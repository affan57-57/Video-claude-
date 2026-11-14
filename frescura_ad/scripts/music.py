import numpy as np, soundfile as sf, sys
from scipy.signal import butter, sosfilt
SR=48000; BPM=118; beat=60/BPM; D=float(sys.argv[2]); N=int(D*SR); rng=np.random.default_rng(3)
L=np.zeros(N); R=np.zeros(N)
def add(x,t,g=1,pan=0):
    i=int(t*SR); x=x[:max(0,N-i)]; L[i:i+len(x)]+=x*g*(1-pan); R[i:i+len(x)]+=x*g*(1+pan)
T=lambda d: np.arange(int(d*SR))/SR
def lp(x,f): return sosfilt(butter(2,f,btype='low',fs=SR,output='sos'),x)
def hp(x,f): return sosfilt(butter(2,f,btype='high',fs=SR,output='sos'),x)
t=T(0.4); kick=np.sin(2*np.pi*np.cumsum(48+110*np.exp(-t*30))/SR)*np.exp(-t*7); kick=np.tanh(1.8*kick)
t=T(0.05); hat=hp(rng.standard_normal(len(t)),7000)*np.exp(-t*90)
t=T(0.25); clap=sosfilt(butter(2,[900,5000],btype='band',fs=SR,output='sos'),rng.standard_normal(len(t)))*np.exp(-t*22)
mid=lambda n: 440*2**((n-69)/12)
prog=[(57,[69,72,76]),(53,[69,72,77]),(48,[67,72,76]),(55,[67,71,74])]  # Am F C G
bar=4*beat; nb=int(D/beat)+1
for b in range(nb):
    tb=b*beat
    if tb>=D: break
    add(kick,tb,0.9)
    add(hat,tb+beat/2,0.25,0.3); add(hat,tb+beat*0.75,0.1,-0.3)
    if b%2==1: add(clap,tb,0.35)
for k in range(int(D/bar)+1):
    root,ch=prog[k%4]; tb=k*bar
    for s in range(8):  # bass eighths, sidechain-ish
        t=T(beat/2); f=mid(root-12); x=np.sin(2*np.pi*f*t)+0.3*np.sin(4*np.pi*f*t); x*=np.minimum(1,t/0.03)*np.exp(-t*3)
        add(x,tb+s*beat/2,0.35 if s%2 else 0.2)
    t=T(bar); pad=sum(np.sin(2*np.pi*mid(n)*t*(1+d))for n in ch for d in(-0.003,0.003))
    pad=lp(pad,2500)*np.minimum(1,t/0.6)*np.minimum(1,(bar-t)/0.4); add(pad,tb,0.06,0)
    # pluck arpeggio
    for s in range(8):
        n=ch[s%3]+12; t=T(0.4); x=np.sin(2*np.pi*mid(n)*t)*np.exp(-t*9); add(x,tb+s*beat/2,0.08,0.4 if s%2 else -0.4)
y=np.stack([L,R],1); fade=np.minimum(1,np.arange(N)/SR/0.3)*np.minimum(1,(D-np.arange(N)/SR)/1.2); y*=fade[:,None]
y=y/np.max(np.abs(y))*0.89; sf.write(sys.argv[1],y.astype(np.float32),SR)
