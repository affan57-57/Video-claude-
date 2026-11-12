import subprocess, sys, json
S,P=sys.argv[1],sys.argv[2]
# name, src, media_start, dur, mode, crop-center-x, speed
plan=[("s01_stress","6101_sd",11.0,2.1,"full",.50,1),("s02_sweat","45680_sd",5.0,2.0,"full",.50,1),
("s03_tired","45683_sd",7.0,2.6,"arch",.40,1),("s04_work","49313_sd",2.0,1.6,"arch",.60,1),
("s05_laundry","45121_sd",4.0,1.8,"arch",.50,1),("s06_cook","42909_hd",1.5,0.9,"full",.45,1),
("s07_baby","8575_sd",2.0,1.3,"full",.50,1),("s08_penat","6101_sd",15.0,1.6,"arch",.50,1),
("s09_shower","34517_sd",2.0,2.6,"arch",.40,1),("s10_wash","33096_sd",6.0,2.5,"full",.30,1),
("s11_clothes","29445_sd",3.0,2.5,"arch",.55,1),("s12_mallbg","31086_sd",2.0,4.9,"blur",.50,1),
("s13_pump","pump_sd",2.35,3.3,"full",.50,1),("s14_foam","pump_sd",15.2,1.7,"full",.50,1),
("s16_bath","49306_sd",3.0,2.0,"full",.50,1),("s17_mall","49312_sd",3.0,2.6,"arch",.50,1),
("s18_phone","42136_hd",0.8,1.7,"full",.50,1),("s19_bubble","44834_hd",2.0,4.6,"full",.50,1),
("s20_endbg","14529_sd",3.0,4.2,"blur",.50,1),("s15_lather","pump_sd",25.0,1.6,"full",.5,1)]
G="eq=contrast=1.06:saturation=0.92:gamma=0.98,colorbalance=rs=0.03:gs=0.0:bs=-0.03:rm=0.02:bm=-0.02:rh=0.02:bh=-0.01"
for n,src,ms,d,mode,cx,sp in [x for x in plan if len(sys.argv)<4 or x[0] in sys.argv[3].split(",")]:
    f=f"{S}/src/{src}.mp4"
    W,H=map(int,subprocess.run(["ffprobe","-v","error","-select_streams","v","-show_entries","stream=width,height","-of","csv=p=0",f],capture_output=True,text=True).stdout.strip().split(","))
    sh= "cas=0.5," if src.endswith("_sd") else "cas=0.25,"
    if W<H:   vf=f"scale=1080:1920:flags=lanczos,{sh}{G}"
    elif mode=="arch":  # 4:5 window
        cw=int(H*0.8)//2*2; x=int(max(0,min(W-cw,W*cx-cw/2))); vf=f"crop={cw}:{H}:{x}:0,scale=880:1100:flags=lanczos,{sh}{G}"
    elif mode=="blur":
        cw=int(H*9/16)//2*2; x=int(max(0,min(W-cw,W*cx-cw/2))); vf=f"crop={cw}:{H}:{x}:0,scale=540:960,gblur=sigma=14,scale=1080:1920,eq=brightness=-0.18:saturation=0.7,{G}"
    else:
        cw=int(H*9/16)//2*2; x=int(max(0,min(W-cw,W*cx-cw/2))); vf=f"crop={cw}:{H}:{x}:0,scale=1080:1920:flags=lanczos,{sh}{G}"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(ms),"-t",str(d),"-i",f,"-an","-vf",vf+",fps=30,format=yuv420p","-c:v","libx264","-preset","medium","-crf","18","-g","15","-movflags","+faststart",f"{P}/assets/v/{n}.mp4"],check=True)
    print(n,flush=True)
