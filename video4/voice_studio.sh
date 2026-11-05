#!/bin/sh
# Video 4 v3 studio polish on the cut voice (audio/voice.wav -> project/assets/audio/voice.wav):
# denoise, gate the car-cabin room tone, close-mic warmth, cut cabin "box", presence + air, de-ess,
# gentle glue compression, exciter sheen; static gain to -14 LUFS (no dynamic loudnorm, so gaps stay quiet).
set -e
cd "$(dirname "$0")"
CH="highpass=f=75,afftdn=nr=12:nf=-44:tn=1,agate=threshold=0.028:ratio=10:attack=2:release=180:range=0.03:knee=3,equalizer=f=120:t=q:w=0.9:g=3,equalizer=f=420:t=q:w=1.3:g=-3.5,equalizer=f=850:t=q:w=1.5:g=-1.5,equalizer=f=4200:t=q:w=1.2:g=3,highshelf=f=11000:g=2.5,deesser=i=0.35,acompressor=threshold=-18dB:ratio=2.5:attack=5:release=120:makeup=1,aexciter=amount=1.2:drive=4:blend=0:freq=6500"
ffmpeg -v error -y -i audio/voice.wav -af "$CH" -ar 48000 -ac 1 work/voice_v3_pre.wav
I=$(ffmpeg -v info -i work/voice_v3_pre.wav -af ebur128=framelog=quiet -f null - 2>&1 | grep " I:" | tail -1 | awk '{print $2}')
G=$(python3 -c "print(round(-14-($I),2))")
ffmpeg -v error -y -i work/voice_v3_pre.wav -af "volume=${G}dB,alimiter=limit=0.95:attack=2:release=40" -ar 48000 -ac 1 project/assets/audio/voice.wav
