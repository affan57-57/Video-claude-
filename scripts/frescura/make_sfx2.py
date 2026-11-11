# Synthesized SFX + minimal luxury music bed for the Frescura Body feedback ad.
# Usage: python make_sfx2.py OUTDIR BPM DURATION
import numpy as np, soundfile as sf, sys, os
from scipy.signal import butter, sosfilt
SR = 48000
out = sys.argv[1]; BPM = float(sys.argv[2]); DUR = float(sys.argv[3])
os.makedirs(out, exist_ok=True)
rng = np.random.default_rng(11)
t = lambda d: np.arange(int(d * SR)) / SR
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], btype='band', fs=SR, output='sos'), x, axis=0)
def hp(x, f): return sosfilt(butter(2, f, btype='high', fs=SR, output='sos'), x, axis=0)
def lp(x, f): return sosfilt(butter(2, f, btype='low', fs=SR, output='sos'), x, axis=0)
def st(x, w=0.0):
    if x.ndim == 2: return x
    return np.stack([x, np.roll(x, int(w * SR))], 1)
def norm(x, db): return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)
def bell(f, d, partials=((1, 1), (2.0, .35), (3.01, .15)), decay=6):
    tt = t(d); x = sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-decay * m ** .5 * tt) for m, a in partials)
    return x * np.minimum(1, tt / 0.002)

def impact(d=1.6):  # cinematic sub boom + noise crack
    tt = t(d); f = 120 * np.exp(-tt * 9) + 38
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.6)
    crack = hp(rng.standard_normal(len(tt)), 1800) * np.exp(-tt * 28) * 0.5
    body = bp(rng.standard_normal(len(tt)), 150, 900) * np.exp(-tt * 7) * 0.35
    x = np.tanh(1.8 * (sub + crack + body)); return st(x, 0.009)
def riser(d=1.2):
    tt = t(d); p = tt / d
    n = rng.standard_normal(len(tt)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        fc = 400 + 7000 * (i / len(n)) ** 2
        y[i:i + seg] = sosfilt(butter(2, [fc * .7, fc * 1.4], btype='band', fs=SR, output='sos'), n[i:i + seg])
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * p ** 2) / SR) * 0.25
    x = (y + tone) * p ** 2.2; x[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR)); return st(x, 0.007)
def whoosh(d=0.55, up=True):
    tt = t(d); n = rng.standard_normal(len(tt)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = 500 + 4500 * (np.sin(np.pi * p) ** 2)
        y[i:i + seg] = sosfilt(butter(2, [fc * .6, fc * 1.6], btype='band', fs=SR, output='sos'), n[i:i + seg])
    env = np.sin(np.pi * tt / d) ** 3; x = y * env
    L = x * (1 - tt / d) + .25 * x; R = x * (tt / d) + .25 * x; return np.stack([L, R], 1)
def tick():  # crisp UI tick for text pops
    tt = t(0.06); x = np.sin(2 * np.pi * 2900 * tt) * np.exp(-tt * 140) + hp(rng.standard_normal(len(tt)), 4000) * np.exp(-tt * 300) * .4
    return st(x)
def pop():
    tt = t(0.14); f = 1100 * np.exp(-tt * 35) + 220
    return st(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 38))
def bubbles(d=1.4, n=26):  # foam bubble pops
    x = np.zeros(int(d * SR) + SR // 4)
    for k in range(n):
        o = int(rng.uniform(0, d) * SR); tt = t(rng.uniform(.02, .05)); f0 = rng.uniform(500, 1600)
        b = np.sin(2 * np.pi * np.cumsum(f0 * (1 + 2.5 * tt / tt[-1])) / SR) * np.exp(-tt * 90) * rng.uniform(.3, 1)
        x[o:o + len(b)] += b
    return st(hp(x, 300), 0.004)
def shimmer(d=1.3, n=18):
    x = np.zeros(int(d * SR) + SR // 2)
    for k in range(n):
        o = int((k / n) * d * 0.85 * SR); f = 2200 * 2 ** (rng.integers(0, 12) / 12 * 1.5)
        b = bell(f, .5, decay=10); x[o:o + len(b)] += b * rng.uniform(.4, 1)
    x = hp(x, 1500); return np.stack([x, np.roll(x, int(.013 * SR))], 1)
def chime():  # luxury two-note chime
    a = bell(1174.7, 1.4, decay=3.5); b = bell(1568, 1.6, decay=3.2)
    x = np.zeros(int(1.9 * SR)); x[:len(a)] += a; o = int(.12 * SR); x[o:o + len(b)] += b * .8; return st(x, .011)
def shutter():
    tt = t(0.12); n = hp(rng.standard_normal(len(tt)), 2500)
    env = np.exp(-((tt - .015) / .006) ** 2) + .7 * np.exp(-((tt - .07) / .008) ** 2); return st(n * env)
def cash():  # checkout "ka-ching"
    x = np.zeros(int(1.3 * SR)); clk = hp(rng.standard_normal(int(.03 * SR)), 3000) * np.exp(-t(.03) * 200)
    x[:len(clk)] += clk; o = int(.07 * SR)
    for f, a in ((2637, 1), (3520, .7), (5274, .3)):
        b = bell(f, 1.2, decay=4.5); x[o:o + len(b)] += b * a
    return st(x, .008)
def glitch():
    x = np.zeros(int(.25 * SR))
    for k in range(6):
        o = int(k * .035 * SR); L = int(.02 * SR); x[o:o + L] += np.sign(np.sin(2 * np.pi * rng.uniform(200, 1500) * t(.02))) * .4
    return st(lp(x, 6000))
def tick_clock():
    return st(bp(rng.standard_normal(int(.03 * SR)), 1500, 5000) * np.exp(-t(.03) * 250))

for name, fn in dict(impact=impact, riser=riser, whoosh=whoosh, tick=tick, pop=pop, bubbles=bubbles,
                     shimmer=shimmer, chime=chime, shutter=shutter, cash=cash, glitch=glitch, clock=tick_clock).items():
    y = norm(fn(), -1.0); sf.write(f"{out}/{name}.wav", y.astype(np.float32), SR); print(name, round(len(y) / SR, 2))

# ---- music bed: minimal luxury pulse (deep house-ish), Am9 - Fmaj7 - Cmaj7 - G6
beat = 60 / BPM; N = int(DUR * SR); mus = np.zeros((N, 2))
def put(x, at, g=1.0):
    i = int(at * SR); x = st(x) if x.ndim == 1 else x; j = min(N, i + len(x))
    if i < N: mus[i:j] += x[:j - i] * g
def kick():
    tt = t(.45); f = 150 * np.exp(-tt * 28) + 46
    return np.tanh(2 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7))
def hat(open_=False):
    d = .2 if open_ else .05; tt = t(d); return hp(rng.standard_normal(len(tt)), 7000) * np.exp(-tt * (18 if open_ else 90))
def clap():
    tt = t(.25); n = bp(rng.standard_normal(len(tt)), 900, 5000)
    env = sum(np.exp(-np.clip(tt - k * .011, 0, None) * 60) * (tt >= k * .011) for k in range(3)) * np.exp(-tt * 9)
    return n * env
mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
chords = [[57, 60, 64, 67, 71], [53, 57, 60, 64, 67], [48, 52, 55, 59, 62], [55, 59, 62, 64, 67]]
bassn = [33, 29, 36, 31]
def pad(notes, d):
    tt = t(d); x = np.zeros(len(tt))
    for m in notes:
        for det in (-.07, .07):
            ph = 2 * np.pi * mtof(m + det / 12 * 0) * (1 + det / 100) * tt
            x += (np.sin(ph) + .25 * np.sin(2 * ph) + .1 * np.sin(3 * ph))
    env = np.minimum(1, tt / .25) * np.minimum(1, (d - tt) / .3); return lp(x * env, 2800) / len(notes)
def bass(m, d):
    tt = t(d); x = np.sin(2 * np.pi * mtof(m) * tt) + .3 * np.sin(4 * np.pi * mtof(m) * tt)
    return np.tanh(1.5 * x) * np.minimum(1, tt / .01) * np.exp(-tt * 2.5)
bar = 4 * beat; nb = int(DUR / bar) + 1
for b in range(nb):
    c = b % 4; t0 = b * bar
    put(pad(chords[c], bar + .3), t0, .22)
    for k in range(4):
        put(kick(), t0 + k * beat, .9)
        put(hat(), t0 + k * beat + beat / 2, .25)
        put(hat(), t0 + k * beat + beat * .75, .08)
        if k in (1, 3): put(clap(), t0 + k * beat, .35)
        put(bass(bassn[c], beat * .45), t0 + k * beat + beat / 2, .45)
    put(hat(True), t0 + 3.5 * beat, .12)
# gentle bell motif every 2 bars
mot = [76, 79, 83, 81]
for b in range(0, nb, 2):
    for k, m in enumerate(mot):
        put(bell(mtof(m), .8, decay=5), b * bar + k * beat * 1.5, .06)
mus = mus * np.minimum(1, t(DUR)[:N, None] / .02)
sf.write(f"{out}/music.wav", norm(mus, -3).astype(np.float32), SR); print("music", DUR)
