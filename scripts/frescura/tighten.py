# Remove awkward pauses: find silent runs (< THR dB, > MINGAP s) inside the kept sections of the
# raw voice and shrink each to KEEP s. Writes segments.json [[src_start, src_end], ...] per section.
# Usage: python tighten.py raw.wav segments.json "0:5.90,7.14:17.80"
import soundfile as sf, numpy as np, json, sys
THR, MINGAP, KEEP, HOP = -27.0, 0.16, 0.10, 0.01
a, sr = sf.read(sys.argv[1]);  a = a if a.ndim == 1 else a.mean(1)
w = int(HOP * sr)
rms = np.array([20 * np.log10(np.sqrt(np.mean(a[i:i + 2 * w] ** 2)) + 1e-9) for i in range(0, len(a) - 2 * w, w)])
out = []
for sec in sys.argv[3].split(','):
    s0, s1 = map(float, sec.split(':')); segs = []; cur = s0
    i = int(s0 / HOP); e = int(s1 / HOP)
    while i < e:
        if rms[i] < THR:
            j = i
            while j < e and rms[j] < THR: j += 1
            g0, g1 = i * HOP, j * HOP
            if g1 - g0 > MINGAP and g0 > s0 + 0.05 and g1 < s1 - 0.05:
                segs.append([round(cur, 3), round(g0 + KEEP / 2, 3)]); cur = round(g1 - KEEP / 2, 3)
            i = j
        else: i += 1
    segs.append([round(cur, 3), s1]); out.append(segs)
json.dump(out, open(sys.argv[2], 'w')); print(json.dumps(out))
print("kept per section:", [round(sum(b - a for a, b in s), 2) for s in out])
