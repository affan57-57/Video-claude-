# Frescura Body — 40s luxury educational ad (HyperFrames)

Pipeline
1. `tr.py` — Whisper large-v3 transcription (Malay) of the voice-over.
2. DeepFilterNet3 denoise (`../scripts/run_df.py`), `cut.py` removes pauses > 0.16s, then ffmpeg studio chain + `atempo=1.16` (49s → 38s voice).
3. `audio_build.py` — synthesized SFX (whoosh, impact, shimmer, pump squish, ka-ching, stamp…) + 120bpm luxury groove, ducked under voice; final mix -11.5 LUFS.
4. `build_html.py` — generates the HyperFrames `index.html` (12 scenes, word-synced captions, GSAP motion).
5. `npx hyperframes render -q draft` for preview; final render after approval.

Script timing (film seconds): hook 0–5.9 · 3 tanda suami peduli 5.9–11 · kecil→makna besar 11–14 · perhatian 14–17 · logo 17–18 · boutique 18–20.5 · foam B-roll 20.5–22.7 · 2 wangian 22.7–27 · tersenyum 27–29.9 · CTA beg kuning 29.9–33.6 · stok terhad + diskaun 33.6–37.5 · end card 37.5–40.
