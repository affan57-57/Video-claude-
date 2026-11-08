# Frescura Body — awareness video ("Real feedback", ~36.7 s, 1080x1920)

Sources (Google Drive): `6.MOV` (voice-over A-roll; picture not used), `tekan pump yg baru.MOV` (pump/foam B-roll),
`5_6059646302818405093.mp4` (beach foam B-roll), and the mall testimonial `output/video_final_studio_HD.mp4`.

1. Voice clean-up: Demucs `htdemucs --two-stems=vocals` -> DeepFilterNet3 (`../run_df.py`, HF `fal/DeepFilterNet3`, ATT=20 A-roll / 12 testimonial).
2. `python build_voice.py aroll_df.wav testi_df.wav output/video_final_studio_HD.mp4 build/`
   cuts awkward pauses, speeds A-roll 1.08x / testimonial 1.04x, studio EQ+de-ess+compression,
   writes `voice.wav`, `testi_edit.mp4` (picture cut to match) and `timeline.json`.
3. `python make_audio.py build/voice.wav frescura-awareness/assets/audio/mix.wav build/sfx`
   synthesised SFX + minimal deep-house bed, ducked under the voice, final -12 LUFS / -1 dBTP.
4. HyperFrames project `frescura-awareness/` (GSAP timeline in `index.html`):
   `npx hyperframes@0.9.23 check`, preview: `npx hyperframes@0.9.23 render -q draft`,
   final (after approval): `npx hyperframes@0.9.23 render -q delivery`.
