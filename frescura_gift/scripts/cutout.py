import onnxruntime as ort, numpy as np, sys
from PIL import Image
s=ort.InferenceSession(sys.argv[1],providers=['CPUExecutionProvider']); inp=s.get_inputs()[0]
for src,dst in zip(sys.argv[2::2],sys.argv[3::2]):
    im=Image.open(src).convert('RGB'); W,H=im.size
    x=np.asarray(im.resize((1024,1024),Image.BICUBIC),np.float32)/255.
    x=(x-[0.485,0.456,0.406])/[0.229,0.224,0.225]; x=x.transpose(2,0,1)[None].astype(np.float32)
    o=s.run(None,{inp.name:x})[-1][0,0]; o=1/(1+np.exp(-o))
    m=Image.fromarray((o*255).astype(np.uint8)).resize((W,H),Image.BICUBIC)
    rgba=im.copy(); rgba.putalpha(m); rgba.save(dst); print(dst)
