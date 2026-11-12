import sys, numpy as np, soundfile as sf, noisereduce as nr
a, sr = sf.read(sys.argv[1], dtype="float32")
if a.ndim > 1: a = a.mean(1)
# noise profile from the quietest 10% of 50 ms frames
f = int(sr*0.05); fr = a[:len(a)//f*f].reshape(-1, f); rms = np.sqrt((fr**2).mean(1))
noise = fr[rms <= np.quantile(rms, 0.10)].ravel()
y = nr.reduce_noise(y=a, sr=sr, y_noise=noise, stationary=True, prop_decrease=0.92, n_fft=2048)
y = nr.reduce_noise(y=y, sr=sr, stationary=False, prop_decrease=0.6, n_fft=1024)
sf.write(sys.argv[2], y, sr, subtype="FLOAT")
