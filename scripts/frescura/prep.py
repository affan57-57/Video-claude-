import subprocess, sys, os
S=sys.argv[1]; V=f'{S}/stock/v'; P=f'{S}/in/pump.mov'; O=f'{S}/hf/frescura/assets/video'; os.makedirs(O,exist_ok=True)
G={ # colour grades
 'warm':  "eq=contrast=1.08:saturation=0.9:gamma=0.97,colorbalance=rs=.06:gs=.01:bs=-.06:rm=.04:bm=-.04,curves=preset=medium_contrast",
 'mute':  "eq=contrast=1.05:saturation=0.75:brightness=-0.02,colorbalance=rs=.03:bs=-.02:rh=.03:bh=-.03",
 'gold':  "eq=contrast=1.06:saturation=0.85,colorbalance=rs=.05:gs=.02:bs=-.07:rh=.04:bh=-.05",
 'clean': "eq=contrast=1.04:saturation=0.9:brightness=0.02,colorbalance=rs=.02:bs=-.01",
 'silver':"eq=contrast=1.1:saturation=0.35:brightness=-0.03,colorbalance=bs=.05:bm=.03",
 'rose':  "eq=contrast=1.08:saturation=1.05:gamma=0.95,colorbalance=rs=.02:bs=-.02",
 'night': "eq=contrast=1.15:saturation=1.1:brightness=-0.12:gamma=0.85,colorbalance=rs=.04:gs=-.08:bs=.14:rm=-.02:bm=.10:rh=.0:bh=.08",
 'pump':  "eq=contrast=1.06:saturation=1.08:brightness=0.01,colorbalance=rs=.02:gs=-.03:bs=-.01,unsharp=5:5:0.4",
 'phone': "eq=contrast=1.05:saturation=0.85,colorbalance=rs=.03:bs=-.03",
}
# name, src, ss, out_dur, speed, cropx (0..1 centre for landscape->9:16), grade
C=[
 ('hook',   f'{V}/44429.mp4', 3.0, 2.3, 1.0, .56,'warm'),
 ('couple', f'{V}/42971.mp4', 1.0, 3.9, 1.0, None,'mute'),
 ('city',   f'{V}/49856.mp4', 2.0, 1.8, 1.4, 'p','gold'),
 ('heat',   f'{V}/40150.mp4', 1.0, 3.4, 1.0, .40,'warm'),
 ('shower1',f'{V}/42914.mp4', 2.0, 2.9, 1.0, .46,'clean'),
 ('shower2',f'{V}/42916.mp4', 1.5, 2.7, 1.0, .52,'clean'),
 ('pumpc',  P, 10.15, 2.4, 1.55, 'p','pump'),
 ('ripple', f'{V}/106.mp4', 0.3, 1.8, 1.0, .5,'silver'),
 ('petals', f'{V}/3237.mp4', 2.0, 1.7, 1.0, .5,'rose'),
 ('violet', f'{V}/1869.mp4', 2.0, 2.0, 1.0, .38,'night'),
 ('lather', P, 24.3, 2.0, 1.5, 'p','pump'),
 ('foamhand',P, 14.6, 2.0, 1.2, 'p','pump'),
 ('phone',  f'{V}/42136.mp4', 0.5, 3.8, 1.0, 'p','phone'),
 ('pumpwide',P, 2.4, 2.0, 1.3, 'p','pump'),
]
for n,src,ss,dur,sp,cx,gr in C:
    if cx=='p': geo="scale=1080:1920:flags=lanczos"
    elif cx is None: geo="crop=ih*1.2:ih,scale=1080:900:flags=lanczos"   # landscape-ish card 6:5
    else: geo=f"crop=ih*9/16:ih:(iw-ih*9/16)*{cx}:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6"
    vf=f"setpts=PTS/{sp},fps=30,{geo},{G[gr]},format=yuv420p"
    cmd=['ffmpeg','-v','error','-y','-ss',str(ss),'-t',str(dur*sp+0.2),'-i',src,'-vf',vf,'-t',str(dur),'-an','-c:v','libx264','-preset','medium','-crf','17','-g','15','-movflags','+faststart',f'{O}/{n}.mp4']
    subprocess.run(cmd,check=True); print(n)
