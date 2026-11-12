import sys, json
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[2], device="cpu", compute_type="int8", cpu_threads=4)
prompt="Frescura Body, Bombshell, Midnight Fantasy, buih lembut, wangian feminin, check out, stok terhad."
import subprocess, numpy as np
aud=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',sys.argv[1],'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True,check=True).stdout,dtype=np.float32)
seg,_=m.transcribe(aud, language="ms", word_timestamps=True, initial_prompt=prompt, vad_filter=False, beam_size=5)
W=[dict(text=w.word.strip(),start=round(w.start,3),end=round(w.end,3)) for s in seg for w in s.words]
json.dump(W,open(sys.argv[3],"w"),ensure_ascii=False)
print(" ".join(f"[{w['start']:.2f}]{w['text']}" for w in W))
