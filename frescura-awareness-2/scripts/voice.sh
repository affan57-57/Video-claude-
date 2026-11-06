#!/usr/bin/env bash
# voice_cut.wav -> voice_final.wav : tempo + studio chain + 2-pass loudnorm
set -e; T=${1:-1.12}
CHAIN="highpass=f=85:poles=2,equalizer=f=250:t=q:w=1.0:g=-2.5,equalizer=f=3000:t=q:w=1.0:g=3,equalizer=f=5500:t=q:w=1.2:g=1.5,highshelf=f=10000:g=2,lowshelf=f=140:g=1.5,deesser=i=0.35:m=0.5:f=0.5,acompressor=threshold=-22dB:ratio=3:attack=6:release=110:knee=4:makeup=3dB,alimiter=limit=0.9:attack=3:release=40:level=false"
ffmpeg -v error -y -i voice_cut.wav -af "rubberband=tempo=$T:pitchq=quality:formant=preserved:transients=crisp:detector=compound:window=short,$CHAIN" -ar 48000 -c:a pcm_f32le voice_fast.wav
MI=$(ffmpeg -hide_banner -i voice_fast.wav -af loudnorm=I=-12:TP=-1.0:LRA=6:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p' | python3 -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -v error -y -i voice_fast.wav -af "loudnorm=I=-12:TP=-1.0:LRA=6:$MI:linear=true,aresample=48000" -c:a pcm_f32le voice_final.wav
ffprobe -v error -show_entries format=duration -of csv=p=0 voice_final.wav
