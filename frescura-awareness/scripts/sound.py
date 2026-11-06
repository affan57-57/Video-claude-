# Synthesised SFX + music bed + final mix for the Frescura awareness video.
# usage: python sound.py voice_final.wav out_mix.wav [stems_dir]
import sys, os, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
DUR = 45.0
N = int(DUR * SR)
rng = np.random.default_rng(11)
T = lambda d: np.arange(int(d * SR)) / SR


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, hi], btype="band", fs=SR, output="sos"), x, axis=0)


def lp(x, f, o=2):
    return sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x, axis=0)


def hp(x, f, o=2):
    return sosfilt(butter(o, f, btype="high", fs=SR, output="sos"), x, axis=0)


def st(x, pan=0.0):
    return np.stack([x * np.sqrt((1 - pan) / 2), x * np.sqrt((1 + pan) / 2)], 1) * 1.41


def norm(x, db=-1.0):
    return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)


_ir = None


def reverb(x, wet=0.3, dec=1.6):
    global _ir
    if _ir is None:
        t = T(dec)
        _ir = np.stack([rng.standard_normal(len(t)) * np.exp(-5 * t / dec) for _ in range(2)], 1)
        _ir = lp(_ir, 7000)
        _ir /= np.sqrt(np.sum(_ir ** 2, 0))
    if x.ndim == 1:
        x = st(x)
    y = np.stack([fftconvolve(x[:, c], _ir[:, c])[: len(x) + len(_ir) - 1] for c in range(2)], 1)
    out = np.zeros_like(y)
    out[: len(x)] += x * (1 - wet)
    return out + y * wet


def bell(f, d, partials=((1, 1), (2.0, 0.4), (3.01, 0.2), (4.2, 0.1)), decay=6):
    t = T(d)
    x = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-decay * m ** 0.5 * t) for m, a in partials)
    return x * np.minimum(1, t / 0.003)


# ---------------- SFX ----------------
def whoosh(d=0.6, lo=250, hi=4200, rev=False):
    n = rng.standard_normal(int(d * SR)); t = T(d); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = lo + (hi - lo) * np.sin(np.pi * p) ** 2
        y[i : i + seg] = bp(n[i : i + seg], fc * 0.55, min(fc * 1.7, 20000))
    env = np.sin(np.pi * t / d) ** 2
    if rev:
        env = (t / d) ** 2.2 * np.exp(-((t / d - 1) ** 2) * 0)
    x = y * env
    L = x * (1 - t / d) + 0.25 * x; R = x * (t / d) + 0.25 * x
    return np.stack([L, R], 1)


def impact(d=1.4, f0=110, f1=38):
    t = T(d)
    f = f1 + (f0 - f1) * np.exp(-t * 9)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    nz = lp(rng.standard_normal(len(t)), 1800) * np.exp(-t * 18) * 0.6
    click = hp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 300) * 0.5
    return reverb(st(sub + nz + click), 0.18)


def riser(d=1.2, f0=200, f1=2400):
    t = T(d); p = t / d
    f = f0 * (f1 / f0) ** (p ** 1.6)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.35 + np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR) * 0.15
    n = rng.standard_normal(len(t)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        fc = f0 * 2 + (8000 - f0 * 2) * (i / len(n)) ** 1.5
        y[i : i + seg] = bp(n[i : i + seg], fc * 0.6, min(fc * 1.6, 20000))
    x = (tone + y * 0.6) * p ** 2.3
    return reverb(st(x), 0.25)


def shimmer(d=1.6, n=26, lo=1800, hi=7000):
    x = np.zeros(int(d * SR) + SR // 2)
    for k in range(n):
        o = int((k / n) ** 1.3 * d * 0.75 * SR); f = rng.uniform(lo, hi)
        b = bell(f, 0.5, partials=((1, 1), (2.01, 0.3)), decay=10); x[o : o + len(b)] += b * rng.uniform(0.4, 1)
    x = hp(x, 1200)
    return reverb(np.stack([x, np.roll(x, int(0.013 * SR))], 1), 0.45, 2.2)


def pop(f0=900, f1=180, d=0.12):
    t = T(d); f = f1 + (f0 - f1) * np.exp(-t * 30)
    return st(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 40))


def bloop(f0=380, f1=1300, d=0.16):
    t = T(d); f = f0 + (f1 - f0) * (t / d) ** 0.7
    return reverb(st(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 1.5), 0.25)


def click(f=2400, d=0.05):
    t = T(d)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 120) + hp(rng.standard_normal(len(t)), 4000) * np.exp(-t * 400) * 0.6
    return st(x)


def clack(f=820):
    t = T(0.25)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 28) + 0.5 * np.sin(2 * np.pi * f * 2.7 * t) * np.exp(-t * 45)
    x += bp(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t * 90) * 0.7
    return reverb(st(x), 0.2)


def scrub(d=1.1):
    t = T(d); n = rng.standard_normal(len(t))
    x = bp(n, 1800, 7500) * (0.55 + 0.45 * np.sin(2 * np.pi * 11 * t) ** 2) * np.sin(np.pi * t / d) ** 0.8
    gr = np.zeros_like(t)
    for k in range(70):
        o = int(rng.uniform(0, d - 0.01) * SR); L = int(0.004 * SR); gr[o : o + L] += rng.standard_normal(L) * rng.uniform(0.3, 1)
    x += hp(gr, 3000) * 0.8
    pan = np.linspace(-0.8, 0.8, len(t))
    return np.stack([x * np.sqrt((1 - pan) / 2), x * np.sqrt((1 + pan) / 2)], 1) * 1.4


def water(d=2.0):
    t = T(d); x = bp(rng.standard_normal(len(t)), 600, 9000) * 0.35
    for k in range(140):
        o = int(rng.uniform(0, d - 0.05) * SR); tt = T(0.03); ff = rng.uniform(600, 1800) + rng.uniform(1000, 2000) * tt / 0.03
        b = np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.sin(np.pi * tt / 0.03)
        x[o : o + len(b)] += b * rng.uniform(0.05, 0.25)
    env = np.minimum(1, t / 0.2) * np.minimum(1, (d - t) / 0.5)
    return reverb(st(x * env), 0.3)


def sweep(f0, f1, d=0.9, amp=1.0):
    t = T(d); f = f0 * (f1 / f0) ** (t / d)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return reverb(st(x * np.sin(np.pi * t / d) ** 0.6 * amp), 0.3)


def tick(hi=True):
    return click(3200 if hi else 2500, 0.04)


def thump(f=58):
    t = T(0.5); x = np.sin(2 * np.pi * f * t) * np.exp(-t * 9) * np.minimum(1, t / 0.004)
    return st(x)


def chord_ding():
    x = np.zeros(int(2.2 * SR))
    for i, f in enumerate([1046.5, 1318.5, 1568.0, 2093.0]):
        b = bell(f, 1.8, decay=3.2); o = int(i * 0.06 * SR); x[o : o + len(b)] += b
    return reverb(st(x), 0.35, 2.0)


def boing():
    t = T(0.35); f = 300 + 500 * np.exp(-t * 14) * (1 + 0.3 * np.sin(2 * np.pi * 18 * t))
    return reverb(st(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 8)), 0.15)


# ---------------- placement ----------------
sfx = np.zeros((N + SR * 3, 2))


def put(x, t, db):
    x = norm(x, db)
    i = int(t * SR)
    if i < 0:
        x = x[-i:]; i = 0
    sfx[i : i + len(x)] += x[: len(sfx) - i]


CUTS = [2.34, 4.34, 6.3, 8.22, 12.54, 13.98, 17.36, 19.54, 21.72, 25.78, 29.26, 30.42, 32.54, 33.72, 34.94, 36.1, 38.9, 40.16]
for k, c in enumerate(CUTS):
    put(whoosh(0.5 + 0.1 * (k % 3), 200 + 80 * (k % 4), 3800 + 600 * (k % 3)), c - 0.3, -9)

# hook
put(impact(1.6, 140, 36), 0.0, -2)
put(whoosh(0.35, 600, 6000), 0.2, -11)
for i in range(9):
    put(click(1800 + i * 160, 0.035), 0.28 + i * 0.035, -20)
put(scrub(0.28), 1.52, -10)
put(pop(1200, 300), 1.75, -9)
put(shimmer(0.9, 10), 1.78, -16)
# egypt
put(shimmer(1.4, 22, 900, 4200), 2.36, -10)
put(bell(1318.5, 1.2, decay=4)[:, None] * np.ones((1, 2)), 3.0, -16)
put(thump(52), 2.36, -8)
# process
put(clack(600), 4.45, -12)
for t_ in (5.9, 6.8, 7.6):
    put(clack(900 + (t_ - 5.9) * 300), t_, -11)
put(sweep(300, 900, 0.5, 0.6), 6.55, -20)
put(sweep(400, 1200, 0.5, 0.6), 7.35, -20)
# minerals
put(riser(0.75, 120, 1600), 8.25, -12)
put(impact(1.0, 120, 45), 9.0, -6)
for t_, f in ((10.12, 700), (10.98, 880), (11.9, 1050)):
    put(clack(f), t_, -7)
    put(shimmer(0.4, 5, 3000, 7000), t_ + 0.05, -20)
# hydration
put(bloop(300, 1100, 0.2), 12.56, -8)
put(sweep(260, 1040, 1.2, 1.0), 12.6, -17)
for i in range(5):
    put(bloop(500 + 120 * i, 1600 + 200 * i, 0.08), 12.75 + i * 0.13, -18)
# scrub
put(impact(0.8, 100, 50), 14.05, -12)
for i in range(3):
    put(pop(700 + i * 150, 250), 14.4 + i * 0.08, -16)
put(scrub(1.1), 15.9, -6)
for i in range(9):
    put(pop(1500 + i * 60, 600, 0.06), 16.12 + i * 0.09, -17)
put(chord_ding()[: int(1.0 * SR)], 16.95, -17)
# routine
put(water(2.2), 17.36, -12)
put(impact(1.0, 110, 42), 20.2, -9)
for i in range(3):
    put(click(2600 + 300 * i, 0.05), 20.7 + i * 0.12, -14)
# reveal
put(riser(1.15, 150, 3000), 21.78, -6)
put(impact(1.8, 150, 34), 22.92, -2)
put(shimmer(2.2, 34, 1500, 7500), 22.95, -7)
put(whoosh(0.9, 1500, 9000), 23.25, -12)
for i in range(16):
    put(bloop(rng.uniform(400, 900), rng.uniform(1300, 2600), 0.07), 24.4 + i * 0.07, -19)
put(pop(1100, 400), 25.08, -9)
# features
for t_ in (25.85, 27.66, 28.4):
    put(whoosh(0.25, 1500, 8000), t_ - 0.08, -13)
    put(click(2200, 0.05), t_ + 0.12, -13)
# two variants
put(impact(1.2, 130, 40), 29.6, -4)
put(whoosh(0.45, 300, 3000), 29.2, -9)
# woman glory / noche
put(thump(56), 30.44, -5); put(thump(56), 30.74, -9)
put(shimmer(1.2, 18, 1200, 5000), 30.62, -13)
put(shimmer(1.8, 20, 700, 3000), 32.56, -10)
put(sweep(180, 90, 1.4, 1.0), 32.56, -15)
# mood
put(click(1800, 0.06), 35.6, -9); put(pop(500, 900, 0.1), 35.62, -12)
# stock
put(impact(1.0, 100, 40), 36.15, -6)
put(sweep(900, 180, 1.0, 1.0), 36.5, -12)
for i in range(3):
    put(bell(880, 0.25, decay=14)[:, None] * np.ones((1, 2)), 37.5 + i * 0.3, -17)
put(sweep(300, 1400, 0.85, 1.0), 37.6, -15)
put(bell(1760, 1.0, decay=5)[:, None] * np.ones((1, 2)), 38.45, -13)
# hurry: clock ticks
for i in range(5):
    put(tick(i % 2 == 0), 38.92 + i * 0.25, -9)
put(impact(0.8, 90, 40), 39.5, -9)
# CTA
put(impact(1.4, 130, 38), 40.16, -4)
for i in range(7):
    put(bloop(300, 600, 0.06), 40.7 + i * 0.6, -24)
put(shimmer(1.4, 22), 41.12, -10)
put(boing(), 42.8, -7)
put(chord_ding(), 42.85, -7)
for t_ in (43.5, 44.1):
    put(click(1600, 0.06), t_, -8); put(pop(800, 300, 0.1), t_ + 0.02, -12)
put(shimmer(1.8, 26, 2000, 8000), 44.2, -13)

# ---------------- music bed (112 BPM) ----------------
BPM = 112; beat = 60 / BPM
mus = np.zeros((N + SR * 3, 2))


def addm(x, t, g=1.0):
    i = int(t * SR); x = x if x.ndim == 2 else st(x)
    mus[i : i + len(x)] += x[: len(mus) - i] * g


def kick():
    t = T(0.38); f = 45 + 110 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5) + hp(rng.standard_normal(len(t)), 4000) * np.exp(-t * 300) * 0.15


def hat(d=0.045):
    t = T(d); return hp(rng.standard_normal(len(t)), 7500) * np.exp(-t * 90)


def clap():
    t = T(0.25); n = bp(rng.standard_normal(len(t)), 900, 5000)
    env = sum(np.exp(-np.maximum(t - o, 0) * 60) * (t >= o) for o in (0, 0.012, 0.024)) * np.exp(-t * 12)
    return n * env


def pad_note(f, d):
    t = T(d); x = np.zeros_like(t)
    for det in (-0.12, 0, 0.13):
        ff = f * 2 ** (det / 12)
        for h in range(1, 7):
            x += np.sin(2 * np.pi * ff * h * t + h) / h ** 1.3
    env = np.minimum(1, t / 0.35) * np.minimum(1, (d - t) / 0.4)
    return x * env


CH = [[57, 60, 64, 67, 71], [53, 57, 60, 64, 67], [48, 55, 59, 64, 67], [55, 59, 62, 64, 69]]  # Am9 Fmaj9 Cmaj7 G6
ROOT = [45, 41, 36, 43]
mf = lambda m: 440 * 2 ** ((m - 69) / 12)
bar = 4 * beat
nbars = int(np.ceil(DUR / bar)) + 1
padbus = np.zeros((N + SR * 3, 2)); bass = np.zeros(N + SR * 3)
for b in range(nbars):
    t0 = b * bar; c = CH[b % 4]
    x = sum(pad_note(mf(m), bar + 0.4) for m in c) / len(c)
    i = int(t0 * SR); padbus[i : i + len(x)] += st(x)[: len(padbus) - i]
    for k, off in enumerate((0, 1.5, 2.5, 3.0)):
        tt = T(beat * 0.9); f = mf(ROOT[b % 4])
        bn = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 3) * np.minimum(1, tt / 0.01)
        j = int((t0 + off * beat) * SR); bass[j : j + len(bn)] += bn[: len(bass) - j] * (1 if k == 0 else 0.7)
padbus = lp(padbus, 2600) * 0.5
padbus = reverb(padbus, 0.35, 2.4)[: len(mus)]
mus += padbus
mus += st(lp(bass, 400)) * 0.55

nb = int(DUR / beat) + 2
kenv = np.ones(len(mus))
for k in range(nb):
    t = k * beat
    build = 21.72 <= t < 22.92
    if t >= 44.2:
        break
    if not build:
        addm(kick(), t, 0.95)
        i = int(t * SR); L = int(0.28 * SR); kenv[i : i + L] = np.minimum(kenv[i : i + L], 1 - 0.55 * np.exp(-np.arange(L) / SR * 9))
    if k % 4 in (1, 3) and not build:
        addm(reverb(st(clap()), 0.3, 1.0), t, 0.35)
    addm(hat(), t + beat / 2, 0.22 if not build else 0.12)
    if 38.9 <= t < 40.16 or t >= 40.16:
        addm(hat(0.03), t + beat / 4, 0.12); addm(hat(0.03), t + 3 * beat / 4, 0.12)
# build: snare roll into drop
for i in range(16):
    t = 21.72 + i * (1.2 / 16)
    addm(clap() * (0.2 + 0.8 * i / 16), t, 0.25)
mus[:, 0] *= kenv; mus[:, 1] *= kenv
# filter sweep during build
i0, i1 = int(21.72 * SR), int(22.92 * SR)
mus[i0:i1] = lp(mus[i0:i1], 900) * 0.7
mus = mus[:N]
fade = np.ones(N); fo = int(44.2 * SR); fade[fo:] = np.linspace(1, 0, N - fo) ** 2
mus *= fade[:, None]

# ---------------- mix ----------------
voice, vsr = sf.read(sys.argv[1], dtype="float32")
assert vsr == SR
if voice.ndim == 2:
    voice = voice.mean(1)
VO = 0.0  # voice offset
v = np.zeros(N); i = int(VO * SR); v[i : i + len(voice)] = voice[: N - i]
# ducking envelope from voice
env = np.abs(v); L = int(0.03 * SR)
env = np.convolve(env, np.ones(L) / L, mode="same")
duck = 1 - 0.55 * np.clip(env / 0.05, 0, 1)
duck = np.convolve(duck, np.ones(int(0.12 * SR)) / int(0.12 * SR), mode="same")
music = norm(mus, -1) * 10 ** (-8.5 / 20) * duck[:, None]
sfx_ = sfx[:N] * 10 ** (-1.5 / 20)
mix = st(v) * 0.707 + music + sfx_
# glue + limit (simple lookahead peak limiter)
peak = np.max(np.abs(mix), 1)
lim = 10 ** (-1.8 / 20)
g = np.minimum(1, lim / (peak + 1e-9))
W = int(0.004 * SR)
from scipy.ndimage import minimum_filter1d, uniform_filter1d
g = minimum_filter1d(g, W * 2 + 1)
g = uniform_filter1d(g, W * 2 + 1)
g = np.minimum(g, minimum_filter1d(np.minimum(1, lim / (peak + 1e-9)), 3))
mix = mix * g[:, None]
mix = np.clip(mix, -lim, lim)
sf.write(sys.argv[2], mix.astype(np.float32), SR, subtype="PCM_24")
if len(sys.argv) > 3:
    os.makedirs(sys.argv[3], exist_ok=True)
    sf.write(sys.argv[3] + "/music.wav", music.astype(np.float32), SR, subtype="PCM_24")
    sf.write(sys.argv[3] + "/sfx.wav", sfx_.astype(np.float32), SR, subtype="PCM_24")
print("ok", mix.shape[0] / SR)
