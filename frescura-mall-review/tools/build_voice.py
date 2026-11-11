# Cut + speed-up voice segments, write voice_raw.wav and segments.json (source->output time map)
import json, subprocess, sys, numpy as np, soundfile as sf
P=sys.argv[1]; SR=48000
SEG=[ # name, src, start, end, tempo
 ("hook1","F7",0.00,3.86,1.12),
 ("hook2","F7",3.98,8.05,1.12),
 ("t1","F6",1.28,10.45,1.06),
 ("t3","F6",10.45,12.45,1.06),
 ("t4","F6",13.50,17.62,1.06),
 ("c1","F7",13.05,18.22,1.12),
 ("c2","F7",18.25,20.02,1.12),
 ("c3","F7",20.02,22.08,1.12),
 ("c4","F7",22.45,25.10,1.12),
]
GAP={"hook2":0.10,"t1":0.35,"t3":0.04,"t4":0.10,"c1":0.40,"c2":0.10,"c3":0.06,"c4":0.12}
out=[]; meta=[]; t=0.0
for name,src,a,b,tp in SEG:
    g=GAP.get(name,0.0); out.append(np.zeros(int(g*SR),np.float32)); t+=g
    tmp=f"{P}/aud/seg_{name}.wav"
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"{P}/aud/{src}_df.wav","-af",f"atrim={a}:{b},asetpts=N/SR/TB,atempo={tp},afade=t=in:d=0.015,areverse,afade=t=in:d=0.03,areverse","-ar","48000","-ac","1",tmp],check=True)
    x,_=sf.read(tmp,dtype="float32"); out.append(x)
    meta.append(dict(name=name,src=src,a=a,b=b,tempo=tp,out0=round(t,3),out1=round(t+len(x)/SR,3))); t+=len(x)/SR
sf.write(f"{P}/aud/voice_raw.wav",np.concatenate(out),SR,subtype="FLOAT")
json.dump(meta,open(f"{P}/segments.json","w"),indent=1); print(json.dumps(meta,indent=0)); print("total",t)
