# Build the final mix: cleaned voice (studio chain, cut, sped) + SFX + ducked music bed.
# Usage: python frescura_audio.py WORK_DIR OUT_WAV
#   WORK_DIR must contain awareness.df.wav, feedback.df.wav (Demucs + DeepFilterNet3 output, 48 kHz mono)
#   and sfx/*.wav (from frescura_sfx.py).
import sys, os, subprocess, numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(__file__))
from frescura_edl import SPEECH, SFX, DURATION

W, OUT = sys.argv[1], sys.argv[2]; SR = 48000
SRC = {"aw": f"{W}/awareness.df.wav", "fb": f"{W}/feedback.df.wav"}
# studio voice: clean low end, de-mud, presence, air, de-ess, two-stage compression
STUDIO = ("highpass=f=85:poles=2,equalizer=f=220:t=q:w=1.0:g=-2.5,equalizer=f=450:t=q:w=1.4:g=-1.5,"
          "equalizer=f=3000:t=q:w=1.0:g=3,equalizer=f=5500:t=q:w=1.2:g=1.5,highshelf=f=10000:g=2.5,"
          "deesser=i=0.35:m=0.5:f=0.5,acompressor=threshold=-24dB:ratio=3:attack=6:release=110:knee=4:makeup=3dB,"
          "acompressor=threshold=-12dB:ratio=6:attack=2:release=60:makeup=1dB")

def ff(args): subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)

voice = np.zeros(int(DURATION * SR))
os.makedirs(f"{W}/segs", exist_ok=True)
for name, path in SRC.items():                  # studio chain + per-source loudness match
    ff(["-i", path, "-af", f"{STUDIO},loudnorm=I=-14:TP=-2:LRA=6:linear=true,aresample={SR}", "-ac", "1", "-c:a", "pcm_f32le", f"{W}/{name}.studio.wav"])
for i, (t0, src, a, b, tempo) in enumerate(SPEECH):
    seg = f"{W}/segs/{i:02d}.wav"
    af = f"atrim={a}:{b},asetpts=PTS-STARTPTS" + (f",atempo={tempo}" if tempo != 1 else "") + ",afade=t=in:d=0.012"
    ff(["-i", f"{W}/{src}.studio.wav", "-af", af, "-c:a", "pcm_f32le", seg])
    x, _ = sf.read(seg); n = len(x); fo = int(0.03 * SR); x[-fo:] *= np.linspace(1, 0, fo)
    s = int(t0 * SR); voice[s:s + n] += x[:len(voice) - s]
    print(f"seg {i}: {src} {a}-{b} -> {t0:.2f}-{t0 + n / SR:.2f}")

st = lambda x: np.stack([x, x], 1)
sfx = np.zeros((len(voice), 2))
for t, name, g in SFX:
    x, sr = sf.read(f"{W}/sfx/{name}.wav"); assert sr == SR
    s = int(t * SR); n = min(len(x), len(sfx) - s); sfx[s:s + n] += x[:n] * 10 ** (g / 20)

music, _ = sf.read(f"{W}/sfx/music.wav"); music = music[:len(voice)]
music = np.concatenate([music, np.zeros((len(voice) - len(music), 2))])
# sidechain-style ducking from the voice envelope (attack 40 ms, release 350 ms)
env = np.abs(voice); h = int(0.01 * SR); blk = np.array([env[i:i + h].max() for i in range(0, len(env), h)])
g = np.zeros_like(blk); cur = 0
for i, v in enumerate(blk):
    tgt = 1.0 if v > 0.02 else 0.0
    cur += (tgt - cur) * (0.25 if tgt > cur else 0.03); g[i] = cur
duck = np.repeat(g, h)[:len(voice)]
mgain = 10 ** (-17 / 20) * (1 - duck * (1 - 10 ** (-9 / 20)))      # bed -17 dB, ducks a further 9 dB under voice
end = int(30.2 * SR); fade = np.ones(len(voice)); fade[end:] = np.linspace(1, 0, len(voice) - end) ** 1.5
mix = st(voice) * 1.0 + sfx + music * (mgain * fade)[:, None]
sf.write(f"{W}/premaster.wav", mix.astype(np.float32), SR, subtype="FLOAT")
ff(["-i", f"{W}/premaster.wav", "-af", "loudnorm=I=-12:TP=-1.2:LRA=8:linear=false,alimiter=limit=0.89:attack=3:release=60:level=false,aresample=48000",
    "-c:a", "pcm_s16le", OUT])
print("wrote", OUT)
