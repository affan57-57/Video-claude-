#!/usr/bin/env bash
# Voice: Demucs vocals -> DeepFilterNet3 -> edit cuts (fillers/repeat/pauses) -> 1.1x -> studio chain -> -14 LUFS
# Usage: voice.sh WORKDIR   (expects WORKDIR/au/sep/htdemucs_ft/orig/vocals.wav, WORKDIR/models/DF3)
set -euo pipefail
W=$1; D=$(cd "$(dirname "$0")/.." && pwd)
ffmpeg -v error -y -i $W/au/sep/htdemucs_ft/orig/vocals.wav -ar 48000 -ac 1 $W/au/voc48.wav
[ -f $W/au/voc_df.wav ] || (cd /tmp && ATT=18 python3 "$D/run_df.py" $W/models/DF3 $W/au/voc48.wav $W/au/voc_df.wav)

# Keep-list (source seconds). Removed: "So," x3, repeated "kita duduk dengan dia,", long pauses.
KEEP="0.00:4.32 4.48:9.72 9.84:16.30 17.06:26.60 27.34:30.82 31.78:32.92 33.43:37.40"
F=""; i=0; L=""
for k in $KEEP; do a=${k%:*}; b=${k#*:}
  F+="[0]atrim=$a:$b,asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st=$(python3 -c "print($b-$a-0.025)"):d=0.025[s$i];"; L+="[s$i]"; i=$((i+1)); done
F+="${L}concat=n=$i:v=0:a=1[c]"
ffmpeg -v error -y -i $W/au/voc_df.wav -filter_complex "$F" -map "[c]" $W/au/voc_cut.wav

CHAIN="atempo=1.1,highpass=f=85:poles=2,equalizer=f=250:t=q:w=1.0:g=-2,equalizer=f=120:t=q:w=0.9:g=1.5,equalizer=f=3000:t=q:w=1.0:g=3,equalizer=f=5500:t=q:w=1.2:g=1.5,highshelf=f=10000:g=2,deesser=i=0.35:m=0.5:f=0.5,acompressor=threshold=-22dB:ratio=3:attack=6:release=110:knee=4:makeup=3dB,alimiter=limit=0.9:level=false"
ffmpeg -v error -y -i $W/au/voc_cut.wav -af "$CHAIN" $W/au/voc_chain.wav
ffmpeg -v error -y -i $W/au/voc_chain.wav -af "loudnorm=I=-14:TP=-1.5:LRA=6,aresample=48000" -c:a pcm_s24le $W/au/voice_studio.wav
ffprobe -v error -show_entries format=duration -of csv=p=0 $W/au/voice_studio.wav
