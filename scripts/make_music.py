"""Original minimal-luxury deep-house bed, 120 BPM, written for the Frescura Body awareness cut.

Downbeats land every 2 s from OFFSET (0.5, 2.5 ... ) so the drop hits at 16.5 s and the urgency
section at 28.5 s. Sections: intro (0-7, filtered, under the hook voice), break (7-16.5, no drums,
under the customer feedback), drop (16.5-28.5, the foam demo), drive (28.5-36.5, urgency + CTA,
ticking 16ths), outro (36.5-end, last chord rings out).
Usage: python make_music.py out.wav [duration_s]
"""
import sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 40.0
BPM = 120.0
BEAT = 60 / BPM
OFFSET = 0.5                    # first downbeat (bar line) in film time
BREAK = 7.0                     # customer feedback: drums out, keys + pad only
DROP, DRIVE, OUTRO = 16.5, 28.5, 36.5
rng = np.random.default_rng(11)
N = int(DUR * SR)

def T(d): return np.arange(int(d * SR)) / SR
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x, axis=0)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x, axis=0)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x, axis=0)
def place(buf, x, t, gain=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= len(buf) or i + len(x) <= 0: return
    if i < 0: x = x[-i:]; i = 0
    x = x[: len(buf) - i]
    if x.ndim == 1:
        buf[i:i + len(x), 0] += x * gain * np.sqrt((1 - pan) / 2) * 1.414
        buf[i:i + len(x), 1] += x * gain * np.sqrt((1 + pan) / 2) * 1.414
    else:
        buf[i:i + len(x)] += x * gain
def midi(n): return 440 * 2 ** ((n - 69) / 12)

# ---------- instruments ----------
def kick():
    t = T(0.45); f = 48 + 110 * np.exp(-t * 28)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5)
    click = hp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 400) * 0.25
    return np.tanh((x + click) * 1.6) * 0.9
def clap():
    t = T(0.35); n = rng.standard_normal(len(t)); env = np.zeros(len(t))
    for k, o in enumerate([0, 0.011, 0.022]):
        i = int(o * SR); env[i:] += np.exp(-(t[: len(t) - i]) * (180 if k < 2 else 22))
    return bp(n * env, 900, 3800) * 0.8
def hat(open_=False):
    d = 0.22 if open_ else 0.05; t = T(d)
    x = hp(rng.standard_normal(len(t)), 7500, 4) * np.exp(-t * (18 if open_ else 90))
    return x * (0.5 if open_ else 0.42)
def shaker():
    t = T(0.08); return bp(rng.standard_normal(len(t)), 5000, 11000) * np.sin(np.pi * t / 0.08) ** 2 * 0.3
def bass(note, d):
    t = T(d); f = midi(note)
    x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t) + 0.08 * np.sin(6 * np.pi * f * t)
    env = np.minimum(1, t / 0.006) * np.exp(-t * 3.2)
    return np.tanh(x * env * 1.4) * 0.55
def keys(notes, d):
    """Rhodes-like FM electric piano chord."""
    t = T(d); y = np.zeros(len(t))
    for n in notes:
        f = midi(n); idx = 1.6 * np.exp(-t * 6)
        y += np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t)) * np.exp(-t * 2.4)
        y += 0.18 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 5)
    y *= np.minimum(1, t / 0.004)
    return lp(y / len(notes), 4200) * 0.6
def pad(notes, d):
    t = T(d); y = np.zeros(len(t))
    for n in notes:
        for det in (-0.07, 0.0, 0.06):
            f = midi(n) * 2 ** (det / 12); ph = rng.uniform(0, 1)
            y += 2 * ((f * t + ph) % 1) - 1
    env = np.minimum(1, t / 0.35) * np.minimum(1, (d - t) / 0.4)
    return lp(y * env / (3 * len(notes)), 1600) * 0.35
def pluck(note, d=0.35):
    t = T(d); f = midi(note)
    x = (2 * ((f * t) % 1) - 1) * np.exp(-t * 11) + 0.4 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 14)
    return lp(x, 3000) * 0.28

# Am9 - Fmaj9 - Dm9 - Esus4/7 (one bar each)
CHORDS = [[57, 60, 64, 67, 71], [53, 57, 60, 64, 67], [50, 53, 57, 60, 64], [52, 57, 59, 62, 64]]
ROOTS = [45, 41, 38, 40]
ARP = [[69, 72, 76, 79], [65, 69, 72, 76], [62, 65, 69, 72], [64, 69, 71, 74]]

drums = np.zeros((N, 2)); bassb = np.zeros((N, 2)); music = np.zeros((N, 2)); padb = np.zeros((N, 2))
side = np.ones(N)  # kick sidechain gain

bar0 = OFFSET - 4 * BEAT * 1  # one pickup bar before the first bar line
nbars = int((DUR - bar0) / (4 * BEAT)) + 1
for b in range(nbars):
    t0 = bar0 + b * 4 * BEAT
    ci = b % 4
    sec = 'intro' if t0 < BREAK - 1e-6 else 'break' if t0 < DROP - 1e-6 else 'drop' if t0 < DRIVE - 1e-6 else 'drive' if t0 < OUTRO - 1e-6 else 'outro'
    for q in range(4):
        tb = t0 + q * BEAT
        if tb < 0 or tb >= DUR: continue
        if sec in ('drop', 'drive') or (sec == 'intro' and tb >= OFFSET):
            g = 0.75 if sec == 'intro' else 1.0
            place(drums, kick(), tb, g)
            i = int(tb * SR); L = int(0.22 * SR)
            if i < N:
                e = 1 - 0.65 * np.exp(-np.arange(min(L, N - i)) / SR * 14)
                side[i:i + len(e)] = np.minimum(side[i:i + len(e)], e)
        if sec in ('drop', 'drive') and q in (1, 3):
            place(drums, clap(), tb, 0.55, 0.05)
        if sec not in ('outro', 'break'):
            place(drums, hat(open_=sec in ('drop', 'drive')), tb + BEAT / 2, 0.8 if sec != 'intro' else 0.5, 0.25)
        if sec == 'drive':
            for s16 in range(4):
                place(drums, shaker(), tb + s16 * BEAT / 4, 0.55 + 0.25 * (s16 % 2), -0.3)
        elif sec == 'drop':
            place(drums, shaker(), tb + BEAT * 0.25, 0.4, -0.3); place(drums, shaker(), tb + BEAT * 0.75, 0.5, -0.3)
        # offbeat bass
        if sec not in ('outro', 'break') and tb >= OFFSET:
            place(bassb, bass(ROOTS[ci], BEAT * 0.45), tb + BEAT / 2, 0.8 if sec == 'intro' else 1.0)
    # keys: stab on 1 and the "and" of 2
    if sec == 'break':
        place(music, keys(CHORDS[ci], 2.0), t0, 0.6, -0.1)
        place(music, pluck(ARP[ci][0] + 12), t0 + 2 * BEAT, 0.5, 0.4)
    elif sec != 'outro':
        place(music, keys(CHORDS[ci], 1.2), t0, 0.9, -0.1)
        place(music, keys(CHORDS[ci], 0.8), t0 + 1.5 * BEAT, 0.55, 0.1)
    else:
        place(music, keys(CHORDS[0], 3.5), t0, 1.0)
    if t0 >= -1:
        place(padb, pad(CHORDS[ci], 4 * BEAT + 0.4), max(t0, 0), 1.0)
    if sec in ('drop', 'drive'):
        for k in range(8):
            place(music, pluck(ARP[ci][k % 4] + (12 if k >= 4 and sec == 'drive' else 0)), t0 + k * BEAT / 2 + BEAT / 4, 0.55, (-0.5, 0.5)[k % 2])

# intro high-pass/low-pass shaping: filter opens into the drop
cut = np.clip((np.arange(N) / SR) / BREAK, 0, 1)
music_lp = lp(music, 1400); music = music_lp * (1 - cut[:, None] ** 3) + music * (cut[:, None] ** 3)
pad_mix = padb * side[:, None]
bus = drums * 0.9 + bassb * side[:, None] * 0.95 + music * side[:, None] * 0.9 + pad_mix * 0.9

# riser into the drop (filtered noise sweep) and reverse cymbal into the drive
def riser(d):
    t = T(d); n = rng.standard_normal(len(t)); y = np.zeros(len(t)); seg = 1024
    for i in range(0, len(t), seg):
        p = i / len(t); fc = 400 + 7000 * p ** 2
        y[i:i + seg] = sosfilt(butter(2, [fc * 0.7, min(fc * 1.4, 20000)], 'band', fs=SR, output='sos'), n[i:i + seg])
    return y * (t / d) ** 2 * 0.5
place(bus, riser(2.0), DROP - 2.0, 0.7)
place(bus, riser(1.0), DRIVE - 1.0, 0.5)

# reverb send
ir_t = T(1.6); ir = rng.standard_normal((len(ir_t), 2)) * np.exp(-ir_t * 4.2)[:, None]
ir = lp(ir, 6000); ir /= np.sqrt((ir ** 2).sum(0))
wet = np.stack([fftconvolve(music[:, c] + pad_mix[:, c] * 0.5, ir[:, c])[:N] for c in range(2)], 1)
bus = bus + wet * 0.35

# outro fade + master
t = np.arange(N) / SR
bus *= np.clip((DUR - t) / 2.2, 0, 1)[:, None]
bus *= np.minimum(1, t / 0.02)[:, None]
bus = np.tanh(bus * 1.3) / np.tanh(1.3)
bus /= np.max(np.abs(bus)) / 0.89
sf.write(sys.argv[1], bus.astype(np.float32), SR, subtype='FLOAT')
print('music', DUR, 's')
