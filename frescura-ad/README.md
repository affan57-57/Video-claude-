# Frescura Body — 40s luxury ad (HyperFrames)

Source: voiceover `2.MOV` (visuals unused), B-roll `tekan pump yg baru.MOV`, product photos + logo.

Pipeline
1. `tr.py` — faster-whisper (medium, ms) word-level transcript.
2. DeepFilterNet3 denoise (atten 18 dB) → `cut.py` removes the flubbed line ("Suami kalau korang, kau selalu") and tightens pauses.
3. `atempo=1.22` + studio EQ/de-ess/compress → -13 LUFS voice (39.2 s).
4. `make_audio.py` synthesises SFX + 122 BPM music; `mix.py` places SFX from `cues.json`, ducks music under voice → -12 LUFS master.
5. `index.html` — HyperFrames composition (Bodoni Moda + Outfit, GSAP), captions from `caps.json`.
   Render: `npx hyperframes render -q high -o out.mp4`
