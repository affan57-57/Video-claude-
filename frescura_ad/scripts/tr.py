import sys,json
from faster_whisper import WhisperModel
m=WhisperModel("medium",device="cpu",compute_type="int8",cpu_threads=4)
segs,info=m.transcribe(__import__("soundfile").read(sys.argv[1],dtype="float32")[0],language="ms",word_timestamps=True,vad_filter=False,beam_size=5,initial_prompt="Frescura Body, Noche Midnight Fantasy, Woman Glory Bombshell, foaming body shower, ocean salt, aromatherapy.")
out=[]
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}",flush=True)
    out.append(dict(start=s.start,end=s.end,text=s.text,words=[dict(w=w.word,s=w.start,e=w.end) for w in s.words]))
json.dump(out,open(sys.argv[2],"w"),ensure_ascii=False,indent=1)
