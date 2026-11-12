import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, sosfiltfilt
SR = 48000; TOTAL = 39.6; N = int(TOTAL * SR)
rng = np.random.default_rng(11)
def t(d): return np.arange(int(d * SR)) / SR
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x, axis=0)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x, axis=0)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x, axis=0)
def nrm(x): return x / (np.max(np.abs(x)) + 1e-9)
def st(x, w=0.0):
    if x.ndim == 2: return x
    d = int(0.0007 * SR * w * 10)
    return np.stack([x, np.roll(x, d)], 1)

# ---------------- SFX library ----------------
def whoosh(d=0.6, f0=300, f1=4000, rev=False):
    n = rng.standard_normal(int(d * SR)); y = np.zeros_like(n); seg = 512; L = len(n)
    for i in range(0, L, seg):
        p = i / L; p = 1 - p if rev else p
        fc = f0 + (f1 - f0) * np.sin(np.pi * p * 0.5) ** 2 if not rev else f0 + (f1 - f0) * p
        fc = min(fc, 18000)
        y[i:i + seg] = sosfilt(butter(2, [fc * .5, min(fc * 1.8, 23000)], 'band', fs=SR, output='sos'), n[i:i + seg])
    tt = t(d); env = (tt / d) ** 1.5 * np.exp(-((tt / d) - 0.7) ** 2 * 0) ; env = np.sin(np.pi * tt / d) ** 1.2
    x = nrm(y * env); pan = np.linspace(-.7, .7, len(x))
    return np.stack([x * (1 - pan) ** .5, x * (1 + pan) ** .5], 1)
def boom(d=1.6, f=48):
    tt = t(d); fr = f + 90 * np.exp(-tt * 18); ph = 2 * np.pi * np.cumsum(fr) / SR
    sub = np.sin(ph) * np.exp(-tt * 2.6)
    cl = lp(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 40) * .6
    x = np.tanh(2.2 * (sub + cl)); return st(nrm(x))
def impact_lux(d=2.5):
    b = boom(d, 42); sh = shimmer(d, 30)
    L = max(len(b), len(sh)); o = np.zeros((L, 2)); o[:len(b)] += b; o[:len(sh)] += sh * .45; return nrm(o)
def bell(f, d, dec=5, parts=((1, 1), (2.01, .35), (3.03, .15), (4.2, .08))):
    tt = t(d); x = sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-dec * m ** .5 * tt) for m, a in parts)
    return x * np.minimum(1, tt / .002)
def shimmer(d=1.2, n=22):
    x = np.zeros(int(d * SR) + SR)
    for k in range(n):
        o = int(rng.uniform(0, d * .7) * SR); f = rng.uniform(2500, 7500)
        b = bell(f, .5, 12, ((1, 1), (2.01, .3))); x[o:o + len(b)] += b * rng.uniform(.3, 1) * (1 - o / len(x))
    x = hp(x, 1800); return nrm(np.stack([x, np.roll(x, int(.013 * SR))], 1))
def tick(f=2200):
    tt = t(.05); x = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 140) + lp(rng.standard_normal(len(tt)), 6000) * np.exp(-tt * 300) * .4
    return st(nrm(x))
def ding(f=1568): return st(nrm(bell(f, 1.0, 5) + .6 * bell(f * 1.5, 1.0, 6)))
def pop(f0=900, f1=200):
    tt = t(.14); fr = f1 + (f0 - f1) * np.exp(-tt * 35); x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt * 38); return st(nrm(x))
def bubbles(d=0.8, n=12):
    x = np.zeros(int(d * SR) + SR // 4)
    for k in range(n):
        o = int(rng.uniform(0, d) * SR); f = rng.uniform(500, 1400); tt = t(.06)
        fr = f * (1 + 2.5 * tt / .06); b = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * tt / .06)
        x[o:o + len(b)] += b * rng.uniform(.4, 1)
    sq = bp(rng.standard_normal(len(x)), 300, 2500) * .25 * np.exp(-np.arange(len(x)) / SR * 3)
    return st(nrm(x + sq), .5)
def shutter():
    x = np.zeros(int(.25 * SR))
    for o, g in [(0, 1), (int(.07 * SR), .7)]:
        tt = t(.05); c = hp(rng.standard_normal(len(tt)), 1500) * np.exp(-tt * 120); x[o:o + len(c)] += c * g
    return st(nrm(x))
def riser(d=1.0):
    tt = t(d); n = rng.standard_normal(len(tt)); y = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        fc = 400 + 7000 * (i / len(n)) ** 2
        y[i:i + seg] = sosfilt(butter(2, [fc * .7, fc * 1.4], 'band', fs=SR, output='sos'), n[i:i + seg])
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * (tt / d) ** 2) / SR) * .25
    x = (y + tone) * (tt / d) ** 2; return st(nrm(x), .6)
def down_tone(d=.6):
    tt = t(d); fr = 900 * np.exp(-tt * 3) + 120; x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * tt / d); return st(nrm(x))
def drone(d=1.8):
    tt = t(d); x = sum(np.sin(2 * np.pi * f * tt) for f in (110, 110.7, 164.8, 220.4)) * np.minimum(1, tt / .3) * np.minimum(1, (d - tt) / .3)
    return st(nrm(lp(x, 900)), .5)
def blip(f=880): tt = t(.09); return st(nrm(np.sign(np.sin(2 * np.pi * f * tt)) * .4 * np.exp(-tt * 30)))
def cash():
    x = np.zeros(int(1.2 * SR)); a = bell(2637, 1.0, 6); b = bell(3520, 1.0, 6); x[:len(a)] += a; x[int(.08 * SR):int(.08 * SR) + len(b)] += b
    c = hp(rng.standard_normal(int(.08 * SR)), 2000) * np.exp(-np.arange(int(.08 * SR)) / SR * 60); x[:len(c)] += c * .5
    return st(nrm(x))
def swipe(d=.35): return whoosh(d, 1200, 9000)
def strike(d=.45):
    tt = t(d); n = bp(rng.standard_normal(len(tt)), 2500, 9000) * np.sin(np.pi * tt / d) ** .5; return st(nrm(n))

E = []  # (time, sound, dB)
def add(tm, snd, db): E.append((tm, snd, db))
# HOOK
add(0.0, lp(boom(2.0, 40), 400), -6); add(0.24, whoosh(.5, 200, 6000), -22)
add(0.72, swipe(.4), -18); add(1.22, down_tone(.6), -17); add(1.78, whoosh(.4), -20)
add(2.72, strike(), -16); add(3.0, whoosh(.5, 3000, 300, rev=True), -15)
add(3.25, pop(), -12); add(3.35, pop(1100, 260), -12); add(4.15, drone(1.7), -20); add(5.33, boom(1.2, 55), -11); add(5.35, shimmer(.8, 10), -22)
# EDU
add(6.10, whoosh(.5), -14); add(7.68, boom(.8, 70), -16)
for k, tm in enumerate([8.35, 9.55, 10.46]):
    add(tm, swipe(.35), -18); add(tm + .35, ding(1568 * 2 ** (k * 4 / 12)), -17)
# RING
add(11.1, whoosh(.5), -14); add(11.3, shimmer(1.4, 26), -21); add(12.85, swipe(.35), -19)
for k in range(10): add(14.15 + k * .12, tick(1800 + k * 80), -19)
add(15.28, ding(2093), -20)
# SELF
add(15.75, whoosh(.5, 400, 5000), -14); add(16.15, shimmer(1.0, 18), -20); add(16.58, pop(700, 180), -18)
# BROLL
add(17.4, swipe(.45), -15); add(17.7, bubbles(.9, 10), -20); add(19.82, swipe(.45), -15); add(20.1, bubbles(1.4, 16), -21)
# MALL
add(21.25, riser(1.0), -14); add(22.25, impact_lux(), -6); add(22.80, shimmer(1.5, 30), -15); add(22.8, whoosh(.6, 300, 5000), -18)
# FEATURES
add(24.25, bubbles(.7, 14), -14); add(24.3, pop(), -16)
add(25.2, swipe(.35), -16); add(25.3, shimmer(.7, 20), -16)
add(25.94, swipe(.35), -16); add(26.0, ding(1318.5), -20)
add(26.76, whoosh(.45), -15)
for k, tm in enumerate([26.96, 27.11, 27.26]): add(tm, pop(800 + k * 200, 220), -13)
add(27.38, boom(.9, 60), -12); add(27.7, whoosh(.5, 4000, 400, rev=True), -18)
# HEROES
add(28.18, whoosh(.45, 200, 7000), -13); add(28.24, boom(1.2, 45), -9); add(28.3, shimmer(.8, 14), -19)
add(29.05, whoosh(.45, 200, 7000), -13); add(29.10, boom(1.2, 50), -10); add(29.2, shimmer(1.2, 30), -15)
# RUGI
add(30.45, shutter(), -12); add(31.31, shutter(), -12)
for k in range(4): add(31.55 + k * .22, ding(1760 + k * 220), -21)
# TANGGUH
for k in range(7): add(32.69 + k * .2, tick(2600 if k % 2 else 2000), -15)
add(33.0, boom(1.0, 55), -10)
# CTA
add(34.05, whoosh(.4), -15); add(34.10, pop(1200, 300), -9); add(34.75, tick(3000), -12); add(34.8, pop(600, 150), -13)
add(34.85, cash(), -14); add(35.42, swipe(.3), -18)
for k in range(8): add(35.7 + k * .2, blip(1200 - k * 70), -24)
add(36.69, blip(1500), -20); add(36.93, blip(1500), -20)
# END
add(37.45, riser(.25), -16); add(37.67, impact_lux(), -6); add(38.1, shimmer(1.4, 30), -14)

sfx = np.zeros((N, 2))
for tm, snd, db in E:
    o = int(tm * SR); s = snd[:max(0, N - o)] * 10 ** (db / 20); sfx[o:o + len(s)] += s

# ---------------- MUSIC (122 bpm luxury deep house) ----------------
BPM = 122; beat = 60 / BPM; bar = 4 * beat
mus = np.zeros((N, 2))
def place(buf, tm, x, g=1.0):
    o = int(tm * SR)
    if o >= N: return
    x = x[:N - o]; buf[o:o + len(x)] += (st(x) if x.ndim == 1 else x) * g
def kick():
    tt = t(.45); fr = 45 + 120 * np.exp(-tt * 30); return np.tanh(1.8 * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt * 6.5))
def hat(o=False):
    d = .22 if o else .05; tt = t(d); return hp(rng.standard_normal(len(tt)), 8000) * np.exp(-tt * (18 if o else 90))
def clap():
    tt = t(.25); n = bp(rng.standard_normal(len(tt)), 900, 5000)
    env = sum(np.exp(-np.maximum(tt - k * .011, 0) * 60) * (tt >= k * .011) for k in range(3)) * np.exp(-tt * 9)
    return n * env
def saw(f, tt): return 2 * ((f * tt) % 1) - 1
chords = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 64]]  # Am7 Fmaj7 Cmaj7 G6
bassn = [45, 41, 36, 43]
mf = lambda m: 440 * 2 ** ((m - 69) / 12)
K, H, OH, C = kick(), hat(), hat(True), clap()
nb = int(TOTAL / beat) + 2
for b in range(nb):
    tm = b * beat
    intro = tm < 0.2
    if tm > TOTAL: break
    place(mus, tm, K, .9)
    place(mus, tm + beat / 2, OH, .16)
    for q in (0.25, 0.75): place(mus, tm + q * beat, H, .10)
    if b % 2 == 1: place(mus, tm, C, .28)
for bi in range(int(TOTAL / bar) + 1):
    tm = bi * bar; ch = chords[bi % 4]; tt = t(bar)
    pad = sum(saw(mf(m) * (1 + dt), tt) for m in ch for dt in (-0.003, 0.003)) / 8
    pad = lp(pad, 1400) * np.minimum(1, tt / .4) * np.minimum(1, (bar - tt) / .3)
    padst = np.stack([pad, np.roll(pad, int(.012 * SR))], 1)
    place(mus, tm, padst, .30)
    # offbeat bass
    for k in range(8):
        bt = t(beat / 2 * .9); f = mf(bassn[bi % 4]) * (2 if k % 4 == 3 else 1)
        bs = lp(np.sin(2 * np.pi * f * bt) + .3 * saw(f, bt), 600) * np.exp(-bt * 6)
        place(mus, tm + k * beat / 2 + beat / 4, bs, .40)
    # pluck arp
    arp = ch + [ch[1] + 12, ch[2] + 12]
    for k in range(16):
        if k % 3 == 2: continue
        n = arp[(k * 3) % len(arp)] + 12; pt = t(.3)
        pl = lp(saw(mf(n), pt), 3500) * np.exp(-pt * 14)
        pan = .4 if k % 2 else -.4
        place(mus, tm + k * beat / 4, np.stack([pl * (1 - pan), pl * (1 + pan)], 1), .07)
# music intro filter sweep 0-1.5s & outro fade
mus = hp(mus, 35)
env = np.ones(N); tt = np.arange(N) / SR
env *= np.clip((tt - 0.15) / 0.6, 0.25, 1)
env *= np.clip((TOTAL - tt) / 1.6, 0, 1)
# drop: music cut briefly before mall impact & end
for a, b in [(21.95, 22.25), (37.4, 37.67)]:
    env[(tt > a) & (tt < b)] *= 0.15
mus *= env[:, None]

# ---------------- VOICE + ducking ----------------
v, vsr = sf.read('/home/user/work/voice_studio.wav'); assert vsr == SR
if v.ndim == 2: v = v.mean(1)
voice = np.zeros(N); voice[:len(v)] = v[:N]
w = int(.03 * SR); rms = np.sqrt(np.convolve(voice ** 2, np.ones(w) / w, 'same'))
act = (rms > 0.02).astype(float)
k = int(.25 * SR); act = np.convolve(act, np.ones(k) / k, 'same').clip(0, 1)
duck = 1 - 0.55 * act
mus_l = 10 ** (-17 / 20)
mix = np.stack([voice, voice], 1) * 1.0 + mus * mus_l * duck[:, None] / (np.max(np.abs(mus)) + 1e-9) + sfx * 0.9
sf.write('/home/user/work/mix_raw.wav', mix.astype(np.float32), SR, subtype='FLOAT')
sf.write('/home/user/work/music_only.wav', (mus / np.max(np.abs(mus))).astype(np.float32), SR, subtype='FLOAT')
print('events', len(E), 'peak', np.max(np.abs(mix)))
