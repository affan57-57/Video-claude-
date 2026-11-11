"""Build the edit: cut list (intro -> testimonial -> closing), tighten pauses, speed up.
Usage: python edit.py WORK_DIR SRC_DIR
Inputs (WORK_DIR): main.studio.wav, feedback.studio.wav (48k mono, cleaned)
Outputs: edl.json, voice.wav (timeline voice), feedback_edit.mp4 (cut+sped video), timeline.json (word times on output timeline)
"""
import json, sys, subprocess, numpy as np, soundfile as sf, os
W, SRC = sys.argv[1], sys.argv[2]
SR = 48000
SPEED = {"main": 1.13, "feedback": 1.07}
# (source, in, out) in source seconds — chosen from word timestamps (see transcript)
SECTIONS = [
  ("intro",   "main",     [(0.00, 1.64), (2.20, 6.44)]),
  ("testi",   "feedback", [(2.44, 6.46), (6.64, 8.90), (8.98, 11.94), (12.06, 16.60), (16.68, 17.90)]),
  ("closing", "main",     [(7.46, 9.26), (9.42, 17.22)]),
]
GAP_BETWEEN_SECTIONS = 0.10
def rms_env(x, win=0.02):
    n = int(win*SR); m = len(x)//n
    return 20*np.log10(np.sqrt((x[:m*n].reshape(m, n)**2).mean(1))+1e-9), n
def split_silences(x, t0, t1, max_gap, keep):
    """Return sub-pieces of [t0,t1] with internal silences longer than max_gap shortened to `keep`."""
    seg = x[int(t0*SR):int(t1*SR)]
    db, n = rms_env(seg); thr = db.max()-38
    quiet = db < thr; pieces = []; start = 0.0; i = 0; L = len(quiet)
    while i < L:
        if quiet[i]:
            j = i
            while j < L and quiet[j]: j += 1
            gs, ge = i*n/SR, j*n/SR
            if ge-gs > max_gap and i > 0 and j < L:
                cut_s = gs + keep/2; cut_e = ge - keep/2
                pieces.append((t0+start, t0+cut_s)); start = cut_e
            i = j
        else: i += 1
    pieces.append((t0+start, t1)); return pieces
def stretch(x, speed):
    p = subprocess.run(["ffmpeg","-v","error","-f","f32le","-ar",str(SR),"-ac","1","-i","-",
        "-af",f"rubberband=tempo={speed}:pitch=1:formant=preserved:transients=crisp:detector=compound:phase=laminar:window=standard:smoothing=on",
        "-f","f32le","-"], input=x.astype(np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.float32)
audio = {k: sf.read(f"{W}/{k}.studio.wav", dtype="float32")[0] for k in ("main","feedback")}
words = {"main": [w for s in json.load(open(f"{W}/main.json")) for w in s["words"]],
         "feedback": [w for s in json.load(open(f"{W}/feedback.ms.json")) for w in s["words"]]}
out = []; edl = []; t = 0.0; tl_words = []; sections = []
FADE = int(0.006*SR)
for name, src, segs in SECTIONS:
    sec_start = t; sp = SPEED[src]
    for (a, b) in segs:
        subs = split_silences(audio[src], a, b, max_gap=0.20 if src=="main" else 0.32, keep=0.07 if src=="main" else 0.12)
        for (s0, s1) in subs:
            x = audio[src][int(s0*SR):int(s1*SR)].copy()
            x[:FADE] *= np.linspace(0,1,FADE); x[-FADE:] *= np.linspace(1,0,FADE)
            y = stretch(x, sp); dur = len(y)/SR
            edl.append(dict(section=name, src=src, src_in=round(s0,3), src_out=round(s1,3), speed=sp, tl_in=round(t,3), tl_out=round(t+dur,3)))
            for w in words[src]:
                if w["s"] >= s0-0.02 and w["e"] <= s1+0.05:
                    tl_words.append(dict(w=w["w"].strip(), s=round(t+(max(w["s"],s0)-s0)/sp,3), e=round(t+(min(w["e"],s1)-s0)/sp,3), section=name, src=src))
            out.append(y); t += dur
    sections.append(dict(name=name, start=round(sec_start,3), end=round(t,3)))
    gap = np.zeros(int(GAP_BETWEEN_SECTIONS*SR), np.float32); out.append(gap); t += GAP_BETWEEN_SECTIONS
voice = np.concatenate(out)
sf.write(f"{W}/voice.wav", voice, SR, subtype="FLOAT")
json.dump(dict(edl=edl, sections=sections, words=tl_words, voice_dur=round(len(voice)/SR,3)), open(f"{W}/timeline.json","w"), ensure_ascii=False, indent=1)
# Testimonial video: same cuts + speed, each cut alternates a subtle punch-in to hide jump cuts
fb = [e for e in edl if e["src"]=="feedback"]
parts = []; fc = []
T0 = fb[0]["tl_in"]
for i, e in enumerate(fb):
    z = 1.0 if i % 2 == 0 else 1.12
    nf = round((e["tl_out"]-T0)*30) - round((e["tl_in"]-T0)*30)  # cumulative frame rounding: no drift vs audio
    fc.append(f"[0:v]trim={e['src_in']}:{e['src_out']},setpts=(PTS-STARTPTS)/{e['speed']},scale=1080:-2:flags=lanczos,"
              f"scale=iw*{z}:ih*{z}:flags=lanczos,crop=1080:1920:(iw-1080)/2:(ih-1920)*0.35,setsar=1,fps=30,"
              f"tpad=stop_mode=clone:stop_duration=0.3,trim=end_frame={nf},setpts=PTS-STARTPTS[v{i}]")
    parts.append(f"[v{i}]")
fc.append("".join(parts)+f"concat=n={len(parts)}:v=1:a=0[v]")
subprocess.run(["ffmpeg","-v","error","-y","-i",f"{SRC}/feedback.mov","-filter_complex",";".join(fc),"-map","[v]",
                "-c:v","libx264","-preset","medium","-crf","16","-pix_fmt","yuv420p","-an",f"{W}/feedback_edit.mp4"], check=True)
print(json.dumps(sections), "voice", len(voice)/SR, "pieces", len(edl))
