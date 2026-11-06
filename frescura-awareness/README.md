# Frescura Body — video awareness "Garam Laut" (45s, 9:16)

Status: **PREVIEW**. The final film has not been rendered yet. It waits for the owner's approval.

## Pipeline
1. **Transcribe**: Whisper large-v3 (Malay) with word timestamps, run on the 2 source clips (`scripts/transcribe.py`).
2. **Voice cleanup**: Demucs (htdemucs_ft) separates the voice, then DeepFilterNet3 removes noise (noise floor -42 → -60 dB).
3. **Edit** (`scripts/edl.py`): cuts the "Bu-" stutter, the cut-off "garam la...", the repeated line "Sebab stok sangat-sangat terhad" and the unclear last line, and shortens pauses longer than 80 ms. Result: 49.3s.
4. **Pace + studio voice** (`scripts/voice.sh`): rubberband tempo ×1.115 (formants preserved), EQ, de-esser, compressor, loudnorm at -12 LUFS. Voice length: 44.2s.
5. **SFX + music** (`scripts/sound.py`): all SFX are synthesised and placed on cues (impact, whoosh, riser, shimmer, clack, scrub, bubbles, clock tick, ding). The 112 BPM minimal beat ducks under the voice. Final mix is about -12 LUFS.
6. **Visuals**: HyperFrames composition (`hyperframes/index.html`): 16 scenes, Wikimedia Commons B-roll, product photos, educational motion graphics and karaoke captions (Bodoni Moda + Outfit).

## Render
```bash
cd hyperframes
npx hyperframes@0.9.19 render -q draft -o preview.mp4      # preview
npx hyperframes@0.9.19 render -q high  -o final.mp4        # final (after approval)
```
B-roll credits: see `CREDITS.md`.
