import subprocess,sys
O=0.25; END=39.4
cues=[(0.02,'impact',-8),(0.0,'whoosh_l',-14),
(1.97,'pop',-13),(2.87,'pop',-13),(3.83,'pop',-13),(4.10,'ding2',-22),
(4.40,'whoosh',-13),(6.15,'boom',-10),(7.30,'whoosh_s',-15),(7.45,'ding',-19),(8.55,'tick',-14),
(9.55,'whoosh',-13),(12.40,'whoosh_s',-16),(12.89,'pop',-12),(13.65,'pop',-12),(14.43,'pop',-12),(16.30,'ding2',-21),
(16.88,'whoosh',-13),(18.05,'riser',-16),(19.25,'sparkle',-14),(19.25,'shimmer',-20),
(19.92,'impact',-9),(19.95,'shimmer',-18),
(21.08,'whoosh_s',-14),(21.2,'bubbles',-12),(22.30,'pop',-13),
(23.08,'whoosh_s',-14),(23.2,'bubbles',-13),(24.0,'ding2',-19),
(24.85,'whoosh',-13),(25.0,'shimmer',-19),
(26.86,'whoosh_s',-14),(26.93,'boom',-9),(27.69,'boom',-10),
(29.05,'whoosh_l',-13),(29.11,'impact',-9),(30.55,'tick',-14),
(32.08,'whoosh',-13),(32.20,'tick',-10),(32.22,'pop',-12),(33.15,'chaching',-13),(34.30,'sparkle',-17),
(35.40,'tick',-14),(35.70,'tick',-14),(36.00,'tick',-14),(36.85,'ding',-18),
(37.08,'whoosh_l',-13),(37.15,'boom',-9),(37.2,'shimmer',-16),(37.4,'sparkle',-14)]
args=['ffmpeg','-v','error','-y','-i','aud/voice.wav','-i','sfx/music.wav']
for t,n,g in cues: args+=['-i',f'sfx/{n}.wav']
f=[f"[0]pan=stereo|c0=c0|c1=c0,adelay={int(O*1000)}:all=1,apad,atrim=0:{END}[vo]",
   "[vo]asplit=2[v1][vsc]",
   f"[1]atrim=0:{END},volume=-17dB,afade=t=in:st=0:d=0.3,afade=t=out:st={END-1.6}:d=1.6[mu]",
   "[mu][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350:makeup=1[mud]"]
labs=[]
for i,(t,n,g) in enumerate(cues):
    f.append(f"[{i+2}]volume={g}dB,adelay={int(t*1000)}:all=1[s{i}]"); labs.append(f"[s{i}]")
f.append(f"[v1][mud]{''.join(labs)}amix=inputs={len(labs)+2}:normalize=0:duration=first,atrim=0:{END},loudnorm=I=-12:TP=-1.0:LRA=8,aresample=48000,alimiter=limit=0.89:level=false[out]")
args+=['-filter_complex',';'.join(f),'-map','[out]','-c:a','pcm_s16le','final_mix.wav']
subprocess.run(args,check=True)
