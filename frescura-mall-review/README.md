# FRESCURA BODY – Mall review edit (PREVIEW)

Structure: F7 intro (hook) → F6 customer feedback → F7 closing → end card. ~35 s, 1080×1920.

- `tools/build_voice.py` – cuts/speeds the voice (F7 ×1.12, F6 ×1.06), removes pauses + repeated "tak tipu" lines. `segments.json` = source→output time map.
- Audio cleanup: Demucs htdemucs_ft (vocals) → DeepFilterNet3 (18 dB) → studio EQ/de-ess/compression → −13 LUFS.
- `tools/gen.py` – writes the HyperFrames project (`hyperframes/index.html`, `compositions/*.html`).
- Video assets (not committed): `hyperframes/assets/video/pump.mp4` (from "tekan pump yg baru.MOV") and `review.mp4` (from F6.MOV), H.264 -g 15, light grade.
- Render: `cd hyperframes && npx hyperframes render -q delivery -o final.mp4`
