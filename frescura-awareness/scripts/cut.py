# Remove awkward pauses using word timestamps, then speed-up via rubberband (pitch kept).
# usage: cut.py transcript.json in.wav out_cut.wav words_out.json TEMPO
import json, sys, subprocess, numpy as np, soundfile as sf
tx, src, dst, wout, tempo = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5])
# corrected spellings for captions (Whisper misheard brand / words)
FIX = {"Atau": "Tahu", "Perjagaan": "Penjagaan", "bet": "beg", "fresh": "FRESCURA", "kurang": None, "bodi": "BODY"}
words = [w for s in json.load(open(tx)) for w in s["words"]]
# brand fix: "fresh kurang bodi" -> "FRESCURA BODY"
out = []; i = 0
while i < len(words):
    w = dict(words[i]); t = w["w"].strip()
    if t.lower() == "fresh" and i + 2 < len(words) and words[i + 1]["w"].strip() == "kurang":
        tail = words[i + 2]["w"].strip(); punct = tail[len("bodi"):]
        out.append(dict(w="FRESCURA", s=w["s"], e=words[i + 1]["e"]))
        out.append(dict(w="BODY" + punct, s=words[i + 2]["s"], e=words[i + 2]["e"])); i += 3; continue
    if t in ("Atau",): t = "Tahu"
    if t == "Perjagaan": t = "Penjagaan"
    if t == "bet": t = "beg"
    if t == "-lama,": out[-1]["w"] = "lama-lama,"; out[-1]["e"] = w["e"]; i += 1; continue
    out.append(dict(w=t, s=w["s"], e=w["e"])); i += 1
words = out
a, sr = sf.read(src, dtype="float32")
if a.ndim > 1: a = a.mean(1)
PRE, POST, GAP_SENT, GAP_WORD = 0.03, 0.06, 0.10, 0.03
segs = []
for w in words:
    s, e = max(0, w["s"] - PRE), w["e"] + POST
    if segs and s <= segs[-1][1] + 0.02: segs[-1][1] = max(segs[-1][1], e)
    else: segs.append([s, e])
pieces = []; newt = 0.0; mapping = []  # (orig_s, orig_e, new_s)
fade = int(0.008 * sr)
for k, (s, e) in enumerate(segs):
    x = a[int(s * sr):int(e * sr)].copy()
    x[:fade] *= np.linspace(0, 1, fade); x[-fade:] *= np.linspace(1, 0, fade)
    mapping.append((s, e, newt)); pieces.append(x); newt += len(x) / sr
    if k < len(segs) - 1:
        prev_word = [w for w in words if w["e"] <= e + 1e-6][-1]["w"]
        g = GAP_SENT if prev_word[-1] in ".,?!" else GAP_WORD
        pieces.append(np.zeros(int(g * sr), np.float32)); newt += g
cut = np.concatenate(pieces)
sf.write(dst + ".tmp.wav", cut, sr, subtype="FLOAT")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", dst + ".tmp.wav", "-af",
                f"rubberband=tempo={tempo}:pitch=1:transients=crisp:detector=compound:phase=laminar:window=standard:smoothing=off:formant=preserved:pitchq=quality:channels=together",
                "-c:a", "pcm_f32le", dst], check=True)
def remap(t):
    for s, e, n in mapping:
        if s - 1e-6 <= t <= e + 1e-6: return (n + (t - s)) / tempo
    # in a gap: snap to the next segment start
    for s, e, n in mapping:
        if t < s: return n / tempo
    return newt / tempo
nw = [dict(w=w["w"], s=round(remap(w["s"]), 3), e=round(remap(w["e"]), 3)) for w in words]
json.dump(nw, open(wout, "w"), ensure_ascii=False, indent=0)
print("orig", len(a) / sr, "cut", newt, "final", newt / tempo)
print(" ".join(f"{w['w']}@{w['s']:.2f}" for w in nw))
