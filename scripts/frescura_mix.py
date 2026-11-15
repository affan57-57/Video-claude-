# Mix studio voice + music bed (sidechain-ducked) + SFX cues -> final stereo track.
# Usage: python frescura_mix.py WORK_DIR DURATION
import sys, subprocess
W, DUR = sys.argv[1], float(sys.argv[2])
VO = 0.5
# (sfx, film-time seconds, gain dB)
CUES = [("boom", 0.0, -3), ("riser", -0.3, -99), ("swish", 0.26, -8), ("pop", 1.25, -8), ("heartbeat", 1.85, -6),
        ("whoosh", 2.66, -8), ("hit", 4.80, -4), ("boom", 4.80, -10), ("whoosh", 5.06, -9),
        ("tick", 6.18, -8), ("ding", 6.43, -11), ("tick", 6.70, -8), ("ding", 6.95, -11), ("tick", 7.52, -8), ("ding", 7.77, -11),
        ("whoosh", 9.02, -9), ("chime", 10.62, -8), ("shimmer", 10.66, -8), ("riser", 11.15, -9), ("hit", 12.30, -5),
        ("foam", 12.90, -7), ("swish", 14.55, -9), ("hit", 14.62, -7), ("hit", 15.54, -7),
        ("whoosh", 16.36, -8), ("foam", 16.6, -8), ("swish", 17.64, -9), ("hit", 18.42, -4), ("hit", 19.78, -4), ("shimmer", 19.8, -8),
        ("whoosh", 20.28, -9), ("swish", 21.78, -10), ("chime", 23.2, -9),
        ("hit", 24.08, -6), ("hit", 24.52, -4), ("tick", 24.2, -9), ("tick", 24.45, -9), ("tick", 24.7, -9), ("tick", 24.95, -9), ("tick", 25.2, -9),
        ("whoosh", 25.38, -9), ("pop", 25.55, -6), ("tap", 26.22, -4), ("kaching", 26.48, -5),
        ("whoosh", 27.88, -7), ("boom", 27.96, -8), ("shimmer", 28.0, -8), ("chime", 28.7, -9)]
CUES = [c for c in CUES if c[2] > -90 and c[1] >= 0]
inputs = ["-i", f"{W}/voice_studio.wav", "-i", f"{W}/sfx/music.wav"]
for name, _, _ in CUES: inputs += ["-i", f"{W}/sfx/{name}.wav"]
f = [f"[0]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay={int(VO*1000)}:all=1,apad=whole_dur={DUR},asplit=2[v][vsc]",
     f"[1]volume=-13dB[mus]",
     "[mus][vsc]sidechaincompress=threshold=0.03:ratio=5:attack=15:release=250:makeup=1[md]"]
labels = []
for i, (name, t, g) in enumerate(CUES):
    f.append(f"[{i+2}]volume={g}dB,adelay={int(t*1000)}:all=1[s{i}]"); labels.append(f"[s{i}]")
f.append(f"[v][md]{''.join(labels)}amix=inputs={len(labels)+2}:normalize=0:duration=first,atrim=0:{DUR},"
         f"afade=t=out:st={DUR-1.2}:d=1.2,alimiter=limit=0.89:attack=3:release=60:level=false,"
         f"loudnorm=I=-12:TP=-1.0:LRA=8[out]")
cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(f), "-map", "[out]", "-ar", "48000", "-c:a", "pcm_s24le", f"{W}/final_mix.wav"]
subprocess.run(cmd, check=True); print("mixed", len(CUES), "cues")
