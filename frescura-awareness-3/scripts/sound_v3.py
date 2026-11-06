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


CUTS = [9.2, 12.88, 25.54, 27.82, 30.0, 33.26]
for k, c in enumerate(CUTS):
    put(whoosh(0.5 + 0.1 * (k % 3), 220 + 70 * (k % 4), 4200 + 500 * (k % 3)), c - 0.3, -9)
IRIS = [5.04, 18.46, 21.88, 37.4, 41.2]
for c in IRIS:
    put(whoosh(0.45, 120, 1800), c - 0.36, -8)
    put(impact(0.9, 100, 40), c, -9)
# HOOK
put(impact(1.6, 140, 34), 0.0, -3)
put(shimmer(1.2, 18, 900, 4000), 0.05, -12)
for i in range(10):
    put(click(1500 + 140 * i, 0.03), 0.42 + i * 0.03, -18)
put(whoosh(0.4, 500, 6000), 2.1, -10)
put(riser(0.55, 200, 2400), 2.2, -11)
put(impact(1.4, 150, 36), 2.72, -2)
for i in range(3):
    put(pop(900 + 200 * i, 400), 2.8 + i * 0.1, -10)
put(shimmer(1.0, 12), 3.18, -15)
put(pop(1200, 500), 3.9, -12)
# 01 OIL
for i in range(8):
    put(bloop(300 + 30 * i, 700 + 60 * i, 0.08), 5.84 + i * 0.06, -16)
for i in range(14):
    put(click(2600 + 80 * (i % 5), 0.02), 7.0 + i * 0.03 + 0.4, -20)
put(sweep(900, 300, 0.8, 1.0), 7.5, -14)
put(chord_ding()[: int(0.8 * SR)], 7.9, -14)
# 02 CALM
put(sweep(160, 700, 0.5, 1.0), 11.0, -16)
put(scrub(0.5), 11.74, -10)
put(sweep(700, 400, 0.6, 1.0), 12.25, -15)
put(shimmer(0.9, 12, 1200, 4500), 12.3, -13)
# 03 SOAK
put(water(1.6), 13.5, -13)
put(sweep(300, 500, 1.0, 0.8), 14.8, -20)
for i in range(16):
    put(bloop(rng.uniform(600, 1200), rng.uniform(1600, 3200), 0.05), 15.85 + i * 0.03, -18)
put(whoosh(0.3, 800, 6000), 16.2, -12)
put(scrub(0.5), 16.5, -12)
put(click(1800, 0.06), 16.9, -10)
put(shimmer(0.8, 10, 1500, 4500), 17.1, -14)
# RITUAL
for i in range(3):
    put(pop(800 + 150 * i, 300), 18.5 + i * 0.12, -11)
put(whoosh(0.3, 1000, 7000), 19.25, -12)
put(riser(0.9, 150, 2000), 20.3, -12)
put(impact(1.3, 140, 36), 21.2, -4)
# PRODUCT
put(water(1.4), 22.3, -18)
put(sweep(200, 700, 0.6, 1.0), 22.3, -14)
put(riser(1.0, 150, 3200), 23.5, -9)
put(impact(1.8, 150, 34), 24.5, -2)
put(shimmer(2.0, 30, 1500, 7500), 24.5, -8)
put(click(700, 0.08), 25.6, -10)
put(water(1.8), 25.6, -14)
for t_ in (26.2, 26.9):
    put(whoosh(0.25, 1500, 8000), t_ - 0.08, -12); put(click(2300, 0.05), t_ + 0.1, -11)
# CLEAN
put(scrub(1.4), 27.9, -12)
put(scrub(0.3), 29.45, -8)
put(clack(500), 29.5, -11)
# VARIANTS
put(thump(56), 30.02, -5); put(thump(56), 30.32, -9)
put(shimmer(1.2, 16, 1200, 5000), 30.4, -13)
put(pop(700, 1200, 0.1), 32.2, -11); put(pop(800, 1300, 0.1), 32.74, -11)
put(shimmer(2.0, 24, 700, 3200), 33.3, -10)
put(sweep(180, 90, 1.6, 1.0), 33.3, -15)
put(pop(600, 1000, 0.1), 36.28, -11); put(pop(700, 1100, 0.1), 36.82, -11)
# STOCK
put(impact(1.0, 100, 40), 37.45, -5)
put(whoosh(0.4, 300, 4000), 37.45, -10); put(whoosh(0.4, 300, 4000), 37.55, -10)
for i in range(6):
    put(bell(880, 0.2, decay=14)[:, None] * np.ones((1, 2)), 38.0 + i * 0.4, -18)
for i in range(3):
    put(pop(500 + 120 * i, 900, 0.08), 39.3 + i * 0.1, -12)
put(boing(), 39.5, -10)
put(whoosh(0.5, 400, 5000), 40.3, -11)
# CTA
put(whoosh(0.35, 1500, 8000), 41.84, -12)
put(boing(), 42.45, -6)
put(chord_ding(), 42.5, -7)
for t_ in (42.95, 43.7, 44.4):
    put(click(1600, 0.05), t_, -11)
put(pop(900, 400), 43.26, -9)
put(shimmer(1.6, 24, 2000, 8000), 43.3, -12)

# ---------------- music bed (112 BPM) ----------------
BPM = 122; beat = 60 / BPM
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


CH = [[53, 56, 60, 63, 67], [49, 56, 60, 63, 65], [44, 51, 55, 60, 63], [51, 55, 58, 63, 65]]  # Fm9 Dbmaj9 Abmaj7 Eb
ROOT = [41, 37, 44, 39]
mf = lambda m: 440 * 2 ** ((m - 69) / 12)
bar = 4 * beat
nbars = int(np.ceil(DUR / bar)) + 1
padbus = np.zeros((N + SR * 3, 2)); bass = np.zeros(N + SR * 3)
for b in range(nbars):
    t0 = b * bar; c = CH[b % 4]
    x = sum(pad_note(mf(m), bar + 0.4) for m in c) / len(c)
    i = int(t0 * SR)
    if i >= len(padbus): continue
    padbus[i : i + len(x)] += st(x)[: len(padbus) - i]
    for k, off in enumerate((0, 1.5, 2.5, 3.0)):
        tt = T(beat * 0.9); f = mf(ROOT[b % 4])
        bn = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 3) * np.minimum(1, tt / 0.01)
        j = int((t0 + off * beat) * SR)
        if j >= len(bass): continue
        bass[j : j + len(bn)] += bn[: len(bass) - j] * (1 if k == 0 else 0.7)
padbus = lp(padbus, 2600) * 0.5
padbus = reverb(padbus, 0.35, 2.4)[: len(mus)]
mus += padbus
mus += st(lp(bass, 400)) * 0.55

nb = int(DUR / beat) + 2
kenv = np.ones(len(mus))
for k in range(nb):
    t = k * beat
    build = 23.5 <= t < 24.5
    if t >= 44.2:
        break
    if not build:
        addm(kick(), t, 0.95)
        i = int(t * SR); L = int(0.28 * SR); kenv[i : i + L] = np.minimum(kenv[i : i + L], 1 - 0.55 * np.exp(-np.arange(L) / SR * 9))
    if k % 4 in (1, 3) and not build:
        addm(reverb(st(clap()), 0.3, 1.0), t, 0.35)
    addm(hat(), t + beat / 2, 0.22 if not build else 0.12)
    if t >= 37.4:
        addm(hat(0.03), t + beat / 4, 0.12); addm(hat(0.03), t + 3 * beat / 4, 0.12)
# build: snare roll into drop
for i in range(16):
    t = 23.5 + i * (1.0 / 16)
    addm(clap() * (0.2 + 0.8 * i / 16), t, 0.25)
mus[:, 0] *= kenv; mus[:, 1] *= kenv
# filter sweep during build
i0, i1 = int(23.5 * SR), int(24.5 * SR)
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
music = norm(mus, -1) * 10 ** (-10.5 / 20) * duck[:, None]
sfx_ = sfx[:N] * 10 ** (-2.5 / 20)
mix = (st(v) * 1.0 + music + sfx_) * 10 ** (float(os.environ.get("GAIN", "0")) / 20)
# glue + limit (simple lookahead peak limiter)
peak = np.max(np.abs(mix), 1)
lim = 10 ** (-2.3 / 20)
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
