"""Cut a voice track down to the kept regions and shrink every pause inside them.

usage: python tighten.py in.wav out.wav map.json START:END [START:END ...]
Pauses (frames quieter than THR dB for longer than MIN_GAP) are shortened to KEEP_GAP.
map.json holds the kept pieces as [src_start, src_end, out_start] so word times can be
moved onto the tightened track.
"""
import sys, json, os
import numpy as np, soundfile as sf

THR = float(os.environ.get("THR", "-40"))       # dB below full scale counts as pause
MIN_GAP = float(os.environ.get("MIN_GAP", "0.14"))
KEEP_GAP = float(os.environ.get("KEEP_GAP", "0.06"))
XF = 0.012                                       # crossfade at every joint

src, dst, mp = sys.argv[1:4]
regions = [tuple(map(float, r.split(":"))) for r in sys.argv[4:]]
a, sr = sf.read(src, dtype="float32")
if a.ndim > 1:
    a = a.mean(1)
hop = int(0.01 * sr)
rms = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2) + 1e-12) for i in range(0, len(a), hop)])
db = 20 * np.log10(rms)
# smooth a little so a single loud frame does not split a pause
db = np.convolve(db, np.ones(3) / 3, mode="same")

pieces = []
for (s, e) in regions:
    i0, i1 = int(s / 0.01), int(e / 0.01)
    quiet = db[i0:i1] < THR
    cur = s
    k = 0
    n = len(quiet)
    while k < n:
        if quiet[k]:
            j = k
            while j < n and quiet[j]:
                j += 1
            gs, ge = s + k * 0.01, s + j * 0.01
            if ge - gs > MIN_GAP:
                # keep half of KEEP_GAP on each side of the pause
                cut_a, cut_b = gs + KEEP_GAP / 2, ge - KEEP_GAP / 2
                if k == 0:
                    cut_a = gs
                if j == n:
                    cut_b = ge
                if cut_a > cur:
                    pieces.append((cur, cut_a))
                cur = cut_b
            k = j
        else:
            k += 1
    if e > cur:
        pieces.append((cur, e))

out = []
mapping = []
t = 0.0
fx = int(XF * sr)
for (s, e) in pieces:
    seg = a[int(s * sr):int(e * sr)].copy()
    if len(seg) < 2 * fx:
        continue
    ramp = np.linspace(0, 1, fx, dtype=np.float32)
    seg[:fx] *= ramp
    seg[-fx:] *= ramp[::-1]
    mapping.append([round(s, 3), round(e, 3), round(t, 3)])
    out.append(seg)
    t += len(seg) / sr
y = np.concatenate(out)
sf.write(dst, y, sr, subtype="FLOAT")
json.dump(mapping, open(mp, "w"))
print(f"{len(pieces)} pieces, {sum(e - s for s, e in regions):.2f}s -> {t:.2f}s")
