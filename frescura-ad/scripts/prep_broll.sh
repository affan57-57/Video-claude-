#!/usr/bin/env bash
# Prepare B-roll for the Frescura Body ad: trim, crop to the frame each scene uses, bake a warm
# "luxury boutique" grade, strip audio. Usage: scripts/prep_broll.sh <stock_dir> <foam.mp4> <out_dir>
# Stock clips are free Mixkit clips (mixkit.co, Mixkit License); foam.mp4 is the brand's own pump clip.
set -euo pipefail
SRC=$1; FOAM=$2; OUT=$3; mkdir -p "$OUT"
GRADE="eq=contrast=1.06:saturation=0.90:gamma=0.98,colorbalance=rs=0.02:bs=-0.03:rh=0.03:gh=0.01:bh=-0.04,curves=all='0/0.035 0.5/0.49 1/0.97',unsharp=5:5:0.45"
ENC="-an -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -r 30 -movflags +faststart"

# win: 1080x1320 portrait window (9:11), cropped from the centre (x offset as a fraction of slack)
win() { # name src start dur xfrac
  ffmpeg -v error -y -ss "$3" -t "$4" -i "$SRC/$2.mp4" -vf "scale=-2:1320:flags=lanczos,crop=1080:1320:(iw-1080)*$5:0,$GRADE" $ENC "$OUT/$1.mp4"
  echo "win  $1"
}
# full: 1080x1920 full-bleed from vertical or centre-cropped landscape
full() { # name src start dur xfrac
  ffmpeg -v error -y -ss "$3" -t "$4" -i "$2" -vf "scale=-2:1920:flags=lanczos,crop=1080:1920:(iw-1080)*$5:0,$GRADE" $ENC "$OUT/$1.mp4"
  echo "full $1"
}

win couple      couple       0.8 2.4 0.55
win hands       hands        1.5 2.4 0.50
win smellroses  smellroses   2.5 2.6 0.50
win brushes     brushes      0.0 4.2 0.45
win maketools   maketools    1.0 4.2 0.50
win handsoap    handsoap     2.6 2.8 0.62
win steamclothes steamclothes 6.0 2.2 0.50
win showerstream showerstream 2.0 3.0 0.50
win redroses    redroses     0.5 5.0 0.50
win stars       stars        0.5 5.0 0.45
win mall        mallperfume  2.0 5.0 0.40
full rosedrops  "$SRC/roseDrops.mp4" 0.5 2.6 0.5
full ripples    "$SRC/ripples.mp4"   0.0 2.6 0.5
full bubbles    "$SRC/bubblespink.mp4" 2.0 4.0 0.5

# The brand's own foam clip: lighter grade (keep the pink foam true to life)
FG="eq=contrast=1.05:saturation=1.06:gamma=0.99,colorbalance=rh=0.02:bh=-0.02,unsharp=5:5:0.5"
ffmpeg -v error -y -ss 3.0 -t 3.4 -i "$FOAM" -vf "scale=1080:1920:flags=lanczos,$FG" $ENC "$OUT/foam-pump.mp4"; echo "full foam-pump"
ffmpeg -v error -y -ss 10.0 -t 3.6 -i "$FOAM" -vf "scale=1080:1920:flags=lanczos,$FG" $ENC "$OUT/foam-hand.mp4"; echo "full foam-hand"
