import json, re, subprocess, numpy as np, soundfile as sf, sys
src, out, txj, outj = sys.argv[1:5]
a, sr = sf.read(src, dtype='float32')
log = subprocess.run(['ffmpeg','-i',src,'-af','silencedetect=noise=-38dB:d=0.18','-f','null','-'],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',log)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',log)]
KEEP=0.14
cuts=[]  # (start,end) removed in source time
for s,e in zip(st,en):
    if s<0.05: continue
    L=e-s
    if L>0.22:
        m=(s+e)/2; r=L-KEEP; cuts.append((m-r/2,m+r/2))
# merge adjacent silences separated by tiny blip (23.28-23.77)
segs=[]; t=0.0
for c0,c1 in cuts: segs.append((t,c0)); t=c1
segs.append((t,len(a)/sr))
fade=int(0.012*sr); parts=[]
for s0,s1 in segs:
    x=a[int(s0*sr):int(s1*sr)].copy(); w=np.linspace(0,1,fade)
    x[:fade]*=w; x[-fade:]*=w[::-1]; parts.append(x)
y=np.concatenate(parts); sf.write(out,y,sr,subtype='FLOAT')
def remap(t):
    acc=0
    for s0,s1 in segs:
        if t<s0: return acc
        if t<=s1: return acc+(t-s0)
        acc+=s1-s0
    return acc
tx=json.load(open(txj)); words=[]
for seg in tx:
    for w in seg['words']: words.append(dict(text=w['w'].strip(),start=round(remap(w['s']),3),end=round(remap(w['e']),3),src=w['s']))
json.dump(dict(segments=segs,cuts=cuts,words=words,duration=len(y)/sr),open(outj,'w'),ensure_ascii=False,indent=1)
print('cuts',[(round(a,2),round(b,2)) for a,b in cuts]); print('dur',len(a)/sr,'->',len(y)/sr)
