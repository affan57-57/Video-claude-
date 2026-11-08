"""Tighten the denoised voice: cut the long pauses, cap every inner pause, split into two takes.

Usage: python voice_edit.py denoised_48k.wav out_dir
Writes out_dir/vo_intro_raw.wav (hook + "jangan skip" line) and out_dir/vo_outro_raw.wav (urgency + CTA),
plus out_dir/cuts.json with the kept source intervals of each take.
"""
import json, sys
import numpy as np, soundfile as sf

src, out = sys.argv[1], sys.argv[2]
a, sr = sf.read(src, dtype="float32")
if a.ndim > 1:
    a = a.mean(1)

# Source intervals of each line (seconds, measured with silencedetect on the denoised stem).
TAKES = {
    "vo_intro": [(0.00, 3.20), (3.36, 8.04)],                       # Bukan kami yang puji... / Jangan skip...
    "vo_outro": [(9.45, 10.58), (10.76, 12.56), (12.66, 16.48), (16.60, 18.86)],  # Stok... / Jangan tunggu... / Tekan beg kuning... / Tengok sekarang...
}
LINE_GAP = 0.10   # pause kept between sentences
MAX_PAUSE = 0.09  # longest pause kept inside a sentence
FADE = 0.012

def env_db(x, win):
    n = len(x) // win
    r = np.sqrt(np.mean(x[: n * win].reshape(n, win) ** 2, 1) + 1e-12)
    return 20 * np.log10(r)

def tighten(seg):
    """Cap inner pauses (< -40 dB for > MAX_PAUSE) to MAX_PAUSE."""
    win = int(0.01 * sr)
    db = env_db(seg, win)
    quiet = db < -40
    keep = np.ones(len(seg), bool)
    i = 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if i > 0 and j < len(quiet) and (j - i) * 0.01 > MAX_PAUSE:
                mid = (i + j) // 2
                half = int(MAX_PAUSE / 2 * sr)
                keep[i * win: mid * win - half] = False
                keep[mid * win + half: j * win] = False
            i = j
        else:
            i += 1
    return seg[keep]

def fade(x):
    n = int(FADE * sr)
    w = np.linspace(0, 1, n, dtype=np.float32)
    x = x.copy(); x[:n] *= w; x[-n:] *= w[::-1]
    return x

cuts = {}
for name, ivs in TAKES.items():
    parts = []
    for k, (s, e) in enumerate(ivs):
        seg = fade(tighten(a[int(s * sr): int(e * sr)]))
        parts.append(seg)
        if k < len(ivs) - 1:
            parts.append(np.zeros(int(LINE_GAP * sr), np.float32))
    y = np.concatenate(parts)
    sf.write(f"{out}/{name}_raw.wav", y, sr, subtype="FLOAT")
    cuts[name] = {"intervals": ivs, "duration_s": round(len(y) / sr, 3)}
    print(name, round(len(y) / sr, 3), "s")
json.dump(cuts, open(f"{out}/cuts.json", "w"), indent=1)
