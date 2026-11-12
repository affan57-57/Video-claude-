import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
SR=48000; R=np.random.default_rng(11); O="/home/user/work/aud/"
T=lambda d: np.arange(int(d*SR))/SR
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],btype='band',fs=SR,output='sos'),x,axis=0)
def lp(x,f,o=2): return sosfilt(butter(o,f,btype='low',fs=SR,output='sos'),x,axis=0)
def hp(x,f,o=2): return sosfilt(butter(o,f,btype='high',fs=SR,output='sos'),x,axis=0)
def nz(d): return R.standard_normal(int(d*SR))
def st(x,w=0.0):
    L=x; Rr=np.roll(x,int(w*SR)) if w else x; return np.stack([L,Rr],1)
def norm(x,db=-1): return x/(np.max(np.abs(x))+1e-9)*10**(db/20)
def sweep_noise(d,f0,f1,q=0.5):
    n=nz(d); y=np.zeros_like(n); seg=512
    for i in range(0,len(n),seg):
        p=i/len(n); fc=f0*(f1/f0)**p
        y[i:i+seg]=sosfilt(butter(2,[fc*(1-q),fc*(1+q)],btype='band',fs=SR,output='sos'),n[i:i+seg])
    return y
sfx={}
# whoosh: up-down sweep, stereo pan
d=0.55; t=T(d); w=sweep_noise(d,400,5000)*np.sin(np.pi*t/d)**2
sfx['whoosh']=np.stack([w*(1-t/d)+.3*w, w*(t/d)+.3*w],1)
d=0.9; t=T(d); w=sweep_noise(d,6000,300)*np.sin(np.pi*t/d)**1.5
sfx['whoosh_down']=np.stack([w*(t/d)+.3*w, w*(1-t/d)+.3*w],1)
# impact: sub drop + noise burst + tail
d=2.2; t=T(d); f=90*np.exp(-t*6)+38; sub=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.2)
burst=lp(nz(d),2500)*np.exp(-t*14); tail=bp(nz(d),200,1200)*np.exp(-t*3)*0.25
sfx['impact']=st(sub*1.0+burst*0.5+tail,0.008)
# riser: 1.2s rising noise + rising tone
d=1.2; t=T(d); env=(t/d)**2.2; tone=np.sin(2*np.pi*np.cumsum(200*(8**(t/d)))/SR)*0.25
sfx['riser']=st((sweep_noise(d,300,9000,0.4)+tone)*env,0.012)
# tick: tiny UI click
d=0.06; t=T(d); sfx['tick']=st(np.sin(2*np.pi*2400*t)*np.exp(-t*120)+hp(nz(d),3000)*np.exp(-t*250)*.4)
# pop
d=0.14; t=T(d); f=1100*np.exp(-t*35)+220; sfx['pop']=st(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*38))
# bell helper
def bell(f,d,dec=5,parts=((1,1),(2.0,.45),(3.01,.22),(4.17,.12))):
    t=T(d); return sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-dec*m**.5*t) for m,a in parts)*np.minimum(1,t/0.002)
# shimmer / sparkle
x=np.zeros(int(1.6*SR))
for k in range(22):
    o=int(R.uniform(0,1.0)*SR); b=bell(R.uniform(3000,7500),0.5,dec=12,parts=((1,1),(2.01,.3))); x[o:o+len(b)]+=b*R.uniform(.3,1)
sfx['shimmer']=st(hp(x,2000),0.013)
# ding (luxury chime)
x=bell(1568,1.6,dec=3.2)+0.6*np.pad(bell(2093,1.4,dec=3.6),(int(.09*SR),int(.2*SR)))[:int(1.6*SR)]
sfx['ding']=st(x,0.01)
# cross / error soft (low double tone)
d=0.35; t=T(d); x=np.sin(2*np.pi*330*t)*np.exp(-t*12); x2=np.pad(np.sin(2*np.pi*262*t)*np.exp(-t*10),(int(.11*SR),0))[:len(t)]
sfx['nope']=st((x+x2)*.7)
# tap (phone)
d=0.08; t=T(d); sfx['tap']=st(lp(nz(d),4000)*np.exp(-t*90)+np.sin(2*np.pi*180*t)*np.exp(-t*60))
# swipe (short whoosh)
d=0.3; t=T(d); w=sweep_noise(d,1500,7000,0.5)*np.sin(np.pi*t/d)**2; sfx['swipe']=st(w,0.006)
# bubble pops for foam
x=np.zeros(int(1.2*SR))
for k in range(14):
    o=int(R.uniform(0,0.9)*SR); dd=0.05; tt=T(dd); f=R.uniform(500,1600)*(1+3*tt/dd)
    b=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*70); x[o:o+len(b)]+=b*R.uniform(.3,1)
sfx['bubbles']=st(x,0.009)
# ka-ching
x=bell(2637,1.0,dec=6)+np.pad(bell(3520,0.9,dec=6),(int(.07*SR),int(.1*SR)))[:int(1.0*SR)]
x[:int(.03*SR)]+=hp(nz(.03),3000)*0.6
sfx['kaching']=st(x,0.01)
# heartbeat thump (hook)
d=0.5; t=T(d); h=np.sin(2*np.pi*55*t)*np.exp(-t*18); h2=np.pad(np.sin(2*np.pi*50*t)*np.exp(-t*20),(int(.18*SR),0))[:len(t)]*.7
sfx['thump']=st(lp(h+h2,300))
# glitch/stutter for hook word
d=0.25; t=T(d); g=np.sign(np.sin(2*np.pi*40*t))*hp(nz(d),800)*0.5*np.exp(-t*8); sfx['glitch']=st(g,0.004)
# typewriter-ish soft key
for k,v in sfx.items():
    sf.write(O+k+'.wav',norm(v.astype(np.float64),-1).astype(np.float32),SR)

# ---------------- MUSIC: 122 bpm luxury deep house ----------------
BPM=122; B=60/BPM; DUR=37.6; N=int(DUR*SR); m=np.zeros((N,2))
DROP=4.35; first=DROP-int(DROP/B)*B  # beat grid aligned to drop
beats=np.arange(first,DUR,B)
def add(x,t0,g=1.0,pan=0.0):
    i=int(t0*SR); 
    if i>=N: return
    x=x[:N-i]
    if x.ndim==1: x=np.stack([x*(1-pan)**.5,x*(1+pan)**.5],1)
    m[i:i+len(x)]+=x*g
kt=T(0.45); kick=np.sin(2*np.pi*np.cumsum(120*np.exp(-kt*25)+45)/SR)*np.exp(-kt*7)+0.1*hp(nz(.45),2000)*np.exp(-kt*80)
ht=T(0.12); hat=hp(nz(.12),7000)*np.exp(-ht*40)
ot=T(0.3); ohat=hp(nz(.3),6000)*np.exp(-ot*12)
ct=T(0.25); clap=bp(nz(.25),900,4000)*(np.exp(-ct*25)+0.5*np.exp(-np.maximum(ct-0.012,0)*25)*(ct>0.012))
# chords: Am9 - Fmaj7 - C/E - G6  (one per bar)
def hz(n): return 440*2**((n-69)/12)
prog=[(45,[57,60,64,67,71]),(41,[53,57,60,64]),(48,[52,55,60,64]),(43,[55,59,62,64])]
bar=4*B
def pad(notes,d):
    t=T(d); x=np.zeros(len(t))
    for n in notes:
        for det in (-0.07,0.07):
            f=hz(n+det); x+=2*(t*f%1)-1
    x=lp(x,1400); env=np.minimum(1,t/0.3)*np.minimum(1,(d-t)/0.4); return x*env/len(notes)
def bassnote(n,d):
    t=T(d); f=hz(n); x=np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*2*f*t); return x*np.minimum(1,t/0.01)*np.exp(-t*3)
def pluck(n,d=0.3):
    t=T(d); f=hz(n); x=(2*(t*f%1)-1); x=lp(x,3000); return x*np.exp(-t*12)
END=34.6
for bi,b0 in enumerate(np.arange(first-4*bar if first-4*bar>-bar else first,DUR,bar)):
    pass
bars=np.arange(first%bar - bar, DUR, bar)
for k,b0 in enumerate(bars):
    root,ch=prog[k%4]
    if b0+bar<0: continue
    p=pad(ch,bar+0.3); 
    if b0<0: p=p[int(-b0*SR):]; t0=0
    else: t0=b0
    add(p,t0,0.55 if b0<DROP else 0.42,0)
for i,bt in enumerate(beats):
    if bt>END+0.6: break
    k=int(round((bt-first)/B)); inbar=k%4
    pre = bt<DROP-0.01
    if pre:
        if bt>DROP-2.1: add(hat,bt+B/2,0.18,0.3)  # build hats
        continue
    if bt<END: add(kick,bt,0.9)
    if bt<END: add(ohat,bt+B/2,0.22,0.25)
    if bt<END: add(hat,bt+B/4,0.10,-0.3); add(hat,bt+3*B/4,0.08,-0.3)
    if inbar in (1,3) and bt<END: add(clap,bt,0.35,0.1)
    root,ch=prog[((k)//4 - int(round((first%bar - bar - first)/bar)))%4] if False else prog[int(np.floor((bt-bars[0])/bar+1e-6))%4]
    if bt<END: add(bassnote(root-12+12,B*0.9),bt+B/2,0.5)
    # arp plucks 16th, sparse
    if bt<END:
        for s in range(2):
            n=ch[(k*2+s)%len(ch)]+12
            add(pluck(n),bt+s*B/2,0.12,0.4 if s else -0.4)
# filtered intro: lowpass first DROP seconds
i=int(DROP*SR); m[:i]=lp(m[:i],900)
# final hit + tail
add(kick,END,1.0); 
mm=m/np.max(np.abs(m))*10**(-3/20)
sf.write(O+'music.wav',mm.astype(np.float32),SR); print('music',len(mm)/SR,'first beat',first)
