#!/bin/bash
# build pump.webm (VP9+alpha) from BiRefNet cutout frames starting at src 6.0s (frame 0060), 15 fps
S=$1; OUT=$2; rm -rf $S/cut/seq; mkdir -p $S/cut/seq; k=0
for f in $(ls $S/cut/out/*.png | sort); do n=$(basename $f .png); [ $((10#$n)) -lt 60 ] && continue; cp $f $S/cut/seq/$(printf %04d $k).png; k=$((k+1)); done
ffmpeg -v error -y -framerate 15 -i $S/cut/seq/%04d.png -vf "scale=928:1696:flags=lanczos,fps=30,format=yuva420p" -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 24 -row-mt 1 -deadline good -cpu-used 4 -auto-alt-ref 0 $OUT
echo "frames $k"
