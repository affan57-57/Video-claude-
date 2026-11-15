"""Synthesize an upbeat luxury deep-house bed + a modern SFX kit (48 kHz stereo WAVs).
Usage: python synth_audio.py OUTDIR MUSIC_SECONDS"""
import sys, os, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
out = sys.argv[1]; MUS = float(sys.argv[2]); os.makedirs(out, exist_ok=True)
rng = np.random.default_rng(11)
T = lambda d: np.arange(int(d * SR)) / SR

def filt(x, f, kind, order=2):
    return sosfilt(butter(order, f, btype=kind, fs=SR, output='sos'), x, axis=0)

def norm(x, peak_db=-1.0):
    return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (peak_db / 20)

def stereo(x, width=0.0, delay_ms=9):
    d = int(delay_ms / 1000 * SR)
    r = np.concatenate([np.zeros(d), x])[:len(x)]
    return np.stack([x, (1 - width) * x + width * r], 1)

def reverb(x, secs=1.8, mix=0.25, seed=3):
    r = np.random.default_rng(seed)
    n = int(secs * SR); tt = np.arange(n) / SR
    ir = r.standard_normal((n, 2)) * np.exp(-tt * 6.9 / secs)[:, None]
    ir = filt(ir, 7000, 'low'); ir[:int(0.012 * SR)] = 0
    if x.ndim == 1: x = np.stack([x, x], 1)
    wet = np.stack([fftconvolve(x[:, c], ir[:, c])[:len(x)] for c in range(2)], 1)
    wet = wet / (np.max(np.abs(wet)) + 1e-9) * np.max(np.abs(x))
    return x * (1 - mix) + wet * mix

def pad_to(x, n):
    return np.concatenate([x, np.zeros((n - len(x),) + x.shape[1:])]) if len(x) < n else x[:n]

def w(name, x, db=-1.0):
    if x.ndim == 1: x = stereo(x)
    sf.write(f"{out}/{name}.wav", norm(x, db).astype(np.float32), SR, subtype='FLOAT')

# ---------------- SFX ----------------
def whoosh(d=0.55, lo=250, hi=5200, rev=False):
    n = rng.standard_normal(int(d * SR)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = lo + (hi - lo) * np.sin(np.pi * p) ** 2
        y[i:i + seg] = sosfilt(butter(2, [fc * .55, min(fc * 1.7, 20000)], 'band', fs=SR, output='sos'), n[i:i + seg])
    tt = T(d); env = np.sin(np.pi * tt / d) ** 1.6
    if rev: env = (tt / d) ** 3
    x = y * env; pan = tt / d
    return reverb(np.stack([x * (1 - pan * .7), x * (.3 + pan * .7)], 1), 0.9, 0.18)

def impact(d=2.2):
    tt = T(d)
    f = 38 + 90 * np.exp(-tt * 18)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.6)
    click = filt(rng.standard_normal(len(tt)), 2500, 'high') * np.exp(-tt * 60) * .5
    body = filt(rng.standard_normal(len(tt)), [80, 900], 'band') * np.exp(-tt * 9) * .8
    return reverb(sub + click + body, 2.4, 0.32)

def riser(d=1.6):
    tt = T(d); f = 300 * (12 ** (tt / d))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * .25
    noise = rng.standard_normal(len(tt)); y = np.zeros_like(noise); seg = 512
    for i in range(0, len(noise), seg):
        fc = 400 + 7000 * (i / len(noise)) ** 2
        y[i:i + seg] = sosfilt(butter(2, [fc * .6, min(fc * 1.5, 20000)], 'band', fs=SR, output='sos'), noise[i:i + seg])
    return reverb((tone + y) * (tt / d) ** 2.2, 1.2, .25)

def bell(f, d, decay=6, partials=((1, 1), (2.0, .45), (3.01, .22), (4.17, .12), (5.43, .06))):
    tt = T(d)
    return sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-decay * m ** .5 * tt) for m, a in partials) * np.minimum(1, tt / .002)

def shimmer(d=1.4, n=22):
    x = np.zeros(int((d + .6) * SR))
    for k in range(n):
        o = int((k / n) ** 1.3 * d * .8 * SR); f = 2200 * 2 ** (rng.integers(0, 14) / 12 * 1.0)
        b = bell(f, .5, 12, ((1, 1), (2.01, .3))); x[o:o + len(b)] += b * rng.uniform(.35, 1)
    return reverb(filt(x, 1500, 'high'), 1.6, .4)

def tick():   # crisp UI tick
    tt = T(.06); return filt(rng.standard_normal(len(tt)), 3000, 'high') * np.exp(-tt * 140) + np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 90) * .6

def pop():
    tt = T(.18); f = 900 * np.exp(-tt * 25) + 300
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 28)

def stamp():  # heavy rubber stamp thud
    tt = T(.6); f = 70 + 120 * np.exp(-tt * 40)
    return reverb(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 12) + filt(rng.standard_normal(len(tt)), [200, 2500], 'band') * np.exp(-tt * 45) * 1.2, .7, .15)

def ding():   # luxury two-note chime (success)
    a = bell(1567.98, 1.6, 4); b = bell(2093.0, 1.8, 4)
    x = np.zeros(int(2.0 * SR)); x[:len(a)] += a; o = int(.11 * SR); x[o:o + len(b)] += b * .9
    return reverb(x, 2.0, .35)

def glass():  # glass vitrine ting
    return reverb(bell(3135.96, 1.4, 5, ((1, 1), (2.76, .5), (5.4, .25))), 2.2, .45)

def bubbles(d=1.4, n=26):
    x = np.zeros(int((d + .2) * SR))
    for k in range(n):
        o = int(rng.uniform(0, d) * SR); tt = T(rng.uniform(.03, .07)); f0 = rng.uniform(500, 1400)
        f = f0 * (1 + 1.6 * tt / tt[-1]); b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / tt[-1])
        x[o:o + len(b)] += b * rng.uniform(.3, 1)
    return reverb(x, .5, .15)

def swipe():  # short modern swipe
    return whoosh(.28, 900, 9000)

def cash():   # checkout "ka-ching"
    x = np.zeros(int(1.5 * SR)); c = tick() * 1.2; x[:len(c)] += c
    o = int(.07 * SR); b = bell(2637, 1.2, 5) + bell(3520, 1.2, 6) * .7; x[o:o + len(b)] += b
    return reverb(x, 1.4, .3)

w('whoosh', whoosh()); w('whoosh_long', whoosh(.9, 150, 4000)); w('swipe', swipe())
w('impact', impact()); w('riser', riser()); w('shimmer', shimmer())
w('tick', tick(), -3); w('pop', pop(), -3); w('stamp', stamp()); w('ding', ding())
w('glass', glass()); w('bubbles', bubbles()); w('cash', cash()); w('rev_whoosh', whoosh(.8, 200, 6000, True))

# ---------------- MUSIC: 122 BPM luxe deep-house bed ----------------
BPM = 122; beat = 60 / BPM; N = int(MUS * SR); mix = np.zeros((N, 2))
def place(x, t, g=1.0):
    if x.ndim == 1: x = stereo(x)
    i = int(t * SR)
    if i >= N: return
    seg = x[:N - i]; mix[i:i + len(seg)] += seg * g

def kick():
    tt = T(.45); f = 48 + 110 * np.exp(-tt * 32)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7) + filt(rng.standard_normal(len(tt)), 3000, 'high') * np.exp(-tt * 300) * .15
def hat(open_=False):
    tt = T(.25 if open_ else .05)
    return filt(rng.standard_normal(len(tt)), 7500, 'high') * np.exp(-tt * (18 if open_ else 110))
def clap():
    tt = T(.3); n = filt(rng.standard_normal(len(tt)), [900, 6000], 'band')
    env = sum(np.exp(-np.maximum(tt - o, 0) * 60) * (tt >= o) for o in (0, .011, .022)) * np.exp(-tt * 9)
    return reverb(n * env, .8, .25)
def saw(f, d):
    tt = T(d); ph = (f * tt) % 1; return 2 * ph - 1
def note(m): return 440 * 2 ** ((m - 69) / 12)

KK, HH, OH, CL = kick(), hat(), hat(True), clap()
prog = [(57, [57, 60, 64, 67]), (53, [53, 57, 60, 64]), (48, [55, 60, 64, 67]), (55, [55, 59, 62, 67])]  # Am9 Fmaj7 C/G G
bars = int(MUS / (4 * beat)) + 1
for b in range(bars):
    t0 = b * 4 * beat; root, chord = prog[b % 4]
    intro = b < 1
    for k in range(4):
        tb = t0 + k * beat
        if not intro: place(KK, tb, .9)
        place(HH, tb + beat / 2, .22 if not intro else .12); place(OH, tb + beat / 2, .10)
        place(HH, tb + beat / 4, .06); place(HH, tb + 3 * beat / 4, .06)
        if k in (1, 3) and not intro: place(CL, tb, .32)
    # sub bass: offbeat pulses
    for k in range(8):
        if intro: break
        tb = t0 + k * beat / 2
        if k % 2 == 1 or k == 0:
            d = beat / 2 * .9; tt = T(d); f = note(root - 12)
            bs = np.sin(2 * np.pi * f * tt) + .3 * np.sin(2 * np.pi * 2 * f * tt)
            place(bs * np.minimum(1, tt / .005) * np.exp(-tt * 3), tb, .42)
    # pad chord (filtered saws), whole bar
    d = 4 * beat; tt = T(d); pad = sum(saw(note(m) * (1 + dt), d) for m in chord for dt in (-.003, .003))
    pad = filt(pad, 1400, 'low') * np.minimum(1, tt / .25) * np.minimum(1, (d - tt) / .3)
    place(stereo(pad, .8, 13), t0, .045)
    # pluck arp (16ths), sparkle on top
    arp = [chord[i % 4] + 12 * (i // 4 % 2) for i in (0, 1, 2, 3, 2, 1, 4, 3)]
    for k, m in enumerate(arp):
        tt = T(.22); f = note(m + 12)
        pl = (np.sin(2 * np.pi * f * tt) + .4 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-tt * 16)
        place(stereo(pl, .9, 4 + 8 * (k % 2)), t0 + k * beat / 2, .07)
mix = reverb(mix, 1.2, .12)
mix = filt(mix, 30, 'high')
# gentle fade-in/out
L = len(mix); tt = np.arange(L) / SR
mix *= np.minimum(1, tt / .4)[:, None] * np.minimum(1, (MUS - tt) / 1.8)[:, None]
sf.write(f"{out}/music.wav", norm(mix, -1).astype(np.float32), SR, subtype='FLOAT')
print('ok', MUS)
