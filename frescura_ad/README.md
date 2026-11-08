# FRESCURA BODY — awareness/review ad (HyperFrames)

PREVIEW only (`output/frescura_PREVIEW.mp4`, watermarked 720p). The final 1080x1920 render waits for approval.

- `project/` — HyperFrames composition (`index.html`) + assets (graded B-roll clips, product images, fonts, final audio mix).
  Render: `cd project && npx hyperframes@0.9.23 render -q high -o final.mp4`
- `scripts/` — the edit, as code:
  - `timeline.py` — EDL: intro VO → full uncut customer feedback (21.3 s, 1.0x) → closing VO → logo (VO x1.10), captions, SFX cues
  - `gen_html.py` + `style.css` + `anim.js` — builds the composition (GSAP motion graphics)
  - `sep_vocals.py` (HTDemucs, safetensors) → `../../scripts/run_df.py` (DeepFilterNet3) → `mix.py` (studio chain, ducked music, SFX, -11 LUFS master)
  - `make_sfx_music.py` — synthesized SFX + 122 BPM lux-house bed (no licensed samples)
- `transcript_*.json` — Whisper large-v3 word timestamps (Malay)
