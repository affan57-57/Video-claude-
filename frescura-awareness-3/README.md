# Frescura Body — awareness #3 "3 Kebaikan Garam Laut" (45s, 9:16)

Status: **PREVIEW**. The final has not been rendered yet. It waits for approval.

## Voice
- Source: 85s of voice-over. Cuts:
  - Removed: oily-back/chest detail, Dead Sea, "kaki pun rasa segar", "Nampak tak?", morning/night shower, repeated order/check-out lines.
  - Keep ranges: `[[0,10.42],[19.12,23.38],[28.86,35.06],[44.6,57.58],[64.88,80.48]]` (`scripts/edl_v2.py`).
- Processing: pauses capped at 80 ms, Demucs, DeepFilterNet3 (noise floor -34 → -53 dB), rubberband ×1.075, studio chain at -12 LUFS. Voice length: 44.1s.

## Visuals: HyperFrames sub-compositions (built directly as compositions)
`hyperframes/index.html` is the root composition `main`. It mounts 13 files from `compositions/` with `data-composition-src`. Each one has its own local-time GSAP timeline.

| composition | root time | content |
|---|---|---|
| `hook` | 0–5.04 | "Garam laut" porthole → giant "3 kebaikan" |
| `one` | 5.04–9.2 | 01 Kawal minyak: oil drops + salt + oil meter |
| `two` | 9.2–12.88 | 02 Tenangkan: itch zig-zag → calm wave, redness → aqua |
| `three` | 12.88–18.46 | 03 Rendam kaki: basin, steam, salt grains, rough → smooth heel |
| `ritual` | 18.46–21.88 | foam video + recap → "MANDI" |
| `product` | 21.88–27.82 | iris porthole reveal, FRESCURA, ticker, pump video + chips |
| `clean` | 27.82–30.0 | lather video, "Tak melekat" |
| `glory` | 30.0–33.26 | split panel, Woman Glory (yakin & menawan) |
| `noche` | 33.26–37.4 | split panel, Noche (lembut & misteri) |
| `stock` | 37.4–41.2 | crossing STOK TERHAD / BATCH INI tickers, friends → bag |
| `cta` | 41.2–45 | Klik link di bawah, TEKAN BEG KUNING, CHECK OUT SEKARANG |
| `captions` | 0–45 | Manrope 800 karaoke captions with a highlight box |
| `hud` | 0–45 | logo, 01/03 index, side progress rail, porthole iris transitions |

- **Style:** "Ocean Index". Fonts are Italiana, Cormorant Garamond italic and Manrope.
- **Media:** only the owner's product photos and foam-pump video.
- **Audio:** synthesised SFX and a 122 BPM bed with voice ducking (`scripts/sound_v3.py`). Mix is about -12 LUFS.

```bash
cd hyperframes && npx hyperframes@0.9.19 render -q draft -o preview.mp4   # final: -q high
```
