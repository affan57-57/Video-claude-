# Frescura Body — awareness video (HyperFrames)
32 s, 1080x1920, luxury-mall look. Voice from `2.MOV` (Drive), foam B-roll from `tekan pump yg baru.MOV`.
1. `tx.py` transcribe -> `words.json`; `timing.py` cuts pauses, 1.10x speed, captions -> `captions.json`, `edl.json`
2. Demucs htdemucs_ft vocals -> DeepFilterNet3 (ATT=14) -> cut/atempo/studio EQ+de-ess+comp -> `voice_final.wav`
3. `synth_audio.py` music bed (122 BPM) + SFX kit; `mix.py` mix -> loudnorm -11 LUFS -> `assets/audio/mix.wav`
4. `build.sh` injects captions into `index.src.html` -> `index.html`; `npx hyperframes render`
