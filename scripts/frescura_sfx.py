# Synthesized SFX + music bed for the FRESCURA BODY ad (no third-party samples).
# Usage: python frescura_sfx.py OUT_DIR [music_seconds]
import sys, os, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
MUSIC_S = float(sys.argv[2]) if len(sys.argv) > 2 else 36.0
rng = np.random.default_rng(11)
T = lambda d: np.arange(int(d * SR)) / SR

def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x, axis=0)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x, axis=0)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x, axis=0)
def norm(x, db=-1.0): return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)
def stereo(x, w=0.0):
    if x.ndim == 2: return x
    d = int(w * SR); r = np.concatenate([np.zeros(d), x])[:len(x)] if d else x
    return np.stack([x, r], 1)
def reverb(x, dur=1.6, mix=0.25, damp=3500):
    n = int(dur * SR); ir = rng.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR * 4.5)[:, None]
    ir = lp(ir, damp); ir /= np.sqrt((ir ** 2).sum(0))
    x = stereo(x); wet = np.stack([fftconvolve(x[:, c], ir[:, c])[:len(x)] for c in range(2)], 1)
    return x * (1 - mix) + wet * mix
def pad_to(x, d):
    n = int(d * SR); x = stereo(x)
    return np.concatenate([x, np.zeros((max(0, n - len(x)), 2))])[:n]
def bell(f, d, parts=((1, 1), (2.0, .35), (3.01, .18), (4.2, .08)), dec=6):
    t = T(d); x = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-dec * m ** .5 * t) for m, a in parts)
    return x * np.minimum(1, t / 0.002)

def sub_hit(d=1.8):                       # cinematic low impact for the hook
    t = T(d); f = 38 + 90 * np.exp(-t * 18); ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 2.6)
    click = hp(rng.standard_normal(len(t)), 2000) * np.exp(-t * 160) * 0.5
    air = bp(rng.standard_normal(len(t)), 300, 3000) * np.exp(-t * 7) * 0.25
    return reverb(np.tanh(1.6 * (body + click + air)), 2.2, 0.2)

def riser(d=1.4):                         # noise + tone sweep up into a cut
    t = T(d); p = t / d; n = rng.standard_normal(len(t)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        fc = 400 + 6000 * (i / len(n)) ** 2
        y[i:i + seg] = sosfilt(butter(2, [fc * .7, fc * 1.4], 'band', fs=SR, output='sos'), n[i:i + seg])
    tone = np.sin(2 * np.pi * np.cumsum(220 + 660 * p ** 2) / SR) * 0.25
    return reverb((y * 0.8 + tone) * p ** 2.2, 1.2, 0.3)

def whoosh(d=0.55, lo=250, hi=5200):      # swept band noise, panned L->R
    t = T(d); n = rng.standard_normal(len(t)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); fc = lo + (hi - lo) * np.sin(np.pi * p) ** 2
        y[i:i + seg] = sosfilt(butter(2, [fc * .6, fc * 1.6], 'band', fs=SR, output='sos'), n[i:i + seg])
    env = np.sin(np.pi * np.minimum(1, t / d)) ** 2.5
    x = y * env; p = t / d
    return reverb(np.stack([x * (1.2 - p), x * (0.2 + p)], 1), 0.9, 0.18)

def tick():                                # glassy UI tick for text reveals
    x = bell(3520, 0.25, ((1, 1), (2.76, .3)), dec=26) + hp(rng.standard_normal(int(.25 * SR)), 5000) * np.exp(-T(.25) * 400) * .4
    return reverb(x, 0.6, 0.15)

def pop(f0=1100):                          # bubble pop (foam)
    t = T(0.14); f = f0 * np.exp(-t * 28) + 220; x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 38)
    return reverb(x, 0.5, 0.12)

def bubbles(d=1.4, n=18):
    x = np.zeros(int(d * SR) + SR // 4)
    for k in range(n):
        o = int(rng.uniform(0, d * .9) * SR); f0 = rng.uniform(700, 2200); p = pop(f0)[:, 0]
        x[o:o + len(p)] += p * rng.uniform(.3, 1)
    return reverb(x, 0.7, 0.2)

def shimmer(d=1.6, n=22):                  # luxury sparkle
    x = np.zeros(int(d * SR) + SR)
    for k in range(n):
        o = int(rng.uniform(0, d * .75) * SR); f = rng.choice([2093, 2637, 3136, 3520, 4186]) * rng.uniform(.995, 1.005)
        b = bell(f, 0.6, ((1, 1), (2.01, .25)), dec=9); x[o:o + len(b)] += b * rng.uniform(.3, 1)
    return reverb(hp(x, 1500), 2.0, 0.4)

def tap():                                 # soft button tap
    t = T(0.09); x = np.sin(2 * np.pi * np.cumsum(1800 * np.exp(-t * 60) + 500) / SR) * np.exp(-t * 70)
    return stereo(x + lp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 300) * 0.3)

def kaching():                             # checkout chime
    x = np.zeros(int(1.6 * SR))
    for i, f in enumerate([2093, 2637, 3136]):
        b = bell(f, 1.3, dec=4); o = int(i * .05 * SR); x[o:o + len(b)] += b * (1 - i * .15)
    x[:int(.06 * SR)] += hp(rng.standard_normal(int(.06 * SR)), 3000) * np.exp(-T(.06) * 80) * .6
    return reverb(x, 1.5, 0.3)

def alert():                               # 'stok terhad' double pulse
    x = np.zeros(int(0.8 * SR))
    for o in (0, .16):
        b = bell(880, .4, ((1, 1), (2, .5), (3, .2)), dec=10); i = int(o * SR); x[i:i + len(b)] += b
    return reverb(x, 0.8, 0.2)

def sting(d=3.0):                          # logo end sting
    t = T(d); x = sub_hit(d)[:, 0] * 0.8
    for f in [523.25, 659.25, 783.99, 1046.5]:
        x += bell(f, d, dec=1.6) * .35
    return reverb(x, 2.8, 0.35)

def tape_stop(d=0.45):                     # quick reverse swell before cut
    t = T(d); x = bp(rng.standard_normal(len(t)), 500, 8000) * (t / d) ** 3
    return reverb(x, 0.5, 0.2)

sfx = dict(sub_hit=sub_hit, riser=riser, whoosh=whoosh, whoosh_fast=lambda: whoosh(0.32, 600, 7000),
           tick=tick, pop=pop, bubbles=bubbles, shimmer=shimmer, tap=tap, kaching=kaching, alert=alert,
           sting=sting, swell=tape_stop)
for k, fn in sfx.items():
    y = stereo(fn()); sf.write(f"{out}/{k}.wav", norm(y).astype(np.float32), SR); print(k, round(len(y) / SR, 2))

# ---- music bed: 118 BPM minimal luxe house (pad chords, plucked bass, soft kick, offbeat hats) ----
BPM = 118; beat = 60 / BPM; N = int(MUSIC_S * SR); mix = np.zeros((N, 2))
def place(buf, x, t0, g=1.0):
    i = int(t0 * SR); x = stereo(x)
    if i >= N: return
    j = min(N, i + len(x)); buf[i:j] += x[:j - i] * g
def kick():
    t = T(0.45); f = 48 + 110 * np.exp(-t * 30)
    return np.tanh(2 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7))
def hat(): t = T(0.07); return hp(rng.standard_normal(len(t)), 7000) * np.exp(-t * 70)
def clap():
    t = T(0.25); n = bp(rng.standard_normal(len(t)), 900, 5000)
    env = sum(np.exp(-np.maximum(0, t - o) * 60) * (t >= o) for o in (0, .012, .024)) / 3
    return reverb(n * env, 0.9, 0.35)
def note(f, d, kind='pad'):
    t = T(d)
    if kind == 'pad':
        x = sum(np.sin(2 * np.pi * f * dt * t + k) for k, dt in enumerate([1, 1.004, .996, 2.002])) / 4
        return lp(x * np.minimum(1, t / .35) * np.minimum(1, (d - t) / .5), 2200)
    if kind == 'bass':
        x = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + np.sin(2 * np.pi * f * t)
        return lp(x * np.exp(-t * 5), 600)
    x = bell(f, d, ((1, 1), (2, .3), (3, .1)), dec=7)   # pluck
    return x
m2f = lambda m: 440 * 2 ** ((m - 69) / 12)
prog = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 64]]  # Am7 Fmaj7 Cmaj7 G6
bar = 4 * beat; nb = int(MUSIC_S / bar) + 1
pads = np.zeros((N, 2)); drums = np.zeros((N, 2)); bass = np.zeros((N, 2)); arp = np.zeros((N, 2))
for b in range(nb):
    ch = prog[b % 4]; t0 = b * bar
    for m in ch: place(pads, note(m2f(m), bar + .4), t0, .16)
    for s in range(4):
        tb = t0 + s * beat
        if b >= 1: place(drums, kick(), tb, .55)
        place(drums, hat(), tb + beat / 2, .16)
        if s in (1, 3) and b >= 1: place(drums, clap(), tb, .22)
        place(bass, note(m2f(ch[0] - 12), beat * .9, 'bass'), tb + beat / 2, .28)
    for k in range(8):
        place(arp, note(m2f(ch[k % 4] + 12 + (12 if k % 3 == 0 else 0)), .5, 'pluck'), t0 + k * beat / 2, .07)
mix = pads + drums + bass + reverb(arp, 1.4, 0.45)
mix = np.tanh(mix * 1.2) * 0.8
fade = np.minimum(1, np.arange(N) / (0.4 * SR)); mix *= fade[:, None]
sf.write(f"{out}/music.wav", norm(mix, -1).astype(np.float32), SR); print("music", MUSIC_S)
