"""Synthesized sound design for the Frescura Body ad: SFX kit + 120 BPM minimal-luxury groove + final mix.
Usage: python sound.py WORK_DIR    (reads voice.wav + timeline.json, writes sfx/, music.wav, mix.wav)
Everything is generated here (no third-party samples), deterministic (seeded).
"""
import json, sys, os, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve
W = sys.argv[1]; SR = 48000; rng = np.random.default_rng(11)
os.makedirs(f"{W}/sfx", exist_ok=True)
T = lambda d: np.arange(int(d*SR))/SR
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x, axis=0)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x, axis=0)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x, axis=0)
def norm(x, db=-1.0): return x/(np.max(np.abs(x))+1e-9)*10**(db/20)
def st(x, w=0.0):
    if x.ndim == 2: return x
    d = int(0.009*SR); R = np.concatenate([np.zeros(d), x])[:len(x)]
    return np.stack([x, x*(1-w)+R*w], 1)
def reverb(x, d=1.6, mix=0.25, damp=6000):
    n = int(d*SR); ir = rng.standard_normal((n, 2))*np.exp(-np.arange(n)/SR*(6.9/d))[:, None]
    ir = lp(ir, damp); x2 = st(x)
    wet = np.stack([fftconvolve(x2[:, c], ir[:, c])[:len(x2)] for c in (0, 1)], 1)
    wet *= np.max(np.abs(x2))/(np.max(np.abs(wet))+1e-9)
    return x2*(1-mix)+wet*mix
def pad_to(x, d):
    y = np.zeros((int(d*SR), 2)); x = st(x); y[:min(len(x), len(y))] = x[:len(y)]; return y
def bell(f, d, decay=5, parts=((1, 1), (2.0, .35), (3.01, .15), (4.16, .08))):
    t = T(d); return sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-decay*m**.5*t) for m, a in parts)*np.minimum(1, t/0.002)

# ---------------- SFX kit ----------------
def impact():  # cinematic sub drop + transient + air tail
    t = T(2.2); f = 34+90*np.exp(-t*9); sub = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.2)
    click = hp(rng.standard_normal(len(t)), 2500)*np.exp(-t*90)*0.5
    body = bp(rng.standard_normal(len(t)), 80, 900)*np.exp(-t*14)*0.8
    return reverb(np.tanh(1.6*(sub+click+body)), 2.4, 0.22)
def whoosh(d=0.55, lo=250, hi=6000, rev=False):
    n = rng.standard_normal(int(d*SR)); t = T(d); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i/len(n); p = 1-p if rev else p
        fc = lo*(hi/lo)**(np.sin(np.pi*p*0.5)**2)
        y[i:i+seg] = sosfilt(butter(2, [fc*0.7, min(fc*1.5, 20000)], 'band', fs=SR, output='sos'), n[i:i+seg])
    env = (t/d)**1.5*np.exp(-((t/d)-0.75)**2*0) ; env = np.sin(np.pi*np.clip(t/d, 0, 1))**2
    x = y*env; pan = np.linspace(-0.8, 0.8, len(x))
    return reverb(np.stack([x*np.sqrt((1-pan)/2), x*np.sqrt((1+pan)/2)], 1), 0.9, 0.18)
def riser(d=1.0):
    t = T(d); f = 180*(12)**(t/d); tone = np.sin(2*np.pi*np.cumsum(f)/SR)*0.25
    nz = bp(rng.standard_normal(len(t)), 1500, 9000)*0.9
    env = (t/d)**2.2; x = (tone+nz)*env
    return reverb(x, 1.2, 0.3)
def pop():
    t = T(0.14); f = 1100*np.exp(-t*32)+220; x = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*38)
    return st(x+hp(rng.standard_normal(len(t)), 4000)*np.exp(-t*300)*0.3)
def click():
    t = T(0.05); x = bp(rng.standard_normal(len(t)), 2000, 9000)*np.exp(-t*220)+np.sin(2*np.pi*1800*t)*np.exp(-t*160)*0.6
    return st(x)
def tick():
    t = T(0.04); return st(np.sin(2*np.pi*3200*t)*np.exp(-t*260)+hp(rng.standard_normal(len(t)), 6000)*np.exp(-t*500)*0.4)
def shimmer(d=1.3, n=22, lo=2600, hi=7500):
    x = np.zeros(int((d+0.6)*SR))
    for k in range(n):
        o = int(rng.uniform(0, d*0.85)*SR); f = rng.uniform(lo, hi); b = bell(f, 0.45, decay=11, parts=((1, 1), (2.01, .25)))
        x[o:o+len(b)] += b*rng.uniform(.3, 1)*(1-o/len(x))
    return reverb(hp(x, 1800), 1.8, 0.35)
def chime():  # two-note luxury chime
    a = bell(1567.98, 1.6, 3.5); b = bell(2349.3, 1.6, 3.5)
    x = np.zeros(int(2.0*SR)); x[:len(a)] += a; o = int(0.09*SR); x[o:o+len(b)] += b*0.8
    return reverb(x, 2.0, 0.35)
def ding_check():
    a = bell(1318.5, 1.0, 5); b = bell(1975.5, 1.0, 5)
    x = np.zeros(int(1.3*SR)); x[:len(a)] += a; o = int(0.075*SR); x[o:o+len(b)] += b
    return reverb(x, 1.4, 0.25)
def stamp():
    t = T(0.6); thud = np.sin(2*np.pi*np.cumsum(70+120*np.exp(-t*40))/SR)*np.exp(-t*12)
    slap = bp(rng.standard_normal(len(t)), 300, 4000)*np.exp(-t*45)
    return reverb(np.tanh(2*(thud+slap*0.7)), 0.7, 0.15)
def bubbles(d=1.2, n=16):
    x = np.zeros(int((d+0.2)*SR))
    for k in range(n):
        o = int(rng.uniform(0, d)*SR); L = int(0.05*SR); t = np.arange(L)/SR
        f0 = rng.uniform(500, 1400); f = f0*(1+t*18)
        b = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*70)*rng.uniform(.4, 1); x[o:o+L] += b
    return reverb(x, 0.8, 0.2)
def splash(d=0.9):
    t = T(d); n = rng.standard_normal(len(t)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i/len(n); fc = 7000*(1-p)+900
        y[i:i+seg] = sosfilt(butter(2, [fc*0.6, min(fc*1.6, 20000)], 'band', fs=SR, output='sos'), n[i:i+seg])
    x = y*np.minimum(1, t/0.01)*np.exp(-t*4.5)
    bb = bubbles(0.5, 8)[:, 0]; x[:len(bb)] += 0.4*bb[:len(x)]
    return reverb(x, 1.4, 0.3)
def clock(d=1.2, bpm=240):
    x = np.zeros(int(d*SR)); step = 60/bpm
    for i, s in enumerate(np.arange(0, d-0.05, step)):
        tk = tick()[:, 0]*(1.0 if i % 2 == 0 else 0.6); o = int(s*SR); x[o:o+len(tk)] += tk
    return reverb(x, 0.4, 0.12)
def alert():  # low luxury "scarcity" pulse
    t = T(0.8); x = np.zeros(len(t))
    for o in (0, 0.18):
        tt = T(0.35); b = (np.sin(2*np.pi*440*tt)+0.5*np.sin(2*np.pi*660*tt))*np.exp(-tt*9)
        x[int(o*SR):int(o*SR)+len(b)] += b
    return reverb(x+0.6*np.sin(2*np.pi*55*t)*np.exp(-t*5), 1.0, 0.2)
def register():  # "cha-ching"
    t = T(1.2); x = np.zeros(len(t))
    cl = bp(rng.standard_normal(int(0.06*SR)), 2000, 8000)*np.exp(-np.arange(int(0.06*SR))/SR*80); x[:len(cl)] += cl
    for f, o in ((2637, 0.08), (3520, 0.12), (4186, 0.16), (5274, 0.19)):
        b = bell(f, 0.9, 6); x[int(o*SR):int(o*SR)+len(b)] += b[:len(x)-int(o*SR)]*0.6
    return reverb(x, 1.6, 0.3)
def tap():
    t = T(0.25); x = np.sin(2*np.pi*np.cumsum(240+500*np.exp(-t*60))/SR)*np.exp(-t*30)+bp(rng.standard_normal(len(t)), 1000, 6000)*np.exp(-t*120)*0.4
    return st(x)
def swipe(): return whoosh(0.32, 900, 9000)
def outro_swell():
    x = reverb(riser(1.2), 1.0, 0.1); y = shimmer(1.6, 30); z = np.zeros((int(3.2*SR), 2))
    z[:len(x)] += x*0.7; o = int(1.15*SR); z[o:o+len(y)] += y[:len(z)-o]; i = impact(); z[o:o+len(i)] += i[:len(z)-o]*0.9
    return z
KIT = dict(impact=impact, whoosh=whoosh, whoosh_rev=lambda: whoosh(0.6, rev=True), riser=riser, pop=pop, click=click, tick=tick,
           shimmer=shimmer, chime=chime, ding=ding_check, stamp=stamp, bubbles=bubbles, splash=splash, clock=clock, alert=alert,
           register=register, tap=tap, swipe=swipe, outro=outro_swell)
sfx = {}
for k, fn in KIT.items():
    y = norm(st(fn()), -1.0); sfx[k] = y; sf.write(f"{W}/sfx/{k}.wav", y.astype(np.float32), SR)

# ---------------- Music: 120 BPM minimal luxury house ----------------
tl = json.load(open(f"{W}/timeline.json")); sec = {s["name"]: s for s in tl["sections"]}
END_CARD = 2.9; TOTAL = tl["voice_dur"]+END_CARD
BPM = 120; beat = 60/BPM; bar = 4*beat; N = int(TOTAL*SR)+SR
mus = np.zeros((N, 2))
def add(x, t0, g=1.0):
    x = st(x); o = int(t0*SR)
    if o >= N: return
    L = min(len(x), N-o); mus[o:o+L] += x[:L]*g
def kick():
    t = T(0.45); f = 45+120*np.exp(-t*30); return np.tanh(1.8*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7))
def hat(open_=False):
    d = 0.18 if open_ else 0.05; t = T(d); return hp(rng.standard_normal(len(t)), 8000)*np.exp(-t*(18 if open_ else 90))
def clap():
    t = T(0.3); x = np.zeros(len(t))
    for o in (0, 0.008, 0.017):
        n = int(o*SR); x[n:] += bp(rng.standard_normal(len(t)-n), 900, 5000)*np.exp(-np.arange(len(t)-n)/SR*28)
    return reverb(x, 0.9, 0.35)
CH = [[57, 60, 64, 67, 71], [53, 57, 60, 64, 67], [55, 59, 62, 65, 69], [52, 55, 59, 62, 67]]  # Am9 Fmaj9 G6/9-ish Em7
BASS = [45, 41, 43, 40]
m2f = lambda m: 440*2**((m-69)/12)
def pad(notes, d):
    t = T(d); x = np.zeros(len(t))
    for m in notes:
        for det in (-0.08, 0.0, 0.08):
            ph = 2*np.pi*m2f(m+det)*t; x += (2*((ph/(2*np.pi)) % 1)-1)*0.12
    x = lp(x, 2200, 2); env = np.minimum(1, t/0.35)*np.minimum(1, (d-t)/0.3); return x*env
def sub(m, d):
    t = T(d); return np.sin(2*np.pi*m2f(m)*t)*np.minimum(1, t/0.01)*np.exp(-t*1.2)
def pluck(m, d=0.5):
    t = T(d); return (np.sin(2*np.pi*m2f(m)*t)+0.3*np.sin(4*np.pi*m2f(m)*t))*np.exp(-t*9)
t_testi, t_close, t_end = sec["testi"]["start"], sec["closing"]["start"], tl["voice_dur"]
nbars = int(TOTAL/bar)+2
for b in range(nbars):
    t0 = b*bar; ci = b % 4
    if t0 > TOTAL: break
    add(pad(CH[ci], bar+0.05), t0, 0.55)
    for k in range(4):
        tb = t0+k*beat
        if tb > t_end+0.2: continue
        full = tb >= t_testi-0.02
        add(kick(), tb, 0.9 if full else 0.55)
        add(hat(True), tb+beat/2, 0.22 if full else 0.12)
        if tb >= t_close-0.02 and k in (1, 3): add(clap(), tb, 0.35)
        if full: add(hat(), tb+beat*0.75, 0.12)
        add(sub(BASS[ci], beat*0.9), tb+beat/2 if full else tb, 0.55 if full else 0.3)
        arp = CH[ci][(k*2) % 5]+12
        add(pluck(arp), tb, 0.16); add(pluck(CH[ci][(k*2+2) % 5]+12), tb+beat/2, 0.11)
# filter sweep: intro is lowpassed and opens into testimonial
cut = int(t_testi*SR); mus_lp = lp(mus, 900, 2)
xf = np.clip((np.arange(N)/SR-(t_testi-1.0))/1.0, 0, 1)[:, None]
mus = mus_lp*(1-xf)+mus*xf
# end: ring-out chord
add(reverb(pad(CH[0]+[76], 3.0), 2.5, 0.4), t_end+0.1, 0.8)
fade = np.clip((TOTAL-np.arange(N)/SR)/1.2, 0, 1)[:, None]; mus *= fade
mus = norm(mus, -1.0)[:int(TOTAL*SR)]
sf.write(f"{W}/music.wav", mus.astype(np.float32), SR)

# ---------------- SFX placement on the edit (output-timeline seconds) ----------------
def wt(word, sect, nth=0):
    hits = [w for w in tl["words"] if w["section"] == sect and w["w"].lower().strip(",.?!").startswith(word)]
    return hits[nth]["s"]
CUES = [  # (sfx, time, gain dB)
  ("impact", 0.00, -4), ("whoosh_rev", 0.0, -9), ("tick", wt("ragu", "intro"), -10), ("pop", wt("body", "intro"), -8),
  ("swipe", wt("sebelum", "intro")-0.08, -9), ("click", wt("keputusan", "intro"), -9),
  ("whoosh", wt("tengok", "intro")-0.1, -9), ("riser", t_testi-1.0, -8), ("impact", t_testi, -7), ("whoosh", t_testi-0.2, -8),
  ("shimmer", wt("lembut", "testi"), -9), ("chime", wt("wangi", "testi"), -10),
  ("stamp", wt("tipu", "testi"), -6), ("ding", wt("betul", "testi"), -9),
  ("shimmer", wt("lembut", "testi", 2), -10), ("bubbles", wt("harum", "testi"), -8), ("splash", wt("fresh", "testi")-0.05, -6),
  ("whoosh", t_close-0.22, -8), ("pop", wt("ha", "closing"), -7), ("ding", wt("yakin", "closing"), -8),
  ("clock", wt("jangan", "closing"), -11), ("alert", wt("terhad", "closing"), -8),
  ("tap", wt("tekan", "closing"), -6), ("pop", wt("kuning", "closing"), -7), ("click", wt("check", "closing"), -7),
  ("register", wt("out", "closing")+0.05, -7), ("swipe", wt("harga", "closing")-0.1, -9), ("shimmer", wt("titok", "closing"), -10),
  ("outro", t_end-1.15, -5),
]
json.dump([dict(sfx=s, t=round(t, 3), db=g) for s, t, g in CUES], open(f"{W}/sfx_cues.json", "w"), indent=1)
L = int(TOTAL*SR); fx = np.zeros((L, 2))
for s, t0, g in CUES:
    x = sfx[s]*10**(g/20); o = max(0, int(t0*SR)); n = min(len(x), L-o); fx[o:o+n] += x[:n]
v = sf.read(f"{W}/voice.wav", dtype="float32")[0]; voice = np.zeros(L); voice[:len(v)] = v[:L]
# sidechain duck music under voice (envelope follower)
env = np.abs(voice); k = int(0.03*SR); env = np.convolve(env, np.ones(k)/k, 'same'); env = env/(env.max()+1e-9)
duck = 1-0.55*np.clip(env*6, 0, 1); duck = np.convolve(duck, np.ones(int(0.12*SR))/int(0.12*SR), 'same')
music = mus*duck[:, None]*10**(-17/20)
mix = st(voice)*0.95+fx+music
sf.write(f"{W}/mix_pre.wav", mix.astype(np.float32), SR)
print("total", TOTAL)
