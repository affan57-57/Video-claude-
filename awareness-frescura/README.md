# FRESCURA BODY — awareness video (HyperFrames)

Preview: `output/frescura_awareness_PREVIEW_v2.mp4` (draft quality, 1080x1920, 36.5 s).

## Pipeline
1. Audio (from the awareness clip): Demucs `htdemucs_ft` vocals -> DeepFilterNet3 (14 dB limit, `scripts/run_df2.py`)
   -> studio EQ/de-ess/compressor -> pauses tightened to 80 ms -> rubberband 1.1x tempo -> -14 LUFS.
2. `scripts/transcribe.py` (faster-whisper large-v3, Malay) for word timings -> `hyperframes/captions.json`.
3. `scripts/make_audio.py voice.wav hyperframes/assets/mix.wav cues.json` synthesizes SFX + a 112 BPM beat,
   ducks music under the voice, mixes to -13.5 LUFS / -1 dBFS.
4. Composition: edit `hyperframes/index.src.html.tpl`, then `python3 build.py` (injects captions into `index.html`).

## Render
```
cd hyperframes
ffmpeg -i assets/mix.flac assets/mix.wav     # composition references mix.wav
npx hyperframes@0.9.23 check
npx hyperframes@0.9.23 render --quality draft -o preview.mp4     # preview
npx hyperframes@0.9.23 render --quality high  -o final.mp4       # final (after approval)
```
