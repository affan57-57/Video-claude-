# FRESCURA BODY – awareness/testimonial edit (HyperFrames)

- `index.html` – HyperFrames composition (1080x1920, 31.5 s). Preview: `npx hyperframes preview`; render: `npx hyperframes render -q high`.
- `assets/media/mix.wav` – final audio (studio-cleaned voice + music + SFX).
- `build/` – how the audio was made:
  1. Demucs `htdemucs_ft --two-stems=vocals` on both source clips.
  2. `denoise_df.py` (DeepFilterNet3, ATT=18) on the presenter voice only (testimonial keeps Demucs vocals + 10% original).
  3. ffmpeg EQ/de-ess/compress chain, pauses cut, presenter speed 1.1x.
  4. `mix_audio.py` – voice + Mixkit music bed (side-chain ducked) + Mixkit SFX on cue.
- Edit order: presenter intro -> customer testimonial -> presenter closing -> logo end card.
- Music/SFX/extra b-roll: Mixkit free licence. Fonts: Bodoni Moda, Marcellus, Jost (OFL).
