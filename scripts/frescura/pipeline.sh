#!/usr/bin/env bash
# Frescura Body awareness ad (30-40s, 9:16): transcript-driven HyperFrames edit.
# Usage: scripts/frescura/pipeline.sh main.mov pump.mov PHOTO_DIR WORK_DIR [final]
# Needs: ffmpeg, node 22 + hyperframes@0.9.33, python: faster-whisper, deepfilternet, torch, scipy, soundfile, safetensors
# DF3 weights: huggingface.co/fal/DeepFilterNet3 (model.safetensors -> checkpoints/model_120.ckpt.best + config.ini)
set -euo pipefail
MAIN=$1; PUMP=$2; PHOTOS=$3; W=$4; MODE=${5:-preview}; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p $W && cd $W
ffmpeg -y -i "$MAIN" -vn -ac 1 -ar 48000 main48.wav && ffmpeg -y -i "$MAIN" -vn -ac 1 -ar 16000 main16.wav
# 1) word-level transcript (Malay)
python3 -c "
import soundfile as sf, json; from faster_whisper import WhisperModel
a,_=sf.read('main16.wav',dtype='float32'); m=WhisperModel('medium',device='cpu',compute_type='int8')
s,_=m.transcribe(a,language='ms',word_timestamps=True,initial_prompt='Self care. Frescura Body. Woman Glory Bombshell. Noche Midnight Fantasy.')
json.dump([dict(s=round(w.start,2),e=round(w.end,2),t=w.word.strip()) for g in s for w in g.words],open('words_fw.json','w'))"
# 2) denoise (DeepFilterNet3, full) -> cut repeat + dead air -> 1.1x -> studio chain
python3 "$D/../run_df.py" models/DF3 main48.wav df_full.wav
python3 "$D/edit_voice.py" df_full.wav words_fw.json voice_cut.wav words_edit.json 1.1
ffmpeg -y -i voice_cut.wav -af "atempo=1.1,highpass=f=85:poles=2,equalizer=f=250:t=q:w=1.0:g=1.5,equalizer=f=420:t=q:w=1.2:g=-3,equalizer=f=3400:t=q:w=1.0:g=3,equalizer=f=6500:t=q:w=1.2:g=1.5,highshelf=f=10000:g=2,deesser=i=0.35:m=0.5:f=0.5,acompressor=threshold=-22dB:ratio=3:attack=6:release=110:knee=4:makeup=3dB,aexciter=amount=1.2:drive=4:freq=4500:blend=0,loudnorm=I=-13:TP=-1.2:LRA=6,aresample=48000" -c:a pcm_s24le voice_studio.wav
# 3) B-roll cut + luxury grade
[ -d hf ] || npx hyperframes init hf --example blank --resolution portrait --non-interactive --skip-transcribe --skip-skills
mkdir -p hf/assets
G="scale=1080:1920:flags=lanczos,eq=contrast=1.12:brightness=-0.05:saturation=1.12:gamma=0.92,curves=preset=medium_contrast,colorbalance=rs=0.03:bs=-0.02:rh=0.02,vignette=PI/4.2,unsharp=5:5:0.6,fps=30,format=yuv420p"
for c in "p1 2.2 4.2" "p2 10.4 3.4" "p3 18.8 4.0" "p4 25.8 4.0" "p5 30.5 3.0"; do set -- $c
  ffmpeg -y -ss $2 -t $3 -i "$PUMP" -an -vf "$G" -c:v libx264 -crf 16 -g 15 hf/assets/$1.mp4; done
cp "$PHOTOS"/logo.jpg "$PHOTOS"/duo_table.jpg "$PHOTOS"/duo_wet.jpg "$PHOTOS"/duo_curve.jpg hf/assets/
# 4) composition + SFX + mix
python3 "$D/build.py" words_edit.json hf/index.html
python3 "$D/make_sfx.py" sfx 34.0
python3 "$D/mix.py" voice_studio.wav sfx hf/index_cues.json mix_raw.wav
ffmpeg -y -i mix_raw.wav -af "loudnorm=I=-11:TP=-1.0:LRA=8,alimiter=limit=0.89:attack=3:release=60:level=false,aresample=48000" -c:a pcm_s24le mix_final.wav
# 5) render (draft preview by default; pass 'final' for full quality) and mux
Q=draft; [ "$MODE" = final ] && Q=delivery
(cd hf && npx hyperframes render -q $Q -o ../video_$MODE.mp4)
ffmpeg -y -i video_$MODE.mp4 -i mix_final.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart frescura_$MODE.mp4
