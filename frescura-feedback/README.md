# FRESCURA BODY – video feedback (HyperFrames)

Preview: `../output/FRESCURA_feedback_PREVIEW.mp4` (draft quality, 1080x1920, ~32s).

- `index.html` – HyperFrames composition (GSAP timeline, captions, motion graphics).
- `assets/` – cut b-roll, feedback edit, product/logo images, fonts, `master.wav`.
- `audio-scripts/` – voice assembly (`build_audio.py`), SFX + bed + mix (`mix.py`),
  DeepFilterNet wrapper (`rundf.py`), transcription (`tr.py`), `timeline.json`.

Final render: `npx hyperframes@0.9.33 render -q delivery -o final.mp4`
