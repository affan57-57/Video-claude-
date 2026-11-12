import sys, numpy as np, onnxruntime as ort
from PIL import Image
sess=ort.InferenceSession(sys.argv[1]); src=sys.argv[2]; box=tuple(map(int,sys.argv[4].split(','))); out=sys.argv[3]
im=Image.open(src).convert('RGB').crop(box); W,H=im.size
x=np.asarray(im.resize((1024,1024),Image.BICUBIC),dtype=np.float32)/255.
x=(x-[0.485,0.456,0.406])/[0.229,0.224,0.225]; x=x.transpose(2,0,1)[None].astype(np.float32)
m=sess.run(None,{'input_image':x})[0][0,0]; m=1/(1+np.exp(-m))
a=Image.fromarray((m*255).astype(np.uint8)).resize((W,H),Image.BICUBIC)
rgba=im.copy(); rgba.putalpha(a); bb=a.point(lambda v:255 if v>20 else 0).getbbox(); rgba.crop(bb).save(out); print(out, bb)
