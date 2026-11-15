import onnxruntime as ort, numpy as np, sys
from PIL import Image
sess=ort.InferenceSession(sys.argv[1],providers=['CPUExecutionProvider'])
src=Image.open(sys.argv[2]).convert('RGB')
for name,box in [('noche',(195,600,595,1660)),('glory',(555,600,955,1660))]:
    im=src.crop(box); W,H=im.size
    x=np.asarray(im.resize((1024,1024),Image.BILINEAR),dtype=np.float32)/255.
    x=(x-0.5)/1.0; x=x.transpose(2,0,1)[None]
    o=sess.run(None,{sess.get_inputs()[0].name:x})[0][0,0]
    o=(o-o.min())/(o.max()-o.min()); a=Image.fromarray((o*255).astype(np.uint8)).resize((W,H),Image.BILINEAR)
    im=im.convert('RGBA'); im.putalpha(a)
    bb=a.point(lambda v:255 if v>40 else 0).getbbox(); im=im.crop(bb)
    im.save(sys.argv[3]+f'/cut_{name}.png'); print(name,im.size)
