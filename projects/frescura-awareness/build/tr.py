import sys
from faster_whisper import WhisperModel
m=WhisperModel("large-v3",device="cpu",compute_type="int8",cpu_threads=4)
import wave,numpy as np; w=wave.open(sys.argv[1]); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
segs,info=m.transcribe(a,language="ms",word_timestamps=True,beam_size=5,vad_filter=False,initial_prompt="Frescura Body, Noche, Woman Glory, body shower, foam, aromaterapi, ocean salt.")
import json; out=[]
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}",flush=True)
    out.append(dict(start=s.start,end=s.end,text=s.text,words=[dict(w=w.word,s=w.start,e=w.end) for w in s.words]))
json.dump(out,open(sys.argv[2],"w"),ensure_ascii=False,indent=1)
