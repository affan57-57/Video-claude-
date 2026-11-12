# Synthesized modern-luxury SFX + minimal music bed (48k stereo)
import numpy as np, soundfile as sf, sys, os
from scipy.signal import butter, sosfilt
SR=48000; out=sys.argv[1]; os.makedirs(out,exist_ok=True); R=np.random.default_rng(11)
T=lambda d: np.arange(int(d*SR))/SR
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],btype='band',fs=SR,output='sos'),x,axis=0)
def lp(x,f,o=2): return sosfilt(butter(o,f,btype='low',fs=SR,output='sos'),x,axis=0)
def hp(x,f,o=2): return sosfilt(butter(o,f,btype='high',fs=SR,output='sos'),x,axis=0)
def st(x,w=0.0):
    d=int(0.008*SR*w); L=x; Rr=np.concatenate([np.zeros(d),x])[:len(x)] if d else x; return np.stack([L,Rr],1)
def norm(x,db=-1): return x/(np.max(np.abs(x))+1e-9)*10**(db/20)
def verb(x,dec=1.2,mix=.25):
    n=int(dec*SR); ir=R.standard_normal((n,2))*np.exp(-np.arange(n)/SR*6/dec)[:,None]; ir=lp(hp(ir,300),7000)
    y=np.stack([np.convolve(x[:,c],ir[:,c])[:len(x)+n] for c in range(2)],1)/40; y=np.vstack([y,np.zeros((len(x)+n-len(y),2))])
    xx=np.vstack([x,np.zeros((n,2))]); return xx*(1-mix)+y*mix*np.max(np.abs(xx))/(np.max(np.abs(y))+1e-9)
def bell(f,d,dec=5,parts=((1,1),(2.76,.35),(5.4,.15),(8.9,.06))):
    t=T(d); return sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-dec*m**.4*t) for m,a in parts)*np.minimum(1,t/0.002)
S={}
# impact: sub drop + noise thump
t=T(1.6); sub=np.sin(2*np.pi*np.cumsum(48+70*np.exp(-t*9))/SR)*np.exp(-t*2.6)
nz=lp(R.standard_normal(len(t)),900)*np.exp(-t*14)*.6
S['impact']=verb(st(np.tanh(1.6*(sub+nz))),1.4,.18)
# riser (reverse-swell noise + rising tone) 1.2s
t=T(1.2); n=R.standard_normal(len(t)); y=np.zeros_like(n)
for i in range(0,len(n),1024):
    p=i/len(n); fc=400+6000*p**2; y[i:i+1024]=bp(n[i:i+1024],fc*.7,min(fc*1.4,20000))
tone=np.sin(2*np.pi*np.cumsum(200+900*(t/1.2)**2)/SR)*.25
S['riser']=st((y*.8+tone)*(t/1.2)**2.2,1)
# whoosh 0.55s, panned sweep
def whoosh(d=0.55,lo=250,hi=4200):
    t=T(d); n=R.standard_normal(len(t)); y=np.zeros_like(n)
    for i in range(0,len(n),512):
        p=i/len(n); fc=lo+(hi-lo)*np.sin(np.pi*p)**2; y[i:i+512]=bp(n[i:i+512],fc*.6,fc*1.5)
    env=np.sin(np.pi*t/d)**3; x=y*env; return np.stack([x*(1-t/d)+.25*x, x*(t/d)+.25*x],1)
S['whoosh']=whoosh(); S['whoosh_s']=whoosh(0.32,500,6000)
# tick: soft UI click
t=T(0.06); S['tick']=st(hp(np.sin(2*np.pi*2400*t)*np.exp(-t*160)+R.standard_normal(len(t))*np.exp(-t*400)*.3,800))
# pop (bubble)
def pop(f0=700):
    t=T(0.1); f=f0*(1+2.2*np.exp(-t*45)); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*42)
x=np.zeros(int(1.0*SR))
for k in range(9):
    o=int(R.uniform(0,.75)*SR); p=pop(R.uniform(500,1300)); x[o:o+len(p)]+=p*R.uniform(.4,1)
S['bubbles']=st(x,1)
# glass shimmer (luxury ting)
x=np.zeros(int(2.2*SR)); b=bell(2093,2.0,2.2); x[:len(b)]+=b
for k,f in enumerate([3136,4186,5274]):
    bb=bell(f,1.2,4)*.35; o=int((0.05+0.06*k)*SR); x[o:o+len(bb)]+=bb
S['shimmer']=verb(st(hp(x,600),1),1.8,.35)
# slam (word hit): short punchy low tom + click
t=T(0.5); tom=np.sin(2*np.pi*np.cumsum(90+160*np.exp(-t*30))/SR)*np.exp(-t*9)
S['slam']=verb(st(np.tanh(2*tom)+hp(R.standard_normal(len(t))*np.exp(-t*80),2000)*.4),.8,.15)
# tap (button)
t=T(0.12); S['tap']=st(np.sin(2*np.pi*np.cumsum(1400*np.exp(-t*20)+300)/SR)*np.exp(-t*55))
# success chime (checkout) two-note
x=np.zeros(int(1.6*SR)); a=bell(1567.98,1.2,3.5); b=bell(2349.3,1.3,3.2); x[:len(a)]+=a; o=int(.11*SR); x[o:o+len(b)]+=b
S['success']=verb(st(x,1),1.2,.25)
# soft swell (pad whoosh for reveals)
t=T(1.8); pad=sum(np.sin(2*np.pi*f*t+R.uniform(0,6)) for f in [261.6,329.6,392,493.9,587.3])
S['swell']=st(lp(pad,2500)*np.sin(np.pi*t/1.8)**2,1)
# camera shutter-ish snap for photo changes
t=T(0.09); S['snap']=st(bp(R.standard_normal(len(t)),1500,9000)*np.exp(-t*90)+np.sin(2*np.pi*180*t)*np.exp(-t*60)*.5)
for k,v in S.items(): sf.write(f'{out}/{k}.wav',norm(v,-1).astype(np.float32),SR)

# ---- music bed: 122 bpm minimal luxe house, Fm9-Dbmaj7-Abmaj7-Eb6
bpm=122; beat=60/bpm; dur=float(sys.argv[2]); N=int(dur*SR); m=np.zeros((N,2))
def add(sig,t0,g=1.0,pan=0.0):
    i=int(t0*SR); s=sig if sig.ndim==2 else np.stack([sig*(1-pan)**.5,sig*(1+pan)**.5],1); j=min(N,i+len(s))
    if i<N: m[i:j]+=s[:j-i]*g
kt=T(0.35); kick=np.sin(2*np.pi*np.cumsum(45+110*np.exp(-kt*28))/SR)*np.exp(-kt*7)
ht=T(0.05); hat=hp(R.standard_normal(len(ht)),7000)*np.exp(-ht*90)
ct=T(0.2); clap=bp(R.standard_normal(len(ct)),900,5000)*np.exp(-ct*25)
chords=[[174.6,207.7,261.6,311.1,392],[138.6,174.6,207.7,261.6,349.2],[207.7,261.6,311.1,392,523.3],[155.6,196,233.1,261.6,311.1]]
bass=[43.65,34.65,51.91,38.89]
bars=int(dur/(4*beat))+1
for b in range(bars):
    t0=b*4*beat; ch=chords[b%4]
    pt=T(4*beat); pad=sum(np.sin(2*np.pi*f*pt)+.3*np.sin(2*np.pi*f*2.003*pt) for f in ch)/len(ch)
    pad=lp(pad,1800)*np.minimum(1,pt/0.4)*np.minimum(1,(4*beat-pt)/0.3)
    add(st(pad,1),t0,.16)
    for q in range(4):
        tb=t0+q*beat
        if b>0 or q>=2: add(kick,tb,.75)
        add(hat,tb+beat/2,.18,.3)
        if q in(1,3): add(clap,tb,.16,-.2)
        bt=T(beat*.45); bs=np.sin(2*np.pi*bass[b%4]*2*bt)*np.exp(-bt*4)
        add(bs,tb+beat/2,.35)
    # pluck arpeggio sixteenths every other bar
    if b%2==1:
        for s in range(8):
            f=ch[[0,2,4,2,1,3,4,3][s]]*2; pl=bell(f,0.4,9,((1,1),(2,.2)))
            add(pl,t0+s*beat/2,.07,(-.5 if s%2 else .5))
m=lp(m,12000); m=np.tanh(m*1.2)
fade=np.ones(N); fl=int(1.2*SR); fade[-fl:]=np.linspace(1,0,fl); fade[:int(.05*SR)]=np.linspace(0,1,int(.05*SR))
sf.write(f'{out}/music.wav',norm(m*fade[:,None],-1).astype(np.float32),SR)
print('ok',list(S))
