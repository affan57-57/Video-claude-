import sys, json
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[2], device="cpu", compute_type="int8", cpu_threads=4)
import soundfile as sf; a,_=sf.read(sys.argv[1],dtype="float32")
segs,info=m.transcribe(a, language="ms", word_timestamps=True, beam_size=5, vad_filter=False,
  initial_prompt="Frescura Body. Sabun mandi buih, body wash, kulit, bakteria, bau badan.")
out=[]
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}", flush=True)
    out.append(dict(start=s.start,end=s.end,text=s.text,words=[dict(w=w.word,s=w.start,e=w.end,p=w.probability) for w in s.words]))
json.dump(out,open(sys.argv[3],"w"),ensure_ascii=False,indent=1)
