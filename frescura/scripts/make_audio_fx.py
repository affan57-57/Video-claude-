"""Synthesize the sound effects and the background music bed for the Frescura Body ad.

usage: python make_audio_fx.py OUT_DIR MUSIC_SECONDS
Everything is generated from code (no samples), so it is free to use.
"""
import sys, os
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
out = sys.argv[1]
MUSIC_LEN = float(sys.argv[2]) if len(sys.argv) > 2 else 40
os.makedirs(out, exist_ok=True)
rng = np.random.default_rng(11)


def t(d):
    return np.arange(int(d * SR)) / SR


def norm(x, db=-1.0):
    return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x, axis=0)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, btype="low", fs=SR, output="sos"), x, axis=0)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, btype="high", fs=SR, output="sos"), x, axis=0)


def stereo(x, width=0.0):
    d = int(0.008 * SR * width)
    return np.stack([x, np.roll(x, d)], 1)


def sweep_noise(d, f0, f1, q=0.5):
    n = rng.standard_normal(int(d * SR))
    y = np.zeros_like(n)
    seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n)
        fc = f0 * (f1 / f0) ** p
        y[i:i + seg] = sosfilt(butter(2, [fc * (1 - q), fc * (1 + q)], btype="band", fs=SR, output="sos"), n[i:i + seg])
    return y


def bell(f, d, partials=((1, 1), (2.0, .35), (3.01, .18), (4.2, .08)), decay=6):
    tt = t(d)
    x = sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-decay * m ** .5 * tt) for m, a in partials)
    return x * np.minimum(1, tt / 0.002)


# ---------------------------------------------------------------- effects
def whoosh(d=0.55):
    tt = t(d)
    y = sweep_noise(d, 250, 5000) * np.sin(np.pi * tt / d) ** 3
    pan = tt / d
    return np.stack([y * (1 - pan) + .25 * y, y * pan + .25 * y], 1)


def swipe(d=0.28):  # short airy swipe for caption changes
    tt = t(d)
    y = hp(sweep_noise(d, 1800, 9000, .4), 1200) * np.exp(-((tt - d * .35) / (d * .25)) ** 2)
    return stereo(y, 1)


def riser(d=1.6):
    tt = t(d)
    n = sweep_noise(d, 300, 9000, .35) * (tt / d) ** 2.2
    f = 180 * (8 ** (tt / d))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * (tt / d) ** 3 * .35
    y = n + tone
    y[-int(.02 * SR):] *= np.linspace(1, 0, int(.02 * SR))
    return stereo(y, 1)


def impact(d=1.8):  # deep cinematic hit for the hook
    tt = t(d)
    f = 38 + 120 * np.exp(-tt * 18)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.6)
    click = lp(rng.standard_normal(len(tt)), 3500) * np.exp(-tt * 60) * .7
    tail = lp(rng.standard_normal(len(tt)), 900) * np.exp(-tt * 3.5) * .25
    y = np.tanh(1.6 * (sub + click + tail))
    return stereo(y, .6)


def pop():
    tt = t(0.14)
    f = 1100 * np.exp(-tt * 32) + 220
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 38)
    return stereo(x)


def tick():  # crisp UI click for checklist items
    tt = t(0.06)
    x = hp(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 140) * .6 + np.sin(2 * np.pi * 2600 * tt) * np.exp(-tt * 90)
    return stereo(x)


def shimmer(d=1.4, n=22):
    x = np.zeros(int((d + .6) * SR))
    for k in range(n):
        o = int(rng.uniform(0, d * .85) * SR)
        f = rng.uniform(2600, 7500)
        b = bell(f, .45, partials=((1, 1), (2.01, .25)), decay=12) * rng.uniform(.3, 1) * (1 - o / len(x))
        x[o:o + len(b)] += b
    x = hp(x, 1800)
    return np.stack([x, np.roll(x, int(.013 * SR))], 1)


def bubbles(d=1.2, n=26):  # foam / soap bubbles
    x = np.zeros(int((d + .2) * SR))
    for k in range(n):
        o = int(rng.uniform(0, d) * SR)
        f0 = rng.uniform(500, 1700)
        L = int(rng.uniform(.03, .07) * SR)
        tt = np.arange(L) / SR
        f = f0 * (1 + 2.5 * tt / tt[-1])
        b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / tt[-1]) ** 2 * rng.uniform(.3, 1)
        x[o:o + L] += b
    x = bp(x, 300, 5000)
    pan = np.linspace(-.5, .5, len(x))
    return np.stack([x * (1 - pan), x * (1 + pan)], 1)


def chime():  # two-note luxury chime for the brand reveal
    a, b = bell(1318.5, 1.3, decay=4), bell(1975.5, 1.6, decay=3.5)
    x = np.zeros(int(2.0 * SR))
    x[:len(a)] += a
    o = int(.14 * SR)
    x[o:o + len(b)] += .8 * b
    return np.stack([x, np.roll(x, int(.01 * SR))], 1)


def ding():  # CTA "cart" ding
    x = bell(2093, 1.0, decay=5)
    y = np.pad(bell(2637, .9, decay=5), (int(.09 * SR), 0))[:len(x)]
    x[:len(y)] += .6 * y
    return stereo(x)


def bass_drop(d=1.0):
    tt = t(d)
    f = 90 * np.exp(-tt * 2.2) + 32
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, tt / .01) * np.exp(-tt * 2.2)
    return stereo(np.tanh(2 * y))


fx = dict(whoosh=whoosh, swipe=swipe, riser=riser, impact=impact, pop=pop, tick=tick,
          shimmer=shimmer, bubbles=bubbles, chime=chime, ding=ding, drop=bass_drop)
for name, fn in fx.items():
    y = norm(fn(), -1.0).astype(np.float32)
    sf.write(f"{out}/{name}.wav", y, SR)
    print(name, round(len(y) / SR, 2))

# ---------------------------------------------------------------- music bed
# 122 BPM minimal deep-house loop: soft kick, off-beat hats, rim, warm pad, sub bass, pluck.
BPM = 122
beat = 60 / BPM
N = int(MUSIC_LEN * SR)
mix = np.zeros((N, 2))


def place(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N:
        return
    s = sig[:N - i]
    if s.ndim == 1:
        s = np.stack([s * (1 - pan) ** .5, s * (1 + pan) ** .5], 1) / 1.0
    mix[i:i + len(s)] += s * gain


def kick():
    tt = t(.4)
    f = 48 + 110 * np.exp(-tt * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)


def hat(open_=False):
    tt = t(.18 if open_ else .05)
    return hp(rng.standard_normal(len(tt)), 7000) * np.exp(-tt * (25 if open_ else 110))


def rim():
    tt = t(.12)
    return bp(rng.standard_normal(len(tt)), 1500, 4500) * np.exp(-tt * 45) + .4 * np.sin(2 * np.pi * 820 * tt) * np.exp(-tt * 60)


def note(f, d, kind="pad"):
    tt = t(d)
    if kind == "pad":
        x = sum(np.sin(2 * np.pi * f * (1 + dt) * tt) for dt in (-.004, 0, .005)) / 3
        x += .3 * np.sin(2 * np.pi * 2 * f * tt)
        env = np.minimum(1, tt / .25) * np.minimum(1, (d - tt) / .3)
        return lp(x * env, 2600)
    if kind == "bass":
        x = np.sin(2 * np.pi * f * tt) + .15 * np.sin(2 * np.pi * 2 * f * tt)
        return x * np.minimum(1, tt / .01) * np.exp(-tt * 3)
    if kind == "pluck":
        x = np.sign(np.sin(2 * np.pi * f * tt)) * .5 + np.sin(2 * np.pi * f * tt)
        return lp(x * np.exp(-tt * 9) * np.minimum(1, tt / .003), 3200)


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


# Am9 - Fmaj7 - Cmaj7 - Em7 (one bar each)
chords = [[57, 60, 64, 67, 71], [53, 57, 60, 64, 69], [48, 55, 59, 64, 67], [52, 55, 59, 62, 67]]
roots = [45, 41, 48, 40]
arp = [0, 2, 4, 3, 1, 3, 4, 2]
bar = 4 * beat
nbars = int(MUSIC_LEN / bar) + 1
for b in range(nbars):
    t0 = b * bar
    c = chords[b % 4]
    for m in c:
        place(note(hz(m), bar + .2, "pad"), t0, .07, pan=rng.uniform(-.4, .4))
    for k in range(8):
        place(note(hz(roots[b % 4]), beat * .5, "bass"), t0 + k * beat * .5 + (beat * .5 if k % 2 == 0 else 0) * 0, .22 if k % 2 else .0)
    for k in range(4):
        place(kick(), t0 + k * beat, .55)
        place(hat(), t0 + k * beat + beat / 2, .13, pan=.3)
        place(hat(), t0 + k * beat + beat * .75, .05, pan=-.3)
        if k in (1, 3):
            place(rim(), t0 + k * beat, .16, pan=-.15)
    if b >= 1:
        for k in range(8):
            place(note(hz(c[arp[k] % len(c)] + 12), beat * .5, "pluck"), t0 + k * beat * .5, .06, pan=.5 * np.sin(k))
    if b % 4 == 3:
        place(hat(True), t0 + 3.5 * beat, .12)

# sidechain-style pump keyed on the kick for movement
tt = np.arange(N) / SR
ph = (tt % beat) / beat
pump = .55 + .45 * np.minimum(1, ph / .35)
mix[:, 0] *= pump
mix[:, 1] *= pump
fade = np.minimum(1, tt / .4) * np.minimum(1, (MUSIC_LEN - tt) / 1.5)
mix *= fade[:, None]
sf.write(f"{out}/music.wav", norm(mix, -3).astype(np.float32), SR)
print("music", MUSIC_LEN, "bpm", BPM)
