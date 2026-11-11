import sys, soundfile as sf
from faster_whisper import WhisperModel
m=WhisperModel("large-v3",device="cpu",compute_type="int8")
a,sr=sf.read(sys.argv[1],dtype="float32")
seg,info=m.transcribe(a,language="ms",word_timestamps=True,vad_filter=False,beam_size=5)
for s in seg:
    print(f"[{s.start:.2f}-{s.end:.2f}] {s.text}")
    print("   "+" ".join(f"{w.word.strip()}@{w.start:.2f}-{w.end:.2f}" for w in s.words))
