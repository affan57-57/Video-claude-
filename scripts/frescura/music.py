import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
SR=48000; BPM=112; B=60/BPM; DUR=32.0; N=int(DUR*SR); R=np.random.default_rng(3)
L=np.zeros(N); Rr=np.zeros(N)
def add(x,t,g=1,pan=0):
    i=int(t*SR); x=x[:max(0,N-i)]; L[i:i+len(x)]+=x*g*(1-pan)**.5; Rr[i:i+len(x)]+=x*g*(1+pan)**.5
def lp(x,f): return sosfilt(butter(2,f,btype='low',fs=SR,output='sos'),x)
def hp(x,f): return sosfilt(butter(2,f,btype='high',fs=SR,output='sos'),x)
tt=lambda d: np.arange(int(d*SR))/SR
t=tt(.35); kick=np.sin(2*np.pi*np.cumsum(45+120*np.exp(-t*28))/SR)*np.exp(-t*7)
t=tt(.06); hat=hp(R.standard_normal(len(t)),7000)*np.exp(-t*70)
t=tt(.25); clap=sum(np.roll(hp(lp(R.standard_normal(len(t)),5000),900)*np.exp(-t*22),int(k*0.008*SR)) for k in range(3))
def note(f,d,kind):
    t=tt(d)
    if kind=='sub': return np.sin(2*np.pi*f*t)*np.minimum(1,t/.01)*np.exp(-t*1.2)*np.minimum(1,(d-t)/.03)
    if kind=='pluck':
        x=sum(np.sin(2*np.pi*f*h*t)/h**1.3 for h in range(1,7))*np.exp(-t*9); return lp(x,3500)*np.minimum(1,t/.003)
    if kind=='pad':
        x=sum(np.sin(2*np.pi*f*(1+dt)*t) for dt in (-.004,0,.004))/3; x+=.3*np.sin(2*np.pi*2*f*t)
        return lp(x,1800)*np.minimum(1,t/.4)*np.minimum(1,(d-t)/.5)
hz=lambda m: 440*2**((m-69)/12)
prog=[(57,[57,60,64,67,71]),(53,[53,57,60,64,67]),(48,[48,52,55,59,64]),(55,[55,59,62,64,69])]
bar=4*B; t0=0.62  # music downbeat just after hook impact
nb=int((DUR-t0)/bar)+1
for b in range(nb):
    root,ch=prog[(b//2)%4]; tb=t0+b*bar
    drop = 21.9<=tb<23.0  # breakdown just before CTA
    for k in range(4):
        tk=tb+k*B
        if tk>30.6: continue
        if not drop: add(kick,tk,.9)
        if k in (1,3) and not drop: add(clap,tk,.28,.1)
        add(hat,tk+B/2,.22,.3); 
        if b%2: add(hat,tk+B*.75,.1,-.3)
        add(note(hz(root-12),B*.9,'sub'),tk+B/2*0,.0 if drop else .55)
    if tb<30.6: add(note(hz(ch[0]),bar*1.02,'pad'),tb,.0); [add(note(hz(m),bar*1.05,'pad'),tb,.07,(i-2)*.2) for i,m in enumerate(ch[1:4])]
    arp=[ch[1],ch[3],ch[4]+12,ch[2]+12,ch[4],ch[3]+12,ch[1]+12,ch[2]]
    for s in range(8):
        ts=tb+s*B/2
        if ts<30.6: add(note(hz(arp[s]),.5,'pluck'),ts,.16,.5 if s%2 else -.5)
# end sting
add(note(hz(45),3,'sub'),30.6,.6); [add(note(hz(m),2.6,'pad'),30.6,.09) for m in (57,64,69,72,76)]
x=np.stack([L,Rr],1)
# simple delay-reverb
for d,g in ((0.268,.25),(0.402,.15),(0.536,.1)): x[int(d*SR):]+=x[:-int(d*SR)]*g
x=x/np.max(np.abs(x))*0.8
fade=np.ones(N); fi=int(31.0*SR); fade[fi:]=np.linspace(1,0,N-fi)**1.5; x*=fade[:,None]
sf.write('music.wav',x.astype(np.float32),SR); print('ok')
