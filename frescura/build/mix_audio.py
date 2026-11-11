import subprocess
D=31.5
# (file, trim_start, out_time_ms, gain, max_len)
sfx=[
 ("2908",0.75,0,0.85,2.2),("1491",0.15,50,0.5,1),("3005",0,1480,0.55,.3),
 ("1486",0.25,2050,0.5,1.4),("2357",0,4650,0.6,.5),("2356",0,5100,0.45,.4),
 ("3046",0.6,4950,0.6,3),("1345",0.3,6000,0.4,1.5),("1491",0.15,6950,0.55,1),
 ("1485",0,7750,0.55,.6),("2363",0,9150,0.7,1.4),("2356",0,10550,0.5,.4),
 ("3115",0,12420,1.6,.5),("1485",0,14950,0.4,.6),("2354",0,16600,0.6,.4),("2354",0,16780,0.6,.4),("2354",0,16960,0.6,.4),("2354",0,17140,0.6,.4),("2354",0,17320,0.6,.4),
 ("1345",0.3,17450,0.45,1.5),("1486",0.25,19350,0.55,1.4),
 ("2908",0.75,21550,0.5,2.0),("3005",0,22820,0.6,.3),("3115",0,22800,1.6,.5),("2357",0,23250,0.5,.5),
 ("2356",0,23850,0.6,.4),("3005",0,24250,0.7,.3),("1491",0.15,24600,0.5,1),("2354",0,24900,0.6,.4),
 ("1485",0,26100,0.5,.6),("1345",0.3,27300,0.5,1.5),
 ("3046",0.6,27850,0.7,3.2),("1345",0.3,29000,0.4,1.5),
]
ins=["-i","au/p1.wav","-i","au/p2.wav","-i","au/fb.wav","-i","au/c.wav","-ss","9.75","-i","mk/mus371.mp3"]
fc=["[0]adelay=150:all=1[v0];[1]adelay=2450:all=1[v1];[2]adelay=7050:all=1,volume=0.95[v2];[3]adelay=19750:all=1[v3];"
    "[v0][v1][v2][v3]amix=inputs=4:normalize=0,pan=stereo|c0=c0|c1=c0,apad=whole_dur=%s,asplit=2[vx][vsc];"%D,
    "[4]aformat=channel_layouts=stereo,aresample=48000,atrim=0:%s,volume=0.30,afade=t=in:d=0.3,afade=t=out:st=%s:d=1.6[m0];[m0][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[mus];"%(D,D-1.6)]
lab=[]
for i,(f,ts,t,g,ml) in enumerate(sfx):
    ins+=["-i",f"mk/sfx{f}.mp3"]
    fc.append(f"[{5+i}]aformat=channel_layouts=stereo,aresample=48000,atrim={ts}:{ts+ml},asetpts=PTS-STARTPTS,afade=t=out:st={ml-0.15:.2f}:d=0.15,volume={g},adelay={t}:all=1[s{i}];"); lab.append(f"[s{i}]")
fc.append(f"{''.join(lab)}amix=inputs={len(lab)}:normalize=0[sfx];[sfx]asplit=2[sfxa][sfxb];[vx]volume=1.0[vv];[vv][mus][sfxa]amix=inputs=3:normalize=0,atrim=0:{D},alimiter=limit=0.89:attack=2:release=60:level=false[out]")
subprocess.check_call(["ffmpeg","-v","error","-y",*ins,"-filter_complex","".join(fc),"-map","[out]","-c:a","pcm_s16le","-ar","48000","au/final.wav","-map","[sfxb]","-t",str(D),"au/sfx_only.wav"])
