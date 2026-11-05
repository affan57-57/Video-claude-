"""Cut awkward pauses/repeats from the source voice and make it sound studio-clean.
Usage: python3 -I edit_audio.py SOURCE.mp4 RNNOISE_MODEL OUT_DIR [CUTS.json]
  CUTS.json (optional): {"keep": [[start, end, label], ...], "keep_gap": 0.08}
Writes OUT_DIR/voice.wav (48k mono, enhanced, -14 LUFS), OUT_DIR/edl.json and
OUT_DIR/remap.json (pauses removed by tightening, in the pre-tightening timeline)."""
import json, subprocess, sys, wave
import numpy as np

src, model, out = sys.argv[1:4]

# (source_start, source_end, label) -- kept ranges, in playback order.
KEEP = [
    (16.33, 18.72, "HOOK: bau dia macam perfume mewah"),
    (0.30, 6.90,   "Biasanya mandi sabun gel / sabun buku... yang ni keluar foaming"),
    # cut 6.90-8.04 repeat "keluar foaming", 8.04-11.10 filler intro
    (11.10, 15.64, "Bukan sahaja berbuih lembut... gebu-gebu"),
    # 15.64-18.72 already used as hook
    (18.72, 29.68, "Keistimewaan: foaming + wangian ala perfume, tekan je pam"),
    # cut 29.68-30.90 repeat "tak payah berbuih"
    (30.90, 34.30, "Dua pilihan wangian: Woman Glory"),
    # cut 34.30-35.58 "dan" + 1s awkward pause
    (35.58, 66.10, "Noce, floral vs fruity, tanpa paraben, ujian, CTA"),
    # cut 66.10-67.46 repeated "tekan beg kuning sekarang"
    (67.46, 70.66, "Pilih wangian favourite, cepat check out"),
]

if len(sys.argv) > 4:
    _cfg = json.load(open(sys.argv[4]))
    KEEP = [tuple(k) for k in _cfg["keep"]]
    _KEEP_GAP = _cfg.get("keep_gap", 0.08)
    _QUIET_DB = _cfg.get("quiet_db", -34)       # pause threshold; raise it for noisy locations
else:
    _KEEP_GAP = 0.08
    _QUIET_DB = -34

SR = 48000
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR),
                      "-f", "s16le", "-"], capture_output=True, check=True).stdout
a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768

def snap(t, win=0.12):
    """Move a cut point to the quietest 10 ms within +-win seconds."""
    h = SR // 100
    best, bt = 1e9, t
    for k in range(int((t - win) * 100), int((t + win) * 100) + 1):
        i = k * h
        if i < 0 or i + h > len(a):
            continue
        e = float(np.mean(a[i:i + h] ** 2))
        if e < best:
            best, bt = e, k / 100
    return bt

fade = int(0.012 * SR)
pieces, edl, t = [], [], 0.0
for s, e, label in KEEP:
    s2 = snap(s, 0.04 if s == 16.33 else 0.12)
    e2 = snap(e)
    seg = a[int(s2 * SR):int(e2 * SR)].copy()
    # level-match: bring each kept segment's speech (loudest half of 20 ms frames) to -20 dBFS,
    # the opening of the recording was ~10 dB quieter than the rest
    fr = seg[:len(seg) // 960 * 960].reshape(-1, 960)
    rms = np.sqrt(np.mean(fr ** 2, 1))
    speech = np.sqrt(np.mean(np.sort(rms)[len(rms) // 2:] ** 2))
    seg *= min(10 ** (-20 / 20) / (speech + 1e-9), 6.0)
    ramp = np.linspace(0, 1, fade)
    seg[:fade] *= ramp
    seg[-fade:] *= ramp[::-1]
    pieces.append(seg)
    edl.append({"src_start": s2, "src_end": e2, "out_start": round(t, 3),
                "out_end": round(t + (e2 - s2), 3), "label": label})
    t += e2 - s2
cut = np.concatenate(pieces)

tmp = f"{out}/voice_cut.wav"
with wave.open(tmp, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(cut, -1, 1) * 32767).astype(np.int16).tobytes())

# Studio chain: rumble cut -> RNN denoise -> residual FFT denoise -> EQ (mud cut,
# presence, air) -> de-ess -> compression -> level evening -> broadcast loudness.
chain = ",".join([
    "highpass=f=85",
    "dynaudnorm=f=150:g=9:p=0.85:m=12:r=0.3",
    f"arnndn=m={model}:mix=0.9",
    "afftdn=nr=10:nf=-40:tn=1",
    "equalizer=f=250:t=q:w=1.2:g=-3",
    "equalizer=f=120:t=q:w=1:g=2",
    "equalizer=f=3500:t=q:w=1.5:g=3",
    "highshelf=f=9000:g=2.5",
    "deesser=i=0.4",
    "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3",
    "dynaudnorm=f=250:g=15:p=0.9:m=8",
    "alimiter=limit=0.89",
    "loudnorm=I=-14:TP=-1.5:LRA=7",
    "aresample=48000",
])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", chain,
                "-ar", "48000", "-ac", "1", f"{out}/voice_enh.wav"], check=True)

# ---- tighten pauses: any gap quieter than QUIET_DB (default -34 dBFS) longer than 0.20 s is shrunk to KEEP_GAP
with wave.open(f"{out}/voice_enh.wav") as w:
    v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
h = SR // 100
db = np.array([20 * np.log10(np.sqrt(np.mean(v[i:i + h] ** 2)) + 1e-9) for i in range(0, len(v) - h, h)])
quiet = db < _QUIET_DB
gaps, i = [], 0
while i < len(quiet):
    if quiet[i]:
        j = i
        while j < len(quiet) and quiet[j]:
            j += 1
        if (j - i) / 100 > 0.20 and i > 0 and j < len(quiet):
            gaps.append((i / 100, j / 100))
        i = j
    else:
        i += 1
KEEP_GAP = _KEEP_GAP
pieces, removed, pos = [], [], 0.0
xf = int(0.01 * SR)
for a0, a1 in gaps:
    cut0 = a0 + KEEP_GAP / 2
    cut1 = a1 - KEEP_GAP / 2
    pieces.append(v[int(pos * SR):int(cut0 * SR)])
    removed.append([round(cut0, 3), round(cut1, 3)])
    pos = cut1
pieces.append(v[int(pos * SR):])
outv = pieces[0]
for p_ in pieces[1:]:            # 10 ms crossfade at each join
    r = np.linspace(0, 1, xf)
    outv = np.concatenate([outv[:-xf], outv[-xf:] * r[::-1] + p_[:xf] * r, p_[xf:]])
with wave.open(f"{out}/voice.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(outv, -1, 1) * 32767).astype(np.int16).tobytes())
json.dump(removed, open(f"{out}/remap.json", "w"))
print(f"tightened {len(removed)} pauses, removed {sum(b - a for a, b in removed):.2f}s:",
      removed)
json.dump({"duration": round(t, 3), "segments": edl}, open(f"{out}/edl.json", "w"), indent=1)
print(f"output duration {t:.2f}s")
for x in edl:
    print(x)
