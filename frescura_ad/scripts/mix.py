import sys,subprocess
X=sys.argv[1]; W=sys.argv[2]; OUT=sys.argv[3]
# (sfx, time_s, gain_dB)
cues=[("impact",0.0,-2),("riser",-0.0,-99),("tick",0.12,-6),("tick",0.5,-6),("glass",0.96,-6),("whoosh",1.7,-5),("shimmer",2.45,-7),
("whoosh",3.2,-4),("impact",5.4,-5),("shimmer",6.6,-6),("glass",7.16,-7),
("swoosh_down",7.6,-5),("pop",8.66,-4),("pop",10.18,-4),("bubbles",10.2,-14),("pop",11.24,-4),
("whoosh",13.2,-5),("tick",15.06,-7),("heartbeat",17.6,-3),("swoosh_down",18.45,-5),
("impact",19.1,-2),("riser",19.45,-6),("impact",21.02,-2),("shimmer",21.1,-5),
("shutter",22.12,-5),("pump",22.9,-3),("bubbles",23.3,-9),("pop",23.7,-8),("pop",23.84,-8),("pop",23.98,-8),
("whoosh",24.9,-4),("glass",26.84,-5),("glass",27.44,-7),
("whoosh",28.2,-5),("shimmer",28.4,-7)]+[("tick",29.9+0.11*i,-7) for i in range(7)]+[
("impact",30.95,-3),("pop",31.0,-3),("pop",31.55,-4),("cha_ching",32.02,-3),("tick",33.3,-8),("tick",33.66,-8),("impact",34.0,-2),
("shimmer",35.1,-4),("glass",35.15,-6)]
cues=[c for c in cues if c[2]>-90]
args=["ffmpeg","-v","error","-y","-i",f"{W}/voice_final.wav","-i",f"{W}/music.wav"]
fc=["[0]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay=0:all=1,apad=pad_dur=2,asplit=2[v][vsc]",
    "[1]volume=-11dB[m0]","[m0][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[m]"]
lab=[]
for i,(n,t,g) in enumerate(cues):
    args+=["-i",f"{X}/{n}.wav"]; fc.append(f"[{i+2}]volume={g}dB,adelay={int(t*1000)}:all=1[s{i}]"); lab.append(f"[s{i}]")
fc.append(f"[v][m]{''.join(lab)}amix=inputs={len(lab)+2}:normalize=0:duration=first,atrim=0:36.6,afade=t=out:st=35.9:d=0.7,alimiter=limit=0.79:attack=3:release=60:level=false,volume=-1.3dB[o]")
args+=["-filter_complex",";".join(fc),"-map","[o]","-c:a","pcm_s24le",OUT]
subprocess.run(args,check=True)
