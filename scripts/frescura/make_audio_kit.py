"""Synthesised SFX + a 120 BPM minimal-luxury music bed for the Frescura ad.
Usage: python make_audio_kit.py OUT_DIR [music_seconds]"""
import sys, os, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
MUS_LEN = float(sys.argv[2]) if len(sys.argv) > 2 else 36.0
rng = np.random.default_rng(11)
T = lambda d: np.arange(int(d * SR)) / SR


def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype="band", fs=SR, output="sos"), x, axis=0)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x, axis=0)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype="high", fs=SR, output="sos"), x, axis=0)
def norm(x, db=-1.0): return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)
def st(x, w=0.0):
    if x.ndim == 2: return x
    d = int(0.009 * SR * w); r = np.concatenate([np.zeros(d), x])[: len(x)] if d else x
    return np.stack([x, r], 1)


def verb(x, mix=0.25, dec=1.6):
    """Cheap stereo reverb: exponentially decaying filtered noise IR."""
    n = int(dec * SR); tt = np.arange(n) / SR
    out = []
    for ch in range(2):
        ir = rng.standard_normal(n) * np.exp(-tt * 6.9 / dec); ir = lp(ir, 6000); ir /= np.sqrt(np.sum(ir ** 2))
        src = x[:, ch] if x.ndim == 2 else x
        out.append(fftconvolve(src, ir)[: len(src) + n])
    wet = np.stack(out, 1)
    L = min(len(wet), len(x) + n); wet = np.pad(wet, ((0, len(x) + n - len(wet)), (0, 0)))
    dry = st(x) if x.ndim == 1 else x
    dry = np.concatenate([dry, np.zeros((n, 2))])
    return dry * (1 - mix) + wet * mix


def bell(f, d, partials=((1, 1), (2.0, .35), (3.01, .15), (4.2, .07)), decay=6):
    tt = T(d); x = sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-decay * m ** .5 * tt) for m, a in partials)
    return x * np.minimum(1, tt / 0.002)


# ---------------- SFX ----------------
def impact():  # cinematic sub boom + click transient
    tt = T(2.2); f = 110 * np.exp(-tt * 9) + 38
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.2)
    n = hp(rng.standard_normal(len(tt)), 2000) * np.exp(-tt * 60) * 0.5
    body = lp(rng.standard_normal(len(tt)), 400) * np.exp(-tt * 8) * 1.2
    return verb(st(sub * 1.0 + n + body), 0.18, 2.0)


def riser(d=1.6):
    tt = T(d); n = rng.standard_normal(len(tt)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = 300 + 7000 * p ** 2
        y[i:i + seg] = bp(n[i:i + seg], fc * .7, min(fc * 1.4, 20000))
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * (tt / d) ** 2) / SR) * 0.25
    env = (tt / d) ** 2.2
    return verb(st((y + tone) * env, 1), 0.3, 1.2)


def whoosh(d=0.55, up=True):
    tt = T(d); n = rng.standard_normal(len(tt)); y = np.zeros_like(n); seg = 256
    for i in range(0, len(n), seg):
        p = i / len(n); p = p if up else 1 - p
        fc = 500 + 5000 * np.sin(np.pi * p / 2) ** 2
        y[i:i + seg] = bp(n[i:i + seg], fc * .6, min(fc * 1.7, 20000))
    env = np.sin(np.pi * tt / d) ** 3
    x = y * env; L = x * (1 - tt / d * .7); R = x * (.3 + tt / d * .7)
    return np.stack([L, R], 1)


def swish():  # short airy text swipe
    return whoosh(0.28)


def shimmer(d=1.4, n=22):
    x = np.zeros(int((d + .6) * SR))
    for k in range(n):
        o = int((k / n) ** 1.3 * d * .8 * SR); f = 2200 * 2 ** (rng.integers(0, 14) / 7)
        b = bell(f, .5, partials=((1, 1), (2.01, .3)), decay=10); x[o:o + len(b)] += b * rng.uniform(.4, 1)
    return verb(st(hp(x, 1800), 1), 0.4, 1.8)


def tick():
    tt = T(0.05); x = np.sin(2 * np.pi * 2600 * tt) * np.exp(-tt * 180) + hp(rng.standard_normal(len(tt)), 4000) * np.exp(-tt * 300) * .4
    return st(x)


def pop():
    tt = T(0.14); f = 1100 * np.exp(-tt * 35) + 220
    return st(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 38))


def foam():  # wet squish: modulated low-passed noise bursts + bubbles
    d = 1.3; tt = T(d); n = lp(rng.standard_normal(len(tt)), 1800) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * tt)) * np.sin(np.pi * tt / d) ** 1.5
    x = n
    for k in range(40):
        o = int(rng.uniform(0, d - .05) * SR); f = rng.uniform(500, 1600); bt = T(0.04)
        b = np.sin(2 * np.pi * np.cumsum(f * (1 + bt * 18)) / SR) * np.exp(-bt * 120); x[o:o + len(b)] += b * .25
    return verb(st(x, .6), 0.15, .8)


def pump():  # plastic pump click + air puff
    tt = T(0.35)
    c = hp(rng.standard_normal(len(tt)), 1500) * np.exp(-tt * 220)
    puff = bp(rng.standard_normal(len(tt)), 300, 2500) * np.exp(-((tt - .09) / .05) ** 2) * .5
    return st(c + puff)


def chime():  # luxe two-note ding
    a = bell(1567.98, 1.4, decay=4); b = bell(2093.0, 1.6, decay=4)
    x = np.zeros(int(1.9 * SR)); x[:len(a)] += a; o = int(.12 * SR); x[o:o + len(b)] += b * .8
    return verb(st(x, .5), .35, 1.8)


def cash():  # checkout: tick + bright bell + coin shimmer
    x = np.zeros(int(1.6 * SR)); t1 = tick()[:, 0]; x[:len(t1)] += t1 * .7
    b = bell(2637, 1.2, decay=5); x[int(.06 * SR):int(.06 * SR) + len(b)] += b
    s = shimmer(.5, 8)[:, 0]; x[int(.1 * SR):int(.1 * SR) + len(s)][:len(x) - int(.1 * SR)] += s[:len(x) - int(.1 * SR)] * .5
    return verb(st(x, .5), .2, 1.0)


def heartbeat():
    x = np.zeros(int(1.0 * SR))
    for o, a in ((0, 1), (0.22, .7)):
        tt = T(0.25); k = np.sin(2 * np.pi * np.cumsum(60 * np.exp(-tt * 6) + 40) / SR) * np.exp(-tt * 18)
        i = int(o * SR); x[i:i + len(k)] += k * a
    return st(x)


def glitch():
    tt = T(0.22); sq = np.sign(np.sin(2 * np.pi * 180 * tt)) * (rng.random(len(tt)) > .5)
    return st(bp(sq, 300, 6000) * np.exp(-tt * 10), 1)


sfx = dict(impact=impact, riser=riser, whoosh=whoosh, swish=swish, shimmer=shimmer, tick=tick, pop=pop,
           foam=foam, pump=pump, chime=chime, cash=cash, heartbeat=heartbeat, glitch=glitch)
for name, fn in sfx.items():
    y = norm(fn(), -1.0); sf.write(f"{OUT}/{name}.wav", y.astype(np.float32), SR)


# ---------------- music bed (120 BPM, A minor-ish luxe house) ----------------
BPM = 120; beat = 60 / BPM; N = int(MUS_LEN * SR)
mus = np.zeros((N, 2))
def add(sig, t0, gain=1.0):
    i = int(t0 * SR); s = st(sig) if sig.ndim == 1 else sig
    j = min(N, i + len(s));
    if i < N: mus[i:j] += s[: j - i] * gain

def kick():
    tt = T(.4); f = 150 * np.exp(-tt * 28) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7) + hp(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 400) * .15
def hat(open_=False):
    tt = T(.18 if open_ else .05); return hp(rng.standard_normal(len(tt)), 7500) * np.exp(-tt * (25 if open_ else 110))
def clap():
    tt = T(.25); n = bp(rng.standard_normal(len(tt)), 900, 5000)
    env = sum(np.exp(-np.maximum(tt - o, 0) * 60) * (tt >= o) for o in (0, .01, .02)) * np.exp(-tt * 9)
    return n * env
def saw(f, d):
    tt = T(d); x = sum(np.sin(2 * np.pi * f * k * tt) / k for k in range(1, 12)); return x
def pad(freqs, d):
    tt = T(d); x = sum(saw(f, d) * .5 + saw(f * 1.004, d) * .5 for f in freqs)
    x = lp(x, 1400) * np.minimum(1, tt / .35) * np.minimum(1, (d - tt) / .4)
    return verb(st(x, 1), .45, 2.2)
def bass(f, d):
    tt = T(d); x = np.sin(2 * np.pi * f * tt) + .3 * np.sin(2 * np.pi * 2 * f * tt)
    return np.tanh(x * 1.6) * np.minimum(1, tt / .01) * np.exp(-tt * 3)

# Am - F - C - G  (one chord per bar)
chords = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [261.63, 329.63, 392.0], [196.0, 246.94, 293.66]]
roots = [55.0, 43.65, 65.41, 49.0]
bars = int(MUS_LEN / (4 * beat)) + 1
for b in range(bars):
    t0 = b * 4 * beat; c = b % 4
    add(pad(chords[c], 4 * beat + .3), t0, .10)
    for s in range(8):  # offbeat bass 8ths
        if s % 2 == 1: add(bass(roots[c] * (2 if s == 7 else 1), beat * .45), t0 + s * beat / 2, .32)
    intro = b < 1
    for q in range(4):
        tq = t0 + q * beat
        if not intro: add(kick(), tq, .55)
        add(hat(), tq + beat / 2, .10)
        if not intro and q % 2 == 1: add(clap(), tq, .22)
        for sx in (1, 3):
            add(hat(), tq + sx * beat / 4, .04)
    # pluck arpeggio on bars 2+
    if b >= 1:
        arp = chords[c] + [chords[c][0] * 2]
        for k in range(8):
            f = arp[[0, 1, 2, 3, 2, 1, 2, 3][k]] * 2
            add(verb(st(bell(f, .35, partials=((1, 1), (2, .2)), decay=9), .8), .3, 1.0), t0 + k * beat / 2, .07)

# sidechain pump on everything but kick is implicit; gentle master
env = np.ones(N); kk = np.arange(N) / SR
mus = lp(mus, 14000)
mus = mus / (np.max(np.abs(mus)) + 1e-9) * 0.8
fade = np.minimum(1, kk / .4)[:, None] * np.minimum(1, (MUS_LEN - kk) / 1.5)[:, None]
sf.write(f"{OUT}/music.wav", (mus * fade).astype(np.float32), SR)
print("ok", list(sfx), "music", MUS_LEN)
