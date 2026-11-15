# Mix: studio voice + ducked music bed + loud SFX on visual cues. Usage: python mix.py SCRATCH OUT.wav
import subprocess, sys
S = sys.argv[1]; OUT = sys.argv[2]; DUR = 31.4
X = f"{S}/sfx"
# (sfx, time_s, gain_dB)
cues = [
    ("whoosh_rev", 0.0, -6), ("tick", 0.02, -6), ("whoosh", 0.45, -9), ("impact", 0.70, -2),
    ("whoosh", 1.20, -7), ("tick", 2.78, -6), ("tick", 3.44, -6), ("swipe", 4.0, -8),
    ("whoosh", 4.45, -7), ("shimmer", 5.30, -8),
    ("whoosh_long", 7.0, -7), ("tap", 7.18, -4), ("tap", 7.90, -4), ("shimmer", 9.2, -12), ("clink", 10.18, -6), ("shimmer", 10.2, -9),
    ("whoosh", 10.65, -7), ("bubbles", 11.6, -9), ("pop", 12.24, -5), ("pop", 12.95, -5), ("pop", 13.5, -5), ("impact", 14.04, -6),
    ("swipe", 14.9, -6), ("shimmer", 16.62, -8), ("clink", 17.46, -7),
    ("whoosh", 18.0, -7), ("bubbles", 18.2, -8), ("tick", 18.46, -6), ("bubbles", 20.5, -9), ("tick", 20.58, -6), ("bubbles", 22.4, -9), ("tick", 22.58, -6),
    ("whoosh", 23.6, -7), ("stamp", 23.74, -2), ("impact", 23.76, -5), ("tick", 24.1, -9), ("tick", 24.3, -9), ("tick", 24.5, -9), ("tick", 24.7, -9),
    ("pop", 24.95, -4), ("tap", 25.2, -4), ("ding", 26.42, -5), ("shimmer", 27.24, -9),
    ("riser", 27.75, -10), ("impact", 28.95, -3), ("shimmer", 29.0, -6),
]
args = ["ffmpeg", "-v", "error", "-y", "-i", f"{S}/audio/voice.wav", "-i", f"{X}/music.wav"]
fc = ["[0]aformat=channel_layouts=stereo,apad=whole_dur=%s,asplit=2[v][vsc]" % DUR,
      # music: gentle, ducked under the voice, rises at the outro
      "[1]atrim=0:%s,volume=-17dB,afade=t=in:d=0.4,afade=t=out:st=%s:d=1.2[m0]" % (DUR, DUR - 1.3),
      "[m0][vsc]sidechaincompress=threshold=0.04:ratio=5:attack=15:release=280:makeup=1[m]"]
labels = "[v][m]"
for i, (n, t, g) in enumerate(cues):
    args += ["-i", f"{X}/{n}.wav"]
    fc.append(f"[{i+2}]volume={g}dB,adelay={int(t*1000)}:all=1[s{i}]"); labels += f"[s{i}]"
fc.append(f"{labels}amix=inputs={len(cues)+2}:normalize=0:duration=first,atrim=0:{DUR},"
          f"loudnorm=I=-12:TP=-1.0:LRA=9,alimiter=limit=0.9:attack=2:release=60:level=false,aresample=48000[out]")
args += ["-filter_complex", ";".join(fc), "-map", "[out]", "-c:a", "pcm_s16le", OUT]
subprocess.run(args, check=True); print("mixed", OUT)
