# Frescura Body – Awareness Ad (HyperFrames)

Pipeline (scratch paths are arguments):
1. `tr.py` – Whisper (medium, ms) transcription with word timestamps → `main_tr.json`
2. DeepFilterNet3 denoise (`../scripts/run_df.py`, full attenuation) → `df_full.wav`
3. `cut.py` – removes pauses >0.12s (keeps 35ms each side), retimes words for 1.17× speed, fixes brand words → `words.json`
4. ffmpeg rubberband 1.17× (formant-preserved) + studio EQ/de-ess/compression → `voice_studio.wav`
5. `prep_broll.sh` – Mixkit (free licence) stock + foam clip → portrait 1080×1920 graded B-roll
6. `cut_bg.py` – BiRefNet background removal for product bottles
7. `mix.py` – voice + "Cat Walk" (Mixkit) music, sidechain-ducked, drop on "Frescura Body", 43 SFX, −11 LUFS
8. `build.py` – generates the HyperFrames `index.html` (GSAP, captions, motion graphics), render with `npx hyperframes render`
