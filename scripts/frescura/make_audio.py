"""Synthesise SFX + a minimal deep-house music bed and mix them under the voice.

Usage: python make_audio.py <voice.wav> <out_mix.wav> [sfx_dir]
Cue times below are film seconds and match the GSAP timeline in frescura-awareness/index.html.
"""
import os, subprocess, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

VOICE, OUT = sys.argv[1], sys.argv[2]
SFX_DIR = sys.argv[3] if len(sys.argv) > 3 else None
SR = 48000
rng = np.random.default_rng(11)


def t(d): return np.arange(int(d * SR)) / SR
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype="band", fs=SR, output="sos"), x, axis=0)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x, axis=0)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype="high", fs=SR, output="sos"), x, axis=0)
def norm(x, db=-1.0): return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)
def st(x, w=0.0):
    if x.ndim == 2: return x
    d = int(0.009 * SR)
    r = np.concatenate([np.zeros(d), x])[:len(x)]
    return np.stack([x, x * (1 - w) + r * w], 1)


IR = (rng.standard_normal((int(1.4 * SR), 2)) * np.exp(-t(1.4) * 4.2)[:, None])
IR = lp(hp(IR, 300), 7000)
IR /= np.sqrt((IR ** 2).sum(0))


def verb(x, wet=0.22):
    x = st(x)
    y = np.stack([fftconvolve(x[:, c], IR[:, c])[:len(x) + len(IR) - 1] for c in range(2)], 1)
    out = np.zeros_like(y); out[:len(x)] += x
    return out + wet * y


def bell(f, d, partials=((1, 1), (2.0, .35), (3.01, .18), (4.2, .08)), decay=6):
    tt = t(d)
    x = sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-decay * m ** .5 * tt) for m, a in partials)
    return x * np.minimum(1, tt / 0.002)


# ---------- SFX ----------
def impact():
    tt = t(1.6)
    f = 32 + 70 * np.exp(-tt * 9)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.6)
    n = lp(rng.standard_normal(len(tt)), 1800) * np.exp(-tt * 18)
    click = hp(rng.standard_normal(len(tt)), 2500) * np.exp(-tt * 160)
    return verb(norm(sub, -1) + 0.5 * norm(n, -1) + 0.35 * norm(click, -1), 0.3)


def whoosh(d=0.55, lo=300, hi=4200):
    n = rng.standard_normal(int(d * SR)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = lo + (hi - lo) * np.sin(np.pi * p) ** 2
        y[i:i + seg] = bp(n[i:i + seg], fc * 0.55, min(fc * 1.7, 20000))
    tt = t(d); env = np.sin(np.pi * tt / d) ** 2.2
    x = y * env
    return verb(np.stack([x * (1.2 - tt / d), x * (0.2 + tt / d)], 1), 0.15)


def riser(d=1.1):
    tt = t(d); p = tt / d
    n = rng.standard_normal(len(tt)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        fc = 400 + 6000 * (i / len(n)) ** 2; y[i:i + seg] = bp(n[i:i + seg], fc * .7, min(fc * 1.4, 20000))
    tone = np.sin(2 * np.pi * np.cumsum(180 + 900 * p ** 2) / SR)
    x = (0.8 * norm(y) + 0.35 * tone) * p ** 2.2
    return verb(x, 0.25)


def tick():
    tt = t(0.09)
    x = np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 90) + 0.6 * hp(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 400)
    return verb(x, 0.12)


def pop():
    tt = t(0.16); f = 1100 * np.exp(-tt * 28) + 220
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 34)
    return verb(x, 0.12)


def bubbles(n=7, d=0.9):
    x = np.zeros(int(d * SR) + SR // 4)
    for k in range(n):
        o = int((k / n * d * 0.85 + rng.uniform(0, .05)) * SR); dd = t(0.05)
        f0 = rng.uniform(500, 1200); f = f0 * (1 + 2.2 * dd / 0.05)
        b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-dd * 70) * rng.uniform(.5, 1)
        x[o:o + len(b)] += b
    return verb(x, 0.2)


def sparkle(d=1.0, n=16):
    x = np.zeros(int(d * SR) + SR // 2)
    for k in range(n):
        o = int(rng.uniform(0, d * 0.8) * SR); f = rng.uniform(2600, 6500)
        b = bell(f, 0.35, partials=((1, 1), (2.01, .3)), decay=14); x[o:o + len(b)] += b * rng.uniform(.4, 1)
    return verb(hp(x, 1500), 0.35)


def shutter():
    x = np.zeros(int(0.25 * SR))
    for o, a in ((0, 1), (0.055, .7)):
        tt = t(0.03); c = bp(rng.standard_normal(len(tt)), 1800, 7000) * np.exp(-tt * 220)
        i = int(o * SR); x[i:i + len(c)] += a * c
    return verb(x, 0.1)


def ding():
    return verb(bell(1568, 1.4, decay=4) + 0.45 * bell(2349.3, 1.4, decay=5), 0.35)


def stamp():
    tt = t(0.5)
    thump = np.sin(2 * np.pi * np.cumsum(70 + 120 * np.exp(-tt * 40)) / SR) * np.exp(-tt * 9)
    slap = bp(rng.standard_normal(len(tt)), 400, 3500) * np.exp(-tt * 45)
    return verb(norm(thump) + 0.7 * norm(slap), 0.2)


def success():
    x = np.zeros(int(1.8 * SR))
    for i, f in enumerate([1046.5, 1318.5, 1568.0, 2093.0]):
        b = bell(f, 1.4, decay=3.8); o = int(i * 0.065 * SR); x[o:o + len(b)] += b
    return verb(x, 0.35)


def drop():  # bass drop for the cut into the testimonial
    tt = t(1.2)
    x = np.sin(2 * np.pi * np.cumsum(120 * np.exp(-tt * 3) + 38) / SR) * np.exp(-tt * 2.2)
    return verb(x, 0.2)


SFX = dict(impact=impact(), whoosh=whoosh(), swish=whoosh(0.32, 900, 6500), riser=riser(), tick=tick(),
           pop=pop(), bubbles=bubbles(), sparkle=sparkle(), shutter=shutter(), ding=ding(), stamp=stamp(),
           success=success(), drop=drop())
SFX = {k: norm(st(v), -1.0) for k, v in SFX.items()}
if SFX_DIR:
    os.makedirs(SFX_DIR, exist_ok=True)
    for k, v in SFX.items(): sf.write(f"{SFX_DIR}/{k}.wav", v.astype(np.float32), SR)

# (time, name, gain dB) — loud on purpose (client asked for strong SFX), voice stays on top
CUES = [
    (0.00, "impact", -3), (0.05, "sparkle", -14), (0.50, "tick", -9), (1.22, "tick", -9),
    (1.80, "whoosh", -6), (2.92, "sparkle", -8), (2.95, "pop", -8),
    (3.62, "swish", -7), (3.70, "shutter", -6), (4.80, "pop", -6), (5.55, "tick", -9),
    (6.80, "swish", -8), (6.95, "riser", -7), (8.05, "drop", -4), (8.10, "impact", -9),
    (13.50, "sparkle", -8), (13.52, "pop", -9),
    (15.80, "whoosh", -8), (15.95, "bubbles", -7), (16.6, "tick", -10),
    (19.70, "whoosh", -8), (20.00, "tick", -9), (20.25, "tick", -9), (20.50, "tick", -9), (21.0, "sparkle", -10),
    (22.30, "swish", -9), (23.68, "stamp", -4),
    (25.30, "shutter", -5), (25.40, "whoosh", -6), (25.75, "shutter", -8), (26.05, "shutter", -8),
    (26.70, "swish", -8), (27.95, "impact", -8), (28.30, "ding", -6),
    (29.30, "whoosh", -7), (30.45, "sparkle", -9), (31.20, "pop", -9),
    (32.35, "swish", -7), (32.62, "pop", -4), (33.05, "tick", -5), (33.10, "bubbles", -10),
    (33.70, "success", -5), (34.80, "whoosh", -8), (35.00, "sparkle", -8),
]

# ---------- music bed: 118 BPM minimal deep house in A minor ----------
voice, sr = sf.read(VOICE, dtype="float32"); assert sr == SR
N = len(voice); dur = N / SR
BPM = 118; beat = 60 / BPM; bar = 4 * beat
mus = np.zeros((N + SR * 2, 2))


def add(buf, x, at, g=1.0):
    i = int(at * SR); x = st(x)
    if i >= len(buf): return
    n = min(len(x), len(buf) - i); buf[i:i + n] += g * x[:n]


def kick():
    tt = t(0.45); f = 48 + 110 * np.exp(-tt * 32)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7) + 0.15 * hp(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 300)


def hat(open_=False):
    tt = t(0.25 if open_ else 0.06)
    return hp(rng.standard_normal(len(tt)), 7500) * np.exp(-tt * (18 if open_ else 90))


def clap():
    tt = t(0.3); x = np.zeros(len(tt))
    for o in (0, 0.011, 0.022):
        i = int(o * SR); L = len(tt) - i; n = bp(rng.standard_normal(L), 900, 5000) * np.exp(-np.arange(L) / SR * 28); x[i:] += n
    return x


def keys(freqs, d):
    tt = t(d); x = np.zeros(len(tt))
    for f in freqs:
        mod = np.sin(2 * np.pi * f * 2 * tt) * 0.8 * np.exp(-tt * 3)
        x += np.sin(2 * np.pi * f * tt + mod)
    env = np.minimum(1, tt / 0.01) * np.exp(-tt * 2.8)
    return lp(x * env * (1 + 0.15 * np.sin(2 * np.pi * 5 * tt)), 3500)


def sub(f, d):
    tt = t(d); env = np.minimum(1, tt / 0.02) * np.minimum(1, (d - tt) / 0.05).clip(0)
    return np.sin(2 * np.pi * f * tt) * env


m2f = lambda m: 440 * 2 ** ((m - 69) / 12)
CH = [([57, 60, 64, 67, 71], 45), ([53, 57, 60, 64], 41), ([48, 52, 55, 59], 48), ([55, 59, 62, 64], 43)]
K, H, HO, C = kick(), hat(), hat(True), clap()
# arrangement: full groove except a breakdown (riser) before the testimonial and a filtered intro hit
nbars = int(dur / bar) + 2
for b in range(nbars):
    t0 = b * bar
    chord, root = CH[b % 4]
    breakdown = 6.6 <= t0 + bar and t0 < 8.1
    for q in range(4):
        tq = t0 + q * beat
        if 6.75 <= tq < 8.1: continue
        add(mus, K, tq, 0.9)
        add(mus, H if q % 2 == 0 else HO, tq + beat / 2, 0.16)
        if q in (1, 3): add(mus, C, tq, 0.28)
        for s in (0, 0.75):
            add(mus, sub(m2f(root - 12), beat * 0.45), tq + s * beat, 0.32)
    for hit in (0, 1.5 * beat, 2.5 * beat):
        if not (6.75 <= t0 + hit < 8.1):
            add(mus, keys([m2f(m) for m in chord], beat * 1.2), t0 + hit, 0.11)
mus = mus[:N]
mus = norm(mus, -6)
fade = np.ones(N); fo = int(1.6 * SR); fade[-fo:] = np.linspace(1, 0, fo)
mus *= fade[:, None]
sf.write("/tmp/_mus.wav", mus.astype(np.float32), SR, subtype="FLOAT")

sfx = np.zeros((N + SR * 3, 2))
for at, name, g in CUES:
    add(sfx, SFX[name], at, 10 ** (g / 20))
sfx = sfx[:N]
sf.write("/tmp/_sfx.wav", sfx.astype(np.float32), SR, subtype="FLOAT")

# music ducked under voice (sidechain), voice on top, glue + limiter, final -12 LUFS / -1 dBTP
fc = ("[1:a]volume=-17dB[m];[0:a]asplit=2[v][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=320[md];"
      "[2:a]volume=-2dB[s];[v][md][s]amix=inputs=3:normalize=0:duration=first,"
      "acompressor=threshold=-14dB:ratio=2:attack=10:release=150:makeup=1dB,"
      "loudnorm=I=-12:TP=-1.0:LRA=8,alimiter=limit=0.89:attack=3:release=60:level=false,aresample=48000")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VOICE, "-i", "/tmp/_mus.wav", "-i", "/tmp/_sfx.wav",
                "-filter_complex", fc, "-c:a", "pcm_s24le", OUT], check=True)
print("wrote", OUT, round(dur, 2), "s")
