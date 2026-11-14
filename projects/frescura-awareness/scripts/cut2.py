import numpy as np,soundfile as sf,json
a,sr=sf.read('main_df.wav')
sil=[(0.918,1.075),(8.026,8.236),(11.995,12.448),(16.73,16.88),(23.833,23.987),(24.542,24.733),(25.544,25.734),(29.128,29.346),(34.855,35.187),(37.59,37.78)]
keep=[];s=0.27
for a0,b0 in sil:
    keep.append((s,a0+0.03)); s=b0-0.03
keep.append((s,41.62))
out=[];f=int(0.012*sr);r=np.linspace(0,1,f);m=[];t=0
for i,(x,y) in enumerate(keep):
    seg=a[int(x*sr):int(y*sr)].copy();seg[:f]*=r;seg[-f:]*=r[::-1];out.append(seg);m.append([x,y,t]);t+=len(seg)/sr
    if i<len(keep)-1: out.append(np.zeros(int(0.03*sr)));t+=0.03
y=np.concatenate(out);sf.write('voice_cut.wav',y,sr,subtype='FLOAT');json.dump(m,open('cutmap.json','w'));print(len(y)/sr)
