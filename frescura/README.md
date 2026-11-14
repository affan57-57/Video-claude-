# Frescura Body — awareness ad (HyperFrames)

Preview: `output/frescura_preview.mp4` (39.4s, 1080x1920, -12 LUFS). Draft quality, not the final render.

Pipeline
1. `scripts/tr.py`: faster-whisper transcription with word timestamps.
2. Demucs (`htdemucs_ft`, vocals) then `scripts/run_df2.py` DeepFilterNet3 (HF `fal/DeepFilterNet3`) to remove noise.
3. `scripts/cut.py`: removes pauses longer than 0.14s and the repeated last sentence.
4. ffmpeg `atempo=1.2` + studio EQ / de-esser / compressor, loudnorm.
5. `scripts/synth.py`: synthesized SFX + 122 BPM music bed. `scripts/mix.py` places SFX on transcript cues and ducks the music.
6. `hyperframes/index.html`: HyperFrames composition (GSAP). Final render: `cd hyperframes && npx hyperframes render -q delivery -o final.mp4`.
