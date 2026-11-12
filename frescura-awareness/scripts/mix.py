# Final mix: studio voice + sidechain-ducked luxe music bed + SFX cues, loud & limited.
import numpy as np, soundfile as sf, sys, subprocess
SR = 48000; W = sys.argv[1]; out = sys.argv[2]; DUR = 34.6
N = int(DUR * SR)
v, _ = sf.read(f"{W}/voice_studio.wav", dtype="float32")
if v.ndim > 1: v = v.mean(1)
voice = np.zeros(N); voice[:min(N, len(v))] = v[:N]
def load(n):
    x, _ = sf.read(f"{W}/sfx/{n}.wav", dtype="float32"); return x if x.ndim == 2 else np.stack([x, x], 1)
mix = np.stack([voice, voice], 1) * 1.0
# music bed with ducking under voice
m = load("music")[:N]; m = np.pad(m, ((0, N - len(m)), (0, 0)))
env = np.abs(voice); k = int(.08 * SR); env = np.convolve(env, np.ones(k) / k, "same")
duck = 1 - .6 * np.clip(env / (env.max() * .25), 0, 1)
fade = np.minimum(1, np.arange(N) / (.3 * SR)) * np.clip((DUR - np.arange(N) / SR) / 1.2, 0, 1)
# music rises at the end card when voice stops
mix += m * (10 ** (-17 / 20)) * duck[:, None] * fade[:, None]
cues = [  # (time, sfx, dB)
    (0.00, "impact", -6), (0.02, "swish", -14), (0.50, "impact", -9), (0.52, "glass", -16), (0.72, "whoosh", -14),
    (1.10, "tick", -20), (1.80, "swish", -15),
    (2.15, "thud", -14), (2.40, "pop", -18), (2.45, "pop", -19), (2.90, "shimmer", -22), (3.40, "whoosh", -18),
    (5.00, "whoosh", -13), (5.50, "pop", -15), (6.20, "pop", -13), (6.70, "pop", -13), (7.22, "swish", -11), (7.80, "impact", -14), (7.85, "glass", -17),
    (9.40, "whoosh", -13), (9.90, "tick", -18), (11.40, "tick", -15), (11.78, "tick", -15), (12.16, "tick", -15), (12.54, "tick", -15), (13.10, "pop", -17),
    (14.05, "whoosh", -12), (14.90, "swish", -15), (15.75, "impact", -12), (15.77, "shimmer", -20),
    (16.55, "whoosh", -13), (16.95, "pump", -9), (17.30, "bubbles", -15), (18.95, "pump", -10), (19.00, "pop", -14), (19.10, "bubbles", -14), (20.10, "pop", -14), (20.30, "shimmer", -19),
    (20.40, "riser", -14), (21.15, "impact", -9), (21.18, "glass", -12), (21.60, "shimmer", -15),
    (22.85, "whoosh", -12), (23.10, "swish", -12), (24.10, "pop", -15), (24.25, "pop", -15),
    (25.15, "whoosh", -12), (25.75, "tap", -8), (25.76, "pop", -13), (26.95, "tap", -9), (27.55, "swish", -15), (28.10, "tap", -7), (28.12, "cash", -11),
    (28.45, "whoosh", -12), (28.80, "tick", -16), (29.10, "tick", -16), (29.35, "tick", -15), (29.55, "tick", -14), (29.65, "impact", -10),
    (30.70, "whoosh", -12), (31.10, "swish", -13), (31.80, "thud", -11),
    (32.05, "riser", -17), (32.30, "impact", -8), (32.32, "glass", -11), (32.40, "shimmer", -13), (33.60, "pop", -17), (34.05, "pop", -18),
]
for t, n, db in cues:
    x = load(n) * 10 ** (db / 20); i = int(t * SR); j = min(N, i + len(x)); mix[i:j] += x[:j - i]
sf.write(out + ".pre.wav", mix.astype(np.float32), SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out + ".pre.wav", "-af",
                "loudnorm=I=-11:TP=-1.0:LRA=8,alimiter=limit=0.89:attack=2:release=40:level=false,afade=t=out:st=33.9:d=0.7",
                "-ar", "48000", "-c:a", "pcm_s16le", out], check=True)
print("mixed", out)
