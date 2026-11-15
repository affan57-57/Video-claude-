# Build keep-intervals that shrink every pause > 0.14s down to 0.07s, then speed-up factor; map words to new timeline.
import json,sys
S=sys.argv[1]; TEMPO=1.06
gaps=[(1.27,1.44),(2.45,2.62),(4.93,5.30),(7.92,8.37),(11.67,11.86),(12.27,12.63),(17.12,17.52),(18.02,18.18),(20.38,20.62),(20.98,21.47),(23.13,23.38),(26.28,26.65),(27.75,28.02),(28.09,28.28),(29.31,29.61),(32.95,33.14)]
END=34.12; keep=[]; t=0.0; HOLD=0.035
for a,b in gaps:
    keep.append((t,a+HOLD)); t=b-HOLD
keep.append((t,END))
def mp(x):
    acc=0
    for a,b in keep:
        if x<=b: return (acc+max(0,x-a))/TEMPO
        acc+=b-a
    return acc/TEMPO
fix={"istri":"isteri","mandihan":"hadiahkan","forming":"foaming","minafatasi":"Midnight Fantasy","menyerit":"dirinya.","Sustuk":"Stok","kuni":"kuning","istime":"istime","kesehangan":"kesayangan","bombshell":"Bombshell","cek":"check","manjakan":"manjakan"}
W=json.load(open(f"{S}/words.json")); out=[]
for x in W:
    w=x["w"].strip()
    k=w.strip(",.!")
    if k in fix: w=w.replace(k,fix[k])
    out.append(dict(w=w,s=round(mp(x["s"]),3),e=round(mp(x["e"]),3)))
# merge split tokens
m=[]
for x in out:
    if m and (x["w"].startswith("-") or x["w"] in("out","kan")): m[-1]["w"]+=("" if x["w"].startswith("-") or x["w"]=="kan" else "")+x["w"]; m[-1]["e"]=x["e"]
    else: m.append(x)
for x in m:
    if x["w"]=="checkout": pass
for i,x in enumerate(m):
    if x["w"]=="dirinya." and m[i-1]["w"]=="dia": m[i-1]["w"]="__drop"
m=[x for x in m if x["w"]!="__drop"]
json.dump(dict(keep=keep,tempo=TEMPO,dur=round(mp(END),3),words=m),open(f"{S}/cut.json","w"),ensure_ascii=False,indent=0)
print("new dur",mp(END)); print(" ".join(f"{x['w']}@{x['s']:.2f}" for x in m))
