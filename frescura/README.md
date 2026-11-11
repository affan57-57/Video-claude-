# Frescura Body: feedback ad (HyperFrames)

A 31 s portrait (1080×1920) ad edited with [HyperFrames](https://hyperframes.heygen.com).
It runs intro VO → customer testimonial → closing VO + CTA → logo end card.

## Story / timeline
| Time | Scene | Voice |
|---|---|---|
| 0.0–1.3 | Hook: foam B-roll, big serif type | "Pelanggan dah cuba." |
| 1.2–2.6 | Product photo, circle reveal | "Sekarang korang bila lagi?" |
| 2.6–5.6 | Ivory editorial: arch product, 5★, wordmark | "Tengok dulu feedback mereka tentang Frescura Body ini." |
| 5.6–19.6 | Testimonial video, with chips for Wangi / Lembut / Cepat kering, a foam cutaway with a formula card, and a "tak tipu" stamp | customer feedback |
| 19.6–23.2 | "Ha!" impact, then foam B-roll showing "Tengok je" struck out and "Beli & rasa sendiri" | "Ha! Jangan sekadar tengok orang lain beli." |
| 23.2–25.6 | Woman Glory and Noche product cards, specs, a stock bar | "Tekan beg kuning … sebelum stok habis!" |
| 25.6–26.9 | Yellow bag CTA | "Check out sekarang di beg kuning." |
| 26.9–31.0 | Logo end card | none |

## Audio
- Voice: Demucs (vocal separation) → DeepFilterNet3 (denoise) → studio EQ/de-esser/compressor.
  Pauses are trimmed with `scripts/tighten.py`, the intro and closing are sped up 1.12×, and everything is normalised.
- SFX and the music bed are synthesised by `scripts/make_audio_fx.py`, so they are royalty-free.
- `scripts/mix.py` builds `assets/audio/master.wav` from `cues.json` (it ducks the music and masters to -11 LUFS).
  To move a sound effect, edit `cues.json` and re-run `python3 scripts/mix.py`.

## Commands
```bash
npx --yes hyperframes@0.9.33 preview --background   # Studio preview
npx --yes hyperframes@0.9.33 check
npx --yes hyperframes@0.9.33 render -q delivery -o ../output/frescura_final.mp4   # final render
```
