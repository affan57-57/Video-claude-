"""Mix the ad's soundtrack: cleaned voice + ducked music bed + SFX on picture cues.
Usage: python mix_audio.py <voice.wav> <music.wav> <sfx_dir> <out.wav>
Voice: brand owner's VO (denoised with DeepFilterNet3, pauses tightened, 1.1x, studio EQ/comp).
Music: "Cat Walk" (Mixkit, free licence), entered on its drop. SFX: Mixkit free sound effects.
All times are film seconds. The voice starts at VO_OFFSET.
"""
import sys, subprocess, numpy as np, soundfile as sf

SR = 48000
DUR = 35.0
VO_OFFSET = 0.10
MUSIC_IN = 29.35          # source second of the drop -> film 0
MUSIC_DB = -12.0          # bed gain before ducking

# (film_time_of_picture_hit, sfx_id, gain_dB, trim_seconds)
# The sfx is placed so its loudest point lands one frame after the picture hit.
CUES = [
    (0.03, 784, -3, 2.2),    # hook: cinematic intro impact on frame 0
    (0.05, 871, -9, 1.3),    # gold shimmer on the hook title
    (1.66, 1491, -8, 1.1),   # cut couple -> hands
    (2.96, 2357, -5, 0.4),   # KEMAS tag
    (3.34, 3005, -5, 0.2),   # BERSIH tag
    (3.36, 166, -12, 0.8),   # cut hands -> roses
    (4.18, 2356, -5, 0.3),   # WANGI tag
    (4.72, 1489, -6, 2.3),   # scene: myth vs fact
    (7.22, 166, -4, 0.8),    # strike-through "bersolek setiap masa"
    (8.44, 1471, -6, 1.4),   # scene: 3 basics
    (10.96, 1137, -4, 0.5),  # 01 kebersihan badan
    (12.00, 1137, -4, 0.5),  # 02 pakaian bersih
    (12.86, 1137, -4, 0.5),  # 03 rutin mandi
    (14.30, 1317, -4, 0.45), # water drop
    (15.48, 867, -8, 2.3),   # PENTING shimmer
    (16.34, 3115, -8, 0.6),  # cut to the brand's foam clip
    (16.60, 1317, -6, 0.45), # foam bubbles
    (17.30, 2925, -9, 1.1),
    (18.36, 871, -8, 1.3),   # ISTIMEWA
    (19.46, 788, -3, 4.0),   # riser into impact: Frescura Body reveal (the one big hit)
    (19.70, 2353, -12, 3.0), # glitter tail on the logo
    (20.52, 2358, -7, 0.5),  # "2" pilihan badge
    (22.48, 1491, -6, 1.1),  # Bombshell bottle slides in
    (23.26, 1465, -8, 2.2),  # Midnight Fantasy bottle slides in
    (24.02, 166, -7, 0.8),   # split screen
    (24.92, 2357, -5, 0.4),  # ATAU
    (26.02, 1492, -9, 1.3),  # stock scene
    (26.60, 1133, -9, 0.35), (27.00, 1133, -10, 0.35), (27.40, 1133, -9, 0.35), (27.80, 1133, -10, 0.35),
    (28.34, 2152, -5, 1.5),  # HABIS impact
    (28.94, 1486, -10, 1.5), # CTA scene
    (29.36, 211, -4, 0.8),   # tap the yellow bag
    (29.42, 2575, -7, 1.3),
    (30.06, 2357, -7, 0.4),  # step 2
    (31.78, 2867, -4, 1.3),  # checkout success
    (32.62, 833, -6, 0.8),   # end card impact
    (32.70, 871, -8, 1.3),
]

def load(path, start=0.0, dur=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(start), "-i", path]
    if dur: cmd += ["-t", str(dur)]
    cmd += ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()

def db(x): return 10 ** (x / 20)

voice_path, music_path, sfx_dir, out = sys.argv[1:5]
N = int(DUR * SR)
voice = np.zeros((N, 2), np.float32); v = load(voice_path)
o = int(VO_OFFSET * SR); voice[o:o + len(v)] = v[: N - o]

music = load(music_path, MUSIC_IN, DUR + 0.5)[:N]
music = np.pad(music, ((0, N - len(music)), (0, 0))) * db(MUSIC_DB)
# fade the bed out under the end card
t = np.arange(N) / SR
music *= np.clip((DUR - t) / 1.8, 0, 1)[:, None] ** 1.5

# sidechain duck: music dips ~7 dB while the voice talks (smoothed envelope)
env = np.abs(voice).mean(1)
win = int(0.12 * SR); k = np.ones(win) / win
env = np.convolve(env, k, "same")
duck = 1 - 0.55 * np.clip(env / 0.05, 0, 1)
music *= duck[:, None]

sfx = np.zeros((N, 2), np.float32)
for hit, sid, g, trim in CUES:
    x = load(f"{sfx_dir}/{sid}.mp3", 0, trim)
    fade = int(min(0.08, trim * 0.3) * SR); x[-fade:] *= np.linspace(1, 0, fade)[:, None]
    x = x / (np.abs(x).max() + 1e-9)
    pk = np.argmax(np.abs(x).mean(1)) / SR
    st = int((hit + 1 / 30 - pk) * SR)
    if st < 0: x = x[-st:]; st = 0
    e = min(N, st + len(x)); sfx[st:e] += x[: e - st] * db(g - 6)

mix = voice + music + sfx
# gentle bus limiter
peak = np.abs(mix).max(); lim = db(-1.0)
if peak > lim:
    g = np.minimum(1, lim / (np.abs(mix).max(1) + 1e-9))
    g = np.minimum.accumulate(g[::-1])[::-1] if False else g
    gs = np.convolve(g, np.ones(240) / 240, "same")
    mix *= np.minimum(g, gs)[:, None]
sf.write(out, mix, SR, subtype="PCM_24")
print("wrote", out, "peak", 20 * np.log10(np.abs(mix).max()))
