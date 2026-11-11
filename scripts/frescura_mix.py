"""Mix voice (intro/close), feedback clip audio, SFX and ducked music bed.
Usage: python frescura_mix.py WAV_DIR SFX_DIR OUT.wav
"""
import sys, numpy as np, soundfile as sf
from scipy.ndimage import uniform_filter1d

W, X, OUT = sys.argv[1:4]
SR = 48000; DUR = 33.4; N = int(DUR * SR)
T_INTRO, T_FB, T_CLOSE = 0.00, 6.10, 21.85
def load(p):
    a, sr = sf.read(p, dtype="float32"); assert sr == SR, (p, sr)
    return np.stack([a, a], 1) if a.ndim == 1 else a
db = lambda g: 10 ** (g / 20)
voice = np.zeros((N, 2)); fx = np.zeros((N, 2))
def put(buf, sig, t, g=0.0):
    o = int(t * SR); e = min(N, o + len(sig)); buf[o:e] += sig[:e - o] * db(g)

put(voice, load(f"{W}/v_intro.wav"), T_INTRO, 1.0)
put(voice, load(f"{W}/v_fb.wav"), T_FB, 0.5)
put(voice, load(f"{W}/v_close.wav"), T_CLOSE, 1.0)

S = {k: load(f"{X}/{k}.wav") for k in "whoosh swipe impact riser shimmer tick pop bubbles kaching glitch clock".split()}
cues = [  # (time, sfx, gain dB)
    (0.00, "impact", -4), (0.00, "glitch", -10), (0.40, "swipe", -9), (1.10, "whoosh", -8),
    (1.80, "shimmer", -10), (2.52, "whoosh", -9), (3.05, "bubbles", -12), (3.00, "tick", -9),
    (3.90, "tick", -9), (4.80, "tick", -9), (4.62, "riser", -9), (6.02, "impact", -8), (6.05, "whoosh", -9),
    (12.40, "shimmer", -11), (14.20, "pop", -9), (14.95, "swipe", -12), (19.25, "shimmer", -13),
    (21.62, "whoosh", -8), (22.70, "swipe", -10), (23.30, "bubbles", -14),
    (24.42, "clock", -9), (24.42, "swipe", -10), (25.40, "whoosh", -9), (25.95, "tick", -6),
    (26.55, "pop", -9), (27.05, "tick", -6), (27.25, "kaching", -7), (27.85, "whoosh", -9),
    (28.55, "pop", -8), (29.20, "pop", -8), (29.85, "pop", -8), (30.60, "shimmer", -12),
    (31.70, "riser", -12), (31.80, "impact", -5), (31.85, "shimmer", -8),
]
for t, k, g in cues: put(fx, S[k], t, g)

music = load(f"{X}/music.wav")[:N]
music = np.pad(music, ((0, N - len(music)), (0, 0)))
# sidechain duck: follow voice envelope
env = uniform_filter1d(np.abs(voice[:, 0]), int(0.12 * SR))
env = np.clip(env / (np.percentile(env, 95) + 1e-9), 0, 1)
duck = 1 - 0.55 * env
gain = np.full(N, db(-15.0))
fb0, fb1 = int(T_FB * SR), int((T_FB + 15.63) * SR)
gain[fb0:fb1] = db(-21.0)  # testimonial has its own ambience: keep bed lower
gain = uniform_filter1d(gain, int(0.3 * SR))
mix = voice + fx + music * (gain * duck)[:, None]
tt = np.arange(N) / SR; mix *= np.minimum(1, (DUR - tt) / 0.6)[:, None]
sf.write(OUT, mix.astype(np.float32), SR, subtype="FLOAT")
print("peak", 20 * np.log10(np.abs(mix).max()))
