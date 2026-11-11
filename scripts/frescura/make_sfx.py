"""Synthesised SFX kit + minimal luxury beat bed for the Frescura Body ad.
Usage: python make_sfx.py OUT_DIR BED_SECONDS"""
import sys, os, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
OUT = sys.argv[1]; BED = float(sys.argv[2]) if len(sys.argv) > 2 else 34.0
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(11)
T = lambda d: np.arange(int(d * SR)) / SR


def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype="band", fs=SR, output="sos"), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype="high", fs=SR, output="sos"), x)
def st(x, w=0.0):
    d = int(w * SR); r = np.roll(x, d) if d else x
    return np.stack([x, r], 1)
def norm(x, db=-1.0): return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)
def bell(f, d, decay=6.0, partials=((1, 1), (2.0, .35), (3.01, .15), (4.2, .07))):
    t = T(d); x = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-decay * m ** .5 * t) for m, a in partials)
    return x * np.minimum(1, t / 0.002)


def whoosh(d=0.6, lo=250, hi=4200, rev=False):
    n = rng.standard_normal(int(d * SR)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = lo + (hi - lo) * np.sin(np.pi * p) ** 2
        y[i:i + seg] = bp(n[i:i + seg], max(fc * .55, 40), min(fc * 1.7, 20000))
    t = T(d); env = np.sin(np.pi * (t / d) ** (0.6 if not rev else 1.6)) ** 2
    x = y * env
    L = x * (1 - t / d) + .25 * x; R = x * (t / d) + .25 * x
    s = np.stack([L, R], 1)
    return s[::-1] if rev else s


def riser(d=1.4):
    t = T(d); n = rng.standard_normal(len(t)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = 300 + 7000 * p ** 2
        y[i:i + seg] = bp(n[i:i + seg], fc * .7, min(fc * 1.4, 20000))
    tone = np.sin(2 * np.pi * np.cumsum(180 + 900 * (t / d) ** 2) / SR) * .25
    x = (y + tone) * (t / d) ** 2.2
    return st(x, .009)


def impact(d=1.8):
    t = T(d); f = 38 + 110 * np.exp(-t * 22)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.8)
    cr = lp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 18) * .6
    tail = bp(rng.standard_normal(len(t)), 120, 900) * np.exp(-t * 3.5) * .25
    x = np.tanh((sub * 1.3 + cr + tail) * 1.4)
    return st(x, .004)


def tap():
    t = T(0.08); x = hp(rng.standard_normal(len(t)), 1800) * np.exp(-t * 160) + np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 90) * .6
    return st(x)


def pop():
    t = T(0.14); f = 1100 * np.exp(-t * 28) + 220
    return st(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 38))


def bubbles(d=1.2, n=16):
    x = np.zeros(int((d + .2) * SR))
    for k in range(n):
        o = int(rng.uniform(0, d) * SR); t = T(rng.uniform(.03, .07))
        f = rng.uniform(500, 1400); f = f * (1 + 2.5 * t / t[-1])
        b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 60) * rng.uniform(.3, 1)
        x[o:o + len(b)] += b
    return st(x, .007)


def shimmer(d=1.3, n=22):
    x = np.zeros(int((d + .5) * SR))
    for k in range(n):
        o = int(rng.uniform(0, d * .85) * SR); f = rng.uniform(2800, 7500)
        b = bell(f, .4, decay=13, partials=((1, 1), (2.01, .3))); x[o:o + len(b)] += b * rng.uniform(.3, 1)
    x = hp(x, 2000)
    return st(x, .012)


def ding():
    a = bell(1567.98, 1.6, 4.0); b = bell(2093.0, 1.4, 4.5)
    x = np.zeros(int(1.8 * SR)); x[:len(a)] += a; o = int(.09 * SR); x[o:o + len(b)] += b * .8
    return st(x, .006)


def tick():
    t = T(0.03); return st(hp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 300) * .7 + np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 200))


def drop():  # water droplet "plip"
    t = T(0.25); f = 700 + 1800 * (1 - np.exp(-t * 40))
    return st(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 22) * np.minimum(1, t / .002))


def swell(d=1.6):  # soft reverse-cymbal swell
    t = T(d); x = hp(rng.standard_normal(len(t)), 4000) * (t / d) ** 3
    return st(x, .01)


def heartbeat_tick():
    t = T(0.12); return st(np.sin(2 * np.pi * 90 * t) * np.exp(-t * 35))


SFX = dict(whoosh=lambda: whoosh(.55), whoosh_l=lambda: whoosh(.9, 150, 3200), whoosh_s=lambda: whoosh(.32, 600, 6000),
           rwhoosh=lambda: whoosh(.7, 300, 5000, rev=True), riser=riser, impact=impact, tap=tap, pop=pop,
           bubbles=bubbles, shimmer=shimmer, ding=ding, tick=tick, drop=drop, swell=swell, thump=heartbeat_tick)
for k, f in SFX.items():
    y = norm(f(), -1.0); sf.write(f"{OUT}/{k}.wav", y.astype(np.float32), SR)

# ---------- music bed: 116 BPM minimal deep/lux groove, Am - Fmaj7 - Cmaj7 - G ----------
BPM = 116; beat = 60 / BPM; N = int(BED * SR)
L = np.zeros(N); R = np.zeros(N)
def put(buf, x, t0, g=1.0):
    i = int(t0 * SR); j = min(N, i + len(x))
    if i < N: buf[i:j] += x[:j - i] * g
def kick():
    t = T(.45); f = 45 + 120 * np.exp(-t * 30); return np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) * 2)
def hat(o=False):
    t = T(.18 if o else .05); return hp(rng.standard_normal(len(t)), 7000) * np.exp(-t * (25 if o else 110))
def clap():
    t = T(.25); n = bp(rng.standard_normal(len(t)), 900, 5000)
    env = sum(np.exp(-np.clip(t - d, 0, None) * 120) * (t >= d) for d in (0, .012, .024)) + np.exp(-t * 18) * .4
    return n * env
mid = lambda m: 440 * 2 ** ((m - 69) / 12)
CH = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 66]]  # Am7 Fmaj7 Cmaj7 G(maj7)
BASS = [45, 41, 36, 43]
bars = int(BED / (4 * beat)) + 1
K, Hh, C = kick(), hat(), clap()
for b in range(bars):
    t0 = b * 4 * beat; ci = b % 4
    for q in range(4):
        tq = t0 + q * beat
        put(L, K, tq, .9); put(R, K, tq, .9)
        put(L, hat(), tq + beat / 2, .22); put(R, hat(), tq + beat / 2 + .004, .26)
        put(L, hat(), tq + beat / 4, .07); put(R, hat(), tq + 3 * beat / 4, .07)
        if q in (1, 3): put(L, C, tq, .28); put(R, C, tq + .003, .28)
    # sub bass: off-beat pulses
    for q in range(4):
        for e in (0.5,):
            tb = t0 + (q + e) * beat; t = T(beat * .45); f = mid(BASS[ci])
            x = (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * 2 * f * t)) * np.minimum(1, t / .005) * np.exp(-t * 4)
            put(L, x, tb, .5); put(R, x, tb, .5)
    # pad stab chords (plucky, filtered)
    for s, (pos, g) in enumerate([(0, .22), (1.5, .14), (3.0, .16)]):
        t = T(beat * 1.3); x = np.zeros(len(t))
        for m in CH[ci]:
            f = mid(m + 12)
            for dt in (-.06, .06):
                ph = 2 * np.pi * f * (1 + dt / 100) * t; x += (2 * ((ph / (2 * np.pi)) % 1) - 1) * .25
        x = lp(x, 2600) * np.exp(-t * 3.2) * np.minimum(1, t / .01)
        put(L, x, t0 + pos * beat, g); put(R, np.roll(x, 300), t0 + pos * beat, g)
mus = np.stack([L, R], 1); mus = np.tanh(mus * 1.1)
fi, fo = int(.4 * SR), int(1.8 * SR)
mus[:fi] *= np.linspace(0, 1, fi)[:, None]; mus[-fo:] *= np.linspace(1, 0, fo)[:, None]
sf.write(f"{OUT}/bed.wav", norm(mus, -3).astype(np.float32), SR)
print("ok", list(SFX), "bed", BED)
