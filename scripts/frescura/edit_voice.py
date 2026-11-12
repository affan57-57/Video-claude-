# Cut awkward pauses, splice with short crossfades, write cut list + remapped word timings.
import sys, json, numpy as np, soundfile as sf
src, trj, out_wav, out_words, tempo = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5])
CUTS = [(5.50, 5.82), (11.32, 11.54), (13.80, 13.96), (28.72, 28.92)]  # seconds in original
END = 31.80
a, sr = sf.read(src, dtype="float32")
keep, t = [], 0.0
for c0, c1 in CUTS: keep.append((t, c0)); t = c1
keep.append((t, END))
xf = int(0.015 * sr); outs = []
for k0, k1 in keep:
    seg = a[int(k0 * sr):int(k1 * sr)].copy()
    if outs:
        prev = outs[-1]; r = np.linspace(0, 1, xf)
        prev[-xf:] = prev[-xf:] * (1 - r) + seg[:xf] * r; seg = seg[xf:]
    outs.append(seg)
y = np.concatenate(outs); sf.write(out_wav, y, sr, subtype="FLOAT")
def remap(t):
    acc = 0.0; xs = xf / sr
    for i, (k0, k1) in enumerate(keep):
        if t <= k1 or i == len(keep) - 1:
            return (acc + max(0.0, min(t, k1) - k0)) / tempo
        acc += (k1 - k0) - xs
words = []
for s in json.load(open(trj)):
    for w in s["words"]:
        words.append(dict(w=w["w"].strip(), s=round(remap(w["s"]), 3), e=round(remap(w["e"]), 3)))
json.dump(dict(duration=round(len(y) / sr / tempo, 3), words=words), open(out_words, "w"), ensure_ascii=False, indent=0)
print("edited len", len(y) / sr, "-> after tempo", len(y) / sr / tempo)
