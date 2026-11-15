import sys, numpy as np, onnxruntime as ort
from PIL import Image, ImageFilter
model, src, dst = sys.argv[1:4]; box=tuple(int(v) for v in sys.argv[4].split(','))
im=Image.open(src).convert('RGB').crop(box)
sess=ort.InferenceSession(model, providers=['CPUExecutionProvider'])
x=np.asarray(im.resize((1024,1024),Image.BILINEAR),dtype=np.float32)/255.
x=(x-0.5)/1.0; x=x.transpose(2,0,1)[None]
m=sess.run(None,{sess.get_inputs()[0].name:x})[0][0,0]
m=(m-m.min())/(m.max()-m.min()+1e-8)
mask=Image.fromarray((m*255).astype(np.uint8)).resize(im.size,Image.BICUBIC)
out=im.copy(); out.putalpha(mask); out.save(dst); print(dst,out.size)
