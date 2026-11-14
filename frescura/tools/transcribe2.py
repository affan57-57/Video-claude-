import json,sys
from faster_whisper import WhisperModel
m=WhisperModel("medium",device="cpu",compute_type="int8",cpu_threads=4)
import soundfile as sf; a,_=sf.read(sys.argv[1],dtype="float32")
segs,info=m.transcribe(a,language="ms",word_timestamps=True,vad_filter=False,beam_size=5,initial_prompt="Suami, isteri. Frescura Body. Buih lembut dan gebu dengan bauan perfume Bombshell dan Midnight Fantasy. Tekan beg kuning, checkout.")
out=[]
for s in segs:
    out.append(dict(start=s.start,end=s.end,text=s.text,words=[dict(w=w.word,s=w.start,e=w.end) for w in s.words]))
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}",flush=True)
json.dump(out,open(sys.argv[2],"w"),ensure_ascii=False,indent=1)
