import sys,json,numpy as np,soundfile as sf
name=sys.argv[1]; d=json.load(open(f'{name}.edl.json'))
a,sr=sf.read(f'{name}.voice.wav',dtype='float32'); F=int(0.006*sr); out=[]
for s,e in d['keep']:
    seg=a[int(round(s*sr)):int(round(e*sr))].copy()
    seg[:F]*=np.linspace(0,1,F); seg[-F:]*=np.linspace(1,0,F); out.append(seg)
y=np.concatenate(out); sf.write(f'{name}.voice_cut.wav',y,sr,subtype='PCM_24'); print(name,len(y)/sr)
