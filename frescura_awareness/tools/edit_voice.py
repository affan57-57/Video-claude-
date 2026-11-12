# Cut redundant line + shrink pauses; write edited voice and orig->edit time map
import soundfile as sf, numpy as np, json, sys
a,sr=sf.read(sys.argv[1]); a=a if a.ndim==1 else a.mean(1)
h=int(0.01*sr)
e=np.array([20*np.log10(np.sqrt(np.mean(a[i:i+h]**2))+1e-9) for i in range(0,len(a)-h,h)])
th=np.percentile(e,95)-30
cuts=[(0.0,0.10),(21.82,24.00),(42.45,len(a)/sr)]   # lead-in, repeated "Jangan lupa menjaga diri sendiri", tail
low=e<th; i=0
while i<len(low):
    if low[i]:
        j=i
        while j<len(low) and low[j]: j+=1
        if j-i>=12: cuts.append(((i+4)/100,(j-4)/100))  # keep 40ms each side
        i=j
    else: i+=1
cuts=sorted(cuts); merged=[]
for c in cuts:
    if merged and c[0]<=merged[-1][1]: merged[-1]=(merged[-1][0],max(merged[-1][1],c[1]))
    else: merged.append(c)
keep=[]; t=0
for s,e_ in merged:
    if s>t: keep.append((t,s))
    t=e_
if t<len(a)/sr: keep.append((t,len(a)/sr))
xf=int(0.012*sr); out=np.zeros(0)
for s,e_ in keep:
    seg=a[int(s*sr):int(e_*sr)].copy()
    if len(out)>xf:
        r=np.linspace(0,1,xf); out[-xf:]=out[-xf:]*(1-r)+seg[:xf]*r; seg=seg[xf:]
    out=np.concatenate([out,seg])
sf.write(sys.argv[2],out.astype(np.float32),sr,subtype='FLOAT')
json.dump(dict(keep=keep,xf=0.012),open(sys.argv[3],'w'))
print('cuts',[(round(x,2),round(y,2)) for x,y in merged]); print('len',len(out)/sr)
