# Frescura Body – iklan 30s (Hyperframes)

- `hyperframes/` – komposisi HTML (11 babak B-roll/motion graphic + kapsyen karaoke). Render: `cd hyperframes && npx hyperframes@0.9.51 render -q delivery -o final.mp4`
- `hyperframes/assets/mix.wav` – suara (Demucs + DeepFilterNet3, jeda dibuang, 1.1x, EQ studio) + SFX + muzik sintesis, -11 LUFS.
- `scripts/audio_mix.py voice.wav out.wav cues.json` – jana SFX/muzik & mix ikut `cues.json`.
- `scripts/cutout.py` – cutout produk (RMBG-1.4 ONNX); `scripts/esr_up.py` – upscale Real-ESRGAN x4.
- `output/frescura_PREVIEW_draft.mp4` – PREVIEW (kualiti draf). Belum render final.
