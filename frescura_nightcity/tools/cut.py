# Usage: cut.py name dur  -> reads name.df.wav silences, name.json words, writes name.edl.json
import sys, json, re, subprocess
name, dur = sys.argv[1], float(sys.argv[2]); extra = json.loads(sys.argv[3]) if len(sys.argv)>3 else []
FPS=30; snap=lambda t: round(t*FPS)/FPS
out = subprocess.run(['ffmpeg','-hide_banner','-i',f'{name}.df.wav','-af','silencedetect=n=-42dB:d=0.15','-f','null','-'],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',out)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',out)]
sil=list(zip(st,en))
m=[]  # merge near silences
for s,e in sil:
    if m and s-m[-1][1]<0.06: m[-1]=(m[-1][0],e)
    else: m.append((s,e))
cuts=[]
for s,e in m:
    if e-s<0.20: continue
    a = s+0.06 if s>0.01 else 0.0; b = e-0.05 if e<dur-0.01 else dur
    if b-a>0.05: cuts.append((a,b))
cuts += [tuple(x) for x in extra]; cuts.sort()
keep=[]; t=0.0
for a,b in cuts:
    if a>t: keep.append((t,a))
    t=max(t,b)
if t<dur: keep.append((t,dur))
keep=[(snap(a),snap(b)) for a,b in keep if snap(b)-snap(a)>=2/FPS]
# remap words
words=[w for s in json.load(open(f'{name}.json')) for w in s['w']]
def remap(t):
    acc=0
    for a,b in keep:
        if t<a: return acc
        if t<=b: return acc+(t-a)
        acc+=b-a
    return acc
W=[]
for w in words:
    s0,e0=remap(w[0]),remap(w[1])
    ws=w[0]
    if not any(a-0.05<=ws<=b for a,b in keep):
        nxt=[a for a,b in keep if a>ws and a<w[1]]
        if nxt: s0=remap(nxt[0]); ws=nxt[0]
    inside=any(a-0.05<=ws<=b for a,b in keep)
    if inside and e0>s0: W.append({'text':w[2].strip(),'start':round(s0,3),'end':round(e0,3),'src':w[0]})
total=sum(b-a for a,b in keep)
json.dump({'keep':keep,'words':W,'duration':round(total,3)},open(f'{name}.edl.json','w'),ensure_ascii=False,indent=0)
print(name,'segments',len(keep),'out dur',round(total,2),'removed',round(dur-total,2))
print(' '.join(f"{w['text']}@{w['start']:.2f}" for w in W))
