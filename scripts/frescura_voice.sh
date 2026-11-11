set -e
CHAIN="highpass=f=85:poles=2,equalizer=f=250:t=q:w=1.0:g=-2,equalizer=f=3000:t=q:w=1.2:g=3,equalizer=f=5500:t=q:w=1.2:g=1.5,highshelf=f=10000:g=2,deesser=i=0.35:m=0.5:f=0.5,acompressor=threshold=-22dB:ratio=3:attack=6:release=110:knee=4:makeup=3dB"
seg(){ echo "[0]atrim=$1:$2,asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st=$(python3 -c "print($2-$1-0.015)"):d=0.015[$3];"; }
# intro
ffmpeg -v error -y -i wav/main_df.wav -filter_complex "$(seg 0 2.94 a)$(seg 3.06 7.00 b)[a][b]concat=n=2:v=0:a=1,atempo=1.15,$CHAIN,loudnorm=I=-14:TP=-1.5:LRA=7,aresample=48000" -c:a pcm_f32le wav/v_intro.wav
ffmpeg -v error -y -i wav/main_df.wav -filter_complex "$(seg 9.10 12.02 a)$(seg 12.30 13.40 b)$(seg 13.62 21.12 c)[a][b][c]concat=n=3:v=0:a=1,atempo=1.15,$CHAIN,loudnorm=I=-14:TP=-1.5:LRA=7,aresample=48000" -c:a pcm_f32le wav/v_close.wav
# feedback: keep user's edit, just gentle loudness match + light presence
ffmpeg -v error -y -i dl/feedback.mp4 -vn -af "highpass=f=70,equalizer=f=3000:t=q:w=1.2:g=2,acompressor=threshold=-20dB:ratio=2:attack=8:release=150:makeup=1dB,loudnorm=I=-15:TP=-1.5:LRA=8,aresample=48000" -ac 1 -c:a pcm_f32le wav/v_fb.wav
for f in v_intro v_close v_fb; do printf "%s %s\n" $f $(ffprobe -v error -show_entries format=duration -of csv=p=0 wav/$f.wav); done
