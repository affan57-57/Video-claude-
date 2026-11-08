"""Cut awkward pauses, speed up, studio-process and lay out the voice track.

Usage: python build_voice.py <aroll_df.wav> <testi_df.wav> <testi_video.mp4> <out_dir>
Writes out_dir/voice.wav (48k stereo, -14 LUFS voice), out_dir/testi_edit.mp4 (testimonial
picture cut/sped to match), out_dir/timeline.json (section start/end in film time).
"""
import json, os, subprocess, sys
import numpy as np, soundfile as sf

AROLL, TESTI, TESTI_VID, OUT = sys.argv[1:5]
os.makedirs(OUT, exist_ok=True)
SR = 48000
A_SPEED, T_SPEED = 1.08, 1.04

# keep-ranges (source seconds), found from the energy envelope of the denoised voice
SECTIONS = [
    ("hook",   AROLL, A_SPEED, [(0.00, 3.50), (3.66, 4.30), (4.48, 5.86), (5.98, 7.24), (7.50, 7.94)]),
    ("listen", AROLL, A_SPEED, [(8.06, 9.00)]),
    ("testi",  TESTI, T_SPEED, [(0.00, 2.84), (3.06, 5.60), (6.36, 18.95)]),
    ("proof",  AROLL, A_SPEED, [(10.00, 11.26), (11.40, 14.10)]),
    ("value",  AROLL, A_SPEED, [(14.28, 15.42), (15.60, 17.70)]),
    ("cta",    AROLL, A_SPEED, [(18.30, 20.60)]),
]
# film-time start of each section (seconds); gaps leave room for transitions/SFX
GAP = {"hook": 0.18, "listen": 0.10, "testi": 0.30, "proof": 0.28, "value": 0.10, "cta": 0.08}
TAIL = 2.0  # end-card hold after the last word

STUDIO = ("highpass=f=85:poles=2,equalizer=f=250:t=q:w=1.0:g=-2.5,equalizer=f=3000:t=q:w=1.0:g=3,"
          "equalizer=f=5500:t=q:w=1.2:g=1.5,highshelf=f=10000:g=2,deesser=i=0.35:m=0.5:f=0.5,"
          "acompressor=threshold=-22dB:ratio=3:attack=6:release=110:knee=4:makeup=3dB")


def cut(path, ranges, fade=0.012):
    a, sr = sf.read(path, dtype="float32")
    assert sr == SR, (path, sr)
    if a.ndim > 1:
        a = a.mean(1)
    parts = []
    for s, e in ranges:
        x = a[int(s * sr):int(e * sr)].copy()
        n = int(fade * sr)
        ramp = np.linspace(0, 1, n, dtype=np.float32)
        x[:n] *= ramp
        x[-n:] *= ramp[::-1]
        parts.append(x)
    return np.concatenate(parts)


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


tl, t = {}, 0.0
film = np.zeros(int(60 * SR), dtype=np.float32)
for name, src, speed, ranges in SECTIONS:
    raw = os.path.join(OUT, f"_{name}_raw.wav")
    proc = os.path.join(OUT, f"_{name}.wav")
    sf.write(raw, cut(src, ranges), SR, subtype="FLOAT")
    ff("-i", raw, "-af", f"atempo={speed},{STUDIO}", "-ar", str(SR), "-c:a", "pcm_f32le", proc)
    x, _ = sf.read(proc, dtype="float32")
    t += GAP[name]
    i = int(t * SR)
    film[i:i + len(x)] += x
    tl[name] = {"start": round(t, 3), "end": round(t + len(x) / SR, 3),
                "speed": speed, "ranges": ranges}
    t += len(x) / SR

total = round(t + TAIL, 2)
film = film[:int(total * SR)]
sf.write(os.path.join(OUT, "_voice_mono.wav"), film, SR, subtype="FLOAT")
# loudness-normalise the whole voice performance (two-pass would be nicer; one-pass is fine at this length)
ff("-i", os.path.join(OUT, "_voice_mono.wav"), "-af",
   "loudnorm=I=-14:TP=-2:LRA=7,aresample=48000,pan=stereo|c0=c0|c1=c0",
   "-c:a", "pcm_f32le", os.path.join(OUT, "voice.wav"))
tl["total"] = total

# testimonial picture: same cuts and speed so lips stay in sync
s = tl["testi"]
chains, labels = [], []
for k, (a, b) in enumerate(s["ranges"]):
    chains.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{k}]")
    labels.append(f"[v{k}]")
fc = ";".join(chains) + f";{''.join(labels)}concat=n={len(labels)}:v=1:a=0,setpts=PTS/{T_SPEED}," \
     "scale=1080:-2:flags=lanczos,crop=1080:1920,fps=30,format=yuv420p[v]"
ff("-i", TESTI_VID, "-filter_complex", fc, "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "slow",
   "-crf", "16", "-g", "15", "-movflags", "+faststart", os.path.join(OUT, "testi_edit.mp4"))

json.dump(tl, open(os.path.join(OUT, "timeline.json"), "w"), indent=1)
print(json.dumps({k: (v if k == "total" else (v["start"], v["end"])) for k, v in tl.items()}, indent=1))
