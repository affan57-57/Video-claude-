# Frescura Body — awareness #2 "Kebaikan Garam Laut" (45s, 9:16)

Status: **PREVIEW**. The final has not been rendered yet. It waits for approval.

- **Voice**: the source is 84s of audio. Repeated or less important lines were cut (spa history, scrub, "jangan pandang remeh…", the first stock and CTA repeats). Pauses are capped at 80 ms, then the voice is processed with Demucs, DeepFilterNet3, rubberband ×1.12 (formants preserved) and a studio chain at -12 LUFS. Voice length: 44.2s. Keep ranges: `[[4.28,20.84],[26.38,28.62],[42.28,72.04],[82.10,83.85]]` (`scripts/edl_v2.py`).
- **Visuals**: only the owner's 4 product photos and the owner's foam-pump video (4 short clips). No stock footage.
- **Style**: "stone & sage" spa editorial. Fonts are Marcellus, Instrument Serif italic and Plus Jakarta Sans 800 (captions). Design features:
  - story-style progress bar
  - blinds transitions
  - dry-skin crack hook
  - mineral orbit diagram
  - moisture capsule
  - rotating "SPA" text ring
  - variant cards with No. 01 / No. 02 labels
  - "STOK TERHAD" stamp
  - yellow-bag CTA
- **Audio**: synthesised SFX and a 118 BPM spa beat with voice ducking (`scripts/sound_v2.py`). Mix is about -12 LUFS.

## HyperFrames composition structure
`hyperframes/index.html` is the root composition (`main`, 45s). It mounts 13 sub-compositions with `data-composition-src`. Each one is a `<template>` file with its own GSAP timeline in local time:

| composition | root time | content |
|---|---|---|
| `hook` | 0–4.62 | dry-skin hook, cracks, "Garam laut" |
| `process` | 4.62–10.0 | sea water → evaporation → sun |
| `minerals` | 10.0–14.42 | Mg / Ca / K orbit |
| `hydrate` | 14.42–16.52 | magnesium moisture capsule |
| `choose` | 16.52–18.46 | "Pilih yang betul" |
| `product` | 18.46–23.92 | FRESCURA reveal + foam "SPA" ring |
| `foam` | 23.92–30.5 | pump/foam/lather clips + features |
| `duo` | 30.5–32.24 | "2 varian" |
| `variants` | 32.24–40.5 | Woman Glory / Noche cards |
| `stock` | 40.5–42.36 | "STOK TERHAD" stamp |
| `cta` | 42.36–45 | yellow bag CTA |
| `captions` | 0–45 | karaoke captions + light/dark theme |
| `hud` | 0–45 | frame, story progress bar, blinds transitions |

`npx hyperframes compositions` lists the compositions. `scripts/split_comps.py` documents how the scenes were split out.

```bash
cd hyperframes && npx hyperframes@0.9.19 render -q draft -o preview.mp4   # final: -q high
```
