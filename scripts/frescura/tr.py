import sys,json
from faster_whisper import WhisperModel
m=WhisperModel("medium",device="cpu",compute_type="int8",cpu_threads=4)
for f in sys.argv[1:]:
    segs,info=m.transcribe(__import__("soundfile").read(f,dtype="float32")[0],language="ms",word_timestamps=True,vad_filter=False,initial_prompt="Frescura Body. Woman Glory Bombshell, Noche Midnight Fantasy. Tekan beg kuning, checkout.")
    out=[]
    for s in segs:
        print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}")
        out+= [dict(w=w.word,s=w.start,e=w.end) for w in s.words]
    json.dump(out,open(f+".json","w"),ensure_ascii=False,indent=0)
