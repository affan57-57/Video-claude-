import sys, json
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[1], device="cpu", compute_type="int8")
import wave, numpy as np
for f in sys.argv[2:]:
    w=wave.open(f); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
    segs, info = m.transcribe(a, language="ms", word_timestamps=True, vad_filter=False, beam_size=5,
        initial_prompt="Frescura Body. Mandian, sabun, kulit, wangi, buih, feedback, testimoni.")
    out=[]
    print("==", f, info.language)
    for s in segs:
        print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}")
        out.append(dict(start=s.start,end=s.end,text=s.text,words=[dict(w=w.word,s=w.start,e=w.end,p=w.probability) for w in s.words]))
    json.dump(out, open(f.replace(".16k.wav",".json"),"w"), ensure_ascii=False, indent=1)
