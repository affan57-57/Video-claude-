# Synthesize SFX + minimal-luxury beat, then mix with the cleaned voice. Usage: make_audio.py voice.wav out.wav cues.json
import numpy as np, soundfile as sf, sys, json, pyloudnorm as pyln
from scipy.signal import butter, sosfilt, fftconvolve
SR=48000; rng=np.random.default_rng(11)
def t(d): return np.arange(int(d*SR))/SR
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],btype='band',fs=SR,output='sos'),x,axis=0)
def hp(x,f,o=2): return sosfilt(butter(o,f,btype='high',fs=SR,output='sos'),x,axis=0)
def lp(x,f,o=2): return sosfilt(butter(o,f,btype='low',fs=SR,output='sos'),x,axis=0)
def st(x,w=0.0):
    d=int(0.009*SR*w); R=np.concatenate([np.zeros(d),x])[:len(x)] if d else x
    return np.stack([x,R],1)
def nrm(x,db=-1): return x/(np.max(np.abs(x))+1e-9)*10**(db/20)
def ir(d=1.6,decay=3.2,seed=3):
    r=np.random.default_rng(seed); n=r.standard_normal((int(d*SR),2))*np.exp(-decay*t(d))[:,None]
    n=lp(n,6000); n[:200]*=np.linspace(0,1,200)[:,None]; return n/np.sqrt(np.sum(n**2))
IR=ir()
def verb(x,wet=0.25):
    if x.ndim==1: x=st(x)
    y=np.stack([fftconvolve(x[:,0],IR[:,0]),fftconvolve(x[:,1],IR[:,1])],1)
    out=np.zeros_like(y); out[:len(x)]+=x*(1-wet); out+=y*wet*3; return out
def bell(f,d,partials=((1,1),(2.0,.4),(3.01,.2),(4.2,.1)),decay=6):
    tt=t(d); x=sum(a*np.sin(2*np.pi*f*m*tt)*np.exp(-decay*m**.5*tt) for m,a in partials)
    return x*np.minimum(1,tt/0.002)
# ---------- SFX ----------
def boom(d=2.2):
    tt=t(d); f=38+90*np.exp(-tt*9); ph=2*np.pi*np.cumsum(f)/SR
    sub=np.sin(ph)*np.exp(-tt*2.2)
    n=lp(rng.standard_normal(len(tt)),1800)*np.exp(-tt*14)*0.6
    click=hp(rng.standard_normal(len(tt)),2500)*np.exp(-tt*120)*0.5
    x=np.tanh(1.6*(sub+n+click)); return verb(st(x,0.3),0.2)
def whoosh(d=0.6,lo=250,hi=4200,rev=False):
    n=rng.standard_normal(int(d*SR)); tt=t(d); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        p=i/len(n); p=p if not rev else p**2; fc=lo+(hi-lo)*np.sin(np.pi*min(p,1))**2
        y[i:i+seg]=sosfilt(butter(2,[fc*0.55,min(fc*1.7,20000)],btype='band',fs=SR,output='sos'),n[i:i+seg])
    env=np.sin(np.pi*tt/d)**2 if not rev else (tt/d)**3*np.exp(-np.maximum(0,tt-0.9*d)*80)
    x=y*env; L=x*(1-tt/d)+0.25*x; R=x*(tt/d)+0.25*x; return verb(np.stack([L,R],1),0.15)
def riser(d=1.2):
    tt=t(d); f=200*2**(tt/d*3.2); ph=2*np.pi*np.cumsum(f)/SR
    x=(np.sin(ph)*0.3+bp(rng.standard_normal(len(tt)),800,9000)*0.7)*(tt/d)**2
    return verb(st(x,0.5),0.3)
def pop(f0=900,d=0.12):
    tt=t(d); f=f0*np.exp(-tt*28)+180; ph=2*np.pi*np.cumsum(f)/SR; return st(np.sin(ph)*np.exp(-tt*38))
def tick(): tt=t(0.05); return st(hp(rng.standard_normal(len(tt)),3000)*np.exp(-tt*160)+np.sin(2*np.pi*2400*tt)*np.exp(-tt*90)*0.6)
def click(): tt=t(0.08); return st(np.sin(2*np.pi*1800*tt)*np.exp(-tt*70)+0.5*hp(rng.standard_normal(len(tt)),4000)*np.exp(-tt*200))
def ding(f=1760): return verb(st(bell(f,1.4,decay=4.5),0.4),0.3)
def chime():
    x=np.zeros(int(1.8*SR))
    for i,f in enumerate([1318.5,1568.0,1975.5,2637.0]):
        b=bell(f,1.4,decay=4); o=int(i*0.06*SR); x[o:o+len(b)]+=b*(0.9-i*0.12)
    return verb(st(x,0.6),0.35)
def sparkle(d=1.0,n=16,seed=5):
    r=np.random.default_rng(seed); x=np.zeros(int(d*SR)+SR//2)
    for k in range(n):
        o=int(r.uniform(0,d*0.8)*SR); f=r.uniform(3000,7500)
        b=bell(f,0.35,partials=((1,1),(2.01,.3)),decay=14); x[o:o+len(b)]+=b*r.uniform(.4,1)
    return verb(st(hp(x,1500),0.8),0.3)
def bubbles(d=1.2,n=22,seed=9):
    r=np.random.default_rng(seed); x=np.zeros(int(d*SR)+SR//4)
    for k in range(n):
        o=int(r.uniform(0,d)*SR); f0=r.uniform(500,1400); dd=r.uniform(0.03,0.07); tt=t(dd)
        f=f0*(1+2.5*tt/dd); b=np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*tt/dd)
        x[o:o+len(b)]+=b*r.uniform(.3,1)
    return verb(st(x,0.5),0.2)
def squish():
    tt=t(0.35); n=bp(rng.standard_normal(len(tt)),300,2500)*np.exp(-tt*12)*np.minimum(1,tt/0.02)
    return st(n)+pop(300,0.35)*0.6
def wave(d=1.8):
    tt=t(d); n=rng.standard_normal((len(tt),2)); y=np.zeros_like(n); seg=1024
    for i in range(0,len(tt),seg):
        p=i/len(tt); fc=400+2200*np.sin(np.pi*p)
        y[i:i+seg]=sosfilt(butter(2,[fc*0.4,fc*2],btype='band',fs=SR,output='sos'),n[i:i+seg],axis=0)
    return y*(np.sin(np.pi*tt/d)**1.5)[:,None]
def kaching():
    x=np.zeros(int(1.6*SR)); c=click()[:,0]; x[:len(c)]+=c
    for i,f in enumerate([2093,2637,3136]):
        b=bell(f,1.2,decay=5); o=int((0.05+i*0.035)*SR); x[o:o+len(b)]+=b*0.7
    return verb(st(x,0.5),0.25)
def hit():
    tt=t(0.9); f=60+140*np.exp(-tt*25); s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*5)
    return verb(st(np.tanh(2*(s+0.4*bp(rng.standard_normal(len(tt)),1500,8000)*np.exp(-tt*30))),0.2),0.2)
def tap(): return pop(1400,0.08)+st(hp(rng.standard_normal(int(0.08*SR)),2000)*np.exp(-t(0.08)*120)*0.4)
SFX=dict(boom=boom,whoosh=whoosh,whoosh_rev=lambda:whoosh(0.7,rev=True),riser=riser,pop=pop,pop_hi=lambda:pop(1500,0.1),tick=tick,click=click,
         ding=ding,ding_lo=lambda:ding(1318.5),chime=chime,sparkle=sparkle,bubbles=bubbles,squish=squish,wave=wave,kaching=kaching,hit=hit,tap=tap)
# ---------- MUSIC: 112 BPM minimal deep-house luxury ----------
def music(dur, drop_at, end_fade):
    bpm=112; b=60/bpm; N=int(dur*SR); out=np.zeros((N,2))
    def add(x,at):
        if x.ndim==1: x=st(x)
        i=int(at*SR); j=min(N,i+len(x));
        if i<N: out[i:j]+=x[:j-i]
    def kick():
        tt=t(0.45); f=48+110*np.exp(-tt*35); return np.tanh(1.5*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*7))
    def hat(o=False):
        d=0.18 if o else 0.05; tt=t(d); return hp(rng.standard_normal(len(tt)),7000)*np.exp(-tt*(25 if o else 90))
    def snap():
        tt=t(0.25); return bp(rng.standard_normal(len(tt)),900,5000)*np.exp(-tt*28)
    chords=[[53,57,60,64,67],[50,53,57,60,64],[46,50,53,57,60],[48,52,55,60,62]]  # Fmaj9 Dm9 Bbmaj9 C6/9
    roots=[41,38,34,36]; mf=lambda m:440*2**((m-69)/12)
    pad=np.zeros((N,2)); bass=np.zeros(N); arp=np.zeros((N,2))
    nb=int(dur/b)+2
    for k in range(nb):
        T=k*b
        if T>=dur: break
        bar=(k//8)%4  # 2 bars per chord (8 beats)
        if T>=drop_at: add(kick()*0.9,T)
        add(hat()*0.25,T+b/2)
        if T>=drop_at:
            add(hat()*0.12,T+b/4); add(hat()*0.12,T+3*b/4)
            if k%2==1: add(snap()*0.35,T)
        if k%8==0:  # pad chord 8 beats
            d=min(8*b+0.5,dur-T); tt=t(d); env=np.minimum(1,tt/0.6)*np.minimum(1,(d-tt)/0.5)
            x=sum(np.sin(2*np.pi*mf(m)*tt+0.3*np.sin(2*np.pi*0.2*tt))+0.4*np.sin(2*np.pi*mf(m)*1.004*tt) for m in chords[bar])
            x=lp(x,1600)*env*0.12; i=int(T*SR); j=min(N,i+len(x)); pad[i:j,0]+=x[:j-i]; pad[i:j,1]+=np.roll(x,300)[:j-i]
        # bass: syncopated 8ths
        if T>=drop_at:
            for off,ln in [(0,0.3),(0.75*b,0.2)]:
                tt=t(ln); x=np.sin(2*np.pi*mf(roots[bar])*tt)*np.exp(-tt*5)*np.minimum(1,tt/0.005)
                i=int((T+off)*SR); j=min(N,i+len(x));
                if i<N: bass[i:j]+=x[:j-i]*0.45
        # arp pluck 16ths sparse
        pat=[0,None,2,None,4,3,None,1]
        for s in range(2):
            idx=pat[(k*2+s)%8]
            if idx is None: continue
            f=mf(chords[bar][idx]+12); x=bell(f,0.5,partials=((1,1),(2,.25)),decay=9)*0.08
            add(st(x,0.7*(1 if s else -1) if False else 0.6),T+s*b/2)
    out+=pad+st(bass)+verb(arp,0.4)[:N]
    out=verb(out*0.6,0.18)[:N]+out*0.4
    # intro filter sweep before drop
    pre=int(drop_at*SR); out[:pre]=lp(out[:pre],900)
    tt=t(dur); fade=np.clip((dur-tt)/end_fade,0,1); out*=fade[:,None]
    return out
def lufs(x): return pyln.Meter(SR).integrated_loudness(x)
if __name__=="__main__":
    voice_p,out_p,cue_p=sys.argv[1:4]; cues=json.load(open(cue_p))
    v,sr=sf.read(voice_p); assert sr==SR
    if v.ndim==1: v=st(v)
    V0=cues["voice_at"]; DUR=cues["duration"]; N=int(DUR*SR)
    voice=np.zeros((N,2)); i=int(V0*SR); voice[i:i+len(v)]=v[:N-i]
    voice*=10**((-14-lufs(voice[i:i+len(v)]))/20)
    sfx=np.zeros((N,2)); cache={}
    for c in cues["sfx"]:
        name,at,db=c
        if name not in cache: cache[name]=nrm(SFX[name](),-1)
        x=cache[name]*10**(db/20); i=int(at*SR); j=min(N,i+len(x)); sfx[i:j]+=x[:j-i]
    m=music(DUR,cues["drop_at"],cues["music_fade"]); m*=10**((-27-lufs(m))/20)
    # duck music under voice
    env=np.abs(voice).max(1); k=int(0.15*SR); env=np.convolve(env,np.ones(k)/k,'same'); env=env/(env.max()+1e-9)
    duck=1-0.45*np.clip(env*6,0,1); m*=duck[:,None]
    mix=voice+sfx+m
    mix*=10**((-13.5-lufs(mix))/20)
    # soft limiter at -1 dBFS
    lim=10**(-1/20); g=np.ones(N); pk=np.abs(mix).max(1)
    over=pk>lim; g[over]=lim/pk[over]
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    g=uniform_filter1d(minimum_filter1d(np.where(over,lim/pk,1.0),int(0.01*SR)),int(0.005*SR))
    mix*=g[:,None]; mix=np.clip(mix,-lim,lim)
    sf.write(out_p,mix.astype(np.float32),SR,subtype="FLOAT")
    print("LUFS mix",round(lufs(mix),2),"voice",round(lufs(voice[int(V0*SR):int(V0*SR)+len(v)]),2),"peak",round(20*np.log10(np.abs(mix).max()),2))
