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

```bash
cd hyperframes && npx hyperframes@0.9.19 render -q draft -o preview.mp4   # final: -q high
```
