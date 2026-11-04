"""Minimalist-modern sound design for video 3: clean UI SFX + a 96 bpm pluck/soft-beat bed, mixed under the voice.
Usage: python3 -I make_audio_lux.py VOICE.wav OUT_DIR      (needs OUT_DIR/sfx_cues.json)
Writes OUT_DIR/sfx/*.wav, OUT_DIR/music.wav, OUT_DIR/mix_raw.wav (stereo 48 kHz)."""
import json, os, sys, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(11)
voice_path, out = sys.argv[1:3]
os.makedirs(f"{out}/sfx", exist_ok=True)

def t(d): return np.arange(int(d * SR)) / SR
def norm(x, g=0.9): return x / (np.max(np.abs(x)) + 1e-9) * g
def onepole(x, k):
    y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x):
        s += k * (v - s); y[i] = s
    return y
def lp_fft(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / fc) ** 4)
    return np.fft.irfft(X, len(x))
def hp_fft(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 - 1 / (1 + (f / fc) ** 4)
    return np.fft.irfft(X, len(x))
def reverb(x, decay=2.8, mix=0.35, seed=3):
    """Stereo reverb: convolve with two decorrelated exponentially-decaying noise tails."""
    r = np.random.default_rng(seed)
    n = int(decay * SR); tt = np.arange(n) / SR
    outs = []
    for ch in range(2):
        ir = r.standard_normal(n) * np.exp(-tt * 6.9 / decay)
        ir = lp_fft(ir, 6000); ir /= np.sqrt(np.sum(ir ** 2))
        L = len(x) + n
        y = np.fft.irfft(np.fft.rfft(x, L) * np.fft.rfft(ir, L), L)[:len(x) + n]
        outs.append(y)
    wet = np.stack(outs, 1)
    dry = np.pad(np.stack([x, x], 1), ((0, n), (0, 0)))
    return dry * (1 - mix) + wet * mix
def save(name, x):
    x = np.clip(x, -1, 1)
    if x.ndim == 1: x = np.stack([x, x], 1)
    with wave.open(name, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())
def load(name):
    with wave.open(name) as w:
        ch = w.getnchannels(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16) / 32768
    x = x.reshape(-1, ch)
    return x if ch == 2 else np.repeat(x, 2, 1)

# ---------------- SFX (soft, expensive-sounding) ----------------
S = {}
d = 1.1; x = t(d); n = rng.standard_normal(len(x))
S["swoosh"] = lp_fft(n, 900) * np.sin(np.pi * x / d) ** 3
S["swoosh"] = norm(reverb(S["swoosh"], 1.2, 0.3)[:, 0], 0.5)
d = 2.6; x = t(d)
sub = np.sin(2 * np.pi * np.cumsum(38 + 50 * np.exp(-x * 4)) / SR) * np.exp(-x * 1.6)
thump = lp_fft(rng.standard_normal(len(x)), 300) * np.exp(-x * 9) * 0.5
S["boom"] = norm(reverb(sub + thump, 2.4, 0.25)[:len(x), 0], 0.95)
d = 3.0; x = t(d)
chime = sum(a * np.sin(2 * np.pi * f * x) * np.exp(-x * dk) for f, a, dk in
            [(1318.5, 1, 1.6), (1975.5, .6, 2.2), (2637, .4, 2.8), (3951, .2, 3.6), (5274, .1, 4.5)])
chime *= np.minimum(1, x / 0.003)
S["chime"] = norm(reverb(chime, 3.0, 0.45)[:len(x), 0], 0.45)
d = 2.2; x = t(d); sh = np.zeros(len(x))
for i in range(22):
    st = int(rng.uniform(0, 1.4) * SR); fr = rng.uniform(4000, 9000); L = int(0.35 * SR)
    seg = np.sin(2 * np.pi * fr * np.arange(L) / SR) * np.exp(-np.arange(L) / SR * 9)
    sh[st:st + L] += seg[:len(sh) - st] * rng.uniform(.3, 1)
S["shimmer"] = norm(reverb(sh * np.minimum(1, x / 0.6), 2.0, 0.5)[:len(x), 0], 0.3)
d = 0.12; x = t(d)
S["tick"] = norm(np.sin(2 * np.pi * 3200 * x) * np.exp(-x * 90) + hp_fft(rng.standard_normal(len(x)), 4000) * np.exp(-x * 200) * .3, 0.35)
d = 2.4; x = t(d); f = 120 + 1100 * (x / d) ** 2.2
rs = (np.sin(2 * np.pi * np.cumsum(f) / SR) * .25 + lp_fft(rng.standard_normal(len(x)), 2500) * .75) * (x / d) ** 2.5
S["riser"] = norm(reverb(rs, 1.5, 0.3)[:len(x), 0], 0.45)
d = 0.8; x = t(d)
S["pop"] = norm(reverb(np.sin(2 * np.pi * np.cumsum(700 * np.exp(-x * 30) + 220) / SR) * np.exp(-x * 40), 0.8, .3)[:len(x), 0], 0.4)
d = 1.0; x = t(d); fz = np.zeros(len(x))
for i in range(14):
    st = int(rng.uniform(0, .6) * SR); L = int(.07 * SR); fr = rng.uniform(600, 1600); xx = np.arange(L) / SR
    fz[st:st + L] += (np.sin(2 * np.pi * np.cumsum(fr * np.exp(-xx * 30) + 260) / SR) * np.exp(-xx * 55))[:len(fz) - st]
S["foam"] = norm(reverb(fz, 0.9, 0.25)[:len(x), 0], 0.4)
d = 0.25; x = t(d)
S["click"] = norm(hp_fft(rng.standard_normal(len(x)), 1500) * np.exp(-x * 160) + np.sin(2 * np.pi * 1800 * x) * np.exp(-x * 120), 0.5)
for k_, v in S.items(): save(f"{out}/sfx/{k_}.wav", v)

# ---------------- MUSIC: 70 bpm felt piano + warm pads + sub swells ----------------
voice = load(voice_path)
L = len(voice) + int(1.5 * SR)
bpm = 96; beat = 60 / bpm
mono = np.zeros(L)
mid = lambda m: 440 * 2 ** ((m - 69) / 12)
def put(buf, start, sig, g=1.0):
    i = int(start * SR)
    if i >= len(buf): return
    sig = sig[:len(buf) - i]; buf[i:i + len(sig)] += sig * g
def piano(fr, d=2.5):
    x = t(d)
    s = sum(a * np.sin(2 * np.pi * fr * h * x + h) * np.exp(-x * (1.2 + h * 0.9)) for h, a in [(1, 1), (2, .45), (3, .18), (4, .08)])
    return lp_fft(s * np.minimum(1, x / 0.004), 3500)
def pad(fr, d):
    x = t(d)
    s = sum(np.sin(2 * np.pi * fr * dt * x) for dt in (1, 1.003, 0.997, 2.0)) * 0.25
    return lp_fft(s * np.minimum(1, x / 1.2) * np.minimum(1, (d - x) / 1.2), 1800)
# Cmaj9 - Am9 - Fmaj7(#11) - Gsus
prog = [(48, [64, 67, 71, 74]), (45, [60, 64, 67, 71]), (41, [57, 60, 64, 69]), (43, [62, 67, 69, 74])]
bar = 4 * beat
nb = int(L / SR / bar) + 1
arp = [0, 2, 1, 3, 2, 1, 3, 2]
for b in range(nb):
    t0 = b * bar; root, ch = prog[b % 4]
    put(mono, t0, pad(mid(root), bar + 1.0), 0.12)
    for nn in ch: put(mono, t0, pad(mid(nn), bar + 1.0), 0.05)
    for i, ai in enumerate(arp):
        put(mono, t0 + i * beat / 2, piano(mid(ch[ai] + 12)), 0.10 if i % 2 == 0 else 0.07)
    if b >= 1:  # clean modern groove after the intro bar
        x = t(0.4); kick = np.sin(2 * np.pi * np.cumsum(45 + 90 * np.exp(-x * 30)) / SR) * np.exp(-x * 9)
        xh = t(0.05); hat = hp_fft(rng.standard_normal(len(xh)), 7000) * np.exp(-xh * 120)
        xc = t(0.18); clap = hp_fft(lp_fft(rng.standard_normal(len(xc)), 5000), 900) * np.exp(-xc * 28)
        for q in range(4):
            put(mono, t0 + q * beat, kick, 0.34 if q % 2 == 0 else 0.0)
            put(mono, t0 + q * beat + beat / 2, hat, 0.10); put(mono, t0 + q * beat + beat * 0.75, hat, 0.05)
            if q in (1, 3): put(mono, t0 + q * beat, clap, 0.16)
music = reverb(mono, 1.6, 0.25)[:L]
tt = np.arange(L) / SR
music *= (np.minimum(1, tt / 2.0) * np.minimum(1, np.maximum(0, (L / SR - tt) / 2.5)))[:, None]
save(f"{out}/music.wav", norm(music, 0.8))

# ---------------- MIX ----------------
cues = json.load(open(f"{out}/sfx_cues.json"))
mix = np.zeros((L, 2)); mix[:len(voice)] += voice
vm = np.abs(voice[:, 0]); win = int(0.2 * SR)
env = np.pad(np.convolve(vm, np.ones(win) / win, "same"), (0, L - len(vm)))
duck = np.where(env > 0.02, 0.26, 0.5)
duck = np.convolve(duck, np.ones(int(0.35 * SR)) / int(0.35 * SR), "same")
mix += norm(music, 0.8) * duck[:, None] * 0.55
for c in cues:
    s = load(f"{out}/sfx/{c['sfx']}.wav"); i = int(c["t"] * SR)
    if i < L:
        s = s[:L - i]; mix[i:i + len(s)] += s * c.get("gain", 0.6)
mix = np.tanh(mix / max(np.max(np.abs(mix)), 1e-9) * 1.1) * 0.92
save(f"{out}/mix_raw.wav", mix)
print("done", L / SR)
