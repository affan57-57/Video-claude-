# Frescura Body – awareness edit (HyperFrames)

Pipeline
1. `scripts/tr.py` – Whisper (medium, ms) word timestamps of the voiceover.
2. `scripts/run_df.py` – DeepFilterNet3 noise removal (ATT=28 dB).
3. `scripts/cut2.py` – shrink awkward pauses; then `atempo=1.13` + studio EQ/de-ess/compression, loudnorm -14 LUFS.
4. `scripts/audio_design.py` – synthesized SFX bus (impacts, whooshes, pops, bell, bubbles, shimmer) + 112 BPM luxe music bed.
5. Mix: voice + SFX + sidechain-ducked music, loudnorm -12 LUFS.
6. `hyperframes/index.html` – full composition (motion graphics, captions, b-roll). Render: `npx hyperframes render`.
   `assets/pump.mp4` (foam b-roll, from Drive) is not committed; drop it into `hyperframes/assets/` before rendering.
7. Mux render + `mix.wav`.
