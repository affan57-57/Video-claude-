# FRESCURA BODY – awareness ad (HyperFrames)

32 s, 1080x1920. Edit structure: Hook → Dengar (product + logo) → Real customer review →
Educational (Gentle Foaming / Ocean Salt / Aromatherapy) → CTA (stok terhad, checkout, beg kuning) → logo end card.

Rebuild:
1. Download sources (3.MOV voiceover, F10.MOV feedback, pump foam MOV) into `work/src/` as awareness.mov, feedback.mov, pump.mov.
2. Audio: Demucs (htdemucs_ft vocals) → DeepFilterNet3 (`scripts/run_df.py`, ATT=18) → `scripts/frescura_sfx.py work/sfx 36` → `scripts/frescura_audio.py work hf/frescura/assets/mix.wav`.
   Cuts/tempo/SFX cues live in `scripts/frescura_edl.py`.
3. Video assets: `assets/pump.mp4` (remux of pump MOV), `assets/feedback.mp4` (feedback scaled to 1080 wide).
4. `npx hyperframes render -o out.mp4` from this folder.
