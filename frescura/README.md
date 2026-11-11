# Frescura Body — awareness video (PREVIEW, not final)

1. Voice: DeepFilterNet3 denoise -> scripts/cut_voice.py (drops 2 false starts + stumbled line, tightens pauses) -> rubberband 1.12x -> studio EQ/de-ess/compress -> -12 LUFS.
2. SFX + music bed synthesized: scripts/make_sfx_lux.py sfx 39; mix: scripts/mix.py -> loudnorm -11 LUFS.
3. Visuals: HyperFrames composition hyperframes/index.html. Preview: npx hyperframes render -q draft; final: -q delivery, then mux with mixed WAV.
