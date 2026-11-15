import json,sys
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[2],device="cpu",compute_type="int8",cpu_threads=4)
import soundfile as sf
aud,_=sf.read(sys.argv[1],dtype="float32")
segs,_=m.transcribe(aud,language="ms",word_timestamps=True,beam_size=5,vad_filter=False,initial_prompt="Frescura Body, Woman Glory Bombshell, Noche Midnight Fantasy, sabun mandi buih, ocean salt, aromaterapi.")
out=[]
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}",flush=True)
    for w in s.words: out.append(dict(w=w.word.strip(),s=round(w.start,2),e=round(w.end,2),p=round(w.probability,2)))
json.dump(out,open(sys.argv[3],"w"),ensure_ascii=False,indent=0)
