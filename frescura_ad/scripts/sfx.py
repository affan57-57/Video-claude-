"""Synthesised SFX + 120bpm minimal-luxury house bed. Usage: python sfx.py outdir"""
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
    d = int(0.008 * SR * w); R = np.concatenate([np.zeros(d), x])[:len(x)] if d else x
    return np.stack([x, R], 1)
def bell(f, d, parts=((1, 1), (2.0, .35), (3.01, .15), (4.2, .07)), dec=6):
    t = T(d); x = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-dec * m ** .5 * t) for m, a in parts)
    return x * np.minimum(1, t / 0.002)

def whoosh(d=0.55, lo=250, hi=5000):
    n = rng.standard_normal(int(d * SR)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = lo + (hi - lo) * np.sin(np.pi * p) ** 1.5
        y[i:i + seg] = sosfilt(butter(2, [fc * .55, min(fc * 1.7, 20000)], btype='band', fs=SR, output='sos'), n[i:i + seg])
    t = T(d); env = (t / d) ** 1.2 * np.exp(-((t / d - 0.62) ** 2) / 0.05)
    x = y * env; L = x * (1.2 - t / d); R = x * (0.2 + t / d); return np.stack([L, R], 1)
def boom(d=1.6):
    t = T(d); f = 34 + 70 * np.exp(-t * 9); ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-t * 2.6) * np.minimum(1, t / 0.004)
    x += 0.35 * lp(rng.standard_normal(len(t)), 900) * np.exp(-t * 22)
    x = np.tanh(x * 1.6); return st(x)
def riser(d=1.2):
    t = T(d); n = rng.standard_normal(len(t)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        fc = 400 + 7000 * (i / len(n)) ** 2
        y[i:i + seg] = sosfilt(butter(2, [fc * .7, min(fc * 1.4, 20000)], btype='band', fs=SR, output='sos'), n[i:i + seg])
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / d) ** 2) / SR) * 0.25
    x = (y + tone) * (t / d) ** 2.2; return st(x, 1)
def tick():
    t = T(0.06); x = np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 140) + 0.4 * hp(rng.standard_normal(len(t)), 4000) * np.exp(-t * 300)
    return st(x)
def pop():
    t = T(0.14); f = 1100 * np.exp(-t * 28) + 220; x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 34)
    return st(x)
def bubbles(d=1.4, n=16):
    x = np.zeros(int(d * SR) + SR // 4)
    for k in range(n):
        o = int(rng.uniform(0, d * 0.9) * SR); tt = T(rng.uniform(.03, .07)); f0 = rng.uniform(500, 1600)
        b = np.sin(2 * np.pi * np.cumsum(f0 * (1 + 2.2 * tt / tt[-1])) / SR) * np.exp(-tt * 70) * rng.uniform(.4, 1)
        x[o:o + len(b)] += b
    return st(hp(x, 300), 0.6)
def sparkle(d=1.0, n=12):
    x = np.zeros(int(d * SR) + SR // 2)
    for k in range(n):
        o = int(rng.uniform(0, d * .8) * SR); b = bell(rng.uniform(2800, 6500), .4, parts=((1, 1), (2.01, .3)), dec=13)
        x[o:o + len(b)] += b * rng.uniform(.4, 1)
    x = hp(x, 1800); return np.stack([x, np.roll(x, int(.012 * SR))], 1)
def shimmer():
    x = np.zeros(int(2.2 * SR))
    for i, f in enumerate([1046.5, 1318.5, 1568.0, 1975.5, 2637.0]):
        b = bell(f, 1.8, dec=2.6); o = int(i * 0.06 * SR); x[o:o + len(b)] += b * (0.9 ** i)
    return st(x, 1)
def tap():  # UI button tap
    t = T(0.12); x = np.sin(2 * np.pi * 1500 * t) * np.exp(-t * 60) + .6 * np.sin(2 * np.pi * 750 * t) * np.exp(-t * 45)
    return st(x)
def cash():
    a = bell(2093, .9, dec=5); b = bell(2637, 1.1, dec=4.5); x = np.zeros(int(1.4 * SR))
    x[:len(a)] += a; o = int(.09 * SR); x[o:o + len(b)] += b
    c = hp(rng.standard_normal(int(.05 * SR)), 3000) * np.exp(-T(.05) * 80) * .5; x[:len(c)] += c; return st(x)
def clock(d=4.0, bpm=120):
    x = np.zeros(int(d * SR)); step = 60 / bpm
    for i in range(int(d / step)):
        t = T(.05); f = 3200 if i % 2 == 0 else 2600
        b = np.sin(2 * np.pi * f * t) * np.exp(-t * 180) + .5 * hp(rng.standard_normal(len(t)), 5000) * np.exp(-t * 400)
        o = int(i * step * SR); x[o:o + len(b)] += b
    return st(x)
def swipe():
    return whoosh(0.32, 900, 9000)
def heart():
    x = np.zeros(int(0.9 * SR))
    for o, a in [(0, 1), (0.2, .7)]:
        t = T(.18); b = np.sin(2 * np.pi * (55 + 40 * np.exp(-t * 30)) * t) * np.exp(-t * 18) * a
        x[int(o * SR):int(o * SR) + len(b)] += b
    return st(np.tanh(x * 2))

for name, fn in dict(whoosh=whoosh, boom=boom, riser=riser, tick=tick, pop=pop, bubbles=bubbles, sparkle=sparkle,
                     shimmer=shimmer, tap=tap, cash=cash, clock=clock, swipe=swipe, heart=heart).items():
    y = norm(fn(), -1.0).astype(np.float32); sf.write(f"{out}/{name}.wav", y, SR)

# ---------------- music bed: 120 bpm, Am9 - Fmaj7 - Cmaj9 - G6, 40.5 s -----------------
BPM = 120; beat = 60 / BPM; DUR = 41.0; N = int(DUR * SR); mix = np.zeros((N, 2))
def put(x, t0, g=1.0):
    i = int(t0 * SR)
    if i >= N: return
    x = st(x) if x.ndim == 1 else x; j = min(N, i + len(x)); mix[i:j] += x[:j - i] * g
def kick():
    t = T(.45); f = 45 + 120 * np.exp(-t * 32); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    return np.tanh(x * 1.4)
def hat(open_=False):
    d = .22 if open_ else .05; t = T(d); return hp(rng.standard_normal(len(t)), 7500) * np.exp(-t * (18 if open_ else 90))
def clap():
    t = T(.25); n = bp(rng.standard_normal(len(t)), 900, 3500); env = np.zeros_like(t)
    for o in [0, .011, .022]: env += (t >= o) * np.exp(-(t - o).clip(0) * 60)
    return n * env * .7 + n * np.exp(-t * 14) * .3
def note(f): return 440 * 2 ** ((f - 69) / 12)
def pad_chord(midis, d):
    t = T(d); x = np.zeros(len(t))
    for m in midis:
        for det in (-0.08, 0.08):
            fr = note(m + det); ph = rng.uniform(0, 6.28)
            saw = 2 * ((fr * t + ph / 6.28) % 1) - 1; x += saw
    x = lp(x, 1400, 4) / len(midis) * 0.5
    env = np.minimum(1, t / .3) * np.minimum(1, (d - t) / .4); return x * env
def stab(midis):
    t = T(.35); x = sum(np.sin(2 * np.pi * note(m) * t) + .3 * np.sin(4 * np.pi * note(m) * t) for m in midis)
    return x / len(midis) * np.exp(-t * 9) * np.minimum(1, t / .003)
def bass(m, d):
    t = T(d); x = np.sin(2 * np.pi * note(m) * t) + .25 * np.sin(4 * np.pi * note(m) * t)
    return x * np.minimum(1, t / .01) * np.exp(-t * 2.2)
prog = [([57, 60, 64, 67, 71], 45), ([53, 57, 60, 64, 67], 41), ([48, 52, 55, 59, 62], 36), ([55, 59, 62, 64, 67], 43)]
DROP = 2.5  # beat drops on the hook question
bars = int(DUR / (4 * beat)) + 1
for b in range(bars):
    t0 = b * 4 * beat; ch, bn = prog[b % 4]
    put(pad_chord(ch, 4 * beat + .3), t0, .55)
    for k in range(4):
        tb = t0 + k * beat
        if tb >= DROP - 0.01:
            put(kick(), tb, .9); put(hat(), tb + beat / 2, .25)
            if k % 2 == 1: put(clap(), tb, .35)
            put(bass(bn, beat * .9), tb + beat / 2, .55)
        put(hat(), tb + beat / 4 * 3, .10)
    if t0 >= DROP: put(stab(ch[1:]), t0 + beat * 1.5, .22); put(stab(ch[1:]), t0 + beat * 3.5, .18)
mix[:, 0] = mix[:, 0]; mix = np.tanh(mix * 0.9)
t = T(DUR); fadein = np.minimum(1, t / 0.4); fade = np.minimum(1, (DUR - t) / 1.2)
# intro (before drop) low-passed / softer
intro = int(DROP * SR); mix[:intro] = lp(mix[:intro], 900) * 0.7
mix *= (fadein * fade)[:, None]
sf.write(f"{out}/music.wav", norm(mix, -1.0).astype(np.float32), SR)
print("done")
