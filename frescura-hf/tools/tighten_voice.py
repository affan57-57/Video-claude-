import numpy as np, soundfile as sf, re, sys, subprocess
a,sr=sf.read('df.wav',dtype='float32')
log=subprocess.run(['ffmpeg','-i','df.wav','-af','silencedetect=n=-38dB:d=0.12','-f','null','-'],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',log)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',log)]
END=45.86; keep=0.07; fade=int(0.008*sr)
cuts=[(s+keep/2,e-keep/2) for s,e in zip(st,en) if e<END and e-s>keep+0.02]
segs=[];t=0.0
for s,e in cuts: segs.append((t,s)); t=e
segs.append((t,END))
out=[]
for s,e in segs:
    x=a[int(s*sr):int(e*sr)].copy(); r=np.linspace(0,1,fade); x[:fade]*=r; x[-fade:]*=r[::-1]; out.append(x)
y=np.concatenate(out); sf.write('tight.wav',y,sr,subtype='FLOAT'); print(len(y)/sr, len(cuts))
