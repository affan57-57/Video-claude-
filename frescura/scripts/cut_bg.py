import onnxruntime as ort, numpy as np, sys
from PIL import Image
sess=ort.InferenceSession("models/birefnet/onnx/model.onnx",providers=["CPUExecutionProvider"])
inp=sess.get_inputs()[0].name
for f in sys.argv[1:]:
    im=Image.open(f).convert("RGB"); W,H=im.size
    x=np.asarray(im.resize((1024,1024),Image.BICUBIC),dtype=np.float32)/255.
    x=(x-[0.485,0.456,0.406])/[0.229,0.224,0.225]; x=x.transpose(2,0,1)[None].astype(np.float32)
    y=sess.run(None,{inp:x})[-1][0,0]; y=1/(1+np.exp(-y))
    m=Image.fromarray((y*255).astype(np.uint8)).resize((W,H),Image.BICUBIC)
    o=im.copy(); o.putalpha(m); o.save(f.rsplit(".",1)[0]+"_cut.png"); print(f)
