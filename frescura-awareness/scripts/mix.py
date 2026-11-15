"""Mix voice + ducked music + SFX cues + pump foley into one 32 s master (48k stereo)."""
import sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
W = sys.argv[1]; OUT = sys.argv[2]; SR = 48000; DUR = 32.0; N = int(DUR * SR)
mix = np.zeros((N, 2))
def load(p):
    x, sr = sf.read(p, dtype='float64'); assert sr == SR, (p, sr)
    return np.stack([x, x], 1) if x.ndim == 1 else x
def put(x, t, db):
    i = int(t * SR); seg = x[:max(0, N - i)]; mix[i:i + len(seg)] += seg * 10 ** (db / 20)

VOICE_AT = 0.25
voice = load(f'{W}/voice_final.wav'); put(voice, VOICE_AT, 0.0)
vend = VOICE_AT + len(voice) / SR

# music: ducked under the voice, lifted for the showcase outro
mus = load(f'{W}/sfx/music.wav')[:N]
t = np.arange(len(mus)) / SR
g = np.interp(t, [0, .2, vend - .1, vend + .5, 31.0, 32], [0.0, .30, .30, .80, .80, 0.0])
g = np.where(t < 0.2, t / .2 * .45, g)  # small lift on the hook hit
mix[:len(mus)] += mus * (10 ** (-6 / 20)) * g[:, None]

# pump foley from the real clip (S5 media 3.4s @ 13.42, S8 media 12.6s @ 20.95)
pa, sr = sf.read(f'{W}/pump_audio.wav', dtype='float64')
pa = sosfilt(butter(2, 180, 'high', fs=SR, output='sos'), pa); pa = pa / (np.max(np.abs(pa)) + 1e-9)
for ms, at, d, db in [(3.4, 13.42, 2.62, -14), (12.6, 20.95, 3.85, -12)]:
    seg = pa[int(ms * SR):int((ms + d) * SR)].copy(); n = len(seg); f = int(.08 * SR)
    seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    put(np.stack([seg, seg], 1), at, db)

S = lambda n: load(f'{W}/sfx/{n}.wav')
CUES = [
 (0.00, 'impact', -3), (0.04, 'whoosh_long', -8), (0.55, 'shimmer', -11),
 (3.42, 'swipe', -7), (3.75, 'whoosh', -10), (4.15, 'whoosh', -10), (5.74, 'tick', -6), (5.76, 'ding', -8), (6.35, 'pop', -5),
 (6.20, 'rev_whoosh', -9), (6.94, 'impact', -5), (7.00, 'shimmer', -9),
 (8.33, 'whoosh', -9), (8.70, 'bubbles', -11), (9.38, 'pop', -5),
 (10.08, 'swipe', -8), (10.95, 'tick', -7), (11.40, 'tick', -7), (11.85, 'tick', -7), (12.02, 'whoosh', -12), (12.28, 'stamp', -2), (12.28, 'impact', -11),
 (13.40, 'whoosh_long', -8), (13.75, 'bubbles', -10), (14.30, 'pop', -9),
 (15.98, 'swipe', -7), (16.02, 'impact', -12),
 *[(16.40 + k * .1, 'tick', -16) for k in range(10)],
 (17.48, 'whoosh', -8), (17.62, 'pop', -4), (17.87, 'pop', -9), (18.30, 'shimmer', -12), (18.95, 'cash', -4), (19.45, 'pop', -7),
 (20.35, 'riser', -11), (20.95, 'impact', -6), (21.20, 'bubbles', -10), (21.50, 'swipe', -10), (22.05, 'swipe', -10), (22.60, 'swipe', -10),
 (24.73, 'whoosh_long', -8), (25.00, 'glass', -8), (25.45, 'glass', -8),
 (27.90, 'riser', -10), (28.60, 'impact', -4), (28.70, 'shimmer', -8), (29.80, 'ding', -8),
]
for t0, n, db in CUES: put(S(n), t0, db)

# master: soft clip + peak limit to -1 dBFS (loudness set afterwards with ffmpeg loudnorm)
mix = np.tanh(mix * 1.1) / 1.1
mix *= np.minimum(1, (DUR - np.arange(N) / SR) / .5)[:, None]
sf.write(OUT, mix.astype(np.float32), SR, subtype='FLOAT')
print('voice end', round(vend, 2))
