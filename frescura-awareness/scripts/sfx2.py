# Synthesized luxury SFX kit + minimal music bed (all original, deterministic).
import numpy as np, soundfile as sf, sys, os
from scipy.signal import butter, sosfilt
SR = 48000; out = sys.argv[1]; os.makedirs(out, exist_ok=True)
rng = np.random.default_rng(11)
T = lambda d: np.arange(int(d * SR)) / SR
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype='band', fs=SR, output='sos'), x, axis=0)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype='low', fs=SR, output='sos'), x, axis=0)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype='high', fs=SR, output='sos'), x, axis=0)
def norm(x, db=-1.0): return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)
def st(x, w=0.0):
    if x.ndim == 2: return x
    d = int(w * SR); R = np.concatenate([np.zeros(d), x])[:len(x)] if d else x
    return np.stack([x, R], 1)
def verb(x, mix=0.25, d=1.6):
    # cheap stereo convolution reverb with decaying noise IR
    n = int(d * SR); t = np.arange(n) / SR
    irL = rng.standard_normal(n) * np.exp(-t * 4.5); irR = rng.standard_normal(n) * np.exp(-t * 4.5)
    irL, irR = lp(irL, 6000), lp(irR, 6000)
    m = x if x.ndim == 1 else x.mean(1)
    L = np.convolve(m, irL)[:len(m) + n]; R = np.convolve(m, irR)[:len(m) + n]
    L = np.pad(L, (0, len(m) + n - len(L))); R = np.pad(R, (0, len(m) + n - len(R)))
    wet = np.stack([L, R], 1); wet = wet / (np.max(np.abs(wet)) + 1e-9) * np.max(np.abs(m))
    dry = st(m); dry = np.concatenate([dry, np.zeros((n, 2))])
    return dry * (1 - mix) + wet * mix

def impact():  # deep cinematic boom + transient (hook)
    t = T(2.2); f = 38 + 90 * np.exp(-t * 9)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
    crack = hp(rng.standard_normal(len(t)), 1800) * np.exp(-t * 40) * 0.6
    body = bp(rng.standard_normal(len(t)), 80, 600) * np.exp(-t * 7) * 0.5
    return verb(np.tanh(1.6 * (sub + crack + body)), 0.3, 2.0)

def riser(d=1.4):  # filtered noise + rising tone into a hit
    t = T(d); n = rng.standard_normal(len(t)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = 400 + 7000 * p ** 2
        y[i:i + seg] = bp(n[i:i + seg], fc * 0.7, min(fc * 1.4, 20000))
    tone = np.sin(2 * np.pi * np.cumsum(220 + 660 * (t / d) ** 2) / SR) * 0.25
    env = (t / d) ** 2.2
    return st((y + tone) * env, 0.007)

def whoosh(d=0.55, up=True):
    t = T(d); n = rng.standard_normal(len(t)); y = np.zeros_like(n); seg = 256
    for i in range(0, len(n), seg):
        p = i / len(n); fc = 300 + 4200 * (np.sin(np.pi * p) ** 2)
        y[i:i + seg] = bp(n[i:i + seg], fc * 0.55, fc * 1.7)
    env = np.sin(np.pi * t / d) ** 2.5
    x = y * env; L = x * (1 - t / d) + .25 * x; R = x * (t / d) + .25 * x
    return np.stack([L, R], 1)

def swish():  # fast short air swipe for text
    return whoosh(0.28)

def tick():  # luxe UI tick (glassy)
    t = T(0.18); x = (np.sin(2 * np.pi * 3200 * t) * .6 + np.sin(2 * np.pi * 5100 * t) * .3) * np.exp(-t * 60)
    x += hp(rng.standard_normal(len(t)), 4000) * np.exp(-t * 200) * .4
    return st(x)

def glass():  # crystal ping
    t = T(1.6); x = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * dcy) for f, a, dcy in
                    [(2093, 1, 3.2), (3136, .45, 4.5), (4186, .3, 6), (5274, .15, 8)])
    return verb(x * np.minimum(1, t / .002), .35, 1.8)

def shimmer(d=1.3, n=22):
    x = np.zeros(int((d + .5) * SR))
    for k in range(n):
        o = int(rng.uniform(0, d * .85) * SR); f = rng.uniform(3000, 8000); t = T(.3)
        b = np.sin(2 * np.pi * f * t) * np.exp(-t * 18) * rng.uniform(.3, 1)
        x[o:o + len(b)] += b * (1 - o / len(x))
    x = hp(x, 2500); L = x; R = np.roll(x, int(.013 * SR)); return np.stack([L, R], 1)

def bubbles(d=1.2, n=26):  # soft foam pops
    x = np.zeros(int((d + .2) * SR))
    for k in range(n):
        o = int(rng.uniform(0, d) * SR); t = T(.05); f0 = rng.uniform(500, 1500)
        f = f0 * (1 + 2.5 * t / .05)
        b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 90) * rng.uniform(.3, 1)
        x[o:o + len(b)] += b
    return verb(x, .2, .8)

def pump():  # pump press "pshh"
    t = T(.5); n = bp(rng.standard_normal(len(t)), 900, 6500)
    env = np.minimum(1, t / .015) * np.exp(-t * 7)
    click = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 80) * .8
    return st(n * env * .7 + click)

def pop():
    t = T(.12); f = 1000 * np.exp(-t * 30) + 200
    return st(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 40))

def thud():  # soft low hit for scene cuts
    t = T(.6); f = 60 + 70 * np.exp(-t * 18)
    return st(np.tanh(2 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)))

def cash():  # CTA register-like bright ding pair
    t = T(1.2); a = np.sin(2 * np.pi * 2637 * t) * np.exp(-t * 5); b = np.sin(2 * np.pi * 3520 * t) * np.exp(-t * 5)
    x = a.copy(); o = int(.09 * SR); x[o:] += b[:len(x) - o]
    return verb(x, .25, 1.2)

def tap():  # finger tap on screen
    t = T(.1); x = bp(rng.standard_normal(len(t)), 600, 3500) * np.exp(-t * 120) + np.sin(2 * np.pi * 220 * t) * np.exp(-t * 60) * .6
    return st(x)

def music(dur, bpm=112):
    # minimal luxe deep-house bed: soft kick, closed hats, warm Rhodes-ish chords, sub bass.
    beat = 60 / bpm; N = int(dur * SR); L = np.zeros(N); R = np.zeros(N)
    t1 = T(.35); kick = np.sin(2 * np.pi * np.cumsum(45 + 110 * np.exp(-t1 * 35)) / SR) * np.exp(-t1 * 9)
    th = T(.06); hat = hp(rng.standard_normal(len(th)), 7000) * np.exp(-th * 70)
    chords = [[57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 65], [52, 55, 59, 62]]  # Am9-ish, Fmaj7, G, Em7
    mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
    def put(buf, x, i, g=1.):
        j = min(N, i + len(x)); buf[i:j] += x[:j - i] * g
    nb = int(dur / beat) + 1
    for b in range(nb):
        i = int(b * beat * SR)
        put(L, kick, i, .9); put(R, kick, i, .9)
        hi = int((b + .5) * beat * SR); put(L, hat, hi, .22); put(R, hat, hi, .3)
        if b % 4 == 0:
            ch = chords[(b // 4) % 4]; d = beat * 4; t = T(d)
            pad = sum(np.sin(2 * np.pi * mtof(m) * t) + .3 * np.sin(2 * np.pi * 2 * mtof(m) * t) for m in ch)
            pad *= np.minimum(1, t / .05) * np.exp(-t * .6) * .12
            put(L, pad, i); put(R, np.roll(pad, 300), i)
            bass = np.sin(2 * np.pi * mtof(ch[0] - 24) * t) * np.minimum(1, t / .02) * np.exp(-t * .8) * .35
            put(L, bass, i); put(R, bass, i)
    x = np.stack([L, R], 1); x = lp(x, 9000)
    # sidechain-ish pump on every beat
    tt = np.arange(N) / SR; ph = (tt % beat) / beat; x[:, :] *= (0.55 + 0.45 * np.minimum(1, ph / .35))[:, None]
    return x

kit = dict(impact=impact, riser=riser, whoosh=whoosh, swish=swish, tick=tick, glass=glass, shimmer=shimmer,
           bubbles=bubbles, pump=pump, pop=pop, thud=thud, cash=cash, tap=tap)
for k, fn in kit.items():
    y = st(fn()); sf.write(f"{out}/{k}.wav", norm(y).astype(np.float32), SR)
dur = float(sys.argv[2]) if len(sys.argv) > 2 else 40
sf.write(f"{out}/music.wav", norm(music(dur), -3).astype(np.float32), SR)
print("ok")
