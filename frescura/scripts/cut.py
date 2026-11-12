import json,re,subprocess,numpy as np,soundfile as sf
SPEED=1.17
a,sr=sf.read("df_full.wav",dtype="float32")
# silences from silencedetect on df audio
out=subprocess.run(["ffmpeg","-hide_banner","-i","df_full.wav","-af","silencedetect=n=-45dB:d=0.12","-f","null","-"],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",out)]; en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",out)]
cuts=[]
for s,e in zip(st,en):
    keep=0.035
    if e-s>2*keep+0.03: cuts.append((s+keep,e-keep))
# keep segments
segs=[];t=0.0
for s,e in cuts: segs.append((t,s)); t=e
segs.append((t,len(a)/sr))
fade=int(0.008*sr); parts=[]
for s,e in segs:
    x=a[int(s*sr):int(e*sr)].copy(); r=np.linspace(0,1,fade)
    x[:fade]*=r; x[-fade:]*=r[::-1]; parts.append(x)
y=np.concatenate(parts); sf.write("voice_cut.wav",y,sr,subtype="FLOAT")
def mp(t):
    acc=0.0
    for s,e in segs:
        if t<s: return acc/SPEED
        if t<=e: return (acc+t-s)/SPEED
        acc+=e-s
    return acc/SPEED
fix={"di":"deodoran","dorong":"","fresh":"Frescura","kura":"","femeni":"feminin","kuni":"kuning","minat":"Midnight","fantasi,":"Fantasy,","cek":"check","stock":"stok","bombshell":"Bombshell","dalam":"dalam troli,"}
d=json.load(open("main_tr.json")); W=[]
for s in d:
    for w in s["words"]:
        k=w["w"].strip(); t=fix.get(k,k)
        if t=="" : W[-1]["e"]=round(mp(w["e"]),3); continue
        W.append(dict(w=t,s=round(mp(w["s"]),3),e=round(mp(w["e"]),3)))
for w in W:
    if w["w"]=="Frescura": w["w"]="Frescura Body"
W=[w for i,w in enumerate(W) if not (w["w"]=="body")]
json.dump(W,open("words.json","w"),ensure_ascii=False,indent=0)
print("cut len",len(y)/sr,"-> sped",len(y)/sr/SPEED, "removed",sum(e-s for s,e in cuts))
print(" ".join(f"{w['w']}@{w['s']:.2f}" for w in W))
