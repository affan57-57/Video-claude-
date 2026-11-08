import json, soundfile as sf
from faster_whisper import WhisperModel
m=WhisperModel("medium",device="cpu",compute_type="int8",cpu_threads=4)
a,_=sf.read('a/vf16.wav',dtype='float32')
segs,_=m.transcribe(a,language="ms",word_timestamps=True,beam_size=5,initial_prompt="Frescura Body. Woman Glory Bombshell. Noche Midnight Fantasy. Garam laut, penjagaan kulit. Stok terhad, batch seterusnya. Beg kuning, checkout.")
W=[]
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}")
    W+= [dict(w=w.word.strip(),s=round(w.start,3),e=round(w.end,3)) for w in s.words]
json.dump(W,open('a/words_final.json','w'),ensure_ascii=False,indent=0)
print(' '.join(f"{w['w']}[{w['s']:.2f}]" for w in W))
