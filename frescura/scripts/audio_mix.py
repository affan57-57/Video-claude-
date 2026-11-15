# Synthesize SFX + luxury deep-house bed, place on timeline, mix with studio voice.
# Usage: python audio_mix.py voice_studio.wav out_mix.wav [cues.json]
import sys, json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
rng = np.random.default_rng(11)
VOICE_OFF = 0.6
TOTAL = 30.0
T = lambda d: np.arange(int(d * SR)) / SR


def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x, axis=0)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x, axis=0)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x, axis=0)
def norm(x, db=-1): return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)
def st(x, w=0.0):
    if x.ndim == 2: return x
    d = int(0.008 * SR * w); R = np.roll(x, d) if d else x
    return np.stack([x, R], 1)


def bell(f, d, decay=6, parts=((1, 1), (2.0, .35), (3.01, .18), (4.2, .08))):
    t = T(d); x = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-decay * m ** .5 * t) for m, a in parts)
    return x * np.minimum(1, t / 0.002)


# ---------------- SFX ----------------
def whoosh(d=0.55, lo=250, hi=5000):
    n = rng.standard_normal(int(d * SR)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = lo + (hi - lo) * np.sin(np.pi * p) ** 1.5
        y[i:i + seg] = sosfilt(butter(2, [fc * .55, min(fc * 1.7, 20000)], 'band', fs=SR, output='sos'), n[i:i + seg])
    t = T(d); env = np.sin(np.pi * (t / d) ** 0.7) ** 2
    x = y * env; return np.stack([x * (1.2 - t / d), x * (0.2 + t / d)], 1)

def boom(d=2.2):
    t = T(d); f = 38 + 70 * np.exp(-t * 9); ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-t * 2.2) + 0.25 * np.tanh(3 * np.sin(ph)) * np.exp(-t * 5)
    n = lp(rng.standard_normal(len(t)), 900) * np.exp(-t * 14) * 0.6
    return st(np.tanh(1.6 * (x + n)))

def riser(d=1.2):
    t = T(d); n = rng.standard_normal(len(t)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        fc = 400 + 7000 * (i / len(n)) ** 2
        y[i:i + seg] = sosfilt(butter(2, [fc * .7, min(fc * 1.4, 20000)], 'band', fs=SR, output='sos'), n[i:i + seg])
    tone = np.sin(2 * np.pi * np.cumsum(220 + 660 * (t / d) ** 2) / SR) * 0.15
    return st((y + tone) * (t / d) ** 2, 1)

def shimmer(d=1.6, n=22):
    x = np.zeros(int(d * SR) + SR)
    for k in range(n):
        o = int(rng.uniform(0, d * .8) * SR); f = rng.choice([1760, 2093, 2637, 3136, 3520, 4186]) * rng.uniform(.998, 1.002)
        b = bell(f, .6, decay=9, parts=((1, 1), (2.0, .25))); x[o:o + len(b)] += b * rng.uniform(.3, 1)
    x = hp(x, 1200); return np.stack([x, np.roll(x, int(.013 * SR))], 1)

def pop():
    t = T(.1); f = 1100 * np.exp(-t * 35) + 220; x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45)
    return st(x)

def tick():
    t = T(.035); x = np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 180) + hp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 300) * .4
    return st(x)

def click():
    t = T(.06); x = hp(rng.standard_normal(len(t)), 1500) * np.exp(-t * 160) + np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 90) * .6
    return st(x)

def ding(): return st(bell(1568, 1.4, decay=4) + .6 * bell(2349, 1.4, decay=5))

def chaching():
    x = np.zeros(int(1.4 * SR)); c = click()[:, 0]; x[:len(c)] += c
    for i, f in enumerate([2637, 3136, 3951]):
        b = bell(f, 1.0, decay=5); o = int((.08 + i * .05) * SR); x[o:o + len(b)] += b * .7
    return st(x, 1)

def swish_soft(d=.35):
    w = whoosh(d, 1500, 9000); return w * .8

def bubbles(d=1.0, n=26):
    x = np.zeros(int(d * SR) + SR // 4)
    for k in range(n):
        o = int(rng.uniform(0, d) * SR); L = int(rng.uniform(.015, .04) * SR); t = np.arange(L) / SR
        f0 = rng.uniform(600, 1800); f = f0 * (1 + 3 * t / t[-1])
        b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / t[-1]) * rng.uniform(.3, 1)
        x[o:o + L] += b
    sq = bp(rng.standard_normal(len(x)), 800, 4000) * .15 * np.exp(-np.arange(len(x)) / SR * 2)
    return st(x + sq, 1)

def heart_ping(): return st(bell(1318.5, 1.0, decay=5) + .5 * bell(1975.5, 1.0, decay=6))

def lid():  # gift box lid lift: soft paper swish + low thump
    t = T(.5); th = np.sin(2 * np.pi * np.cumsum(90 + 60 * np.exp(-t * 20)) / SR) * np.exp(-t * 12)
    return st(th) * .8 + whoosh(.5, 800, 6000)[:len(t)] * .7

def alert():
    x = np.zeros(int(.5 * SR))
    for i in range(2):
        t = T(.09); b = np.sign(np.sin(2 * np.pi * 880 * t)) * .3 + np.sin(2 * np.pi * 1760 * t)
        b *= np.exp(-t * 25); o = int(i * .14 * SR); x[o:o + len(b)] += b
    return st(lp(x, 6000))

SFX = dict(whoosh=whoosh, boom=boom, riser=riser, shimmer=shimmer, pop=pop, tick=tick, click=click, ding=ding,
           chaching=chaching, swish=swish_soft, bubbles=bubbles, heart=heart_ping, lid=lid, alert=alert)
CACHE = {k: norm(st(f()), -1) for k, f in SFX.items()}

# ---------------- Music bed (122 BPM luxe deep house) ----------------
BPM = 122; B = 60 / BPM
def note(m): return 440 * 2 ** ((m - 69) / 12)
chords = [[57, 60, 64, 67, 71], [53, 57, 60, 64, 67], [48, 52, 55, 59, 62], [55, 59, 62, 64, 66]]  # Am9 Fmaj9 Cmaj9 G6/9
bass = [45, 41, 36, 43]
N = int((TOTAL + 1) * SR); mus = np.zeros((N, 2))
def add(buf, x, t0, g=1.0):
    i = int(t0 * SR);
    if i >= len(buf): return
    x = st(x); L = min(len(x), len(buf) - i); buf[i:i + L] += x[:L] * g

kick = (lambda t: np.tanh(2.2 * np.sin(2 * np.pi * np.cumsum(45 + 110 * np.exp(-t * 30)) / SR) * np.exp(-t * 7)))(T(.45))
clap = (lambda t: bp(rng.standard_normal(len(t)), 900, 5000) * (np.exp(-t * 28) + .5 * np.exp(-((t - .012) % .011) * 400) * (t < .035)))(T(.25))
hat = (lambda t: hp(rng.standard_normal(len(t)), 7500) * np.exp(-t * 60))(T(.08))
ohat = (lambda t: hp(rng.standard_normal(len(t)), 6500) * np.exp(-t * 14))(T(.25))
def pad(ms, d):
    t = T(d); x = np.zeros(len(t))
    for m in ms:
        for det in (-0.09, 0.0, 0.09):
            f = note(m + 12) * 2 ** (det / 12); x += ((2 * ((f * t) % 1) - 1)) * .2
    x = lp(x, 1400, 2); env = np.minimum(1, t / .25) * np.minimum(1, (d - t) / .3); return x * env
def pluck(m, d=.35):
    t = T(d); f = note(m + 12); x = (2 * ((f * t) % 1) - 1) * np.exp(-t * 9); return lp(x, 3500)
def subb(m, d):
    t = T(d); x = np.sin(2 * np.pi * note(m) * t) + .3 * np.sin(4 * np.pi * note(m) * t)
    return x * np.minimum(1, t / .01) * np.minimum(1, (d - t) / .05)

end_break = 25.3
n_beats = int(TOTAL / B) + 1
for b in range(n_beats):
    t0 = b * B
    if t0 > TOTAL: break
    bar = b // 4; ch = bar % 4; beat = b % 4
    if t0 < end_break - 0.01:
        if t0 >= 0.55: add(mus, kick, t0, .9)
        if beat in (1, 3) and t0 >= 0.55: add(mus, clap, t0, .35)
        add(mus, hat, t0 + B / 2, .22); add(mus, hat, t0 + B / 4 * 3, .1)
        if beat % 2 == 1: add(mus, ohat, t0 + B / 2, .12)
        add(mus, subb(bass[ch], B * .45), t0 + B / 2, .5)
        arp = chords[ch][(b * 3) % 5]; add(mus, pluck(arp), t0, .18); add(mus, pluck(chords[ch][(b * 3 + 2) % 5]), t0 + B / 2, .12)
    if beat == 0: add(mus, pad(chords[ch], 4 * B), t0, .22)
# final chord ring after end break
add(mus, pad(chords[0], 4.5), end_break, .3); add(mus, subb(45, 2.5) * np.exp(-T(2.5) * 1.2), end_break, .5)
add(mus, kick, end_break, 1.0)
# intro filter sweep on first 1s
sw = int(1.2 * SR)
for c in range(2):
    seg = mus[:sw, c].copy(); lo = lp(seg, 600); mix = np.linspace(1, 0, sw) ** 1.5
    mus[:sw, c] = lo * mix + seg * (1 - mix)
mus = norm(mus, -3)

# ---------------- Timeline ----------------
voice, vsr = sf.read(sys.argv[1]); assert vsr == SR
if voice.ndim == 2: voice = voice.mean(1)
cues = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else []
fx = np.zeros((N, 2))
for c in cues:
    add(fx, CACHE[c['s']], c['t'], 10 ** (c.get('db', -12) / 20))

vo = np.zeros((N, 2)); add(vo, np.stack([voice, voice], 1) * 0.7071, VOICE_OFF, 1.0)
# duck music under voice
env = np.abs(vo[:, 0]); k = int(.15 * SR)
env = np.convolve(env, np.ones(k) / k, 'same'); speech = (env > 0.01).astype(float)
k2 = int(.3 * SR); speech = np.convolve(speech, np.ones(k2) / k2, 'same')
duck = 10 ** ((-9 * np.clip(speech, 0, 1)) / 20)
mix = vo + fx + mus * 10 ** (-11 / 20) * duck[:, None]
mix = mix[:int(TOTAL * SR)]
fo = int(1.2 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
sf.write(sys.argv[2], mix.astype(np.float32), SR, subtype='FLOAT')
print('ok', len(mix) / SR)
