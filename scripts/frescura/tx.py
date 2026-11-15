import sys, json
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[3] if len(sys.argv)>3 else "medium", device="cpu", compute_type="int8", cpu_threads=4)
import subprocess, numpy as np
raw=subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-f","f32le","-ac","1","-ar","16000","-"],capture_output=True).stdout
audio=np.frombuffer(raw,np.float32)
segs, info = m.transcribe(audio, language="ms", word_timestamps=True, beam_size=5, vad_filter=False,
    initial_prompt="Frescura Body, Woman Glory, Bombshell, Noche, Midnight Fantasy, foam, aromaterapi, ocean salt, sabun mandi buih.")
out=[]
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}", flush=True)
    out.append(dict(start=s.start,end=s.end,text=s.text,words=[dict(w=w.word,s=w.start,e=w.end,p=w.probability) for w in s.words]))
json.dump(out, open(sys.argv[2],"w"), ensure_ascii=False, indent=1)
