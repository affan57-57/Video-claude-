import sys
from faster_whisper import WhisperModel
m=WhisperModel("large-v3",device="cpu",compute_type="int8",cpu_threads=4)
for f in sys.argv[1:]:
    import soundfile as sf; a,_=sf.read(f,dtype="float32"); segs,_=m.transcribe(a,language="ms",word_timestamps=True,vad_filter=False,beam_size=5)
    print("=====",f)
    for s in segs:
        print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}")
        print("   ", " ".join(f"{w.word.strip()}@{w.start:.2f}-{w.end:.2f}" for w in s.words))
