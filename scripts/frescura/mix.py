import subprocess, sys
S=sys.argv[1]; X=f'{S}/sfx'; OUT=sys.argv[2]
VO=0.2; DUR=33.9; MOFF=29.45-(14.82+VO)
# (time, sfx id, gain dB)
CUES=[
 (0.00,'788',-6),(0.00,'1492',-8),(0.80,'3005',-4),(1.40,'2357',-6),
 (1.93,'1490',-9),(3.60,'2357',-8),(4.95,'2354',-9),
 (5.48,'3115',-7),(5.75,'2568',-4),(7.05,'2568',-4),(7.85,'2568',-4),(9.05,'2568',-4),(9.30,'3124',-8),
 (9.94,'166',-6),(10.05,'1317',-8),(10.75,'951',-10),
 (12.58,'1489',-12),(13.05,'3124',-7),(13.65,'3124',-7),(14.30,'3124',-7),
 (12.45,'790',-9),(15.02,'2900',-5),(15.02,'2633',-9),
 (16.36,'3115',-7),(16.70,'2925',-6),(17.40,'3000',-6),(18.0,'2925',-9),
 (18.48,'166',-7),(18.62,'1317',-6),(19.96,'2350',-9),
 (21.28,'1492',-9),(21.36,'871',-8),(22.86,'3115',-8),(23.05,'2925',-7),(23.7,'3000',-8),
 (24.56,'1490',-9),(26.05,'2568',-2),(26.10,'2357',-4),(27.00,'2870',-9),
 (28.14,'3115',-7),(28.95,'3124',-6),(29.70,'3124',-6),(30.45,'2354',-8),
 (31.42,'1143',-8),(31.45,'2633',-8),(33.0,'1133',-12),
]
inp=['-i',f'{S}/work/voice.wav','-ss',str(MOFF),'-t',str(DUR+1),'-i',f'{S}/music/371.mp3']
fc=[f"[0]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay={int(VO*1000)}:all=1,apad,atrim=0:{DUR},asplit=2[vo][sc]",
    f"[1]aresample=48000,volume=-7dB,afade=t=in:st=0:d=0.05,afade=t=out:st={DUR-1.3}:d=1.3,atrim=0:{DUR}[m0]",
    "[m0][sc]sidechaincompress=threshold=0.04:ratio=5:attack=15:release=260:makeup=1[mus]"]
labels=['[vo]','[mus]']
for k,(t,i,g) in enumerate(CUES):
    inp+=['-i',f'{X}/{i}.mp3']; n=k+2
    fc.append(f"[{n}]aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,adelay={int(t*1000)}:all=1[s{k}]"); labels.append(f'[s{k}]')
fc.append(''.join(labels)+f"amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{DUR},loudnorm=I=-11:TP=-1.2:LRA=8,alimiter=limit=0.89:attack=1:release=40:level=false,aresample=48000[out]")
subprocess.run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fc),'-map','[out]','-c:a','pcm_s16le',OUT],check=True)
print('ok')
