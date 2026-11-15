import onnxruntime as ort, numpy as np, sys
from PIL import Image
sess=ort.InferenceSession(sys.argv[1]); im=Image.open(sys.argv[2]).convert('RGB'); W,H=im.size
x=np.asarray(im.resize((1024,1024),Image.BILINEAR),dtype=np.float32)/255.-0.5
y=sess.run(None,{sess.get_inputs()[0].name:x.transpose(2,0,1)[None]})[0][0,0]
y=(y-y.min())/(y.max()-y.min()); m=Image.fromarray((y*255).astype(np.uint8)).resize((W,H),Image.BILINEAR)
rgba=im.copy(); rgba.putalpha(m); rgba.save(sys.argv[3]); 
a=np.asarray(m)>128; cols=a.sum(0); print('cols with fg ranges:'); on=False
for i,c in enumerate(cols):
    if c>40 and not on: st=i; on=True
    if c<=40 and on: print(st,i); on=False
rows=a.sum(1); r=np.where(rows>20)[0]; print('rows',r.min(),r.max())
