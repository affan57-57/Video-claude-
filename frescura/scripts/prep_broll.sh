#!/usr/bin/env bash
# name src start dur cropx sat
S=$1; P=$2
mk(){ n=$1; src=$2; ss=$3; d=$4; cx=$5; sat=$6
  ffmpeg -v error -y -ss $ss -t $d -i $src -an -vf "crop=ih*9/16:ih:(iw-ih*9/16)*$cx:0,scale=1080:1920:flags=lanczos,fps=30,eq=contrast=1.06:saturation=$sat:gamma=0.97,colorbalance=rh=0.03:bh=-0.03:rs=-0.01:bs=0.02,unsharp=5:5:0.4,format=yuv420p" -c:v libx264 -preset medium -crf 17 -g 15 -movflags +faststart $P/broll/$n.mp4 && echo ok $n; }
ST=$S/stock
mk b01 $ST/23381.mp4 12 4.9 0.45 0.4 &
mk b02 $ST/50966.mp4 1.5 4.9 0.5 1.0 &
mk b03 $ST/42914.mp4 5 2.3 0.55 0.85 &
mk b04 $ST/21769.mp4 2 1.7 0.62 0.85 &
wait
mk b05 $ST/34517.mp4 3 2.4 0.55 0.9 &
mk b07 $ST/9253.mp4 1 1.9 0.72 0.85 &
mk b09 $ST/22402.mp4 5 1.3 0.5 0.8 &
mk b10 $ST/6824.mp4 4 1.2 0.15 1.0 &
wait
mk b11 $ST/23437.mp4 6 1.3 0.5 0.85 &
mk b12 $ST/4148.mp4 3 3.6 0.5 1.1 &
mk b14 $ST/6824.mp4 9 2.2 0.1 1.0 &
mk b15 $ST/9163.mp4 1 2.5 0.35 0.7 &
wait
mk b16 $ST/42136.mp4 1 3.0 0.5 0.85 &
mk b17 $ST/14529.mp4 3 2.0 0.5 0.8 &
# foam clip is already portrait 720x1280
ffmpeg -v error -y -ss 2.6 -t 1.8 -i $S/dl/foam.mp4 -an -vf "scale=1080:1920:flags=lanczos,fps=30,eq=contrast=1.05:saturation=1.05,unsharp=5:5:0.6,format=yuv420p" -c:v libx264 -crf 17 -g 15 -movflags +faststart $P/broll/foam_pump.mp4 && echo ok foam1 &
ffmpeg -v error -y -ss 25 -t 1.8 -i $S/dl/foam.mp4 -an -vf "scale=1080:1920:flags=lanczos,fps=30,eq=contrast=1.05:saturation=1.05,unsharp=5:5:0.6,format=yuv420p" -c:v libx264 -crf 17 -g 15 -movflags +faststart $P/broll/foam_lather.mp4 && echo ok foam2 &
ffmpeg -v error -y -ss 12 -t 1.8 -i $S/dl/foam.mp4 -an -vf "scale=1080:1920:flags=lanczos,fps=30,eq=contrast=1.05:saturation=1.05,unsharp=5:5:0.6,format=yuv420p" -c:v libx264 -crf 17 -g 15 -movflags +faststart $P/broll/foam_hand.mp4 && echo ok foam3 &
wait
