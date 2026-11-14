import sys,json
from faster_whisper import WhisperModel
m=WhisperModel("medium",device="cpu",compute_type="int8",cpu_threads=4)
import soundfile as sf
aud,_=sf.read(sys.argv[1],dtype="float32")
segs,info=m.transcribe(aud,language="ms",word_timestamps=True,vad_filter=False,initial_prompt="Frescura Body, Woman Glory Bombshell, Noche Midnight Fantasy, foam, ocean salt, aromatherapy.")
out=[]
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}",flush=True)
    out.append(dict(start=s.start,end=s.end,text=s.text,words=[dict(w=w.word,s=w.start,e=w.end) for w in s.words]))
json.dump(out,open(sys.argv[2],"w"),ensure_ascii=False,indent=1)
