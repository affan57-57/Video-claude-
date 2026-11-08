# Frescura Body — awareness video (HyperFrames)

Pipeline (preview stage, final render not done yet):
1. Voice: DeepFilterNet3 denoise → pause removal from energy envelope (gaps >0.16s cut to 0.08s) → studio EQ/de-ess/compress → atempo 1.07 → -14 LUFS (`../scripts/run_df.py`, scratch scripts in session).
2. Transcript of the cleaned voice: `scripts/transcript_voice.json` (faster-whisper large-v3). Captions built with `scripts/build_captions.py` (fixes brand names: Frescura Body, Bombshell, Midnight Fantasy, beg kuning).
3. Visuals: `comp/index.html` (HyperFrames 0.8.193 + GSAP) — 12 scenes, B-roll from pump footage + product photos.
4. Audio: `scripts/make_audio_assets.py sfx 39` (synth SFX + music bed), `scripts/mix_audio.py` → `render/final_audio.wav` (-11 LUFS).
5. Preview: `npx hyperframes@0.8.193 render -q draft`, then mux with final_audio → `render/FRESCURA_preview.mp4`.
