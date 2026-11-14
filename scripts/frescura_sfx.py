"""Synthesized SFX pack + upbeat minimal-luxury music bed (no licensing issues).
Usage: python frescura_sfx.py OUTDIR [music_seconds]
"""
import sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
OUT = sys.argv[1]
MUS_LEN = float(sys.argv[2]) if len(sys.argv) > 2 else 40.0
rng = np.random.default_rng(11)
t = lambda d: np.arange(int(d * SR)) / SR


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, hi], btype="band", fs=SR, output="sos"), x, axis=0)


def hp(x, f, o=2):
    return sosfilt(butter(o, f, btype="high", fs=SR, output="sos"), x, axis=0)


def lp(x, f, o=2):
    return sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x, axis=0)


def st(x, w=0.0):
    if x.ndim == 2:
        return x
    d = int(w * SR)
    return np.stack([x, np.roll(x, d) if d else x], 1)


def norm(x, db=-1.0):
    return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)


def bell(f, d, partials=((1, 1), (2.0, .4), (3.01, .2), (4.2, .1)), decay=6):
    tt = t(d)
    x = sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-decay * m ** .5 * tt) for m, a in partials)
    return x * np.minimum(1, tt / 0.003)


def whoosh(d=0.55, lo=250, hi=5200):
    n = rng.standard_normal(int(d * SR)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = lo + (hi - lo) * np.sin(np.pi * p) ** 2
        y[i:i + seg] = bp(n[i:i + seg], fc * .55, min(fc * 1.7, 20000))
    tt = t(d); env = np.sin(np.pi * tt / d) ** 1.5
    x = y * env; return np.stack([x * (1 - tt / d) + .25 * x, x * (tt / d) + .25 * x], 1)


def impact():  # cinematic sub boom + click transient
    tt = t(1.6); f = 55 * np.exp(-tt * 3) + 32
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 3.2)
    nz = lp(rng.standard_normal(len(tt)), 2500) * np.exp(-tt * 18)
    clk = hp(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 120)
    return st(sub * 1.0 + nz * .35 + clk * .25, 0.004)


def riser(d=1.4):
    tt = t(d); n = rng.standard_normal(len(tt)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = 400 + 7000 * p ** 2
        y[i:i + seg] = bp(n[i:i + seg], fc * .7, min(fc * 1.4, 20000))
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * (tt / d) ** 2) / SR) * .25
    env = (tt / d) ** 2.2
    return st((y + tone) * env, 0.007)


def tick():
    tt = t(0.05); x = hp(rng.standard_normal(len(tt)), 4000) * np.exp(-tt * 260) + np.sin(2 * np.pi * 3200 * tt) * np.exp(-tt * 200) * .6
    return st(x)


def glass():  # crystal tap (luxury)
    x = bell(2093, 1.6, partials=((1, 1), (2.76, .5), (5.4, .25), (8.9, .1)), decay=4)
    return st(x, 0.009)


def ping():  # phone notification
    a = bell(1567.98, .45, decay=10); b = bell(2093, .6, decay=9)
    x = np.zeros(int(.7 * SR)); x[:len(a)] += a; o = int(.09 * SR); x[o:o + len(b)] += b
    return st(x)


def shutter():
    tt = t(.18); x = hp(rng.standard_normal(len(tt)), 1800) * (np.exp(-tt * 90) + .7 * np.exp(-np.maximum(tt - .07, 0) * 120) * (tt > .07))
    return st(x)


def pop():
    tt = t(0.14); f = 1000 * np.exp(-tt * 28) + 200
    return st(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 38))


def squish():  # foam pump: airy wet squelch
    tt = t(.55); n = rng.standard_normal(len(tt)); y = np.zeros_like(n); seg = 256
    for i in range(0, len(n), seg):
        p = i / len(n); fc = 900 + 1600 * np.sin(np.pi * p * 2.3) ** 2
        y[i:i + seg] = bp(n[i:i + seg], fc * .6, fc * 1.5)
    bub = np.zeros_like(tt)
    for k in range(18):
        o = int(rng.uniform(.05, .45) * SR); b = bell(rng.uniform(700, 1800), .08, partials=((1, 1),), decay=40)
        bub[o:o + len(b)] += b[:len(bub) - o] * .5
    env = np.minimum(1, tt / .03) * np.exp(-tt * 3)
    return st((y * .8 + bub) * env, 0.005)


def sparkle(d=1.1, n=16):
    x = np.zeros(int(d * SR) + SR // 2)
    for k in range(n):
        o = int(rng.uniform(0, d * .8) * SR); b = bell(rng.uniform(2600, 6500), .4, partials=((1, 1), (2.01, .3)), decay=13)
        x[o:o + len(b)] += b * rng.uniform(.4, 1)
    x = hp(x, 1500); return np.stack([x, np.roll(x, int(.011 * SR))], 1)


def heartbeat():
    x = np.zeros(int(1.1 * SR))
    for o, a in ((0, 1), (.22, .7)):
        tt = t(.25); f = 70 * np.exp(-tt * 10) + 40
        b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 16) * a; s = int(o * SR); x[s:s + len(b)] += b
    return st(x)


def kaching():
    x = np.zeros(int(1.5 * SR))
    c = hp(rng.standard_normal(int(.06 * SR)), 2500) * np.exp(-t(.06) * 80); x[:len(c)] += c * .6
    for i, f in enumerate([2637, 3136, 3951]):
        b = bell(f, 1.2, decay=5); o = int((.05 + i * .045) * SR); x[o:o + len(b)] += b[:len(x) - o]
    return st(x, .006)


def glitch():
    tt = t(.35); x = np.sign(np.sin(2 * np.pi * 180 * tt)) * .3 + hp(rng.standard_normal(len(tt)), 2000) * .5
    gate = (np.floor(tt * 40) % 2 == 0) * np.exp(-tt * 6); return st(x * gate, .003)


def typing(d=1.0, rate=14):
    x = np.zeros(int(d * SR))
    for k in range(int(d * rate)):
        o = int((k / rate + rng.uniform(-.01, .01)) * SR); c = tick()[:, 0] * rng.uniform(.4, .9)
        if 0 <= o < len(x) - len(c): x[o:o + len(c)] += c
    return st(x)


def tada():
    x = np.zeros(int(1.8 * SR))
    for i, f in enumerate([1046.5, 1318.5, 1568.0, 2093.0]):
        b = bell(f, 1.4, decay=3.5); o = int(i * .07 * SR); x[o:o + len(b)] += b
    return st(x, .008)


SFX = dict(whoosh=whoosh, whoosh_s=lambda: whoosh(.32, 600, 8000), impact=impact, riser=riser, tick=tick,
           glass=glass, ping=ping, shutter=shutter, pop=pop, squish=squish, sparkle=sparkle,
           heartbeat=heartbeat, kaching=kaching, glitch=glitch, typing=typing, tada=tada)
for name, fn in SFX.items():
    y = norm(fn(), -1.0); sf.write(f"{OUT}/{name}.wav", y.astype(np.float32), SR)

# ---------------- music bed: 120 BPM minimal luxury house ----------------
BPM = 120; beat = 60 / BPM; N = int(MUS_LEN * SR); mus = np.zeros((N, 2))


def add(buf, x, at):
    s = int(at * SR)
    if s >= len(buf): return
    x = st(x) if x.ndim == 1 else x; e = min(len(buf), s + len(x)); buf[s:e] += x[:e - s]


def kick():
    tt = t(.45); f = 140 * np.exp(-tt * 28) + 46
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7) + hp(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 300) * .15


def hat(open_=False):
    tt = t(.25 if open_ else .06); return hp(rng.standard_normal(len(tt)), 7000) * np.exp(-tt * (18 if open_ else 90))


def clap():
    tt = t(.3); n = bp(rng.standard_normal(len(tt)), 900, 5000)
    env = sum(np.exp(-np.maximum(tt - d, 0) * 60) * (tt >= d) for d in (0, .012, .024)) * np.exp(-tt * 9)
    return n * env


def pluck(f, d=.35):
    tt = t(d); x = sum(np.sin(2 * np.pi * f * h * tt) / h ** 1.6 for h in (1, 2, 3, 4)) * np.exp(-tt * 9)
    return lp(x, 3500)


def pad(freqs, d):
    tt = t(d); x = np.zeros(len(tt))
    for f in freqs:
        for det in (-.12, 0, .12):
            x += np.sin(2 * np.pi * f * 2 ** (det / 12) * tt + rng.uniform(0, 6))
    env = np.minimum(1, tt / .5) * np.minimum(1, (d - tt) / .4)
    return lp(x * env, 1800) / len(freqs)


# Am9 - Fmaj7 - Cmaj7 - G6 (moody, luxe)
prog = [[220, 261.6, 329.6, 493.9], [174.6, 220, 261.6, 329.6], [130.8, 196, 246.9, 329.6], [196, 246.9, 293.7, 329.6]]
bass = [55, 43.65, 65.41, 49]
bar = beat * 4; nb = int(MUS_LEN / bar) + 1
for b in range(nb):
    t0 = b * bar; ch = prog[b % 4]
    add(mus, st(pad(ch, bar + .3) * .22, .013), t0)
    for i in range(4):
        tb = t0 + i * beat
        if b >= 1 or i >= 2: add(mus, kick() * .9, tb)
        add(mus, hat() * .16, tb + beat / 2)
        add(mus, hat() * .07, tb + beat * .75)
        if i in (1, 3) and b >= 1: add(mus, clap() * .32, tb)
        # off-beat sub bass
        tt = t(beat * .45); bs = np.sin(2 * np.pi * bass[b % 4] * tt) * np.minimum(1, tt / .01) * np.exp(-tt * 3)
        if b >= 1: add(mus, bs * .55, tb + beat / 2)
    # arpeggio plucks
    arp = [ch[0] * 2, ch[2] * 2, ch[1] * 2, ch[3] * 2] * 2
    for k, f in enumerate(arp):
        add(mus, st(pluck(f) * .1, .02 * (k % 2)), t0 + k * beat / 2)
# sidechain-ish duck on kicks
tt = np.arange(N) / SR; ph = (tt % beat) / beat; duck = 0.55 + 0.45 * np.minimum(1, ph / .35)
mus[:, 0] *= duck; mus[:, 1] *= duck
fade = np.minimum(1, tt / .3) * np.minimum(1, (MUS_LEN - tt) / 1.5)
mus *= fade[:, None]
sf.write(f"{OUT}/music.wav", norm(mus, -1.0).astype(np.float32), SR)
print("ok")
