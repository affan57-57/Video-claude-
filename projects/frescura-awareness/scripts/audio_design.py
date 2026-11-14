"""Synthesize SFX bus + luxe music bed (112 BPM) for the Frescura Body edit.
Writes sfx_bus.wav and music_bus.wav (48 kHz stereo, 37.2 s)."""
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve
SR = 48000; DUR = 37.2; N = int(DUR * SR); rng = np.random.default_rng(3)
t = lambda d: np.arange(int(d * SR)) / SR
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype='band', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype='high', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype='low', fs=SR, output='sos'), x)
def norm(x): return x / (np.max(np.abs(x)) + 1e-9)
def ir(d=1.4, damp=4.0):
    tt = t(d); n = rng.standard_normal((len(tt), 2)) * np.exp(-damp * tt)[:, None]
    n[:, 0] = lp(n[:, 0], 6000); n[:, 1] = lp(n[:, 1], 6000); return n / np.sqrt((n ** 2).sum(0))
IR = ir()
def verb(x, wet=.25):
    m = x if x.ndim == 1 else x.mean(1)
    w = np.stack([fftconvolve(m, IR[:, 0]), fftconvolve(m, IR[:, 1])], 1)
    d = np.zeros_like(w); d[:len(m)] = x[:, None] if x.ndim == 1 else x
    return d * (1 - wet) + w * wet * 3
def st(x): return np.stack([x, x], 1)
def bell(f, d, parts=((1, 1), (2.0, .45), (3.01, .22), (4.2, .1)), dec=6):
    tt = t(d); x = sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-dec * m ** .5 * tt) for m, a in parts)
    return x * np.minimum(1, tt / .002)
# ---------------- SFX ----------------
def impact(big=1.0):
    tt = t(1.6); f = 38 + 90 * np.exp(-tt * 18); ph = 2 * np.pi * np.cumsum(f) / SR
    sub = np.sin(ph) * np.exp(-tt * 3.2); click = hp(rng.standard_normal(len(tt)), 1500) * np.exp(-tt * 60) * .5
    body = bp(rng.standard_normal(len(tt)), 80, 900) * np.exp(-tt * 9) * .6
    return verb(norm(sub * 1.2 + click + body) * big, .2)
def whoosh(d=.55, lo=300, hi=4200):
    n = rng.standard_normal(int(d * SR)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = lo + (hi - lo) * np.sin(np.pi * p) ** 2
        y[i:i + seg] = bp(n[i:i + seg], fc * .6, min(fc * 1.7, 20000))
    tt = t(d); env = np.sin(np.pi * tt / d) ** 2; x = norm(y * env)
    return np.stack([x * (1 - tt / d) + .3 * x, x * (tt / d) + .3 * x], 1)
def riser(d=1.2):
    tt = t(d); n = rng.standard_normal(len(tt)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        fc = 400 + 7000 * (i / len(n)) ** 2; y[i:i + seg] = bp(n[i:i + seg], fc * .7, min(fc * 1.4, 20000))
    tone = np.sin(2 * np.pi * np.cumsum(220 + 660 * (tt / d) ** 2) / SR) * .25
    return verb(norm((y + tone) * (tt / d) ** 2), .25)
def pop():
    tt = t(.14); f = 1100 * np.exp(-tt * 28) + 220; x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 38)
    return verb(norm(x), .15)
def tick():
    tt = t(.05); x = np.sin(2 * np.pi * 2600 * tt) * np.exp(-tt * 160) + hp(rng.standard_normal(len(tt)), 4000) * np.exp(-tt * 300) * .4
    return st(norm(x))
def glass(f=2093):
    x = bell(f, 1.6, dec=4) + .4 * bell(f * 1.5, 1.6, dec=5); return verb(norm(x), .35)
def chime():
    x = np.zeros(int(1.8 * SR))
    for i, f in enumerate([1318.5, 1760, 2637]):
        b = bell(f, 1.4, dec=4); o = int(i * .07 * SR); x[o:o + len(b)] += b
    return verb(norm(x), .35)
def shimmer(d=1.2, n=26):
    x = np.zeros(int((d + .5) * SR))
    for k in range(n):
        o = int(rng.uniform(0, d * .8) * SR); b = bell(rng.uniform(2600, 7000), .4, parts=((1, 1), (2.01, .3)), dec=14)
        x[o:o + len(b)] += b * rng.uniform(.4, 1)
    x = hp(x, 1800); return verb(np.stack([x, np.roll(x, int(.012 * SR))], 1) / np.max(np.abs(x)), .3)
def swipe():
    tt = t(.22); x = hp(rng.standard_normal(len(tt)), 2500) * np.sin(np.pi * tt / .22) ** 1.5
    return st(norm(x))
def bubbles(d=1.6, n=40):
    x = np.zeros(int((d + .2) * SR))
    for k in range(n):
        o = int(rng.uniform(0, d) * SR); L = int(rng.uniform(.012, .03) * SR); tt = np.arange(L) / SR
        f0 = rng.uniform(500, 1400); b = np.sin(2 * np.pi * np.cumsum(f0 + f0 * 2.5 * tt / tt[-1]) / SR) * np.exp(-tt * 120)
        x[o:o + L] += b * rng.uniform(.3, 1)
    return verb(norm(x), .15)
def ringbell():
    x = np.zeros(int(2.2 * SR))
    for i in range(6):
        f = 1568 if i % 2 == 0 else 2093; b = bell(f, 1.2, dec=5); o = int(i * .13 * SR); x[o:o + len(b)] += b * (1 - i * .1)
    return verb(norm(x), .3)
def gift_thud():
    tt = t(.4); x = np.sin(2 * np.pi * np.cumsum(140 * np.exp(-tt * 8) + 60) / SR) * np.exp(-tt * 14)
    return verb(norm(x + bp(rng.standard_normal(len(tt)), 200, 1500) * np.exp(-tt * 30) * .3), .2)
def typewriter_ticks(d=3.2, n=24):
    x = np.zeros((int((d + .2) * SR), 2)); tk = tick()
    for k in range(n):
        o = int(d * (1 - (1 - k / n) ** 1.6) * SR); x[o:o + len(tk)] += tk * .55
    return x
bus = np.zeros((N, 2))
def put(sig, at, db):
    s = sig if sig.ndim == 2 else st(sig); i = int(at * SR); s = s[:max(0, N - i)]
    bus[i:i + len(s)] += s * 10 ** (db / 20)
cues = [
    (impact(1.0), 0.0, -4), (shimmer(), 0.05, -14), (whoosh(), 1.42, -9), (typewriter_ticks(), 1.7, -16),
    (impact(.6), 3.10, -10), (whoosh(.45), 5.75, -10), (pop(), 6.30, -8), (pop(), 6.85, -8), (pop(), 8.10, -8),
    (chime(), 9.62, -13), (whoosh(), 10.28, -10), (impact(.5), 11.30, -12), (swipe(), 12.85, -9),
    (whoosh(.4, 600, 6000), 13.25, -13), (tick(), 14.62, -8), (glass(2637), 14.62, -19), (tick(), 15.77, -8), (glass(2349), 15.77, -19),
    (whoosh(), 17.28, -10), (gift_thud(), 18.85, -8), (riser(1.3), 19.05, -12), (impact(1.0), 20.34, -5), (shimmer(1.4, 34), 20.36, -10),
    (glass(1760), 21.0, -14), (whoosh(.35), 21.78, -11), (bubbles(), 23.25, -11), (whoosh(.35), 23.2, -12),
    (whoosh(), 24.88, -10), (impact(.45), 25.80, -11), (glass(2093), 25.80, -15), (impact(.45), 26.22, -11), (glass(2637), 26.22, -15),
    (whoosh(.6, 200, 2500), 26.82, -10), (impact(.55), 28.22, -11), (swipe(), 29.1, -9), (riser(.45), 29.95, -16), (impact(.7), 30.40, -8),
    (chime(), 31.42, -14), (whoosh(), 31.82, -10), (ringbell(), 32.08, -9), (pop(), 33.40, -7), (impact(.6), 33.40, -12),
    (riser(.8), 34.55, -15), (impact(1.0), 35.30, -6), (shimmer(1.6, 36), 35.35, -10),
]
for s, a, db in cues: put(s, a, db)
sf.write('sfx_bus.wav', bus.astype(np.float32), SR)
# ---------------- MUSIC (112 BPM, Am-F-C-G) ----------------
bpm = 112; beat = 60 / bpm; mus = np.zeros((N, 2))
def addm(sig, at, g):
    s = sig if sig.ndim == 2 else st(sig); i = int(at * SR)
    if i >= N: return
    s = s[:N - i]; mus[i:i + len(s)] += s * g
def kick():
    tt = t(.45); f = 45 + 120 * np.exp(-tt * 30); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7)
def hat(open_=False):
    d = .18 if open_ else .05; tt = t(d); return hp(rng.standard_normal(len(tt)), 7500) * np.exp(-tt * (25 if open_ else 90))
def clap():
    tt = t(.25); n = bp(rng.standard_normal(len(tt)), 900, 5000)
    env = sum(np.exp(-np.maximum(tt - o, 0) * 60) * (tt >= o) for o in (0, .012, .024)); return verb(n * env, .3)
chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
mf = lambda m: 440 * 2 ** ((m - 69) / 12)
def pad(notes, d):
    tt = t(d); x = np.zeros(len(tt))
    for m in notes:
        for det in (-.12, 0, .12):
            f = mf(m + 12) * 2 ** (det / 12); x += 2 * ((tt * f) % 1) - 1
    x = lp(x, 1400, 2); env = np.minimum(1, tt / .25) * np.minimum(1, (d - tt) / .3); return x * env / 9
def bass(m, d):
    tt = t(d); f = mf(m - 12); x = np.sin(2 * np.pi * f * tt) + .3 * np.sin(4 * np.pi * f * tt)
    return x * np.minimum(1, tt / .01) * np.exp(-tt * 2.2)
def pluck(m, d=.4):
    tt = t(d); f = mf(m + 24); return (np.sin(2 * np.pi * f * tt) + .3 * np.sin(6 * np.pi * f * tt)) * np.exp(-tt * 9)
nbeats = int(DUR / beat) + 1
for b in range(nbeats):
    at = b * beat; bar = b // 4; ch = chords[(bar // 2) % 4]
    full = at >= 20.30; mid = at >= 1.5
    if at > 35.4: break
    if b % 8 == 0: addm(pad(ch, beat * 8), at, .55)
    if mid: addm(kick(), at, .9 if full else .7)
    if mid: addm(hat(), at + beat / 2, .16); addm(hat(), at + beat * .75, .06 if full else 0)
    if full and b % 2 == 1: addm(clap(), at, .32)
    if mid and b % 2 == 0: addm(bass(ch[0], beat * 1.9), at, .45)
    if full or (mid and b % 4 == 2):
        arp = [ch[0], ch[1], ch[2], ch[1]][b % 4]; addm(pluck(arp), at + beat / 2, .10)
# tail
addm(pad(chords[0], 2.2), 35.3, .6)
mus = np.stack([lp(mus[:, 0], 14000), lp(mus[:, 1], 14000)], 1)
mus[int(36.2 * SR):] *= np.linspace(1, 0, N - int(36.2 * SR))[:, None]
sf.write('music_bus.wav', (mus / np.max(np.abs(mus)) * .7).astype(np.float32), SR)
print('ok')
