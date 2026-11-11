# Mix: studio voice + ducked music bed + SFX cues placed on transcript beats.
import numpy as np, soundfile as sf, sys
from scipy.ndimage import uniform_filter1d
SR = 48000; D = 38.6; N = int(D * SR)
voice, _ = sf.read("voice_final.wav"); voice = np.stack([voice, voice], 1) if voice.ndim == 1 else voice
mix = np.zeros((N, 2)); mix[:len(voice)] += voice[:N]
def load(n):
    x, _ = sf.read(f"sfx/{n}.wav"); return x if x.ndim == 2 else np.stack([x, x], 1)
# (time, sfx, gain dB) — SFX pushed loud as requested, still under the voice peaks
CUES = [
 (0.00, "impact", -4), (0.02, "whoosh", -9), (0.28, "swipe", -8), (0.50, "pop", -8), (0.90, "tick", -10),
 (1.96, "glitch", -7), (2.38, "whoosh", -9),
 (1.30, "riser", -8), (2.66, "impact", -3), (2.66, "shimmer", -7), (3.70, "whoosh", -8), (3.85, "drop", -9),
 (4.08, "pop", -6), (5.34, "pop", -6), (7.40, "pop", -6), (8.40, "shimmer", -6), (8.40, "swipe", -9),
 (8.95, "whoosh", -6), (9.10, "swipe", -10), (9.86, "tick", -8), (9.98, "tick", -9), (10.10, "tick", -9), (10.22, "tick", -9),
 (10.98, "swipe", -9), (13.25, "whoosh", -6), (13.60, "bubble", -7), (14.04, "shimmer", -8),
 (16.15, "whoosh", -6), (16.20, "impact", -10), (17.00, "shimmer", -8), (18.14, "pop", -6), (19.84, "shimmer", -6),
 (20.50, "whoosh", -6), (21.20, "pump", -3), (21.40, "bubble", -6), (22.80, "pump", -4), (23.82, "pop", -5), (24.00, "swipe", -9),
 (24.45, "whoosh", -5), (25.78, "pop", -6), (25.85, "whoosh", -5), (27.14, "ding", -9),
 (28.10, "riser", -8), (28.25, "impact", -6), (28.66, "swipe", -8), (30.64, "impact", -4), (30.64, "shimmer", -8),
 (31.55, "whoosh", -6), *[(31.8 + i * 0.18, "tick", -7) for i in range(8)], (32.32, "drop", -4), (32.32, "glitch", -10),
 (33.48, "whoosh", -6), (33.94, "pop", -4), (34.06, "ding", -7), (34.90, "swipe", -8), (36.56, "chaching", -4),
 (37.20, "impact", -4), (37.20, "shimmer", -5),
]
sfxbus = np.zeros_like(mix)
for t, n, g in CUES:
    x = load(n) * 10 ** (g / 20); o = int(t * SR); e = min(N, o + len(x)); sfxbus[o:e] += x[:e - o]
bed, _ = sf.read("sfx/bed.wav"); bed = bed[:N]; bed = np.pad(bed, ((0, N - len(bed)), (0, 0)))
# sidechain duck from voice envelope
env = uniform_filter1d(np.abs(mix[:, 0]), int(0.12 * SR)); env = env / (env.max() + 1e-9)
duck = 1 - 0.55 * np.clip(env * 6, 0, 1)
fade = np.ones(N); fade[-int(1.2 * SR):] = np.linspace(1, 0, int(1.2 * SR)); fade[:int(0.05 * SR)] = np.linspace(0, 1, int(0.05 * SR))
out = mix + sfxbus + bed * 10 ** (-17 / 20) * duck[:, None] * fade[:, None]
sf.write("mix_pre.wav", out.astype(np.float32), SR, subtype="FLOAT"); print("ok", len(CUES), "cues")
