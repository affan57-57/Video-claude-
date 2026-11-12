import json, numpy as np, soundfile as sf, subprocess, sys
S=sys.argv[1]; TEMPO=1.13; KEEP=0.07; XF=0.012
a,sr=sf.read(f"{S}/audio/voice_full.wav",dtype="float32")
sil=[(14.2913,14.4735),(15.6627,15.8525),(25.8446,26.1586),(30.7674,31.1015),(36.5408,36.7768),(37.8177,38.0854),(39.4376,39.6791),(42.0942,42.3059),(43.5033,43.9166)]
cuts=[(s+KEEP/2,e-KEEP/2) for s,e in sil]  # remove the middle of each pause
head=0.03; tail=45.70
segs=[]; t=head
for s,e in cuts: segs.append((t,s)); t=e
segs.append((t,tail))
out=[]; fade=int(XF*sr)
for s,e in segs:
    x=a[int(s*sr):int(e*sr)].copy(); r=np.linspace(0,1,fade); x[:fade]*=r; x[-fade:]*=r[::-1]; out.append(x)
y=np.concatenate(out); sf.write(f"{S}/audio/voice_cut.wav",y,sr,subtype="FLOAT")
def remap(t):
    acc=0
    for s,e in segs:
        if t<s: return acc/TEMPO
        if t<=e: return (acc+t-s)/TEMPO
        acc+=e-s
    return acc/TEMPO
fix={"perasan":"perasan","tak,":"tak,","fresh":"Frescura","kura":None,"body":"Body","Niak":"Nikmati","mati":None,"femenin.":"feminin.",
     "minat":"Midnight","fantasi,":"Fantasy,","peminat":"Midnight","bayi":None,"kuning":None,"cek":"check","out":"out","terhat.":"terhad.","stres,":"stres,","urus":"urus","sama":"sambung"}
w=json.load(open(f"{S}/transcript.json")); w=w["words"] if isinstance(w,dict) else w
res=[]
for x in w:
    t=x["text"]; nt=fix.get(t,t)
    if nt is None:
        if res: res[-1]["end"]=round(remap(x["end"]),3)
        continue
    if t=="fantasi," and x["start"]>40: nt="Fantasy,"
    res.append(dict(text=nt,start=round(remap(x["start"]),3),end=round(remap(x["end"]),3)))
json.dump(res,open(f"{S}/words.json","w"),ensure_ascii=False,indent=0)
subprocess.run(["ffmpeg","-v","error","-y","-i",f"{S}/audio/voice_cut.wav","-af",f"atempo={TEMPO},alimiter=limit=0.89:attack=3:release=60:level=false,loudnorm=I=-12:TP=-1:LRA=5,aresample=48000","-c:a","pcm_s24le",f"{S}/audio/voice_final.wav"],check=True)
print(len(y)/sr/TEMPO); print(" ".join(f"[{r['start']:.2f}]{r['text']}" for r in res))
