# FRESCURA BODY — awareness/review ad (HyperFrames)

Final: `output/FRESCURA_BODY_final_1080x1920.mp4` (40 s, 1080x1920 30fps, H.264 + AAC 320k, -11.3 LUFS). Preview: `output/frescura_PREVIEW.mp4`.

- `project/` — HyperFrames composition (`index.html`) + assets (graded B-roll clips, product images, fonts, final audio mix).
  Render: `cd project && npx hyperframes@0.9.23 render -q high -o final.mp4`
- `scripts/` — the edit, as code:
  - `timeline.py` — EDL: intro VO → full uncut customer feedback (21.3 s, 1.0x) → closing VO → logo (VO x1.10), captions, SFX cues
  - `gen_html.py` + `style.css` + `anim.js` — builds the composition (GSAP motion graphics)
  - `sep_vocals.py` (HTDemucs, safetensors) → `../../scripts/run_df.py` (DeepFilterNet3) → `mix.py` (studio chain, ducked music, SFX, -11 LUFS master)
  - `make_sfx_music.py` — synthesized SFX + 122 BPM lux-house bed (no licensed samples)
- `transcript_*.json` — Whisper large-v3 word timestamps (Malay)
