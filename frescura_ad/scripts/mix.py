# Build final mix: cleaned voices (EDL + tempo + studio chain) + ducked music + SFX.
# usage: python mix.py WORKDIR OUT.wav
import sys, os, subprocess, numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(__file__))
from timeline import *

W = sys.argv[1]; OUT = sys.argv[2]; SR = 48000
def run(*a): subprocess.run(a, check=True)
CHAIN = ("highpass=f=85:poles=2,equalizer=f=250:t=q:w=1.0:g=-3,equalizer=f=120:t=q:w=1.0:g=1.5,"
         "equalizer=f=3000:t=q:w=1.2:g=3,equalizer=f=5500:t=q:w=1.2:g=1.5,highshelf=f=10000:g=2,"
         "deesser=i=0.35:m=0.5:f=0.5,acompressor=threshold=-22dB:ratio=3:attack=6:release=110:knee=4:makeup=3dB")

def lufs(path):
    r = subprocess.run(["ffmpeg", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float([l for l in r.splitlines() if l.strip().startswith("I:")][-1].split()[1])

def fade(x, ms=12):
    n = int(SR * ms / 1000); x = x.copy(); r = np.linspace(0, 1, n)
    x[:n] *= r; x[-n:] *= r[::-1]; return x

# --- main VO: tempo whole file, then cut ---
run("ffmpeg", "-v", "error", "-y", "-i", f"{W}/main_clean_full.wav", "-af", f"rubberband=tempo={MAIN_TEMPO}:pitchq=quality:formant=preserved,{CHAIN}", "-ar", "48000", "-ac", "1", "-c:a", "pcm_f32le", f"{W}/main_fast.wav")
main, _ = sf.read(f"{W}/main_fast.wav", dtype="float32")
# --- feedback: cut segments then tempo ---
fb_raw, _ = sf.read(f"{W}/feedback_clean_full.wav", dtype="float32")
fbc = np.concatenate([fade(fb_raw[int(a * SR):int(b * SR)]) for a, b in FB_SEGS])
sf.write(f"{W}/fb_cut.wav", fbc, SR, subtype="FLOAT")
run("ffmpeg", "-v", "error", "-y", "-i", f"{W}/fb_cut.wav", "-af", f"rubberband=tempo={FB_TEMPO}:pitchq=quality:formant=preserved,{CHAIN}", "-ar", "48000", "-ac", "1", "-c:a", "pcm_f32le", f"{W}/fb_fast.wav")
fb, _ = sf.read(f"{W}/fb_fast.wav", dtype="float32")

# loudness match: both voices to -14 LUFS before mix
for name in ["main_fast", "fb_fast"]:
    pass
gm = 10 ** ((-14 - lufs(f"{W}/main_fast.wav")) / 20); gf = 10 ** ((-14.5 - lufs(f"{W}/fb_fast.wav")) / 20)
main *= gm; fb *= gf

N = int(TOTAL * SR) + SR
voice = np.zeros(N, np.float32)
for a, b, o in MAIN_SEGS:
    s = fade(main[int(a / MAIN_TEMPO * SR):int(b / MAIN_TEMPO * SR)]); i = int(o * SR); voice[i:i + len(s)] += s
i = int(FB_OUT * SR); voice[i:i + len(fb)] += fade(fb)

# --- music with ducking ---
mus, msr = sf.read(f"{W}/sfx/music.wav", dtype="float32"); assert msr == SR
mus = np.pad(mus, ((0, max(0, N - len(mus))), (0, 0)))[:N]
env = np.sqrt(np.convolve(voice ** 2, np.ones(int(.03 * SR)) / int(.03 * SR), mode="same"))
act = (env > 10 ** (-38 / 20)).astype(np.float32)
# attack 40ms / release 350ms smoothing
g = np.zeros_like(act); a_c = np.exp(-1 / (0.04 * SR)); r_c = np.exp(-1 / (0.35 * SR)); y = 0.0
for k in range(N):
    x = act[k]; c = a_c if x > y else r_c; y = c * y + (1 - c) * x; g[k] = y
mus_gain_db = -15 - 9 * g  # -15 dB bed in gaps, -24 dB under speech
t = np.arange(N) / SR
mus_gain_db += np.where((t > EDU[0]) & (t < EDU[1]), 4, 0) + np.where(t > END[0], 4, 0)
mus = mus * (10 ** (mus_gain_db / 20))[:, None]
mus *= np.clip((TOTAL - t) / 1.0, 0, 1)[:, None]  # fade out last 1 s
mus *= np.clip(t / 0.05, 0, 1)[:, None]

mix = np.stack([voice, voice], 1) + mus
for name, at, gdb in sfx_cues():
    if gdb < -60: continue
    s, _ = sf.read(f"{W}/sfx/{name}.wav", dtype="float32")
    i = int(max(at, 0) * SR); L = min(len(s), N - i)
    mix[i:i + L] += s[:L] * 10 ** (gdb / 20)
mix = mix[:int(TOTAL * SR)]
sf.write(f"{W}/premix.wav", mix, SR, subtype="FLOAT")
# loud & punchy master: -11 LUFS integrated, true-peak -1 dB
run("ffmpeg", "-v", "error", "-y", "-i", f"{W}/premix.wav", "-af",
    "acompressor=threshold=-14dB:ratio=2:attack=10:release=150:makeup=1dB,loudnorm=I=-11:TP=-1.0:LRA=6,alimiter=limit=0.89:attack=1:release=40:level=false,aresample=48000",
    "-c:a", "pcm_s16le", OUT)
print("voice gains", gm, gf, "final LUFS", lufs(OUT))
