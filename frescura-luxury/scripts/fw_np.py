import sys,json
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[2],device="cpu",compute_type="int8",cpu_threads=4)
prompt="Abang, jangan tunggu isteri merajuk. Hadiahkan Foaming Body Shower Frescura Body. Dua pilihan haruman iaitu perfume Bombshell dan Midnight Fantasy. Ingat abang, bahagiakan isteri tak semestinya perlukan hadiah yang mahal. Stok terhad! Tekan beg kuning sekarang dan terus checkout."
import subprocess,numpy as np
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',sys.argv[1],'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
segs,_=m.transcribe(a,language="ms",word_timestamps=True,vad_filter=False,beam_size=5)
W=[]
for s in segs:
    print("%.2f-%.2f %s"%(s.start,s.end,s.text))
    for w in s.words: W.append(dict(text=w.word.strip(),start=round(w.start,3),end=round(w.end,3),p=round(w.probability,2)))
json.dump(W,open(sys.argv[3],"w"),ensure_ascii=False,indent=0)
