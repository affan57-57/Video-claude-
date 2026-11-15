"""Edit decision list for the voice: cut awkward pauses, speed up, and map word times to film time.
Writes captions.json (chunks of words in film time) and edl.json (segments for the audio cut)."""
import json, sys
W = json.load(open(sys.argv[1])); outdir = sys.argv[2]
SPEED = 1.10
VOICE_AT = 0.25          # film time where the voice starts
# kept segments of the original recording (seconds) -- sentence-level, pauses removed
SEGS = [(0.00, 7.30), (7.40, 10.90), (11.15, 14.80), (15.20, 18.00), (18.30, 20.05), (20.08, 23.80)]
starts = []; t = VOICE_AT
for a, b in SEGS:
    starts.append(t); t += (b - a) / SPEED
END = t
def film(x):
    for (a, b), s in zip(SEGS, starts):
        if a - 0.1 <= x <= b + 0.1: return round(s + (min(max(x, a), b) - a) / SPEED, 3)
    raise ValueError(x)

FIX = {"Fresh": "FRESCURA", "Cura": None, "Body": "BODY", "berkenaan.": "berkenan.", "terhat.": "terhad.",
       "kulit": "kulit", "check": "checkout", "out": None, "Bio.": "Bio."}
words = []
for i, w in enumerate(W):
    txt = w["w"].strip()
    if txt == "kulit" and W[i - 1]["w"].strip() == "beg": txt = "kuning"
    elif txt in FIX:
        if FIX[txt] is None:  # merged into previous token
            words[-1]["e"] = film(w["e"]); continue
        txt = FIX[txt]
    words.append(dict(t=txt, s=film(w["s"]), e=film(w["e"])))
if "-sangat" in [x["t"] for x in words]:
    j = [x["t"] for x in words].index("-sangat"); words[j - 1]["t"] += "-sangat"; words[j - 1]["e"] = words[j]["e"]; del words[j]

CHUNKS = [4, 4, 2, 3, 4, 4, 4, 5, 4, 3, 4, 3, 4, 3, 3, 3]
caps = []; k = 0
for n in CHUNKS:
    grp = words[k:k + n]; k += n
    caps.append(dict(s=grp[0]["s"], e=grp[-1]["e"], w=grp))
assert k == len(words), (k, len(words), [x["t"] for x in words[k:]])
for i in range(len(caps) - 1): caps[i]["e"] = min(caps[i + 1]["s"], caps[i]["e"] + 0.25)
json.dump(caps, open(f"{outdir}/captions.json", "w"), ensure_ascii=False)
json.dump(dict(speed=SPEED, voice_at=VOICE_AT, segs=SEGS, end=round(END, 3)), open(f"{outdir}/edl.json", "w"))
for c in caps: print(f"{c['s']:6.2f}-{c['e']:6.2f}  " + " ".join(f"{x['t']}@{x['s']}" for x in c["w"]))
print("voice ends", round(END, 2))
