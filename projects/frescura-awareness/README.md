# FRESCURA BODY — Awareness ad (HyperFrames)

**Status: PREVIEW (draft render), not final.** -> output/frescura_awareness_PREVIEW.mp4 (37.2 s, 1080x1920)

Pipeline: build/tr.py (Whisper large-v3 transcript) -> DeepFilterNet3 denoise (scripts/run_df.py) -> build/edit_voice.py (drop repeated CTA + awkward phrase, shorten pauses) -> rubberband 1.10x + studio chain -> build/audio.py (SFX + music bed + ducking) -> build/build.py (generates hyperframes/index.html) -> npx hyperframes render.
