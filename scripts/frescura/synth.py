import numpy as np, soundfile as sf, sys
from scipy.signal import butter, sosfilt
SR=48000; out=sys.argv[1]; R=np.random.default_rng(11)
T=lambda d: np.arange(int(d*SR))/SR
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],btype='band',fs=SR,output='sos'),x,axis=0)
def lp(x,f,o=2): return sosfilt(butter(o,f,btype='low',fs=SR,output='sos'),x,axis=0)
def hp(x,f,o=2): return sosfilt(butter(o,f,btype='high',fs=SR,output='sos'),x,axis=0)
def nrm(x,db=-1): return x/(np.max(np.abs(x))+1e-9)*10**(db/20)
def st(x,w=0.0):
    d=int(0.009*SR); r=np.concatenate([np.zeros(d),x])[:len(x)]; return np.stack([x,(1-w)*x+w*r],1)
def bell(f,d,dec=5,parts=((1,1),(2.76,.35),(5.4,.12))):
    t=T(d); return sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-dec*m**.4*t) for m,a in parts)*np.minimum(1,t/0.002)
def sweepnoise(d,f0,f1,shape):
    n=R.standard_normal(int(d*SR)); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        p=i/len(n); fc=f0*(f1/f0)**p; y[i:i+seg]=bp(n[i:i+seg],fc*.7,min(fc*1.5,23000))
    return y*shape(T(d)/d)
S={}
# impact: sub drop + noise thump + tail
t=T(2.2); sub=np.sin(2*np.pi*np.cumsum(38+90*np.exp(-t*9))/SR)*np.exp(-t*1.6)
th=lp(R.standard_normal(len(t)),900)*np.exp(-t*18); S['impact']=st(nrm(sub*1.0+th*.6),.5)
# whoosh L->R
w=sweepnoise(0.55,500,6000,lambda p:np.sin(np.pi*p)**2); pn=T(.55)/.55
S['whoosh']=np.stack([w*(1-pn)+.3*w,w*pn+.3*w],1)
w=sweepnoise(0.35,1200,9000,lambda p:np.sin(np.pi*p)**3); S['swish']=st(w,.6)
# riser 1.6s
r=sweepnoise(1.6,300,9000,lambda p:p**2.2); tt=T(1.6); r+=0.25*np.sin(2*np.pi*np.cumsum(200+900*(tt/1.6)**2)/SR)*(tt/1.6)**2
S['riser']=st(r,.7)
# glass ting
S['ting']=st(bell(2093,1.6,4)+.5*bell(3136,1.6,6),.4)
# sparkle shimmer
x=np.zeros(int(1.4*SR))
for k in range(22):
    o=int(R.uniform(0,.9)*SR); b=bell(R.uniform(3000,7500),.4,14,((1,1),(2.01,.3))); x[o:o+len(b)]+=b*R.uniform(.3,1)
S['sparkle']=st(hp(x,2000),.9)
# soft click / tick
t=T(.05); S['tick']=st(hp(R.standard_normal(len(t))*np.exp(-t*400),2500)+.5*np.sin(2*np.pi*1800*t)*np.exp(-t*200))
# pop
t=T(.14); S['pop']=st(np.sin(2*np.pi*np.cumsum(260+700*np.exp(-t*35))/SR)*np.exp(-t*30))
# bass hit (short boom)
t=T(.8); S['boom']=st(np.sin(2*np.pi*np.cumsum(50+70*np.exp(-t*14))/SR)*np.exp(-t*4.5))
# tap (button)
t=T(.09); S['tap']=st(np.sin(2*np.pi*np.cumsum(1300*np.exp(-t*20)+400)/SR)*np.exp(-t*45)+.2*hp(R.standard_normal(len(t)),4000)*np.exp(-t*90))
# cha-ching (luxury) : two bells + shimmer
x=np.zeros(int(1.6*SR)); a=bell(2637,1.2,5); b=bell(3520,1.2,5); x[:len(a)]+=a; o=int(.09*SR); x[o:o+len(b)]+=b
S['ching']=st(x,.5)
# foam squish: filtered bubbly noise
t=T(.7); n=R.standard_normal(len(t)); bub=np.zeros_like(t)
for k in range(40):
    o=int(R.uniform(0,.6)*SR); f=R.uniform(600,2200); L=int(.03*SR); tt=np.arange(L)/SR
    bub[o:o+L]+=np.sin(2*np.pi*f*(1+tt*30)*tt)*np.exp(-tt*120)
S['foam']=st(lp(bub*.6+bp(n,300,2500)*np.sin(np.pi*t/.7)**2*.5,5000),.5)
# reverse swell (pre-hit)
r=sweepnoise(.9,800,12000,lambda p:p**3); S['swell']=st(r,.8)
for k,v in S.items(): sf.write(f"{out}/{k}.wav",nrm(v,-1).astype(np.float32),SR)
print(list(S))
