import sys, numpy as np, onnxruntime as ort
from PIL import Image
sess=ort.InferenceSession(sys.argv[1])
im=Image.open(sys.argv[2]).convert('RGB'); W,H=im.size
x=np.asarray(im.resize((1024,1024),Image.LANCZOS),dtype=np.float32)/255.
x=(x-0.5)/1.0; x=x.transpose(2,0,1)[None]
p=sess.run(None,{sess.get_inputs()[0].name:x})[0][0,0]
p=(p-p.min())/(p.max()-p.min())
m=Image.fromarray((p*255).astype(np.uint8)).resize((W,H),Image.LANCZOS)
m.save(sys.argv[3])
