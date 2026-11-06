# Frescura Body — awareness #4 "Noir Spotlight" (45s, 9:16)

Status: **PREVIEW**. The final has not been rendered yet. It waits for approval.

## Voice
- Source: 69s of voice-over. Cuts:
  - Removed: the sea-salt evaporation line (already in #1–#3), "pilihan dalam rawatan spa", "kena tunggu lama untuk restock", "Bayangkan orang lain… sabun biasa… rugi kan".
  - Keep ranges: `[[0,9.95],[15.06,22.70],[26.24,48.95],[61.02,69.05]]` (`scripts/edl_v2.py`).
- Processing: pauses capped at 80 ms, Demucs, DeepFilterNet3 (noise floor -28 → -48 dB), rubberband ×1.07 with formants preserved, studio chain. Voice length: 44.2s.
- Loud master (`scripts/loud_master.sh`): denser voice, 4×-oversampled look-ahead limiter. Result: -8.3 LUFS, 0 clipped samples.

## Visuals: HyperFrames sub-compositions
`hyperframes/index.html` is the root `main`. It mounts 13 files from `compositions/` with `data-composition-src`, each with a local-time GSAP timeline.

| composition | root time | content |
|---|---|---|
| `hook` | 0–4.02 | spotlight on product, "KULIT LEMBUT macam lepas spa? / BADAN WANGI macam baru pakai perfume?" |
| `mandi` | 4.02–6.84 | foam video, "HANYA DENGAN MANDI" + ripples |
| `secret` | 6.84–13.08 | keyhole → "GARAM laut", 3D salt crystal, Mg / Ca |
| `moist` | 13.08–16.5 | droplet locked in a gold ring, "KEKAL LEMBAP & lembut", silk waves |
| `formula` | 16.5–23.72 | FRESCURA hero: GARAM LAUT + WANGIAN PERFUME MEWAH = 1 FOAMING BODY SHOWER |
| `pump` | 23.72–26.2 | pump video "1× SEKALI PUMP" → foam "BERBUIH lembut" |
| `glory` | 26.2–29.66 | N° I Woman Glory, scent waves, "manis & menggoda" |
| `noche` | 29.66–33.12 | N° II Noche, stars, "lembut & misteri" |
| `listen` | 33.12–36.76 | "DENGAR SINI" sound rings, stock bars → TERHAD |
| `soldout` | 36.76–39.86 | "JANGAN TUNGGU" + neon SOLD OUT typing |
| `cta` | 39.86–45 | KLIK LINK di bawah, CHECK OUT SEKARANG, TEKAN BEG KUNING, "sebelum anda rugi" |
| `captions` | 0–45 | Sora 800 86px, DM Serif italic gold accents, glow on the active word |
| `hud` | 0–45 | FRESCURA + progress line, roman-numeral scene index, light-wipe transitions |

- **Fonts:** Cinzel, DM Serif Display italic, Sora.
- **Media:** only the owner's photos and foam video.
- Some product photos have wrong brand text on the label ("INTOLUSA" / "INTNSLIFE"). Those photos are used only blurred or small. The TikTok Shop screenshot is not used.

```bash
cd hyperframes && npx hyperframes@0.9.19 render -q draft -o preview.mp4   # final: -q high
```
