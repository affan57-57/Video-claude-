import numpy as np, soundfile as sf, sys, os
from scipy.signal import butter, sosfilt
SR=48000; out=sys.argv[1]; os.makedirs(out,exist_ok=True); rng=np.random.default_rng(11)
T=lambda d: np.arange(int(d*SR))/SR
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],btype='band',fs=SR,output='sos'),x,axis=0)
def lp(x,f,o=2): return sosfilt(butter(o,f,btype='low',fs=SR,output='sos'),x,axis=0)
def hp(x,f,o=2): return sosfilt(butter(o,f,btype='high',fs=SR,output='sos'),x,axis=0)
def norm(x,db=-1): return x/(np.max(np.abs(x))+1e-9)*10**(db/20)
def st(x,w=0.0):
    d=int(0.008*SR*w); R=np.roll(x,d) if d else x; return np.stack([x,R],1)
def save(n,x): x=norm(x); x=x if x.ndim==2 else st(x); sf.write(f"{out}/{n}.wav",x.astype(np.float32),SR); print(n,round(len(x)/SR,2))
def bell(f,d,decay=5,parts=((1,1),(2.0,.35),(3.01,.15))):
    t=T(d); return sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-decay*m**.5*t) for m,a in parts)*np.minimum(1,t/0.002)
def sweep_noise(d,f0,f1,q=0.6):
    n=rng.standard_normal(int(d*SR)); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        p=i/len(n); fc=f0*(f1/f0)**p
        y[i:i+seg]=bp(n[i:i+seg],max(40,fc*(1-q)),min(20000,fc*(1+q)))
    return y
# --- impact / boom (hook)
def boom(d=2.2):
    t=T(d); f=120*np.exp(-t*9)+38; ph=2*np.pi*np.cumsum(f)/SR
    sub=np.sin(ph)*np.exp(-t*2.2); click=hp(rng.standard_normal(len(t)),2000)*np.exp(-t*60)*0.5
    body=lp(rng.standard_normal(len(t)),900)*np.exp(-t*12)*0.6
    x=sub+click+body; return np.tanh(x*1.6)
def hit():  # tight punchy impact
    t=T(0.9); f=180*np.exp(-t*25)+55; x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*6)
    x+=hp(rng.standard_normal(len(t)),1500)*np.exp(-t*45)*0.7; return np.tanh(2*x)
def whoosh(d=0.6,f0=250,f1=5000):
    t=T(d); y=sweep_noise(d,f0,f1); env=np.sin(np.pi*np.minimum(1,t/d))**2.5
    x=y*env; L=x*(1-t/d)+0.25*x; R=x*(t/d)+0.25*x; return np.stack([L,R],1)
def swoosh_down(): return whoosh(0.5,6000,300)
def riser(d=2.8):
    t=T(d); y=sweep_noise(d,200,9000,0.4)*(t/d)**2.2
    tone=sum(np.sin(2*np.pi*(110*k)*(1+0.9*(t/d)**2)*t) for k in (1,1.5,2))*0.08*(t/d)**2
    x=y+tone; x[-int(0.02*SR):]*=np.linspace(1,0,int(0.02*SR)); return st(x,1)
def shimmer(d=1.8,n=26,lo=2500,hi=8000):
    x=np.zeros(int(d*SR)+SR)
    for k in range(n):
        o=int(rng.uniform(0,d*0.7)*SR); b=bell(rng.uniform(lo,hi),0.6,decay=10)
        x[o:o+len(b)]+=b*rng.uniform(.3,1)
    x=hp(x,1800); return np.stack([x,np.roll(x,int(0.013*SR))],1)
def chime():
    x=np.zeros(int(2.2*SR))
    for i,f in enumerate([1567.98,2093.0,2637.0]):
        b=bell(f,2.0,decay=2.6); o=int(i*0.06*SR); x[o:o+len(b)]+=b*(1-0.2*i)
    return st(x,1)
def tick():
    t=T(0.08); x=np.sin(2*np.pi*2400*t)*np.exp(-t*120)+hp(rng.standard_normal(len(t)),4000)*np.exp(-t*200)*0.5; return x
def tap():
    t=T(0.18); f=700*np.exp(-t*30)+220; x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*30); return x
def pop():
    t=T(0.12); f=1300*np.exp(-t*40)+300; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*45)
def bubbles(d=1.4,n=22):
    x=np.zeros(int(d*SR)+SR//4)
    for k in range(n):
        o=int(rng.uniform(0,d)*SR); t=T(rng.uniform(0.03,0.07)); f0=rng.uniform(600,2200)
        b=np.sin(2*np.pi*np.cumsum(f0*(1+3*t/t[-1]))/SR)*np.exp(-t*60)*rng.uniform(.3,1); x[o:o+len(b)]+=b
    return np.stack([x,np.roll(x,int(0.009*SR))],1)
def pump():  # plastic press + air puff
    t=T(0.5); c=hp(rng.standard_normal(len(t)),2500)*np.exp(-t*150)
    c2=np.roll(hp(rng.standard_normal(len(t)),2000)*np.exp(-t*170),int(0.09*SR))*0.7
    puff=bp(rng.standard_normal(len(t)),300,3000)*np.exp(-((t-0.2)/0.09)**2)*0.6
    return c+c2+puff
def scrape(d=1.0):  # sandpaper
    n=rng.standard_normal(int(d*SR)); t=T(d)
    am=0.55+0.45*np.sign(np.sin(2*np.pi*7*t))*np.abs(np.sin(2*np.pi*7*t))**.3
    grit=(rng.random(len(n))<0.02)*rng.standard_normal(len(n))*3
    x=bp(n*am+grit,1200,9000)*np.minimum(1,t/0.05)*np.minimum(1,(d-t)/0.15); return st(x,1)
def glitch(d=0.35):
    x=np.zeros(int(d*SR)); p=0
    while p<len(x):
        L=int(rng.uniform(0.01,0.05)*SR); t=np.arange(L)/SR
        s=np.sign(np.sin(2*np.pi*rng.uniform(80,1200)*t))*0.6 if rng.random()<.5 else hp(rng.standard_normal(L),3000)
        x[p:p+L]=s[:len(x)-p]*rng.uniform(.3,1); p+=L
    return st(lp(x,9000),1)
def buzz():  # soft error "no"
    t=T(0.42); x=sum(np.sin(2*np.pi*f*t) for f in (180,182.5,360))*np.exp(-t*4)*(t<0.40); return lp(np.tanh(2*x),2500)
def drop():  # water droplet
    t=T(0.35); f=600+1800*(t/0.06).clip(0,1); x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*25); return x
def ching():  # luxury register/sparkle CTA
    x=np.zeros(int(1.8*SR))
    for i,f in enumerate([2093,2637,3136,4186]):
        b=bell(f,1.4,decay=4); o=int(i*0.045*SR); x[o:o+len(b)]+=b
    return st(x,1)
def camera():
    t=T(0.3); a=hp(rng.standard_normal(len(t)),1500)*np.exp(-t*90); b=np.roll(a,int(0.08*SR))*0.8; return a+b
for n,f in dict(boom=boom,hit=hit,whoosh=whoosh,swoosh=swoosh_down,riser=riser,shimmer=shimmer,chime=chime,tick=tick,tap=tap,
                pop=pop,bubbles=bubbles,pump=pump,scrape=scrape,glitch=glitch,buzz=buzz,drop=drop,ching=ching,camera=camera).items():
    save(n,f())
