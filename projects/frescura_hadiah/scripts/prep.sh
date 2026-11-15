#!/bin/bash
# name src start dur speed xoff(0..1 crop position)
S=stock; O=hf/proj/media
GRADE="eq=contrast=1.07:saturation=0.92:brightness=-0.01,colorbalance=rs=0.03:gs=0.01:bs=-0.04:rh=0.03:bh=-0.03,unsharp=5:5:0.6"
mk(){ n=$1; src=$2; ss=$3; d=$4; sp=$5; xo=$6
  ffmpeg -v error -y -ss $ss -t $(python3 -c "print($d*$sp+0.1)") -i $src -an -vf "setpts=PTS/$sp,crop=ih*9/16:ih:(iw-ih*9/16)*$xo:0,scale=1080:1920:flags=lanczos,$GRADE,fps=30,format=yuv420p" -c:v libx264 -preset fast -crf 17 -g 15 -t $d $O/$n.mp4; echo "$n $(ffprobe -v error -show_entries format=duration -of csv=p=0 $O/$n.mp4)"; }
mk s0_mall    $S/v25516.mp4 0.5 2.2 1   0.5
mk s1_door    $S/v21812.mp4 2.0 1.7 1.2 0.55
mk s2_gift    $S/v14839.mp4 4.0 1.7 1   0.45
mk s3_hug     $S/v6607.mp4  9.5 1.4 1   0.5
mk s4_cheek   $S/v930.mp4   3.0 3.0 1   0.45
mk s5_store   $S/v21980.mp4 2.0 2.0 1   0.5
mk s6_roses   $S/v6824.mp4  2.0 2.0 1   0.3
mk s7_sky     $S/v4148.mp4  0.0 1.6 1.4 0.5
mk s9_busy    $S/v6749.mp4  1.0 2.9 1.3 0.5
mk s10a_emb   $S/v42975.mp4 3.0 1.6 1   0.5
mk s10b_joy   $S/v4643.mp4  9.0 1.4 1   0.55
mk s11_mall   $S/v23437.mp4 6.0 1.9 1   0.6
mk s12_lav    $S/v1244.mp4  1.0 4.4 1   0.5
mk s14_spray  $S/v20766.mp4 0.5 4.3 1   0.6
# pump (already portrait)
ffmpeg -v error -y -ss 2.8 -t 3.0 -i src/pump.mov -an -vf "setpts=PTS/1.4,scale=1080:1920:flags=lanczos,$GRADE,fps=30,format=yuv420p" -c:v libx264 -crf 17 -g 15 -t 2.1 $O/s8a_pump.mp4
ffmpeg -v error -y -ss 17.5 -t 3.0 -i src/pump.mov -an -vf "setpts=PTS/1.5,scale=1080:1920:flags=lanczos,$GRADE,fps=30,format=yuv420p" -c:v libx264 -crf 17 -g 15 -t 1.8 $O/s8b_foam.mp4
ls $O | wc -l
