import sys, json
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
for f in sys.argv[1:]:
    import soundfile as sf; a,_=sf.read(f,dtype="float32")
    segs, info = m.transcribe(a, language="ms", word_timestamps=True, vad_filter=False, beam_size=5)
    out=[]
    for s in segs:
        print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}", flush=True)
        out.append(dict(start=s.start,end=s.end,text=s.text,words=[dict(w=w.word,s=w.start,e=w.end,p=w.probability) for w in s.words]))
    json.dump(out, open(f.replace('.wav','.json'),'w'), ensure_ascii=False, indent=1)
