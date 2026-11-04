"""Synthesize SFX + a light background music bed, then mix with the voice.
Usage: python3 -I make_audio.py VOICE.wav OUT_DIR
Writes OUT_DIR/sfx/*.wav, OUT_DIR/music.wav and OUT_DIR/mix.wav (stereo, 48k)."""
import json, os, sys, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(7)
voice_path, out = sys.argv[1:3]
os.makedirs(f"{out}/sfx", exist_ok=True)

def t(d): return np.arange(int(d * SR)) / SR
def env(n, a=0.005, r=0.2):
    x = np.arange(n) / SR
    e = np.minimum(1, x / max(a, 1e-4)) * np.exp(-x / max(r, 1e-4))
    return e
def lp(x, k):  # cheap one-pole low-pass, k in 0..1
    y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x):
        s += k * (v - s); y[i] = s
    return y
def norm(x, g=0.9): return x / (np.max(np.abs(x)) + 1e-9) * g
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

# ---------------- SFX ----------------
S = {}
d = 0.55; n = rng.standard_normal(int(d*SR)); x = t(d)
k = np.linspace(0.02, 0.35, len(n)) ** 1.5
y = np.empty_like(n); s = 0
for i, v in enumerate(n): s += k[i]*(v - s); y[i] = s
S["whoosh"] = norm(y * np.sin(np.pi * x / d) ** 2, 0.7)
S["whoosh_rev"] = S["whoosh"][::-1].copy()
d = 0.12; x = t(d); f = 900 * np.exp(-x * 25) + 300
S["pop"] = norm(np.sin(2*np.pi*np.cumsum(f)/SR) * env(len(x), 0.001, 0.03), 0.8)
d = 1.4; x = t(d)
bell = sum(a*np.sin(2*np.pi*fr*x) * np.exp(-x*dec) for fr, a, dec in
           [(1568, 1, 3), (3136, .5, 5), (4704, .25, 8), (2093, .35, 4)])
S["ding"] = norm(bell * env(len(x), 0.002, 10), 0.6)
d = 0.05; x = t(d)
S["click"] = norm(rng.standard_normal(len(x)) * np.exp(-x*300) + np.sin(2*np.pi*2400*x)*np.exp(-x*200), 0.7)
d = 0.5; x = t(d); f = 180 + 120*np.sin(2*np.pi*9*x)*np.exp(-x*5) + 200*np.exp(-x*8)
S["boing"] = norm(np.sin(2*np.pi*np.cumsum(f)/SR) * env(len(x), 0.003, 0.18), 0.7)
d = 0.7; x = t(d); f = 120*np.exp(-x*6) + 45
thud = np.sin(2*np.pi*np.cumsum(f)/SR) * env(len(x), 0.001, 0.18)
S["impact"] = norm(thud + lp(rng.standard_normal(len(x)), 0.2) * np.exp(-x*30) * 0.6, 0.95)
d = 0.4; x = t(d)
S["stamp"] = norm(np.sin(2*np.pi*np.cumsum(90*np.exp(-x*10)+50)/SR)*env(len(x),0.001,0.08)
                  + lp(rng.standard_normal(len(x)), 0.5)*np.exp(-x*60)*0.8, 0.95)
d = 0.35; x = t(d)
S["error"] = norm(np.sign(np.sin(2*np.pi*140*x)) * 0.5 * env(len(x), 0.005, 0.25)
                  * (1 + 0.5*np.sign(np.sin(2*np.pi*14*x))), 0.45)
d = 1.0; x = t(d)
sp = np.zeros(len(x))
for i in range(14):
    st = int(rng.uniform(0, 0.75) * SR); fr = rng.uniform(3000, 7000); L = int(0.18*SR)
    seg = np.sin(2*np.pi*fr*np.arange(L)/SR) * np.exp(-np.arange(L)/SR*25)
    sp[st:st+L] += seg[:len(sp)-st]
S["sparkle"] = norm(sp, 0.35)
d = 1.6; x = t(d); f = 200 + 900 * (x/d)**2
S["riser"] = norm((np.sin(2*np.pi*np.cumsum(f)/SR)*0.4 + lp(rng.standard_normal(len(x)), 0.15)*0.6)
                  * (x/d)**2, 0.5)
d = 0.9; x = t(d)
ka = sum(np.sin(2*np.pi*fr*x)*np.exp(-x*6) for fr in (2637, 3520, 5274))
S["cash"] = norm(np.concatenate([np.zeros(int(.06*SR)), ka])[:len(x)] + np.pad(S["click"], (0, len(x)-len(S["click"]))), 0.55)
d = 0.6; x = t(d)
fz = np.zeros(len(x))
for i in range(10):
    st = int(rng.uniform(0, 0.45)*SR); L = int(0.06*SR); fr = rng.uniform(500, 1400)
    xx = np.arange(L)/SR; seg = np.sin(2*np.pi*np.cumsum(fr*np.exp(-xx*30)+250)/SR)*np.exp(-xx*60)
    fz[st:st+L] += seg[:len(fz)-st]
S["bubbles"] = norm(fz, 0.5)
d = 0.25; x = t(d)
S["tick"] = norm(np.sin(2*np.pi*1800*x)*np.exp(-x*80), 0.4)
for k_, v in S.items():
    if v is not None: save(f"{out}/sfx/{k_}.wav", v)

# ---------------- MUSIC (upbeat pluck-pop bed, 112 bpm) ----------------
voice = load(voice_path)
L = len(voice) + int(0.6 * SR)
bpm = 112; beat = 60 / bpm
music = np.zeros((L, 2))
def add(buf, start, sig, pan=0.0, g=1.0):
    i = int(start * SR)
    if i >= len(buf): return
    sig = sig[:len(buf) - i]
    buf[i:i+len(sig), 0] += sig * g * (1 - max(pan, 0))
    buf[i:i+len(sig), 1] += sig * g * (1 + min(pan, 0))
def note(fr, d, kind="pluck"):
    x = t(d)
    if kind == "pluck":
        s = (np.sin(2*np.pi*fr*x) + 0.4*np.sin(2*np.pi*2*fr*x) + 0.15*np.sin(2*np.pi*3*fr*x))
        return s * env(len(x), 0.003, 0.22)
    if kind == "pad":
        s = sum(np.sin(2*np.pi*fr*dt*x) for dt in (1, 1.004, 0.996, 2.001))
        a = np.minimum(1, x/0.3) * np.minimum(1, (d - x)/0.3)
        return s * a * 0.25
    if kind == "bass":
        return np.tanh(2*np.sin(2*np.pi*fr*x)) * env(len(x), 0.004, 0.35)
kick_x = t(0.35); kick = np.sin(2*np.pi*np.cumsum(50 + 110*np.exp(-kick_x*30))/SR) * np.exp(-kick_x*9)
hat_x = t(0.06); hat = np.diff(rng.standard_normal(len(hat_x)+1)) * np.exp(-hat_x*90) * 0.25
clap_x = t(0.2); clap = lp(rng.standard_normal(len(clap_x)), 0.6) * np.exp(-clap_x*25) * 0.35
mid = lambda m: 440 * 2 ** ((m - 69) / 12)
# I–V–vi–IV in C major
prog = [(60, 64, 67), (55, 59, 62), (57, 60, 64), (53, 57, 60)]
bars = int(L / SR / (4 * beat)) + 1
arp_pat = [0, 1, 2, 1, 2, 0, 1, 2]
for b in range(bars):
    t0 = b * 4 * beat
    ch = prog[b % 4]
    add(music, t0, note(mid(ch[0] - 12), 4 * beat, "pad"), 0, 0.10)
    for nn in ch[1:]:
        add(music, t0, note(mid(nn), 4 * beat, "pad"), 0, 0.06)
    for i in range(8):
        add(music, t0 + i * beat / 2, note(mid(ch[arp_pat[i]] + 12), 0.3), (-0.3 if i % 2 else 0.3), 0.07)
    for i in range(4):
        add(music, t0 + i*beat, note(mid(ch[0] - 24), beat*0.9, "bass"), 0, 0.12)
        add(music, t0 + i*beat, kick, 0, 0.32)
        add(music, t0 + i*beat + beat/2, hat, 0.2, 0.5)
        add(music, t0 + i*beat + beat*0.75, hat, -0.2, 0.3)
        if i in (1, 3): add(music, t0 + i*beat, clap, 0, 0.6)
music[:int(0.8*SR)] *= 0  # silence under the cold-open hook impact, music drops in after
fade_in = np.minimum(1, np.maximum(0, (np.arange(L)/SR - 0.8) / 0.4))
fade_out = np.minimum(1, np.maximum(0, (L/SR - np.arange(L)/SR) / 1.2))
music *= (fade_in * fade_out)[:, None]
save(f"{out}/music.wav", norm(music, 0.8))

# ---------------- MIX ----------------
cues = json.load(open(f"{out}/sfx_cues.json"))
mix = np.zeros((L, 2))
mix[:len(voice)] += voice * 1.0
# sidechain-style ducking: music sits ~-20 dB under speech, rises in gaps
vm = np.abs(voice[:, 0]); win = int(0.15 * SR)
envv = np.convolve(vm, np.ones(win)/win, "same")
envv = np.pad(envv, (0, L - len(envv)))
duck = np.where(envv > 0.02, 0.22, 0.45)
duck = np.convolve(duck, np.ones(int(0.25*SR))/int(0.25*SR), "same")
mix += norm(music, 0.8) * duck[:, None] * 0.55
for c in cues:
    s = load(f"{out}/sfx/{c['sfx']}.wav")
    add(mix, c["t"], s[:, 0], c.get("pan", 0), c.get("gain", 0.6))
peak = np.max(np.abs(mix))
mix = np.tanh(mix / max(peak, 1e-9) * 1.1) * 0.92
save(f"{out}/mix_raw.wav", mix)
print("done; duration", L / SR)
