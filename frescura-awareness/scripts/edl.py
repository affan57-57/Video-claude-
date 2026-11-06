# Build tightened voice track: keep ranges, cap pauses, crossfade joins. Writes voice_cut.wav + edl.json
import numpy as np, soundfile as sf, subprocess, re, json, sys
SR=48000; CAP=float(sys.argv[1]) if len(sys.argv)>1 else 0.10
def sil(f):
    o=subprocess.run(["ffmpeg","-hide_banner","-i",f,"-af","silencedetect=n=-40dB:d=0.07","-f","null","-"],capture_output=True,text=True).stderr
    s=[float(x) for x in re.findall(r"silence_start: ([0-9.]+)",o)]; e=[float(x) for x in re.findall(r"silence_end: ([0-9.]+)",o)]
    return list(zip(s,e))
plan=[("part1",[(0.0,17.60)]),("part2",[(0.52,35.93),(37.34,38.86)])]
pieces=[]; edl=[]
for p,keeps in plan:
    a,_=sf.read(f"{p}.df.wav",dtype="float32"); S_=sil(f"{p}.df.wav")
    for k0,k1 in keeps:
        # split keep range at long silences
        cuts=[(max(s,k0),min(e,k1)) for s,e in S_ if e>k0 and s<k1 and min(e,k1)-max(s,k0)>CAP]
        t=k0
        for s,e in cuts:
            h=CAP/2; seg=(t, s+h); 
            if seg[1]>seg[0]: edl.append((p,)+seg)
            t=e-h
        if k1>t: edl.append((p,t,k1))
out=[]; X=int(0.012*SR); mp=[]; pos=0.0
for p,s,e in edl:
    a,_=sf.read(f"{p}.df.wav",dtype="float32"); seg=a[int(s*SR):int(e*SR)].copy()
    if out:
        prev=out[-1]; f=np.linspace(0,1,X); seg[:X]=seg[:X]*f+prev[-X:]*(1-f); out[-1]=prev[:-X]; pos-=X/SR
    mp.append(dict(src=p,s=s,e=e,out=pos)); out.append(seg); pos+=len(seg)/SR
y=np.concatenate(out); sf.write("voice_cut.wav",y,SR,subtype="FLOAT")
json.dump(mp,open("edl.json","w"),indent=0); print("segments",len(mp),"dur",len(y)/SR)
