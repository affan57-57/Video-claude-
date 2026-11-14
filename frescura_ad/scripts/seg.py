import sys, numpy as np, onnxruntime as ort
from PIL import Image
s=ort.InferenceSession(sys.argv[1]); name=s.get_inputs()[0].name
for src,dst in zip(sys.argv[2::2],sys.argv[3::2]):
    im=Image.open(src).convert('RGB'); x=np.asarray(im.resize((1024,1024),Image.BILINEAR),dtype=np.float32)/255.
    x=(x-0.5)/1.0; x=x.transpose(2,0,1)[None]
    p=s.run(None,{name:x})[0][0,0]; p=(p-p.min())/(p.max()-p.min())
    mask=Image.fromarray((p*255).astype(np.uint8)).resize(im.size,Image.LANCZOS)
    im.putalpha(mask); im.save(dst); print('ok',dst)
