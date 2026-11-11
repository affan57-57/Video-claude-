# Synth SFX + minimal luxury house bed, then mix with studio voice (ducking) -> mix.wav
import numpy as np, soundfile as sf, json, sys
from scipy.signal import butter, sosfilt, sosfiltfilt
SR = 48000
rng = np.random.default_rng(42)
voice_path, cues_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
cues = json.load(open(cues_path)); TOTAL = cues["total"]
def t(d): return np.arange(int(d*SR))/SR
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],btype='band',fs=SR,output='sos'),x)
def lp(x,f,o=2): return sosfilt(butter(o,f,btype='low',fs=SR,output='sos'),x)
def hp(x,f,o=2): return sosfilt(butter(o,f,btype='high',fs=SR,output='sos'),x)
def nrm(x,db=-1): return x/(np.max(np.abs(x))+1e-9)*10**(db/20)
def st(x,w=0.0):
    if x.ndim==2: return x
    d=int(0.007*SR); R=np.concatenate([np.zeros(d),x])[:len(x)]
    return np.stack([x,(1-w)*x+w*R],1)
def verb(x,dec=1.2,mix=.25):
    L=int(dec*SR); ir=rng.standard_normal(L)*np.exp(-np.arange(L)/SR*(6.9/dec)); ir=lp(ir,6000)
    from scipy.signal import fftconvolve
    if x.ndim==1: x=st(x,.6)
    y=np.stack([fftconvolve(x[:,0],ir)[:len(x)], fftconvolve(x[:,1],np.roll(ir,331))[:len(x)]],1)
    y=nrm(y,-1)*mix; return x*(1-mix)+y
def bell(f,d,dec=6,parts=((1,1),(2.0,.35),(3.0,.15),(4.24,.08))):
    tt=t(d); return sum(a*np.sin(2*np.pi*f*m*tt)*np.exp(-dec*m**.5*tt) for m,a in parts)*np.minimum(1,tt/.002)
def sweep_noise(d,f0,f1,q=.5):
    n=rng.standard_normal(int(d*SR)); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        p=i/len(n); fc=f0*(f1/f0)**p
        y[i:i+seg]=sosfilt(butter(2,[max(40,fc*(1-q)),min(20000,fc*(1+q))],btype='band',fs=SR,output='sos'),n[i:i+seg])
    return y

S = {}
def whoosh(d=.55, rev=False):
    tt=t(d); env=np.sin(np.pi*np.clip(tt/d,0,1))**3
    y=sweep_noise(d,250,5000,.6)*env
    L=y*np.linspace(1.3,.3,len(y)); R=y*np.linspace(.3,1.3,len(y)); x=np.stack([L,R],1)
    return verb(x,.6,.2)
S['whoosh']=whoosh(.5); S['whoosh2']=whoosh(.42)[:, ::-1].copy()
S['swoosh_card']=verb(st(sweep_noise(.35,3000,600,.5)*np.sin(np.pi*t(.35)/.35)**2,.5),.5,.15)
def impact(d=1.6,soft=False):
    tt=t(d); f=55*np.exp(-tt*3)+38; ph=2*np.pi*np.cumsum(f)/SR
    sub=np.sin(ph)*np.exp(-tt*(3.5 if not soft else 5))
    click=hp(rng.standard_normal(len(tt)),2000)*np.exp(-tt*90)*(.5 if not soft else .2)
    body=lp(rng.standard_normal(len(tt)),900)*np.exp(-tt*14)*(.6 if not soft else .3)
    return verb(st(sub+click+body,.3),1.4,.18)
S['impact']=impact(); S['impact_soft']=impact(1.2,True)
S['tink']=verb(st(bell(2637,1.2,5)+.6*bell(3951,1.2,7)),1.5,.35)
S['ding']=verb(st(bell(1567.98,1.2,4)+bell(2093,1.2,4)*.6),1.4,.3)
def pop():
    tt=t(.14); f=1100*np.exp(-tt*35)+250; return st(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*38))
S['pop']=verb(pop(),.4,.12)
def tick():
    tt=t(.06); return st(hp(rng.standard_normal(len(tt)),3000)*np.exp(-tt*180)+np.sin(2*np.pi*3200*tt)*np.exp(-tt*120)*.5)
S['tick']=tick()
def click():
    tt=t(.12); x=np.sin(2*np.pi*1800*tt)*np.exp(-tt*90)+hp(rng.standard_normal(len(tt)),4000)*np.exp(-tt*250)*.8
    return verb(st(x),.3,.1)
S['click']=click()
def shimmer(d=1.4,n=26,lo=3000,hi=8000):
    x=np.zeros(int(d*SR)+SR//2)
    for k in range(n):
        o=int((k/n)**1.2*d*.85*SR); b=bell(rng.uniform(lo,hi),.5,14,((1,1),(2.01,.25)))*rng.uniform(.4,1)*(1-k/n*.5); x[o:o+len(b)]+=b
    return verb(st(hp(x,1500),.8),1.6,.4)
S['shimmer']=shimmer(); S['sparkle']=shimmer(.8,18,4000,9000)
def riser(d=1.0):
    tt=t(d); y=sweep_noise(d,400,9000,.3)*(tt/d)**2; tone=np.sin(2*np.pi*np.cumsum(200+800*(tt/d)**2)/SR)*(tt/d)**3*.3
    return verb(st(y+tone,.6),.8,.25)
S['riser_short']=riser(.9)
def stamp():
    tt=t(.5); x=lp(rng.standard_normal(len(tt)),1500)*np.exp(-tt*30)+np.sin(2*np.pi*90*tt)*np.exp(-tt*16)
    return verb(st(x),.5,.15)
S['stamp']=stamp()
def wave(d=2.2):
    tt=t(d); n=lp(rng.standard_normal(len(tt)),2500)*(np.sin(np.pi*tt/d)**2)*(0.6+0.4*np.sin(2*np.pi*tt*1.1))
    return verb(st(n,.8),1.2,.3)
S['wave']=wave()
def bubbles(d=1.6,n=22):
    x=np.zeros(int(d*SR)+SR//4)
    for k in range(n):
        o=int(rng.uniform(0,d)*SR); L=int(.05*SR); tt=np.arange(L)/SR; f0=rng.uniform(500,1600)
        b=np.sin(2*np.pi*np.cumsum(f0*(1+tt*30))/SR)*np.exp(-tt*70)*rng.uniform(.3,1); x[o:o+L]+=b
    return verb(st(x,.7),.5,.2)
S['bubbles']=bubbles()
def night():
    x=np.zeros(int(2.2*SR))
    for i,f in enumerate([783.99,1174.66,1567.98,2349.3]):
        b=bell(f,1.8,3); o=int(i*.12*SR); x[o:o+len(b)]+=b[:len(x)-o]
    return verb(st(x,.8),2.2,.5)
S['night']=night()
def alarm():
    x=np.zeros(int(.7*SR))
    for o in (0,.22):
        b=bell(1318.5,.25,10,((1,1),(2,.3))); i=int(o*SR); x[i:i+len(b)]+=b
    return st(x)
S['alarm']=alarm()
def drain(d=1.3):
    tt=t(d); f=900*np.exp(-tt*1.6)+120; return verb(st(np.sin(2*np.pi*np.cumsum(f)/SR)*.35*np.minimum(1,(d-tt)/.2)+bp(rng.standard_normal(len(tt)),300,2000)*.15*np.exp(-tt)),.6,.2)
S['drain']=drain()
def bounce():
    tt=t(.35); f=300+500*np.abs(np.sin(tt*28))*np.exp(-tt*6); return verb(st(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*8)),.4,.15)
S['bounce']=bounce()
def cash():
    x=np.zeros(int(1.2*SR)); a=bell(2093,1.0,5); b=bell(2637,1.0,5)
    x[:len(a)]+=a; o=int(.09*SR); x[o:o+len(b)]+=b[:len(x)-o]
    tt=t(.08); x[:len(tt)]+=hp(rng.standard_normal(len(tt)),5000)*np.exp(-tt*80)*.6
    return verb(st(x,.6),1.0,.3)
S['cash']=cash()

# ---------------- music bed: minimal luxe house, 118 BPM, Dm9 - Bbmaj7 - Gm9 - A7sus ----------------
BPM=118; beat=60/BPM; N=int(TOTAL*SR)+SR
mus=np.zeros((N,2))
def place(buf,x,at,g=1.0):
    i=int(at*SR)
    if i>=len(buf): return
    if x.ndim==1: x=np.stack([x,x],1)
    n=min(len(x),len(buf)-i); buf[i:i+n]+=x[:n]*g
def kick():
    tt=t(.45); f=48+110*np.exp(-tt*28); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*7.5)+hp(rng.standard_normal(len(tt)),3000)*np.exp(-tt*300)*.2
def hat(open_=False):
    tt=t(.25 if open_ else .05); return hp(rng.standard_normal(len(tt)),8000)*np.exp(-tt*(18 if open_ else 140))
def clap():
    tt=t(.3); n=bp(rng.standard_normal(len(tt)),900,5000); env=np.exp(-tt*22)
    for d in (.0,.011,.022): env+=np.exp(-np.maximum(0,tt-d)*120)*(tt>=d)*.6
    return n*env*.6
def snap():
    tt=t(.08); return bp(rng.standard_normal(len(tt)),1800,6000)*np.exp(-tt*80)
KICK,HAT,OH,CLAP=kick(),hat(),hat(True),clap()
def midi(n): return 440*2**((n-69)/12)
CH=[[50,57,60,64,65+4],[46,53,57,62,65],[43,50,53,58,62],[45,52,55,59,64]]  # D-Bb-G-A voicings
def epiano(f,d):
    tt=t(d); mod=np.sin(2*np.pi*f*14*tt)*np.exp(-tt*6)*1.2
    return np.sin(2*np.pi*f*tt+mod)*np.exp(-tt*1.4)*np.minimum(1,tt/.004)
def pad(freqs,d):
    tt=t(d); x=sum(np.sin(2*np.pi*f*tt+0.3*np.sin(2*np.pi*.4*tt+k))+np.sin(2*np.pi*f*1.003*tt) for k,f in enumerate(freqs))
    env=np.minimum(1,tt/.6)*np.minimum(1,(d-tt)/.6); return lp(x*env,2200)
bars=int(TOTAL/(4*beat))+2
start_drums=0.0
for b in range(bars):
    t0=b*4*beat; ch=CH[b%4]
    place(mus,st(pad([midi(n) for n in ch[1:]],4*beat)*.05,.8),t0)
    # e-piano stabs syncopated
    for off in (0.0,1.5,2.5,3.5):
        for n in ch[1:]: place(mus,st(epiano(midi(n+12),.8)*.035,.4),t0+off*beat)
    # sub bass
    for off,ln in ((0,.4),(.75,.2),(1.5,.4),(2.5,.4),(3.25,.2)):
        tt=t(ln*beat*1.6); bs=np.sin(2*np.pi*midi(ch[0]-12)*tt)*np.minimum(1,(ln*beat*1.6-tt)/.03)*np.minimum(1,tt/.005)
        place(mus,bs*.22,t0+off*beat)
    for k in range(4):
        tb=t0+k*beat
        place(mus,KICK*.55,tb)
        place(mus,st(HAT*.10,.3),tb+beat/2); place(mus,st(HAT*.05,.3),tb+beat/4*3)
        if k%2==1: place(mus,st(CLAP*.22,.6),tb)
        if k==3: place(mus,st(OH*.06,.5),tb+beat/2)
        place(mus,st(snap()*.04,.5),tb+beat/4)
# sidechain pump from kick grid
tt=np.arange(N)/SR; ph=(tt%beat)/beat; pump=np.minimum(1,0.35+ph*2.2)
mus[:,0]*=pump; mus[:,1]*=pump
mus=lp(mus.T,14000).T

# ---------------- voice + ducking ----------------
v,vsr=sf.read(voice_path); assert vsr==SR
if v.ndim==2: v=v.mean(1)
voice=np.zeros(N); i=int(cues["voice_at"]*SR); voice[i:i+len(v)]=v[:N-i]
# envelope follower for ducking
e=np.abs(voice); e=sosfiltfilt(butter(2,6,fs=SR,output='sos'),e); e=e/(e.max()+1e-9)
duck=1-0.62*np.clip(e*4,0,1)
mus*=duck[:,None]
# music: intro hit at 0, gentle outro
fade=np.ones(N); o=int((TOTAL-1.6)*SR); fade[o:]=np.linspace(1,0,N-o)
mus*=fade[:,None]
mus=nrm(mus,-1)*10**(-17/20)   # bed level

sfxbus=np.zeros((N,2))
for at,name,g in cues["sfx"]:
    x=nrm(S[name],-1)*10**((g-6)/20); place(sfxbus,x,at)
mix=np.stack([voice,voice],1)*10**(0/20)*0.92+mus+sfxbus
mix=mix[:int(TOTAL*SR)]
sf.write(out.replace('.wav','_pre.wav'),mix.astype(np.float32),SR,subtype='FLOAT')
print("pre-mix written")
