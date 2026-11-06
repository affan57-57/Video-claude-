#!/usr/bin/env bash
# Louder, clean master for awareness #3 (no clipping).
# 1) densify voice  2) mix with headroom  3) 4x-oversampled look-ahead limiter -> about -8.4 LUFS, true peak -1.8 dBFS
set -e; D=$(dirname "$0")
ffmpeg -v error -y -i voice_final.wav -af "acompressor=threshold=-20dB:ratio=3:attack=4:release=90:knee=6:makeup=1dB,volume=8dB,alimiter=limit=0.84:attack=5:release=80:level=false:asc=1" -c:a pcm_f32le voice_loud.wav
GAIN=-4 python3 -I "$D/sound_v3.py" voice_loud.wav mix_pre.wav
ffmpeg -v error -y -i mix_pre.wav -af "aresample=192000,volume=6dB,alimiter=limit=0.80:attack=5:release=60:level=false:asc=1,aresample=48000" -c:a pcm_s24le mix.wav
