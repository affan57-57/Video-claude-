# Synthesized SFX + minimal luxury groove for the Frescura Body ad.
# Usage: python frescura_sfx.py OUT_DIR MUSIC_SECONDS
import numpy as np, soundfile as sf, sys, os
from scipy.signal import butter, sosfilt

SR = 48000
out = sys.argv[1]; MUSIC_LEN = float(sys.argv[2]) if len(sys.argv) > 2 else 34.0
os.makedirs(out, exist_ok=True)
rng = np.random.default_rng(11)
T = lambda d: np.arange(int(d * SR)) / SR

def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype="band", fs=SR, output="sos"), x, axis=0)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x, axis=0)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype="high", fs=SR, output="sos"), x, axis=0)
def norm(x, db=-1.0): return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)
def st(x, w=0.0):
    if x.ndim == 2: return x
    d = int(w * SR); r = np.roll(x, d) if d else x
    return np.stack([x, r], 1)
def bell(f, d, partials=((1, 1), (2.0, .4), (3.01, .2), (4.2, .1)), decay=6):
    tt = T(d); x = sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-decay * m ** .5 * tt) for m, a in partials)
    return x * np.minimum(1, tt / 0.002)

def sweep_noise(d, f0, f1, q=0.5, env=None):
    n = rng.standard_normal(int(d * SR)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = f0 * (f1 / f0) ** p
        y[i:i + seg] = sosfilt(butter(2, [fc * (1 - q), min(fc * (1 + q), SR / 2 - 100)], btype="band", fs=SR, output="sos"), n[i:i + seg])
    return y

def whoosh(d=0.55):
    tt = T(d); y = sweep_noise(d, 400, 5000) ; env = np.sin(np.pi * np.minimum(1, tt / d)) ** 3
    x = y * env; pan = tt / d
    return np.stack([x * (1 - pan) + .3 * x, x * pan + .3 * x], 1)

def swish(d=0.28):  # short fast text swipe
    tt = T(d); y = sweep_noise(d, 1500, 9000, .4); env = (tt / d) ** 1.5 * np.exp(-((tt - d * .7) / (d * .25)) ** 2) * 3
    return st(y * env, 0.006)

def riser(d=1.2):
    tt = T(d); y = sweep_noise(d, 200, 7000, .35); env = (tt / d) ** 2.2
    tone = np.sin(2 * np.pi * np.cumsum(180 + 900 * (tt / d) ** 2) / SR) * .25 * (tt / d) ** 2
    return st(y * env + tone, 0.01)

def boom(d=1.6):  # deep cinematic impact
    tt = T(d); f = 38 + 110 * np.exp(-tt * 18); ph = 2 * np.pi * np.cumsum(f) / SR
    sub = np.sin(ph) * np.exp(-tt * 2.6)
    click = lp(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 60) * .9
    tail = lp(rng.standard_normal(len(tt)), 900) * np.exp(-tt * 3.5) * .25
    x = np.tanh(1.6 * (sub + click + tail))
    return st(x, 0.004)

def hit(d=0.5):  # tighter punch for text slams
    tt = T(d); f = 60 + 160 * np.exp(-tt * 30); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)
    x += hp(rng.standard_normal(len(tt)), 2500) * np.exp(-tt * 45) * .5
    return st(np.tanh(2 * x))

def ding(): return st(bell(1760, 1.1, decay=5) + .35 * bell(2637, 1.1, decay=8), 0.008)
def tick():
    tt = T(0.05); x = np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 180) + hp(rng.standard_normal(len(tt)), 4000) * np.exp(-tt * 250) * .4
    return st(x)
def pop():
    tt = T(0.14); f = 1100 * np.exp(-tt * 28) + 200; x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 35)
    return st(x)
def tap():  # UI tap for the CTA
    tt = T(0.09); x = np.sin(2 * np.pi * 1300 * tt) * np.exp(-tt * 70) + .6 * np.sin(2 * np.pi * 650 * tt) * np.exp(-tt * 50)
    return st(x)
def shimmer(d=1.4, n=26):
    x = np.zeros(int(d * SR) + SR // 2)
    for k in range(n):
        o = int((k / n) ** 1.3 * d * .85 * SR); f = rng.uniform(2600, 7500)
        b = bell(f, .45, partials=((1, 1), (2.01, .25)), decay=11); x[o:o + len(b)] += b * rng.uniform(.4, 1)
    x = hp(x, 1800); return np.stack([x, np.roll(x, int(.013 * SR))], 1)
def chime():  # luxury two-note
    a = bell(1318.5, 1.2, decay=4); b = bell(1975.5, 1.4, decay=4)
    x = np.zeros(int(1.7 * SR)); x[:len(a)] += a; o = int(.11 * SR); x[o:o + len(b)] += .8 * b
    return st(x, 0.01)
def kaching():
    x = np.zeros(int(1.2 * SR))
    for i, f in enumerate([2093, 2637, 3136, 4186]):
        b = bell(f, 1.0, decay=6); o = int(i * .035 * SR); x[o:o + len(b)] += b * (1 - i * .12)
    tt = T(.08); cl = hp(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 80)
    x[:len(cl)] += cl * 1.2
    return st(x, 0.006)
def foam():  # soft bubbly squish for the pump
    d = 0.9; x = np.zeros(int(d * SR))
    for k in range(60):
        o = int(rng.uniform(0, d * .8) * SR); tt = T(.03); f = rng.uniform(500, 1600)
        b = np.sin(2 * np.pi * np.cumsum(f * (1 + 2 * tt / .03)) / SR) * np.exp(-tt * 120); x[o:o + len(b)] += b * rng.uniform(.2, 1)
    n = bp(rng.standard_normal(len(x)), 300, 2500) * .3 * np.sin(np.pi * T(d) / d)
    return st(x + n, .007)
def heartbeat():
    x = np.zeros(int(1.0 * SR))
    for o, a in [(0, 1), (.22, .7)]:
        tt = T(.25); b = np.sin(2 * np.pi * np.cumsum(55 + 40 * np.exp(-tt * 30)) / SR) * np.exp(-tt * 18) * a
        i = int(o * SR); x[i:i + len(b)] += b
    return st(np.tanh(2 * x))

sfx = dict(whoosh=whoosh, swish=swish, riser=riser, boom=boom, hit=hit, ding=ding, tick=tick, pop=pop, tap=tap,
           shimmer=shimmer, chime=chime, kaching=kaching, foam=foam, heartbeat=heartbeat)
for k, fn in sfx.items():
    y = norm(fn(), -1.0); sf.write(f"{out}/{k}.wav", y.astype(np.float32), SR, subtype="PCM_24")

# ---- Music: 120 BPM minimal luxe-house groove (kick, clap, hats, sub, warm pad) ----
BPM = 120; beat = 60 / BPM; N = int(MUSIC_LEN * SR); mix = np.zeros((N, 2))
def place(sig, t, g=1.0):
    i = int(t * SR); s = st(sig) if sig.ndim == 1 else sig; L = min(len(s), N - i)
    if L > 0: mix[i:i + L] += s[:L] * g
def kick():
    tt = T(.35); f = 48 + 120 * np.exp(-tt * 35); return np.tanh(2.2 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7))
def clap():
    tt = T(.25); n = bp(rng.standard_normal(len(tt)), 900, 5000); e = np.exp(-tt * 22)
    for o in (.0, .011, .022): e = e + np.exp(-np.maximum(tt - o, 0) * 120) * (tt >= o) * .6
    return n * e * .6
def hat(open_=False):
    tt = T(.18 if open_ else .05); return hp(rng.standard_normal(len(tt)), 7000) * np.exp(-tt * (18 if open_ else 90))
def saw_pad(freqs, d):
    tt = T(d); x = np.zeros(len(tt))
    for f in freqs:
        for det in (-0.12, 0.0, 0.11):
            ph = (f * (1 + det / 100) * tt + rng.uniform()) % 1; x += (2 * ph - 1)
    x = lp(x, 1600) / (len(freqs) * 3)
    env = np.minimum(1, tt / .25) * np.minimum(1, (d - tt) / .4)
    return x * env
# Am - F - C - G   (A2 roots), 2 bars each (8 beats = 4s)
prog = [(110.0, [220.0, 261.63, 329.63, 440.0]), (87.31, [174.61, 220.0, 261.63, 349.23]),
        (130.81, [196.0, 261.63, 329.63, 392.0]), (98.0, [196.0, 246.94, 293.66, 392.0])]
nbeats = int(MUSIC_LEN / beat)
for b in range(nbeats):
    t = b * beat
    place(kick(), t, .9)
    if b % 2 == 1: place(clap(), t, .35)
    place(hat(), t + beat / 2, .22)
    if b % 4 == 3: place(hat(True), t + beat / 2, .15)
for i, c in enumerate(range(0, nbeats, 8)):
    root, ch = prog[i % 4]; t = c * beat; d = min(8 * beat, MUSIC_LEN - t)
    if d <= .5: break
    p = saw_pad(ch, d); place(np.stack([p, np.roll(p, int(.017 * SR))], 1), t, .55)
    for k in range(int(d / (beat / 2))):  # offbeat sub bass pluck
        tt = T(beat / 2 * .9); s = np.sin(2 * np.pi * root * tt) * np.exp(-tt * 6)
        place(s, t + k * beat / 2 + beat / 2 * (k % 2 == 0) * 0, .30 if k % 2 else .0)
# sidechain-style pump on the pad/bass
env = np.ones(N)
for b in range(nbeats):
    i = int(b * beat * SR); L = int(beat * SR); tt = np.arange(L) / SR
    env[i:i + L] = (1 - .55 * np.exp(-tt * 9))[:max(0, min(L, N - i))]
mix *= env[:, None] ** 0.6
fade = np.minimum(1, np.arange(N) / (0.6 * SR)) * np.minimum(1, (N - np.arange(N)) / (1.5 * SR))
mix *= fade[:, None]
sf.write(f"{out}/music.wav", norm(mix, -1.0).astype(np.float32), SR, subtype="PCM_24")
print("ok", list(sfx), MUSIC_LEN)
