"""Frescura Body ad: synthesize SFX + luxury deep-house bed, place SFX on transcript cues, mix with voice.
Usage: python frescura_audio.py voice.wav out_mix.wav
"""
import sys
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
rng = np.random.default_rng(11)
VOICE, OUT = sys.argv[1], sys.argv[2]
TOTAL = 39.5


def t(d):
    return np.arange(int(d * SR)) / SR


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, hi], btype="band", fs=SR, output="sos"), x)


def lp(x, f, o=2):
    return sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x)


def hp(x, f, o=2):
    return sosfilt(butter(o, f, btype="high", fs=SR, output="sos"), x)


def norm(x, db=-1.0):
    return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)


def bell(f, d, partials=((1, 1), (2.0, 0.35), (3.01, 0.18), (4.2, 0.08)), decay=6):
    tt = t(d)
    x = sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-decay * m ** 0.5 * tt) for m, a in partials)
    return x * np.minimum(1, tt / 0.002)


# ---------------- SFX (mono, later panned) ----------------
def whoosh(d=0.55, lo=250, hi=5000):
    n = rng.standard_normal(int(d * SR))
    y = np.zeros_like(n)
    seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n)
        fc = lo + (hi - lo) * np.sin(np.pi * p) ** 2
        y[i:i + seg] = bp(n[i:i + seg], fc * 0.6, min(fc * 1.7, 20000))
    return y * np.sin(np.pi * t(d) / d) ** 2


def riser(d=0.9):
    tt = t(d)
    n = hp(rng.standard_normal(len(tt)), 1500)
    f = 200 * (2 ** (tt / d * 3))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    return (n * 0.6 + tone) * (tt / d) ** 2.2


def impact(d=1.6):
    tt = t(d)
    f = 30 + 90 * np.exp(-tt * 18)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 3.2)
    crack = lp(rng.standard_normal(len(tt)), 3500) * np.exp(-tt * 28) * 0.7
    tail = lp(rng.standard_normal(len(tt)), 900) * np.exp(-tt * 4) * 0.12
    return np.tanh(1.6 * (sub + crack + tail))


def pop():
    tt = t(0.13)
    f = 1100 * np.exp(-tt * 35) + 220
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 38)


def click():
    tt = t(0.05)
    return hp(rng.standard_normal(len(tt)), 2500) * np.exp(-tt * 160) + 0.6 * np.sin(2 * np.pi * 1800 * tt) * np.exp(-tt * 90)


def tick():
    tt = t(0.06)
    return np.sin(2 * np.pi * 3200 * tt) * np.exp(-tt * 140) + 0.4 * hp(rng.standard_normal(len(tt)), 5000) * np.exp(-tt * 300)


def tock():
    tt = t(0.07)
    return np.sin(2 * np.pi * 2100 * tt) * np.exp(-tt * 120)


def shimmer(d=1.4, n=22):
    x = np.zeros(int((d + 0.5) * SR))
    for k in range(n):
        o = int((k / n) * d * 0.85 * SR + rng.uniform(0, 0.03) * SR)
        f = rng.uniform(2600, 7200)
        b = bell(f, 0.4, partials=((1, 1), (2.01, 0.3)), decay=12)
        x[o:o + len(b)] += b * rng.uniform(0.4, 1) * (1 - 0.5 * k / n)
    return hp(x, 1800)


def bubble(n=7, d=0.6):
    x = np.zeros(int((d + 0.2) * SR))
    for k in range(n):
        o = int(rng.uniform(0, d) * SR)
        tt = t(0.07)
        f0 = rng.uniform(500, 1400)
        f = f0 * (1 + tt * 18)
        b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 55)
        x[o:o + len(b)] += b * rng.uniform(0.4, 1)
    return x


def chime():
    x = np.zeros(int(1.3 * SR))
    for i, f in enumerate([1567.98, 2093.0]):
        b = bell(f, 1.1, decay=5)
        o = int(i * 0.09 * SR)
        x[o:o + len(b)] += b
    return x


def kaching():
    x = np.zeros(int(1.4 * SR))
    c = click()
    x[:len(c)] += c
    for i, f in enumerate([2637, 3520, 4186]):
        b = bell(f, 1.0, decay=6)
        o = int((0.06 + i * 0.05) * SR)
        x[o:o + len(b)] += b * 0.7
    return x


def thud():
    tt = t(0.35)
    f = 70 + 120 * np.exp(-tt * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 14)


def glitch():
    tt = t(0.18)
    sq = np.sign(np.sin(2 * np.pi * 420 * tt)) * (np.floor(tt * 60) % 2)
    return lp(sq, 4000) * np.exp(-tt * 9) * 0.5


def beep():
    tt = t(0.16)
    return np.sin(2 * np.pi * 1320 * tt) * np.minimum(1, (0.16 - tt) / 0.03) * np.minimum(1, tt / 0.005)


S = {k: f() for k, f in dict(whoosh=whoosh, riser=riser, impact=impact, pop=pop, click=click, tick=tick, tock=tock,
                             shimmer=shimmer, bubble=bubble, chime=chime, kaching=kaching, thud=thud, glitch=glitch,
                             beep=beep).items()}
S["swish"] = whoosh(0.32, 900, 9000)

# (time, sfx, gain dB, pan)  -- time on the edited voice timeline (seconds)
CUES = [
    (0.00, "impact", -6, 0), (0.00, "whoosh", -10, -0.3), (0.55, "shimmer", -14, 0.3),
    (1.00, "pop", -10, -0.4), (1.80, "pop", -10, 0.4), (3.85, "pop", -9, 0), (3.90, "chime", -16, 0),
    (4.45, "swish", -11, 0.3), (4.95, "glitch", -15, -0.2), (5.25, "glitch", -15, 0.2),
    (5.75, "whoosh", -11, 0),
    (5.95, "riser", -13, 0), (6.68, "impact", -7, 0), (6.70, "shimmer", -12, 0),
    (7.65, "swish", -11, -0.3), (8.05, "bubble", -13, 0.2),
    (9.40, "click", -10, -0.3), (9.95, "pop", -12, 0), (10.22, "click", -10, 0.3),
    (10.75, "whoosh", -11, 0), (11.55, "shimmer", -15, -0.2),
    (12.30, "tick", -12, -0.4), (12.75, "tick", -12, 0), (13.20, "tick", -12, 0.4),
    (14.70, "swish", -11, 0), (15.05, "shimmer", -13, 0.3), (16.10, "bubble", -14, -0.2),
    (17.30, "chime", -16, 0),
    (18.00, "whoosh", -11, 0),
    *[(18.80 + i * 0.17, "tick", -14, -0.6 + i * 0.2) for i in range(7)],
    (20.95, "thud", -8, 0), (21.05, "glitch", -16, 0),
    (21.45, "riser", -13, 0), (22.40, "impact", -8, -0.15), (22.45, "shimmer", -15, -0.3),
    (24.36, "impact", -8, 0.15), (24.40, "shimmer", -15, 0.3),
    (26.90, "swish", -11, 0), (27.15, "beep", -17, 0), (27.70, "beep", -17, 0), (28.20, "beep", -15, 0),
    *[(28.70 + i * 0.5, "tick" if i % 2 == 0 else "tock", -14, 0) for i in range(6)],
    (31.45, "whoosh", -10, 0), (31.95, "pop", -8, 0), (33.05, "click", -8, 0), (33.20, "kaching", -11, 0),
    (35.45, "shimmer", -15, 0), (37.20, "riser", -14, 0), (37.95, "impact", -7, 0), (38.00, "shimmer", -12, 0),
]


# ---------------- Music bed: 118 BPM dark-luxe deep house ----------------
def music():
    bpm = 118.0
    beat = 60 / bpm
    n = int(TOTAL * SR)
    L = np.zeros(n)
    R = np.zeros(n)

    def add(sig, at, g=1.0, pan=0.0):
        o = int(at * SR)
        if o >= n:
            return
        s = sig[: n - o] * g
        L[o:o + len(s)] += s * np.sqrt((1 - pan) / 2)
        R[o:o + len(s)] += s * np.sqrt((1 + pan) / 2)

    tt = t(0.45)
    kick = np.sin(2 * np.pi * np.cumsum(45 + 110 * np.exp(-tt * 28)) / SR) * np.exp(-tt * 7)
    kick = np.tanh(kick * 1.8)
    th = t(0.09)
    hat = hp(rng.standard_normal(len(th)), 7000) * np.exp(-th * 55)
    ts = t(0.25)
    clap = bp(rng.standard_normal(len(ts)), 900, 5000) * (np.exp(-ts * 25) + 0.4 * np.exp(-((ts - 0.012) ** 2) / 1e-5))
    # chords (Am9, Fmaj7, Cmaj7, Em7) as soft Rhodes-like pads
    chords = [[220.0, 261.63, 329.63, 392.0, 493.88], [174.61, 220.0, 261.63, 329.63, 392.0],
              [130.81, 196.0, 246.94, 329.63, 392.0], [164.81, 196.0, 246.94, 293.66, 392.0]]
    bass = [55.0, 43.65, 65.41, 41.2]
    bar = 4 * beat
    nb = int(TOTAL / bar) + 1
    for b in range(nb):
        t0 = b * bar
        ch = chords[b % 4]
        td = t(bar + 0.6)
        pad = sum(np.sin(2 * np.pi * f * td + 0.3 * np.sin(2 * np.pi * 4.5 * td)) * (0.6 if i else 1) for i, f in enumerate(ch))
        pad *= np.minimum(1, td / 0.25) * np.exp(-td * 0.55)
        add(lp(pad, 2400), t0, 0.05, 0)
        # sub bass offbeat pumps
        for k in range(4):
            tb = t(beat * 0.45)
            bs = np.sin(2 * np.pi * bass[b % 4] * 2 * tb) * np.minimum(1, tb / 0.01) * np.exp(-tb * 5)
            add(np.tanh(bs * 1.5), t0 + k * beat + beat / 2, 0.22, 0)
        for k in range(4):
            tk = t0 + k * beat
            if tk < 0.0 or tk > TOTAL - 1.3:
                continue
            add(kick, tk, 0.55)
            add(hat, tk + beat / 2, 0.11, 0.3)
            add(hat, tk + beat * 0.75, 0.05, -0.3)
            if k in (1, 3):
                add(clap, tk, 0.12, 0)
        # pluck arp
        for k in range(8):
            f = ch[(k * 3) % len(ch)] * 2
            tp = t(0.3)
            pl = np.sin(2 * np.pi * f * tp) * np.exp(-tp * 14)
            add(pl, t0 + k * beat / 2, 0.035, -0.5 + (k % 4) * 0.33)
    m = np.stack([L, R], 1)
    tt = np.arange(n) / SR
    env = np.minimum(1, tt / 0.15) * np.clip((TOTAL - tt) / 1.6, 0, 1)
    return m * env[:, None]


v, sr = sf.read(VOICE, dtype="float64")
assert sr == SR, sr
if v.ndim > 1:
    v = v.mean(1)
n = int(TOTAL * SR)
voice = np.zeros(n)
voice[: min(n, len(v))] = v[:n]

mus = music()
# sidechain duck music under voice (smoothed envelope)
env = np.abs(voice)
win = int(0.12 * SR)
env = np.convolve(env, np.ones(win) / win, mode="same")
duck = 1 - 0.55 * np.clip(env / (np.percentile(env, 90) + 1e-9), 0, 1)
mus = norm(mus, -1) * 10 ** (-17 / 20) * duck[:, None]

fx = np.zeros((n, 2))
for at, name, db, pan in CUES:
    s = norm(S[name], -1) * 10 ** (db / 20)
    o = int(at * SR)
    s = s[: n - o]
    fx[o:o + len(s), 0] += s * np.sqrt((1 - pan) / 2) * 1.41
    fx[o:o + len(s), 1] += s * np.sqrt((1 + pan) / 2) * 1.41

mix = voice[:, None] * np.array([1.0, 1.0]) + mus + fx
sf.write(OUT, mix.astype(np.float32), SR, subtype="FLOAT")
print("wrote", OUT, mix.shape[0] / SR, "s")
