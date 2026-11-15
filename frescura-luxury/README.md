# Frescura Body — "Sebelum Terlambat" (luxury mall edit)

9:16, ~34.6 s, HyperFrames project.

- `scripts/edit_voice.py` – cuts awkward pauses + filler "So" from the denoised voice (Demucs → DeepFilterNet3).
- Voice chain: atempo 1.12, EQ, de-esser, compressor, loudnorm -13 LUFS (see session notes).
- `scripts/gen.py` – generates `hyperframes/index.html` + `compositions/*.html` from `words_voice.json`.
- Large media (voice.wav, music.wav, foam.mp4) are not committed; regenerate from the source videos.

Music: "Winter Clouds (Chilling House Dub)" by happySize-Project, CC BY-SA 3.0 (Jamendo).
SFX: HyperFrames bundled library.
