"""Mix studio voice (+0.3s), generated music bed (ducked under voice) and SFX cues into final_audio.wav (38s, ~-11 LUFS)."""
import subprocess
OFF=0.3; DUR=38.0
CUES=[  # (time s, sfx, gain dB)
 (0.0,'impact',-4),(0.0,'sub_drop',-6),(0.05,'shimmer',-14),(1.55,'whoosh',-10),(1.75,'pop',-9),
 (2.62,'whoosh_down',-9),(3.6,'pop',-12),(3.85,'shimmer',-15),(3.8,'whoosh',-14),(5.6,'pop',-10),(5.73,'pop',-10),(5.86,'pop',-10),(5.99,'pop',-10),
 (7.1,'swipe',-10),(7.7,'chime',-12),(8.45,'whoosh',-11),(9.05,'tick',-12),(9.95,'riser',-10),(11.2,'impact',-9),(11.25,'shimmer',-11),
 (12.05,'swipe',-10),(12.45,'click',-6),(12.5,'bubbles',-12),(14.0,'pop',-9),(14.75,'pop',-9),
 (15.1,'whoosh',-11),(15.3,'bubbles',-11),(16.15,'pop',-10),(18.0,'swipe',-12),(18.25,'pop',-10),(18.3,'shimmer',-14),
 (20.05,'whoosh_down',-9),(20.15,'impact',-9),(20.4,'shimmer',-14),(22.45,'pop',-10),(23.35,'pop',-10),
 (24.0,'whoosh',-10),(24.15,'shimmer',-10),(25.8,'pop',-10),(26.5,'pop',-10),
 (27.2,'swipe',-10),*[(27.8+i*0.2,'tick',-13) for i in range(7)],
 (29.4,'whoosh_down',-9),(29.5,'sub_drop',-6),(30.4,'impact',-8),*[(30.0+i*0.25,'tick',-14) for i in range(8)],
 (32.15,'whoosh',-10),(32.3,'pop',-8),(32.85,'click',-6),(32.9,'notify',-9),(33.1,'pop',-10),
 (35.2,'whoosh_down',-10),(35.35,'chime',-8),(35.4,'shimmer',-10),
]
ins=['-i','render/voice_studio.wav','-i','sfx/music_bed.wav']; f=[]
f.append(f"[0]adelay={int(OFF*1000)}:all=1,apad=whole_dur={DUR},pan=stereo|c0=c0|c1=c0,asplit=2[v][vsc]")
f.append(f"[1]atrim=0:{DUR},volume=-15dB,afade=t=in:d=0.2[m0]")
f.append("[m0][vsc]sidechaincompress=threshold=0.04:ratio=5:attack=20:release=300:makeup=1[mduck]")
f.append(f"[mduck]volume='if(gt(t,35.1),2.2,1)':eval=frame,afade=t=out:st={DUR-1.6}:d=1.6[m]")
lab=[]
for k,(t,n,g) in enumerate(CUES):
    ins+=['-i',f'sfx/{n}.wav']; i=k+2
    f.append(f"[{i}]volume={g}dB,adelay={int(t*1000)}:all=1[s{k}]"); lab.append(f"[s{k}]")
f.append(f"[v][m]{''.join(lab)}amix=inputs={len(lab)+2}:normalize=0:duration=first,atrim=0:{DUR},"
         "acompressor=threshold=-14dB:ratio=2:attack=5:release=80,loudnorm=I=-11:TP=-1.0:LRA=7,aresample=48000[out]")
subprocess.run(['ffmpeg','-v','error','-y',*ins,'-filter_complex',';'.join(f),'-map','[out]','-c:a','pcm_s24le','render/final_audio.wav'],check=True)
print('ok')
