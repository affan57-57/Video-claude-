"""Mix voice, sound effects and the ducked music bed from cues.json into assets/audio/master.wav.

usage: python scripts/mix.py   (run from the project folder; then loudness is set by ffmpeg)
"""
import json, subprocess
import numpy as np, soundfile as sf

SR = 48000
cfg = json.load(open("cues.json"))
N = int(cfg["duration"] * SR)
mix = np.zeros((N, 2))
db = lambda g: 10 ** (g / 20)


def load(p):
    a, sr = sf.read(p, dtype="float64", always_2d=True)
    assert sr == SR, (p, sr)
    return a if a.shape[1] == 2 else np.repeat(a, 2, 1)


def place(a, at, g):
    i = int(at * SR)
    a = a[:max(0, N - i)]
    mix[i:i + len(a)] += a * g


# voice + a 0/1 activity mask for ducking
speech = np.zeros(N)
for v in cfg["voice"]:
    a = load(v["src"])
    place(a, v["at"], db(v["gain_db"]))
    i = int(v["at"] * SR)
    speech[i:i + len(a)] = 1

for name, at, g in cfg["sfx"]:
    place(load(f"assets/audio/sfx/{name}.wav"), at, db(g))

# music: smooth ducking under speech (80 ms attack, 350 ms release)
m = cfg["music"]
mus = load(m["src"])[:N]
env = np.where(speech[:len(mus)] > 0, db(m["duck_db"]), db(m["bed_db"]))
k = int(0.35 * SR)
env = np.convolve(np.pad(env, (k, k), mode="edge"), np.ones(k) / k, mode="same")[k:-k]
mix[:len(mus)] += mus * env[:, None]

sf.write("assets/audio/premaster.wav", mix.astype(np.float32), SR, subtype="FLOAT")
# loud, punchy social-media master: -11 LUFS, true peak -1 dB
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "assets/audio/premaster.wav", "-af",
                "acompressor=threshold=-16dB:ratio=2:attack=10:release=150:makeup=1dB,"
                "loudnorm=I=-11:TP=-1.0:LRA=8,alimiter=limit=0.89:level=false,aresample=48000",
                "-c:a", "pcm_s24le", "assets/audio/master.wav"], check=True)
print("wrote assets/audio/master.wav", cfg["duration"], "s")
