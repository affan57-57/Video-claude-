import subprocess, json, sys, re
S, P = sys.argv[1], sys.argv[2]; X=f"{P}/assets/sfx"; OUT=f"{P}/assets/audio/mix.wav"; DUR=33.0
cues=[("impact",0.0,-4),("shimmer",0.05,-14),("swoosh",0.2,-12),
 ("swoosh",1.42,-11)]+[("tick",1.5+i*0.14,-15) for i in range(10)]+[
 ("swoosh_low",2.95,-9),("pop",3.4,-10),("pop",3.9,-10),("pop",4.45,-10),("pop",5.05,-10),
 ("swoosh",5.6,-11),("thump",5.95,-6),("thump",6.55,-7),
 ("riser",6.1,-12),("swoosh",7.3,-8),("shimmer",7.45,-11),("ding",9.6,-12),
 ("swoosh",11.25,-10),("bubbles",12.0,-12),("pop",12.9,-12),("bubbles",13.5,-12),
 ("swoosh",14.65,-8),("impact",15.55,-13),("shimmer",15.95,-13),("swoosh_low",16.42,-11),("shimmer",16.8,-13),
 ("swoosh",17.55,-11),("swoosh_low",19.25,-10),("ding",19.54,-13),("tick",19.5,-10),("tick",19.9,-10),("tick",20.3,-10),
 ("swoosh",21.3,-8),("pop",21.5,-9),("tap",21.86,-5),("pop",22.9,-12)]+[("tick",23.2+i*0.12,-14) for i in range(11)]+[
 ("impact",23.72,-12),
 ("swoosh",24.62,-10),("tap",25.66,-5),("success",25.82,-9),("kaching",25.9,-10),
 ("swoosh_low",27.3,-10),("shimmer",28.9,-11),("reverse",29.05,-12),("swoosh",29.8,-8),("impact",29.95,-6),("shimmer",30.0,-10),("pop",30.5,-10),("ding",32.0,-13)]
ins=["-i",f"{S}/work/voice_studio.wav","-i",f"{S}/work/music.wav"]; fg=[]
for i,(n,t,db) in enumerate(cues):
    ins+=["-i",f"{X}/{n}.wav"]; ms=int(t*1000)
    fg.append(f"[{i+2}]aresample=48000,aformat=channel_layouts=stereo,volume={db}dB,adelay={ms}|{ms}[s{i}]")
fg.append("[0]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay=1000|1000,apad=whole_dur=33,asplit=2[v][vk]")
fg.append("[1]aformat=channel_layouts=stereo,volume=-15dB,atrim=0:33[m0]")
fg.append("[m0][vk]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350:makeup=1[m]")
fg.append("".join(f"[s{i}]" for i in range(len(cues)))+f"amix=inputs={len(cues)}:normalize=0:duration=longest,volume=-1dB[fx]")
fg.append("[v][m][fx]amix=inputs=3:normalize=0:duration=first,atrim=0:33,afade=t=out:st=32.2:d=0.8,alimiter=limit=0.89:attack=2:release=60:level=false[pre]")
def run(extra, af):
    cmd=["ffmpeg","-v","info","-y",*ins,"-filter_complex",";".join(fg)+f";[pre]{af}[out]","-map","[out]",*extra]
    return subprocess.run(cmd,capture_output=True,text=True)
r=run(["-f","null","-"],"loudnorm=I=-13:TP=-1.2:LRA=9:print_format=json")
j=json.loads(re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}",r.stderr)[-1])
af=(f"loudnorm=I=-13:TP=-1.2:LRA=9:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:"
    f"measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aresample=48000")
r=run(["-c:a","pcm_s24le",OUT],af); print(r.returncode, r.stderr[-300:] if r.returncode else "ok", len(cues),"cues")
