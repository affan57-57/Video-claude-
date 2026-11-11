# Synthesized luxury-minimal SFX kit + light background beat (no third-party samples).
import numpy as np, soundfile as sf, sys, os
from scipy.signal import butter, sosfilt
SR = 48000; out = sys.argv[1]; os.makedirs(out, exist_ok=True); rng = np.random.default_rng(11)
T = lambda d: np.arange(int(d * SR)) / SR
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype='band', fs=SR, output='sos'), x, axis=0)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype='low', fs=SR, output='sos'), x, axis=0)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype='high', fs=SR, output='sos'), x, axis=0)
def norm(x, db=-1.0): return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)
def st(x, w=0.0):
    if x.ndim == 2: return x
    d = int(0.008 * SR * w); r = np.roll(x, d) if d else x
    return np.stack([x, r], 1)
def rev(x, d=1.2, mix=0.25):  # cheap stereo reverb: decaying noise convolution
    n = int(d * SR); ir = rng.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR * 5)[:, None]
    ir = lp(ir, 7000); x2 = st(x)
    wet = np.stack([np.convolve(x2[:, c], ir[:, c])[:len(x2)] for c in range(2)], 1)
    return x2 + mix * norm(wet, 0) * np.max(np.abs(x2))
def sweep_noise(d, f0, f1, q=0.5):
    n = rng.standard_normal(int(d * SR)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = f0 * (f1 / f0) ** p
        y[i:i + seg] = bp(n[i:i + seg], fc * (1 - q), min(fc * (1 + q), 20000))
    return y

def whoosh(d=0.55):
    y = sweep_noise(d, 400, 5000, .6); t = T(d); env = np.sin(np.pi * (t / d) ** 0.7) ** 2
    x = y * env; return np.stack([x * (1 - t / d) + .3 * x, x * (t / d) + .3 * x], 1)
def swipe(d=0.28):
    y = sweep_noise(d, 6000, 1500, .5); t = T(d); return st(y * np.exp(-t * 9) * np.minimum(1, t / .01), .6)
def impact(d=1.6):  # deep sub boom + transient
    t = T(d); f = 38 + 90 * np.exp(-t * 18); ph = 2 * np.pi * np.cumsum(f) / SR
    sub = np.sin(ph) * np.exp(-t * 2.6); click = hp(rng.standard_normal(len(t)), 1500) * np.exp(-t * 60) * .5
    return rev(sub + click, 1.6, .18)
def riser(d=1.4):
    t = T(d); y = sweep_noise(d, 300, 9000, .35) * (t / d) ** 2
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / d) ** 2) / SR) * (t / d) ** 3 * .25
    return rev(y + tone, 1.0, .3)
def bell(f, d, dec=6, parts=((1, 1), (2.0, .35), (3.0, .15), (4.16, .08))):
    t = T(d); return sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-dec * m ** .5 * t) for m, a in parts) * np.minimum(1, t / .002)
def shimmer(d=1.6, n=22):
    x = np.zeros(int(d * SR) + SR)
    for k in range(n):
        o = int((k / n) * d * .8 * SR + rng.uniform(0, .03) * SR); b = bell(rng.choice([2093, 2637, 3136, 3520, 4186]) * rng.uniform(.995, 1.005), .5, 12)
        x[o:o + len(b)] += b * (0.4 + 0.6 * k / n)
    return rev(hp(x, 1800), 1.5, .4)
def pop():
    t = T(.1); ph = 2 * np.pi * np.cumsum(1100 * np.exp(-t * 35) + 220) / SR; return st(np.sin(ph) * np.exp(-t * 45))
def bubble():
    x = np.zeros(int(.6 * SR))
    for k in range(7):
        d = rng.uniform(.03, .07); t = T(d); f0 = rng.uniform(500, 1400)
        b = np.sin(2 * np.pi * np.cumsum(f0 * (1 + 2.5 * t / d)) / SR) * np.sin(np.pi * t / d) ** 2
        o = int(rng.uniform(0, .5) * SR); x[o:o + len(b)] += b * rng.uniform(.4, 1)
    return rev(x, .4, .2)
def pump():  # plastic click + air squish
    t = T(.45); click = hp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 120)
    sq = bp(rng.standard_normal(len(t)), 300, 2500) * np.exp(-((t - .12) / .07) ** 2) * .6
    return st(click + sq + bubble()[:len(t), 0] * .3)
def tick():
    t = T(.06); return st(hp(np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 140) + .3 * rng.standard_normal(len(t)) * np.exp(-t * 200), 1000))
def glitch(d=0.35):
    x = np.zeros(int(d * SR)); i = 0
    while i < len(x):
        L = int(rng.uniform(.01, .04) * SR); f = rng.choice([90, 180, 1200, 2400])
        seg = np.sign(np.sin(2 * np.pi * f * np.arange(L) / SR)) * rng.uniform(.2, .7); x[i:i + L] = seg[:len(x[i:i + L])]; i += L + int(rng.uniform(0, .015) * SR)
    return st(lp(x, 6000) * np.exp(-T(d) * 3), .5)
def ding():
    a = bell(1568, 1.6, 4); b = bell(2093, 1.6, 4); x = np.zeros(int(1.9 * SR)); x[:len(a)] += a; o = int(.09 * SR); x[o:o + len(b)] += b
    return rev(x, 1.4, .35)
def chaching():
    x = np.zeros(int(1.4 * SR)); c = hp(rng.standard_normal(int(.05 * SR)), 3000) * np.exp(-T(.05) * 80)
    x[:len(c)] += c; x[int(.05 * SR):int(.05 * SR) + len(c)] += c * .7
    for i, f in enumerate([2637, 3520, 4186]):
        b = bell(f, 1.1, 5); o = int((.12 + .05 * i) * SR); x[o:o + len(b)] += b * .6
    return rev(x, 1.0, .3)
def bass_drop():
    t = T(1.2); f = 120 * np.exp(-t * 3) + 35; return rev(np.tanh(2 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 2.2), 1.0, .1)

kit = dict(whoosh=whoosh, swipe=swipe, impact=impact, riser=riser, shimmer=shimmer, pop=pop, bubble=bubble,
           pump=pump, tick=tick, glitch=glitch, ding=ding, chaching=chaching, drop=bass_drop)
for k, fn in kit.items():
    y = st(fn()); sf.write(f"{out}/{k}.wav", norm(y, -1).astype(np.float32), SR)

# Background bed: 118 BPM minimal luxe groove (sub kick, soft clap, airy hats, warm pad chords)
D = float(sys.argv[2]) if len(sys.argv) > 2 else 40; bpm = 118; b = 60 / bpm; N = int(D * SR); mix = np.zeros((N, 2))
def put(x, t0, g=1.0):
    x = st(x); o = int(t0 * SR); e = min(N, o + len(x));
    if o < N: mix[o:e] += x[:e - o] * g
kt = T(.5); kick = np.sin(2 * np.pi * np.cumsum(45 + 110 * np.exp(-kt * 30)) / SR) * np.exp(-kt * 6)
ht = T(.05); hat = hp(rng.standard_normal(len(ht)), 8000) * np.exp(-ht * 90)
ct = T(.25); clap = bp(rng.standard_normal(len(ct)), 900, 4000) * np.exp(-ct * 22)
chords = [[220.0, 261.6, 329.6, 392.0], [174.6, 220.0, 261.6, 329.6], [196.0, 246.9, 293.7, 370.0], [164.8, 207.7, 246.9, 329.6]]
beat = 0; t0 = 0.0
while t0 < D:
    bar, pos = divmod(beat, 4)
    if t0 > 0.0: put(kick, t0, .9 if pos in (0, 2) else .55)
    if pos in (1, 3) and t0 > 2.6: put(clap, t0, .35)
    for s in (0, .5): put(hat, t0 + s * b, .18 if s else .1)
    if pos == 0:
        ch = chords[bar % 4]; dur = 4 * b; tt = T(dur)
        pad = sum(np.sin(2 * np.pi * f * tt + np.sin(2 * np.pi * .3 * tt)) + .5 * np.sin(2 * np.pi * f * 2.003 * tt) for f in ch)
        pad = lp(pad, 1800) * np.minimum(1, tt / .4) * np.minimum(1, (dur - tt) / .5) * .08
        put(np.stack([pad, np.roll(pad, 300)], 1), t0)
    beat += 1; t0 += b
mix = lp(mix, 12000); sf.write(f"{out}/bed.wav", norm(mix, -3).astype(np.float32), SR)
print("ok", list(kit), "bed", D)
