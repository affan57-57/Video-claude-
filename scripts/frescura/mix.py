"""Mix voice + ducked music + SFX into final_mix.wav. Usage: mix.py VOICE.wav KITDIR OUT.wav TOTAL"""
import sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
V, K, OUT, TOTAL = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]); SR = 48000
N = int(TOTAL * SR)
def load(p):
    x, sr = sf.read(p, dtype="float32", always_2d=True); assert sr == SR, (p, sr)
    return x if x.shape[1] == 2 else np.repeat(x, 2, 1)
db = lambda d: 10 ** (d / 20)
voice = np.zeros((N, 2)); v = load(V)[:N]; voice[:len(v)] = v * db(1.0)
# SFX cue list: (time, name, gain dB)
CUES = [(0.0, "impact", -4), (0.02, "shimmer", -12), (1.28, "swish", -14), (2.86, "shimmer", -11),
        (3.80, "whoosh", -9), (4.10, "chime", -15), (4.5, "tick", -16), (4.9, "tick", -16), (5.6, "tick", -16),
        (6.46, "pop", -10), (6.90, "pop", -10), (7.30, "pop", -10), (8.15, "shimmer", -10),
        (8.62, "whoosh", -9), (9.3, "swish", -13), (10.66, "swish", -14), (11.0, "riser", -12), (11.5, "tick", -15),
        (12.42, "impact", -9), (12.42, "shimmer", -8), (14.45, "whoosh", -8), (14.70, "impact", -6),
        (15.3, "swish", -14), (15.54, "shimmer", -10), (16.42, "whoosh", -9), (16.75, "pump", -8), (16.95, "foam", -9),
        (17.70, "impact", -10), (17.70, "shimmer", -11), (18.40, "whoosh", -9), (19.0, "tick", -15), (19.16, "tick", -15),
        (19.32, "tick", -15), (19.48, "tick", -15), (20.30, "whoosh", -8), (20.5, "shimmer", -11), (22.32, "chime", -12),
        (23.12, "whoosh", -9), (23.40, "foam", -10), (23.9, "swish", -13), (24.62, "whoosh", -10),
        (24.85, "tick", -11), (25.15, "tick", -11), (25.45, "tick", -11), (25.75, "tick", -11), (25.98, "pop", -9),
        (26.10, "whoosh", -9), (27.38, "impact", -4), (27.6, "heartbeat", -6), (28.4, "heartbeat", -7),
        (29.0, "whoosh", -10), (29.40, "pop", -7), (29.36, "tick", -9), (30.10, "cash", -6), (30.86, "whoosh", -9),
        (31.08, "impact", -7), (31.1, "shimmer", -8), (31.6, "chime", -10)]
sfx = np.zeros((N, 2)); cache = {}
for t, n, g in CUES:
    x = cache.setdefault(n, load(f"{K}/{n}.wav")); i = int(t * SR); j = min(N, i + len(x)); sfx[i:j] += x[: j - i] * db(g)
# music + sidechain ducking from voice envelope
mus = np.zeros((N, 2)); m = load(f"{K}/music.wav")[:N]; mus[:len(m)] = m
env = np.abs(voice[:, 0]); env = sosfilt(butter(1, 6, fs=SR, output="sos"), env); env = env / (env.max() + 1e-9)
duck = 1 - 0.55 * np.clip(env * 3, 0, 1)
tt = np.arange(N) / SR
lvl = np.where(tt < 31.0, db(-15), db(-9))  # lift music for the outro
mus = mus * (duck * lvl)[:, None]
fade = np.minimum(1, (TOTAL - tt) / 1.2)[:, None]
mix = (voice + sfx + mus) * fade
sf.write(OUT, mix.astype(np.float32), SR, subtype="FLOAT")
print("peak", np.abs(mix).max())
