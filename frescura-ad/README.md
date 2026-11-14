# Frescura Body — iklan "Jangan tunggu isteri merajuk" (HyperFrames)

Pipeline:
1. Audio: DeepFilterNet3 denoise (`scripts/run_df.py`, ATT=14) → potong jeda senyap (>120 ms, ambang -40 dB) → rubberband tempo 1.12x → EQ/de-esser/kompresor studio → loudnorm -13 LUFS (38.6 s).
2. Transkripsi: faster-whisper medium (`tr.py`) pada suara akhir; pembetulan manual dalam `caps.json`.
3. B-roll Mixkit (lesen percuma) dipotong & di-grade dengan `prep.sh`; video pump pengguna dipercepat 1.6x/1.8x.
4. Komposisi HyperFrames: `template.html` + `build.py` (SFX Mixkit, kapsyen, font Bodoni Moda + Outfit) → `index.html`.
5. Render: `npx hyperframes render -q draft` (preview) / `-q delivery` (final).
