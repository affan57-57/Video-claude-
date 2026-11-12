import sys,json
from faster_whisper import WhisperModel
m=WhisperModel("medium",device="cpu",compute_type="int8")
import soundfile as sf; a,_=sf.read(sys.argv[1],dtype="float32")
segs,info=m.transcribe(a,language="ms",word_timestamps=True,vad_filter=False,beam_size=5)
out=[]
for s in segs:
    w=[(x.start,x.end,x.word) for x in s.words]
    out.append(dict(s=s.start,e=s.end,t=s.text,w=w)); print(f"{s.start:6.2f}-{s.end:6.2f} {s.text}",flush=True)
json.dump(out,open(sys.argv[2],"w"),ensure_ascii=False,indent=0)
