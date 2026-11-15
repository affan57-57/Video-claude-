# Synthesised SFX + minimal luxury groove (deterministic). Usage: python make_sfx_lux.py OUTDIR
import numpy as np, soundfile as sf, sys, os
from scipy.signal import butter, sosfilt, fftconvolve
SR = 48000; OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(11)
T = lambda d: np.arange(int(d * SR)) / SR
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype='band', fs=SR, output='sos'), x, axis=0)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype='low', fs=SR, output='sos'), x, axis=0)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype='high', fs=SR, output='sos'), x, axis=0)
def norm(x, db=-1.0): return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)
def st(x, w=0.0):
    d = int(0.009 * SR); r = np.concatenate([np.zeros(d), x])[:len(x)]
    return np.stack([x, x * (1 - w) + r * w], 1)
def verb(x, d=1.6, mix=0.25):
    n = int(d * SR); ir = rng.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR * 4.5)[:, None]
    ir = lp(ir, 7000); y = np.stack([fftconvolve(x[:, c], ir[:, c])[:len(x)] for c in range(2)], 1)
    return x * (1 - mix) + norm(y, -6) * mix * np.max(np.abs(x))
def pad(x, d): return np.concatenate([x, np.zeros((int(d * SR), 2))]) if x.ndim == 2 else np.concatenate([x, np.zeros(int(d * SR))])

def whoosh(d=0.55, lo=250, hi=5200, rev=False):
    n = rng.standard_normal(int(d * SR)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = lo + (hi - lo) * (np.sin(np.pi * p) ** 2)
        y[i:i + seg] = sosfilt(butter(2, [fc * .55, min(fc * 1.7, 20000)], btype='band', fs=SR, output='sos'), n[i:i + seg])
    tt = T(d); env = (tt / d) ** 2.2 if rev else np.sin(np.pi * tt / d) ** 1.6
    x = y * env; L = x * (1.1 - tt / d); R = x * (0.1 + tt / d)
    return verb(np.stack([L, R], 1), 1.0, .2)
def impact(d=1.8):
    tt = T(d); f = 38 + 90 * np.exp(-tt * 18); ph = 2 * np.pi * np.cumsum(f) / SR
    sub = np.sin(ph) * np.exp(-tt * 2.6)
    cr = hp(rng.standard_normal(len(tt)), 900) * np.exp(-tt * 28) * .5
    body = lp(rng.standard_normal(len(tt)), 400) * np.exp(-tt * 9) * .8
    return verb(st(np.tanh(1.6 * (sub + cr + body)), .4), 2.2, .3)
def riser(d=1.2):
    tt = T(d); n = rng.standard_normal(len(tt)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        fc = 400 + 7000 * (i / len(n)) ** 2
        y[i:i + seg] = sosfilt(butter(2, [fc * .7, fc * 1.4], btype='band', fs=SR, output='sos'), n[i:i + seg])
    tone = np.sin(2 * np.pi * np.cumsum(220 + 660 * (tt / d) ** 2) / SR) * .25
    return st((y + tone) * (tt / d) ** 2, .5)
def bell(f, d, parts=((1, 1), (2.0, .35), (3.01, .18), (4.2, .08)), dec=5):
    tt = T(d); x = sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-dec * m ** .5 * tt) for m, a in parts)
    return x * np.minimum(1, tt / .002)
def shimmer(d=1.4, n=22):
    x = np.zeros(int(d * SR) + SR)
    for k in range(n):
        o = int((k / n) ** 1.3 * d * .85 * SR); b = bell(rng.uniform(2800, 7500), .5, ((1, 1), (2.01, .3)), 12)
        x[o:o + len(b)] += b * rng.uniform(.35, 1)
    return verb(st(hp(x, 2000), .8), 1.8, .35)
def tick():
    tt = T(.05); x = np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 160) + hp(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 300) * .5
    return st(x)
def pop():
    tt = T(.14); f = 1100 * np.exp(-tt * 32) + 220; x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 36); return st(x)
def bubbles(d=1.6, n=16):
    x = np.zeros(int(d * SR) + SR // 4)
    for k in range(n):
        tt = T(.06); f0 = rng.uniform(500, 1400); f = f0 * (1 + 2.5 * tt / .06)
        b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 70); o = int(rng.uniform(0, d) * SR); x[o:o + len(b)] += b * rng.uniform(.4, 1)
    return verb(st(x, .6), .8, .2)
def clink():
    x = bell(3520, 1.6, ((1, 1), (2.76, .5), (5.4, .25), (8.9, .12)), 4) + .6 * bell(4186, 1.6, ((1, 1), (2.7, .3)), 5)
    return verb(st(x, .7), 2.0, .3)
def ding():  # checkout / success two-note
    a = bell(1568, 1.0, dec=4); b = bell(2093, 1.3, dec=3.5); x = np.zeros(int(1.6 * SR)); x[:len(a)] += a; o = int(.11 * SR); x[o:o + len(b)] += b
    return verb(st(x, .5), 1.4, .25)
def tap():
    tt = T(.09); x = lp(rng.standard_normal(len(tt)), 2500) * np.exp(-tt * 90) + np.sin(2 * np.pi * 180 * tt) * np.exp(-tt * 60)
    return st(x)
def stamp():
    tt = T(.6); x = lp(rng.standard_normal(len(tt)), 1800) * np.exp(-tt * 22) + np.sin(2 * np.pi * np.cumsum(90 * np.exp(-tt * 9) + 50) / SR) * np.exp(-tt * 10)
    return verb(st(np.tanh(2 * x), .3), .9, .2)
def swipe(d=.28): return whoosh(d, 1200, 9000)

fx = dict(whoosh=whoosh(), whoosh_long=whoosh(.9, 150, 4000), whoosh_rev=whoosh(.7, 300, 6000, True), impact=impact(),
          riser=riser(), shimmer=shimmer(), tick=tick(), pop=pop(), bubbles=bubbles(), clink=clink(), ding=ding(),
          tap=tap(), stamp=stamp(), swipe=swipe())
for k, v in fx.items():
    sf.write(f"{OUT}/{k}.wav", norm(pad(v, .05), -1).astype(np.float32), SR)

# ---- Minimal luxury groove, 118 BPM, Am9 - Fmaj7 - Cmaj7 - G6 ----
BPM = 118; beat = 60 / BPM; bars = 16; L = int(bars * 4 * beat * SR) + SR * 3
mus = np.zeros((L, 2))
def add(buf, x, t, g=1.0):
    i = int(t * SR); x = x if x.ndim == 2 else st(x); n = min(len(x), len(buf) - i)
    if n > 0: buf[i:i + n] += x[:n] * g
def kick():
    tt = T(.45); f = 45 + 120 * np.exp(-tt * 30); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7) + hp(rng.standard_normal(len(tt)), 4000) * np.exp(-tt * 400) * .2
def hat(o=False):
    tt = T(.25 if o else .06); return hp(rng.standard_normal(len(tt)), 7500) * np.exp(-tt * (18 if o else 90))
def clap():
    tt = T(.3); n = bp(rng.standard_normal(len(tt)), 900, 4000); e = sum(np.exp(-np.maximum(tt - k * .011, 0) * 60) * (tt >= k * .011) for k in range(3)) * .5 + np.exp(-tt * 14) * .5
    return n * e
def note(f, d, kind='pad'):
    tt = T(d)
    if kind == 'pad':
        x = sum(np.sin(2 * np.pi * f * dt * tt + p) for dt, p in ((1, 0), (1.004, 1), (.996, 2), (2.001, .5)))
        env = np.minimum(1, tt / .35) * np.minimum(1, (d - tt) / .5); return lp(x * env, 2200) * .25
    if kind == 'bass':
        x = np.sin(2 * np.pi * f * tt) + .3 * np.tanh(3 * np.sin(2 * np.pi * f * tt)); env = np.minimum(1, tt / .01) * np.exp(-tt * 3.5); return lp(x * env, 600)
    if kind == 'pluck':
        x = np.sign(np.sin(2 * np.pi * f * tt)) * .5 + np.sin(2 * np.pi * 2 * f * tt) * .3; return lp(x * np.exp(-tt * 9), 3000) * .5
mid = lambda m: 440 * 2 ** ((m - 69) / 12)
chords = [[57, 60, 64, 67, 71], [53, 57, 60, 64, 69], [48, 55, 59, 64, 67], [55, 59, 62, 64, 69]]
roots = [45, 41, 36, 43]
for b in range(bars):
    t0 = b * 4 * beat; c = chords[b % 4]
    for m in c: add(mus, st(note(mid(m), 4 * beat + .4), .6), t0, .5)
    for k in range(4):
        add(mus, kick(), t0 + k * beat, .9)
        add(mus, hat(), t0 + k * beat + beat / 2, .28); add(mus, hat(), t0 + k * beat + beat * .75, .12)
        if k in (1, 3): add(mus, clap(), t0 + k * beat, .35)
    for k, off in enumerate([0, .75, 1.5, 2.5, 3.0]):
        add(mus, note(mid(roots[b % 4]) * (2 if k == 3 else 1), beat * .9, 'bass'), t0 + off * beat, .55)
    arp = [c[2], c[4], c[3], c[1]]
    for k in range(8):
        if (b + k) % 3 != 2: add(mus, st(note(mid(arp[k % 4] + 12), .4, 'pluck'), .9), t0 + k * beat / 2 + beat / 4, .12)
mus = verb(mus, 1.5, .15)
sf.write(f"{OUT}/music.wav", norm(mus, -3).astype(np.float32), SR)
print("ok", list(fx), round(L / SR, 1))
