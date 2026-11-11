# Final audio mix for the Frescura Body feedback ad (film time in seconds).
# Usage: python mix.py WORKDIR out.wav     (expects v0.wav v1.wav fb.wav sfx/*.wav sfx/music.wav in WORKDIR)
import numpy as np, soundfile as sf, sys, os
W = sys.argv[1]; SR = 48000; DUR = 30.5; N = int(DUR * SR)
mix = np.zeros((N, 2))
def load(p):
    a, sr = sf.read(os.path.join(W, p), dtype='float64'); assert sr == SR, (p, sr)
    return np.stack([a, a], 1) if a.ndim == 1 else a
def put(name, t, db=0.0, src=None):
    a = src if src is not None else load(name); i = int(t * SR); j = min(N, i + len(a))
    mix[i:j] += a[:j - i] * 10 ** (db / 20)
VOICE = [("v0.wav", 0.35), ("v1.wav", 18.45)]
for f, t in VOICE: put(f, t, 0.0)
put("fb.wav", 6.0, 0.0)
S = lambda n: f"sfx/{n}.wav"
CUES = [  # (sfx, time, dB)
    ("whoosh", .30, -19), ("tick", .64, -14), ("whoosh", 1.02, -15), ("pop", 1.73, -12),
    ("shutter", 2.43, -10), ("whoosh", 2.38, -14), ("tick", 2.56, -15), ("tick", 2.76, -15),
    ("pop", 3.05, -13), ("pop", 3.45, -13), ("pop", 3.85, -13), ("shimmer", 3.1, -20),
    ("shutter", 4.53, -11), ("bubbles", 4.6, -12), ("riser", 4.75, -12), ("whoosh", 5.72, -10), ("impact", 5.98, -12),
    ("whoosh", 18.12, -12), ("shimmer", 18.3, -17), ("bubbles", 18.4, -16), ("pop", 18.97, -13),
    ("impact", 19.58, -13), ("shutter", 19.6, -12), ("pop", 20.61, -12),
    ("whoosh", 21.12, -12), ("pop", 21.72, -9), ("chime", 21.65, -15), ("tick", 21.62, -12), ("tick", 22.28, -12), ("cash", 22.38, -10),
    ("whoosh", 22.8, -13), ("glitch", 25.05, -14), ("impact", 25.08, -7),
    ("whoosh", 26.3, -13), ("shimmer", 26.45, -14), ("chime", 26.55, -12), ("pop", 27.58, -14),
]
for n, t, db in CUES: put(S(n), t, db)
imp = load(S("impact"))[:int(.34 * SR)].copy(); imp *= np.linspace(1, 0, len(imp))[:, None] ** 2
put(None, 0.0, -8, src=imp)  # short hook hit that ends before "Jangan beli"
for k in range(9): put(S("clock"), 23.2 + k * 0.24, -16)
# music bed with ducking: under voice -21 dB, under feedback -30 dB, end card -16 dB
mus = load("sfx/music.wav")[:N]; tt = np.arange(N) / SR
g = np.full(N, -21.0)
g[(tt >= 5.9) & (tt < 18.3)] = -31.0
g[tt >= 26.45] = -15.0
g[tt < 0.95] = -60.0
k = int(.12 * SR); g = np.convolve(np.pad(g, (k, k), mode='edge'), np.ones(2 * k + 1) / (2 * k + 1), mode='same')[k:-k]
env = 10 ** (g / 20) * np.minimum(1, (DUR - tt) / 1.2).clip(0, 1)
mix += mus * env[:, None]
mix[:, :] *= np.minimum(1, (DUR - tt) / 0.35).clip(0, 1)[:, None]
sf.write(sys.argv[2], mix.astype(np.float32), SR, subtype='FLOAT'); print("peak", np.abs(mix).max())
