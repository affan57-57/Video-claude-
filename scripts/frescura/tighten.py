import sys, numpy as np, soundfile as sf
x,sr=sf.read(sys.argv[1],dtype='float32'); keep_gap=float(sys.argv[3]) if len(sys.argv)>3 else 0.10
hop=int(0.01*sr); n=len(x)//hop
rms=np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2)+1e-12) for i in range(n)]); db=20*np.log10(rms)
thr=db.max()-33; sil=db<thr
# find silent runs >= 0.14s
runs=[]; i=0
while i<n:
    if sil[i]:
        j=i
        while j<n and sil[j]: j+=1
        if (j-i)*0.01>=0.12: runs.append((i,j))
        i=j
    else: i+=1
cuts=[]
for a,b in runs:
    a_s,b_s=a*0.01,b*0.01
    if a==0: cuts.append((0,max(0,b_s-0.05))); continue
    if b>=n: cuts.append((a_s+0.08,len(x)/sr)); continue
    L=b_s-a_s
    if L>keep_gap: m=(a_s+b_s)/2; cuts.append((m-(L-keep_gap)/2, m+(L-keep_gap)/2))
print("cuts:",[(round(a,2),round(b,2)) for a,b in cuts], "removed", round(sum(b-a for a,b in cuts),2))
segs=[]; pos=0; fade=int(0.008*sr)
for a,b in cuts:
    segs.append(x[int(pos*sr):int(a*sr)]); pos=b
segs.append(x[int(pos*sr):])
out=segs[0]
for s in segs[1:]:
    if len(s)<2*fade: continue
    w=np.linspace(0,1,fade); ov=out[-fade:]*(1-w)+s[:fade]*w
    out=np.concatenate([out[:-fade],ov,s[fade:]])
sf.write(sys.argv[2],out,sr,subtype='FLOAT'); print("dur",len(x)/sr,"->",len(out)/sr)
