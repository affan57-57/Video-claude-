import subprocess
A="aud/"
cues=[("thump",0.0,-6),("impact",0.02,-8),("whoosh",2.0,-14),("pop",3.98,-12),("riser",3.15,-12),("impact",4.35,-10),("whoosh_down",4.3,-14),
("tick",5.7,-10),("tick",6.4,-10),("swipe",6.05,-14),("tick",7.05,-10),("nope",8.42,-11),
("whoosh",8.85,-14),("pop",9.14,-11),("pop",10.08,-11),("ding",11.6,-14),
("swipe",12.58,-14),("glitch",14.38,-12),("swipe",14.4,-13),
("whoosh",16.05,-14),("pop",16.84,-11),("pop",17.28,-11),("pop",18.14,-11),("shimmer",18.14,-17),("swipe",17.98,-15),
("riser",18.3,-13),("impact",19.5,-8),("shimmer",19.55,-13),("ding",20.14,-13),("whoosh",20.88,-14),("bubbles",21.24,-12),("swipe",21.9,-15),
("whoosh_down",23.15,-14),("shimmer",24.42,-14),("shimmer",25.66,-14),("swipe",24.85,-15),
("whoosh",26.28,-14),("swipe",27.38,-15),("bubbles",27.45,-13),
("swipe",28.78,-14),("tap",29.15,-8),("pop",29.4,-10),("kaching",30.3,-12),
("impact",31.3,-11),("tick",31.9,-13),("tick",32.3,-13),("tick",32.7,-13),("whoosh",33.05,-14),("ding",34.26,-13),
("impact",34.62,-8),("shimmer",34.7,-12)]
VO=0.3
inp=["-i","work_voice.wav","-i",A+"music.wav"]+sum([["-i",A+n+".wav"] for n,_,_ in cues],[])
f=[f"[0]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay={int(VO*1000)}:all=1,apad=whole_dur=37.4,volume=1.0,asplit=2[v][vsc]",
   "[1]volume=-15dB,atrim=0:37.4[mus0]",
   "[mus0][vsc]sidechaincompress=threshold=0.04:ratio=6:attack=15:release=250:makeup=1[mus]"]
lab=[]
for i,(n,t,db) in enumerate(cues):
    f.append(f"[{i+2}]volume={db}dB,adelay={int(t*1000)}:all=1[s{i}]"); lab.append(f"[s{i}]")
f.append("[v][mus]"+"".join(lab)+f"amix=inputs={len(cues)+2}:normalize=0:duration=first,atrim=0:37.2,afade=t=out:st=36.2:d=1.0[m]")
f.append("[m]acompressor=threshold=-14dB:ratio=2:attack=10:release=150:makeup=1,loudnorm=I=-11:TP=-1.0:LRA=8,alimiter=limit=0.89:level=false,aresample=48000[o]")
subprocess.run(["ffmpeg","-v","error","-y"]+inp+["-filter_complex",";".join(f),"-map","[o]","-c:a","pcm_s16le","hf/frescura/assets/audio/mix.wav"],check=True)
