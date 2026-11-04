"""Replace words in the edited voice with newly recorded phrases (studio-processed and level-matched).
Usage: python3 -I splice_voice.py VOICE.wav NEW_RECORDING.mp4 RNNOISE_MODEL OUT_DIR
Writes OUT_DIR/voice.wav (new voice) and OUT_DIR/inserts.json ([[at_old_time, +seconds], ...]) for timeline remapping."""
import json, subprocess, sys, wave
import numpy as np

voice_p, new_p, model, out = sys.argv[1:5]
SR = 48000
# (old_start, old_end_guess, snap_window, new_start, new_end, label, pause_after)
#  old_*: region in VOICE.wav to replace;  new_*: phrase in NEW_RECORDING (take 2)
REPL = [
    (20.80, 21.50, (21.40, 21.62), 5.16, 7.30, "Woman Glory -> Woman Glory by Bombshell", 0.10),
    (24.50, 25.04, (24.99, 25.08), 8.14, 10.14, "Noche -> Noche by Midnight Fantasy", 0.22),
]
CHAIN = ",".join([
    "highpass=f=85", "dynaudnorm=f=150:g=9:p=0.85:m=12:r=0.3", f"arnndn=m={model}:mix=0.9",
    "afftdn=nr=10:nf=-40:tn=1", "equalizer=f=250:t=q:w=1.2:g=-3", "equalizer=f=120:t=q:w=1:g=2",
    "equalizer=f=3500:t=q:w=1.5:g=3", "highshelf=f=9000:g=2.5", "deesser=i=0.4",
    "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3", "alimiter=limit=0.89",
])

def rd(p):
    with wave.open(p) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
def wr(p, x):
    with wave.open(p, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
def speech_rms(x):
    fr = x[:len(x) // 960 * 960].reshape(-1, 960); r = np.sqrt(np.mean(fr ** 2, 1))
    return np.sqrt(np.mean(np.sort(r)[len(r) // 2:] ** 2))
def snap(x, lo, hi):
    h = SR // 100; best, bt = 1e9, lo
    for k in range(int(lo * 100), int(hi * 100) + 1):
        e = float(np.mean(x[k * h:(k + 1) * h] ** 2))
        if e < best: best, bt = e, k / 100
    return bt
def trim_silence(x, thr_db=-38):
    h = SR // 100
    db = np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + h] ** 2)) + 1e-9) for i in range(0, len(x) - h, h)])
    on = np.where(db > thr_db)[0]
    return x[max(on[0] - 3, 0) * h:(on[-1] + 4) * h]

voice = rd(voice_p)
# studio-process the new recording once, at 48 kHz mono
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", new_p, "-vn", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                     capture_output=True, check=True).stdout
src = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
src *= min(10 ** (-20 / 20) / (speech_rms(src) + 1e-9), 6.0)
wr(f"{out}/new_pre.wav", src)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{out}/new_pre.wav", "-af", CHAIN, "-ar", str(SR), "-ac", "1",
                f"{out}/new_proc.wav"], check=True)
proc = rd(f"{out}/new_proc.wav")
target = speech_rms(voice[int(18 * SR):int(28 * SR)])

xf = int(0.015 * SR)
pieces, inserts, pos = [], [], 0.0
for a, b_guess, (lo, hi), ns, ne, label, pause in REPL:
    gap = np.zeros(int(pause * SR), np.float32)
    b = snap(voice, lo, hi)
    ph = trim_silence(proc[int(ns * SR):int(ne * SR)].copy())
    ph *= target / (speech_rms(ph) + 1e-9)
    r = np.linspace(0, 1, xf); ph[:xf] *= r; ph[-xf:] *= r[::-1]
    pieces.append(voice[int(pos * SR):int(a * SR)])
    new_seg = np.concatenate([ph, gap])
    pieces.append(new_seg)
    inserts.append([round(a, 3), round(b, 3), round(len(new_seg) / SR - (b - a), 3)])
    print(f"{label}: replaced {a:.2f}-{b:.2f}s ({b-a:.2f}s) with {len(new_seg)/SR:.2f}s")
    pos = b
pieces.append(voice[int(pos * SR):])
outv = pieces[0]
for p_ in pieces[1:]:
    r = np.linspace(0, 1, xf)
    outv = np.concatenate([outv[:-xf], outv[-xf:] * r[::-1] + p_[:xf] * r, p_[xf:]])
wr(f"{out}/voice.wav", outv)
json.dump(inserts, open(f"{out}/inserts.json", "w"))
print("new duration", len(outv) / SR)
