#!/usr/bin/env bash
# name  src  start  dur  W H  cropfilter(optional)
set -e
O=proj/assets/v
mk(){ n=$1; s=$2; ss=$3; d=$4; vf=$5
  ffmpeg -v error -y -ss $ss -t $d -i $s -an -vf "$vf,fps=30,format=yuv420p" -c:v libx264 -preset medium -crf 16 -g 10 -bf 0 -movflags +faststart $O/$n.mp4; echo "$n ok"; }
# hook top: rose landing (slow-mo) 1080x960; rose sits right of centre
mk rose_splash broll/29439.mp4 2.0 4.2 "crop=810:720:400:0,scale=1080:960:flags=lanczos,unsharp=5:5:0.6"
# hook bottom: stardust mountains 1080x960
mk night_hook broll/46203.mp4 0.5 4.2 "crop=810:720:235:0,scale=1080:960:flags=lanczos,unsharp=5:5:0.5"
# WG scene: pump foam into palm (vertical source 720x1280)
mk wg_pump src/pump.mov 2.7 3.4 "scale=1080:1920:flags=lanczos,unsharp=5:5:0.5"
# Noche scene: milky way, full bleed
mk noche_sky broll/4148.mp4 1.0 3.6 "crop=405:720:430:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.4"
# formula circles
mk perfume broll/20766.mp4 0.0 3.0 "crop=720:720:420:0,scale=540:540:flags=lanczos"
mk seasalt broll/22402.mp4 4.0 3.0 "crop=720:720:280:0,scale=540:540:flags=lanczos"
# minerals: turquoise foaming ocean full bleed
mk ocean broll/2091.mp4 3.0 4.8 "crop=405:720:440:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.4"
# soft skin: pump into palm then model touching skin
mk pump_palm src/pump.mov 10.4 1.2 "scale=1080:1920:flags=lanczos,unsharp=5:5:0.5"
mk skin broll/48616.mp4 1.0 1.6 "crop=405:720:410:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5"
# ASMR lather
mk lather src/pump.mov 14.6 1.6 "scale=1080:1920:flags=lanczos,unsharp=5:5:0.5"
mk lather2 src/pump.mov 25.2 1.0 "scale=1080:1920:flags=lanczos,unsharp=5:5:0.5"
