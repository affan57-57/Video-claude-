# Tighten voice: keep ranges, cap pauses inside them, small breath gap at joins. -> voice_cut.wav, edl.json
import numpy as np, soundfile as sf, subprocess, re, json, sys
SR=48000; SRC=sys.argv[1]; KEEPS=json.loads(sys.argv[2]); CAP=float(sys.argv[3]) if len(sys.argv)>3 else 0.08; GAP=0.07
import os
THR=os.environ.get("SIL_DB","-40")
o=subprocess.run(["ffmpeg","-hide_banner","-i",SRC,"-af",f"silencedetect=n={THR}dB:d=0.07","-f","null","-"],capture_output=True,text=True).stderr
SIL=list(zip([float(x) for x in re.findall(r"silence_start: ([0-9.]+)",o)],[float(x) for x in re.findall(r"silence_end: ([0-9.]+)",o)]))
a,_=sf.read(SRC,dtype="float32"); X=int(0.012*SR)
out=[]; mp=[]; pos=0.0
def add(seg,s,e,xf):
    global pos
    seg=seg.copy()
    if out and xf:
        f=np.linspace(0,1,X); seg[:X]=seg[:X]*f+out[-1][-X:]*(1-f); out[-1]=out[-1][:-X]; pos-=X/SR
    mp.append(dict(s=s,e=e,out=pos)); out.append(seg); pos+=len(seg)/SR
for k0,k1 in KEEPS:
    if out:
        f=np.linspace(1,0,X); out[-1][-X:]*=f
        out.append(np.zeros(int(GAP*SR),dtype="float32")); pos+=GAP
    cuts=[(max(s,k0),min(e,k1)) for s,e in SIL if e>k0 and s<k1 and min(e,k1)-max(s,k0)>CAP]
    t=k0; first=True
    for s,e in cuts:
        h=CAP/2
        if s+h>t: add(a[int(t*SR):int((s+h)*SR)],t,s+h,not first)
        first=False; t=e-h
    seg=a[int(t*SR):int(k1*SR)]
    if first: seg=seg.copy(); seg[:X]*=np.linspace(0,1,X)
    add(seg,t,k1,not first)
y=np.concatenate(out); sf.write("voice_cut.wav",y,SR,subtype="FLOAT")
json.dump(mp,open("edl.json","w"),indent=0); print("segments",len(mp),"dur",round(len(y)/SR,2))
