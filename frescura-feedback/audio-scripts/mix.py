import numpy as np, soundfile as sf, json
from scipy.signal import butter, sosfilt
SR=48000; rng=np.random.default_rng(11)
T=json.load(open("timeline.json"))["T"]; N=int(T["total"]*SR)
tt=lambda d: np.arange(int(d*SR))/SR
def bp(x,lo,hi): return sosfilt(butter(2,[lo,hi],btype='band',fs=SR,output='sos'),x)
def hp(x,f): return sosfilt(butter(2,f,btype='high',fs=SR,output='sos'),x)
def lp(x,f): return sosfilt(butter(2,f,btype='low',fs=SR,output='sos'),x)
def bell(f,d,decay=6,parts=((1,1),(2.0,.4),(3.01,.2),(4.2,.1))):
    t=tt(d); x=sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-decay*m**.5*t) for m,a in parts); return x*np.minimum(1,t/0.003)
def whoosh(d=0.55,up=True):
    n=rng.standard_normal(int(d*SR)); y=np.zeros_like(n); s=1024
    for i in range(0,len(n),s):
        p=i/len(n); p=p if up else 1-p; fc=350+5000*p**1.6; y[i:i+s]=bp(n[i:i+s],fc*0.6,fc*1.5)
    t=tt(d); return y*np.sin(np.pi*t/d)**2
def impact():
    t=tt(1.3); f=95*np.exp(-t*9)+38; sub=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*3.2)
    cl=hp(rng.standard_normal(len(t)),1800)*np.exp(-t*60)*0.5; body=lp(rng.standard_normal(len(t)),400)*np.exp(-t*14)*0.6
    return np.tanh((sub+cl+body)*1.6)
def riser(d=1.3):
    t=tt(d); n=rng.standard_normal(len(t)); y=np.zeros_like(n); s=1024
    for i in range(0,len(n),s):
        p=i/len(n); fc=500+7000*p**2; y[i:i+s]=bp(n[i:i+s],fc*0.7,fc*1.4)
    tone=np.sin(2*np.pi*np.cumsum(300+900*(t/d)**2)/SR)*0.25
    return (y+tone)*(t/d)**2.2
def pop(f0=900):
    t=tt(0.13); f=f0*np.exp(-t*30)+200; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*38)
def click():
    t=tt(0.05); return (hp(rng.standard_normal(len(t)),2500)*np.exp(-t*220)+np.sin(2*np.pi*1900*t)*np.exp(-t*120))
def tick():
    t=tt(0.06); return np.sin(2*np.pi*2400*t)*np.exp(-t*110)+0.4*np.sin(2*np.pi*4800*t)*np.exp(-t*150)
def sparkle(d=0.9,n=16):
    x=np.zeros(int(d*SR)+SR//2)
    for k in range(n):
        o=int(rng.uniform(0,d*0.8)*SR); b=bell(rng.uniform(2600,6200),0.35,14,((1,1),(2.01,.3))); x[o:o+len(b)]+=b*rng.uniform(.4,1)
    return hp(x,1500)
def squish():
    d=0.55; t=tt(d); n=rng.standard_normal(len(t)); y=np.zeros_like(n); s=512
    for i in range(0,len(n),s):
        p=i/len(n); fc=900+1800*np.sin(np.pi*p); y[i:i+s]=bp(n[i:i+s],fc*0.5,fc*1.8)
    am=0.6+0.4*np.sin(2*np.pi*38*t); env=np.minimum(1,t/0.04)*np.exp(-t*4.5)
    th=np.sin(2*np.pi*np.cumsum(140*np.exp(-t*8)+60)/SR)*np.exp(-t*18)*0.8
    return y*am*env+th
def kaching():
    x=np.zeros(int(1.3*SR)); c=click(); x[:len(c)]+=c*0.8
    for o,f in ((0.07,2093),(0.16,2637),(0.16,3136)):
        b=bell(f,1.0,5,((1,1),(2.4,.35),(3.9,.15))); i=int(o*SR); x[i:i+len(b)]+=b
    return x
def chord(fs,d=1.6):
    x=np.zeros(int(d*SR))
    for i,f in enumerate(fs):
        b=bell(f,d-0.1*i,3.2); o=int(i*0.06*SR); x[o:o+len(b)]+=b
    return x
def nm(x,db): return x/np.max(np.abs(x))*10**(db/20)
L=np.zeros(N+SR*3); R=np.zeros(N+SR*3)
def put(x,t,db,pan=0.0):
    x=nm(x,db); i=max(0,int(t*SR)); L[i:i+len(x)]+=x*np.sqrt((1-pan)/2)*1.414; R[i:i+len(x)]+=x*np.sqrt((1+pan)/2)*1.414
A1,A2,A3=T["A1"][0],T["A2"][0],T["A3"][0]; FS=T["fb_start"]; F2,F3,F4=T["F2"][0],T["F3"][0],T["F4"][0]
ES=T["edu_start"]; C1,C2,C3,C4,C5=[T[k][0] for k in("C1","C2","C3","C4","C5")]; EN=T["end_start"]
put(impact(),0.0,-5); put(whoosh(0.5),0.0,-11,-.3)
for i,t in enumerate((0.55,0.95,1.35,1.75)): put(tick(),t,-20,(-.4,.4)[i%2])
put(whoosh(0.45),A2-0.2,-9,.3); put(pop(),A2+0.05,-9)
put(pop(700),A3+0.05,-10); put(riser(1.5),FS-1.5,-9)
put(impact(),FS,-6); put(whoosh(0.5,False),FS,-11); put(click(),FS+0.35,-10); put(pop(1100),FS+0.55,-12)
put(sparkle(1.0),F2+0.05,-10); put(bell(1568,1.0,5),F2+0.05,-12)
for i,(dt,f) in enumerate(((1.55,1318.5),(2.2,1568),(2.95,2093))): put(bell(f,0.9,6),F2+dt,-9,(-.5,0,.5)[i]); put(pop(900+200*i),F2+dt,-12)
put(whoosh(0.4),F3-0.15,-13,-.3); put(pop(600),F3+0.1,-11)
put(pop(1000),F4+0.2,-9); put(sparkle(0.8,12),F4+0.2,-12)
put(whoosh(0.4,False),F4+1.45,-11,.4); put(bell(2093,1.0,5),F4+1.65,-10)
put(chord((1046.5,1318.5,1568),1.2),F4+2.35,-13)
put(whoosh(0.55),ES-0.25,-8); put(impact(),ES,-9)
put(squish(),ES+0.45,-6); put(squish(),ES+1.25,-9)
for i,dt in enumerate((0.95,1.65,2.35)): put(pop(800+250*i),ES+dt,-8,(-.4,.4,-.4)[i]); put(tick(),ES+dt+0.04,-14)
put(sparkle(0.8),ES+2.6,-12)
put(whoosh(0.5),C1-0.3,-8,-.3); put(chord((880,1108.7,1318.5,1760),1.6),C1,-9)
put(whoosh(0.4,False),C2-0.15,-11,.3); put(impact(),C2,-10)
n=9
for i in range(n): put(tick(),C2+0.25+2.1*(1-(1-i/(n-1))**1.0)*0.95 if False else C2+0.3+i*0.24,-13+i*0.5,(-.5,.5)[i%2])
put(bell(740,0.5,9),C2+1.0,-11); put(bell(622,0.6,9),C2+1.18,-11)
put(whoosh(0.3),C3-0.2,-10); put(click(),C3+0.3,-6); put(bell(1760,0.9,5),C3+0.32,-9)
put(pop(1000),C4,-8); put(click(),C4+0.5,-6); put(pop(1300),C4+0.52,-10)
put(whoosh(0.4),C5-0.1,-12); put(kaching(),C5+0.95,-6); put(sparkle(0.9),C5+1.0,-13)
put(impact(),EN,-6); put(riser(0.6),EN-0.6,-12); put(sparkle(1.4,22),EN+0.1,-11); put(chord((523.25,783.99,1046.5,1318.5,1568),2.3),EN+0.05,-9)
sfx=np.stack([L,R],1)[:N]
# soft bed: pad + pulse (116 bpm)
bpm=116; beat=60/bpm; t=np.arange(N)/SR; bed=np.zeros(N)
chords=[(110,164.81,220,261.63,329.63),(87.31,130.81,174.61,220,261.63),(130.81,196,261.63,329.63,392),(98,146.83,196,246.94,293.66)]
bar=beat*4
for k in range(int(T["total"]/bar)+1):
    s=int(k*bar*SR); e=min(N,int((k+1)*bar*SR)+SR//4); 
    if s>=N: break
    tl=np.arange(e-s)/SR; env=np.minimum(1,tl/0.4)*np.minimum(1,(tl[-1]-tl)/0.3+0.001)
    c=sum(np.sin(2*np.pi*f*tl)+0.3*np.sin(2*np.pi*2*f*tl+0.5) for f in chords[k%4])
    bed[s:e]+=c*env*0.12
bed=lp(bed,1800)
kick=np.zeros(N); kt=tt(0.25); kk=np.sin(2*np.pi*np.cumsum(120*np.exp(-kt*22)+45)/SR)*np.exp(-kt*13)
hat=hp(rng.standard_normal(int(0.04*SR)),7000)*np.exp(-tt(0.04)*120)
for b in range(int(T["total"]/beat*2)):
    i=int(b*beat/2*SR)
    if b%2==0 and i+len(kk)<N: kick[i:i+len(kk)]+=kk*(0.9 if b%8==0 else 0.6)
    if b%2==1 and i+len(hat)<N: kick[i:i+len(hat)]+=hat*0.18
    # pluck arpeggio
    ch=chords[int(b*beat/2/bar)%4]; f=ch[2+(b%3)]*2; p=bell(f,0.3,12,((1,1),(2,.2)))
    if i+len(p)<N: kick[i:i+len(p)]+=p*0.10
music=bed+kick*0.5
fade=np.minimum(1,t/0.5)*np.minimum(1,(T["total"]-t)/1.5); music*=fade
# duck under feedback (noisier voice) a bit more
duck=np.ones(N); a,b=int(FS*SR),int(T["fb_end"]*SR); duck[a:b]=0.7
music=nm(music*duck,-17)
voice=sf.read("au/voice_track.wav")[0][:N]; voice=np.pad(voice,(0,N-len(voice)))
sf.write("au/voice_st.wav",np.stack([voice,voice],1).astype(np.float32),SR)
sf.write("au/sfx.wav",sfx.astype(np.float32),SR); sf.write("au/music.wav",np.stack([music,music],1).astype(np.float32),SR)
