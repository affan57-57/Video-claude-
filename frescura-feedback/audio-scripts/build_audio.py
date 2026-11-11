import numpy as np, soundfile as sf, subprocess, json, sys
sys.path.insert(0,'.')
SR=48000
def seg(src,a,b,tempo,name):
    out=f"au/s_{name}.wav"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-to",str(b),"-i",src,"-af",f"afade=t=in:d=0.012,areverse,afade=t=in:d=0.02,areverse,atempo={tempo}","-ar","48000","-ac","1",out],check=True)
    return sf.read(out)[0]
VT,FT=1.12,1.06
VO=[("A1",0.00,2.16),("A2",2.55,3.60),("A3",3.85,6.22)]
FB=[("F1",3.48,6.15),("F2",8.52,12.40),("F3",13.10,15.25),("F4",15.85,18.92)]
CL=[("C1",8.31,10.92),("C2",11.03,13.80),("C3",14.35,15.22),("C4",15.35,16.38),("C5",16.93,18.98)]
T={}; t=0.35; tr=np.zeros(SR*40)
def place(name,x,t):
    i=int(t*SR); tr[i:i+len(x)]+=x; T[name]=[round(t,3),round(t+len(x)/SR,3)]; return t+len(x)/SR
for n,a,b in VO: t=place(n,seg("au/vo_st.wav",a,b,VT,n),t)+0.10
t=t-0.10+0.15; T["fb_start"]=round(t,3)
for n,a,b in FB: t=place(n,seg("au/fb_st.wav",a,b,FT,n),t)
T["fb_end"]=round(t,3); T["edu_start"]=round(t+0.05,3); t=t+3.6; T["edu_end"]=round(t-0.05,3)
gaps={"C1":0.10,"C2":0.14,"C3":0.10,"C4":0.14,"C5":0}
for n,a,b in CL: t=place(n,seg("au/vo_st.wav",a,b,VT,n),t)+gaps[n]
T["end_start"]=round(t+0.15,3); T["total"]=round(t+2.6,2)
tr=tr[:int(T["total"]*SR)]
sf.write("au/voice_track.wav",tr.astype(np.float32),SR)
json.dump(dict(T=T,FB=FB,FT=FT),open("timeline.json","w"),indent=1); print(json.dumps(T))
