"""Synthesised SFX + minimal-lux music bed for the Frescura Body feedback ad.
Usage: python frescura_sfx.py OUT_DIR MUSIC_SECONDS
"""
import sys, os, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
out = sys.argv[1]; MUS = float(sys.argv[2]) if len(sys.argv) > 2 else 34
os.makedirs(out, exist_ok=True)
rng = np.random.default_rng(11)
T = lambda d: np.arange(int(d * SR)) / SR
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype="band", fs=SR, output="sos"), x, axis=0)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype="high", fs=SR, output="sos"), x, axis=0)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x, axis=0)
def norm(x, db=-1.0): return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)
def st(x, w=0.0):
    d = int(w * SR); r = np.roll(x, d) if d else x
    return np.stack([x, r], 1)

def sweep_noise(d, f0, f1, q=0.5):
    n = rng.standard_normal(int(d * SR)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = f0 * (f1 / f0) ** p
        y[i:i + seg] = bp(n[i:i + seg], fc * (1 - q), min(fc * (1 + q), SR / 2 - 100))
    return y

def whoosh(d=0.55):  # fast airy swish, left->right
    tt = T(d); y = sweep_noise(d, 400, 5000) * np.sin(np.pi * tt / d) ** 3
    return np.stack([y * (1 - tt / d) + .25 * y, y * (tt / d) + .25 * y], 1)

def swipe(d=0.28):  # short tight swipe for text
    tt = T(d); y = sweep_noise(d, 2500, 9000, .4) * np.exp(-((tt - d * .35) / (d * .22)) ** 2)
    return st(y, .006)

def impact(d=1.6):  # deep cinematic boom + transient
    tt = T(d); f = 38 + 70 * np.exp(-tt * 9)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.6)
    click = hp(rng.standard_normal(len(tt)), 1500) * np.exp(-tt * 90) * .6
    body = lp(rng.standard_normal(len(tt)), 900) * np.exp(-tt * 7) * .5
    return st(np.tanh(1.6 * (sub + click + body)), .004)

def riser(d=1.4):  # noise + pitch riser into hit
    tt = T(d); n = sweep_noise(d, 300, 8000, .35) * (tt / d) ** 2
    tone = sum(np.sin(2 * np.pi * np.cumsum(200 * k * 2 ** (2 * tt / d)) / SR) for k in (1, 1.5, 2)) * (tt / d) ** 3 * .15
    return st(n + tone, .01)

def bell(f, d, dec=6, parts=((1, 1), (2.0, .35), (3.01, .15))):
    tt = T(d); return sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-dec * m ** .5 * tt) for m, a in parts) * np.minimum(1, tt / .002)

def shimmer(d=1.2):  # luxury glass shimmer
    x = np.zeros(int((d + .5) * SR))
    for k in range(18):
        o = int(rng.uniform(0, d * .75) * SR); b = bell(rng.choice([2093, 2349, 2637, 3136, 3520, 4186]), .5, 10)
        x[o:o + len(b)] += b * rng.uniform(.3, 1)
    return st(hp(x, 1800), .012)

def tick():  # UI click
    tt = T(.05); return st(hp(rng.standard_normal(len(tt)), 2500) * np.exp(-tt * 260) + np.sin(2 * np.pi * 1800 * tt) * np.exp(-tt * 180) * .6)

def pop():  # bubbly pop (foam)
    tt = T(.14); f = 1400 * np.exp(-tt * 28) + 240
    return st(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 38))

def bubbles(d=1.4):  # many little pops for foam
    x = np.zeros(int((d + .2) * SR)); p = pop()[:, 0]
    for k in range(26):
        o = int(rng.uniform(0, d) * SR); s = rng.uniform(.6, 1.6)
        pk = np.interp(np.arange(0, len(p), s), np.arange(len(p)), p)
        x[o:o + len(pk)] += pk * rng.uniform(.2, .8)
    return st(x, .009)

def kaching():  # checkout register
    x = np.zeros(int(1.4 * SR)); tt = T(.06)
    x[:len(tt)] += hp(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 80)
    for i, f in enumerate([2637, 3520]):
        b = bell(f, 1.2, 4.5); o = int((.05 + i * .09) * SR); x[o:o + len(b)] += b * .8
    return st(x, .008)

def glitch(d=.32):  # digital stutter for hook
    x = np.zeros(int(d * SR)); seg = int(.02 * SR)
    for i in range(0, len(x) - seg, seg):
        if rng.random() < .7:
            f = rng.choice([180, 360, 720, 1440, 2880])
            x[i:i + seg] = np.sign(np.sin(2 * np.pi * f * T(seg / SR))) * rng.uniform(.2, .7)
    return st(lp(x, 7000), .003)

def heartbeat_tick():  # urgency tick-tock for "stok tak banyak"
    x = np.zeros(int(1.0 * SR))
    for i, f in enumerate([1900, 1500, 1900, 1500]):
        tt = T(.04); o = int(i * .25 * SR); x[o:o + len(tt)] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 150)
    return st(x)

sfx = dict(whoosh=whoosh, swipe=swipe, impact=impact, riser=riser, shimmer=shimmer, tick=tick,
           pop=pop, bubbles=bubbles, kaching=kaching, glitch=glitch, clock=heartbeat_tick)
for k, fn in sfx.items():
    y = norm(fn(), -1.0); sf.write(f"{out}/{k}.wav", y.astype(np.float32), SR); print(k, round(len(y) / SR, 2))

# ---- music bed: 122 BPM minimal deep-house, Am9 - Fmaj7 - Cmaj7 - Em7 ----
bpm = 122; beat = 60 / bpm; N = int(MUS * SR); m = np.zeros((N, 2))
def place(sig, t, g=1.0):
    o = int(t * SR); e = min(N, o + len(sig))
    if o < N: m[o:e] += sig[:e - o] * g
kt = T(.35); kick = np.sin(2 * np.pi * np.cumsum(48 + 120 * np.exp(-kt * 35)) / SR) * np.exp(-kt * 9)
kick = st(np.tanh(kick * 1.4))
ht = T(.06); hat = st(hp(rng.standard_normal(len(ht)), 7000) * np.exp(-ht * 70), .002)
ct = T(.2); clap = st(bp(rng.standard_normal(len(ct)), 900, 4000) * np.exp(-ct * 25), .008)
chords = [[220, 261.6, 329.6, 392, 493.9], [174.6, 220, 261.6, 329.6, 392], [130.8, 196, 246.9, 329.6, 392], [164.8, 196, 246.9, 293.7, 392]]
bassn = [55, 43.65, 65.4, 41.2]
nb = int(MUS / beat) + 1
for b in range(nb):
    t = b * beat
    place(kick, t, .9)
    place(hat, t + beat / 2, .25); place(hat, t + beat / 4 * 3, .08)
    if b % 2 == 1: place(clap, t, .32)
for bar in range(nb // 4 + 1):
    t0 = bar * 4 * beat; ch = chords[bar % 4]; d = 4 * beat
    tt = T(d); pad = sum(np.sin(2 * np.pi * f * tt + k) + .3 * np.sin(2 * np.pi * f * 2.003 * tt) for k, f in enumerate(ch))
    pad = lp(pad, 2200) * np.minimum(1, tt / .4) * np.minimum(1, (d - tt) / .4) * .06
    # side-chain pump
    pump = 1 - .6 * np.exp(-((tt % beat) / .09))
    place(st(pad * pump, .015), t0)
    for k in range(4):  # off-beat bass
        bt = T(beat / 2); f = bassn[bar % 4]
        bs = np.tanh(2 * np.sin(2 * np.pi * f * bt)) * np.exp(-bt * 6) * .35
        place(st(lp(bs, 400)), t0 + k * beat + beat / 2)
    # sparkle arp
    for k in range(8):
        f = ch[(k * 2) % 5] * 4; place(st(bell(f, .4, 12) * .05, .01), t0 + k * beat / 2 + beat / 4)
tt = np.arange(N) / SR
m *= np.minimum(1, tt / 1.0)[:, None] * np.minimum(1, (MUS - tt) / 1.5)[:, None]
sf.write(f"{out}/music.wav", norm(m, -3).astype(np.float32), SR); print("music", MUS)
