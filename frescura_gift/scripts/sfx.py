import numpy as np, soundfile as sf, sys
from scipy.signal import butter, sosfilt
SR=48000; out=sys.argv[1]; rng=np.random.default_rng(11)
T=lambda d: np.arange(int(d*SR))/SR
def nz(n): return rng.standard_normal(n)
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],btype='band',fs=SR,output='sos'),x,axis=0)
def lp(x,f,o=2): return sosfilt(butter(o,f,btype='low',fs=SR,output='sos'),x,axis=0)
def hp(x,f,o=2): return sosfilt(butter(o,f,btype='high',fs=SR,output='sos'),x,axis=0)
def norm(x,db=-1): return x/np.max(np.abs(x))*10**(db/20)
def st(x,w=0.0):
    if x.ndim==2: return x
    d=int(0.007*SR*w); R=np.roll(x,d) if d else x; return np.stack([x,R],1)
def sweepnoise(d,f0,f1,q=0.5,shape=None):
    n=nz(int(d*SR)); y=np.zeros_like(n); seg=512; N=len(n)
    for i in range(0,N,seg):
        p=i/N; fc=f0*(f1/f0)**p
        y[i:i+seg]=sosfilt(butter(2,[fc*(1-q),fc*(1+q)],btype='band',fs=SR,output='sos'),n[i:i+seg])
    return y
def whoosh(d=0.55,up=True):
    tt=T(d); y=sweepnoise(d,400 if up else 4000,4000 if up else 400)
    env=(np.sin(np.pi*tt/d)**3); x=y*env
    L=x*np.linspace(1,0.3,len(x)); R=x*np.linspace(0.3,1,len(x)); return np.stack([L,R],1)
def impact():
    tt=T(1.6); f=55+90*np.exp(-tt*18); ph=2*np.pi*np.cumsum(f)/SR
    sub=np.sin(ph)*np.exp(-tt*2.6); click=hp(nz(len(tt)),2000)*np.exp(-tt*60)*0.5
    body=lp(nz(len(tt)),900)*np.exp(-tt*9)*0.6
    tail=bp(nz(len(tt)),200,3000)*np.exp(-tt*3.5)*0.12
    x=sub*1.0+click+body+tail; return st(np.tanh(x*1.6),1)
def riser(d=1.0):
    tt=T(d); y=sweepnoise(d,300,9000,0.35); env=(tt/d)**2.2
    tone=np.sin(2*np.pi*np.cumsum(200+1400*(tt/d)**2)/SR)*0.25*env
    return st(y*env+tone,1)
def tap():
    tt=T(0.08); x=hp(nz(len(tt)),1500)*np.exp(-tt*120)+np.sin(2*np.pi*1800*tt)*np.exp(-tt*90)*0.6; return st(x)
def pop():
    tt=T(0.14); f=1100*np.exp(-tt*28)+220; x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*38); return st(x)
def bell(f,d,dec=5,parts=((1,1),(2.0,.35),(3.0,.15),(4.1,.08))):
    tt=T(d); return sum(a*np.sin(2*np.pi*f*m*tt)*np.exp(-dec*m**.5*tt) for m,a in parts)*np.minimum(1,tt/0.002)
def shimmer(d=1.2,n=18):
    x=np.zeros(int(d*SR)+SR//2)
    for k in range(n):
        o=int(rng.uniform(0,d*0.7)*SR); b=bell(rng.uniform(3000,7500),0.4,14,((1,1),(2.01,.3)))
        x[o:o+len(b)]+=b*rng.uniform(.3,1)*(1-o/len(x))
    x=hp(x,2000); return np.stack([x,np.roll(x,int(0.013*SR))],1)
def bubbles(d=1.8,n=60):
    x=np.zeros(int(d*SR)+SR//4)
    for k in range(n):
        o=int(rng.uniform(0,d)*SR); L=int(rng.uniform(0.02,0.06)*SR); tt=np.arange(L)/SR
        f0=rng.uniform(500,1600); f=f0*(1+tt*rng.uniform(8,25))
        b=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*rng.uniform(40,90))
        x[o:o+L]+=b*rng.uniform(.2,1)
    fizz=hp(nz(len(x)),5000)*0.04
    x=x+fizz; env=np.minimum(1,np.arange(len(x))/SR/0.15)*np.minimum(1,(len(x)/SR-np.arange(len(x))/SR)/0.5)
    x*=env; return np.stack([x,np.roll(x,int(0.009*SR))],1)
def pumpsquish():
    tt=T(0.35); x=lp(nz(len(tt)),2500)*np.exp(-tt*14)*(1+np.sin(2*np.pi*35*tt))*0.5
    clk=tap()[:,0]; x[:len(clk)]+=clk*0.7; return st(x)
def scribble(d=0.45):
    tt=T(d); n=bp(nz(len(tt)),1800,6000); am=0.5+0.5*np.sign(np.sin(2*np.pi*14*tt)); x=n*am*np.sin(np.pi*tt/d)
    return st(x)
def ding():
    return st(bell(1568,1.4,4)+0.6*np.pad(bell(2093,1.2,5),(int(0.09*SR),int(1.4*SR)))[:int(1.4*SR)])
def ticks(n=6,gap=0.06):
    x=np.zeros(int((n*gap+0.1)*SR))
    for i in range(n):
        t_=tap()[:,0]*0.6; o=int(i*gap*SR); x[o:o+len(t_)]+=t_
    return st(x)
def subdrop():
    tt=T(1.2); f=80*np.exp(-tt*1.5)+30; x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.minimum(1,tt/0.01)*np.exp(-tt*2); return st(x)
def swish(d=0.3): 
    tt=T(d); y=sweepnoise(d,6000,1500,0.4)*np.sin(np.pi*tt/d)**2; return st(y,1)
FX=dict(whoosh_up=lambda:whoosh(0.55,True),whoosh_dn=lambda:whoosh(0.5,False),whoosh_long=lambda:whoosh(0.9,True),
 impact=impact,riser=riser,tap=tap,pop=pop,shimmer=shimmer,bubbles=bubbles,pump=pumpsquish,scribble=scribble,ding=ding,ticks=ticks,subdrop=subdrop,swish=swish)
for k,fn in FX.items():
    y=norm(fn(),-1.0); sf.write(f"{out}/{k}.wav",y.astype(np.float32),SR)
print('ok',list(FX))
