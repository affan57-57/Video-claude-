# Frescura Body — 40s luxury ad (HyperFrames)

Pipeline (scripts in `tools/`, run from a scratch dir):
1. `denoise.py` — spectral-gate noise reduction (noisereduce), then a studio EQ/de-esser/compression chain in ffmpeg
2. `edit_voice.py` — cut pauses, speed voice up 1.13x (pitch kept), remap word timings → ~38.9 s
3. `fw.py` — faster-whisper (Malay) word timestamps for captions
4. `sfx_kit.py` — synthesized SFX kit + 120 BPM music bed (no third-party samples)
5. `prep.py` — trim, 9:16 / arch crop, warm grade of B-roll (Mixkit free license) + client pump footage
6. `gen.py` — writes the HyperFrames composition `index.html` (scenes, motion graphics, karaoke captions)
7. `mix.py` — voice + ducked music + timed SFX, mastered to about -11 LUFS
Render: `npx hyperframes render -q draft` (preview) or `-q delivery` (final), then mux `final_mix.wav`.
