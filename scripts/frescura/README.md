# Frescura Body – "Hadiah kecil" ad (HyperFrames)

1. `transcribe.py` – faster-whisper (ms) word timestamps.
2. `voice.sh WORKDIR` – Demucs vocals → DeepFilterNet3 → cut fillers ("So," ×3, repeated "kita duduk dengan dia", pauses) → 1.1× → studio EQ/comp → -14 LUFS.
3. `make_audio_kit.py OUT 36` – synthesised SFX + 120 BPM music bed.
4. `mix.py voice.wav kit out.wav 34` – voice + ducked music + SFX cues; then loudnorm -13 LUFS → `assets/final_mix.wav`.
5. `build_comp.py PROJECT [--preview]` – writes the HyperFrames `index.html` (8 scenes, captions, motion graphics).
6. `npx hyperframes render -q draft` (preview) / default quality (final).
