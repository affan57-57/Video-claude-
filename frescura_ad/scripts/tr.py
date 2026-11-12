import sys,json
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[2],device="cpu",compute_type="int8",cpu_threads=4)
segs,info=m.transcribe(__import__("soundfile").read(sys.argv[1],dtype="float32")[0],language="ms",word_timestamps=True,vad_filter=False,beam_size=5)
out=[]
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}",flush=True)
    out+= [dict(w=w.word,s=w.start,e=w.end) for w in s.words]
json.dump(out,open(sys.argv[3],"w"),ensure_ascii=False)
