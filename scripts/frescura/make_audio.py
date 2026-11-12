# Synthesized SFX + 120 BPM minimal-luxury house bed, mixed under the studio voice.
# Usage: python make_audio.py voice_studio.wav out_dir  -> out_dir/{music.wav,sfx.wav,mix_pre.wav}
import sys, json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, sosfiltfilt

SR = 48000
VOICE, OUT = sys.argv[1], sys.argv[2]
VO_OFF = 0.35          # voice starts here in film time
TOTAL = 32.0
rng = np.random.default_rng(11)
N = int(TOTAL * SR)
t_ = lambda d: np.arange(int(d * SR)) / SR

def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype="band", fs=SR, output="sos"), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype="high", fs=SR, output="sos"), x)
def nrm(x, db=0): m = np.max(np.abs(x)) or 1; return x / m * 10 ** (db / 20)
def st(x, w=0.0):
    d = int(w * SR)
    return np.stack([x, np.roll(x, d) if d else x], 1)

# ---------------- SFX ----------------
def whoosh(d=0.6, f0=250, f1=5000, rev=False):
    n = rng.standard_normal(int(d * SR)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        p = i / len(n); p = 1 - p if rev else p
        fc = f0 * (f1 / f0) ** (np.sin(np.pi * p * 0.5) ** 1.5)
        y[i:i + seg] = sosfilt(butter(2, [fc * 0.55, min(fc * 1.7, 20000)], btype="band", fs=SR, output="sos"), n[i:i + seg])
    tt = t_(d); env = np.sin(np.pi * np.clip(tt / d, 0, 1)) ** 2
    x = y * env; L = x * (1 - tt / d * 0.7); R = x * (0.3 + tt / d * 0.7)
    return nrm(np.stack([L, R], 1))

def boom(d=1.6):
    tt = t_(d); f = 32 + 90 * np.exp(-tt * 14); ph = 2 * np.pi * np.cumsum(f) / SR
    sub = np.sin(ph) * np.exp(-tt * 2.6)
    click = hp(rng.standard_normal(len(tt)), 2000) * np.exp(-tt * 90) * 0.35
    body = lp(rng.standard_normal(len(tt)), 400) * np.exp(-tt * 9) * 0.6
    return nrm(st(np.tanh(1.6 * (sub + click + body)), 0.004))

def riser(d=1.4):
    tt = t_(d); n = rng.standard_normal(len(tt)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        fc = 400 * (12000 / 400) ** (i / len(n)); y[i:i + seg] = sosfilt(butter(2, [fc * 0.7, min(fc * 1.4, 22000)], btype="band", fs=SR, output="sos"), n[i:i + seg])
    tone = np.sin(2 * np.pi * np.cumsum(220 * 2 ** (2 * tt / d)) / SR) * 0.25
    env = (tt / d) ** 2.2
    return nrm(st((y + tone) * env, 0.009))

def bell(f, d, dec=6, parts=((1, 1), (2.0, .35), (3.01, .18), (4.2, .08))):
    tt = t_(d); x = sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-dec * m ** .5 * tt) for m, a in parts)
    return x * np.minimum(1, tt / 0.002)

def shimmer(d=1.3, n=22):
    x = np.zeros(int((d + .5) * SR))
    for k in range(n):
        o = int(rng.uniform(0, d * .85) * SR); b = bell(rng.uniform(3000, 8000), .4, dec=16, parts=((1, 1), (2.01, .25)))
        x[o:o + len(b)] += b * rng.uniform(.3, 1) * (1 - o / len(x))
    x = hp(x, 2200); return nrm(np.stack([x, np.roll(x, int(.013 * SR))], 1))

def ting():   # glass "luxury" ting
    x = bell(2093, 2.2, dec=2.2, parts=((1, 1), (2.76, .3), (5.4, .12), (8.9, .05))); y = bell(3136, 1.6, dec=3); x[:len(y)] += 0.5 * y
    return nrm(st(x, 0.011))

def tick():
    tt = t_(0.05); x = np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 160) + hp(rng.standard_normal(len(tt)), 4000) * np.exp(-tt * 300) * .5
    return nrm(st(x))

def pop(f=700):
    tt = t_(0.14); fr = f * np.exp(-tt * 25) + f * .3; x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt * 38)
    return nrm(st(x))

def bubbles(d=1.2, n=16):
    x = np.zeros((int((d + .3) * SR), 2))
    for k in range(n):
        o = int(rng.uniform(0, d) * SR); p = pop(rng.uniform(500, 1400)) * rng.uniform(.25, .8); x[o:o + len(p)] += p
    return nrm(x)

def swipe(d=0.28):
    tt = t_(d); n = hp(rng.standard_normal(len(tt)), 1500); env = np.sin(np.pi * tt / d) ** 3
    return nrm(st(bp(n, 1800, 9000) * env, 0.006))

def snap():  # text slam transient
    tt = t_(0.25); x = hp(rng.standard_normal(len(tt)), 900) * np.exp(-tt * 55) + np.sin(2 * np.pi * 90 * tt) * np.exp(-tt * 22)
    return nrm(st(np.tanh(2 * x)))

SFX = dict(whoosh=whoosh(), whoosh_l=whoosh(0.9, 150, 3000), whoosh_r=whoosh(0.5, 400, 7000, rev=True), boom=boom(),
           riser=riser(), shimmer=shimmer(), ting=ting(), tick=tick(), pop=pop(), bubbles=bubbles(), swipe=swipe(), snap=snap())

# cue sheet: (film time, sfx, gain dB). Riser cues are placed so their peak lands on the time given.
V = lambda s: s + VO_OFF
CUES = [
    (0.00, "boom", -4), (0.00, "whoosh_l", -10), (0.02, "snap", -9),
    (V(0.84), "snap", -8), (V(0.84), "boom", -9),                       # "suami tegur"
    (V(3.10), "swipe", -13), (V(4.02), "shimmer", -16),                # kebersihan / penjagaan
    (V(4.90), "whoosh", -10),                                          # -> scene 2
    (V(7.00), "pop", -12), (V(8.32), "whoosh_r", -12), (V(8.68), "snap", -10), (V(9.24), "ting", -16),
    (V(9.80), "whoosh", -10),                                          # -> scene 3 steps
    (V(10.24), "tick", -8), (V(11.94), "tick", -8), (V(12.10), "bubbles", -15), (V(14.02), "tick", -8),
    (V(14.44), "pop", -12), (V(15.55), "whoosh_l", -10),
    (V(18.08) - 1.4, "riser", -12), (V(18.08), "boom", -5), (V(18.08), "ting", -10), (V(18.3), "shimmer", -13),  # product reveal
    (V(20.12), "bubbles", -12), (V(20.80), "swipe", -12), (V(21.24), "shimmer", -17), (V(21.60), "swipe", -12),
    (V(22.90), "whoosh", -11), (V(23.80), "snap", -10), (V(24.50), "snap", -10), (V(24.55), "ting", -16),
    (V(25.30), "whoosh_l", -9), (V(25.36), "boom", -8), (V(26.96), "tick", -10),
    (V(27.95), "riser", -14), (28.45, "boom", -6), (28.45, "ting", -9), (28.6, "shimmer", -12), (30.2, "pop", -12),
]
sfx = np.zeros((N + SR * 3, 2))
for at, name, g in CUES:
    x = SFX[name] * 10 ** (g / 20); o = max(0, int(at * SR)); sfx[o:o + len(x)] += x[:len(sfx) - o]
sfx = sfx[:N]

# ---------------- MUSIC (120 BPM) ----------------
BPM = 120; B = 60 / BPM; music = np.zeros((N, 2))
def put(x, at, g=1.0):
    o = int(at * SR); x = x if x.ndim == 2 else st(x); n = min(len(x), N - o)
    if n > 0: music[o:o + n] += x[:n] * g
def kick():
    tt = t_(0.42); f = 45 + 110 * np.exp(-tt * 32); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7.5)
    return np.tanh(1.4 * x)
def hat(open_=False):
    d = .18 if open_ else .05; tt = t_(d); return hp(rng.standard_normal(len(tt)), 7500) * np.exp(-tt * (18 if open_ else 90))
def clap():
    tt = t_(0.3); n = bp(rng.standard_normal(len(tt)), 900, 5000)
    env = sum(np.exp(-np.clip(tt - k * .011, 0, None) * 140) * (tt >= k * .011) for k in range(3)) + np.exp(-tt * 18) * .5
    return n * env
def saw(f, d, det=0.0):
    tt = t_(d); return 2 * ((f * (1 + det) * tt) % 1) - 1
def pad(freqs, d):
    tt = t_(d); x = sum(saw(f, d, dd) for f in freqs for dd in (-0.004, 0.0, 0.004)) / (3 * len(freqs))
    env = np.minimum(1, tt / .35) * np.minimum(1, (d - tt) / .4); return lp(x, 1600) * env
def sub(f, d):
    tt = t_(d); return np.sin(2 * np.pi * f * tt) * np.minimum(1, tt / .01) * np.exp(-tt * 1.5)
def pluck(f, d=.35):
    tt = t_(d); return lp(saw(f, d), 3000) * np.exp(-tt * 9)

nt = lambda m: 440 * 2 ** ((m - 69) / 12)
PROG = [([62, 65, 69, 72, 76], 38), ([58, 62, 65, 69, 72], 34), ([55, 58, 62, 65, 69], 31), ([57, 61, 64, 67, 71], 33)]  # Dm9 Bbmaj9 Gm9 A7(9)
K, H, HO, C = kick(), hat(), hat(True), clap()
bars = int(TOTAL / (4 * B)) + 1
DROP = V(18.08)
for bar in range(bars):
    t0 = bar * 4 * B; chord, root = PROG[(bar // 2) % 4]
    if bar % 2 == 0: put(st(pad([nt(m) for m in chord], 8 * B), .012), t0, .55)
    for b in range(4):
        tb = t0 + b * B
        full = tb >= DROP - 0.01 or (2.0 <= tb < 16.0)
        if tb < 0.5 or (V(17.0) <= tb < DROP - 0.01): continue        # breakdown before the reveal
        put(K, tb, .9 if full else .6)
        put(H, tb + B / 2, .22); put(H, tb + B / 4 * 3, .08)
        if b in (1, 3): put(C, tb, .35)
        if b == 3 and bar % 2: put(HO, tb + B / 2, .12)
        put(sub(nt(root - 12), B * .9), tb + B / 2, .55)
    if tb >= 5:
        for k, m in enumerate([chord[2], chord[4], chord[3], chord[1]]):
            put(st(pluck(nt(m + 12)), .02), t0 + k * B + B * .75, .13)
# filter sweep intro / breakdown already shaped by arrangement; gentle master LP on music
music = np.stack([lp(music[:, 0], 9000), lp(music[:, 1], 9000)], 1)
music = nrm(music, -1)

# ---------------- MIX ----------------
v, vsr = sf.read(VOICE, dtype="float32"); assert vsr == SR
if v.ndim == 1: v = st(v)
voice = np.zeros((N, 2)); o = int(VO_OFF * SR); n = min(len(v), N - o); voice[o:o + n] = v[:n]
# sidechain ducking from the voice envelope
env = np.abs(voice[:, 0]); env = sosfiltfilt(butter(1, 6, fs=SR, output="sos"), env); env = env / (env.max() or 1)
duck = 1 - 0.55 * np.clip(env * 4, 0, 1)
music_d = music * duck[:, None] * 10 ** (-13.5 / 20)
fade = np.minimum(1, np.arange(N) / (0.05 * SR)) * np.clip((TOTAL - np.arange(N) / SR) / 1.2, 0, 1)
mix = (voice + music_d + sfx * 10 ** (-1 / 20)) * fade[:, None]
sf.write(f"{OUT}/music.wav", music_d.astype(np.float32), SR)
sf.write(f"{OUT}/sfx.wav", sfx.astype(np.float32), SR)
sf.write(f"{OUT}/mix_pre.wav", mix.astype(np.float32), SR)
json.dump(dict(vo_offset=VO_OFF, total=TOTAL, cues=[[round(a, 3), s, g] for a, s, g in CUES]), open(f"{OUT}/cues.json", "w"), indent=0)
print("ok", mix.shape[0] / SR)
