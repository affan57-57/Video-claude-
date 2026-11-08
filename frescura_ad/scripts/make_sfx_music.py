# Synthesize SFX + a minimal luxury deep-house bed (no samples, no licensing issues).
# usage: python make_sfx_music.py OUTDIR MUSIC_SECONDS
import sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
OUT = sys.argv[1]
MUS_DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 34.0
rng = np.random.default_rng(11)

def t(d): return np.arange(int(d * SR)) / SR
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype="band", fs=SR, output="sos"), x, axis=0)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x, axis=0)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype="high", fs=SR, output="sos"), x, axis=0)
def norm(x, db=-1.0): return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)
def st(x, w=0.0):
    if x.ndim == 2: return x
    R = np.roll(x, int(w * SR)) if w else x
    return np.stack([x, R], 1)
def bell(f, d, partials=((1, 1), (2.0, .45), (3.01, .22), (4.2, .1)), decay=6):
    tt = t(d); x = sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-decay * m ** .5 * tt) for m, a in partials)
    return x * np.minimum(1, tt / 0.002)
def pad_to(x, n):
    return np.concatenate([x, np.zeros((n - len(x),) + x.shape[1:])]) if len(x) < n else x[:n]

# ---------- SFX ----------
def impact():  # cinematic sub boom + noise crack
    d = 2.2; tt = t(d)
    f = 38 + 90 * np.exp(-tt * 9); ph = 2 * np.pi * np.cumsum(f) / SR
    sub = np.sin(ph) * np.exp(-tt * 1.8)
    crack = hp(rng.standard_normal(len(tt)), 1500) * np.exp(-tt * 28) * 0.5
    body = lp(rng.standard_normal(len(tt)), 400) * np.exp(-tt * 6) * 0.8
    x = np.tanh(1.6 * (sub + crack + body))
    return st(x, 0.009)

def riser(d=1.6):
    tt = t(d); n = rng.standard_normal(len(tt)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = 400 + 7000 * p ** 2
        y[i:i + seg] = sosfilt(butter(2, [fc * .7, min(fc * 1.4, 20000)], btype="band", fs=SR, output="sos"), n[i:i + seg])
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * (tt / d) ** 2) / SR) * 0.25
    env = (tt / d) ** 2.2
    return st((y + tone) * env, 0.013)

def whoosh(d=0.55, lo=300, hi=4200):
    tt = t(d); n = rng.standard_normal(len(tt)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = lo + (hi - lo) * np.sin(np.pi * p) ** 2
        y[i:i + seg] = sosfilt(butter(2, [fc * .6, fc * 1.6], btype="band", fs=SR, output="sos"), n[i:i + seg])
    env = np.sin(np.pi * tt / d) ** 2
    x = y * env; L = x * (1 - tt / d) + .25 * x; R = x * (tt / d) + .25 * x
    return np.stack([L, R], 1)

def swish(): return whoosh(0.28, 900, 7000)

def pop():
    tt = t(0.14); f = 1100 * np.exp(-tt * 34) + 220; ph = 2 * np.pi * np.cumsum(f) / SR
    return st(np.sin(ph) * np.exp(-tt * 38))

def tap():  # UI click
    tt = t(0.06); x = hp(rng.standard_normal(len(tt)), 2500) * np.exp(-tt * 160) + np.sin(2 * np.pi * 2200 * tt) * np.exp(-tt * 90) * .6
    return st(x)

def ding():  # luxury crystal bell (major 6th dyad)
    a = bell(1567.98, 1.6, decay=3.2); b = bell(2637.0, 1.4, decay=4) * .5
    return st(pad_to(a, len(a)) + pad_to(b, len(a)), 0.007)

def sparkle(d=1.1, n=18):
    x = np.zeros(int(d * SR) + SR // 2)
    for k in range(n):
        o = int(rng.uniform(0, d * .85) * SR); f = rng.uniform(2800, 7000)
        b = bell(f, .35, partials=((1, 1), (2.01, .3)), decay=14); x[o:o + len(b)] += b * rng.uniform(.4, 1)
    x = hp(x, 1800)
    return np.stack([x, np.roll(x, int(.011 * SR))], 1)

def stamp():  # heavy stamp thud
    tt = t(0.6); f = 70 + 160 * np.exp(-tt * 25); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)
    k = lp(rng.standard_normal(len(tt)), 2500) * np.exp(-tt * 45)
    return st(np.tanh(2 * (s + .7 * k)))

def kaching():
    x = np.zeros(int(1.4 * SR))
    clk = hp(rng.standard_normal(int(.05 * SR)), 2000) * np.exp(-np.arange(int(.05 * SR)) / SR * 90)
    x[:len(clk)] += clk * .8
    for i, f in enumerate([2093.0, 2637.0, 3136.0]):
        b = bell(f, 1.2, decay=3.5); o = int((.06 + i * .045) * SR); x[o:o + len(b)] += b[:len(x) - o] * .6
    return st(x, .006)

def tick():
    tt = t(0.04); return st(hp(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 220) + np.sin(2 * np.pi * 3800 * tt) * np.exp(-tt * 200) * .4)

def glitch():
    d = .35; n = int(d * SR); x = np.zeros(n); i = 0
    while i < n:
        L = int(rng.uniform(.008, .03) * SR); f = rng.choice([180, 360, 720, 1440, 90])
        seg = np.sign(np.sin(2 * np.pi * f * np.arange(L) / SR)) * rng.uniform(.3, 1)
        if rng.random() < .4: seg = rng.standard_normal(L) * .6
        x[i:i + L] = seg[:n - i]; i += L + int(rng.uniform(0, .01) * SR)
    return st(lp(x, 6000) * np.hanning(n) ** .3)

def shimmer(d=2.0):  # soft airy pad swell for luxury reveals
    tt = t(d); x = sum(np.sin(2 * np.pi * f * tt + rng.uniform(0, 6)) for f in [1046.5, 1318.5, 1568, 2093, 2637])
    x = x * np.sin(np.pi * tt / d) ** 2 + hp(rng.standard_normal(len(tt)), 6000) * .15 * np.sin(np.pi * tt / d)
    return st(x, .017)

def bubble():  # foam bubbles
    x = np.zeros(int(1.0 * SR))
    for k in range(26):
        o = int(rng.uniform(0, .85) * SR); d = rng.uniform(.03, .07); tt = t(d)
        f0 = rng.uniform(600, 1800); f = f0 * (1 + 2.5 * tt / d)
        b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 60); x[o:o + len(b)] += b * rng.uniform(.3, 1)
    return st(x, .004)

def bass_drop():
    d = 1.0; tt = t(d); f = 120 * np.exp(-tt * 3) + 35; s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.5)
    return st(np.tanh(2 * s))

SFX = dict(impact=impact, riser=riser, whoosh=whoosh, swish=swish, pop=pop, tap=tap, ding=ding, sparkle=sparkle,
           stamp=stamp, kaching=kaching, tick=tick, glitch=glitch, shimmer=shimmer, bubble=bubble, drop=bass_drop)
for name, fn in SFX.items():
    y = norm(fn(), -1.0).astype(np.float32); sf.write(f"{OUT}/{name}.wav", y, SR)

# ---------- MUSIC: 122 BPM minimal lux house ----------
BPM = 122; beat = 60 / BPM; N = int(MUS_DUR * SR)
mix = np.zeros((N, 2))
def place(sig, at, gain=1.0):
    s = st(sig) if sig.ndim == 1 else sig
    i = int(at * SR)
    if i >= N: return
    L = min(len(s), N - i); mix[i:i + L] += s[:L] * gain

def kick():
    tt = t(.45); f = 48 + 140 * np.exp(-tt * 38); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7)
    return np.tanh(1.8 * (x + hp(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 300) * .3))
def hat(open_=False):
    d = .22 if open_ else .05; tt = t(d); return hp(rng.standard_normal(len(tt)), 8000) * np.exp(-tt * (18 if open_ else 110))
def clap():
    tt = t(.25); n = bp(rng.standard_normal(len(tt)), 900, 5000)
    env = sum(np.exp(-np.clip(tt - o, 0, None) * 70) * (tt >= o) for o in (0, .011, .022)) * .5 + np.exp(-tt * 18) * (tt >= .022)
    return n * env
def saw(f, d):
    tt = t(d); return sum(np.sin(2 * np.pi * f * k * tt) / k for k in range(1, 12))

# chord progression (Fm9 - Dbmaj7 - Ab(add9) - Eb6), 2 bars each, warm filtered pad
mid = lambda n: 440 * 2 ** ((n - 69) / 12)
chords = [[53, 56, 60, 63, 67], [49, 53, 56, 60, 65], [56, 60, 63, 70, 72], [51, 55, 58, 60, 67]]
roots = [41, 37, 44, 39]
bar = 4 * beat
nb = int(MUS_DUR / beat) + 1
for b in range(nb):
    at = b * beat
    section = at / MUS_DUR
    place(kick(), at, .9)
    place(hat(), at + beat / 2, .22)
    place(hat(), at + beat / 4 * 3, .08)
    if b % 2 == 1: place(clap(), at, .38)
    if b % 8 == 7: place(hat(True), at + beat / 2, .18)
for c in range(int(MUS_DUR / (2 * bar)) + 1):
    at = c * 2 * bar; ch = chords[c % 4]
    d = 2 * bar
    pad = sum(saw(mid(n), d) for n in ch) / len(ch)
    pad = lp(pad, 1400) * np.minimum(1, t(d) / .4) * np.minimum(1, (d - t(d)) / .3)
    place(np.stack([pad, np.roll(pad, int(.015 * SR))], 1), at, .16)
    # sub bass on offbeats
    for b8 in range(8):
        tt = t(beat * .45); f = mid(roots[c % 4] - 12)
        bs = np.tanh(2 * np.sin(2 * np.pi * f * tt)) * np.exp(-tt * 5) * np.minimum(1, tt / .005)
        place(lp(bs, 300), at + b8 * beat + beat / 2, .42)
    # pluck arp
    for s16 in range(0, 32, 3):
        n = ch[(s16 // 3) % len(ch)] + 12; tt = t(.3)
        pl = lp(saw(mid(n), .3), 3000) * np.exp(-tt * 14)
        place(np.stack([pl * .7, np.roll(pl, int(.02 * SR))], 1), at + s16 * beat / 4, .07)

# sidechain pump from kick
env = np.ones(N)
for b in range(nb):
    i = int(b * beat * SR); L = int(beat * SR)
    if i >= N: break
    seg = 1 - .55 * np.exp(-np.arange(min(L, N - i)) / SR * 9)
    env[i:i + len(seg)] = seg
mix *= env[:, None]
mix = np.tanh(mix * 1.2)
mix = norm(mix, -1.0).astype(np.float32)
sf.write(f"{OUT}/music.wav", mix, SR)
print("ok beat=", beat)
