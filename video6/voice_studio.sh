#!/bin/sh
# Video 6 studio polish (quiet room, floor ~-45 dBFS): audio/voice.wav -> project/assets/audio/voice.wav
set -e
cd "$(dirname "$0")"
CH="highpass=f=90,afftdn=nr=12:nf=-44:tn=1,agate=threshold=0.02:ratio=8:attack=2:release=200:range=0.04:knee=3,equalizer=f=200:t=q:w=1:g=2,equalizer=f=450:t=q:w=1.3:g=-3,equalizer=f=900:t=q:w=1.5:g=-1.5,equalizer=f=3800:t=q:w=1.2:g=3,highshelf=f=10500:g=2,deesser=i=0.4,acompressor=threshold=-18dB:ratio=2.5:attack=5:release=120:makeup=1,aexciter=amount=1.0:drive=3.5:blend=0:freq=6500"
mkdir -p work
ffmpeg -v error -y -i audio/voice.wav -af "$CH" -ar 48000 -ac 1 work/voice_pre.wav
I=$(ffmpeg -v info -i work/voice_pre.wav -af ebur128=framelog=quiet -f null - 2>&1 | grep " I:" | tail -1 | awk '{print $2}')
G=$(python3 -c "print(round(-14-($I),2))")
ffmpeg -v error -y -i work/voice_pre.wav -af "volume=${G}dB,alimiter=limit=0.95:attack=2:release=40" -ar 48000 -ac 1 project/assets/audio/voice.wav
ffmpeg -v error -y -i project/assets/audio/voice.wav -ac 1 -ar 16000 audio/voice16k.wav
