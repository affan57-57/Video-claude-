"""Cut the voice-over: drop the repeated CTA line and trim dead air, then emit an
edit map (source time -> edited time) used to retime the word transcript."""
import json, sys, numpy as np, soundfile as sf
src, words_json, out_wav, out_words = sys.argv[1:5]
TEMPO = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
# (start, end) in SOURCE seconds, each a clean phrase; pauses inside are removed
SEGS = [
    (0.00, 3.16),            # Hari yang penat ... diri sendiri.
    (3.70, 4.22), (4.50, 5.92),   # Self care | tak semestinya mahal.
    (6.00, 8.54),            # Ianya boleh bermula dengan mandi yang selesa.
    (8.86, 15.32),           # Frescura Body mengandungi garam laut ... kulit.
    (15.46, 19.02), (19.14, 20.46),  # Digabungkan ... macam | memanjakan diri.
    (20.60, 23.47), (23.70, 25.50), (26.10, 28.26),  # Pilih Woman Glory ... / Noche ... / bau manis, lembut dan misteri.
    (28.70, 30.48), (30.62, 32.92),  # Kamu dah jaga ... / Sekarang giliran jaga diri sendiri.
    (33.16, 34.24),          # Stok batch ini dah terhad.
    (34.58, 35.80),          # Klik link di bawah.
    (37.52, 39.64),          # Tekan beg kuning dan checkout sekarang.  (2nd take kept, 1st take removed)
]
GAP = 0.06          # breath gap between phrases
FADE = 0.012
a, sr = sf.read(src, dtype="float32")
parts, emap, t = [], [], 0.0
for s, e in SEGS:
    seg = a[int(s*sr):int(e*sr)].copy(); n = int(FADE*sr)
    seg[:n] *= np.linspace(0, 1, n); seg[-n:] *= np.linspace(1, 0, n)
    parts += [seg, np.zeros(int(GAP*sr), np.float32)]
    emap.append((s, e, t)); t += (e - s) + GAP
y = np.concatenate(parts); sf.write(out_wav, y, sr, subtype="FLOAT")
def remap(x):
    for s, e, o in emap:
        if s - 0.05 <= x <= e + 0.05: return (o + min(max(x - s, 0), e - s)) / TEMPO
    return None
W = json.load(open(words_json)); res = []
for w in W:
    s, e = remap(w["s"]), remap(w["e"])
    if s is None or e is None: continue
    res.append(dict(t=w["t"], s=round(s, 3), e=round(e, 3)))
json.dump(res, open(out_words, "w"), ensure_ascii=False, indent=0)
print(f"cut length {t:.2f}s -> {t/TEMPO:.2f}s at {TEMPO}x; {len(res)} words")
