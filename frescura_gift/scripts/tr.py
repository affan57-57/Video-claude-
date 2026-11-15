import sys
from faster_whisper import WhisperModel
m=WhisperModel("medium",device="cpu",compute_type="int8",cpu_threads=4)
import soundfile as sf
a,_=sf.read(sys.argv[1],dtype="float32")
segs,info=m.transcribe(a,language="ms",word_timestamps=True,vad_filter=False,beam_size=5)
for s in segs:
    print(f"[{s.start:.2f}-{s.end:.2f}] {s.text}")
    for w in s.words: print(f"   {w.start:6.2f} {w.end:6.2f} {w.word}")
