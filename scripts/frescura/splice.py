# Splice segments (from tighten.py) out of a voice wav with 12 ms equal-power crossfades.
# Usage: python splice.py in.wav segments.json SECTION_INDEX out.wav
import soundfile as sf, numpy as np, json, sys
a, sr = sf.read(sys.argv[1], dtype='float32'); segs = json.load(open(sys.argv[2]))[int(sys.argv[3])]
X = int(0.012 * sr); fi = np.sin(np.linspace(0, np.pi / 2, X)) ** 2; fo = fi[::-1]
out = np.zeros(0, dtype=np.float32)
for s, e in segs:
    c = a[int(s * sr):int(e * sr)].copy()
    if len(out) >= X and len(c) >= X:
        c[:X] = c[:X] * fi + out[-X:] * fo; out = out[:-X]
    out = np.concatenate([out, c])
sf.write(sys.argv[4], out, sr); print(sys.argv[4], round(len(out) / sr, 3))
