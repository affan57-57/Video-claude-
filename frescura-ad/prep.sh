# name src ss dur speed xoff(0..1 crop position)
mk(){ n=$1; src=$2; ss=$3; d=$4; sp=$5; xo=${6:-0.5}; ff=${7:-}
 ffmpeg -v error -y -ss $ss -t $(python3 -c "print($d*$sp)") -i $src -an -vf "setpts=PTS/$sp,fps=30,scale=-2:1920:flags=lanczos,crop=1080:1920:(iw-1080)*$xo:0,eq=contrast=1.06:saturation=0.86:gamma=0.97${ff},vignette=PI/5,format=yuv420p" -c:v libx264 -preset medium -crf 18 -g 15 -movflags +faststart $n.mp4 && echo "$n $(ffprobe -v error -show_entries format=duration -of csv=p=0 $n.mp4)"; }
mk c01 b4748.mp4 0.5 3.6 1 0.5
mk c02 b46708.mp4 1.5 1.8 1 0.55
mk c03 b33379.mp4 1.0 1.9 1 0.6
mk c04 b18303.mp4 0 5.4 1 0.5
mk c05 b46804.mp4 0 5.2 1 0.45
mk c06 b33635.mp4 0.5 3.8 1 0.5
mk c07 b14839.mp4 0 2.4 1 0.55
mk c07b b8755.mp4 2 1.6 1 0.5
mk c10 b17852.mp4 2 1.8 2 0.5
mk c11 b4148.mp4 0 2.2 1 0.5
mk c13 b25334.mp4 0.5 2.0 1 0.6
mk c14 b44834.mp4 1 2.2 1 0.5
mk c15 b42123.mp4 1 2.8 1 0.55
mk c16 b23437.mp4 1 2.0 1 0.5
mk c12 b1869.mp4 2 2.2 1 0.5
