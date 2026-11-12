import json,subprocess,sys
S=sys.argv[1]; TOTAL=float(sys.argv[2]); A=json.load(open(f"{S}/anchors.json"))
W={w["w"]:w["s"] for w in json.load(open(f"{S}/words.json"))[::-1]}
X=f"{S}/sfxsrc/sfx_"
ev=[(0.0,1143,-4),(1.39,2364,-8),(2.04,2902,-3),(A["bila"],166,-10),(A["tiba"]-.1,1492,-7),(A["tiba"]+.3,3005,-10),
(A["menjauh"],1489,-8),(A["bau"],498,-3),(A["jangan"]-.1,1490,-7),(A["teru"],2867,-11),(A["peluh"]-.15,2925,-10),
(A["past"]-.05,1492,-8),(12.13,3005,-7),(12.4,2568,-6),(A["bers"],3005,-7),(A["bers"]+.27,2568,-6),(A["guna"],3005,-7),(A["guna"]+.27,2568,-6),
(A["semes"]-.1,1490,-8),(A["semes"]+.2,2925,-9),(A["rutin"]+.5,166,-10),(A["menarik"]-.55,1489,-10),
(A["pastinya"],2936,-5),(A["fb"]-.05,2900,-3),(A["fb"],871,-6),(A["dengan"]-.3,1492,-9),(A["buih"],2925,-5),
(A["garam"]-.05,1198,-8),(A["wangi"]-.05,2350,-8),(A["jangan2"],2902,-6),(A["tindakan"],498,-6),
(A["tekan"]-.1,1490,-8),(A["kuning"],2568,-2),(A["kuning"]+.02,3005,-6),(A["masuk"]+.05,166,-8),(A["masuk"]+.66,2364,-6),
(A["teruta"]-.05,1492,-8),(A["bomb"]-.05,871,-6),(A["mid"]-.1,2350,-8),(A["check"],1993,-6),(A["terhad"]-.15,2902,-4),
(A["end"],2900,-5),(A["end"]+.1,871,-6)]
inp=["-i",f"{S}/voice_studio.wav","-ss","8.72","-t",str(TOTAL+0.5),"-i",f"{S}/sfxsrc/mus_371.mp3"]
fc=["[0]aresample=48000,pan=stereo|c0=c0|c1=c0,apad=whole_dur=%.2f,asplit=2[v][sc]"%TOTAL,
    "[1]aresample=48000,volume=-15dB,afade=t=in:d=0.3,afade=t=out:st=%.2f:d=1.6[m0]"%(TOTAL-1.6),
    "[m0][sc]sidechaincompress=threshold=0.04:ratio=5:attack=15:release=280:makeup=1[m]"]
labs=["[v]","[m]"]
for i,(t,f,g) in enumerate(ev):
    inp+=["-i",f"{X}{f}.mp3"]; k=i+2
    fc.append(f"[{k}]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,adelay={int(max(t,0)*1000)}:all=1[s{i}]"); labs.append(f"[s{i}]")
fc.append(f"{''.join(labs)}amix=inputs={len(labs)}:normalize=0:duration=first,atrim=0:{TOTAL},loudnorm=I=-11:TP=-1.2:LRA=8,alimiter=limit=0.89:level=false[o]")
cmd=["ffmpeg","-v","error","-y",*inp,"-filter_complex",";".join(fc),"-map","[o]","-ar","48000","-c:a","pcm_s16le",f"{S}/hf/frescura/assets/audio/mix.wav"]
subprocess.run(cmd,check=True); print("events",len(ev))
