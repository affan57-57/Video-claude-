"""Mix voice + SFX + ducked music bed for the Frescura Body ad.
Usage: python mix.py voice_studio.wav SFX_DIR cues.json OUT.wav"""
import sys, json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

VO, SFX, CUES, OUT = sys.argv[1:5]
SR, O, END = 48000, 0.30, 34.0
c = json.load(open(CUES))
N = int(END * SR)
mix = np.zeros((N, 2))
v, sr = sf.read(VO, dtype="float64"); assert sr == SR
v = v if v.ndim == 1 else v.mean(1)
vo = np.zeros(N); vo[int(O * SR):int(O * SR) + len(v)] = v[:N - int(O * SR)]
cache = {}
def S(name):
    if name not in cache: cache[name] = sf.read(f"{SFX}/{name}.wav", dtype="float64")[0]
    return cache[name]
def put(name, t, db):
    x = S(name) * 10 ** (db / 20); i = int(max(t, 0) * SR); j = min(N, i + len(x))
    if i < N: mix[i:j] += x[:j - i]

# scene cut times (same rule as build.py: 60 ms before the word)
b = lambda k: c[k] - 0.06
cues = [
    ("whoosh_s", 0.05, -8), ("impact", 0.22, -4), ("shimmer", 0.3, -16),
    ("whoosh", 1.45, -8), ("pop", c["hook_masa"], -12), ("shimmer", c["hook_masa"] + .4, -14),
    ("whoosh_l", b("self") - .15, -9), ("tap", c["mahal"] + .25, -6), ("thump", c["mahal"] + .25, -6), ("pop", c["mahal"] + .45, -10),
    ("whoosh", b("ianya") - .12, -8), ("bubbles", b("ianya") + .2, -12), ("drop", c["selesa"] - .1, -12),
    ("riser", b("fres") - 1.4, -12), ("impact", b("fres"), -5), ("shimmer", b("fres") + .05, -9),
    ("whoosh", b("garam") - .12, -8), ("drop", c["bahan"], -11),
    ("pop", c["kaya"], -9), ("pop", c["kaya"] + .14, -9), ("pop", c["kaya"] + .28, -9), ("tick", c["mineral"], -12),
    ("whoosh_s", b("sudah") - .08, -8), ("bubbles", b("sudah") + .3, -11), ("pop", c["kulit"], -11),
    ("whoosh", b("gab") - .12, -8), ("pop", c["perfume"] - .2, -9), ("rwhoosh", c["perfume"] - .05, -11),
    ("thump", c["perfume"] + .75, -6), ("shimmer", c["perfume"] + .8, -10),
    ("whoosh_s", b("setiap") - .08, -9), ("bubbles", b("setiap") + .1, -11), ("shimmer", c["manjakan"] - .3, -8),
    ("whoosh_l", b("pilih") - .15, -7), ("impact", b("pilih"), -10), ("tap", c["manis1"], -8), ("tap", c["serlah"], -8),
    ("whoosh", b("ataupun") - .05, -7), ("shimmer", c["noche"], -12),
    ("tap", c["manis2"], -8), ("tap", c["lembut"], -8), ("tap", c["misteri"], -8),
    ("swell", b("kamu") - 1.2, -14), ("whoosh", b("kamu") - .1, -10),
    ("whoosh", b("sekarang1") - .12, -8), ("thump", c["giliran"] - .05, -5), ("impact", c["giliran"] + .6, -6),
    ("whoosh_s", b("stok") - .06, -8), ("impact", c["terhad"] - .12, -6),
] + [("tick", b("stok") + .1 + k * .09, -10) for k in range(10)] + [
    ("whoosh", b("klik") - .12, -8), ("drop", c["tekan"] + .1, -8), ("pop", c["tekan"] + .45, -8),
    ("ding", c["kuning"], -9), ("pop", c["checkout"] - .15, -9), ("tap", c["sekarang2"], -4),
    ("swell", 30.9, -14), ("impact", 32.3, -5), ("shimmer", 32.35, -7), ("ding", 32.9, -14),
]
for n, t, db in cues: put(n, t, db)
sfx = mix.copy()

# music bed, side-chain ducked by the voice (-9 dB under speech)
bed = sf.read(f"{SFX}/bed.wav", dtype="float64")[0][:N]
env = np.abs(vo); sos = butter(1, 6, fs=SR, output="sos"); env = sosfilt(sos, env); env = env / (env.max() + 1e-9)
duck = 10 ** (-9 * np.clip(env * 6, 0, 1) / 20)
bed = bed * 10 ** (-17 / 20) * duck[:, None]

out = sfx + bed + np.stack([vo, vo], 1)
sf.write(OUT, out.astype(np.float32), SR, subtype="FLOAT")
print("cues", len(cues), "peak", np.abs(out).max())
