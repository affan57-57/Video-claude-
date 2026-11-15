# Tighten pauses, drop the opening false start, speed up, and remap word timestamps.
# Usage: python frescura_voice.py denoised.wav words.json out_voice.wav out_words.json
import sys, json, numpy as np, soundfile as sf
src, wj, out_wav, out_words = sys.argv[1:5]
TEMPO = 1.12          # speech speed-up (applied later with ffmpeg atempo; timestamps divided here)
START = 1.40          # skip the "Kami—" false start
KEEP_GAP = 0.07       # pauses longer than this are shortened to this
a, sr = sf.read(src, dtype="float32"); a = a if a.ndim == 1 else a.mean(1)
h = int(.01 * sr)
rms = np.array([np.sqrt(np.mean(a[i:i + h] ** 2)) for i in range(0, len(a) - h, h)])
db = 20 * np.log10(rms + 1e-9); low = db < -45
gaps = []; s = None
for i, v in enumerate(low):
    if v and s is None: s = i
    if (not v or i == len(low) - 1) and s is not None:
        if (i - s) * .01 > KEEP_GAP + .06: gaps.append((s * .01, i * .01))
        s = None
# keep-segments in original time
keep = []; t = START
for g0, g1 in gaps:
    if g1 <= START: continue
    g0 = max(g0, START)
    c0, c1 = g0 + KEEP_GAP / 2, g1 - KEEP_GAP / 2
    if c1 - c0 < .05: continue
    keep.append((t, c0)); t = c1
END = min(len(a) / sr, 34.15)
keep.append((t, END))
# splice with 8 ms crossfades
xf = int(.008 * sr); outp = np.zeros(0, np.float32)
for k0, k1 in keep:
    seg = a[int(k0 * sr):int(k1 * sr)].copy()
    if len(outp) and len(seg) > xf:
        r = np.linspace(0, 1, xf, dtype=np.float32)
        outp[-xf:] = outp[-xf:] * (1 - r) + seg[:xf] * r; seg = seg[xf:]
    outp = np.concatenate([outp, seg])
sf.write(out_wav, outp, sr, subtype="FLOAT")
def remap(t):
    acc = 0.0
    for k0, k1 in keep:
        if t < k0: return acc / TEMPO
        if t <= k1: return (acc + t - k0) / TEMPO
        acc += (k1 - k0) - xf / sr
    return acc / TEMPO
words = [w for w in json.load(open(wj)) if w["e"] > START + .05]
res = [dict(w=w["w"].strip(), s=round(remap(max(w["s"], START)), 3), e=round(remap(w["e"]), 3)) for w in words]
json.dump(res, open(out_words, "w"), ensure_ascii=False, indent=0)
print("cuts:", [(round(x, 2), round(y, 2)) for x, y in keep])
print("spliced %.2fs -> after tempo %.2fs" % (len(outp) / sr, len(outp) / sr / TEMPO))
