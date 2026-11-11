# Frescura Body: feedback ad (30.5 s, 1080x1920)

HyperFrames composition plus an audio pipeline. The large source videos (foam.mp4, feedback.mp4) are not committed.
Put them in `assets/` before rendering: foam is scaled to 1080x1920, feedback is the original 688x1280 file, both with audio removed.

Structure: hook (0-6 s, intro voice) -> customer feedback video uncut (6-18.3 s) -> closing voice and CTA (18.45-26.4 s) -> brand end card (to 30.5 s).

Audio steps (scripts in `../scripts/frescura`, plus `../scripts/run_df.py`):
1. Denoise the main voice with DeepFilterNet3 (`ATT=20 run_df.py`).
2. `tighten.py` removes pauses (writes segments.json); `splice.py` cuts the sections.
3. Studio chain: EQ, de-esser, compressor, atempo 1.08, loudnorm -13 LUFS.
4. `make_sfx2.py sfx 112 40` synthesizes the SFX and music bed; `mix.py` places them and ducks the music.
5. Master to -11 LUFS, then mux with the HyperFrames render.
