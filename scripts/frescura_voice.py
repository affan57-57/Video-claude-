"""Tighten pauses in a cleaned voice track, then speed up (pitch preserved by ffmpeg atempo afterwards).
Usage: python frescura_voice.py in.wav out.wav [thr_db] [min_gap] [keep_gap]
"""
import sys, numpy as np, soundfile as sf

x, sr = sf.read(sys.argv[1], dtype="float32")
mono = x if x.ndim == 1 else x.mean(1)
thr = float(sys.argv[3]) if len(sys.argv) > 3 else -38.0
min_gap = float(sys.argv[4]) if len(sys.argv) > 4 else 0.13
keep = float(sys.argv[5]) if len(sys.argv) > 5 else 0.07
hop = int(0.01 * sr)
rms = np.array([np.sqrt(np.mean(mono[i:i + hop] ** 2) + 1e-12) for i in range(0, len(mono), hop)])
db = 20 * np.log10(rms)
quiet = db < thr
runs, i = [], 0
while i < len(quiet):
    if quiet[i]:
        j = i
        while j < len(quiet) and quiet[j]: j += 1
        runs.append((i, j)); i = j
    else:
        i += 1
segs, pos, removed = [], 0, 0.0
fade = int(0.008 * sr)
for a, b in runs:
    dur = (b - a) * 0.01
    sa, sb = a * hop, b * hop
    if a == 0:  # leading silence: keep only 0.05 s
        pos = max(0, sb - int(0.05 * sr)); removed += dur; continue
    if dur >= min_gap:
        k = int(keep * sr / 2)
        segs.append((pos, sa + k)); pos = sb - k; removed += dur - keep
segs.append((pos, min(len(x), pos + int(len(x) - pos))))
# trailing silence
out = []
for s, e in segs:
    seg = x[s:e].copy()
    n = min(fade, len(seg) // 2)
    if n > 0:
        r = np.linspace(0, 1, n)
        if seg.ndim == 2: r = r[:, None]
        seg[:n] *= r; seg[-n:] *= r[::-1]
    out.append(seg)
y = np.concatenate(out)
# trim tail silence
ym = y if y.ndim == 1 else y.mean(1)
nz = np.where(np.abs(ym) > 10 ** (thr / 20))[0]
y = y[: nz[-1] + int(0.15 * sr)]
sf.write(sys.argv[2], y, sr, subtype="FLOAT")
print(f"in {len(x)/sr:.2f}s -> out {len(y)/sr:.2f}s, removed {removed:.2f}s, cuts {len(segs)-1}")
