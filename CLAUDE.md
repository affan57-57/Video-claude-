# Frescura Body — awareness video editing (handoff spec)

The client speaks Malay (casual Kedah/northern style). Reply in Malay, short and clear.

## What the client asks for every time
- **Transcribe first** (faster-whisper `large-v3-turbo`, `language='ms'`, word timestamps) and plan edits from the transcript.
- Remove repeats, false starts ("Okay" retakes) and awkward pauses; find the **strongest hook** for the first 2–4 s.
- Face on screen: **max ~1 s** (client asked to cut it to under 1 s in video 3). Only use shots where he **looks into the lens**; he often reads below the camera, so check gaze frame by frame. Selfie recordings are **mirrored** → `hflip` so the label reads.
- Everything else: educational motion graphics, lots of B-roll, animation, SFX, B-roll matched to what he says.
- Voice must sound **studio-clean**: level-match each kept segment to −20 dBFS *before* denoise (his openings are often ~4–10 dB quieter), then RNNoise + FFT denoise, EQ, de-ess, compression, loudnorm −14 LUFS.
- **Never render final first**: draft preview with a PREVIEW tag → wait for approval → final (1080p `-q delivery`; 4K on request).

## Product facts (get these right)
- Brand: **FRESCURA BODY** (whisper hears "fresh kura bodi", "Flaskura", "First Cooler").
- Scents: **Woman Glory by Bombshell** (red/rose; fresh, floral, feminine) and **Noche by Midnight Fantasy** (violet/night sky; sweet, fruity, seductive). Whisper hears Noche as "noce/nocay/No Chair".
- Gentle foaming pump body shower, 500 ml, paraben-free, "tanpa bahan berbahaya yang dilarang dalam kosmetik", lab tested ("ujian makmal" — the words after it are unclear; show only "UJIAN MAKMAL").
- CTA: "tekan beg kuning" (whisper: "mic kuning", "make money", "backbone", "back on it"), stok terhad.
- Do **not** show unverifiable health/superlative claims (e.g. "mengawal tekanan darah", "membuang toksin", "sabun pertama di dunia") — flag them to the client instead.
- Product photos: `hf/project/assets/product*` (`hero_foam`, `duo_wood`, `duo_marble`, `duo_diag`, `glory_card`, `noche_card`). Never alter the bottle/label pixels.
- Modesty: avoid stock clips with exposed skin; no alcohol (champagne) clips.

## Pipeline (scripts/ + videoN/)
1. `scripts/transcribe.py AUDIO16K.wav OUT.json`
2. `scripts/edit_audio.py SOURCE.mp4 sh.rnnn OUT_DIR [cuts.json]` → `voice.wav`, `edl.json`, `remap.json`
   (rnnoise model: `curl -L -o sh.rnnn https://raw.githubusercontent.com/GregorR/rnnoise-models/master/somnolent-hogwash-2018-09-01/sh.rnnn`)
3. Re-transcribe `voice.wav` → `words.json` (captions use these final times).
4. B-roll from Mixkit (free licence): `https://assets.mixkit.co/videos/<id>/<id>-1080.mp4` (some only `-720`). Prep with `videoN/prep_broll.py`.
5. Background replacement of client footage: `scripts/matte_clip.py` (rembg BiRefNet-general-lite, ~15 s/frame on CPU — run alone, it needs ~10 GB RAM) → `video2/compose_pump.py` (`LIGHT=1` for ivory backdrop).
6. Sound: `videoN/sfx_cues.py` + `make_audio_lux.py` (luxury, 70 bpm) / `make_audio_min.py` (minimal, 96 bpm) → `mix.wav` → loudnorm −14.
7. Composition: `videoN/build.py PROJECT [--final]` writes a HyperFrames `index.html` (GSAP). Check with `npx hyperframes@0.9.10 lint` + `snapshot --at …` and look at the frames.
8. Render: `npx hyperframes@0.9.10 render -q draft` (preview) / `-q delivery` (final) / `--resolution portrait-4k` (4K; AI-upscale low-res clips first with `scripts/ai_upscale.py`, Real-ESRGAN general-x4v3).
9. Splicing newly recorded phrases into an edited voice: `video3/splice_voice.py` (+ `inserts.json` remap in `build.py`).

## Styles delivered
- Video 1 (`hf/project`): TikTok-bold, red/yellow, karaoke captions.
- Video 2 (`video2/`): **luxury premium corporate** — black + champagne gold, Playfair/Cormorant serif, thin gold frame, light leaks.
- Video 3 (`video3/`): **modern motion graphics, minimalist luxury** — ivory, thin Montserrat, hairlines, B-roll in round/rounded masks, pill captions, section counter + progress bar. Client loved this one.
