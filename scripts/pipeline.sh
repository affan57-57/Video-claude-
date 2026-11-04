#!/usr/bin/env bash
# Q&A testimonial video cleanup: denoise -> studio voice -> SFX -> AI sharpen.
# Usage: scripts/pipeline.sh input.mp4 output.mp4   (needs ffmpeg, demucs, deepfilternet, torch, safetensors, pillow, numpy, scipy, soundfile)
# Models (safetensors, from Hugging Face): fal/DeepFilterNet3 -> models/DF3 (config.ini + checkpoints/model_120.ckpt.best),
#                                          OzzyGT/RealESRGAN_general_x4v3 -> models/esr_general_x4v3.safetensors
set -euo pipefail
IN=$1; OUT=$2; D=$(dirname "$0"); W=work; mkdir -p $W/fr_in sfx

# 1) Audio: separate voice from mall noise (Demucs), then DeepFilterNet3 limited to 12 dB
ffmpeg -y -i "$IN" -vn -ar 44100 -ac 2 $W/orig.wav
demucs -n htdemucs_ft --two-stems=vocals -o $W/sep $W/orig.wav
ffmpeg -y -i $W/sep/htdemucs_ft/orig/vocals.wav -ar 48000 -ac 1 $W/vocals_48k.wav
ATT=12 python "$D/run_df.py" models/DF3 $W/vocals_48k.wav $W/df_voc12.wav

# 2) Studio voice chain (EQ, de-esser, compression) + loudness -14 LUFS
CHAIN="highpass=f=80:poles=2,equalizer=f=320:t=q:w=1.2:g=-2.5,equalizer=f=3200:t=q:w=1.1:g=2.5,equalizer=f=6000:t=q:w=1.2:g=1.5,highshelf=f=9000:g=1.5,deesser=i=0.3:m=0.5:f=0.5,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:knee=4:makeup=2dB"
ffmpeg -y -i $W/df_voc12.wav -af "$CHAIN,loudnorm=I=-14:TP=-1.5:LRA=7,aresample=48000" -c:a pcm_f32le $W/voice_studio.wav

# 3) SFX (synthesized) placed on transcript cues
python "$D/make_sfx.py" sfx
X=sfx
ffmpeg -y -i $W/voice_studio.wav -i $X/whoosh.wav -i $X/chime.wav -i $X/sparkle.wav -i $X/ding.wav -i $X/sparkle.wav -i $X/pop.wav -i $X/applause.wav -i $X/tada.wav -filter_complex "
[0]pan=stereo|c0=0.7071*c0|c1=0.7071*c0,apad=pad_dur=1.3[v];
[1]volume=-21dB,adelay=0:all=1[s1];      [2]volume=-17dB,adelay=5650:all=1[s2];
[3]volume=-22dB,adelay=6850:all=1[s3];   [4]volume=-20dB,adelay=8450:all=1[s4];
[5]volume=-25dB,adelay=13300:all=1[s5];  [6]volume=-15dB,adelay=15000:all=1[s6];
[7]volume=-26dB,adelay=18700:all=1[s7];  [8]volume=-18dB,adelay=19000:all=1[s8];
[v][s1][s2][s3][s4][s5][s6][s7][s8]amix=inputs=9:normalize=0:duration=first,atrim=0:20.7,afade=t=out:st=20.0:d=0.7,alimiter=limit=0.84:attack=2:release=50:level=false" -c:a pcm_s24le $W/final_audio.wav

# 4) Video: Real-ESRGAN general-x4v3 per frame (output resized to 1080x1976), then light finishing
ffmpeg -y -i "$IN" -vsync 0 $W/fr_in/%05d.png
TILE=384 python "$D/esr.py" models/esr_general_x4v3.safetensors $W/fr_in $W/fr_esr
