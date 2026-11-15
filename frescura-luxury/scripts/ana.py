import sys,subprocess,numpy as np
for f in sys.argv[1:]:
    sr=11025
    x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar",str(sr),"-f","f32le","-"],capture_output=True).stdout,dtype=np.float32)
    w=sr*5; rms=[20*np.log10(np.sqrt(np.mean(x[i:i+w]**2))+1e-9) for i in range(0,len(x)-w,w)]
    hop=256; fr=np.array([np.sum(np.abs(np.fft.rfft(x[i:i+1024]*np.hanning(1024)))) for i in range(0,min(len(x),sr*90)-1024,hop)])
    on=np.maximum(0,np.diff(np.log(fr+1e-6))); on-=on.mean()
    ac=np.correlate(on,on,'full')[len(on)-1:]; fps=sr/hop
    lags=np.arange(int(fps*60/180),int(fps*60/70)); L=lags[np.argmax(ac[lags])]
    print(f, "len %.0fs"%(len(x)/sr), "bpm %.1f"%(60*fps/L)); print(" ".join("%d"%r for r in rms))
