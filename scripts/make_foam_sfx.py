"""Foam sounds for the pump B-roll: a soft pump 'squish' and a cluster of tiny bubble pops.
Usage: python make_foam_sfx.py out_dir
"""
import sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000; out = sys.argv[1]; rng = np.random.default_rng(5)
T = lambda d: np.arange(int(d * SR)) / SR

def bubble(f0, d=0.06):
    t = T(d); f = f0 * (1 + 2.2 * t / d)            # rising pitch = a popping bubble
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 70) * np.minimum(1, t / 0.0015)

def bubbles(d=1.4, n=38):
    x = np.zeros((int(d * SR) + SR // 10, 2))
    for k in range(n):
        o = int((rng.uniform(0, 1) ** 1.6) * d * SR); b = bubble(rng.uniform(900, 3200)) * rng.uniform(0.25, 1)
        p = rng.uniform(-0.8, 0.8); x[o:o + len(b), 0] += b * (1 - p) / 2; x[o:o + len(b), 1] += b * (1 + p) / 2
    return x

def squish(d=0.42):
    t = T(d); n = rng.standard_normal(len(t)); y = np.zeros(len(t)); seg = 512
    for i in range(0, len(t), seg):
        p = i / len(t); fc = 1800 - 1200 * p
        y[i:i + seg] = sosfilt(butter(2, [fc * 0.6, fc * 1.5], 'band', fs=SR, output='sos'), n[i:i + seg])
    env = np.minimum(1, t / 0.03) * np.exp(-t * 7)
    y = y * env + 0.35 * bubbles(d, 10)[: len(t), 0]
    return np.stack([y, y], 1)

for name, x in (("foam-bubbles", bubbles()), ("pump-squish", squish())):
    x = x / np.max(np.abs(x)) * 10 ** (-3 / 20)
    sf.write(f"{out}/{name}.wav", x.astype(np.float32), SR); print(name, round(len(x) / SR, 2))
